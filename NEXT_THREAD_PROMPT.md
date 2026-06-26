# SpineSliceV2 下一串接續提示

請接續 `SpineSliceV2 拆圖工具` 的工作。原專案在：

```text
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2
```

先讀：

```text
C:\Users\kurtpan\Documents\Codex\2026-05-27\spineslicev2\CONTINUATION_HANDOFF_2026-05-27.md
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\TEST_FINDINGS.md
C:\Users\kurtpan\Documents\Codex\2026-05-22\spine\SpineSliceV2\STAGE1_WORKFLOW.md
```

目前方向：

- SpineSliceV2 已轉成 Lovart 式 AI 拆件候選流程。
- Stage 1：先生成大件 component sheet，依圖分類為 portrait / half_action / full_action / hybrid。
- Stage 2：在 Stage 1 候選可用後再細拆四肢、道具、柔性件。
- 單件迭代已可用：`--gpt-part`、`--gpt-revise-part`、`--part-candidates`。
- 3/4 頭像的眼睛/嘴巴不能靠通用 prompt 強拆，容易變正面素材；需改走 face close-up Stage 2 或 source crop/manual extraction。
- 關節端必須提示「圓潤實心，不要空洞/管口/黑洞」。

下一步優先做：

1. 把輸入圖分類與 `stage1_mode.txt` 接進 UI。
2. 強化單件迭代 UI：保留、重生、修正 note、候選表。
3. 設計 face close-up Stage 2 流程，處理 3/4 臉的眼皮、閉眼、嘴型、鬍子、眼鏡。
4. 補 QA checklist，避免白底、文字標籤、錯視角、全身幻覺、空心關節端。

工作原則：

- 不要刪或覆蓋 `SpineSliceV1`。
- 不要把 GPT 圖當成原圖真值。
- 高相似度臉部以原圖/source crop 優先。
- 壞一個部件就修一個部件，不要重跑整張。
