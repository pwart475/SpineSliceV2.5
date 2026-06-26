# PSD Visual Review Notes

Inspection method: user-provided Photoshop screenshot, PSD packaging QC metrics, and alpha-mask silhouette inspection from `_psd_packaging_layers/`.

## Initial Problem Seen

The first Photoshop-opened PSD showed severe over-removal:

- `right_arm_front_hand` was reduced to fragments.
- `lower_torso_waist`, quiver/arrows, and several torso/accessory parts had broken silhouettes.
- Many components looked like scattered cut scraps rather than usable transparent layers.

## Root Cause

The previous PSD packaging cleanup estimated background color from each crop border median. When a subject touched the crop edge, the median could become subject color instead of sheet background color. Flood-fill then removed valid subject pixels.

## Fix Applied

`scripts/build_green_archer_stage1_psd.py` now removes only pixels close to the known dark sheet background `(19, 20, 20)`.

It no longer lets arbitrary crop-border colors become background seeds.

## Post-Fix Metrics

- `right_arm_front_hand` alpha coverage improved from 12.5% to 28.4%.
- `lower_torso_waist` alpha coverage improved from 20.7% to 51.6%.
- Near-black visible in both high-risk layers is now 0.0%.
- `PSD_PACKAGING_QC.md` passes all packaging gates.

## Remaining Manual Checks

The PSD still needs visual inspection in Photoshop for:

- Cut-off edges where alpha touches the crop boundary.
- Fine edge halos around hands, arrows, feather, beard, and bag.
- Duplicated pixels between money bag/hands, hair/head, and side pouch/lower torso.
