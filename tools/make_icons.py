#!/usr/bin/env python3
"""Ritar appikoner och iPhone-startskärmar till docs/icons/ (kör en gång när utseendet ändras).

    python3 tools/make_icons.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "docs" / "icons"
FONT = HERE / "barlow-condensed-latin-700-normal.woff"
ASPHALT, ORANGE, INK, WHITE = (21, 25, 28), (242, 140, 0), (17, 17, 17), (238, 241, 242)


def plate(draw, cx, cy, w):
    """ADR-skylt: orange med svart kant och mittlinje, 'ADR' upptill och en bock nedtill."""
    h = w * 0.62
    b = max(2, round(w * 0.055))
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    draw.rounded_rectangle((x0, y0, x1, y1), radius=w * 0.05, fill=ORANGE, outline=INK, width=b)
    draw.line((x0, cy, x1, cy), fill=INK, width=round(b * 0.8))
    f = ImageFont.truetype(str(FONT), round(h * 0.42))
    draw.text((cx, y0 + h * 0.27), "ADR", font=f, fill=INK, anchor="mm")
    s, my = h * 0.15, cy + h * 0.23
    draw.line([(cx - s * 1.2, my), (cx - s * 0.3, my + s * 0.8), (cx + s * 1.4, my - s * 0.9)],
              fill=INK, width=round(b * 1.1), joint="curve")


def icon(size, scale, name):
    im = Image.new("RGB", (size, size), ASPHALT)
    plate(ImageDraw.Draw(im), size / 2, size / 2, size * scale)
    im.save(OUT / name)


def splash(w, h, name):
    im = Image.new("RGB", (w, h), ASPHALT)
    d = ImageDraw.Draw(im)
    pw = min(w, h) * 0.42
    plate(d, w / 2, h * 0.44, pw)
    f = ImageFont.truetype(str(FONT), round(pw * 0.26))
    d.text((w / 2, h * 0.44 + pw * 0.55), "ADR-kollen", font=f, fill=WHITE, anchor="mm")
    im.save(OUT / name, optimize=True)


OUT.mkdir(parents=True, exist_ok=True)
icon(180, 0.78, "apple-touch-icon.png")
icon(192, 0.78, "icon-192.png")
icon(512, 0.78, "icon-512.png")
icon(512, 0.58, "maskable-512.png")      # innehållet inom säkra zonen för runda ikoner
# iPhone-startskärmar (bredd, höjd i pixlar)
for w, h in [(1290, 2796), (1179, 2556), (1284, 2778), (1170, 2532), (1125, 2436), (1242, 2688), (828, 1792), (750, 1334), (1080, 2340)]:
    splash(w, h, f"splash-{w}x{h}.png")
print("klart:", sorted(p.name for p in OUT.iterdir()))
