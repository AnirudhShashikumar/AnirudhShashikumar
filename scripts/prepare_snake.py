"""Validate generated contribution SVGs and freeze one for reduced-motion users."""

from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "assets" / "generated"
SVG = "http://www.w3.org/2000/svg"


def validate(path: Path) -> str:
    text = path.read_text()
    root = ET.fromstring(text)
    if root.tag != f"{{{SVG}}}svg" or "viewBox" not in root.attrib:
        raise ValueError(f"Invalid SVG: {path}")
    if not 500 < path.stat().st_size < 1_000_000:
        raise ValueError(f"Unexpected SVG size: {path}")
    if "pending-first-run" in text:
        raise ValueError("Generator did not replace the initial placeholder")
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] in {"script", "foreignObject", "image", "animate", "animateTransform", "animateMotion", "set"}:
            raise ValueError(f"Unexpected embedded content in {path}")
        if any(key.lower().startswith("on") for key in element.attrib):
            raise ValueError(f"Unexpected event handler in {path}")
    return text


def main() -> None:
    light = validate(DIRECTORY / "contributions.svg")
    validate(DIRECTORY / "contributions-dark.svg")
    # Retain the generator's fills and layout; override CSS motion only.
    # An opaque light backing keeps this static calendar legible in both themes.
    root = ET.fromstring(light)
    x, y, width, height = root.attrib["viewBox"].replace(",", " ").split()
    backing = (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        'rx="8" fill="#ffffff"/>'
    )
    start = light.index(">", light.index("<svg")) + 1
    frozen = light[:start] + backing + light[start:]
    frozen = frozen.replace(
        "</svg>",
        '<style>*{animation:none!important;transition:none!important}</style></svg>',
    )
    target = DIRECTORY / "contributions-static.svg"
    target.write_text(frozen)
    validate(target)
    print("Validated both themes and generated the static contribution calendar.")


if __name__ == "__main__":
    main()
