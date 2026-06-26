from __future__ import annotations

from collections import deque
from pathlib import Path
import json

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "green_archer_stage1_psd"
SHEET = OUT / "stage1_sheet_v2.png"
ORIGINAL = OUT / "original.png"
LAYER_DIR = OUT / "layers"
PACKAGE_LAYER_DIR = OUT / "_psd_packaging_layers"
LAYER_DIR.mkdir(parents=True, exist_ok=True)
PACKAGE_LAYER_DIR.mkdir(parents=True, exist_ok=True)

# Manual boxes for the accepted Stage 1 sheet v2 generated in this thread.
# Coordinates are intentionally generous; Photoshop/manual cleanup remains expected.
SPECS = [
    ("head_face_beard", (68, 40, 302, 250)),
    ("green_hat_with_red_feather", (415, 30, 690, 180)),
    ("hair_front_back", (805, 40, 1015, 185)),
    ("green_neck_scarf_collar", (465, 210, 725, 365)),
    ("upper_torso", (260, 230, 515, 520)),
    ("lower_torso_waist", (455, 530, 790, 760)),
    ("left_arm_grip_pose", (40, 235, 245, 505)),
    ("right_arm_front_hand", (205, 560, 460, 815)),
    ("money_bag", (40, 520, 235, 795)),
    ("quiver", (850, 220, 1005, 545)),
    ("arrows_bundle", (1010, 235, 1175, 520)),
    ("side_pouch", (815, 610, 1070, 790)),
]

# Do not infer background from each crop border: limbs/clothes often touch crop edges.
# Only flood-fill pixels close to the known dark sheet background.
SHEET_BACKGROUND_RGB = (19, 20, 20)
BACKGROUND_THRESHOLD = 34
MAX_BACKGROUND_CHANNEL = 72
MAX_BACKGROUND_SPREAD = 28


def color_distance_sq(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def is_sheet_background(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    if max(rgb) > MAX_BACKGROUND_CHANNEL:
        return False
    if max(rgb) - min(rgb) > MAX_BACKGROUND_SPREAD:
        return False
    return color_distance_sq(rgb, SHEET_BACKGROUND_RGB) <= BACKGROUND_THRESHOLD * BACKGROUND_THRESHOLD


def remove_edge_connected_background(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    w, h = rgba.size
    pixels = rgba.load()
    remove = bytearray(w * h)
    queue: deque[tuple[int, int]] = deque()

    def enqueue_if_bg(x: int, y: int) -> None:
        idx = y * w + x
        if remove[idx]:
            return
        r, g, b, a = pixels[x, y]
        if a > 0 and is_sheet_background((r, g, b)):
            remove[idx] = 1
            queue.append((x, y))

    for x in range(w):
        enqueue_if_bg(x, 0)
        enqueue_if_bg(x, h - 1)
    for y in range(h):
        enqueue_if_bg(0, y)
        enqueue_if_bg(w - 1, y)

    while queue:
        x, y = queue.popleft()
        if x > 0:
            enqueue_if_bg(x - 1, y)
        if x + 1 < w:
            enqueue_if_bg(x + 1, y)
        if y > 0:
            enqueue_if_bg(x, y - 1)
        if y + 1 < h:
            enqueue_if_bg(x, y + 1)

    for y in range(h):
        for x in range(w):
            if remove[y * w + x]:
                r, g, b, _a = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)
    return rgba


def main() -> None:
    sheet = Image.open(SHEET).convert("RGBA")
    package_layers = []
    for name, box in SPECS:
        crop = sheet.crop(box)

        # Stage 1 source crop stays raw. Background removal is only for PSD packaging.
        raw_path = LAYER_DIR / f"{name}.png"
        crop.save(raw_path)

        package_path = PACKAGE_LAYER_DIR / f"{name}.png"
        remove_edge_connected_background(crop).save(package_path)
        package_layers.append({"name": name, "path": package_path.resolve().as_posix()})

    jsx_path = OUT / "build_green_archer_stage1.jsx"
    psd_path = OUT / "green_archer_stage1_draft.psd"
    preview_path = OUT / "green_archer_stage1_draft_preview.png"

    layer_rows = ",\n".join(
        f"  {{ name: {json.dumps(item['name'])}, path: {json.dumps(item['path'])} }}"
        for item in package_layers
    )

    jsx = f"""#target photoshop
app.displayDialogs = DialogModes.NO;
var doc = app.documents.add(1800, 1300, 72, "green_archer_stage1_draft", NewDocumentMode.RGB, DocumentFill.TRANSPARENT);

function convertActiveLayerToSmartObject() {{
  executeAction(stringIDToTypeID("newPlacedLayer"), undefined, DialogModes.NO);
}}

function placeLayer(path, name, x, y, maxW, maxH, opacity, visible, makeSmartObject) {{
  var opened = app.open(File(path));
  opened.selection.selectAll();
  opened.selection.copy();
  opened.close(SaveOptions.DONOTSAVECHANGES);
  app.activeDocument = doc;
  doc.paste();
  var layer = doc.activeLayer;
  layer.name = name;
  layer.opacity = opacity;
  layer.visible = visible;
  var b = layer.bounds;
  var w = b[2].as("px") - b[0].as("px");
  var h = b[3].as("px") - b[1].as("px");
  var s = Math.min(100, maxW / w * 100, maxH / h * 100);
  layer.resize(s, s, AnchorPosition.MIDDLECENTER);
  b = layer.bounds;
  w = b[2].as("px") - b[0].as("px");
  h = b[3].as("px") - b[1].as("px");
  layer.translate(x - b[0].as("px") + (maxW - w) / 2, y - b[1].as("px") + (maxH - h) / 2);
  if (makeSmartObject) {{
    convertActiveLayerToSmartObject();
    doc.activeLayer.name = name;
  }}
  return layer;
}}

placeLayer({json.dumps(ORIGINAL.resolve().as_posix())}, "00_reference_original", 500, 160, 800, 1000, 35, true, false);
placeLayer({json.dumps(SHEET.resolve().as_posix())}, "01_stage1_sheet_reference", 70, 40, 460, 330, 45, true, false);

var layers = [
{layer_rows}
];
var cols = 4;
var cellW = 420;
var cellH = 230;
for (var i = 0; i < layers.length; i++) {{
  var col = i % cols;
  var row = Math.floor(i / cols);
  placeLayer(layers[i].path, layers[i].name, 60 + col * cellW, 420 + row * cellH, 320, 180, 100, true, true);
}}

var psdOpts = new PhotoshopSaveOptions();
psdOpts.layers = true;
doc.saveAs(File({json.dumps(psd_path.resolve().as_posix())}), psdOpts, true, Extension.LOWERCASE);
var pngOpts = new PNGSaveOptions();
pngOpts.compression = 6;
doc.saveAs(File({json.dumps(preview_path.resolve().as_posix())}), pngOpts, true, Extension.LOWERCASE);
doc.close(SaveOptions.DONOTSAVECHANGES);
"""
    jsx_path.write_text(jsx, encoding="utf-8")
    print(jsx_path)
    print(psd_path)
    print(preview_path)


if __name__ == "__main__":
    main()



