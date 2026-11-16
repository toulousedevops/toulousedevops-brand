"""Generate the clean, font-independent logo files from the brand geometry.

Outputs (relative to the repository root):
  logo/toulouse-devops-logo.svg   full logo, text outlined, transparent background
  logo/toulouse-devops-mark.svg   symbol only (infinity + Occitan cross)
"""

from pathlib import Path

from brand import C, symbol
from textpath import font

ROOT = Path(__file__).resolve().parent.parent

# Wordmark settings from the Inkscape source (text3-3 in group g9).
WORD_SIZE = 61.4773
WORD_X = 169.97122
WORD_BASELINES = (233.01033, 288.3399)
WORD_STROKE = 0.960583
G9_TRANSLATE = (0.53012211, 8.9447838)


def wordmark():
    ubuntu = font("Ubuntu-Medium.ttf")
    d = " ".join(
        ubuntu.path(line, WORD_X, y, WORD_SIZE, anchor="middle")
        for line, y in zip(("Toulouse", "DevOps"), WORD_BASELINES)
    )
    return f'<path d="{d}" fill="{C["primary"]}" stroke="{C["primary"]}" stroke-width="{WORD_STROKE}"/>'


def logo_group(flat=False):
    """Full logo content in the 338.67 x 338.67 logo coordinate system.

    flat=True removes transparency (only valid on a white background).
    """
    tx, ty = G9_TRANSLATE
    return f'<g transform="translate({tx},{ty})">{symbol(flat)}{wordmark()}</g>'


def svg(viewbox, body, title, width=None, height=None):
    size = f' width="{width}" height="{height}"' if width else ""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}"{size}>'
        f"<title>{title}</title>{body}</svg>\n"
    )


def main():
    side = 338.66666
    (ROOT / "logo/toulouse-devops-logo.svg").write_text(
        svg(f"0 0 {side} {side}", logo_group(), "Toulouse DevOps", 1280, 1280)
    )
    # Symbol only: crop tightly around the infinity stroke, with a small margin.
    tx, ty = G9_TRANSLATE
    mark = f'<g transform="translate({tx},{ty})">{symbol()}</g>'
    (ROOT / "logo/toulouse-devops-mark.svg").write_text(
        svg("2 16 334 174", mark, "Toulouse DevOps", 1336, 696)
    )


if __name__ == "__main__":
    main()
