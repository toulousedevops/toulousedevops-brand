"""Generate the Toulouse DevOps roll-up banner (kakemono), 850 x 2000 mm.

All text is converted to outlines so the SVG/PDF render identically on any
machine, including the print shop's RIP. One SVG user unit = 1 mm.

Output: kakemono/toulouse-devops-kakemono-85x200.svg
"""

from pathlib import Path

import segno

from brand import C, cross
from build_logo import logo_group
from textpath import font

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "kakemono/toulouse-devops-kakemono-85x200.svg"

W, H = 850, 2000
MARGIN = 70  # side safe margin (mm)
CONTENT_W = W - 2 * MARGIN

SITE_URL = "https://toulouse-devops.org/"

ubuntu_bold = font("Ubuntu-Bold.ttf")
ubuntu_medium = font("Ubuntu-Medium.ttf")
inter = font("Inter-VariableFont_opsz,wght.ttf", wght=400, opsz=32)
inter_semi = font("Inter-VariableFont_opsz,wght.ttf", wght=600, opsz=32)

TOPICS = [
    "CI/CD", "Kubernetes", "Cloud", "Infra as Code", "Observabilité",
    "SRE", "Sécurité", "FinOps",
]

parts = []


def text(f, s, x, y, size, fill, anchor="start", tracking=0.0):
    parts.append(f'<path d="{f.path(s, x, y, size, anchor, tracking)}" fill="{fill}"/>')


def fit(f, s, size, max_w):
    """Largest size <= `size` so that `s` fits in `max_w`."""
    w = f.width(s, size)
    return size if w <= max_w else size * max_w / w


def wrap(f, s, size, max_w):
    lines, cur = [], ""
    for word in s.split():
        cand = f"{cur} {word}".strip()
        if cur and f.width(cand, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    lines.append(cur)
    return lines


def qr_path(data, x, y, size):
    qr = segno.make(data, error="m", boost_error=False)
    matrix = list(qr.matrix)
    n = len(matrix)
    m = size / n
    d = []
    for r, row in enumerate(matrix):
        c = 0
        while c < n:
            if row[c]:
                start = c
                while c < n and row[c]:
                    c += 1
                d.append(f"M{x + start * m:.3f} {y + r * m:.3f}h{(c - start) * m:.3f}v{m:.3f}h{-(c - start) * m:.3f}z")
            else:
                c += 1
    return "".join(d)


def build():
    # Vertical positions are in mm from the top. With the banner standing on
    # its base, height above the floor is roughly 2050 - y.

    # ---- Background --------------------------------------------------------
    parts.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

    # ---- Logo (official artwork, transparency flattened for print) ----------
    logo_w = 540
    s = logo_w / 338.66666
    parts.append(
        f'<g transform="translate({(W - logo_w) / 2:.3f},45) scale({s:.5f})">{logo_group(flat=True)}</g>'
    )

    # ---- Tagline ------------------------------------------------------------
    tagline = "Un meetup gratuit chaque mois"
    size = fit(ubuntu_bold, tagline, 58, CONTENT_W)
    text(ubuntu_bold, tagline, W / 2, 615, size, C["primary"], "middle")
    parts.append(f'<rect x="{W / 2 - 45}" y="645" width="90" height="7" rx="3.5" fill="{C["accent"]}"/>')
    text(inter, "Ouvert à tous · Talks · Pizza", W / 2, 712, 36, C["text"], "middle")

    # ---- Navy panel with a wave edge (echoes the infinity loop) -------------
    wave = "M0 800 C 250 735, 600 865, 850 780"
    panel = f"{wave} L850 {H} L0 {H} Z"
    parts.append(f'<clipPath id="panel"><path d="{panel}"/></clipPath>')
    parts.append(f'<path d="{panel}" fill="{C["primary"]}"/>')
    parts.append(
        f'<path d="M0 772 C 250 707, 600 837, 850 752" fill="none" '
        f'stroke="{C["accent"]}" stroke-width="7" stroke-linecap="round"/>'
    )
    # Large Occitan cross rising from the bottom edge, centred: a deliberate
    # emblem filling the low area that the roll-up base partly hides. Its
    # colour sits between Bleu principal and Bleu clair (solid, no opacity).
    cs = 1.5
    cx_native, cy_native = 399.0, 267.0  # cross centre in its own coordinates
    parts.append(
        f'<g clip-path="url(#panel)">'
        f'<g transform="translate({W / 2 - cx_native * cs:.2f},{2030 - cy_native * cs:.2f}) scale({cs})">'
        f'{cross("#163d74")}</g></g>'
    )

    # ---- Join card with QR code: at ~95-125 cm from the floor ---------------
    card_y, card_h = 850, 300
    parts.append(
        f'<rect x="{MARGIN}" y="{card_y}" width="{CONTENT_W}" height="{card_h}" rx="26" fill="#ffffff"/>'
    )
    # 30 mm padding keeps a quiet zone of > 4 modules around the code.
    qr_size = card_h - 60
    qx, qy = MARGIN + 30, card_y + 30
    parts.append(f'<path d="{qr_path(SITE_URL, qx, qy, qr_size)}" fill="{C["primary"]}"/>')
    tx = qx + qr_size + 40
    tw = MARGIN + CONTENT_W - 30 - tx
    text(ubuntu_bold, "Rejoins-nous !", tx, card_y + 122, fit(ubuntu_bold, "Rejoins-nous !", 60, tw), C["primary"])
    parts.append(f'<rect x="{tx}" y="{card_y + 148}" width="64" height="6" rx="3" fill="{C["accent"]}"/>')
    text(inter_semi, "toulouse-devops.org", tx, card_y + 222, fit(inter_semi, "toulouse-devops.org", 42, tw), C["accent"])

    # ---- Key figures --------------------------------------------------------
    col_w = CONTENT_W / 3
    stats = [("40", "meetups"), ("2000", "membres"), ("100", "talks")]
    num_size = min(fit(ubuntu_bold, n + "+", 86, col_w - 16) for n, _ in stats)
    for i, (num, label) in enumerate(stats):
        cx = MARGIN + col_w * (i + 0.5)
        wn = ubuntu_bold.width(num, num_size)
        wp = ubuntu_bold.width("+", num_size)
        x0 = cx - (wn + wp) / 2
        text(ubuntu_bold, num, x0, 1285, num_size, "#ffffff")
        text(ubuntu_bold, "+", x0 + wn, 1285, num_size, C["accent-light"])
        text(inter_semi, label.upper(), cx, 1333, 24, C["primary-pale"], "middle", tracking=0.08)

    # ---- Topic chips --------------------------------------------------------
    chip_size, chip_h, pad, gap = 24, 54, 24, 14
    rows, cur, cur_w = [], [], 0.0
    for t in TOPICS:
        w = inter_semi.width(t, chip_size) + 2 * pad
        if cur and cur_w + gap + w > CONTENT_W:
            rows.append((cur, cur_w))
            cur, cur_w = [], 0.0
        cur_w += (gap if cur else 0) + w
        cur.append((t, w))
    rows.append((cur, cur_w))
    y = 1400
    for row, row_w in rows:
        x = (W - row_w) / 2
        for t, w in row:
            parts.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{chip_h}" rx="{chip_h / 2}" '
                f'fill="{C["primary-light"]}" stroke="{C["primary-pale"]}" stroke-width="1.5"/>'
            )
            text(inter_semi, t, x + w / 2, y + chip_h / 2 + chip_size * 0.36, chip_size, "#ffffff", "middle")
            x += w + gap
        y += chip_h + gap

    # ---- Call for speakers --------------------------------------------------
    y += 34
    cta = "Envie de partager ? Propose ton talk !"
    cta_size = 32
    cta_w = ubuntu_medium.width(cta, cta_size) + 70
    # Keep clear of the bottom ~80 mm, which sits in/near the roll-up base.
    assert y + 76 <= 1920, f"layout overflows: CTA ends at {y + 76:.0f} mm"
    parts.append(
        f'<rect x="{(W - cta_w) / 2:.2f}" y="{y:.2f}" width="{cta_w:.2f}" height="76" rx="38" fill="{C["accent"]}"/>'
    )
    text(ubuntu_medium, cta, W / 2, y + 38 + cta_size * 0.35, cta_size, "#ffffff", "middle")

    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">'
        "<title>Toulouse DevOps – kakemono 85 x 200 cm</title>"
        + "".join(parts)
        + "</svg>\n"
    )
    OUT.write_text(svg)


if __name__ == "__main__":
    build()
