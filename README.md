# 法規 RAG 問答 agent — 起始 repo（Workshop Starter）

歡迎！這是工作坊的**起始 repo**。它能跑起來，但「什麼都還不會」——
你的任務是用 AI 工具鏈把下面的 **6 個缺口**補完，最後部署上 Railway，
並用提案模板把你做的東西「提案」出來。

> 這是 `master`（起始狀態）。卡關時，完整答案在 `solution` branch：
> 看單一檔案 `git show solution:app/rag.py`，或整包對照 `git checkout solution`。

---

## 怎麼開始

```bash
python -m venv .venv && . .venv/Scripts/activate   # Windows
pip install -r requirements.txt
pytest -v      # 你會看到核心測試是「紅」的 —— 那就是你的起點
uvicorn app.main:app --reload   # 開 http://localhost:8000（介面陽春、問答還不會動）
```

---

## 缺口地圖（依難度遞增，由易到難補）

每個缺口有三層提示。**先自己試 ~10 分鐘，卡住再往下看一層**——
這是刻意的「有效掙扎」，直接看答案學不起來。

### 缺口 1 · 解析回應 `parse_response`（核心，有測試）
- 🎯 **目標**：實作 `app/rag.py` 的 `parse_response`，讓 `pytest tests/test_rag.py` 的 parse 測試通過。
- 💡 **提示**：用 brainstorming / 看 test 反推：輸入是 Responses API 回應物件，要拼出 `answer` 字串、收集去重的 `citations`（檔名）。遍歷 `response.output` → 每個 item 的 `content` → 取 `text` 與 `annotations[].filename`。
- 📖 **參考**：`git show solution:app/rag.py`

### 缺口 2 · 呼叫 file search `answer_question`（核心，有測試）
- 🎯 **目標**：實作 `app/rag.py` 的 `answer_question`，讓 test_rag.py 全綠。
- 💡 **提示**：用 **context7 MCP** 查 OpenAI Responses API 的 `file_search` tool 用法。呼叫 `client.responses.create(model=, input=, tools=[{"type":"file_search","vector_store_ids":[...]}])`，再丟給 `parse_response`。
- 📖 **參考**：`git show solution:app/rag.py`、[OpenAI file search 指南](https://developers.openai.com/api/docs/guides/tools-file-search)

### 缺口 3 · chunking 策略（研究型）
- 🎯 **目標**：決定 `scripts/ingest.py` 的 `MAX_CHUNK_SIZE_TOKENS` 與 `CHUNK_OVERLAP_TOKENS`。
- 💡 **提示**：法規 chunking 是長期被研究的領域，別套預設值。用 **context7 MCP** 研究兩件事：①OpenAI file search 的參數範圍限制、②法規/長文 RAG 社群主流作法，再對齊到 file search 的兩顆旋鈕。約束：max 100–4096、overlap ≤ max/2。
- 📖 **參考**：`git show solution:scripts/ingest.py`

### 缺口 4 · 前端美化（設計）
- 🎯 **目標**：把 `static/index.html` 從陽春聊天框變成有質感的問答介面（訊息氣泡、引用來源卡片、loading 狀態、RWD）。
- 💡 **提示**：在 brainstorming 階段用 **visual companion** 邊聊邊出 mockup，再用 **frontend-design skill** 落地成 HTML/CSS。Tailwind 走 CDN，免 build。
- 📖 **參考**：`git show solution:static/index.html`（注意：solution 也只是基準，鼓勵做得更好）

### 缺口 5 · E2E 測試（驗證）
- 🎯 **目標**：對部署後（或本地）頁面跑「問一題 → 看到答案與引用」的端對端測試。
- 💡 **提示**：用 **playwright skill** 寫測試、用 **playwright MCP** 實際操作瀏覽器點點看。
- 📖 **參考**：playwright-core / playwright-cli skill

### 缺口 6 · 錯誤監控（上線後）
- 🎯 **目標**：接入 Sentry，讓上線後的錯誤（缺 key、vector store 空、OpenAI 逾時）可被追蹤。
- 💡 **提示**：用 **sentry MCP** + sentry-sdk-setup skill 安裝 SDK，故意觸發一個錯誤，再用 sentry MCP 查到那個 issue。
- 📖 **參考**：sentry-sdk-setup skill

---

## 建立語料索引（補完缺口 2、3 後）
```bash
# 把法規語料放進 data/（每條乾淨分界、條號入檔名）
export OPENAI_API_KEY=sk-...
python scripts/ingest.py        # 完成後記下印出的 VECTOR_STORE_ID
```

## 本地啟動
```bash
export OPENAI_API_KEY=sk-... VECTOR_STORE_ID=vs_...
uvicorn app.main:app --reload
```

## 部署到 Railway（GitHub 連結式 CICD）
1. 把本 repo push 到你自己的 GitHub
2. Railway → New Project → Deploy from GitHub repo → 選此 repo
3. Variables 設定 `OPENAI_API_KEY`、`VECTOR_STORE_ID`、`OPENAI_MODEL`
4. 之後每次 push 到預設分支即自動 build & deploy
5. 用 `railway logs` 看部署日誌、`railway open` 開線上頁

> 不使用 `railway up` 本地直推；一律走 GitHub 連結，確保 CICD。
