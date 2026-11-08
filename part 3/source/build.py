"""Inline the VinUni logo and Carlito fonts into the slide template."""
import base64
import sys
from pathlib import Path

template, assets, out = (Path(p) for p in sys.argv[1:4])


def b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


html = template.read_text(encoding="utf-8")
html = html.replace("{{LOGO}}", "data:image/png;base64," + b64(assets / "vinuni_logo.png"))
html = html.replace("{{CARLITO_R}}", b64(assets / "fonts" / "Carlito-Regular.ttf"))
html = html.replace("{{CARLITO_B}}", b64(assets / "fonts" / "Carlito-Bold.ttf"))
html = html.replace("{{CARLITO_I}}", b64(assets / "fonts" / "Carlito-Italic.ttf"))
assert "{{" not in html, "unreplaced placeholder"
out.write_text(html, encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")
