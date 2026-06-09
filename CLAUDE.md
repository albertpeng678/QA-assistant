# CLAUDE.md — 工作坊起始 repo 導覽

> 這份檔案會被 Claude Code 自動讀取。學員也請先讀一遍，建立全貌。

## 這是什麼

這是一個**工作坊起始 repo（starter）**。它能跑起來，但問答功能還沒實作 ——
你的任務是用 AI 工具鏈把 6 個缺口補完，部署上 Railway，最後用提案模板把成果「提案」出來。

產品本身：一個**法規 RAG 問答 agent**，用 **OpenAI file search（託管服務）** 對法規語料做問答並附條文引用。

> ⚠️ **不要自建 RAG**（不要裝 LangChain/向量資料庫）。引擎就是 OpenAI file search 託管服務 —— 這是 3 小時做得完的關鍵。

## 整體流程（你會走的路）

1. **brainstorming** 釐清要做什麼，順手用 **visual companion + frontend-design** 出前端 mockup
2. **writing-plans** 把需求落成 `spec.md` + `plan.md`（最後會餵給提案模板）
3. 補 6 個缺口（見下）→ 跑通問答
4. 部署上 **Railway**（GitHub 連結式 CICD）
5. 用 `workshop/proposal-template.md` 吃 spec+plan → 生成 7 步提案 → 丟 Gamma

## 6 個缺口（完整三層提示卡在 README.md）

| # | 缺口 | 用哪個工具 |
|---|---|---|
| 1 | `app/rag.py` `parse_response`（核心·有測試） | 看 test 反推、brainstorming |
| 2 | `app/rag.py` `answer_question`（核心·有測試） | **context7** 查 file_search 用法 |
| 3 | `scripts/ingest.py` chunking 參數 | **context7** 研究法規 chunking |
| 4 | `static/index.html` 前端美化 | **frontend-design** + visual companion |
| 5 | E2E 測試 | **playwright** skill + MCP |
| 6 | 錯誤監控 | **sentry** MCP + sdk-setup skill |

> 起點驗證：`pytest -v` 應為 **3 紅 4 綠**。紅的就是缺口 1/2 的 TDD 目標。

## 怎麼工作（給 Claude 的指引）

- **遵循 superpowers 工作流**：實作前先 TDD（先讓失敗測試通過）、卡關用 systematic-debugging、寫完用 code review。
- **遵循 karpathy guidelines**：最小改動、不過度設計、surface 假設、定義可驗證的成功條件。
- **缺口要引導學員自己想**，不要直接把答案貼上去。優先「指方向 + 教學員用對的 skill/工具」，例如缺口 2、3 一律先用 context7 研究，而非憑記憶給 code。
- 完整答案在 `solution` branch（`git show solution:app/rag.py`），**僅作最後參考**，別一開始就看。

## 硬約束

- **部署走 GitHub 連結式 CICD**：push 到 GitHub → Railway 連結該 repo → 自動 build。**不要用 `railway up` 本地直推**。
- **Secrets 走環境變數**：`OPENAI_API_KEY`、`VECTOR_STORE_ID`、`OPENAI_MODEL` 進 Railway variables，**不要進 repo**。
- file search 的 chunking 只有兩顆旋鈕（`max_chunk_size_tokens` 100–4096、`chunk_overlap_tokens` ≤ max/2）；structure-awareness 靠**上傳前的語料前處理**。

## 常用指令

```bash
python -m venv .venv && . .venv/Scripts/activate   # Windows
pip install -r requirements.txt
pytest -v                          # 跑測試（起點 3 紅 4 綠）
uvicorn app.main:app --reload      # 本地啟動 http://localhost:8000
python scripts/ingest.py           # 建語料索引（補完缺口 2/3 後）
```
