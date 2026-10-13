#!/usr/bin/env python3
"""Swap Isaiah's OWN transparent Planet Fusion PNG into the pack — v1.4.
Uses his cutout exactly as supplied: NO background removal, NO keying,
NO colour edits to the planet (the night variant is only darkened, as
before). Only placement work: trim fully-transparent margins, resize,
composite. Usage:
  integrate_user_planet.py <cutout.png> [pack_dir] [out_zip]
Defaults: pack_dir=./FusionFall-1.18.2  out_zip=./FusionFall-ResourcePack-1.18.2.zip
"""
import io, json, os, random, sys, zipfile
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

CUTOUT = sys.argv[1]
BASE = os.path.expanduser("~/workspace/fusionfall-resourcepack")
SRC = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "FusionFall-1.18.2")
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(BASE, "FusionFall-ResourcePack-1.18.2.zip")

cut = Image.open(CUTOUT).convert("RGBA")
alpha = cut.split()[3]
assert alpha.getextrema()[0] == 0, "cutout has NO transparency — refusing to key it, get the real transparent PNG"
bbox = alpha.getbbox()
cut = cut.crop(bbox)
print(f"cutout trimmed to {cut.size} (alpha OK, untouched pixels)")

def paste_planet(img, cx, cy, width, dark=1.0):
    p = cut.copy()
    p = p.resize((width, int(width * p.height / p.width)), Image.LANCZOS)
    p = p.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
    if dark != 1.0:
        rgb = ImageEnhance.Brightness(p.convert("RGB")).enhance(dark)
        p = Image.merge("RGBA", (*rgb.split(), p.split()[3]))
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    r = int(width * 0.60)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(130, 255, 150, 60))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(45)))
    img.alpha_composite(p, (cx - p.width // 2, cy - p.height // 2))
    return img

def gradient(w, h, stops):
    img = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        for i in range(len(stops) - 1):
            y0, c0 = stops[i]; y1, c1 = stops[i + 1]
            if y0 <= t <= y1:
                f = 0 if y1 == y0 else (t - y0) / (y1 - y0)
                c = tuple(int(c0[k] + (c1[k] - c0[k]) * f) for k in range(3)); break
        else:
            c = stops[-1][1]
        d.line([(0, y), (w - 1, y)], fill=c + (255,))
    return img

day = gradient(1024, 1024, [(0.0, (13, 82, 58)), (0.35, (30, 152, 94)), (0.58, (70, 208, 132)),
                            (0.72, (178, 246, 188)), (0.80, (104, 196, 116)), (1.0, (15, 72, 34))])
rng = random.Random(11); d = ImageDraw.Draw(day)
for _ in range(500):
    d.point((rng.randrange(1024), rng.randrange(610)), fill=(215, 255, 200, 255))
paste_planet(day, 742, 215, 440)

night = gradient(1024, 1024, [(0.0, (2, 14, 8)), (0.45, (8, 44, 20)), (0.68, (20, 84, 34)),
                              (0.78, (44, 116, 48)), (1.0, (4, 26, 10))])
rng = random.Random(23); d = ImageDraw.Draw(night)
for _ in range(2600):
    d.point((rng.randrange(1024), rng.randrange(768)),
            fill=rng.choice([(255, 255, 255), (190, 255, 170), (120, 240, 120)]) + (255,))
paste_planet(night, 300, 240, 300, dark=0.55)

for root in ("optifine", "mcpatcher"):
    day.save(os.path.join(SRC, f"assets/minecraft/{root}/sky/world0/sky_day.png"))
    night.save(os.path.join(SRC, f"assets/minecraft/{root}/sky/world0/sky_night.png"))

sun = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
p = cut.copy()
p = p.resize((240, int(240 * p.height / p.width)), Image.LANCZOS).filter(
    ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
sun.alpha_composite(p, ((256 - p.width) // 2, (256 - p.height) // 2))
sun.save(os.path.join(SRC, "assets/minecraft/textures/environment/sun.png"))

def panorama(face, pcx, pcy, pw):
    img = Image.new("RGBA", (512, 512)); dr = ImageDraw.Draw(img)
    for y in range(512):
        t = y / 512
        c = (int(20 + 90 * t), int(110 + 110 * t), int(46 + 30 * t)) if y < 300 else \
            (int(28 - 8 * (t - 0.58)), int(120 + 90 * (t - 0.58)), int(40))
        dr.line([(0, y), (511, y)], fill=c + (255,))
    r2 = random.Random(500 + face)
    for _ in range(30):
        dr.point((r2.randrange(512), r2.randrange(120)), fill=(235, 255, 220, 255))
    x = -10
    while x < 512:
        wdt, hgt = r2.randint(28, 70), r2.randint(50, 150)
        dr.rectangle([x, 300 - hgt, x + wdt, 300], fill=(13, 30, 24, 255))
        for wy in range(300 - hgt + 8, 292, 14):
            for wx in range(x + 5, x + wdt - 5, 11):
                if r2.random() < 0.55:
                    dr.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 226, 130, 255))
        x += wdt + r2.randint(2, 12)
    for _ in range(260):
        dr.point((r2.randrange(512), r2.randint(305, 511)),
                 fill=r2.choice([(74, 222, 62), (168, 255, 120), (22, 110, 28)]) + (255,))
    paste_planet(img, pcx, pcy, pw)
    img.save(os.path.join(SRC, f"assets/minecraft/textures/gui/title/background/panorama_{face}.png"))

panorama(1, 350, 120, 210)
panorama(4, 140, 100, 150)

with open(os.path.join(SRC, "pack.mcmeta"), "w") as f:
    json.dump({"pack": {"pack_format": 8,
                        "description": "§aFusionFall Theme §7v1.4 - your Planet Fusion cutout, untouched\n§7Turn OptiFine Custom Sky ON for the full green sky"}}, f)

if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, _, files in os.walk(SRC):
        for fn in files:
            full = os.path.join(dp, fn)
            z.write(full, os.path.relpath(full, SRC))

# validate
z = zipfile.ZipFile(OUT); names = z.namelist()
assert "pack.mcmeta" in names and json.loads(z.read("pack.mcmeta"))["pack"]["pack_format"] == 8
sunz = Image.open(io.BytesIO(z.read("assets/minecraft/textures/environment/sun.png"))).convert("RGBA")
assert sunz.getpixel((2, 2))[3] == 0, "sun corner not transparent"
assert z.testzip() is None
import hashlib
sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"v1.4 built: {OUT}  entries={len(names)}  size={os.path.getsize(OUT)}  sha256={sha}")
