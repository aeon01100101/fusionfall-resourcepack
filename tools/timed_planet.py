"""v1.7 - Planet Fusion rotation correlates with Minecraft time of day.

Layer stack (world0, both optifine + mcpatcher trees):
  sky1  day sky base (replace, always)
  sky2  night sky base (alpha, fades in 17:30-19:30, out by 5:30)
  sky3..sky11  the 9 rotation PNGs, one per 2h40m slice of the 24h cycle,
               crossfading +/-15 min around each boundary, with daylight
               brightness baked per slice (dim at night, full at noon).
OptiFine time reference (official sky.properties doc):
  sunrise 6:00 = tick 0, noon 12:00 = 6000, sunset 18:00 = 12000,
  midnight 0:00 = 18000. Layers load until a missing number: 1..11 contiguous.
"""
import os, shutil
import numpy as np
from PIL import Image

BASE = "FusionFall-1.18.2/assets/minecraft"
TREES = [f"{BASE}/optifine/sky/world0", f"{BASE}/mcpatcher/sky/world0"]
ROT_DIR = "rotations"
BRIGHT = [0.50, 0.52, 0.75, 0.95, 1.00, 0.95, 0.85, 0.60, 0.50]  # per slice
CX, CY, DRAW = 362, 238, 610  # planet centre + drawn size of the 180px rot canvas

def fmt(m):
    m %= 1440
    return f"{m//60}:{m%60:02d}"

def build_layer_png(rot_path, bright):
    rot = Image.open(rot_path).convert("RGBA")  # 180x180, content centred
    arr = np.asarray(rot).astype(float)
    arr[:, :, :3] *= bright
    rot = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((DRAW, DRAW), Image.LANCZOS)
    layer = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    layer.alpha_composite(rot, (CX - DRAW // 2, CY - DRAW // 2))
    return layer

for tree in TREES:
    # remove the old two-layer planet setup
    for f in ("sky_planet_day.png", "sky_planet_night.png",
              "sky2.properties", "sky4.properties"):
        p = os.path.join(tree, f)
        if os.path.exists(p):
            os.remove(p)
    # sky2 = night base (was layer 3 in v1.5)
    with open(os.path.join(tree, "sky2.properties"), "w") as f:
        f.write("# Layer 2 - NIGHT SKY ONLY (pure dark-green sky, no planet)\n"
                "source=./sky_night.png\nblend=alpha\nrotate=false\n"
                "startFadeIn=17:30\nendFadeIn=19:30\nendFadeOut=5:30\n"
                "weather=clear rain thunder\n")
    # sky3..sky11 = rotation time slices
    for i in range(9):
        ang = i * 40
        layer = build_layer_png(f"{ROT_DIR}/planet-fusion-rot-{ang:03d}.png", BRIGHT[i])
        layer.save(os.path.join(tree, f"sky_planet_rot_{ang:03d}.png"))
        start, end = i * 160, i * 160 + 160
        with open(os.path.join(tree, f"sky{i+3}.properties"), "w") as f:
            f.write(f"# Layer {i+3} - Planet Fusion rotation {ang:03d} deg, "
                    f"game time {fmt(start)}-{fmt(end)} (brightness {BRIGHT[i]:.2f})\n"
                    f"source=./sky_planet_rot_{ang:03d}.png\nblend=alpha\nrotate=false\n"
                    f"startFadeIn={fmt(start-15)}\nendFadeIn={fmt(start+15)}\n"
                    f"endFadeOut={fmt(end+15)}\nweather=clear rain thunder\n")
    print(tree, "->", sorted(os.listdir(tree)))
print("v1.7 layers built")
