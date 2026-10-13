"""v1.9 - lava built from Isaiah's actual Fusion Matter texture
(CNUF-Fusion-Matter-Texture.webp from his aeon01100101/Dump repo).
The image is made seamlessly tileable (4-shift tent blend), then:
  lava_still 20 frames 16x16 - slow upward roll + gentle pulse
  lava_flow  16 frames 32x32 - faster downward roll
  magma      the same texture, darkened, under the v1.8 crack network
"""
import json
import numpy as np
from PIL import Image, ImageDraw

B = "FusionFall-1.18.2/assets/minecraft/textures/block/"
src = Image.open("source-images/fusion-matter-user.webp").convert("RGBA")
arr = np.asarray(src).astype(float)
opaque = arr[:, :, 3] > 128
mean = arr[opaque][:, :3].mean(0) if opaque.any() else (20, 200, 40)
bg = np.zeros_like(arr); bg[:, :, :3] = mean; bg[:, :, 3] = 255
alpha = (arr[:, :, 3:4] / 255.0)
comp = Image.fromarray((arr[:, :, :3] * alpha + bg[:, :, :3] * (1 - alpha)).astype(np.uint8), "RGB")
print("transparent share composited over mean green", mean.round(0), ":", round(1 - float(opaque.mean()), 3))

# square crop -> 256, then seamless via 4-shift tent blend
s = min(comp.size)
comp = comp.crop(((comp.width - s) // 2, (comp.height - s) // 2,
                  (comp.width - s) // 2 + s, (comp.height - s) // 2 + s)).resize((256, 256), Image.LANCZOS)
A = np.asarray(comp).astype(float)
wy = np.linspace(0, 1, 256)[:, None, None]; wx = np.linspace(0, 1, 256)[None, :, None]
T = (A * (1 - wx) * (1 - wy) + np.roll(A, 128, 1) * wx * (1 - wy)
     + np.roll(A, 128, 0) * (1 - wx) * wy + np.roll(np.roll(A, 128, 0), 128, 1) * wx * wy)
tile = Image.fromarray(T.astype(np.uint8), "RGB")
tile.save("source-images/fusion-matter-tileable.png")

def frame(size, dy, pulse):
    rolled = tile.transform((256, 256), Image.AFFINE, (1, 0, 0, 0, 1, -dy), resample=Image.BICUBIC) \
        if False else Image.fromarray(np.roll(T, dy, 0).astype(np.uint8), "RGB")
    f = np.asarray(rolled.resize((size, size), Image.LANCZOS)).astype(float) * pulse
    return Image.fromarray(np.clip(f, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

strip = Image.new("RGBA", (16, 16 * 20))
for t in range(20):
    strip.paste(frame(16, int(t * 256 / 20), 1 + 0.05 * np.sin(2 * np.pi * t / 20)), (0, 16 * t))
strip.save(B + "lava_still.png")
with open(B + "lava_still.png.mcmeta", "w") as f:
    json.dump({"animation": {"frametime": 3, "frames": list(range(20))}}, f)

strip = Image.new("RGBA", (32, 32 * 16))
for t in range(16):
    strip.paste(frame(32, -int(t * 256 / 16), 1.0), (0, 32 * t))
strip.save(B + "lava_flow.png")
with open(B + "lava_flow.png.mcmeta", "w") as f:
    json.dump({"animation": {"frametime": 2, "frames": list(range(16))}}, f)

# magma: his texture darkened to cooled rock + glowing crack network (v1.8 pattern)
dark = Image.fromarray((np.asarray(tile.resize((16, 16), Image.LANCZOS)).astype(float) * 0.30).astype(np.uint8), "RGB")
d = ImageDraw.Draw(dark)
rng = np.random.default_rng(4242)
cracks = set()
for (sx, sy) in [(2, 2), (8, 1), (13, 3), (1, 8), (6, 6), (11, 9), (15, 13), (3, 13), (8, 14), (13, 7)]:
    x, y = sx, sy
    for _ in range(int(rng.integers(5, 9))):
        cracks.add((x, y))
        x = min(15, max(0, x + int(rng.integers(-1, 2)))); y = min(15, max(0, y + int(rng.integers(-1, 2))))
for (x, y) in cracks:
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < 16 and 0 <= ny < 16 and (nx, ny) not in cracks: d.point((nx, ny), fill=(58, 128, 20))
for (x, y) in cracks: d.point((x, y), fill=(148, 252, 78))
hot = [p for p in cracks if sum((p[0] + dx, p[1] + dy) in cracks for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 2]
for p in hot[::2]: d.point(p, fill=(230, 255, 175))
dark.convert("RGBA").save(B + "magma.png")
print("lava rebuilt from his fusion matter texture")
