"""建立 vector store 並以 static chunking 上傳 data/ 內所有語料檔。
用法: python scripts/ingest.py
完成後會印出 VECTOR_STORE_ID，請填入 Railway variables。
"""
import os
import sys
from pathlib import Path
from openai import OpenAI

# chunking 參數由 context7 研究法規 RAG 主流作法後決定：
# 社群甜蜜點約 512 token / overlap ~size/4；對齊 file search 的兩顆旋鈕。
MAX_CHUNK_SIZE_TOKENS = 512
CHUNK_OVERLAP_TOKENS = 128

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit("請先設定 OPENAI_API_KEY 環境變數")

    files = [p for p in DATA_DIR.iterdir() if p.is_file() and p.suffix in {".txt", ".md"}]
    if not files:
        sys.exit(f"{DATA_DIR} 內沒有 .txt/.md 語料檔")

    client = OpenAI(api_key=api_key)
    vector_store = client.vector_stores.create(name="法規語料")
    print(f"已建立 vector store: {vector_store.id}")

    streams = [open(p, "rb") for p in files]
    try:
        batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=streams,
            chunking_strategy={
                "type": "static",
                "static": {
                    "max_chunk_size_tokens": MAX_CHUNK_SIZE_TOKENS,
                    "chunk_overlap_tokens": CHUNK_OVERLAP_TOKENS,
                },
            },
        )
    finally:
        for s in streams:
            s.close()

    print(f"上傳狀態: {batch.status}")
    print(f"檔案計數: {batch.file_counts}")
    print(f"\n>>> VECTOR_STORE_ID={vector_store.id}")
    print(">>> 請填入 Railway variables 的 VECTOR_STORE_ID")

if __name__ == "__main__":
    main()
