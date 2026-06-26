from pathlib import Path
import json

from PIL import Image


OUT = Path(r"C:\Users\kurtpan\Documents\Codex\green_archer_stage1_psd")
SHEET = OUT / "stage1_sheet_v2.png"
ORIGINAL = OUT / "original.png"
LAYER_DIR = OUT / "layers"
LAYER_DIR.mkdir(parents=True, exist_ok=True)

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


def main() -> None:
    sheet = Image.open(SHEET).convert("RGBA")
    layers = []
    for name, box in SPECS:
        crop = sheet.crop(box)
        path = LAYER_DIR / f"{name}.png"
        crop.save(path)
        layers.append({"name": name, "path": path.resolve().as_posix()})

    jsx_path = OUT / "build_green_archer_stage1.jsx"
    psd_path = OUT / "green_archer_stage1_draft.psd"
    preview_path = OUT / "green_archer_stage1_draft_preview.png"

    layer_rows = ",\n".join(
        f"  {{ name: {json.dumps(item['name'])}, path: {json.dumps(item['path'])} }}"
        for item in layers
    )

    jsx = f"""#target photoshop
app.displayDialogs = DialogModes.NO;
var doc = app.documents.add(1800, 1300, 72, "green_archer_stage1_draft", NewDocumentMode.RGB, DocumentFill.TRANSPARENT);

function placeLayer(path, name, x, y, maxW, maxH, opacity, visible) {{
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
  return layer;
}}

placeLayer({json.dumps(ORIGINAL.resolve().as_posix())}, "00_reference_original", 500, 160, 800, 1000, 35, true);
placeLayer({json.dumps(SHEET.resolve().as_posix())}, "01_stage1_sheet_reference", 70, 40, 460, 330, 45, true);

var layers = [
{layer_rows}
];
var cols = 4;
var cellW = 420;
var cellH = 230;
for (var i = 0; i < layers.length; i++) {{
  var col = i % cols;
  var row = Math.floor(i / cols);
  placeLayer(layers[i].path, layers[i].name, 60 + col * cellW, 420 + row * cellH, 320, 180, 100, true);
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
