#target photoshop
app.displayDialogs = DialogModes.NO;
var doc = app.documents.add(1800, 1300, 72, "green_archer_stage1_draft", NewDocumentMode.RGB, DocumentFill.TRANSPARENT);

function placeLayer(path, name, x, y, maxW, maxH, opacity, visible) {
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
}

placeLayer("C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/original.png", "00_reference_original", 500, 160, 800, 1000, 35, true);
placeLayer("C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/stage1_sheet_v2.png", "01_stage1_sheet_reference", 70, 40, 460, 330, 45, true);

var layers = [
  { name: "head_face_beard", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/head_face_beard.png" },
  { name: "green_hat_with_red_feather", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/green_hat_with_red_feather.png" },
  { name: "hair_front_back", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/hair_front_back.png" },
  { name: "green_neck_scarf_collar", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/green_neck_scarf_collar.png" },
  { name: "upper_torso", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/upper_torso.png" },
  { name: "lower_torso_waist", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/lower_torso_waist.png" },
  { name: "left_arm_grip_pose", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/left_arm_grip_pose.png" },
  { name: "right_arm_front_hand", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/right_arm_front_hand.png" },
  { name: "money_bag", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/money_bag.png" },
  { name: "quiver", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/quiver.png" },
  { name: "arrows_bundle", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/arrows_bundle.png" },
  { name: "side_pouch", path: "C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/layers/side_pouch.png" }
];
var cols = 4;
var cellW = 420;
var cellH = 230;
for (var i = 0; i < layers.length; i++) {
  var col = i % cols;
  var row = Math.floor(i / cols);
  placeLayer(layers[i].path, layers[i].name, 60 + col * cellW, 420 + row * cellH, 320, 180, 100, true);
}

var psdOpts = new PhotoshopSaveOptions();
psdOpts.layers = true;
doc.saveAs(File("C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/green_archer_stage1_draft.psd"), psdOpts, true, Extension.LOWERCASE);
var pngOpts = new PNGSaveOptions();
pngOpts.compression = 6;
doc.saveAs(File("C:/Users/kurtpan/Documents/Codex/green_archer_stage1_psd/green_archer_stage1_draft_preview.png"), pngOpts, true, Extension.LOWERCASE);
doc.close(SaveOptions.DONOTSAVECHANGES);
