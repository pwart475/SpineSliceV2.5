# Local Image Viewing Workaround

The Codex `view_image` helper currently fails in this Windows sandbox with `CreateProcessWithLogonW failed: 1385`.

Use this local browser viewer instead.

## Open An Image

From the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\open_image_viewer.ps1 -ImagePath green_archer_stage1_psd\green_archer_stage1_draft_preview.png
```

The script opens `tools_image_viewer.html` in Chrome or Edge and passes the image as a `file://` URL.

## Capture For Review

After the viewer window is active, capture it:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\kurtpan\.codex\skills\screenshot\scripts\take_screenshot.ps1 -Mode temp -ActiveWindow
```

This gives a real GUI screenshot even when the built-in image viewer is unavailable.

## Notes

- Use this for GUI-level inspection.
- Use `scripts/inspect_image_ascii.py` for terminal alpha/gray silhouette inspection.
- The workaround does not replace direct Photoshop approval for PSD layer quality.
