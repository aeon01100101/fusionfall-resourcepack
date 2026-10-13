"""v1.8 - lava becomes Fusion Matter.

Vanilla 1.18.2 fluid geometry: lava_still.png 16x320 (20 frames of 16x16),
lava_flow.png 32x512 (16 frames of 32x32). Fields are built from integer-
frequency sinusoids only, so every frame tiles seamlessly in space and the
animation loops perfectly in time (period = frame count).
Palette: deep goo -> acid green -> glowing pale core.
Also: magma block as dark fusion rock with glowing green cracks.
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw

B = "FusionFall-1.18.2/assets/minecraft/textures/block/"
rng = np.random.default_rng(1182)

STOPS = [(0.00, (13, 71, 6)), (0.35, (30, 125, 8)), (0.60, (62, 196, 13)),
         (0.80, (107, 242, 36)), (0.93, (185, 255, 112)), (1.00, (234, 255, 192))]

def ramp(v):
    v = np.clip(v, 0, 1)
    out = np.zeros(v.shape + (3,))
    for (v0, c0), (v1, c1) in zip(STOPS, STOPS[1:]):
        m = (v >= v0) & (v <= v1)
        t = np.where(v1 > v0, (v - v0) / max(v1 - v0, 1e-9), 0)
        for ch in range(3):
            out[..., ch] = np.where(m, c0[ch] + (c1[ch] - c0[ch]) * t, out[..., ch])
    return out.astype(np.uint8)

def field(x, y, t, T, size, flow=False):
    """Periodic goo field in [~0, ~1]. x,y are coordinate grids of `size`."""
    ph = 2 * math.pi * t / T
    yy = y + (size * t / T if flow else 0)  # downward scroll for flow
    n1 = np.sin(2 * math.pi * (3 * x + 2 * yy) / size + 2 * ph)
    n2 = np.sin(2 * math.pi * (x - 3 * yy) / size - 3 * ph + 1.3)
    n3 = np.sin(2 * math.pi * (5 * yy) / size + 5 * ph + 0.7 * np.sin(2 * math.pi * 2 * x / size))
    F = 0.44 + 0.21 * n1 + 0.18 * n2 + 0.15 * n3
    # pulsing bubbles (torus distance -> tileable)
    for (bx, by, s, p) in [(3, 11, 2.2, 0.0), (11, 4, 1.8, 1.9), (7, 8, 1.5, 3.6), (13, 13, 2.0, 5.1)]:
        bx, by = bx * size / 16, by * size / 16
        dx = np.minimum(np.abs(x - bx), size - np.abs(x - bx))
        dy = np.minimum(np.abs(y - by), size - np.abs(y - by))
        F = F + 0.38 * np.exp(-(dx ** 2 + dy ** 2) / (2 * (s * size / 16) ** 2)) * (0.5 + 0.5 * np.sin(ph + p))
    if flow:  # vertical streaks so the flow direction reads
        F = F * (0.88 + 0.12 * np.sin(2 * math.pi * 7 * x / size))
    return F

# ---- lava_still: 20 frames, 16x16 ----
T = 20
strip = Image.new("RGBA", (16, 16 * T))
gx, gy = np.meshgrid(np.arange(16), np.arange(16))
for t in range(T):
    strip.paste(Image.fromarray(ramp(field(gx, gy, t, T, 16)), "RGB").convert("RGBA"), (0, 16 * t))
strip.save(B + "lava_still.png")
with open(B + "lava_still.png.mcmeta", "w") as f:
    json.dump({"animation": {"frametime": 3, "frames": list(range(T))}}, f)

# ---- lava_flow: 16 frames, 32x32 ----
T = 16
strip = Image.new("RGBA", (32, 32 * T))
gx, gy = np.meshgrid(np.arange(32), np.arange(32))
for t in range(T):
    strip.paste(Image.fromarray(ramp(field(gx, gy, t, T, 32, flow=True)), "RGB").convert("RGBA"), (0, 32 * t))
strip.save(B + "lava_flow.png")
with open(B + "lava_flow.png.mcmeta", "w") as f:
    json.dump({"animation": {"frametime": 2, "frames": list(range(T))}}, f)

# ---- magma block: dark fusion rock, glowing green cracks ----
rng2 = np.random.default_rng(4242)
base = np.zeros((16, 16, 3), dtype=int)
for yy in range(16):
    for xx in range(16):
        v = int(rng2.integers(-6, 7)); base[yy, xx] = (48 + v, 44 + v, 28 + v // 2)
img = Image.fromarray(base.astype(np.uint8), "RGB"); d = ImageDraw.Draw(img)
cracks = set()
for (sx, sy) in [(2,2),(8,1),(13,3),(1,8),(6,6),(11,9),(15,13),(3,13),(8,14),(13,7)]:
    x, y = sx, sy
    for _ in range(int(rng2.integers(5, 9))):
        cracks.add((x, y))
        x = min(15, max(0, x + int(rng2.integers(-1, 2)))); y = min(15, max(0, y + int(rng2.integers(-1, 2))))
for (x, y) in cracks:
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < 16 and 0 <= ny < 16 and (nx, ny) not in cracks: d.point((nx, ny), fill=(58, 128, 20))
for (x, y) in cracks: d.point((x, y), fill=(148, 252, 78))
hot = [p for p in cracks if sum((p[0]+dx, p[1]+dy) in cracks for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))) >= 2]
for p in hot[::2]: d.point(p, fill=(230, 255, 175))
img.convert("RGBA").save(B + "magma.png")
print("fusion-matter lava + magma written")
