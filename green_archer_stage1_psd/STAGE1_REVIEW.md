# Stage 1 Package Review

Package: `green_archer_stage1_psd`
Verdict: **STRUCTURE PASS - VISUAL REVIEW NEEDED**

## Gates

- Required files present: **PASS**
- Expected Stage 1 raw component set: **PASS**
- Stage 1 torso split rule: **PASS**
- Raw layer PNGs stay uncut before PSD packaging: **PASS**
- PSD packaging layer set exists: **PASS**
- PSD packaging layers are transparent: **PASS**
- Photoshop JSX references PSD packaging layers: **PASS**
- Photoshop JSX does not reference raw `layers/`: **PASS**
- Photoshop JSX converts component layers to Smart Objects: **PASS**

## Raw Layer Stats

| Layer | Size | Alpha coverage | Near-black visible | BBox |
|---|---:|---:|---:|---|
| `arrows_bundle` | 165x285 | 100.0% | 0.2% | `(0, 0, 165, 285)` |
| `green_hat_with_red_feather` | 275x150 | 100.0% | 0.5% | `(0, 0, 275, 150)` |
| `green_neck_scarf_collar` | 260x155 | 100.0% | 0.7% | `(0, 0, 260, 155)` |
| `hair_front_back` | 210x145 | 100.0% | 0.5% | `(0, 0, 210, 145)` |
| `head_face_beard` | 234x210 | 100.0% | 0.6% | `(0, 0, 234, 210)` |
| `left_arm_grip_pose` | 205x270 | 100.0% | 0.4% | `(0, 0, 205, 270)` |
| `lower_torso_waist` | 335x230 | 100.0% | 0.3% | `(0, 0, 335, 230)` |
| `money_bag` | 195x275 | 100.0% | 0.5% | `(0, 0, 195, 275)` |
| `quiver` | 155x325 | 100.0% | 0.5% | `(0, 0, 155, 325)` |
| `right_arm_front_hand` | 255x255 | 100.0% | 0.4% | `(0, 0, 255, 255)` |
| `side_pouch` | 255x180 | 100.0% | 0.3% | `(0, 0, 255, 180)` |
| `upper_torso` | 255x290 | 100.0% | 0.3% | `(0, 0, 255, 290)` |

## PSD Packaging Layer Stats

| Layer | Size | Alpha coverage | Near-black visible | BBox |
|---|---:|---:|---:|---|
| `arrows_bundle` | 165x285 | 16.9% | 0.0% | `(0, 0, 165, 285)` |
| `green_hat_with_red_feather` | 275x150 | 64.9% | 0.0% | `(0, 2, 275, 150)` |
| `green_neck_scarf_collar` | 260x155 | 31.1% | 0.0% | `(0, 0, 260, 155)` |
| `hair_front_back` | 210x145 | 42.8% | 0.0% | `(0, 32, 210, 145)` |
| `head_face_beard` | 234x210 | 55.8% | 0.2% | `(55, 27, 234, 210)` |
| `left_arm_grip_pose` | 205x270 | 39.7% | 0.0% | `(32, 0, 205, 270)` |
| `lower_torso_waist` | 335x230 | 51.6% | 0.0% | `(0, 0, 275, 230)` |
| `money_bag` | 195x275 | 42.5% | 0.0% | `(42, 0, 195, 275)` |
| `quiver` | 155x325 | 36.3% | 0.5% | `(0, 0, 155, 325)` |
| `right_arm_front_hand` | 255x255 | 28.4% | 0.0% | `(0, 0, 255, 255)` |
| `side_pouch` | 255x180 | 44.1% | 0.0% | `(0, 0, 255, 104)` |
| `upper_torso` | 255x290 | 29.9% | 0.0% | `(0, 0, 255, 290)` |

## Findings

- Raw `layers/` PNGs are intentionally opaque crops at Stage 1. Do not run background removal during Stage 1 review.
- `_psd_packaging_layers/` contains transparent PNGs generated only by the PSD packaging build script.
- Photoshop JSX is expected to consume `_psd_packaging_layers/`, not raw `layers/`.
- Photoshop JSX is expected to convert component layers to Smart Objects after import.
- Edge quality and duplicated-pixel checks still need visual inspection in Photoshop after packaging.

## Next Actions

1. Inspect `PSD_PACKAGING_CONTACT_SHEET.png` and `PSD_PACKAGING_QC.md` for per-layer risks.
2. Inspect `green_archer_stage1_draft_preview.png` or open the PSD in Photoshop for visual split-logic approval.
3. If rejected, regenerate only the failed components and rerun this review.
