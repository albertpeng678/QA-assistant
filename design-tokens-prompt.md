# Design Tokens 生成 Prompt（frontend-design skill 專用）

> 用途：用 frontend-design skill 只做「設計決策」，一次產出一套可跨產品重用的 design tokens（網站 / AI chatbot / dashboard 共用）。
> 產出後：挑一套貼進 `globals.css`（或純 HTML 的 `index.html` 的 `:root`）當「唯一視覺真相」，之後用 ui-ux-pro-max 做版型時只消費、不重挑。

---

## Prompt（直接複製以下整段）

```
使用 Frontend Design skill，但只執行「設計決策」階段，不要產生任何頁面、元件或 layout。

# 任務
為我的個人品牌產出一套可跨產品重用的 design tokens（網站、AI chatbot、dashboard 都會共用這一套）。

# Design direction
- 風格形容詞：[填兩個，例如 calm and precise / editorial and warm]
- 主色系：navy blue（海軍藍）。primary 必須是沉穩、專業的 navy 調，不要亮藍、不要藍紫。
- 參考成熟度：對齊 Linear / Vercel / Stripe 的 SaaS 視覺慣例。克制、單一強調色、留白充足。
- 明確不要 anti-convention：這是要長期重用的品牌地基，不是一次性炫技頁。

# 硬限制（負面範例）
- 主色系固定為 navy blue。
- 整體實際運用的「主要色彩」不得超過 5 種（navy 主色 + 中性灰階 + 至多一個強調色 + 必要的語意色 success/warning/destructive 計為功能色，不灌水）。維持克制的色票。
- 不要紫色／藍紫漸層。
- 不要 Inter、Roboto、或任何已被 AI 生成濫用到爛的字體。
- 不要五彩、不要玩具感配色。

# Icon 規範（重要）
- 全面禁止使用 emoji 當作 icon 或裝飾。
- 所有 icon 必須來自「同一套」design system 的 icon library（預設指定 Lucide，shadcn 預設 icon set；若不適合可改用單一一套 outline icon family，但全專案只能用同一套）。
- 在 token 檔中加入 icon 規範註解：指定 icon library 名稱、預設 stroke width、預設尺寸 scale（例如 16 / 20 / 24），讓後續所有 icon 視覺一致。

# 輸出格式（嚴格遵守，否則無法使用）
輸出「一份可直接貼進 shadcn 的 globals.css 的 CSS variables」，用 oklch 色彩空間（shadcn v4 預設）。必須包含下列四區，缺一不可：

## 1. shadcn 語意 token（drop-in 主體，亮色 + 暗色都要）
請輸出完整的 `:root { }`（亮色）與 `.dark { }`（暗色）兩套，每套都要含這些 shadcn 標準 token：
--background / --foreground
--card / --card-foreground
--popover / --popover-foreground
--primary / --primary-foreground   （primary = navy blue）
--secondary / --secondary-foreground
--muted / --muted-foreground
--accent / --accent-foreground
--destructive / --destructive-foreground
--success / --success-foreground
--warning / --warning-foreground
--border / --input / --ring
--radius
（暗色不是把亮色變暗就好，要重新平衡對比與飽和度。）

## 2. 字體（可直接使用）
- 指定具體 Google Fonts 名稱（heading 一個、body 一個，需與 navy／專業風格相稱）。
- 附可直接貼用的 `@import url(...)`。
- 定義 `--font-heading` 與 `--font-body` 兩個 CSS 變數。

## 3. Icon 規範（以註解形式寫入 token 檔）
- 指定 icon library 名稱（預設 Lucide）。
- 定義 `--icon-stroke`（預設線寬）與 icon 尺寸 scale（如 --icon-sm / --icon-md / --icon-lg）。
- 註明：全專案禁止 emoji，icon 一律取自此單一 library。

## 4. 原始 scale（供參考與擴充）
- neutral 灰階 50–900（oklch）。
- spacing scale、border-radius scale、shadow scale（各 3–5 階即可）。

# 其他要求
- 每個關鍵決策（navy 主色選擇、強調色、字體配對、圓角程度、陰影強度、icon library）後面附「一行」理由。
- 只輸出這份 token 檔與其理由註解，不要解說、不要範例頁、不要 layout。
- 把這視為「提案」：可以的話給我 2 個方向各一套完整 token（方向 A / 方向 B），我會自己挑一套定稿。
```

---

## 跑完之後怎麼接（交接給 ui-ux-pro-max）

1. 從產出的 1～2 套提案中**挑一套**，貼進 `globals.css`（純 HTML 專案則貼進 `index.html` 的 `<style>:root{...}</style>`）。這份即「唯一視覺真相」。
2. 用 ui-ux-pro-max 做介面時，**不要跑 `--design-system` 重挑配色**，而是明確指示：
   > 「設計 token 已定於 `globals.css`，你只負責 layout 與元件結構。所有顏色／字體／圓角一律引用既有 token，禁止新增色票、禁止換字體、禁止使用 emoji，所有 icon 一律取自已指定的 icon library。」

## 本次新增的兩條規則（對照）

- **禁 emoji + 統一 icon**：所有 icon 取自單一 design-system icon library（預設 Lucide），含線寬與尺寸 scale，並寫進 token 檔當規範。
- **navy 主色 + 色彩 ≤ 5 種**：primary 固定 navy blue，主要運用色彩不超過 5 種，維持克制色票。
