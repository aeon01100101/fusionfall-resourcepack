#!/usr/bin/env python3
"""v1.5 — SEPARATE the sky from Planet Fusion into their own files/layers.
Before: planet was baked into sky_day.png / sky_night.png.
Now (OptiFine/MCPatcher layer stack, world0):
  sky1 = sky_day.png          pure green day sky, NO planet      (replace, always)
  sky2 = sky_planet_day.png   ONLY his Planet Fusion, transparent (alpha, day window)
  sky3 = sky_night.png        pure night sky, NO planet           (alpha, night window)
  sky4 = sky_planet_night.png ONLY the planet, darkened           (alpha, night window)
world1 (End) unchanged — it never had a planet baked in.
His cutout pixels are used untouched (same source as v1.4).
"""
import json, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

BASE = os.path.expanduser("~/workspace/fusionfall-resourcepack")
SRC = os.path.join(BASE, "FusionFall-1.18.2")
cut = Image.open(os.path.join(BASE, "source-images/planet-from-github.png")).convert("RGBA")
bbox = cut.split()[3].getbbox()
cut = cut.crop(bbox)
print("cutout:", cut.size)

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

def planet_only(cx, cy, width, dark=1.0):
    """Transparent 1024 canvas carrying ONLY the planet (+ its soft goo glow)."""
    img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    p = cut.copy()
    p = p.resize((width, int(width * p.height / p.width)), Image.LANCZOS)
    p = p.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
    if dark != 1.0:
        rgb = ImageEnhance.Brightness(p.convert("RGB")).enhance(dark)
        p = Image.merge("RGBA", (*rgb.split(), p.split()[3]))
    glow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    r = int(width * 0.52)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(130, 255, 150, 60))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(45)))
    img.alpha_composite(p, (cx - p.width // 2, cy - p.height // 2))
    # edge feather: alpha tapers to 0 within 90px of every border (planet body is central, unaffected)
    import numpy as np
    arr = np.asarray(img).astype(float)
    yy, xx = np.mgrid[0:1024, 0:1024]
    dist = np.minimum(np.minimum(xx, 1023 - xx), np.minimum(yy, 1023 - yy))
    factor = np.clip(dist / 90.0, 0, 1) ** 0.5
    arr[:, :, 3] *= factor
    return Image.fromarray(arr.astype("uint8"), "RGBA")

# --- pure skies (no planet pasted) ---
day = gradient(1024, 1024, [(0.0, (13, 82, 58)), (0.35, (30, 152, 94)), (0.58, (70, 208, 132)),
                            (0.72, (178, 246, 188)), (0.80, (104, 196, 116)), (1.0, (15, 72, 34))])
rng = random.Random(11); d = ImageDraw.Draw(day)
for _ in range(500):
    d.point((rng.randrange(1024), rng.randrange(610)), fill=(215, 255, 200, 255))
night = gradient(1024, 1024, [(0.0, (2, 14, 8)), (0.45, (8, 44, 20)), (0.68, (20, 84, 34)),
                              (0.78, (44, 116, 48)), (1.0, (4, 26, 10))])
rng = random.Random(23); d = ImageDraw.Draw(night)
for _ in range(2600):
    d.point((rng.randrange(1024), rng.randrange(768)),
            fill=rng.choice([(255, 255, 255), (190, 255, 170), (120, 240, 120)]) + (255,))

planet_day = planet_only(735, 245, 420)
planet_night = planet_only(300, 240, 300, dark=0.55)

for root in ("optifine", "mcpatcher"):
    w0 = os.path.join(SRC, f"assets/minecraft/{root}/sky/world0")
    day.save(os.path.join(w0, "sky_day.png"))
    night.save(os.path.join(w0, "sky_night.png"))
    planet_day.save(os.path.join(w0, "sky_planet_day.png"))
    planet_night.save(os.path.join(w0, "sky_planet_night.png"))
    props = {
        "sky1.properties": "# Layer 1 - DAY SKY ONLY (pure green sky, no planet)\nsource=./sky_day.png\nblend=replace\nrotate=false\nweather=clear rain thunder\n",
        "sky2.properties": "# Layer 2 - PLANET FUSION ONLY, daytime (transparent elsewhere)\nsource=./sky_planet_day.png\nblend=alpha\nrotate=false\nstartFadeIn=4:30\nendFadeIn=5:30\nendFadeOut=19:30\nweather=clear rain thunder\n",
        "sky3.properties": "# Layer 3 - NIGHT SKY ONLY (pure dark-green sky, no planet)\nsource=./sky_night.png\nblend=alpha\nrotate=false\nstartFadeIn=17:30\nendFadeIn=19:30\nendFadeOut=5:30\nweather=clear rain thunder\n",
        "sky4.properties": "# Layer 4 - PLANET FUSION ONLY, night (darkened, transparent elsewhere)\nsource=./sky_planet_night.png\nblend=alpha\nrotate=false\nstartFadeIn=17:30\nendFadeIn=19:30\nendFadeOut=5:30\nweather=clear rain thunder\n",
    }
    for name, txt in props.items():
        open(os.path.join(w0, name), "w").write(txt)

with open(os.path.join(SRC, "pack.mcmeta"), "w") as f:
    json.dump({"pack": {"pack_format": 8,
                        "description": "§aFusionFall Theme §7v1.5 - sky & Planet Fusion in separate layers\n§7Turn OptiFine Custom Sky ON for the full green sky"}}, f)

# standalone copies for Isaiah
os.makedirs(os.path.join(BASE, "separate"), exist_ok=True)
day.save(os.path.join(BASE, "separate/sky-day.png"))
night.save(os.path.join(BASE, "separate/sky-night.png"))
planet_day.save(os.path.join(BASE, "separate/planet-fusion-day-layer.png"))
planet_night.save(os.path.join(BASE, "separate/planet-fusion-night-layer.png"))
cut.save(os.path.join(BASE, "separate/planet-fusion-cutout.png"))
print("separated: sky_day / sky_night are planet-free; planet lives in its own 2 layer files")
