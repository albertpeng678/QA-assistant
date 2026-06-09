# B — 參考用 RAG 問答 agent 實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建一個單一 FastAPI 服務，透過 OpenAI Responses API 的 file_search tool 對法規語料做 RAG 問答（含引用來源），並可經 GitHub 連結部署上 Railway。

**Architecture:** 單一 FastAPI 服務同時 serve 靜態前端與 API。RAG 邏輯封裝在 `app/rag.py`，OpenAI client 以參數注入，回應解析（answer + citations）抽成純函式以便單元測試免打真 API。語料以 `scripts/ingest.py` 一次性建 vector store（static chunking 512/128），`vector_store_id` 與 API key 走 Railway variables。

**Tech Stack:** Python 3.11、FastAPI、uvicorn、openai (Python SDK)、pytest、httpx (TestClient)、Tailwind CDN（前端免 build）。

---

## File Structure

| 檔案 | 職責 |
|---|---|
| `app/__init__.py` | package marker |
| `app/config.py` | 讀環境變數（`OPENAI_API_KEY`, `VECTOR_STORE_ID`, `OPENAI_MODEL`） |
| `app/rag.py` | `parse_response()` 純函式 + `answer_question()` 呼叫 file_search |
| `app/main.py` | FastAPI app：`GET /health`、`GET /`、`POST /api/ask` |
| `static/index.html` | 陽春聊天 UI（Tailwind CDN；之後 frontend-design 美化） |
| `scripts/ingest.py` | 建 vector store、static chunking 上傳語料、印 `vector_store_id` |
| `data/` | 法規語料純文字檔（每條乾淨分界，條號入檔名） |
| `tests/test_rag.py` | `parse_response` 與 `answer_question`（mock client）單元測試 |
| `tests/test_main.py` | 端點測試（TestClient + 注入 fake rag） |
| `requirements.txt` | 相依套件 |
| `Procfile` / `railway.json` | Railway 啟動與部署設定 |
| `.env.example` | 環境變數範本 |
| `README.md` | 跑法、部署、ingest 說明 |

---

### Task 1: 專案骨架 + config + health 端點

**Files:**
- Create: `app/__init__.py`、`app/config.py`、`app/main.py`
- Create: `requirements.txt`
- Test: `tests/test_main.py`

- [ ] **Step 1: 寫 requirements.txt**

```
fastapi==0.115.6
uvicorn[standard]==0.34.0
openai==1.59.6
pytest==8.3.4
httpx==0.28.1
```

- [ ] **Step 2: 建立虛擬環境並安裝**

Run:
```bash
python -m venv .venv && . .venv/Scripts/activate && pip install -r requirements.txt
```
Expected: 安裝成功，無錯誤。

- [ ] **Step 3: 寫失敗測試（health 端點）**

`tests/test_main.py`:
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_returns_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
```

- [ ] **Step 4: 執行測試確認失敗**

Run: `pytest tests/test_main.py::test_health_returns_ok -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'app.main'`）

- [ ] **Step 5: 寫 config.py**

`app/config.py`:
```python
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
```

- [ ] **Step 6: 寫最小 main.py（含 health）**

`app/__init__.py`: 空檔。

`app/main.py`:
```python
from fastapi import FastAPI

app = FastAPI(title="法規 RAG 問答")

@app.get("/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 7: 執行測試確認通過**

Run: `pytest tests/test_main.py::test_health_returns_ok -v`
Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add app requirements.txt tests/test_main.py
git commit -m "feat: FastAPI 骨架與 health 端點"
```

---

### Task 2: RAG 回應解析純函式 `parse_response`

把 Responses API 回傳物件解析成 `{"answer": str, "citations": [str]}`。設計成純函式，用假物件測試，免打真 API。

**Files:**
- Create: `app/rag.py`
- Test: `tests/test_rag.py`

- [ ] **Step 1: 寫失敗測試**

`tests/test_rag.py`:
```python
from types import SimpleNamespace
from app.rag import parse_response

def _fake_response():
    annotation = SimpleNamespace(filename="勞動基準法-第24條.txt")
    content = SimpleNamespace(text="加班費依第24條計算。", annotations=[annotation])
    message = SimpleNamespace(type="message", content=[content])
    file_search_call = SimpleNamespace(type="file_search_call", content=None)
    return SimpleNamespace(output=[file_search_call, message])

def test_parse_response_extracts_answer_and_citations():
    result = parse_response(_fake_response())
    assert result["answer"] == "加班費依第24條計算。"
    assert result["citations"] == ["勞動基準法-第24條.txt"]

def test_parse_response_dedupes_and_handles_no_annotations():
    content = SimpleNamespace(text="無引用的回答。", annotations=[])
    message = SimpleNamespace(type="message", content=[content])
    result = parse_response(SimpleNamespace(output=[message]))
    assert result["answer"] == "無引用的回答。"
    assert result["citations"] == []
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `pytest tests/test_rag.py -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'app.rag'`）

- [ ] **Step 3: 寫 parse_response**

`app/rag.py`:
```python
def parse_response(response):
    """把 Responses API 回應解析為 answer 與去重後的 citations。"""
    answer_parts = []
    citations = []
    for item in response.output:
        content = getattr(item, "content", None)
        if not content:
            continue
        for part in content:
            text = getattr(part, "text", None)
            if text:
                answer_parts.append(text)
            for ann in getattr(part, "annotations", []) or []:
                filename = getattr(ann, "filename", None)
                if filename and filename not in citations:
                    citations.append(filename)
    return {"answer": "".join(answer_parts), "citations": citations}
```

- [ ] **Step 4: 執行測試確認通過**

Run: `pytest tests/test_rag.py -v`
Expected: PASS（2 passed）

- [ ] **Step 5: Commit**

```bash
git add app/rag.py tests/test_rag.py
git commit -m "feat: RAG 回應解析 parse_response"
```

---

### Task 3: `answer_question` — 呼叫 file_search（client 注入可 mock）

**Files:**
- Modify: `app/rag.py`
- Test: `tests/test_rag.py`

- [ ] **Step 1: 追加失敗測試**

於 `tests/test_rag.py` 末尾追加：
```python
from app.rag import answer_question

class _FakeResponses:
    def __init__(self, response):
        self._response = response
        self.calls = []
    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._response

class _FakeClient:
    def __init__(self, response):
        self.responses = _FakeResponses(response)

def test_answer_question_calls_file_search_with_vector_store():
    client = _FakeClient(_fake_response())
    result = answer_question(client, "加班費怎麼算?", vector_store_id="vs_123", model="gpt-4o-mini")
    assert result["answer"] == "加班費依第24條計算。"
    assert result["citations"] == ["勞動基準法-第24條.txt"]
    call = client.responses.calls[0]
    assert call["model"] == "gpt-4o-mini"
    assert call["input"] == "加班費怎麼算?"
    assert call["tools"] == [{"type": "file_search", "vector_store_ids": ["vs_123"]}]
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `pytest tests/test_rag.py::test_answer_question_calls_file_search_with_vector_store -v`
Expected: FAIL（`ImportError: cannot import name 'answer_question'`）

- [ ] **Step 3: 實作 answer_question**

於 `app/rag.py` 追加：
```python
def answer_question(client, question, *, vector_store_id, model):
    """以 file_search tool 對 vector store 提問，回傳 answer + citations。"""
    response = client.responses.create(
        model=model,
        input=question,
        tools=[{"type": "file_search", "vector_store_ids": [vector_store_id]}],
    )
    return parse_response(response)
```

- [ ] **Step 4: 執行測試確認通過**

Run: `pytest tests/test_rag.py -v`
Expected: PASS（3 passed）

- [ ] **Step 5: Commit**

```bash
git add app/rag.py tests/test_rag.py
git commit -m "feat: answer_question 呼叫 file_search"
```

---

### Task 4: `POST /api/ask` 端點（依賴注入 rag）

**Files:**
- Modify: `app/main.py`
- Test: `tests/test_main.py`

- [ ] **Step 1: 追加失敗測試（用 dependency override 注入假 rag）**

於 `tests/test_main.py` 追加：
```python
from app.main import app, get_answerer

def test_ask_returns_answer_and_citations():
    def fake_answerer(question):
        return {"answer": f"回答：{question}", "citations": ["a.txt"]}
    app.dependency_overrides[get_answerer] = lambda: fake_answerer
    try:
        resp = client.post("/api/ask", json={"question": "測試問題"})
        assert resp.status_code == 200
        assert resp.json() == {"answer": "回答：測試問題", "citations": ["a.txt"]}
    finally:
        app.dependency_overrides.clear()

def test_ask_rejects_empty_question():
    resp = client.post("/api/ask", json={"question": "  "})
    assert resp.status_code == 422
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `pytest tests/test_main.py -v`
Expected: FAIL（`ImportError: cannot import name 'get_answerer'`）

- [ ] **Step 3: 實作端點與 answerer 依賴**

改寫 `app/main.py`：
```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel, field_validator
from openai import OpenAI

from app import config
from app.rag import answer_question

app = FastAPI(title="法規 RAG 問答")

class AskRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError("question 不可為空")
        return v.strip()

def get_answerer():
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    def answerer(question: str):
        return answer_question(
            client, question,
            vector_store_id=config.VECTOR_STORE_ID,
            model=config.OPENAI_MODEL,
        )
    return answerer

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/ask")
def ask(req: AskRequest, answerer=Depends(get_answerer)):
    return answerer(req.question)
```

- [ ] **Step 4: 執行測試確認通過**

Run: `pytest tests/test_main.py -v`
Expected: PASS（health + 2 個 ask 測試）

- [ ] **Step 5: Commit**

```bash
git add app/main.py tests/test_main.py
git commit -m "feat: /api/ask 端點與依賴注入"
```

---

### Task 5: 靜態前端（陽春版）+ 掛載

陽春可用版；STEP 6 由 frontend-design 美化。

**Files:**
- Create: `static/index.html`
- Modify: `app/main.py`
- Test: `tests/test_main.py`

- [ ] **Step 1: 追加失敗測試（首頁回 HTML）**

於 `tests/test_main.py` 追加：
```python
def test_index_serves_html():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "法規 RAG" in resp.text
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `pytest tests/test_main.py::test_index_serves_html -v`
Expected: FAIL（404）

- [ ] **Step 3: 寫陽春前端**

`static/index.html`:
```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>法規 RAG 問答</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <main class="max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-4">法規 RAG 問答</h1>
    <div id="log" class="space-y-3 mb-4"></div>
    <form id="f" class="flex gap-2">
      <input id="q" class="flex-1 border rounded px-3 py-2" placeholder="輸入你的法規問題…" />
      <button class="bg-blue-600 text-white px-4 py-2 rounded">送出</button>
    </form>
  </main>
  <script>
    const log = document.getElementById("log");
    document.getElementById("f").addEventListener("submit", async (e) => {
      e.preventDefault();
      const q = document.getElementById("q").value.trim();
      if (!q) return;
      log.innerHTML += `<div class="font-medium">Q: ${q}</div>`;
      const r = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const d = await r.json();
      const cites = (d.citations || []).join("、");
      log.innerHTML += `<div class="bg-white border rounded p-3">${d.answer}${cites ? `<div class="text-xs text-gray-500 mt-2">來源：${cites}</div>` : ""}</div>`;
      document.getElementById("q").value = "";
    });
  </script>
</body>
</html>
```

- [ ] **Step 4: 掛載靜態檔並加首頁路由**

於 `app/main.py` 的 import 區追加：
```python
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
```
於 `app = FastAPI(...)` 之後追加：
```python
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")
```

- [ ] **Step 5: 執行測試確認通過**

Run: `pytest tests/test_main.py::test_index_serves_html -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add static/index.html app/main.py tests/test_main.py
git commit -m "feat: 陽春靜態前端與首頁路由"
```

---

### Task 6: ingest 腳本（建 vector store + static chunking 上傳）

不寫自動化測試（一次性腳本、需真 API）；以「乾跑印出設定」步驟驗證。

**Files:**
- Create: `scripts/ingest.py`
- Create: `data/.gitkeep`

- [ ] **Step 1: 寫 ingest.py**

`scripts/ingest.py`:
```python
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
```

- [ ] **Step 2: 建 data 目錄佔位**

```bash
mkdir -p data && touch data/.gitkeep
```

- [ ] **Step 3: 乾跑驗證（無 key 時正確報錯）**

Run: `python scripts/ingest.py`（在未設 OPENAI_API_KEY 的 shell）
Expected: 印出「請先設定 OPENAI_API_KEY 環境變數」並 exit。

- [ ] **Step 4: Commit**

```bash
git add scripts/ingest.py data/.gitkeep
git commit -m "feat: ingest 腳本（static chunking 512/128）"
```

---

### Task 7: Railway 部署設定 + .env.example + README

**Files:**
- Create: `Procfile`、`railway.json`、`.env.example`、`.gitignore`、`README.md`

- [ ] **Step 1: 寫 Procfile**

`Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

- [ ] **Step 2: 寫 railway.json（healthcheck）**

`railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": { "builder": "NIXPACKS" },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

- [ ] **Step 3: 寫 .env.example**

`.env.example`:
```
OPENAI_API_KEY=sk-...
VECTOR_STORE_ID=vs_...
OPENAI_MODEL=gpt-4o-mini
```

- [ ] **Step 4: 寫 .gitignore**

`.gitignore`:
```
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
```

- [ ] **Step 5: 寫 README.md**

`README.md`:
````markdown
# 法規 RAG 問答 agent

OpenAI file search + FastAPI，部署於 Railway。

## 本地開發
```bash
python -m venv .venv && . .venv/Scripts/activate
pip install -r requirements.txt
pytest -v                      # 跑測試
```

## 建立語料索引（一次性）
```bash
# 把法規語料放進 data/（每條乾淨分界、條號入檔名）
export OPENAI_API_KEY=sk-...
python scripts/ingest.py        # 完成後記下印出的 VECTOR_STORE_ID
```

## 本地啟動
```bash
export OPENAI_API_KEY=sk-... VECTOR_STORE_ID=vs_...
uvicorn app.main:app --reload
# 開 http://localhost:8000
```

## 部署到 Railway（GitHub 連結式 CICD）
1. 把本 repo push 到 GitHub
2. Railway → New Project → Deploy from GitHub repo → 選此 repo
3. Variables 設定 `OPENAI_API_KEY`、`VECTOR_STORE_ID`、`OPENAI_MODEL`
4. 之後每次 push 到預設分支即自動 build & deploy
5. 用 `railway logs` 看部署日誌、`railway open` 開線上頁

> 不使用 `railway up` 本地直推；一律走 GitHub 連結，確保 CICD。
````

- [ ] **Step 6: 驗證測試仍全綠**

Run: `pytest -v`
Expected: 全部 PASS。

- [ ] **Step 7: Commit**

```bash
git add Procfile railway.json .env.example .gitignore README.md
git commit -m "chore: Railway 部署設定與 README"
```

---

## Self-Review

**1. Spec coverage（對 spec §3 B）：**
- §3.1 單一 FastAPI + 靜態前端 → Task 1/4/5 ✅
- §3.1 `GET /` / `POST /api/ask` / `GET /health` → Task 1/4/5 ✅
- §3.1 file_search + citations → Task 2/3 ✅
- §3.2 ingest + static chunking 512/128 → Task 6 ✅
- §3.2 chunking 由 context7 研究驅動 → Task 6 註解標明（工作坊時學員實際做研究）✅
- §3.3 Railway variables / GitHub CICD / 不本地直推 → Task 7 ✅
- §3.4 資料流 → Task 3 + 4 串起 ✅

**2. Placeholder scan：** 無 TBD/TODO；每個 code 步驟都有完整程式碼。ingest 不寫單元測試已說明理由（一次性、需真 API）。✅

**3. Type consistency：** `parse_response(response) -> {"answer","citations"}`、`answer_question(client, question, *, vector_store_id, model)`、`get_answerer()` 回傳 `answerer(question)`、`AskRequest.question` — 跨 Task 2/3/4 命名一致。✅

> 註：本計畫是「參考實作 B」。A（起始 repo）將以此為基準，按缺口地圖砍出學員版；C/D 為文件，另行起草。
