# Run Photoshop Packaging

This package keeps Stage 1 review crops and PSD packaging inputs separate.

## Inputs

- Raw Stage 1 crops: `green_archer_stage1_psd/layers/`
- PSD packaging transparent inputs: `green_archer_stage1_psd/_psd_packaging_layers/`
- Photoshop script: `green_archer_stage1_psd/build_green_archer_stage1.jsx`

Do not manually background-remove files in `layers/`. The build script regenerates `_psd_packaging_layers/` for PSD packaging.
During Photoshop import, every component from `_psd_packaging_layers/` is converted into a Smart Object. Reference layers stay normal layers.

## Build Packaging Inputs

Run from the repo root:

```powershell
C:\Users\kurtpan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\build_green_archer_stage1_psd.py
C:\Users\kurtpan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\review_stage1_package.py
```

Expected QC files:

- `green_archer_stage1_psd/STAGE1_REVIEW.md`
- `green_archer_stage1_psd/PSD_PACKAGING_QC.md`

## Run JSX In Photoshop

Manual route:

1. Open Photoshop.
2. Choose `File > Scripts > Browse...`.
3. Select `green_archer_stage1_psd/build_green_archer_stage1.jsx`.
4. Wait for the PSD and PNG preview save to finish.

Known local Photoshop path:

```text
C:\Program Files\Adobe\Adobe Photoshop 2026\Photoshop.exe
```

## Outputs

- PSD: `green_archer_stage1_psd/green_archer_stage1_draft.psd`
- Preview: `green_archer_stage1_psd/green_archer_stage1_draft_preview.png`

## Photoshop Visual QC

Check these before Stage 1 acceptance:

- JSX imported `_psd_packaging_layers/`, not raw `layers/`.
- Component layers are Smart Objects in the PSD.
- Component names match the Stage 1 list.
- No obvious black halo around feather, beard, hands, arrows, money bag, or pouch.
- Dark outlines and interior shadows were not removed as background.
- Money bag is not duplicated inside hand layers.
- Hair is not duplicated inside head layer.
- Side pouch is not duplicated inside lower torso layer.
- Coarse split logic is acceptable for Stage 1; do not request Stage 2 micro-splits here.

If any item fails, regenerate only the failed component or adjust PSD packaging cleanup, then rerun the review scripts.
