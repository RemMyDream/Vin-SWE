"""Tile rendered slide PNGs into 2x2 contact sheets for review.
Usage: python make_grid.py <render_dir> [first last]"""
import sys, glob, os
from PIL import Image, ImageDraw
d = sys.argv[1]
files = sorted(glob.glob(os.path.join(d, "slide-*.png")))
if len(sys.argv) > 3:
    a, b = int(sys.argv[2]), int(sys.argv[3])
    files = [f for f in files if a <= int(os.path.basename(f)[6:8]) <= b]
W = 1000
out = []
for i in range(0, len(files), 4):
    chunk = files[i:i+4]
    ims = [Image.open(f).convert("RGB") for f in chunk]
    h = int(W * ims[0].height / ims[0].width)
    sheet = Image.new("RGB", (2 * W + 12, 2 * h + 12), "white")
    for k, (f, im) in enumerate(zip(chunk, ims)):
        im = im.resize((W, h), Image.LANCZOS)
        x, y = (k % 2) * (W + 12), (k // 2) * (h + 12)
        sheet.paste(im, (x, y))
        ImageDraw.Draw(sheet).rectangle([x, y, x + 60, y + 26], fill="black")
        ImageDraw.Draw(sheet).text((x + 8, y + 6), os.path.basename(f)[6:8], fill="white")
    p = os.path.join(d, f"grid-{i//4+1:02d}.png")
    sheet.save(p)
    out.append(p)
print("\n".join(out))
