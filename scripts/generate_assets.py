#!/usr/bin/env python3
"""Generate Persona 3 style SVG assets for the fcitx5 skin.

Design: "塔尔塔罗斯 HUD". A tactical terminal: a deep-navy screen framed by
cyan corner brackets, a clock-tick ruler pinned to the top edge, and a
selected candidate drawn as an outlined box (thin cyan frame + translucent
fill) with a solid cyan tag at its left end.

Geometry rules, because fcitx5 stretches 9-patch edges and centers: the
bracket elbows and the side cards sit inside the fixed corner/edge tiles;
everything in the stretched strips is a horizontal or vertical line.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class Palette:
    deep_blue: str = "#0A1B33"
    darker_blue: str = "#071427"
    cyan: str = "#5FD6FF"
    text: str = "#CFE9FF"
    comment: str = "#6F8BAB"
    highlight_text: str = "#EAF7FF"
    white: str = "#ffffff"


PALETTE = Palette()


def svg_root(width: float, height: float, content: str) -> str:
    # preserveAspectRatio="none" lets fcitx5 stretch the SVG freely to fill
    # the panel / highlight region regardless of the source aspect ratio.
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width:g} {height:g}" width="{width:g}" height="{height:g}" '
        f'preserveAspectRatio="none">\n'
        f"{content}\n"
        f"</svg>"
    )


def svg_rect(
    left: float,
    top: float,
    right: float,
    bottom: float,
    fill: str,
    opacity: float | None = None,
) -> str:
    extra = f' fill-opacity="{opacity:g}"' if opacity is not None else ""
    return (
        f'  <rect x="{left:g}" y="{top:g}" width="{right - left:g}" '
        f'height="{bottom - top:g}" fill="{fill}"{extra}/>\n'
    )


def svg_path(d: str, stroke: str, width: float) -> str:
    return (
        f'  <path d="{d}" fill="none" stroke="{stroke}" '
        f'stroke-width="{width:g}" stroke-linecap="square"/>\n'
    )


def svg_slab(rect: tuple[float, float, float, float], skew: float, fill: str) -> str:
    left, top, right, bottom = rect
    points = (
        (left, top),
        (right, top),
        (right - skew, bottom),
        (left - skew, bottom),
    )
    path = " ".join(f"{x:g},{y:g}" for x, y in points)
    return f'  <polygon points="{path}" fill="{fill}"/>\n'


@dataclass(frozen=True)
class PanelGeometry:
    """Canvas size, 9-patch margins and the HUD chrome offsets.

    The corner brackets are L-shaped strokes whose elbows all sit inside the
    four corner tiles. The side cards are small bumps whose sloped ends sit
    inside the left/right edge tiles.
    """

    width: int = 480
    height: int = 84
    margin_left: int = 22
    margin_right: int = 22
    margin_top: int = 26
    margin_bottom: int = 26
    # Screen body.
    screen: tuple[float, float, float, float] = (22.0, 3.0, 458.0, 81.0)
    # Corner brackets: stroke width and elbow span.
    bracket_width: float = 3.0
    bracket_span: float = 36.0
    bracket_drop: float = 25.0
    # Data bars near the bottom edge.
    bar_y: float = 72.0
    bar_h: float = 4.0
    # Side cards protruding from the left/right edges.
    card_left: tuple[float, float, float, float] = (0.0, 30.0, 22.0, 48.0)
    card_right: tuple[float, float, float, float] = (458.0, 36.0, 480.0, 52.0)
    card_skew: float = 4.0


PANEL = PanelGeometry()


def generate_panel(geometry: PanelGeometry = PANEL) -> str:
    """Input panel background: screen, corner brackets, side cards."""
    g = geometry
    p = PALETTE
    sl, st, sr, sb = g.screen
    content = svg_rect(sl, st, sr, sb, p.deep_blue)
    content += svg_rect(sl + 4.0, st + 4.0, sr - 4.0, sb - 4.0, p.darker_blue)

    # Corner brackets: elbows at the screen corners.
    s = g.bracket_width
    span = g.bracket_span
    drop = g.bracket_drop
    content += (
        f'  <g fill="none" stroke="{p.cyan}" stroke-width="{s:g}" '
        f'stroke-linecap="square">\n'
        f'    <path d="M {sl:g} {st + drop:g} L {sl:g} {st:g} L {sl + span:g} {st:g}"/>\n'
        f'    <path d="M {sr - span:g} {st:g} L {sr:g} {st:g} L {sr:g} {st + drop:g}"/>\n'
        f'    <path d="M {sr:g} {sb - drop:g} L {sr:g} {sb:g} L {sr - span:g} {sb:g}"/>\n'
        f'    <path d="M {sl + span:g} {sb:g} L {sl:g} {sb:g} L {sl:g} {sb - drop:g}"/>\n'
        f"  </g>\n"
    )

    # Two short data bars near the bottom edge, unequal lengths.
    content += svg_rect(90.0, g.bar_y, 124.0, g.bar_y + g.bar_h, p.cyan, 0.35)
    content += svg_rect(128.0, g.bar_y, 146.0, g.bar_y + g.bar_h, p.cyan, 0.35)

    # Side cards protruding past the screen edges.
    cl = g.card_left
    content += svg_slab((cl[0], cl[1], cl[2], cl[3]), g.card_skew, p.deep_blue)
    cr = g.card_right
    content += svg_slab((cr[0], cr[1], cr[2], cr[3]), -g.card_skew, p.deep_blue)
    return svg_root(g.width, g.height, content)


def generate_highlight(
    width: int = 160,
    height: int = 34,
    tag_width: float = 10.0,
) -> str:
    """Candidate highlight: cyan outline box + translucent fill + left tag.

    The solid tag sits inside the fixed left margin column; the stretched
    center is the translucent fill between two flat horizontal frame lines.
    """
    p = PALETTE
    content = svg_rect(2.0, 2.0, width - 2.0, height - 2.0, p.cyan, 0.18)
    content += (
        f'  <rect x="2" y="2" width="{width - 4:g}" height="{height - 4:g}" '
        f'fill="none" stroke="{p.cyan}" stroke-width="2"/>\n'
    )
    content += svg_slab(
        (0.0, 6.0, tag_width, height - 8.0),
        2.0,
        p.cyan,
    )
    return svg_root(width, height, content)


def generate_ticks(
    width: int = 260,
    height: int = 14,
    step: float = 10.0,
) -> str:
    """Clock-tick ruler decal used as the panel overlay along the top edge.

    Long ticks every sixth step with two marker dots, like a midnight clock.
    Fixed-size decal, never stretched.
    """
    p = PALETTE
    marks: list[str] = []
    x = 4.0
    i = 0
    while x < width - 2.0:
        big = i % 6 == 0
        y0, y1 = (1.0, height - 1.0) if big else (5.0, height - 3.0)
        sw = 1.8 if big else 0.9
        marks.append(
            f'    <path d="M {x:g} {y0:g} L {x:g} {y1:g}" stroke-width="{sw:g}"/>\n'
        )
        x += step
        i += 1
    body = (
        f'  <g stroke="{p.cyan}" stroke-opacity="0.7">\n'
        + "".join(marks)
        + "  </g>\n"
        f'  <g fill="{p.cyan}" fill-opacity="0.85">\n'
        f'    <circle cx="{width / 2 - 6:g}" cy="7" r="2.4"/>\n'
        f'    <circle cx="{width - 12:g}" cy="7" r="2.4"/>\n'
        f"  </g>\n"
    )
    return svg_root(width, height, body)


def generate_arrow(direction: str, size: float = 28.0) -> str:
    """Page button: a cyan wedge with a deep-blue drop shadow."""
    p = PALETTE
    w = size
    h = size * 1.08
    half = h / 2
    if direction == "next":
        pts = [(4.0, 3.0), (w - 3.0, half), (4.0, h - 3.0)]
    else:
        pts = [(w - 4.0, 3.0), (3.0, half), (w - 4.0, h - 3.0)]
    shadow = " ".join(f"{x + 2.5:g},{y + 2.5:g}" for x, y in pts)
    body = " ".join(f"{x:g},{y:g}" for x, y in pts)
    content = (
        f'  <polygon points="{shadow}" fill="{p.deep_blue}"/>\n'
        f'  <polygon points="{body}" fill="{p.cyan}"/>\n'
    )
    return svg_root(w, h, content)


THEME_CONF = f"""[Metadata]
Name=P3 Moonlight
Version=2
Author=OpenCode
Description=A fcitx5 skin inspired by the visual style of Persona 3
ScaleWithDPI=True

[InputPanel]
NormalColor={PALETTE.text}ff
CandidateLabelColor={PALETTE.cyan}ff
HighlightCandidateColor={PALETTE.highlight_text}ff
HighlightCandidateLabelColor={PALETTE.darker_blue}ff
CandidateCommentColor={PALETTE.comment}ff
HighlightCandidateCommentColor=#0A3B57ff
HighlightColor={PALETTE.cyan}ff
HighlightBackgroundColor=#00000000
LabelTextSizeFactor=85
Spacing=0

[InputPanel/Background]
Image=panel.svg
Color={PALETTE.deep_blue}ff
BorderColor={PALETTE.cyan}ff
BorderWidth=0
Overlay=ticks.svg
Gravity=TopCenter
OverlayOffsetX=0
OverlayOffsetY=5

[InputPanel/Background/Margin]
Left={PANEL.margin_left}
Right={PANEL.margin_right}
Top={PANEL.margin_top}
Bottom={PANEL.margin_bottom}

[InputPanel/Background/OverlayClipMargin]
Left=18
Right=18
Top=0
Bottom=6

[InputPanel/Highlight]
Image=highlight.svg
Color={PALETTE.cyan}ff
BorderColor=#00000000

[InputPanel/Highlight/Margin]
Left=12
Right=4
Top=4
Bottom=4

[InputPanel/TextMargin]
Left=12
Right=4
Top=4
Bottom=4

[InputPanel/ContentMargin]
Left=20
Right=18
Top=22
Bottom=20

[InputPanel/BlurMargin]
Left=12
Right=12
Top=12
Bottom=12

[InputPanel/PrevPage]
Image=prev.svg

[InputPanel/NextPage]
Image=next.svg

[Menu]
NormalColor={PALETTE.text}ff
HighlightCandidateColor={PALETTE.highlight_text}ff
Spacing=4

[Menu/Separator]
Color={PALETTE.cyan}ff
"""


def write_asset(directory: Path, name: str, content: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_text(content, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate Persona 3 style fcitx5 skin assets."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "dist" / "p3-skin",
        help="Output directory for generated assets.",
    )
    parser.add_argument(
        "--no-conf",
        action="store_true",
        help="Only write SVGs, leave theme.conf untouched.",
    )
    args = parser.parse_args(argv)

    out = args.out
    write_asset(out, "panel.svg", generate_panel())
    write_asset(out, "highlight.svg", generate_highlight())
    write_asset(out, "ticks.svg", generate_ticks())
    write_asset(out, "prev.svg", generate_arrow("prev"))
    write_asset(out, "next.svg", generate_arrow("next"))
    if not args.no_conf:
        write_asset(out, "theme.conf", THEME_CONF)

    print(f"Generated assets in: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
