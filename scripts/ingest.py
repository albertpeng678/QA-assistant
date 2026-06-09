"""建立 vector store 並以 static chunking 上傳 data/ 內所有語料檔。
用法: python scripts/ingest.py
完成後會印出 VECTOR_STORE_ID，請填入 Railway variables。
"""
import os
import sys
from pathlib import Path
from openai import OpenAI

# 🎯 缺口 3（研究型，無測試）：chunking 策略
# 法規 chunking 是長期被深入研究的領域（條文層級、跨條引用）。
# 請用 context7 MCP 研究：(1) OpenAI file search 的 chunking 參數與範圍限制，
# (2) 法規 / 長文 RAG 社群的主流 chunking 作法，再決定下面兩個值。
# 約束：max 介於 100–4096；overlap 須 ≤ max/2。提示見 README「缺口地圖」。
MAX_CHUNK_SIZE_TOKENS = None  # TODO: context7 研究後填入
CHUNK_OVERLAP_TOKENS = None   # TODO: context7 研究後填入

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
