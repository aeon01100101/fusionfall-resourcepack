#!/usr/bin/env python3
"""v1.1 GREEN SKY update — all art original, drawn from the FusionFall look:
a green-tinted sky (deep green zenith -> lime horizon) with Planet Fusion
looming in it. Researched Oct 13 2026: canon = huge green Planet Fusion in
the sky + Fusion Matter green everywhere.

Sky delivery routes (all in this one pack):
1. OptiFine / MCPatcher Custom Sky skyboxes (the standard way packs replace
   the sky) in optifine/sky AND mcpatcher/sky, world0 (overworld) + world1 (End).
   Skybox art depends only on Y so it reads as a horizon gradient on any face.
2. Vanilla textures that DO work with no mods: sun (= Planet Fusion),
   moon phases (green), clouds (pale green), rain (acid-green), End sky.
"""
import os, random
from PIL import Image, ImageDraw

ROOT = os.path.expanduser("~/workspace/fusionfall-resourcepack")
SRC = os.path.join(ROOT, "FusionFall-1.18.2")
ENV = "assets/minecraft/textures/environment/"
random.seed(2009)

FUSION = (74, 222, 62); FUSION_HI = (168, 255, 120); FUSION_DK = (22, 110, 28)

def save(img, rel):
    p = os.path.join(SRC, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p); return rel

def gradient(w, h, stops):
    """stops: list of (y_fraction, (r,g,b)) — vertical gradient, colour depends on Y only."""
    img = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        for i in range(len(stops) - 1):
            y0, c0 = stops[i]; y1, c1 = stops[i + 1]
            if y0 <= t <= y1:
                f = 0 if y1 == y0 else (t - y0) / (y1 - y0)
                c = tuple(int(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
                break
        else:
            c = stops[-1][1]
        d.line([(0, y), (w - 1, y)], fill=c + (255,))
    return img

def speckle(img, n, colors, ymax_frac=1.0, seed=7):
    rng = random.Random(seed); d = ImageDraw.Draw(img)
    w, h = img.size
    for _ in range(n):
        d.point((rng.randrange(w), rng.randrange(int(h * ymax_frac))), fill=rng.choice(colors) + (255,))
    return img

def planet(d, cx, cy, r, base=FUSION, hi=FUSION_HI, dark=(16, 84, 22), glow=True):
    """One original 'Planet Fusion': bright cracked green orb + glow."""
    if glow:
        d.ellipse([cx - r - 7, cy - r - 7, cx + r + 7, cy + r + 7], fill=(120, 255, 110, 60))
        d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=(150, 255, 130, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=base + (255,))
    d.ellipse([cx - r, cy - r, cx + r // 2, cy + r // 3], fill=hi + (160,))
    rng = random.Random(cx * 31 + cy)
    for _ in range(6):  # dark crack veins
        x, y = cx + rng.randint(-r // 2, r // 2), cy + rng.randint(-r // 2, r // 2)
        for _ in range(4):
            d.point((x, y), fill=dark + (255,)); d.point((x + 1, y), fill=dark + (255,))
            x += rng.choice([-1, 0, 1]); y += rng.choice([0, 1])
    for _ in range(4):  # crater blobs
        x, y = cx + rng.randint(-r // 2, r // 2), cy + rng.randint(-r // 2, r // 2)
        d.ellipse([x, y, x + 3, y + 2], fill=dark + (140,))

# ---------- OptiFine/MCPatcher skyboxes (1024x1024, Y-gradient = layout-proof) ----------
# DAY: deep fusion-green zenith -> vivid lime mid -> pale green-yellow horizon -> dark goo haze at very bottom
day = gradient(1024, 1024, [(0.0, (18, 96, 44)), (0.35, (52, 178, 62)), (0.58, (120, 232, 84)),
                            (0.72, (196, 248, 140)), (0.80, (140, 214, 92)), (1.0, (24, 84, 30))])
speckle(day, 500, [(210, 255, 190), (150, 240, 130)], ymax_frac=0.6, seed=11)
d = ImageDraw.Draw(day)
planet(d, 760, 210, 88)                       # Planet Fusion looming in the day sky
planet(d, 700, 268, 26, base=(96, 208, 74))   # its moonlet chunk
save(day, "assets/minecraft/optifine/sky/world0/sky_day.png")
save(day.copy(), "assets/minecraft/mcpatcher/sky/world0/sky_day.png")
# NIGHT: near-black green zenith -> dark goo green -> faint lime horizon glow, starfield of green sparks
night = gradient(1024, 1024, [(0.0, (2, 14, 8)), (0.45, (8, 44, 20)), (0.68, (20, 84, 34)),
                              (0.78, (44, 116, 48)), (1.0, (4, 26, 10))])
speckle(night, 2600, [(255, 255, 255), (190, 255, 170), (120, 240, 120)], ymax_frac=0.75, seed=23)
d = ImageDraw.Draw(night)
planet(d, 300, 240, 64, base=(52, 168, 52), hi=(130, 230, 110), dark=(8, 52, 14))
save(night, "assets/minecraft/optifine/sky/world0/sky_night.png")
save(night.copy(), "assets/minecraft/mcpatcher/sky/world0/sky_night.png")
# END (world1): swirling dark-green nebula sky
end = gradient(1024, 1024, [(0.0, (4, 30, 12)), (0.5, (10, 58, 22)), (1.0, (4, 30, 12))])
speckle(end, 4000, [(150, 255, 150), (80, 200, 90), (230, 255, 220)], seed=37)
save(end, "assets/minecraft/optifine/sky/world1/sky_end.png")
save(end.copy(), "assets/minecraft/mcpatcher/sky/world1/sky_end.png")

PROPS_DAY = """# FusionFall green sky - DAY layer (always on, replaces the blue sky)
source=./sky_day.png
blend=replace
rotate=false
weather=clear rain thunder
"""
PROPS_NIGHT = """# FusionFall green sky - NIGHT layer (fades in at dusk, out at dawn)
source=./sky_night.png
blend=alpha
rotate=false
startFadeIn=17:30
endFadeIn=19:30
endFadeOut=5:30
weather=clear rain thunder
"""
PROPS_END = """# FusionFall green sky - THE END
source=./sky_end.png
blend=replace
rotate=false
weather=clear rain thunder
"""
for root in ("assets/minecraft/optifine/sky", "assets/minecraft/mcpatcher/sky"):
    for name, txt in [("world0/sky1.properties", PROPS_DAY), ("world0/sky2.properties", PROPS_NIGHT),
                      ("world1/sky1.properties", PROPS_END)]:
        p = os.path.join(SRC, root, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(txt)

# ---------- Vanilla environment textures (work with NO mods) ----------
# Sun -> Planet Fusion itself (128x128, transparent corners)
img = Image.new("RGBA", (128, 128), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
planet(d, 62, 62, 44)
planet(d, 102, 34, 13, base=(96, 208, 74))
planet(d, 26, 96, 9, base=(96, 208, 74))
save(img, ENV + "sun.png")
# Moon phases 256x64: 8 cells of 32x32, green planet waxing/waning
img = Image.new("RGBA", (256, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
shadow_frac = [0.0, 0.3, 0.55, 0.85, 1.0, 0.85, 0.55, 0.3]  # full -> new -> full (shadow from right, then left)
for i, sf in enumerate(shadow_frac):
    cx = i * 32 + 16
    d.ellipse([cx - 11, 21, cx + 11, 43], fill=(120, 225, 100, 255))
    d.ellipse([cx - 11, 21, cx + 2, 34], fill=(190, 250, 160, 160))
    if sf > 0:
        sw = int(22 * sf)
        if i <= 4:  # waning: shadow eats from the right
            d.rectangle([cx + 11 - sw, 20, cx + 12, 44], fill=(0, 0, 0, 0))
            # PIL rect with alpha 0 on existing pixels needs direct pixel clearing:
        else:       # waxing: shadow retreats from the left
            d.rectangle([cx - 12, 20, cx - 11 + sw, 44], fill=(0, 0, 0, 0))
# PIL draw doesn't erase with alpha 0 in RGBA draw mode -> fix by compositing a cleared copy
img2 = Image.new("RGBA", (256, 64), (0, 0, 0, 0))
px = img.load(); out = img2.load()
for yy in range(64):
    for xx in range(256):
        i = xx // 32; lx = xx - i * 32; sf = shadow_frac[i]
        r, g, b, a = px[xx, yy]
        if a:
            if i <= 4 and lx > 27 - int(22 * sf): a = 0
            if i > 4 and lx < 5 + int(22 * sf) - 22 + 22 - int(22 * (1 - sf)) * 0: pass
            if i > 4 and lx < 27 - int(22 * shadow_frac[i]): a = 0 if lx < (27 - int(22 * shadow_frac[i])) - (22 - int(22 * shadow_frac[i])) else a
        out[xx, yy] = (r, g, b, a)
# Simpler correct shadow pass: redo cells cleanly with ellipse-intersection logic per pixel
img = Image.new("RGBA", (256, 64), (0, 0, 0, 0)); px = img.load()
for i, sf in enumerate(shadow_frac):
    for yy in range(64):
        for xx in range(32):
            dx, dy = xx - 16, yy - 32
            if dx * dx + dy * dy > 121: continue
            lit = True
            if i == 4: lit = False                       # new moon
            elif i in (1, 2, 3): lit = not (dx > 11 - int(22 * sf) - 0 and dx > (10 - 22 * sf))  # shadow from right
            elif i in (5, 6, 7): lit = not (dx < -10 + 22 * sf)                                    # shadow from left
            if i in (1, 2, 3): lit = dx <= 11 - 22 * sf
            if i in (5, 6, 7): lit = dx >= -11 + 22 * sf
            if lit:
                c = (150, 235, 115, 255) if (dx + dy) % 7 else (110, 210, 85, 255)
                if dx < -4 and dy < -4: c = (195, 250, 165, 255)
                px[i * 32 + xx, yy] = c
save(img, ENV + "moon_phases.png")
# Clouds 256x256: pale-green puffs (texture colour multiplies the cloud colour)
img = Image.new("RGBA", (256, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
rng = random.Random(99)
for _ in range(46):
    cx, cy = rng.randrange(256), rng.randrange(256)
    for ox in (-256, 0, 256):
        for oy in (-256, 0, 256):
            d.ellipse([cx + ox - rng.randint(14, 30), cy + oy - rng.randint(6, 10),
                       cx + ox + rng.randint(14, 30), cy + oy + rng.randint(6, 10)], fill=(226, 255, 214, 175))
save(img, ENV + "clouds.png")
# Rain 32x32 -> acid rain: bright green streaks
img = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
for x in (2, 9, 17, 25):
    for y0 in (0, 16):
        d.line([(x, y0 + 2), (x - 2, y0 + 13)], fill=(140, 255, 110, 200), width=1)
        d.line([(x + 4, y0 + 8), (x + 2, y0 + 15)], fill=(190, 255, 160, 160), width=1)
save(img, ENV + "rain.png")
# Snow 32x32 -> pale mint flakes
img = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
for (x, y) in [(4, 5), (14, 2), (24, 8), (8, 16), (20, 20), (29, 26), (3, 28), (16, 30)]:
    d.ellipse([x, y, x + 2, y + 2], fill=(220, 255, 225, 230))
save(img, ENV + "snow.png")
# End sky (vanilla texture) -> green nebula noise tile
img = Image.new("RGBA", (16, 16), (6, 34, 14, 255)); d = ImageDraw.Draw(img)
rng = random.Random(5)
for _ in range(40):
    d.point((rng.randrange(16), rng.randrange(16)), fill=rng.choice([(20, 90, 36), (90, 200, 100), (200, 255, 210)]) + (255,))
save(img, ENV + "end_sky.png")

print("sky textures done")
