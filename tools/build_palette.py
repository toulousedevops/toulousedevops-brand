"""Export the brand palette as JSON, CSS, SCSS and GIMP/Inkscape palette files."""

import json
from pathlib import Path

from brand import PALETTE

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "colors"


def rgb(hex_):
    h = hex_.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def main():
    OUT.mkdir(exist_ok=True)
    data = {k: {**v, "rgb": list(rgb(v["hex"]))} for k, v in PALETTE.items()}
    (OUT / "palette.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    css = ["/* Toulouse DevOps brand palette */", ":root {"]
    css += [f"  --tdo-{k}: {v['hex']}; /* {v['name']} – {v['usage']} */" for k, v in PALETTE.items()]
    css.append("}")
    (OUT / "palette.css").write_text("\n".join(css) + "\n")

    scss = ["// Toulouse DevOps brand palette"]
    scss += [f"$tdo-{k}: {v['hex']}; // {v['name']}" for k, v in PALETTE.items()]
    (OUT / "palette.scss").write_text("\n".join(scss) + "\n")

    gpl = ["GIMP Palette", "Name: Toulouse DevOps", "Columns: 4", "#"]
    gpl += ["{:3d} {:3d} {:3d}\t{}".format(*rgb(v["hex"]), v["name"]) for v in PALETTE.values()]
    (OUT / "toulouse-devops.gpl").write_text("\n".join(gpl) + "\n")


if __name__ == "__main__":
    main()
