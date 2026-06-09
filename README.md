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
