# SpineSliceV2.5 Handoff - 2026-06-26

## Current Package

Primary package folder:

`C:\Users\kurtpan\Documents\Codex\SpineSliceV2.5_HANDOFF_20260626`

Working output folder:

`C:\Users\kurtpan\Documents\Codex\green_archer_stage1_psd`

## User Goal

Continue the SpineSlice workflow toward V2.5:

- Build a usable character-slicing workflow for Spine animation.
- Stage 1 should produce coarse, reviewable component layers.
- Stage 2 should fine-split only after Stage 1 is accepted.
- Codex should self-review generated images and only package acceptable layers into PSD.

## Latest Test Subject

Green archer / Robin Hood half-body character:

`C:\Users\kurtpan\Documents\Codex\green_archer_stage1_psd\original.png`

The user supplied a half-body image with a money bag occluding hands and torso.

## Latest Generated Files

Stage 1 sheet:

`C:\Users\kurtpan\Documents\Codex\green_archer_stage1_psd\stage1_sheet_v2.png`

Draft PSD:

`C:\Users\kurtpan\Documents\Codex\green_archer_stage1_psd\green_archer_stage1_draft.psd`

Preview:

`C:\Users\kurtpan\Documents\Codex\green_archer_stage1_psd\green_archer_stage1_draft_preview.png`

Layer PNGs:

`C:\Users\kurtpan\Documents\Codex\green_archer_stage1_psd\layers\`

PSD build script:

`C:\Users\kurtpan\Documents\Codex\2026-05-27\spineslicev2\build_green_archer_stage1_psd.py`

Photoshop JSX:

`C:\Users\kurtpan\Documents\Codex\green_archer_stage1_psd\build_green_archer_stage1.jsx`

## Current Component Set

Stage 1 components used in the draft PSD:

- `head_face_beard`
- `green_hat_with_red_feather`
- `hair_front_back`
- `green_neck_scarf_collar`
- `upper_torso`
- `lower_torso_waist`
- `left_arm_grip_pose`
- `right_arm_front_hand`
- `money_bag`
- `quiver`
- `arrows_bundle`
- `side_pouch`

## Important General Rules

Rules file:

`C:\Users\kurtpan\Documents\Codex\green_archer_stage1_psd\SPINESLICE_GENERAL_RULES_20260626.md`

Rules added today:

1. Second original / deoccluded reference:
   - Use only when occlusion over target is roughly above 50%.
   - Use it to infer hidden large shapes.
   - Do not use it to change pose, hand gesture, facial angle, expression, or final silhouette.
   - It is reliable for clothes/torso/large hair masses; less reliable for fingers, face, expression, and grip contact points.

2. Stage 1 torso split:
   - For half-body or normal character Stage 1, torso should be split only by waist/belt:
     - `upper_torso`
     - `lower_torso_waist`
   - Do not split chest strap, tunic plates, shoulder holes, leather seams, or decorations into many Stage 1 pieces unless they are major independent moving parts.
   - Fine torso splitting belongs in Stage 2.

3. No duplicated pixels:
   - If money bag is a layer, hands cannot contain the complete money bag.
   - If hair is a layer, head cannot duplicate the full hair mass.
   - If side pouch is a layer, lower torso cannot contain the side pouch body.

## Status of Latest PSD

`green_archer_stage1_draft.psd` is a draft logic-check PSD.

It contains:

- Original reference layer.
- Stage 1 sheet reference layer.
- Main component layers from the accepted Stage 1 sheet.

Limitations:

- Not final alpha cleanup.
- Component layers were cropped from a black-background sheet.
- Use it to inspect layer naming and coarse split logic first.
- Photoshop/manual cleanup or better segmentation is still needed before production Spine import.

## GitHub Upload Status

Blocked in current session:

- `git` executable is not available in PATH.
- `.git` folders under `C:\Users\kurtpan\Documents\Codex` and `...\spineslicev2` are empty, not valid Git repositories.
- No GitHub remote URL is available.

To upload:

1. Install or expose Git in PATH.
2. Provide GitHub repo URL or initialize a repo.
3. Commit and push the handoff package.

## Recommended Next Actions for SpineSliceV2.5

1. Read this handoff.
2. Read `SPINESLICE_GENERAL_RULES_20260626.md`.
3. Inspect `green_archer_stage1_draft_preview.png`.
4. Open `green_archer_stage1_draft.psd` in Photoshop.
5. Decide whether Stage 1 split logic is accepted.
6. If accepted, build workflow automation around:
   - self-review,
   - duplicated-part detection,
   - second-original trigger,
   - torso split rule,
   - PSD packaging only after acceptance.
7. If not accepted, regenerate only failed components, not the whole sheet.
