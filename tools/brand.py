"""Shared brand constants: colour palette and the logo symbol geometry.

The symbol geometry is taken verbatim from the Inkscape source file
(logo/source/logo-toulouse-devops-2026.inkscape.svg), layer "g8".
"""

PALETTE = {
    "primary": {"name": "Bleu principal", "hex": "#0e2d5a", "usage": "Titles, main elements, footer"},
    "accent": {"name": "Rouge accent", "hex": "#c83737", "usage": "CTAs, badges, attention elements"},
    "primary-light": {"name": "Bleu clair", "hex": "#1a4a8a", "usage": "Hover, links, secondary accents"},
    "primary-pale": {"name": "Bleu pâle", "hex": "#e8eef5", "usage": "Section backgrounds, cards"},
    "accent-light": {"name": "Rouge clair", "hex": "#e85555", "usage": "CTA hover"},
    "accent-pale": {"name": "Rouge pâle", "hex": "#fdf2f2", "usage": "Alerts, notifications"},
    "text": {"name": "Gris texte", "hex": "#374151", "usage": "Body text"},
    "text-light": {"name": "Gris clair", "hex": "#6b7280", "usage": "Secondary text, captions"},
    "background": {"name": "Fond de page", "hex": "#fafbfc", "usage": "Page background"},
    "surface": {"name": "Surface", "hex": "#ffffff", "usage": "Cards, containers"},
    "border": {"name": "Bordure", "hex": "#e5e7eb", "usage": "Borders, separators"},
}

C = {k: v["hex"] for k, v in PALETTE.items()}

# Occitan cross (path + 12 pommels), in its own 0..800 coordinate system.
_CROSS_PATH = (
    "m 183.175,267 9.125,7.138 c 14.633,11.443 38.502,35.909 45.015,77.3 l 1.722,10.924 8.36,-7.312 "
    "c 14.038,-12.277 55.754,-44.434 116.757,-53.224 -8.792,61.003 -40.948,102.718 -53.224,116.756 "
    "l -7.312,8.361 10.924,1.721 c 41.392,6.515 65.857,30.383 77.301,45.015 l 7.137,9.126 7.138,-9.126 "
    "c 11.442,-14.632 35.907,-38.5 77.299,-45.015 l 10.924,-1.721 -7.312,-8.361 "
    "c -12.276,-14.038 -44.432,-55.753 -53.224,-116.756 61.003,8.79 102.719,40.947 116.756,53.224 "
    "l 8.361,7.312 1.721,-10.924 c 6.514,-41.391 30.383,-65.857 45.014,-77.3 l 9.127,-7.138 -9.127,-7.138 "
    "c -14.631,-11.443 -38.5,-35.908 -45.014,-77.299 l -1.721,-10.925 -8.361,7.312 "
    "c -14.037,12.277 -55.753,44.434 -116.756,53.225 8.792,-61.003 40.948,-102.719 53.224,-116.756 "
    "l 7.312,-8.362 -10.924,-1.72 C 442.025,98.821 417.56,74.953 406.118,60.321 l -7.138,-9.126 -7.137,9.126 "
    "c -11.444,14.632 -35.909,38.5 -77.301,45.016 l -10.924,1.72 7.312,8.362 "
    "c 12.276,14.037 44.432,55.753 53.224,116.756 -61.003,-8.791 -102.719,-40.948 -116.757,-53.225 "
    "l -8.36,-7.312 -1.722,10.925 c -6.513,41.391 -30.382,65.856 -45.015,77.299 z "
    "m 35.125,0 c 27.829,-25.798 34.256,-54.425 34.256,-54.425 40.625,34.242 103.986,41.96 135.664,43.666 "
    "-1.707,-31.679 -9.424,-95.039 -43.665,-135.666 0,0 28.625,-6.425 54.425,-34.255 "
    "25.799,27.83 54.424,34.255 54.424,34.255 -34.241,40.627 -41.958,103.987 -43.665,135.666 "
    "31.678,-1.706 95.039,-9.424 135.665,-43.666 0,0 6.425,28.627 34.255,54.425 "
    "-27.83,25.799 -34.255,54.425 -34.255,54.425 -40.626,-34.242 -103.987,-41.96 -135.665,-43.666 "
    "1.707,31.679 9.424,95.039 43.665,135.666 0,0 -28.625,6.425 -54.424,34.255 "
    "-25.8,-27.83 -54.425,-34.255 -54.425,-34.255 34.241,-40.627 41.958,-103.987 43.665,-135.666 "
    "-31.678,1.706 -95.039,9.424 -135.664,43.666 0,0 -6.427,-28.626 -34.256,-54.425 z"
)


def _cross_pommels():
    import re
    from pathlib import Path

    # Pommel centres are read from the source file so they stay in sync.
    src = Path(__file__).resolve().parent.parent / "logo/source/logo-toulouse-devops-2026.inkscape.svg"
    text = src.read_text()
    block = text[text.index('id="g13-6"'):]
    block = block[: block.index("</g>")]
    circles = re.findall(r'cx="([\d.]+)"\s+cy="([\d.]+)"\s+r="([\d.]+)"', block)
    return circles


def cross(fill):
    """Occitan cross in its native 0..800 coordinate system."""
    pommels = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>' for cx, cy, r in _cross_pommels())
    return f'<g fill="{fill}"><path d="{_CROSS_PATH}"/>{pommels}</g>'


# Infinity loop with the four white "flow" chevrons, in logo coordinates.
INFINITY_PATH = (
    "M 301.06836,128.13795 C 318.7132,100.30018 311.60363,63.533855 284.85281,44.280957 "
    "258.10198,25.028057 220.9809,29.961064 200.18672,55.532203 148.95291,104.41122 158.76459,123.79479 "
    "129.13105,145.89083 90.466985,165.23714 54.182915,155.97569 36.538065,128.13793 "
    "18.893225,100.30018 26.002785,63.533855 52.753615,44.280961 c 26.75082,-19.2529 63.871915,-14.319892 "
    "84.666095,11.251247 20.05019,22.55472 41.19561,64.325102 80.30389,93.122182 "
    "29.41583,16.58275 65.69991,7.32131 83.34476,-20.51644 z"
)
CHEVRONS = [
    "m 58.984535,58.186643 -23.11643,6.577573 -4.23926,-24.042399",
    "m 298.97223,37.467892 5.67186,23.355173 -24.18931,3.299247",
    "m 55.137175,130.66353 4.46037,23.61651 -24.32722,2.04792",
    "m 299.91715,155.67193 -24.03232,-0.28596 2.7912,-24.25318",
]


# Colour of the navy loop seen through the 85 % white disc (flattened).
_LOOP_UNDER_DISC = "#dbe0e6"


def symbol(flat=False):
    """The logo symbol (infinity + Occitan cross), in logo coordinates.

    Matches the Inkscape group g8 (before the g9 translate).

    With flat=True the semi-transparent white disc behind the cross is
    replaced by opaque shapes giving the same result on a white background,
    so print files contain no transparency.
    """
    chevrons = "".join(f'<path d="{d}"/>' for d in CHEVRONS)
    loop = (
        f'd="{INFINITY_PATH}" fill="none" stroke-width="24.0499" '
        f'stroke-linecap="round" stroke-linejoin="round"'
    )
    disc = 'cx="168.01363" cy="96.00174" r="68.072556"'
    if flat:
        disc_svg = (
            f'<clipPath id="tdo-disc"><circle {disc}/></clipPath>'
            f'<circle {disc} fill="#ffffff"/>'
            f'<path {loop} stroke="{_LOOP_UNDER_DISC}" clip-path="url(#tdo-disc)"/>'
        )
    else:
        disc_svg = f'<circle {disc} fill="#ffffff" fill-opacity="0.85"/>'
    return (
        f'<path {loop} stroke="{C["primary"]}"/>'
        f'<g fill="none" stroke="#ffffff" stroke-width="5">{chevrons}</g>'
        f'{disc_svg}'
        f'<g transform="matrix(0.22853119,0,0,0.22853119,77.479965,34.98386)">{cross(C["accent"])}</g>'
    )
