# PSD Packaging QC

Package: `green_archer_stage1_psd`
Verdict: **PASS - VISUAL REVIEW NEEDED**
Contact sheet: `green_archer_stage1_psd/PSD_PACKAGING_CONTACT_SHEET.png`

## Packaging Gates

- Packaging layer set exists: **PASS**
- Packaging layers are transparent: **PASS**
- JSX references `_psd_packaging_layers/`: **PASS**
- JSX avoids raw `layers/`: **PASS**
- JSX converts component layers to Smart Objects: **PASS**

## Per-Layer Risk Table

| Layer | Alpha coverage | BBox | Risk notes |
|---|---:|---|---|
| `arrows_bundle` | 16.9% | `(0, 0, 165, 285)` | alpha touches crop edge; inspect cut-off |
| `green_hat_with_red_feather` | 64.9% | `(0, 2, 275, 150)` | alpha touches crop edge; inspect cut-off |
| `green_neck_scarf_collar` | 31.1% | `(0, 0, 260, 155)` | alpha touches crop edge; inspect cut-off |
| `hair_front_back` | 42.8% | `(0, 32, 210, 145)` | alpha touches crop edge; inspect cut-off |
| `head_face_beard` | 55.8% | `(55, 27, 234, 210)` | alpha touches crop edge; inspect cut-off |
| `left_arm_grip_pose` | 39.7% | `(32, 0, 205, 270)` | alpha touches crop edge; inspect cut-off |
| `lower_torso_waist` | 51.6% | `(0, 0, 275, 230)` | alpha touches crop edge; inspect cut-off |
| `money_bag` | 42.5% | `(42, 0, 195, 275)` | alpha touches crop edge; inspect cut-off |
| `quiver` | 36.3% | `(0, 0, 155, 325)` | alpha touches crop edge; inspect cut-off |
| `right_arm_front_hand` | 28.4% | `(0, 0, 255, 255)` | alpha touches crop edge; inspect cut-off |
| `side_pouch` | 44.1% | `(0, 0, 255, 104)` | alpha touches crop edge; inspect cut-off |
| `upper_torso` | 29.9% | `(0, 0, 255, 290)` | alpha touches crop edge; inspect cut-off |

## Manual Photoshop Checks

- Check feather, beard, hands, arrows, and bag edge halos after PSD import.
- Check that dark outlines and interior shadows were not removed as background.
- Check money bag, hair, and side pouch are not duplicated inside neighboring layers.
- Check layer pivots/overlap are acceptable before Spine import.
