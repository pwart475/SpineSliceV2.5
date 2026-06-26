from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw


EXPECTED_LAYERS = [
    "head_face_beard",
    "green_hat_with_red_feather",
    "hair_front_back",
    "green_neck_scarf_collar",
    "upper_torso",
    "lower_torso_waist",
    "left_arm_grip_pose",
    "right_arm_front_hand",
    "money_bag",
    "quiver",
    "arrows_bundle",
    "side_pouch",
]

FORBIDDEN_STAGE1_TORSO_HINTS = (
    "strap",
    "chest",
    "tunic_plate",
    "plate",
    "seam",
    "shoulder_hole",
    "decoration",
)

CONTACT_SHEET_NAME = "PSD_PACKAGING_CONTACT_SHEET.png"


@dataclass(frozen=True)
class ImageStats:
    path: Path
    size: tuple[int, int]
    alpha_coverage: float
    near_black_visible_ratio: float
    bbox: tuple[int, int, int, int] | None


@dataclass(frozen=True)
class ReviewData:
    root: Path
    raw_stats: list[ImageStats]
    package_stats: list[ImageStats]
    missing_required: list[Path]
    missing_layers: list[str]
    unexpected_layers: list[str]
    missing_package_layers: list[str]
    unexpected_package_layers: list[str]
    torso_over_split: list[str]
    jsx_missing_package_refs: list[str]
    jsx_raw_layer_refs: list[str]
    jsx_exists: bool
    jsx_smart_object_enabled: bool


def image_data(image: Image.Image):
    return image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()


def inspect_image(path: Path) -> ImageStats:
    image = Image.open(path).convert("RGBA")
    total = image.width * image.height
    visible = 0
    near_black = 0
    for r, g, b, a in image_data(image):
        if a > 0:
            visible += 1
            if r < 12 and g < 12 and b < 12:
                near_black += 1

    return ImageStats(
        path=path,
        size=image.size,
        alpha_coverage=visible / total if total else 0.0,
        near_black_visible_ratio=near_black / visible if visible else 0.0,
        bbox=image.getbbox(),
    )


def draw_checkerboard(size: tuple[int, int], cell: int = 12) -> Image.Image:
    w, h = size
    image = Image.new("RGBA", size, (235, 235, 235, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            color = (250, 250, 250, 255) if (x // cell + y // cell) % 2 == 0 else (188, 188, 188, 255)
            draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=color)
    return image


def format_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def make_contact_sheet(stats: list[ImageStats], out_path: Path) -> None:
    cols = 4
    cell_w = 360
    cell_h = 300
    label_h = 34
    rows = (len(stats) + cols - 1) // cols
    sheet = draw_checkerboard((cols * cell_w, rows * cell_h))
    draw = ImageDraw.Draw(sheet)

    for index, item in enumerate(stats):
        image = Image.open(item.path).convert("RGBA")
        image.thumbnail((cell_w - 44, cell_h - label_h - 34), Image.Resampling.LANCZOS)
        col = index % cols
        row = index // cols
        x0 = col * cell_w
        y0 = row * cell_h
        x = x0 + (cell_w - image.width) // 2
        y = y0 + label_h + (cell_h - label_h - image.height) // 2
        sheet.alpha_composite(image, (x, y))
        draw.rectangle((x0, y0, x0 + cell_w - 1, y0 + label_h - 1), fill=(28, 31, 34, 235))
        draw.text((x0 + 10, y0 + 9), f"{item.path.stem}  alpha {format_pct(item.alpha_coverage)}", fill=(255, 255, 255, 255))
        draw.rectangle((x0, y0, x0 + cell_w - 1, y0 + cell_h - 1), outline=(70, 70, 70, 255))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(out_path)


def passfail(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def layer_names(paths: list[Path]) -> list[str]:
    return [path.stem for path in paths]


def risk_notes(item: ImageStats) -> list[str]:
    notes: list[str] = []
    if item.bbox is None:
        return ["empty alpha"]

    left, top, right, bottom = item.bbox
    width, height = item.size
    if item.alpha_coverage < 0.15:
        notes.append("very thin alpha; inspect for over-removal")
    if item.alpha_coverage > 0.80:
        notes.append("high alpha coverage; inspect for leftover background")
    if item.near_black_visible_ratio > 0.01:
        notes.append("near-black remains; inspect halo/interior shadows")
    if left == 0 or top == 0 or right == width or bottom == height:
        notes.append("alpha touches crop edge; inspect cut-off")
    return notes or ["manual visual check"]


def write_stats_table(lines: list[str], title: str, stats: list[ImageStats]) -> None:
    lines.append(title)
    lines.append("")
    lines.append("| Layer | Size | Alpha coverage | Near-black visible | BBox |")
    lines.append("|---|---:|---:|---:|---|")
    for item in stats:
        lines.append(
            "| "
            f"`{item.path.stem}` | "
            f"{item.size[0]}x{item.size[1]} | "
            f"{format_pct(item.alpha_coverage)} | "
            f"{format_pct(item.near_black_visible_ratio)} | "
            f"`{item.bbox}` |"
        )
    lines.append("")


def collect_review_data(root: Path) -> ReviewData:
    layer_dir = root / "layers"
    package_layer_dir = root / "_psd_packaging_layers"
    jsx_path = root / "build_green_archer_stage1.jsx"
    required_files = [
        root / "original.png",
        root / "stage1_sheet_v2.png",
        root / "green_archer_stage1_draft.psd",
        root / "green_archer_stage1_draft_preview.png",
        root / "SPINESLICE_GENERAL_RULES_20260626.md",
        jsx_path,
    ]

    raw_paths = sorted(layer_dir.glob("*.png")) if layer_dir.exists() else []
    package_paths = sorted(package_layer_dir.glob("*.png")) if package_layer_dir.exists() else []
    raw_names = layer_names(raw_paths)
    package_names = layer_names(package_paths)
    jsx_text = jsx_path.read_text(encoding="utf-8") if jsx_path.exists() else ""

    return ReviewData(
        root=root,
        raw_stats=[inspect_image(path) for path in raw_paths],
        package_stats=[inspect_image(path) for path in package_paths],
        missing_required=[path for path in required_files if not path.exists()],
        missing_layers=[name for name in EXPECTED_LAYERS if name not in raw_names],
        unexpected_layers=[name for name in raw_names if name not in EXPECTED_LAYERS],
        missing_package_layers=[name for name in EXPECTED_LAYERS if name not in package_names],
        unexpected_package_layers=[name for name in package_names if name not in EXPECTED_LAYERS],
        torso_over_split=[name for name in raw_names if any(hint in name for hint in FORBIDDEN_STAGE1_TORSO_HINTS)],
        jsx_missing_package_refs=[name for name in EXPECTED_LAYERS if f"_psd_packaging_layers/{name}.png" not in jsx_text],
        jsx_raw_layer_refs=[name for name in EXPECTED_LAYERS if f"/layers/{name}.png" in jsx_text or f"\\layers\\{name}.png" in jsx_text],
        jsx_exists=jsx_path.exists(),
        jsx_smart_object_enabled="newPlacedLayer" in jsx_text and "convertActiveLayerToSmartObject" in jsx_text,
    )


def gates(data: ReviewData) -> dict[str, bool]:
    raw_names = [item.path.stem for item in data.raw_stats]
    raw_opaque_layers = [item for item in data.raw_stats if item.alpha_coverage >= 0.995]
    package_transparent_layers = [item for item in data.package_stats if item.alpha_coverage < 0.995]
    return {
        "file_gate": not data.missing_required,
        "component_gate": not data.missing_layers and not data.unexpected_layers,
        "package_component_gate": not data.missing_package_layers and not data.unexpected_package_layers,
        "torso_gate": "upper_torso" in raw_names and "lower_torso_waist" in raw_names and not data.torso_over_split,
        "raw_layers_gate": bool(data.raw_stats) and len(raw_opaque_layers) == len(data.raw_stats),
        "packaging_alpha_gate": bool(data.package_stats) and len(package_transparent_layers) == len(data.package_stats),
        "jsx_package_gate": data.jsx_exists and not data.jsx_missing_package_refs,
        "jsx_no_raw_gate": data.jsx_exists and not data.jsx_raw_layer_refs,
        "jsx_smart_object_gate": data.jsx_exists and data.jsx_smart_object_enabled,
    }


def stage_verdict(gate_map: dict[str, bool]) -> str:
    if not gate_map["file_gate"] or not gate_map["component_gate"]:
        return "FAIL"
    if not all(gate_map.values()):
        return "CONTINUE"
    return "STRUCTURE PASS - VISUAL REVIEW NEEDED"


def write_stage_report(data: ReviewData, report_path: Path) -> int:
    gate_map = gates(data)
    verdict = stage_verdict(gate_map)
    lines: list[str] = []
    lines.append("# Stage 1 Package Review")
    lines.append("")
    lines.append(f"Package: `{data.root.as_posix()}`")
    lines.append(f"Verdict: **{verdict}**")
    lines.append("")
    lines.append("## Gates")
    lines.append("")
    lines.append(f"- Required files present: **{passfail(gate_map['file_gate'])}**")
    lines.append(f"- Expected Stage 1 raw component set: **{passfail(gate_map['component_gate'])}**")
    lines.append(f"- Stage 1 torso split rule: **{passfail(gate_map['torso_gate'])}**")
    lines.append(f"- Raw layer PNGs stay uncut before PSD packaging: **{passfail(gate_map['raw_layers_gate'])}**")
    lines.append(f"- PSD packaging layer set exists: **{passfail(gate_map['package_component_gate'])}**")
    lines.append(f"- PSD packaging layers are transparent: **{passfail(gate_map['packaging_alpha_gate'])}**")
    lines.append(f"- Photoshop JSX references PSD packaging layers: **{passfail(gate_map['jsx_package_gate'])}**")
    lines.append(f"- Photoshop JSX does not reference raw `layers/`: **{passfail(gate_map['jsx_no_raw_gate'])}**")
    lines.append(f"- Photoshop JSX converts component layers to Smart Objects: **{passfail(gate_map['jsx_smart_object_gate'])}**")
    lines.append("")
    write_stats_table(lines, "## Raw Layer Stats", data.raw_stats)
    write_stats_table(lines, "## PSD Packaging Layer Stats", data.package_stats)
    lines.append("## Findings")
    lines.append("")
    lines.append("- Raw `layers/` PNGs are intentionally opaque crops at Stage 1. Do not run background removal during Stage 1 review.")
    lines.append("- `_psd_packaging_layers/` contains transparent PNGs generated only by the PSD packaging build script.")
    lines.append("- Photoshop JSX is expected to consume `_psd_packaging_layers/`, not raw `layers/`.")
    lines.append("- Photoshop JSX is expected to convert component layers to Smart Objects after import.")
    lines.append("- Edge quality and duplicated-pixel checks still need visual inspection in Photoshop after packaging.")
    lines.append("")
    lines.append("## Next Actions")
    lines.append("")
    lines.append("1. Inspect `PSD_PACKAGING_CONTACT_SHEET.png` and `PSD_PACKAGING_QC.md` for per-layer risks.")
    lines.append("2. Inspect `green_archer_stage1_draft_preview.png` or open the PSD in Photoshop for visual split-logic approval.")
    lines.append("3. If rejected, regenerate only the failed components and rerun this review.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return 0 if verdict != "FAIL" else 1


def write_packaging_qc_report(data: ReviewData, report_path: Path) -> None:
    gate_map = gates(data)
    packaging_ok = (
        gate_map["package_component_gate"]
        and gate_map["packaging_alpha_gate"]
        and gate_map["jsx_package_gate"]
        and gate_map["jsx_no_raw_gate"]
        and gate_map["jsx_smart_object_gate"]
    )
    verdict = "PASS - VISUAL REVIEW NEEDED" if packaging_ok else "CONTINUE"
    contact_sheet = data.root / CONTACT_SHEET_NAME
    lines: list[str] = []
    lines.append("# PSD Packaging QC")
    lines.append("")
    lines.append(f"Package: `{data.root.as_posix()}`")
    lines.append(f"Verdict: **{verdict}**")
    lines.append(f"Contact sheet: `{contact_sheet.as_posix()}`")
    lines.append("")
    lines.append("## Packaging Gates")
    lines.append("")
    lines.append(f"- Packaging layer set exists: **{passfail(gate_map['package_component_gate'])}**")
    lines.append(f"- Packaging layers are transparent: **{passfail(gate_map['packaging_alpha_gate'])}**")
    lines.append(f"- JSX references `_psd_packaging_layers/`: **{passfail(gate_map['jsx_package_gate'])}**")
    lines.append(f"- JSX avoids raw `layers/`: **{passfail(gate_map['jsx_no_raw_gate'])}**")
    lines.append(f"- JSX converts component layers to Smart Objects: **{passfail(gate_map['jsx_smart_object_gate'])}**")
    lines.append("")
    lines.append("## Per-Layer Risk Table")
    lines.append("")
    lines.append("| Layer | Alpha coverage | BBox | Risk notes |")
    lines.append("|---|---:|---|---|")
    for item in data.package_stats:
        lines.append(f"| `{item.path.stem}` | {format_pct(item.alpha_coverage)} | `{item.bbox}` | {'; '.join(risk_notes(item))} |")
    lines.append("")
    lines.append("## Manual Photoshop Checks")
    lines.append("")
    lines.append("- Check feather, beard, hands, arrows, and bag edge halos after PSD import.")
    lines.append("- Check that dark outlines and interior shadows were not removed as background.")
    lines.append("- Check money bag, hair, and side pouch are not duplicated inside neighboring layers.")
    lines.append("- Check layer pivots/overlap are acceptable before Spine import.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("green_archer_stage1_psd")
    data = collect_review_data(root)
    make_contact_sheet(data.package_stats, root / CONTACT_SHEET_NAME)
    write_packaging_qc_report(data, root / "PSD_PACKAGING_QC.md")
    return write_stage_report(data, root / "STAGE1_REVIEW.md")


if __name__ == "__main__":
    raise SystemExit(main())

