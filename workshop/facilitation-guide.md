# 3 小時工作坊 · 帶課指南（Facilitation Guide）

> 目標：引導學員從「拿到起始 repo」→ vibe coding 補完 → 部署上線 Railway →
> 用提案模板生成 7 步提案丟 Gamma。途中完整體驗 superpowers / frontend-design /
> context7 / playwright / sentry 全套工具鏈。

---

## 教學引導原則（為什麼這樣設計）

本工作坊刻意**強引導但不手把手**，依四條教學設計實證原則：

1. **Scaffolding + Fading（鷹架漸撤）**：引導前重後輕。起始 repo 的 6 缺口按難度遞增，前面附完整三層提示，後面只給目標。
2. **Productive Struggle（有效掙扎）**：難度不全拿掉。每缺口「卡得住、卡得動」，套 **10 分鐘規則**（先自己試 10 分鐘，再看下一層提示）。
3. **Expertise Reversal（專家逆轉）**：程度不一 → 三層提示卡讓快的人跳過、慢的人有底。
4. **Assistance Dilemma + Worked Example**：節奏為「看範例 → 補一半 → 自己做」。**solution branch = worked example，master 起始 repo = completion problem。**

### 引導節奏：里程碑齊步、缺口自控
- **里程碑齊步**（講師帶全班同步）：開場 brainstorming、部署上線、用 C 生成提案。守住「完整上線」硬底線，沒人脫隊。
- **缺口自控**（學員自己掌握）：6 個缺口用三層提示卡 + 10 分鐘規則，講師只在全班普遍卡關時介入。

---

## 行前清單（請學員上課前 1 天完成）

> 寄給學員，務必勾完再來。任一項裝不起來請提前回報。

- [ ] **Claude Code** 已安裝並可開啟
- [ ] **Python 3.11+**（`python --version`）
- [ ] **Git** 已安裝、有 **GitHub 帳號**並可 SSH push（`ssh -T git@github.com` 成功）
- [ ] **Railway 帳號**（用 GitHub 登入即可）
- [ ] **OpenAI API key**（有額度，file search 首 1GB 向量儲存免費）
- [ ] 已 clone 起始 repo（`git clone … && git checkout master`）

---

## 時間表（含降級分級）

| 時段 | 內容 | 用到的工具 | 等級 |
|---|---|---|---|
| **-0:30–0:00** | **開場帶裝**：逐項確認行前清單、補裝 Railway CLI、確認 key 可用、跑 `pytest -v` 看到 3 紅 4 綠（確認起點一致） | — | 必做 |
| **0:00–0:30** | **brainstorming 齊步**：用 brainstorming 釐清要做的法規 RAG agent；同步用 **visual companion + frontend-design** 邊聊邊出前端 mockup | brainstorming, frontend-design, visual companion | 必做 |
| **0:30–0:50** | **writing-plans**：把需求落成 `spec.md` + `plan.md`（這兩份最後餵 C 模板） | writing-plans, karpathy | **必做（C 的輸入）** |
| **0:50–1:40** | **核心實作（缺口自控）**：補缺口 1/2（parse_response、answer_question，TDD 讓 test_rag 轉綠）、缺口 3（**context7 研究 chunking**）、缺口 2 用 context7 查 file search 用法 | context7, TDD, karpathy, systematic-debugging | 必做 |
| **1:40–2:00** | **前端落地 + code review**：把 mockup 套進 `static/`（缺口 4）、跑 code review | frontend-design, code-review | code review 可降級 |
| **2:00–2:35** | **部署上線（齊步）**：建語料索引 `ingest.py` → GitHub repo → Railway 連結 → CICD → **playwright 驗證**（缺口 5） | Railway CLI, playwright(skill+MCP) | **必做（最高優先）** |
| **2:35–2:50** | **錯誤監控**：接入 Sentry（缺口 6），故意觸發錯誤、用 sentry MCP 查 issue | sentry MCP | **可降級為講師 demo** |
| **2:50–3:00** | **生成提案（齊步）**：用 `proposal-template.md` 吃 spec+plan → 7 步成稿 → 丟 Gamma | C 模板, Gamma | **必做** |

---

## 降級策略（「完整上線」最優先）

時間是硬牆。趕不完時**依序砍**，永不砍主幹：

1. 先砍：**Sentry 改講師 demo**（學員看不自己做）
2. 再砍：**code review 縮短**（只看核心 rag.py）
3. 最後砍：**前端美化留半成品**（功能對、不漂亮）

**永不砍的主幹**：brainstorming → spec/plan → 核心實作 → 部署上線 → C 生成提案。
兩個終極產出（RAG agent 上線 + C 生成提案）都在主幹內。

**判斷時機**：里程碑齊步讓講師能即時看全班進度。每到里程碑點名「幾人完成」，落後過半就當場啟動降級。

---

## 缺口三層提示卡（講師對照）

學員的 README 已含完整三層卡。講師端口訣：**先指目標、再等掙扎、最後才給參考**。

| 缺口 | 難度 | 卡關常見點 | 講師介入時機 |
|---|---|---|---|
| 1 parse_response | ★ | 不會看 test 反推 | 引導「先讀測試的 assert」 |
| 2 answer_question | ★★ | 不知 file_search 怎麼呼叫 | **逼用 context7** 查，而非直接給 code |
| 3 chunking | ★★ | 想套預設值帶過 | 強調法規 chunking 是研究領域、**逼用 context7** |
| 4 前端美化 | ★★ | mockup 落地卡住 | 指向 frontend-design skill |
| 5 E2E | ★★★ | 沒寫過 playwright | 指向 playwright skill + MCP 實際點 |
| 6 sentry | ★★★ | 整合順序亂 | 指向 sentry-sdk-setup skill |

---

## 常見卡關與備援

- **OpenAI key 沒額度 / file search 報錯**：準備 1–2 把備用 key；或先用講師預建的 vector_store_id 讓學員先跑通問答，回頭再自建。
- **Railway 部署失敗**：確認走 GitHub 連結（非 `railway up`）、healthcheck `/health`、變數三個都設。`railway logs` 看日誌。
- **chunking 研究發散**：限時 10 分鐘，產出「max + overlap 兩個數字 + 一句理由」即可，別陷入論文。
- **全班大幅落後**：立即啟動降級策略，確保 2:35 前所有人「部署上線」這個里程碑達成。

---

## 講師備課檢查

- [ ] 起始 repo（master）`pytest -v` = 3 紅 4 綠
- [ ] solution branch 可 `git checkout` 對照答案
- [ ] 預建一個 vector_store 當備援
- [ ] `proposal-template.md` + `sample-output-rag-agent.md` 印出/開好
- [ ] Gamma 帳號可用
