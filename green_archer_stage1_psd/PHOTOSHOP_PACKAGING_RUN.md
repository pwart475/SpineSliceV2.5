# Photoshop Packaging Run

Run status: **completed after cleanup fix**

## Script

`green_archer_stage1_psd/build_green_archer_stage1.jsx`

The JSX imports transparent PNGs from `_psd_packaging_layers/`, not raw `layers/`.
Component imports are converted to Smart Objects. Reference layers are left as normal layers.

## Outputs Updated

| File | Size | Last write time |
|---|---:|---|
| `green_archer_stage1_psd/green_archer_stage1_draft.psd` | 4,285,780 bytes | 2026-06-26 15:18:47 Asia/Taipei |
| `green_archer_stage1_psd/green_archer_stage1_draft_preview.png` | 1,373,877 bytes | 2026-06-26 15:18:47 Asia/Taipei |

## Fix Included

The PSD packaging cleanup no longer infers background from crop-border median color. It only removes pixels close to the known dark sheet background.

## Follow-Up Visual Checks

- Inspect the open Photoshop document for component naming and coarse split logic.
- Confirm component layers show as Smart Objects in Photoshop.
- Check `right_arm_front_hand` and `lower_torso_waist` again; both are improved by alpha metrics but still need visual approval.
- Check money bag, hair, and side pouch are not duplicated inside neighboring layers.

## Current Tool Limitation

This session can confirm file generation, alpha metrics, and terminal-rendered silhouettes. Final visual approval still needs direct Photoshop inspection or user-provided screenshot.
