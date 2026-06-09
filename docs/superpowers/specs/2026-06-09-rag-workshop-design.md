# RAG 工作坊設計總綱（A/B/C/D 四交付物）

- **日期**：2026-06-09
- **狀態**：設計定稿，待 user review
- **作者**：與 albertpeng 經 superpowers:brainstorming 共同產出

---

## 0. 一句話總覽

學員拿到「缺口腳手架 **A**」→ 用全套 superpowers / MCP 工具鏈把它補成「可上線的 RAG 問答 agent **B**」並部署上 Railway → 再用「通用 prompt 模板 **C**」把過程產生的 spec + plan 生成 7 步提案內容丟 Gamma；整個過程由「3 小時流程 **D**」編排，忠於 `Xchange_Mentorship - 提案簡報模板（套用面試實際案例）.pptx` 那份 7 步簡報。

### 雙終極產出（呼應原始需求）

1. 一個**上線的 RAG 問答 agent**（OpenAI file search + Railway）
2. 一份用 **C 模板**生成、可丟 Gamma 的 **7 步 PM 提案內容**

### 四份交付物與依賴順序

建置順序 **B → A → C → D**（讓前一塊的產出成為後一塊的素材）：

- **B**：參考實作（地面真相，做它時自然產生真實 spec/plan 當 C 的 fixture）
- **A**：起始 repo（= B 砍掉學員要 vibe code 的部分；缺口地圖）
- **C**：通用提案 prompt 模板（用 B 的真實 spec/plan 壓測）
- **D**：3 小時流程（有了 A/B/C 與真實耗時才能釘死）

---

## 1. 核心設計原則：缺口地圖 + 工具生命週期

A 不是「砍一個半成品」，而是「設計一張缺口地圖，每個缺口剛好指向一個 skill/MCP」。學員把缺口補完 = 自然用過全套工具 = 產品上線。

### 1.1 工具 ↔ 缺口對應表（靜態腳手架）

| 工具 | 在哪一刻被用到 | A 要留的「缺口」 |
|---|---|---|
| superpowers: brainstorming | 開場釐清做什麼產品 | （流程性，不需缺口） |
| superpowers: writing-plans | brainstorm 後出 spec/plan | 無 ingest 邏輯 → 逼先規劃 |
| karpathy-guidelines | 整個 coding 過程 | 核心函式留空 → 寫時套用 |
| frontend-design + visual companion | brainstorming 階段產 mockup | `static/index.html` 只給陽春版 → 逼美化 |
| context7 MCP | 查 file search 參數 + 法規 chunking 研究 | ingest 的 chunking 參數留 TODO → 逼研究 |
| playwright skill + MCP | 部署後驗證問答流程 | 無測試 → 逼寫 E2E + MCP 實際點 |
| sentry MCP | 上線後錯誤監控 | 無 Sentry 整合 → 逼接入、查 issue |

### 1.2 superpowers skill 生命週期（動態工作流）

| 階段 | 觸發的 skill |
|---|---|
| 釐清做什麼 | brainstorming（貫穿全程） |
| 落成規劃 | writing-plans |
| 開始實作前 | test-driven-development |
| 寫 code 時 | karpathy-guidelines（surgical、別過度複雜） |
| 卡關除錯 | systematic-debugging |
| 寫完一塊 | requesting-code-review / receiving-code-review |
| 宣稱完成前 | verification-before-completion |
| 收尾整合 | finishing-a-development-branch |

---

## 2. 教學引導設計（強引導但不手把手）

依教學設計實證理論（見參考來源），把「引導性強化」落地為四條原則：

1. **Scaffolding + Fading（鷹架漸撤）**：引導前重後輕。A 的七個缺口按**難度遞增排序**，前面的洞附完整提示，後面的洞只給目標。
2. **Productive Struggle（有效掙扎）**：難度不全拿掉。每個缺口「卡得住、但卡得動」，明訂「先自己試 10 分鐘再看下一層提示」。
3. **Expertise Reversal Effect（專家逆轉效應）**：學員程度不一 → 引導**分層**，基礎提示人人看、進階學員可跳過。
4. **Assistance Dilemma + Worked Example**：節奏為 worked example（看範例）→ completion problem（補一半）→ 自己做。**B 就是 worked example，A 就是 completion problem。**

### 2.1 缺口的「三層提示卡」格式（A 的每個缺口都用）

```
🎯 目標   ：（人人看）這個缺口要達成什麼
💡 提示   ：（卡住 10 分鐘再看）該用哪個工具/skill、方向是什麼
📖 參考   ：（最後才看）B 對應段落 / 官方文件連結
```

### 2.2 接手機制：混合制（里程碑齊步、缺口自控）

| 範圍 | 引導方式 | 為什麼 |
|---|---|---|
| 關鍵里程碑（brainstorming 開場、部署上線、C 生成提案） | 講師齊步 | 守住「完整上線」硬底線，沒人脫隊 |
| 各段內部的七個缺口 | 三層提示卡、學員自控 | 保留 productive struggle 與 fading |

理由：3 小時是硬牆 + 「完整上線」最優先 → 純自控節奏會長尾失控（快的人早做完、慢的人卡死沒上線）。混合制 = 在「不能有人沒上線」的護欄內，給學員最大自主掙扎空間。

---

## 3. B — 參考用 RAG 問答 agent

### 3.1 架構：單一 FastAPI 服務 + 靜態前端

收斂成單一服務（非前後端兩個服務），理由：一個 repo、一個 Railway service、一次 GitHub CICD，3 小時最穩。

- `GET /` → serve `static/index.html`（brainstorming 階段用 frontend-design 產的成品；Tailwind CDN，免 build step）
- `POST /api/ask` → 呼叫 OpenAI **Responses API** 的 `file_search` tool（帶 `vector_store_id`）→ 回傳答案 + citations（annotations → 條號 / 檔名）
- `GET /health` → Railway healthcheck

### 3.2 語料 & chunking：法規 / 官方法令

- `scripts/ingest.py`：建 vector store → static chunking 上傳整理好的法規檔 → 印出 `vector_store_id`
- **chunking 參數決策由 context7 研究驅動**（教學橋段：研究領域理想 → 對齊 file search 的旋鈕）
- 研究結論（context7 + web search + 官方）：
  - file search 是**託管服務**，只提供兩顆旋鈕：`max_chunk_size_tokens`（100–4096，預設 800）、`chunk_overlap_tokens`（預設 400，須 ≤ size/2）+ 檢索端 `ranking_options.score_threshold`
  - 社群對法規 chunking 主流：structure-aware 遞迴切分、目標約 400–512 token / overlap ~50；2026/02 benchmark recursive 512-token 居首
  - **映射作法**：`max_chunk_size_tokens≈512`、`chunk_overlap_tokens≈128`（≈size/4，安全 ≤ size/2），勝過預設 800/400 對法條精準檢索
  - structure-awareness 移到**前處理**：上傳前把語料整理成「每條乾淨分界」，條號寫進**檔名 / file attributes**（file search 支援 per-file metadata 過濾）
- 計費：vector store 首 1GB 免費，之後 $0.10/GB/天 → 教學成本近乎零

### 3.3 部署：GitHub 連結式 CICD

- `OPENAI_API_KEY` / `VECTOR_STORE_ID` 走 **Railway variables**（不進 repo）
- 學員建 GitHub repo → push → Railway 連結該 repo → 之後每次 push 自動 build & deploy
- **不本地直推**（不用 `railway up`）；Railway CLI 給講師 / Claude 協助：`railway login` / `link` / `variables --set` / `logs` / `open`

### 3.4 資料流

使用者問 → `/api/ask` → Responses API（`file_search`, `vector_store_ids`）→ 取 output text + annotations → 前端顯示答案與引用來源

---

## 4. A — 學員起始 repo 腳手架

### 4.1 分寸：骨架齊全、核心留空

骨架齊全到「能跑起來但什麼都不會」；七個工具各對應一個刻意留空的洞。

- **留**：目錄結構、`requirements.txt`、Railway 設定檔（`railway.json` / `Procfile`）、空 FastAPI 殼、陽春 `static/index.html`、語料原始檔、README（任務說明 + 缺口清單 + 三層提示卡）
- **砍**：file search 呼叫邏輯、ingest 的 chunking 參數、前端美化、E2E 測試、Sentry 整合

### 4.2 缺口排序（難度遞增，呼應 fading）

缺口在 README 內按難度遞增排列，前面附完整三層提示，後面只給目標層。實作環節全程套 §1.2 的 superpowers skill 生命週期。

---

## 5. C — 通用套用生成模板

### 5.1 形態：一份結構化 prompt 模板文件

不是 skill（簡單、便於攜帶、任何 LLM 都能用）。學員把 spec.md + plan.md 貼進去，連同模板丟給 LLM，吐出 7 步逐頁內容。**通用** —— RAG agent 只是第一個範例，模板不可寫死成只服務 RAG agent。

### 5.2 內部結構

```
# PM 提案生成模板

## 使用方式
把你的 spec.md + plan.md 貼在 <輸入文件> 之間，連同本模板丟給 LLM。

## 輸入
<輸入文件>
{學員貼 spec + plan}
</輸入文件>

## 生成指令
針對下方 7 個 STEP，逐一產出可直接貼進 Gamma 的逐頁內容。

### STEP N · {環節名}
- 核心問句：{簡報的 CORE QUESTION}
- 填空骨架：{簡報的 YOUR ANSWER 骨架}
- 抽取規則：{告訴 LLM 去 spec/plan 哪裡找這步的素材}
- 104 few-shot 範例：{簡報該步的右欄 104 範例，當示範}
- 輸出格式：{一頁簡報的標題 + 重點 bullet}
```

### 5.3 7 步對應（來自簡報）

| STEP | 環節 | 核心問句 |
|---|---|---|
| 1 | NORTH STAR 北極星 | 靠什麼單一指標衡量核心價值 |
| 2 | BOTTLENECK 可優化處 | 北極星卡在哪、證據、為何值得解 |
| 3 | USER NEEDS 使用者端 | 誰 / 情境 / 痛點 → User Story |
| 4 | SUCCESS 成功定義 | 解了什麼才算成功（不放數字） |
| 5 | MECHANISM 機制 | 功能如何推動北極星、怎麼歸因 |
| 6 | SOLUTION 解方展現 | 流程 / 畫面 / 競品差異 |
| 7 | VALIDATION 驗證 | 兩層指標體系 + 護欄 |

### 5.4 輸出成品度

**可直接丟 Gamma 的成稿**：每頁標題 + 完整 bullet，填好填滿。LLM 從 spec/plan 抽不到的地方明確標註「需補充」。**104 範例當 few-shot 寫進每步**（LLM 看例子學格式與語氣）。

---

## 6. D — 3 小時工作坊流程

### 6.1 學員起點

**課堂前 30 分鐘帶裝環境**（不佔正式 3 小時）：Claude Code、Railway CLI、GitHub 帳號、OpenAI API key、Python。另發一份「行前清單」。

### 6.2 時間架構（含降級分級）

| 時段 | 內容 | 用到的工具 | 等級 |
|---|---|---|---|
| -0:30–0:00 | 行前帶裝 | — | 必做 |
| 0:00–0:30 | brainstorming + visual companion / frontend-design 產 mockup | brainstorming, frontend-design, visual companion | 必做 |
| 0:30–0:50 | writing-plans 出 spec + plan | writing-plans, karpathy | **必做（C 的輸入）** |
| 0:50–1:40 | 核心實作：file search 呼叫 + ingest（context7 研究 chunking）+ TDD | context7, TDD, karpathy, systematic-debugging | 必做 |
| 1:40–2:00 | mockup 套進 static + code review | frontend-design, code-review | code review 可降級 |
| 2:00–2:35 | Railway 部署上線 + playwright 驗證 | Railway CLI, playwright(skill+MCP) | **必做（最高優先）** |
| 2:35–2:50 | sentry 接入 | sentry MCP | **可降級為講師 demo** |
| 2:50–3:00 | 用 C 生成提案丟 Gamma | C 模板, Gamma | **必做** |

### 6.3 降級策略（「完整上線」最優先）

趕不完時依序砍：① sentry 改講師 demo → ② code review 縮短 → ③ frontend 美化留半成品。

**永不砍的主幹**：brainstorming → spec/plan → 實作 → 部署上線 → C 生成提案。兩個終極產出（RAG agent 上線 + C 生成提案）都在「必做」內。

### 6.4 引導節奏

里程碑齊步（開場、部署、C 生成）、缺口自控（三層提示卡 + 10 分鐘規則）。主幹齊步讓講師能即時看到全班進度，當場決定是否降級。

---

## 7. 參考來源

### 技術
- [OpenAI file search guide](https://developers.openai.com/api/docs/guides/tools-file-search)
- [OpenAI vector stores chunking](https://developers.openai.com/api/docs/api-reference/vector-stores)
- 法規 chunking 社群實務：[Legal RAG retrieval](https://arxiv.org/html/2510.06999v1)、[Weaviate chunking strategies](https://weaviate.io/blog/chunking-strategies-for-rag)

### 教學設計
- [Instructional scaffolding (Wikipedia)](https://en.wikipedia.org/wiki/Instructional_scaffolding)
- [Fading distributed scaffolds (NIH)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6519686/)
- [Expertise reversal effect (Springer)](https://link.springer.com/article/10.1007/s11251-009-9102-0)
- [Worked examples & assistance dilemma (Springer)](https://link.springer.com/article/10.1007/s11251-009-9107-8)

### 素材
- `Xchange_Mentorship - 提案簡報模板（套用面試實際案例）.pptx`（7 步 PM 提案模板，C 的 few-shot 來源）
