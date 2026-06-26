# SpineSliceV2 接續傳承摘要

日期：2026-05-27  
原專案位置：`C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2`

## 一句話狀態

SpineSliceV2 已從「直接把原圖切成 source-locked layer」演化成「Lovart 式 AI 拆件圖 + Stage 1/Stage 2 分階段 + 單件迭代 + Photoshop JSX 打包」的工作流。現在重點不是追求全自動一次到位，而是把 AI 生成物變成可人工挑件、可反覆局部修正、可進 Photoshop/Spine 的素材候選流程。

## 核心原則

- 原圖是視覺權威。不要用 GPT 覆蓋已可見且 likeness-critical 的像素。
- GPT 適合補被遮擋、裁切、背側、關節銜接、衣物/肢體延伸，不適合重畫臉、眼睛、嘴巴等高相似度區域。
- Stage 1 先做大件，不追求細節拆完。
- Stage 2 在 Stage 1 候選可用後才做細拆。
- 單一部件錯了時，用單件再生，不要重跑整張 Stage 2。
- 透明 PNG 是硬要求；工具目前會嘗試自動移除 GPT 輸出的白/淺色連通背景。

## 目前工具能力

主程式：`run_v2.py`

已支援命令：

```powershell
python run_v2.py --init
python run_v2.py --new-project PROJECT
python run_v2.py --preview-annotations PROJECT --profile generic_two_stage --stage 1
python run_v2.py --make-default-annotations PROJECT --profile generic_two_stage --stage 1
python run_v2.py --slice PROJECT
python run_v2.py --contact-sheet PROJECT
python run_v2.py --stage-review PROJECT
python run_v2.py --set-stage-status PROJECT --review-status approved --review-note "..."

python run_v2.py --gpt-stage1-sheet PROJECT
python run_v2.py --gpt-stage2-sheet PROJECT
python run_v2.py --gpt-part PROJECT --part "right_leg"
python run_v2.py --gpt-revise-part PROJECT --part "right_leg" --note "..."
python run_v2.py --part-candidates PROJECT --part "right_leg"
python run_v2.py --transparentize path\to\image.png
```

本地 UI：

```powershell
python spine_ui_server.py
```

開啟：

```text
http://127.0.0.1:8765
```

UI 目前用於 Lovart 式檢查與保留/重生部件，並能產生 Photoshop JSX 打包腳本：

```text
projects/<PROJECT>/psd/import_lovart_parts.jsx
projects/<PROJECT>/psd/<PROJECT>_LovartStyle.psd
```

## Prompt 路由

目前不能用單一萬用 prompt。先分類來源圖：

1. `portrait_face`：頭像/胸像，臉、頭髮、帽子、眼鏡、鬍子、領口優先。
2. `half_action`：半身動作，手、道具、姿勢、上半身結構優先。
3. `full_action`：全身動作，四肢、武器、披風、尾巴、服裝大件優先。
4. `hybrid`：不確定時各跑一張 face/action 候選，再人工挑。

專案內可用 `stage1_mode.txt` 控制 Stage 1 prompt：

- `portrait`：使用 `prompts/stage1_portrait_face_sheet_zh.md`
- 缺省或其他值：使用 `prompts/stage1_spine_component_sheet_zh.md`

## 已驗證經驗

### Stage 1 可接受條件

- 全身/半身圖有正確大件：頭、身體、左右手臂、左右腿或可見範圍內的肢體。
- 重要道具被獨立出來，例如劍、盾、權杖、餐盤、食物、飲料、帽子、披風、尾巴、翅膀、眼鏡。
- 頭像/胸像不應腦補完整腿或腳。
- 大體比例、服裝、光影、視角可用，足以讓人手工挑件。

Stage 1 不應卡在：

- 眼睛/嘴巴角度不完美。
- 尚未拆到手肘、膝蓋、手腕、腳踝。
- 手指、鞋子、細小飾品沒有拆。
- 局部小漂移但候選仍可當作下一階段素材。

### Stage 2 已證明可用

在 `TEST_WARRIOR_SWORD`、`TEST_JAGUAR_FULL` 上，Stage 2 能把 Stage 1 大件拆成更適合 Spine 的細件：

- 手臂：上臂、前臂、手。
- 腿：大腿、小腿、腳。
- 武器、盾、腰帶、披風、羽毛、尾巴、權杖等可保留或再細拆。
- 加入「末端要圓潤實心、不要空心洞/黑洞/管口」後，關節端品質明顯改善。

### 單件迭代已通過 smoke test

測試：

```powershell
python run_v2.py --gpt-part TEST_JAGUAR_FULL --part right_leg
```

結果：

- 成功輸出單獨 right_leg，不是整張 component sheet。
- 會建立：

```text
projects/<PROJECT>/gpt_parts/<PART>/<PART>_gpt_1.png
projects/<PROJECT>/gpt_parts/<PART>/<PART>_candidates.png
projects/<PROJECT>/gpt_parts/<PART>/next_actions.md
```

這是後續最值得延伸的方向，因為它符合「只修壞掉的零件」的製作節奏。

## 已踩坑

### 3/4 臉的眼睛嘴巴會被 GPT 正面化

即使 prompt 說明保留 3/4，眼睛、嘴巴、閉眼線條仍容易變成通用正面素材。這在 `TEST_WHITEHAIR_BUST`、`TEST_HAT_BUST` 都出現。

建議：

- Stage 1 頭像/胸像先保留完整臉，不強拆五官。
- 需要表情時，再從最佳 Stage 1 頭部或臉部 close-up 做 Stage 2 face-detail pass。
- 最高保真需求下，眼睛/嘴巴仍以 source crop/manual extraction 優先。

### 不要讓頭像 prompt 補出全身

頭像/胸像 prompt 必須明說「不是全身圖，不要補完整身體、雙腿或腳」。這條很重要。

### 柔性件不能轉成背面視角

長髮、馬尾、披風、尾巴、翅膀都應維持原圖可見角度，不要讓 GPT 腦補成背面視角。

### 關節末端容易生成空洞

Stage 2 和單件 prompt 必須包含：

```text
圓潤、實心、柔和收邊的柱體端或球面端。
不要空心洞、黑洞、管口、挖空剖面或可見內壁。
```

## 重要測試樣本結論

- `TEST_WARRIOR_SWORD`：全身武器角色。大武器應明確獨立；Stage 2 適合拆四肢、劍、盾、腰帶。
- `TEST_BOXER_HALF`：半身拳擊角色。手套/拳頭/姿勢優先，臉部微件次要。
- `TEST_OLDMAN_PORTRAIT`：頭像。臉、眼鏡、眉毛、鬍子、衣領拆得好。
- `TEST_WHITEHAIR_BUST`：頭像。髮束與 collar 好，但眼嘴角度容易正面化。
- `TEST_JAGUAR_FULL`：全身獸人/部落風角色。頭飾、羽毛、披風、尾巴、權杖都應優先獨立。
- `TEST_HAT_BUST`：頭像。帽子/頭髮/衣領可用，但 Stage 1 若混太多五官細節會失焦。
- `TEST_SERVER_HALF`：半身持物角色。餐盤、食物、飲料要明確命名為重要手持道具。

## 下一步建議

1. 把「輸入圖分類」做成工具或 UI 的第一步：portrait / half_action / full_action / hybrid。
2. 讓 UI 可以設定 `stage1_mode.txt` 和 character note，不要每次手改檔。
3. 強化單件迭代：
   - 一鍵產生更多候選。
   - 一鍵 revise with note。
   - candidates sheet 顯示保留/淘汰狀態。
4. 補一個「face close-up Stage 2」流程，專門處理 3/4 臉的眼皮、閉眼、嘴型、鬍子、眼鏡。
5. 把 `next_actions.md` 的建議接進 UI，變成可點選的修正方向。
6. 若要進 production，建立人工 QA 表：
   - likeness
   - source angle
   - transparent background
   - no labels/text
   - complete overlap
   - solid rounded joint ends
   - no unwanted full-body hallucination

## 接手時先讀的檔案

```text
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\README.md
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\STAGE1_WORKFLOW.md
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\TEST_FINDINGS.md
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\SpineSliceV2_HANDOFF.md
```

## 接手時不要忘

- 不要刪或覆蓋 `SpineSliceV1`。
- 不要把 GPT 生成圖當成 source-truth。
- 對頭像/胸像，Stage 1 不要貪心拆五官。
- 對全身/半身，先把大件、道具、可動件弄對。
- 壞一個部件就修一個部件，單件迭代比重跑整張更接近實務製作。

## 2026-05-27 接續實作紀錄

已完成第一個接續項目：把輸入圖分類與 Stage 1 角色補充需求接進本地 UI。

修改檔案：

```text
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\spine_ui_server.py
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\spine_ui.html
```

新增能力：

- UI 左側新增「輸入圖分類」下拉：
  - `full_action`
  - `half_action`
  - `portrait_face`
  - `hybrid`
- UI 可編輯 `Stage 1 角色補充需求`，寫入專案的 `stage1_character_note.md`。
- 後端新增 `/api/stage1-settings`，用來保存分類與角色補充需求。
- 後端新增 `/api/generate-stage1`，會先保存設定，再呼叫 `gpt_stage1_sheet(project)`。
- 後端新增 `/api/generate-stage2`，呼叫 `gpt_stage2_sheet(project)`。
- `portrait_face` 會寫成 `stage1_mode.txt = portrait`，沿用現有 `load_stage1_template()` 的 portrait prompt 路由。
- 其他模式會寫入自己的模式名，但目前仍走 component prompt；這保留未來針對 `half_action`、`full_action`、`hybrid` 拆出不同 prompt 的空間。

驗證：

```powershell
python -m py_compile spine_ui_server.py run_v2.py
```

通過。

本地 UI server 已重啟：

```text
http://127.0.0.1:8765
```

`/api/project?project=TEST_WARRIOR_SWORD` 已確認會回傳：

```text
stage1_mode: full_action
stage1_character_note: 既有角色補充需求
```

## 2026-05-27 拖放讀入實作紀錄

依使用需求「檔案讀入要用拖進去的」，本地 UI 已新增拖放/選檔讀入來源圖。

修改檔案：

```text
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\spine_ui_server.py
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\spine_ui.html
```

新增能力：

- 左側 source 圖區現在是 drop zone。
- 可把圖片直接拖進 UI。
- 也可按「選擇圖片」使用檔案選擇器。
- 前端用 `FileReader.readAsDataURL()` 讀圖，再 POST 到 `/api/upload-source`。
- 後端解 data URL，使用 PIL 轉為 RGBA，存成：

```text
projects/<PROJECT>/source.png
```

- 專案名自動使用檔名 stem。
- 若同名專案已存在，自動避讓為 `_2`, `_3`，避免覆蓋既有專案。
- 上傳時會連同目前 UI 的 `stage1_mode` 與 `stage1_character_note` 一起寫入新專案。
- 上傳完成後 UI 會刷新專案列表並切換到新專案。

驗證：

```powershell
python -m py_compile spine_ui_server.py run_v2.py
```

通過。

本地 server 已重啟：

```text
http://127.0.0.1:8765
```

HTTP 頁面內容已確認包含：

```text
dropZone
選擇圖片
/api/upload-source
```

後端小測：

```text
decode_data_url(...) -> 8 bytes
unique_project_name("TEST_WARRIOR_SWORD.png") -> TEST_WARRIOR_SWORD_2
```

## 2026-05-27 貼上圖片實作紀錄

依使用需求「從網頁複製就可貼上到圖片輸入區」，本地 UI 已新增剪貼簿圖片讀入。

修改檔案：

```text
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\spine_ui.html
```

新增能力：

- 網頁上複製圖片後，可在 SpineSliceV2 UI 直接貼上。
- 前端監聽 `paste` event。
- 若剪貼簿中有 `image/*` item，會轉成 `File`，並走既有 `/api/upload-source` 上傳流程。
- 若剪貼簿不是圖片，事件不攔截，textarea 仍可正常貼文字。
- UI 提示改為：

```text
或把圖片拖到這裡 / 貼上圖片
```

驗證：

```powershell
python -m py_compile spine_ui_server.py run_v2.py
```

通過。頁面內容已確認包含 `貼上圖片` 與 `imageFileFromPaste`。

## 2026-05-27 Stage 1 補充需求自動生成

依使用回憶「之前會有相對應的拆圖 prompt 自動生成，依據給的圖去做判斷生成 prompt，有大概規則可套用」，已補回規則式自動生成。

修改檔案：

```text
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\spine_ui_server.py
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\spine_ui.html
```

新增能力：

- 後端新增 `infer_stage1_mode(project)`：
  - 讀 `source.png`
  - 用 `detect_character_bbox()` 取得角色外框
  - 依 bbox / image 比例粗判 `full_action`、`half_action`、`portrait_face`、`hybrid`
- 後端新增 `stage1_note_for_mode(mode, reason)`：
  - 依模式套用 Stage 1 補充需求規則
  - 包含不要補出構圖外身體、不要換視角、Stage 1 不貪拆五官、道具/頭髮/披風/尾巴等獨立件規則
- 後端新增 `/api/suggest-stage1-prompt`：
  - 重新生成 `stage1_mode.txt`
  - 重新生成 `stage1_character_note.md`
  - 回傳判斷理由與 bbox ratio
- UI 新增「自動生成補充需求」按鈕。
- 拖入/貼上新圖時，不再沿用上一個專案的 Stage 1 補充文字；新專案會自動依圖生成一份初稿。

注意：

- 純規則式判斷不是視覺理解模型；如果 source 幾乎填滿整張畫布，尤其有大武器或滿版背景，bbox 可能無法分辨全身/頭像。
- 這種情況目前會偏向 `hybrid`，並在補充需求中提示先產生可人工挑選的大件候選。
- 使用者仍可手動改成 `full_action`、`half_action` 或 `portrait_face`。

驗證：

```powershell
python -m py_compile spine_ui_server.py run_v2.py
```

通過。

`TEST_WARRIOR_SWORD` smoke test：

```text
mode: hybrid
bbox_ratio: 1.03
reason: 來源圖幾乎填滿整張畫布，無法只靠外框判斷全身或頭像，先用混合模式產生可人工挑選的大件候選。
```

## 2026-05-27 透明 PNG 硬規則

依使用需求「產出的圖要透明 PNG」，已把透明輸出從 prompt 建議提升成所有 GPT 生成呼叫的硬性附加規則。

修改檔案：

```text
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\run_v2.py
```

新增/調整：

- 新增 `TRANSPARENT_OUTPUT_REQUIREMENT`，每次 `call_openai_image_edit()` 都會自動附加到 prompt 後面。
- 硬性規則包含：
  - 必須是帶 alpha channel 的透明背景 PNG。
  - 背景 alpha 必須為 0。
  - 不可白底、灰底、棋盤格底、純色底、漸層底、陰影底、外框或紙張。
  - 拆件間空白必須完全透明。
- 影像 API 設定仍維持：

```json
"output_format": "png",
"background": "transparent"
```

- GPT 回傳後仍會執行 `make_connected_light_background_transparent(output)`，移除連通白/淺色背景。
- 透明化後明確以 PNG 儲存：

```python
image.save(path, format="PNG")
```

- 單件候選比較圖 `make_part_candidate_sheet()` 的 canvas 已從白底改成透明底。

驗證：

```powershell
python -m py_compile run_v2.py spine_ui_server.py
```

通過。本地 server 已重啟。
