#!/usr/bin/env python3
"""Generate P3-style SVG assets for the fcitx5 skin.

Only two assets are required for this minimal skin:

* panel.svg     — solid deep-blue input panel background
* highlight.svg — solid cyan highlight behind the selected candidate

All coordinates and colors are parameterized so the theme can be tuned
without hand-editing SVG files.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class Palette:
    # Persona 3 inspired palette.
    deep_blue: str = "#172a47"
    highlight_blue: str = "#3db4d6"
    white: str = "#ffffff"


PALETTE = Palette()


def svg_root(width: int, height: int, content: str) -> str:
    # preserveAspectRatio="none" lets fcitx5 stretch the SVG freely to fill
    # the panel / highlight region regardless of the source aspect ratio.
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'preserveAspectRatio="none">\n'
        f"{content}\n"
        f"</svg>"
    )


def generate_panel(
    width: int = 260,
    height: int = 56,
) -> str:
    """Input panel background: a flat deep-blue rectangle.

    Matches the clean rectangular panel in images/result.jpg.
    """
    p = PALETTE
    content = (
        f'  <rect x="0" y="0" width="{width}" height="{height}" '
        f'fill="{p.deep_blue}"/>\n'
    )
    return svg_root(width, height, content)


def generate_highlight(
    width: int = 160,
    height: int = 36,
    pad: int = 0,
) -> str:
    """Candidate highlight: a flat cyan/blue rectangle filling the candidate area."""
    p = PALETTE
    content = (
        f'  <rect x="{pad}" y="{pad}" width="{width - pad * 2}" '
        f'height="{height - pad * 2}" fill="{p.highlight_blue}"/>\n'
    )
    return svg_root(width, height, content)


def write_asset(directory: Path, name: str, svg: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_text(svg, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate minimal P3-style fcitx5 skin assets."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "dist" / "p3-skin",
        help="Output directory for generated assets.",
    )
    args = parser.parse_args(argv)

    out = args.out
    write_asset(out, "panel.svg", generate_panel())
    write_asset(out, "highlight.svg", generate_highlight())

    print(f"Generated assets in: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
