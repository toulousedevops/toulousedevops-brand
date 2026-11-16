"""Convert text to SVG path data (outlined text) using HarfBuzz shaping.

Outlined text makes the generated SVG/PDF files independent of the fonts
installed on the machine that opens or prints them.
"""

import functools
import os
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONT_DIRS = [
    os.environ.get("FONTS_DIR", ""),
    str(Path(__file__).resolve().parent.parent / "fonts"),
    str(Path.home() / "Library/Fonts"),
    "/Library/Fonts",
    str(Path.home() / ".local/share/fonts"),
    str(Path.home() / ".fonts"),
    "/usr/share/fonts",
    "/usr/local/share/fonts",
]


def find_font(filename):
    """Locate a font file by name in the usual font directories."""
    for d in filter(None, FONT_DIRS):
        for p in Path(d).rglob(filename):
            return p
    raise FileNotFoundError(
        f"Font {filename!r} not found. Install it (Google Fonts) or set FONTS_DIR."
    )


class Font:
    """A shaped, outlinable font, optionally instanced from a variable font."""

    def __init__(self, filename, variations=None):
        path = find_font(filename)
        tt = TTFont(path)
        if variations and "fvar" in tt:
            tt = instancer.instantiateVariableFont(tt, variations)
        self.tt = tt
        self.glyphset = tt.getGlyphSet()
        self.order = tt.getGlyphOrder()
        self.upem = tt["head"].unitsPerEm
        blob = hb.Blob.from_file_path(str(path))
        self.hbfont = hb.Font(hb.Face(blob))
        if variations:
            self.hbfont.set_variations(variations)

    def shape(self, text, features=None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, features or {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions

    def width(self, text, size, tracking=0.0):
        """Advance width of `text` at `size` (user units). Tracking is in em."""
        _, pos = self.shape(text)
        scale = size / self.upem
        return sum(p.x_advance for p in pos) * scale + tracking * size * len(pos)

    def path(self, text, x, y, size, anchor="start", tracking=0.0):
        """Return SVG path data for `text` with its baseline at (x, y)."""
        infos, pos = self.shape(text)
        scale = size / self.upem
        w = self.width(text, size, tracking)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        pen = SVGPathPen(self.glyphset, ntos=_fmt)
        cx = 0.0
        for info, p in zip(infos, pos):
            gx = x + (cx + p.x_offset) * scale
            gy = y - p.y_offset * scale
            tpen = TransformPen(pen, (scale, 0, 0, -scale, gx, gy))
            self.glyphset[self.order[info.codepoint]].draw(tpen)
            cx += p.x_advance + tracking * self.upem
        return pen.getCommands()


def _fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


@functools.lru_cache(maxsize=None)
def font(filename, wght=None, opsz=None):
    variations = {}
    if wght is not None:
        variations["wght"] = wght
    if opsz is not None:
        variations["opsz"] = opsz
    return Font(filename, variations or None)
