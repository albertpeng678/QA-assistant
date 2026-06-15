# Design System — "Airy Glass"

> 個人品牌設計系統 · 唯一視覺真相（Single Source of Truth）
> 風格：**translucent · rounded · airy（毛玻璃透明感 / 圓潤 / 呼吸感）** · 主色：**navy blue** · 主色 ≤5 · 禁 emoji · 亮/暗雙模式 · oklch
> 用途：任何產品（網站 / AI chatbot / dashboard / 文件站）都以此為基底。**任何工具或 AI 只能「引用」本檔的 token，不得自行新增色票、換字體或用 emoji。**

---

## 0. 怎麼用這份文件（先讀這段）

這份文件是**約束**，不是靈感。它存在的目的，是讓「每次做產品都長不一樣、不像成熟 SaaS」的問題消失。

**三條鐵則（給人，也給 AI）：**

1. **只引用 token，永不寫死值。** 顏色一律用 `var(--primary)` 這類語意 token，禁止寫 `#1b2a52` 或 `oklch(...)` 的字面值在元件裡。要調整視覺，只改本檔 §2 的 token。
2. **禁止 emoji。** 所有 icon 一律取自 **Lucide**（§7）。emoji 不是 icon。
3. **主色 ≤5。** navy 主色 + 中性灰階 + 1 個品牌強調色（teal）為「主色」；success/warning/destructive 為功能色，不算入也不灌水。不得引入第 6 種裝飾色。

**交接給 AI 時，把 §11 那段貼進 prompt 或 `CLAUDE.md`。**

---

## 1. 設計原則（Personality）

> 本系統的人格由三個核心感受構成：**透明（Translucency）+ 圓潤（Roundness）+ 呼吸（Breathing）**，再以**可信（Trustworthy）**收束。依據 Apple HIG（Materials / Liquid Glass）、Material Design、Microsoft Fluent、NN/g、WCAG，以及曲線偏好的神經科學研究（Bar & Neta；嬰兒圖式 PNAS）。

| 原則 | 白話 | 落地做法（含依據） |
|---|---|---|
| **Translucency（透明分層）** | 半透明是**層級語言，不是裝飾**——讓 UI 漂浮、聚焦、有空間深度 | 毛玻璃**只用在功能層**（app bar、composer、浮層、來源卡、chips）；**內容與條文坐實色、高對比面板**；對比 ≥4.5:1；**單層、小面積、不堆疊**（永不 glass-on-glass）；提供 `prefers-reduced-transparency` fallback 退實色（Apple/Fluent/NN/g） |
| **Roundness（圓潤柔和）** | 圓角=安全（不觸發杏仁核威脅感）+ 友善（嬰兒圖式獎賞迴路） | 用語意化 radius scale（§5）；**嵌套同心：外半徑 = 內半徑 + padding**；主體用**微-中圓（12–20px）**，關鍵容器追求 squircle 連續曲率（corner-smoothing ≈ 60%）；直角只留給高密度資料區（Material Shape / Apple HIG / Cloud Four） |
| **Breathing（呼吸從容）** | 慷慨留白=精緻、從容、可信；雜亂=疲勞、不信任 | **8pt 節拍**（§4），間距只取自 scale；**群組間距 > 群組內間距**（接近律）；body **行高 1.5×、段距 2×、CJK 欄寬 ≤40 字**；**先給過量留白再回收**（WCAG 1.4.12 / Material / Carbon / Refactoring UI / NN/g） |
| **Trustworthy（可信可查）** | 給的是「可被查證」的資訊，且永遠讀得清楚 | 引用、來源、狀態都明確可見（§12）；對比達 WCAG AA（§9）；玻璃再美也不犧牲可讀——內容清晰優先於背景花俏 |

**一句話定調：** 漂浮的霧面玻璃 + 柔潤圓角 + 從容留白 = 輕盈、現代、可信的工具。

> **與舊版差異**：本系統原為「editorial 出版人格（暖紙白 + 高對比襯線）」，已調整為「透明・圓潤・呼吸」。連帶建議：§5 圓角採較大尺度（見該節）；§3 標題字可由高對比襯線（Fraunces）改為更柔潤的人文 sans（如 Hanken Grotesk / Spline Sans 粗體）以呼應圓潤感——若採用請同步更新 §3。

---

## 2. 色彩系統（Color）

### 2.1 結構：語意配對（semantic pairs）

每個「表面色」都有一個對應的「其上文字色」。元件永遠成對使用，對比即有保證。

| Token | 用途 | 配對前景 |
|---|---|---|
| `--background` / `--foreground` | 全站底色 / 主文字 | — |
| `--card` / `--card-foreground` | 卡片、浮起表面 | — |
| `--popover` / `--popover-foreground` | 下拉、彈出層 | — |
| `--primary` / `--primary-foreground` | **navy 主色**：主要按鈕、連結、強調 | — |
| `--secondary` / `--secondary-foreground` | 次要按鈕、次要表面 | — |
| `--muted` / `--muted-foreground` | 低調背景 / 輔助文字 | — |
| `--accent` / `--accent-foreground` | **互動染色面**（hover、選取、active），非品牌色 | — |
| `--brand-accent` / `--brand-accent-foreground` | **唯一品牌強調色（teal）**：CTA 點綴、引用角標、重點數據 | — |
| `--destructive` / `--destructive-foreground` | 危險、刪除、錯誤（功能色） | — |
| `--success` / `--success-foreground` | 成功、通過（功能色） | — |
| `--warning` / `--warning-foreground` | 警告、待處理（功能色） | — |
| `--border` | 邊框、分隔線 | — |
| `--input` | 輸入框邊框 | — |
| `--ring` | focus 外框（鍵盤可見） | — |

> **`--accent` vs `--brand-accent` 的關鍵差異**：`--accent` 是 shadcn 既有 token，語意是「hover/選取時的微染色背景」，必須夠淡。品牌強調色（teal）若塞進 `--accent` 會破壞所有元件的 hover 行為。所以品牌色獨立成 `--brand-accent`，**用得克制**（一個畫面通常只出現一兩次）。

### 2.2 Token 值（亮色 `:root`）

```
--background:            oklch(0.992 0.004 95)    /* 暖紙白，非冷螢幕白 */
--foreground:            oklch(0.225 0.018 262)   /* 墨黑帶 navy，呼應襯線油墨感 */
--card:                  oklch(1 0 0)
--card-foreground:       oklch(0.225 0.018 262)
--popover:               oklch(1 0 0)
--popover-foreground:    oklch(0.225 0.018 262)
--primary:               oklch(0.325 0.10 262)    /* navy（略帶 indigo 深度）= 自信沉穩 */
--primary-foreground:    oklch(0.99 0.004 95)
--secondary:             oklch(0.96 0.006 90)
--secondary-foreground:  oklch(0.29 0.04 262)
--muted:                 oklch(0.96 0.006 90)
--muted-foreground:      oklch(0.51 0.018 262)
--accent:                oklch(0.945 0.012 200)
--accent-foreground:     oklch(0.29 0.04 262)
--brand-accent:          oklch(0.665 0.105 200)   /* 沉穩 teal，navy 鄰近冷色 → 內斂不衝突 */
--brand-accent-foreground: oklch(0.99 0.004 200)
--destructive:           oklch(0.55 0.205 27)
--destructive-foreground:oklch(0.99 0.003 95)
--success:               oklch(0.59 0.12 155)
--success-foreground:    oklch(0.99 0.003 95)
--warning:               oklch(0.77 0.14 75)
--warning-foreground:    oklch(0.25 0.03 75)
--border:                oklch(0.915 0.007 90)
--input:                 oklch(0.915 0.007 90)
--ring:                  oklch(0.325 0.10 262)
--radius:                0.375rem
```

### 2.3 Token 值（暗色 `.dark` — 重新平衡，非單純調暗）

```
--background:            oklch(0.20 0.018 262)    /* 深墨藍底，維持油墨氣質 */
--foreground:            oklch(0.955 0.005 90)
--card:                  oklch(0.232 0.018 262)
--card-foreground:       oklch(0.955 0.005 90)
--popover:               oklch(0.232 0.018 262)
--popover-foreground:    oklch(0.955 0.005 90)
--primary:               oklch(0.69 0.105 262)    /* 提亮 navy-indigo，深底上才跳得出 */
--primary-foreground:    oklch(0.20 0.018 262)
--secondary:             oklch(0.275 0.02 262)
--secondary-foreground:  oklch(0.955 0.005 90)
--muted:                 oklch(0.275 0.02 262)
--muted-foreground:      oklch(0.685 0.02 262)
--accent:                oklch(0.295 0.025 262)
--accent-foreground:     oklch(0.955 0.005 90)
--brand-accent:          oklch(0.72 0.10 200)
--brand-accent-foreground: oklch(0.19 0.02 200)
--destructive:           oklch(0.62 0.19 27)
--destructive-foreground:oklch(0.98 0.003 95)
--success:               oklch(0.65 0.125 155)
--success-foreground:    oklch(0.19 0.02 155)
--warning:               oklch(0.80 0.135 75)
--warning-foreground:    oklch(0.23 0.03 75)
--border:                oklch(0.295 0.02 262)
--input:                 oklch(0.315 0.02 262)
--ring:                  oklch(0.69 0.105 262)
--radius:                0.375rem
```

### 2.4 中性灰階（原始 scale，供擴充）

暖灰、與紙白同色溫。用於需要精細灰階層次時；日常請優先用語意 token。

```
--neutral-50:  oklch(0.985 0.004 90)
--neutral-100: oklch(0.96 0.006 90)
--neutral-200: oklch(0.915 0.007 90)
--neutral-300: oklch(0.855 0.009 88)
--neutral-400: oklch(0.695 0.013 86)
--neutral-500: oklch(0.55 0.016 84)
--neutral-600: oklch(0.44 0.018 80)
--neutral-700: oklch(0.35 0.018 262)
--neutral-800: oklch(0.27 0.018 262)
--neutral-900: oklch(0.225 0.018 262)
```

### 2.5 使用規則

- **主色 navy 用在**：主要按鈕、連結、focus ring、選中態、品牌標誌。不要整片背景刷 navy（它是強調，不是底）。
- **brand-accent（teal）用在**：引用角標、單一最重要的 CTA、重點數據/圖表線。**一個畫面出現次數 ≤2**，過量就失去強調力。
- **大面積請用** `--background` / `--card` / `--muted`，靠明度與留白分層，而非顏色。
- **文字層級**：主文字 `--foreground` → 輔助 `--muted-foreground` → 禁用/佔位再更淡。不要用純黑 `#000`。
- **功能色只表達狀態**，不拿來當裝飾或品牌色。

---

## 3. 字體系統（Typography）

### 3.1 字型

```
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&family=Spline+Sans:wght@400;500;600&display=swap');

--font-heading: 'Fraunces', Georgia, serif;     /* 標題：高對比襯線，編輯人格 */
--font-body:    'Spline Sans', system-ui, sans-serif; /* 內文：現代中性無襯線 */
```

- **Fraunces 只用於標題 / 大型展示文字**（h1–h4、hero、引言）。它有 optical sizing，越大越有戲。
- **Spline Sans 用於所有內文、UI 文字、按鈕、標籤、數據**。
- 絕不使用 Inter / Roboto / Arial / 系統預設當主字體。

### 3.2 字級階梯（Type Scale）

模組化比例（約 major third 1.25），base = 16px。

| 角色 | size | line-height | weight | letter-spacing | 字型 |
|---|---|---|---|---|---|
| Display | 3rem / 48px | 1.1 | 600 | -0.02em | Fraunces |
| H1 | 2.25rem / 36px | 1.15 | 600 | -0.015em | Fraunces |
| H2 | 1.75rem / 28px | 1.2 | 600 | -0.01em | Fraunces |
| H3 | 1.375rem / 22px | 1.3 | 500 | -0.005em | Fraunces |
| H4 | 1.125rem / 18px | 1.4 | 600 | 0 | Spline Sans |
| Body-lg | 1.125rem / 18px | 1.6 | 400 | 0 | Spline Sans |
| Body | 1rem / 16px | 1.6 | 400 | 0 | Spline Sans |
| Body-sm | 0.875rem / 14px | 1.55 | 400 | 0 | Spline Sans |
| Caption | 0.75rem / 12px | 1.4 | 400 | 0 | Spline Sans |
| Overline | 0.6875rem / 11px | 1.3 | 500 | 0.08em（大寫） | Spline Sans |

```
--text-display: 3rem;     --text-h1: 2.25rem;  --text-h2: 1.75rem;
--text-h3: 1.375rem;      --text-h4: 1.125rem; --text-body-lg: 1.125rem;
--text-body: 1rem;        --text-sm: 0.875rem; --text-caption: 0.75rem;
--text-overline: 0.6875rem;
--weight-regular: 400;    --weight-medium: 500; --weight-semibold: 600;
--leading-tight: 1.15;    --leading-snug: 1.3;  --leading-normal: 1.6;
```

### 3.3 排版規則

- 長文內容欄寬 **≤ 70 字元**（約 65ch），用 `--container-prose`（§8）。
- 標題與內文之間至少 `--space-3`；段落間 `--space-4`。
- 數字若需對齊（表格、數據），用 `font-variant-numeric: tabular-nums`。
- 不要全大寫整句長文；大寫只用於 Overline 標籤。

---

## 4. 間距系統（Spacing）

4px 基準網格。所有 margin / padding / gap 只能取自此階梯。

```
--space-0: 0;      --space-1: 0.25rem;  /* 4  */  --space-2: 0.5rem;  /* 8  */
--space-3: 0.75rem;/* 12 */ --space-4: 1rem;     /* 16 */  --space-5: 1.25rem; /* 20 */
--space-6: 1.5rem; /* 24 */ --space-8: 2rem;     /* 32 */  --space-10: 2.5rem; /* 40 */
--space-12: 3rem;  /* 48 */ --space-16: 4rem;    /* 64 */  --space-20: 5rem;   /* 80 */
--space-24: 6rem;  /* 96 */
```

**節奏建議**：元件內間距用 1–4；元件之間用 4–8；區塊（section）之間用 12–24。寧可留白多一點——editorial 風格的質感大半來自空間。

---

## 5. 圓角（Radius）

偏緊的圓角，呼應印刷/編輯的銳利。

```
--radius-sm: 0.1875rem; /* 3px  — badge、小標籤 */
--radius-md: 0.375rem;  /* 6px  — 預設：按鈕、輸入框、卡片 (= --radius) */
--radius-lg: 0.625rem;  /* 10px — 大卡片、彈出層 */
--radius-xl: 1rem;      /* 16px — 對話框、大型容器 */
--radius-full: 9999px;  /* 膠囊：chips、頭像、純圓 */
```

---

## 6. 陰影 / 層級（Elevation）

暖色調、低擴散，營造紙感而非戲劇性浮空。

```
--shadow-xs: 0 1px 2px oklch(0.225 0.018 262 / 0.06);
--shadow-sm: 0 1px 3px oklch(0.225 0.018 262 / 0.08), 0 1px 2px oklch(0.225 0.018 262 / 0.06);
--shadow-md: 0 4px 14px oklch(0.225 0.018 262 / 0.09);
--shadow-lg: 0 14px 36px oklch(0.225 0.018 262 / 0.13);
--shadow-xl: 0 24px 56px oklch(0.225 0.018 262 / 0.16);
```

**層級語意**：卡片靜止 `xs`–`sm`；hover 抬升一階；下拉/popover `md`；對話框/抽屜 `lg`–`xl`。暗色模式下陰影效果弱，改用 `--border` 與 `--card` 明度差分層。

---

## 7. Icon 規範（Iconography）

- **唯一 icon library：Lucide**（https://lucide.dev）。shadcn 預設，outline 風格與本系統一致。
- **全面禁止 emoji** 當 icon 或裝飾。emoji 破壞一致性、跨平台渲染不一。
- 規格：

```
--icon-stroke: 1.5;   /* 線寬，呼應襯線的細緻筆畫；標題旁的 icon 可用 1.75 */
--icon-sm: 16px;      /* 內文中、密集 UI */
--icon-md: 20px;      /* 預設：按鈕、列表項 */
--icon-lg: 24px;      /* 標題、空狀態 */
```

- icon 顏色跟隨文字（`currentColor`）；強調時才用 `--primary` 或 `--brand-accent`。
- icon 與文字並排時，垂直置中、間距 `--space-2`。
- 同一概念全站固定同一個 icon（例如「來源」永遠 `book-marked`、「送出」永遠 `arrow-up`）。

**常用對照**（建議固定）：送出=`arrow-up`／停止=`square`／複製=`copy`／來源=`book-marked`／法規=`scale`／搜尋=`search`／成功=`check-circle-2`／警告=`triangle-alert`／錯誤=`circle-x`／載入=`loader-circle`。

---

## 8. 版面與斷點（Layout）

```
--container-prose: 45rem;  /* 720px — 長文、聊天對話區（單欄好讀） */
--container-app:   75rem;  /* 1200px — 應用主框 */
--container-wide:  90rem;  /* 1440px — 寬版 dashboard */

/* 斷點 */
--bp-sm: 640px;  --bp-md: 768px;  --bp-lg: 1024px;  --bp-xl: 1280px;
```

- 內容置中，兩側留白；行動裝置滿版並保留 `--space-4` 邊距。
- 對話/問答介面內容欄固定 `--container-prose`，輸入框置中對齊同寬。

---

## 9. 無障礙（Accessibility）

- **對比**：正文對背景 ≥ 4.5:1；大型文字/UI 元件 ≥ 3:1（本 token 已按此校準，改值後需複驗）。
- **Focus**：所有可聚焦元件顯示 `--ring` 外框（`outline: 2px solid var(--ring); outline-offset: 2px`）。不可移除 focus 樣式。
- **點擊區**：互動目標 ≥ 44×44px（行動裝置）。
- **不單靠顏色**傳達狀態：搭配 icon、文字、形狀。
- **動態內容**（串流回覆）用 `aria-live="polite"`。
- 尊重 `prefers-reduced-motion`：關閉非必要動畫。

---

## 10. 動態（Motion）

```
--duration-fast: 120ms;   --duration-base: 180ms;   --duration-slow: 280ms;
--ease-standard: cubic-bezier(0.2, 0, 0, 1);   /* 一般進出 */
--ease-emphasis: cubic-bezier(0.3, 0, 0, 1);   /* 強調、彈出 */
```

- 克制原則：hover/狀態切換用 `fast`；元件進出用 `base`；大面積/對話框用 `slow`。
- 高影響時刻才動畫（頁面載入一次性 stagger）；避免到處微動畫造成廉價感。
- 一律包 `@media (prefers-reduced-motion: reduce) { *{animation:none!important;transition:none!important} }`。

---

## 11. 元件規格（Component Recipes）

所有元件**只引用 token**。以下為**本產品核心元件**的標準規格；**完整可選元件全集（7 大類 ~120 種）與 NN/g 選用原則見 §16 元件目錄**。挑元件先查 §16，再用本節/本檔 token 上樣式。

### Button
| 變體 | 背景 | 文字 | 邊框 | 用途 |
|---|---|---|---|---|
| Primary | `--primary` | `--primary-foreground` | 無 | 主要動作（每區塊至多 1） |
| Secondary | `--secondary` | `--secondary-foreground` | `--border` | 次要動作 |
| Ghost | 透明 | `--foreground` | 無（hover 顯 `--accent`） | 工具列、低調動作 |
| Destructive | `--destructive` | `--destructive-foreground` | 無 | 刪除/危險 |
| CTA-accent | `--brand-accent` | `--brand-accent-foreground` | 無 | **全頁唯一**最重要轉換點 |

- 尺寸：sm `padding:6px 12px;font-size:14px` ／ md（預設）`padding:8px 16px;font-size:15px` ／ lg `padding:11px 22px;font-size:16px`。
- 圓角 `--radius-md`；字重 500；icon+文字間距 `--space-2`。
- 狀態：hover 明度 ±4%；active 下沉 1px；focus 顯 `--ring`；disabled `opacity:.5; 不可點`。

### Input / Textarea
- 背景 `--background`；邊框 `--input`；圓角 `--radius-md`；padding `8px 12px`；文字 `--foreground`；佔位 `--muted-foreground`。
- focus：邊框轉 `--ring` + `outline:2px var(--ring)`。
- 錯誤態：邊框 `--destructive`，下方 caption 用 `--destructive`。

### Card
- 背景 `--card`；邊框 `--border`；圓角 `--radius-lg`；padding `--space-6`；陰影 `--shadow-sm`。
- hover（可點時）抬升至 `--shadow-md`，transition `--duration-base`。

### Badge / Chip
- Badge：`--radius-sm`，padding `2px 8px`，font 11–12px。狀態色用功能色的淡底（如 success 底 + success 文字）。
- Chip（可點，如範例提問）：`--radius-full`，邊框 `--border`，padding `5px 12px`，hover 顯 `--accent`。

### Source Card（引用來源 — 跨產品關鍵元件）
- 容器：`--card` 底、`--border` 框、`--radius-md`、padding `10px 12px`、flex gap `--space-2`。
- 左側 icon `book-marked`（`--icon-sm`，色 `--primary`）。
- 標題用 `--font-heading` 600 12px：**來源精確定位**（如「個人資料保護法 第 12 條」），不要只給檔名。
- 內文 caption `--muted-foreground`：被引用的原文片段，可展開高亮。

### Inline Citation（引用角標）
- `--brand-accent` 底、`--brand-accent-foreground` 文字、`--radius-sm`、min-width 16px、font 10px 600。
- 緊貼句末、可點擊跳至對應 Source Card。

### Chat Message
- **使用者訊息**：靠右、`--primary` 底氣泡、`--primary-foreground` 文字、`--radius-lg(+)`、max-width 78%。
- **AI 回覆**：**全寬、不加氣泡**、`--foreground` 文字、行高 1.6；上方小標（icon + 名稱，`--muted-foreground`）。
- 每則 hover 顯示動作列（複製/重生成，ghost button）。

### Composer（輸入框）
- sticky 底部、置中對齊 `--container-prose`；`--card` 底、`--input` 框、`--radius-lg`。
- textarea 自動長高；Enter 送出、Shift+Enter 換行。
- 送出鈕：`--primary` 圓鈕 + `arrow-up`；串流中換成 `square`（停止）。

---

## 12. 問答 / Chatbot 介面慣例（此產品類型常用）

做對話式產品時，除上述元件外，遵守這份慣例 checklist（違反視為 bug）：

- 內容欄置中 `--container-prose`；composer sticky 底部同寬。
- 使用者訊息右氣泡、AI 回覆全寬無氣泡（**不要把 AI 長回覆塞右側氣泡**）。
- 串流逐 token + 末端游標；首 token 前顯示「思考中／檢索中」狀態。
- 引用：inline 角標 `[1]` + Source Card（來源精確到條號）+ 可展開原文；查無來源要**明示**不可硬掰。
- 空狀態放 3–4 個範例提問 chips，不要只放灰字 placeholder。
- 自動黏底捲動；使用者上捲時暫停並出現「↓ 跳到最新」。
- 全程禁 emoji，icon 一律 Lucide。

---

## 13. 反模式（絕對不要）

- 寫死顏色/尺寸字面值（破壞單一真相）。
- 用 emoji 當 icon。
- 引入第 2、第 3 個強調色或漸層（尤其紫/藍紫漸層）。
- 用 Inter / Roboto / 系統字體當主字。
- 標題用無襯線、內文用襯線（反過來了）。
- 大面積刷 navy 當背景。
- 純黑文字、純白冷底（本系統用墨黑 + 暖紙白）。
- 到處微動畫、玩具感配色、五彩狀態點。
- AI「自由發揮」重挑配色——它只能消費本檔。

---

## 14. 可直接貼用：`globals.css`（shadcn / Tailwind v4）

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&family=Spline+Sans:wght@400;500;600&display=swap');

:root {
  --background: oklch(0.992 0.004 95);
  --foreground: oklch(0.225 0.018 262);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.225 0.018 262);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.225 0.018 262);
  --primary: oklch(0.325 0.10 262);
  --primary-foreground: oklch(0.99 0.004 95);
  --secondary: oklch(0.96 0.006 90);
  --secondary-foreground: oklch(0.29 0.04 262);
  --muted: oklch(0.96 0.006 90);
  --muted-foreground: oklch(0.51 0.018 262);
  --accent: oklch(0.945 0.012 200);
  --accent-foreground: oklch(0.29 0.04 262);
  --brand-accent: oklch(0.665 0.105 200);
  --brand-accent-foreground: oklch(0.99 0.004 200);
  --destructive: oklch(0.55 0.205 27);
  --destructive-foreground: oklch(0.99 0.003 95);
  --success: oklch(0.59 0.12 155);
  --success-foreground: oklch(0.99 0.003 95);
  --warning: oklch(0.77 0.14 75);
  --warning-foreground: oklch(0.25 0.03 75);
  --border: oklch(0.915 0.007 90);
  --input: oklch(0.915 0.007 90);
  --ring: oklch(0.325 0.10 262);
  --radius: 0.375rem;
  --font-heading: 'Fraunces', Georgia, serif;
  --font-body: 'Spline Sans', system-ui, sans-serif;
}

.dark {
  --background: oklch(0.20 0.018 262);
  --foreground: oklch(0.955 0.005 90);
  --card: oklch(0.232 0.018 262);
  --card-foreground: oklch(0.955 0.005 90);
  --popover: oklch(0.232 0.018 262);
  --popover-foreground: oklch(0.955 0.005 90);
  --primary: oklch(0.69 0.105 262);
  --primary-foreground: oklch(0.20 0.018 262);
  --secondary: oklch(0.275 0.02 262);
  --secondary-foreground: oklch(0.955 0.005 90);
  --muted: oklch(0.275 0.02 262);
  --muted-foreground: oklch(0.685 0.02 262);
  --accent: oklch(0.295 0.025 262);
  --accent-foreground: oklch(0.955 0.005 90);
  --brand-accent: oklch(0.72 0.10 200);
  --brand-accent-foreground: oklch(0.19 0.02 200);
  --destructive: oklch(0.62 0.19 27);
  --destructive-foreground: oklch(0.98 0.003 95);
  --success: oklch(0.65 0.125 155);
  --success-foreground: oklch(0.19 0.02 155);
  --warning: oklch(0.80 0.135 75);
  --warning-foreground: oklch(0.23 0.03 75);
  --border: oklch(0.295 0.02 262);
  --input: oklch(0.315 0.02 262);
  --ring: oklch(0.69 0.105 262);
  --radius: 0.375rem;
}

/* Tailwind v4：把 token 暴露成工具類（bg-primary、text-muted-foreground…） */
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-brand-accent: var(--brand-accent);
  --color-brand-accent-foreground: var(--brand-accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-success: var(--success);
  --color-success-foreground: var(--success-foreground);
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --font-sans: var(--font-body);
  --font-serif: var(--font-heading);
  --radius-sm: 0.1875rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.625rem;
  --radius-xl: 1rem;
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```

> **純 HTML + Tailwind CDN 專案**：只貼 `:root` / `.dark` 兩段到 `<style>`，元件用 `style="background:var(--primary)"` 或 `class="bg-[hsl(var(--primary))]"` 引用即可，不需 `@theme`。

---

## 15. 交接給 AI（貼進 `CLAUDE.md` 或 prompt）

```markdown
## 前端設計規則（每次做 UI 必遵守）
- 設計系統唯一真相是 `design-system.md`。做任何 UI 前先讀它。
- 顏色/字體/圓角/間距一律引用其中的 token，禁止寫死字面值、禁止新增色票。
- 字體固定 Fraunces（標題）+ Spline Sans（內文），不得更換。
- 禁止 emoji；所有 icon 一律使用 Lucide。
- 主色 navy + 中性 + 單一 teal 強調，主色 ≤5；teal 每頁用 ≤2 次。
- 用 ui-ux-pro-max 做版型時：只負責 layout 與元件結構，視覺一律引用既有 token，
  不要跑 --design-system 重挑配色。
- 對話式產品遵守 design-system.md §12 的問答介面 checklist。
```

---

## 16. 元件目錄（Component Inventory & NN/g 原則）

> 來源：以 WebSearch（NN/g 慣例）+ Context7（盤點 shadcn/Radix/MUI/Ant Design 實際元件）整理。挑元件先看本目錄與對應 NN/g 原則，再用 §2–§7 的 token 上樣式。
> 圖例：**S**=shadcn/ui · **R**=Radix · **M**=MUI · **A**=Ant Design

### 16.0 全景（~120+ 種常見元件，7 大類）

| 類別 | 元件數 | 代表元件 |
|---|---|---|
| 1 表單與輸入 | ~31 | input、select、combobox、checkbox、radio、switch、slider、date picker、file upload、OTP、rating、cascader、transfer |
| 2 導航與尋路 | ~18 | navbar、sidebar、tabs、breadcrumb、pagination、menu、command palette、stepper、bottom nav、drawer nav、anchor |
| 3 覆蓋層與漸進揭露 | ~17 | modal、alert dialog、drawer/sheet、bottom sheet、popover、tooltip、hover card、accordion、collapsible、context menu、tabs |
| 4 回饋與狀態 | ~17 | alert、banner、toast、notification、progress、spinner、skeleton、empty state、error/result page、inline validation、status badge |
| 5 資料展示 | ~22 | table/data grid、list、card、badge、tag/chip、avatar、stat/KPI、timeline、tree、description list、carousel、calendar、chart、kanban、comparison table |
| 6 操作按鈕 + 版面媒體 | ~24 | button 變體、icon button、button group、split button、toggle、FAB、grid、stack、divider、aspect ratio、scroll area、resizable、sticky、icon |
| 7 AI / 對話式 | ~23 | message bubble、thread、composer、streaming、suggestions、follow-up、inline citation、source card、reasoning、tool call、code block、actions、scroll-to-bottom、empty state |

### 16.1 表單與輸入
text input · textarea · number · password · search · select · multi-select · combobox/autocomplete · listbox · checkbox(+group) · radio group · switch · toggle group · slider · date/time/range picker · file upload · rich text · OTP · tags input · rating · color picker · cascader(A) · transfer(A) · mentions(A) · form/field · label · validation message · input addon
- 標籤放欄位上方，少用 placeholder 取代標籤（[form-design-placeholders](https://www.nngroup.com/articles/form-design-placeholders/)）
- 互斥選一→radio；可複選→checkbox；選項 ≥5→dropdown/listbox（[checkboxes-vs-radio-buttons](https://www.nngroup.com/articles/checkboxes-vs-radio-buttons/)）
- toggle 只用於即時生效的二元狀態（[toggle-switch-guidelines](https://www.nngroup.com/articles/toggle-switch-guidelines/)）

### 16.2 導航與尋路
navbar/top bar · sidebar · tabs · breadcrumb · pagination · menu/menubar · dropdown menu · context menu · mega menu · command palette(Cmd+K) · stepper/wizard · bottom nav · drawer/hamburger · link · anchor/scrollspy/TOC · tree nav · segmented control · back-to-top · utility nav · sticky header
- 導航核心是回答「我在哪裡」（高亮目前項/breadcrumb/local nav）（[navigation-you-are-here](https://www.nngroup.com/articles/navigation-you-are-here/)）
- 可發現性 > 美感：隱藏主導航使可發現性近乎減半（[menu-design](https://www.nngroup.com/articles/menu-design/)）
- 別創意化關鍵控制：漢堡用三橫線、breadcrumb 用「>」（[hamburger-menu-icon](https://www.nngroup.com/articles/hamburger-menu-icon-recognizability/)）

### 16.3 覆蓋層與漸進式揭露
modal dialog · non-modal dialog · alert/confirm dialog · drawer/side sheet · bottom sheet · popover · tooltip · info tip · hover card · accordion · collapsible · dropdown menu · context menu · tabs · expandable panel · lightbox · coach mark · inline expand(show more/less)

**漸進式揭露階梯（輕→重，挑「展示細節又不撐長畫面」用）**
1. Inline expand → 2. Tooltip/Info tip → 3. Collapsible → 4. Accordion（多個短區段、不需對照）→ 5. Tabs（少量長區段）→ 6. Expandable panel/Hover card → 7. Popover → **8. Drawer/Bottom sheet（大量細節、不離開頁面）← 法條全文用這層** → 9. Modal（必須中斷，最後手段）

- Modal 是重量級手段，能不用就不用（[modal-nonmodal-dialog](https://www.nngroup.com/articles/modal-nonmodal-dialog/)）
- 關鍵資訊不可藏在揭露層後；tooltip 只放次要說明（[tooltip-guidelines](https://www.nngroup.com/articles/tooltip-guidelines/)）
- Accordion 適合短且不需對照的內容，長內容/需看全部時避免（[accordions-on-desktop](https://www.nngroup.com/articles/accordions-on-desktop/)）

### 16.4 回饋與狀態
alert/inline · banner · toast/snackbar · notification · progress bar · circular progress · spinner · skeleton · empty state · error/error boundary · success/confirmation · inline validation · status badge · loading button · callout · result page · status tracker/steps
- 系統狀態可見性（Heuristic #1）：>1 秒操作就要回饋，連空狀態都要說明（[visibility-system-status](https://www.nngroup.com/articles/visibility-system-status/)）
- 依等待時長選載入指示：2–10 秒 spinner、整頁 skeleton、>10 秒進度條（[skeleton vs progress vs spinners](https://www.nngroup.com/videos/skeleton-screens-vs-progress-bars-vs-spinners/)）
- 關鍵訊息（尤其錯誤）絕不用會自動消失的 toast（[indicators-validations-notifications](https://www.nngroup.com/articles/indicators-validations-notifications/)）
- 錯誤訊息要人性化、可修正、非敵意（[error-message-guidelines](https://www.nngroup.com/articles/error-message-guidelines/)）

### 16.5 資料展示
table/data grid · list · card · badge · tag/chip · avatar(+group) · tooltip · stat/KPI card · timeline · tree view · description list · carousel · calendar · chart(bar/line/scatter/pie/area/gauge/heatmap/treemap/radar/funnel/sparkline) · kanban · gallery/masonry · code block · comparison table · pagination · image · skeleton
- 先想任務再選元件（找/比較/檢視/操作）（[data-tables](https://www.nngroup.com/articles/data-tables/)）
- 圖表絕大多數用 bar/line/scatter 即可（[choosing-chart-types](https://www.nngroup.com/articles/choosing-chart-types/)）
- 善用非文字視覺指示（avatar/顏色/形狀/badge）（[visual-indicators](https://www.nngroup.com/articles/visual-indicators-differentiators/)）
- 比較表命脈是「內容完整一致」，項目過多收斂到 ≤5（[comparison-tables](https://www.nngroup.com/articles/comparison-tables/)）

### 16.6 操作按鈕 + 版面媒體
**Actions**：button(primary/secondary/ghost/destructive/link) · icon button · button group · split button · toggle/toggle group · FAB · dropdown button · loading button · segmented control · back-to-top
**Layout & Media**：grid/container · stack/flex · divider/separator · spacer · aspect ratio · scroll area · resizable panels · collapsible sidebar · hero · footer · image/avatar · video player · icon set · skeleton layout · sticky/affix
- 建立視覺層級：用 scale/color/spacing 讓 primary 最突出（[visual-hierarchy](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)）
- 按鈕狀態要溝通互動（default/hover/focus/active/disabled/loading）（[button-states](https://www.nngroup.com/articles/button-states-communicate-interaction/)）
- icon 常有歧義，盡量加文字標籤（[icon-usability](https://www.nngroup.com/articles/icon-usability/)）
- 以網格＋留白組織版面（建議 8px 系統）（[using-grids](https://www.nngroup.com/articles/using-grids-in-interface-designs/)）

### 16.7 AI / 對話式
message bubble(user/AI) · thread/conversation · thread list · composer/prompt input · streaming/typing · prompt suggestions · follow-up suggestions · inline citation · source card/reference · reasoning(CoT) · tool call · code block · markdown renderer · actions(copy/regenerate/feedback) · branch picker · scroll-to-bottom · attachment · model picker · stop generation · empty state w/ examples

**現成元件庫**：assistant-ui（headless primitives）、Vercel AI Elements、shadcn.io/ai（~50 元件可複製）

**關鍵 pattern（★=RAG 引用場景特別需要）**
- 串流是社交契約，但配 scroll-to-bottom 別綁架閱讀（[response-outlining](https://www.nngroup.com/articles/response-outlining/)）
- 混合式 UI 勝過純輸入框：用 suggestions/follow-up/空狀態範例（[shapeof.ai](https://www.shapeof.ai/)）
- ★ **inline citation + source card**：行內角標(hover 出來源) + 底部書目式清單，可點擊查證（[shadcn inline-citation](https://www.shadcn.io/ai/inline-citation)）
- ★ 來源呈現方式會改變使用者信任與行為，法規場景建議「行內標記 + footer 書目」雙軌（[arxiv 2512.12207](https://arxiv.org/pdf/2512.12207)）
- ★ 能力透明 + 優雅降級：能明說「查無此條/不確定」，避免幻覺式自信（[ai-chatbots-design-guidelines](https://www.nngroup.com/articles/ai-chatbots-design-guidelines/)）

### 16.8 本產品（法規 RAG 問答）相關子集

| 用途 | 元件 | 揭露層級 |
|---|---|---|
| 對話 | message bubble、thread、markdown renderer、streaming | — |
| 輸入 | composer、stop generation、prompt suggestions、follow-up suggestions | — |
| **引用（核心）** | **inline citation（L1 hover 速覽）→ source card 摘要（L2 inline）→ 完整條文（L3 drawer/bottom sheet）** | 三層漸進揭露 |
| 狀態 | thinking/skeleton、empty state w/ examples、error/「查無條文」 | — |
| 動作 | copy、regenerate、scroll-to-bottom | — |

> 這些都以本檔 token 套樣式、Lucide icon、無 emoji。純 HTML 可參考 shadcn.io/ai 的 `Sources`/`Inline Citation` 原始碼改寫，不必引入框架。詳細規格見 §11。

---

## 17. 版本

- v1.1 — 整合 §16 元件目錄（7 大類 ~120 元件 + NN/g 選用原則，源自 `ui-component-catalog.md`）。
- v1.0 — 初版（editorial and confident / navy / teal accent）。建立於本專案，可複製到任何新產品根目錄作為 `design-system.md`。
- 改 token 後，務必複驗 §9 對比，並更新本節版本。
```
