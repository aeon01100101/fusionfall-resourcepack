#!/usr/bin/env python3
"""
FusionFall-themed resource pack for Minecraft 1.18.2 — ALL ART ORIGINAL.
Every texture below is drawn pixel-by-pixel with Pillow from a palette.
No assets are copied/ripped from FusionFall, Cartoon Network, or vanilla
Minecraft (vanilla textures are replaced, never redistributed from a jar).
pack_format 8 == Minecraft 1.18 / 1.18.1 / 1.18.2
"""
import json, os, random, zipfile
from PIL import Image, ImageDraw

ROOT = os.path.expanduser("~/workspace/fusionfall-resourcepack")
SRC  = os.path.join(ROOT, "FusionFall-1.18.2")
OUT  = os.path.join(ROOT, "FusionFall-ResourcePack-1.18.2.zip")

random.seed(1182)  # deterministic builds

# ---------- palette ----------
FUSION      = (74, 222, 62)    # bright fusion-matter green
FUSION_HI   = (168, 255, 120)  # glowing highlight
FUSION_DK   = (22, 110, 28)    # deep goo green
FUSION_DEEP = (10, 58, 18)
SLIME       = (122, 236, 84)
DEX_ORANGE  = (255, 128, 32)
DEX_WHITE   = (238, 242, 245)
CARTOON_SKY = (64, 190, 230)
DIRT        = (134, 96, 67)
DIRT_DK     = (104, 72, 47)
DIRT_LT     = (164, 124, 88)
STONE       = (128, 128, 128)
STONE_DK    = (96, 96, 96)
STONE_LT    = (162, 162, 162)
WOOD        = (168, 132, 82)
WOOD_DK     = (122, 92, 54)
WOOD_LT     = (196, 160, 106)

def save(img, rel):
    p = os.path.join(SRC, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p)
    return rel

def px(draw, x, y, c):
    draw.point((x, y), fill=c)

def noise_tile(base, variants, w=16, h=16, speckle=None, speckle_n=0):
    img = Image.new("RGBA", (w, h), base + (255,))
    d = ImageDraw.Draw(img)
    for y in range(h):
        for x in range(w):
            if random.random() < 0.42:
                px(d, x, y, random.choice(variants) + (255,))
    if speckle:
        for _ in range(speckle_n):
            px(d, random.randrange(w), random.randrange(h), speckle + (255,))
    return img

def blobs(img, color, n, maxr=2):
    d = ImageDraw.Draw(img)
    w, h = img.size
    for _ in range(n):
        cx, cy = random.randrange(w), random.randrange(h)
        r = random.randint(1, maxr)
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r and 0 <= cx + dx < w and 0 <= cy + dy < h:
                    px(d, cx + dx, cy + dy, color + (255,))
    return img

B = "assets/minecraft/textures/block/"
I = "assets/minecraft/textures/item/"
E = "assets/minecraft/textures/entity/"
G = "assets/minecraft/textures/gui/"

# ================= BLOCKS =================
# Grass top: light mint-green blades so the (also custom) colormap tints it vivid fusion green
img = noise_tile((178, 240, 150), [(158, 228, 128), (198, 248, 170), (140, 214, 110)], speckle=FUSION_DK, speckle_n=10)
save(img, B + "grass_block_top.png")
# Dirt: classic brown, infected with glowing fusion spots
img = noise_tile(DIRT, [DIRT_DK, DIRT_LT, (120, 84, 56)])
blobs(img, FUSION_DK, 3); blobs(img, FUSION, 2, maxr=1)
save(img, B + "dirt.png"); save(img.copy(), B + "coarse_dirt.png"); save(img.copy(), B + "rooted_dirt.png")
# Grass side: dirt with a thick fusion-grass cap + goo drips; overlay fully transparent to force our colours
img = Image.open(os.path.join(SRC, B + "dirt.png")).copy()
d = ImageDraw.Draw(img)
for x in range(16):
    depth = random.choice([3, 3, 4, 4, 5])
    for y in range(depth):
        px(d, x, y, random.choice([FUSION, SLIME, (150, 240, 120)]) + (255,))
    if random.random() < 0.3:
        px(d, x, depth, FUSION_DK + (255,))
save(img, B + "grass_block_side.png")
save(Image.new("RGBA", (16, 16), (0, 0, 0, 0)), B + "grass_block_side_overlay.png")
# Snowy variant reuses side look
save(img.copy(), B + "grass_block_snow.png")
save(noise_tile((245, 250, 250), [(225, 238, 240), (255, 255, 255)], speckle=FUSION_HI, speckle_n=4), B + "snow.png")
# Stone / cobble / bricks with fusion cracks in the mortar
img = noise_tile(STONE, [STONE_DK, STONE_LT, (112, 112, 112)], speckle=FUSION_DK, speckle_n=3)
save(img, B + "stone.png"); save(img.copy(), B + "andesite.png")
img = Image.new("RGBA", (16, 16), FUSION_DK + (255,)); d = ImageDraw.Draw(img)
for (x0, y0, x1, y1) in [(0,0,7,4),(8,0,15,5),(0,5,5,10),(6,6,15,10),(0,11,8,15),(9,11,15,15)]:
    d.rectangle([x0, y0, x1, y1], fill=random.choice([STONE, STONE_LT, (118,118,118)]) + (255,))
    d.rectangle([x0, y0, x1, y0], fill=STONE_LT + (255,))
save(img, B + "cobblestone.png")
img2 = img.copy(); blobs(img2, FUSION, 6, maxr=1); blobs(img2, FUSION_DK, 6)
save(img2, B + "mossy_cobblestone.png")
img = Image.new("RGBA", (16, 16), STONE_DK + (255,)); d = ImageDraw.Draw(img)
for row, y in enumerate([0, 4, 8, 12]):
    off = 0 if row % 2 == 0 else 4
    for x in range(-4, 17, 8):
        d.rectangle([x + off, y, x + off + 7, y + 3], fill=random.choice([STONE, (138,138,138)]) + (255,))
        d.rectangle([x + off, y, x + off + 7, y], fill=STONE_LT + (255,))
    if row == 2:
        d.line([(2, y + 1), (6, y + 3), (10, y + 1)], fill=FUSION + (255,))
save(img, B + "stone_bricks.png"); save(img.copy(), B + "mossy_stone_bricks.png")
# Bedrock: near-black with fusion veins
img = noise_tile((52, 52, 58), [(34, 34, 40), (74, 74, 80)])
d = ImageDraw.Draw(img); d.line([(1, 12), (5, 7), (4, 3), (9, 1)], fill=FUSION_DK + (255,)); d.line([(10, 15), (12, 9), (15, 6)], fill=FUSION_DK + (255,))
save(img, B + "bedrock.png")
# Planks / logs (DexLabs crate-wood: warm wood, orange-ish grain)
img = Image.new("RGBA", (16, 16), WOOD + (255,)); d = ImageDraw.Draw(img)
for y in (3, 7, 11, 15):
    d.line([(0, y), (15, y)], fill=WOOD_DK + (255,))
for y in range(16):
    for _ in range(2):
        px(d, random.randrange(16), y, random.choice([WOOD_DK, WOOD_LT]) + (255,))
for seam_y, seam_x in [(3, 11), (7, 4), (11, 12), (15, 6)]:
    px(d, seam_x, seam_y - 0, WOOD_DK + (255,))
save(img, B + "oak_planks.png"); save(img.copy(), B + "birch_planks.png")
img = noise_tile((106, 84, 50), [(88, 68, 38), (124, 100, 62)])
d = ImageDraw.Draw(img)
for x in (2, 7, 12):
    d.line([(x, 0), (x, 15)], fill=(74, 56, 30, 255))
save(img, B + "oak_log.png"); save(img.copy(), B + "spruce_log.png")
img = Image.new("RGBA", (16, 16), WOOD_DK + (255,)); d = ImageDraw.Draw(img)
for r, c in [(6, WOOD_LT), (4, WOOD), (2, WOOD_LT)]:
    d.rectangle([8 - r, 8 - r, 7 + r, 7 + r], outline=c + (255,))
save(img, B + "oak_log_top.png"); save(img.copy(), B + "spruce_log_top.png")
# Leaves: light fusion-green so foliage colormap stays vivid; scattered transparent holes + goo berries
img = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
for y in range(16):
    for x in range(16):
        if random.random() < 0.12:
            continue
        px(d, x, y, random.choice([(150, 235, 120), (128, 220, 100), (178, 248, 148), (104, 196, 82)]) + (255,))
blobs(img, FUSION_HI, 2, maxr=1)
save(img, B + "oak_leaves.png"); save(img.copy(), B + "birch_leaves.png"); save(img.copy(), B + "jungle_leaves.png")
# Sand / gravel / glass
save(noise_tile((219, 207, 163), [(203, 190, 142), (232, 222, 184)], speckle=FUSION, speckle_n=3), B + "sand.png")
save(noise_tile((130, 126, 124), [(104, 100, 98), (156, 150, 146), DIRT], speckle=FUSION_DK, speckle_n=4), B + "gravel.png")
img = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
d.rectangle([0, 0, 15, 15], outline=FUSION + (255,))
d.line([(2, 13), (6, 9)], fill=(220, 255, 220, 160)); d.line([(3, 13), (7, 9)], fill=(220, 255, 220, 120))
save(img, B + "glass.png")
img = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.line([(0, 0), (15, 0)], fill=FUSION + (255,))
save(img, B + "glass_pane_top.png")
# Ores: stone/deepslate base + chunky crystals
def ore(base, base_vars, gem, gem_hi, name, deep=False):
    img = noise_tile(base, base_vars)
    d = ImageDraw.Draw(img)
    for _ in range(4):
        cx, cy = random.randint(1, 13), random.randint(1, 13)
        for (dx, dy) in [(0,0),(1,0),(0,1),(1,1),(0,-0)]:
            px(d, cx + dx, cy + dy, gem + (255,))
        px(d, cx, cy, gem_hi + (255,))
    save(img, B + name)
ore(STONE, [STONE_DK, STONE_LT], FUSION, FUSION_HI, "emerald_ore.png")
ore(STONE, [STONE_DK, STONE_LT], (64, 235, 235), (200, 255, 255), "diamond_ore.png")
ore(STONE, [STONE_DK, STONE_LT], (200, 200, 205), (245, 245, 250), "iron_ore.png")
ore(STONE, [STONE_DK, STONE_LT], (250, 200, 60), (255, 236, 150), "gold_ore.png")
ore(STONE, [STONE_DK, STONE_LT], (40, 40, 44), (90, 90, 96), "coal_ore.png")
ore(STONE, [STONE_DK, STONE_LT], (235, 50, 40), (255, 130, 110), "redstone_ore.png")
ore(STONE, [STONE_DK, STONE_LT], (50, 90, 220), (130, 170, 255), "lapis_ore.png")
DEEP = (76, 76, 84); DEEPV = [(58, 58, 66), (94, 94, 102)]
ore(DEEP, DEEPV, FUSION, FUSION_HI, "deepslate_emerald_ore.png", True)
ore(DEEP, DEEPV, (64, 235, 235), (200, 255, 255), "deepslate_diamond_ore.png", True)
ore(DEEP, DEEPV, (200, 200, 205), (245, 245, 250), "deepslate_iron_ore.png", True)
ore(DEEP, DEEPV, (250, 200, 60), (255, 236, 150), "deepslate_gold_ore.png", True)
ore(DEEP, DEEPV, (40, 40, 44), (90, 90, 96), "deepslate_coal_ore.png", True)
save(noise_tile(DEEP, DEEPV, speckle=FUSION_DK, speckle_n=3), B + "deepslate.png")
# Obsidian / nether / end — the "Fusion Fallen" dimensions
img = noise_tile((24, 16, 38), [(36, 24, 54), (14, 10, 26)])
d = ImageDraw.Draw(img); d.line([(2, 14), (6, 8), (5, 3)], fill=FUSION_DK + (255,)); d.line([(11, 15), (13, 8), (15, 5)], fill=(90, 50, 140, 255))
save(img, B + "obsidian.png"); save(img.copy(), B + "crying_obsidian.png")
save(blobs(noise_tile((112, 38, 32), [(92, 28, 24), (134, 50, 40)]), FUSION, 3, maxr=1), B + "netherrack.png")
save(noise_tile((226, 224, 168), [(206, 202, 138), (240, 238, 190)], speckle=FUSION, speckle_n=5), B + "end_stone.png")
img = noise_tile((238, 220, 90), [(220, 198, 66), (252, 238, 140)])
blobs(img, (255, 255, 210), 5, maxr=1); save(img, B + "glowstone.png")
save(noise_tile((70, 58, 50), [(54, 44, 38), (88, 74, 62)], speckle=FUSION_DK, speckle_n=4), B + "soul_sand.png")
# Work blocks: crafting table (DexLabs workbench), furnace, bookshelf
img = Image.open(os.path.join(SRC, B + "oak_planks.png")).copy(); d = ImageDraw.Draw(img)
d.rectangle([1, 1, 14, 14], outline=DEX_ORANGE + (255,)); d.rectangle([4, 4, 11, 11], outline=WOOD_DK + (255,))
d.rectangle([7, 1, 8, 14], fill=WOOD_DK + (255,)); d.rectangle([1, 7, 14, 8], fill=WOOD_DK + (255,))
save(img, B + "crafting_table_top.png")
img = Image.open(os.path.join(SRC, B + "oak_planks.png")).copy(); d = ImageDraw.Draw(img)
d.rectangle([2, 3, 7, 9], outline=DEX_ORANGE + (255,)); d.rectangle([9, 3, 13, 9], outline=FUSION_DK + (255,))
save(img, B + "crafting_table_side.png"); save(img.copy(), B + "crafting_table_front.png")
img = Image.open(os.path.join(SRC, B + "cobblestone.png")).copy(); d = ImageDraw.Draw(img)
d.rectangle([4, 8, 11, 14], fill=(20, 20, 20, 255)); d.rectangle([5, 10, 10, 14], fill=FUSION + (255,)); d.rectangle([6, 12, 9, 14], fill=FUSION_HI + (255,))
d.rectangle([5, 2, 10, 4], fill=(30, 30, 30, 255))
save(img, B + "furnace_front.png")
imgf = img.copy(); save(imgf, B + "furnace_front_on.png")
save(Image.open(os.path.join(SRC, B + "cobblestone.png")).copy(), B + "furnace_side.png")
save(Image.open(os.path.join(SRC, B + "stone.png")).copy(), B + "furnace_top.png")
img = Image.open(os.path.join(SRC, B + "oak_planks.png")).copy(); d = ImageDraw.Draw(img)
for x, c in [(2, (196, 60, 50)), (6, FUSION_DK), (10, (60, 90, 200))]:
    d.rectangle([x, 2, x + 2, 13], fill=c + (255,)); d.rectangle([x, 2, x + 2, 4], fill=DEX_WHITE + (255,))
save(img, B + "bookshelf.png")
# TNT -> Fusion Barrel
img = noise_tile((46, 160, 44), [FUSION_DK, (60, 190, 56)]); d = ImageDraw.Draw(img)
d.rectangle([0, 6, 15, 10], fill=(18, 18, 18, 255))
for x, chx in [(3, 1), (7, 1), (11, 1)]:
    px(d, x, 7, FUSION_HI + (255,)); px(d, x, 9, FUSION_HI + (255,))
save(img, B + "tnt_side.png")
img = noise_tile(WOOD, [WOOD_DK, WOOD_LT]); d = ImageDraw.Draw(img); d.ellipse([4, 4, 11, 11], outline=(18, 18, 18, 255)); save(img, B + "tnt_top.png"); save(img.copy(), B + "tnt_bottom.png")
# Pumpkin family (Fusion-o'-lantern)
img = noise_tile((232, 128, 20), [(206, 108, 14), (248, 152, 34)]); d = ImageDraw.Draw(img)
for x in (3, 7, 11): d.line([(x, 0), (x, 15)], fill=(190, 96, 10, 255))
save(img, B + "pumpkin_side.png"); save(img.copy(), B + "pumpkin_top.png")
imgc = img.copy(); d = ImageDraw.Draw(imgc)
d.rectangle([3, 6, 5, 8], fill=(20, 16, 8, 255)); d.rectangle([10, 6, 12, 8], fill=(20, 16, 8, 255)); d.rectangle([6, 11, 9, 12], fill=(20, 16, 8, 255))
save(imgc, B + "carved_pumpkin.png")
imgl = imgc.copy(); d = ImageDraw.Draw(imgl)
d.rectangle([3, 6, 5, 8], fill=FUSION_HI + (255,)); d.rectangle([10, 6, 12, 8], fill=FUSION_HI + (255,)); d.rectangle([6, 11, 9, 12], fill=FUSION_HI + (255,))
save(imgl, B + "jack_o_lantern.png")
# Mycelium / podzol as fusion-soil variants
save(blobs(noise_tile((122, 96, 128), [(104, 80, 112), (142, 116, 148)]), FUSION, 4, maxr=1), B + "mycelium_top.png")
save(noise_tile((122, 92, 58), [(102, 76, 44), (146, 112, 72)], speckle=FUSION_DK, speckle_n=4), B + "podzol_top.png")
# Water/lava are animated strip textures — a tinted still frame each (vanilla .mcmeta anim still applies by filename convention in-pack? No:
# resource packs need the .mcmeta sidecar for animation; we ship a simple 2-frame strip + mcmeta below.)
img = Image.new("RGBA", (16, 32), (30, 110, 220, 190)); d = ImageDraw.Draw(img)
for y in range(32):
    for _ in range(3): px(d, random.randrange(16), y, (90, 180, 255, 190))
    if y % 8 == 0: d.line([(0, y), (15, y)], fill=(140, 230, 160, 200))
save(img, B + "water_still.png")
with open(os.path.join(SRC, B + "water_still.png.mcmeta"), "w") as f:
    json.dump({"animation": {"frametime": 2, "frames": [0, 1]}}, f)
img = Image.new("RGBA", (16, 32), (230, 90, 10, 255)); d = ImageDraw.Draw(img)
for y in range(32):
    for _ in range(3): px(d, random.randrange(16), y, random.choice([(255, 170, 30), (255, 220, 90)]) + (255,))
save(img, B + "lava_still.png")
with open(os.path.join(SRC, B + "lava_still.png.mcmeta"), "w") as f:
    json.dump({"animation": {"frametime": 3, "frames": [0, 1]}}, f)

# ================= ITEMS =================
def blank(): return Image.new("RGBA", (16, 16), (0, 0, 0, 0))
def sword(blade, blade_hi, guard, name):
    img = blank(); d = ImageDraw.Draw(img)
    for i in range(9):  # diagonal blade from top-right to mid
        x, y = 14 - i, 1 + i
        px(d, x, y, blade + (255,)); px(d, x - 1, y, blade_hi + (255,))
    for (x, y) in [(5, 10), (6, 11), (4, 11), (6, 9)]:  # guard
        px(d, x, y, guard + (255,))
    for i in range(4):  # grip
        px(d, 4 - 0 - i + 1, 12 + i - 1 + 1, (70, 48, 28, 255)) if False else None
    for (x, y) in [(4, 12), (3, 13), (2, 14)]:
        px(d, x, y, (88, 58, 30, 255))
    px(d, 1, 15, DEX_ORANGE + (255,))  # pommel
    save(img, I + name)
sword((52, 220, 225), (190, 255, 255), FUSION, "diamond_sword.png")
sword((38, 38, 44), (90, 90, 100), FUSION, "netherite_sword.png")
sword((205, 205, 210), (245, 245, 250), DEX_ORANGE, "iron_sword.png")
sword((250, 205, 70), (255, 238, 160), DEX_ORANGE, "golden_sword.png")
sword(STONE, STONE_LT, WOOD_DK, "stone_sword.png")
sword(WOOD, WOOD_LT, WOOD_DK, "wooden_sword.png")
# Pickaxe / axe in the diamond (Nano) colourway
def tool(head, name, kind):
    img = blank(); d = ImageDraw.Draw(img)
    for (x, y) in [(3, 12), (4, 11), (5, 10), (6, 9)]:  # handle
        px(d, x, y, (110, 78, 40, 255))
    if kind == "pick":
        for (x, y) in [(6, 9), (7, 7), (8, 5), (9, 4), (11, 3), (13, 3), (14, 4), (15, 6), (5, 8), (4, 6), (3, 4), (2, 3), (4, 3), (6, 4)]:
            px(d, x, y, head + (255,))
    else:
        for (x, y) in [(6, 9), (7, 8), (8, 7), (9, 6), (10, 5), (11, 4), (11, 6), (11, 8), (10, 9), (9, 9), (12, 3), (13, 4)]:
            px(d, x, y, head + (255,))
    save(img, I + name)
tool((52, 220, 225), "diamond_pickaxe.png", "pick"); tool((52, 220, 225), "diamond_axe.png", "axe")
tool((205, 205, 210), "iron_pickaxe.png", "pick");   tool((205, 205, 210), "iron_axe.png", "axe")
# Gems / orbs / food
def gem(c, hi, name):
    img = blank(); d = ImageDraw.Draw(img)
    d.polygon([(8, 1), (13, 6), (8, 15), (3, 6)], fill=c + (255,))
    d.polygon([(8, 1), (13, 6), (3, 6)], fill=hi + (255,))
    save(img, I + name)
gem(FUSION, FUSION_HI, "emerald.png")
gem((52, 220, 225), (190, 255, 255), "diamond.png")
def orb(c, hi, name):
    img = blank(); d = ImageDraw.Draw(img)
    d.ellipse([3, 3, 12, 12], fill=c + (255,)); d.ellipse([5, 4, 8, 7], fill=hi + (255,))
    save(img, I + name)
orb(FUSION, FUSION_HI, "ender_pearl.png")
orb((30, 30, 36), FUSION, "ender_eye.png")
img = blank(); d = ImageDraw.Draw(img)
d.ellipse([4, 5, 12, 14], fill=(120, 235, 90, 255)); d.ellipse([5, 6, 8, 9], fill=(190, 255, 160, 255))
px(d, 8, 4, WOOD_DK + (255,)); px(d, 9, 3, FUSION_DK + (255,)); save(img, I + "apple.png")
img = blank(); d = ImageDraw.Draw(img)
d.ellipse([4, 5, 12, 14], fill=(250, 205, 70, 255)); d.ellipse([5, 6, 8, 9], fill=(255, 240, 170, 255))
px(d, 8, 4, WOOD_DK + (255,)); save(img, I + "golden_apple.png"); save(img.copy(), I + "enchanted_golden_apple.png")
img = blank(); d = ImageDraw.Draw(img)  # totem: little Nano robot
d.rectangle([4, 3, 11, 10], fill=(235, 200, 90, 255)); d.rectangle([5, 5, 6, 6], fill=FUSION + (255,)); d.rectangle([9, 5, 10, 6], fill=FUSION + (255,))
d.rectangle([6, 8, 9, 9], fill=(120, 84, 30, 255)); d.rectangle([5, 11, 10, 14], fill=(200, 164, 70, 255))
d.rectangle([2, 6, 3, 10], fill=(200, 164, 70, 255)); d.rectangle([12, 6, 13, 10], fill=(200, 164, 70, 255))
save(img, I + "totem_of_undying.png")
img = blank(); d = ImageDraw.Draw(img)  # bow: DexLabs orange limbs
for t in range(16):
    x = int(4 + 7 * abs((t - 7.5) / 7.5))
    px(d, x, t, DEX_ORANGE + (255,)); px(d, 12, t, (240, 240, 240, 255))
save(img, I + "bow.png")
img = blank(); d = ImageDraw.Draw(img)  # stick with fusion tip
for i in range(10): px(d, 4 + i, 11 - i, (130, 94, 52, 255))
px(d, 13, 2, FUSION + (255,)); px(d, 14, 1, FUSION_HI + (255,)); save(img, I + "stick.png")
img = blank(); d = ImageDraw.Draw(img)  # blaze rod -> fusion rod
for i in range(11): px(d, 5 + i // 2, 12 - i, FUSION_DK + (255,) if i % 3 else FUSION + (255,))
save(img, I + "blaze_rod.png")
img = blank(); d = ImageDraw.Draw(img)  # nether star -> fusion star
d.polygon([(8, 1), (10, 6), (15, 6), (11, 9), (13, 14), (8, 11), (3, 14), (5, 9), (1, 6), (6, 6)], fill=FUSION_HI + (255,))
save(img, I + "nether_star.png")
img = blank(); d = ImageDraw.Draw(img)  # XP bottle
d.rectangle([6, 2, 9, 4], fill=(170, 130, 80, 255)); d.rectangle([5, 5, 10, 13], outline=(210, 240, 255, 255))
d.rectangle([6, 9, 9, 12], fill=FUSION + (255,)); save(img, I + "experience_bottle.png")
for ingot, name in [((205, 205, 210), "iron_ingot.png"), ((250, 205, 70), "gold_ingot.png")]:
    img = blank(); d = ImageDraw.Draw(img)
    d.polygon([(3, 10), (5, 6), (11, 6), (13, 10), (11, 12), (5, 12)], fill=ingot + (255,))
    d.line([(5, 7), (11, 7)], fill=(255, 255, 255, 255)); save(img, I + name)
img = blank(); d = ImageDraw.Draw(img)  # redstone dust -> fusion dust pile
for (x, y) in [(4,11),(6,10),(8,11),(10,10),(12,11),(7,9),(9,9),(8,8)]:
    px(d, x, y, FUSION + (255,))
save(img, I + "redstone.png"); save(img.copy(), I + "glowstone_dust.png")

# ================= ENTITIES =================
# Creeper 64x32: whole sheet fusion-green goo, face drawn on the head-front face (x8-16, y8-16)
img = noise_tile((58, 190, 52), [(44, 160, 40), (76, 214, 66), FUSION_DK], w=64, h=32)
blobs(img, FUSION_DEEP, 14, maxr=2); blobs(img, FUSION_HI, 6, maxr=1)
d = ImageDraw.Draw(img)
for (x, y, w2, h2) in [(9, 10, 2, 2), (13, 10, 2, 2)]:
    d.rectangle([x, y, x + w2 - 1, y + h2 - 1], fill=(8, 8, 8, 255))
d.rectangle([11, 12, 12, 13], fill=(8, 8, 8, 255)); d.rectangle([10, 14, 11, 15], fill=(8, 8, 8, 255)); d.rectangle([12, 14, 13, 15], fill=(8, 8, 8, 255))
save(img, E + "creeper/creeper.png")
# Zombie 64x64 (Steve layout): green skin, Dex-orange shirt, dark pants
img = Image.new("RGBA", (64, 64), (70, 170, 60, 255)); d = ImageDraw.Draw(img)
d.rectangle([0, 0, 31, 15], fill=(86, 196, 66, 255))                    # head zone
d.rectangle([8, 8, 23, 15], fill=(96, 208, 74, 255))
d.rectangle([11, 11, 12, 12], fill=(10, 10, 10, 255)); d.rectangle([19, 11, 20, 12], fill=(10, 10, 10, 255))  # eyes (front)
d.rectangle([20, 16, 39, 31], fill=DEX_ORANGE + (255,))                  # torso shirt
d.rectangle([40, 16, 55, 31], fill=(86, 196, 66, 255))                   # arm skin
d.rectangle([32, 48, 47, 63], fill=(86, 196, 66, 255))
d.rectangle([4, 16, 15, 31], fill=(38, 44, 84, 255))                     # leg pants
d.rectangle([16, 48, 27, 63], fill=(38, 44, 84, 255))
save(img, E + "zombie/zombie.png")
# Enderman 64x64: near-black body, fusion spots, glowing green eyes on head-front + separate eyes layer
img = noise_tile((26, 22, 34), [(18, 15, 26), (36, 30, 46)], w=64, h=64)
blobs(img, FUSION_DK, 18, maxr=1); d = ImageDraw.Draw(img)
d.rectangle([9, 12, 11, 12], fill=FUSION_HI + (255,)); d.rectangle([20 - 8, 12, 22 - 8, 12], fill=FUSION_HI + (255,))
save(img, E + "enderman/enderman.png")
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
d.rectangle([9, 12, 11, 12], fill=FUSION_HI + (255,)); d.rectangle([12, 12, 14, 12], fill=FUSION_HI + (255,))
save(img, E + "enderman/enderman_eyes.png")
# Spider 64x32: dark goo body, eight bright eyes on the head face (front at x24-32? head box x24..32,y10..18 approx) — paint eyes band
img = noise_tile((30, 60, 30), [(22, 46, 22), (42, 84, 40)], w=64, h=32)
d = ImageDraw.Draw(img)
for x in (26, 28, 30):
    px(d, x, 13, (255, 60, 40, 255)); px(d, x, 14, FUSION_HI + (255,))
save(img, E + "spider/spider.png")
# Pig 64x64: fusion-infected light-green pig (head/snout zone kept readable)
img = noise_tile((150, 230, 130), [(132, 214, 112), (170, 244, 152)], w=64, h=64)
d = ImageDraw.Draw(img)
d.rectangle([12, 13, 19, 15], fill=(110, 200, 92, 255))  # snout approx on head front (8-24, 8-16 zone -> snout centre)
d.rectangle([10, 10, 11, 11], fill=(10, 10, 10, 255)); d.rectangle([20, 10, 21, 11], fill=(10, 10, 10, 255))
save(img, E + "pig/pig.png")

# ================= GUI =================
# widgets.png 256x256: hotbar + selected slot + menu buttons; rest transparent (vanilla fallback art is NOT
# redistributed — untextured regions fall back to magenta? No: missing areas of widgets are used for many icons.
# To stay safe we only theme the hotbar strip rows and button rows, and fill the remaining icon area with
# transparent pixels ONLY where vanilla draws from other sheets in 1.18.2 for HUD icons (icons.png). Widgets
# regions we don't draw are left transparent-black like many minimal packs; buttons/hotbar are the visible win.)
img = Image.new("RGBA", (256, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
d.rectangle([0, 0, 181, 21], fill=(16, 22, 18, 200))
for i in range(9):
    x0 = 1 + i * 20
    d.rectangle([x0, 1, x0 + 19, 20], outline=FUSION_DK + (255,))
    d.rectangle([x0 + 1, 2, x0 + 18, 19], outline=(60, 70, 62, 255))
d.rectangle([0, 22, 23, 43], outline=FUSION_HI + (255,)); d.rectangle([1, 23, 22, 42], outline=FUSION + (255,))
for y0 in (66, 86, 106):  # menu button slices
    d.rectangle([0, y0, 199, y0 + 19], fill=(34, 40, 36, 255))
    d.rectangle([0, y0, 199, y0 + 19], outline=FUSION_DK + (255,))
    d.rectangle([0, y0, 199, y0 + 1], fill=(84, 96, 86, 255))
save(img, G + "widgets.png")
# icons.png 256x256: only the crosshair area (0,0)-(15,15) drawn, rest transparent keeps vanilla? No — same-sheet
# icons (hearts etc.) would vanish. SAFER: skip icons.png entirely.
# inventory.png 256x256: full panel, slots on the standard 18px grid
img = Image.new("RGBA", (256, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
d.rectangle([0, 0, 175, 165], fill=(22, 30, 24, 255)); d.rectangle([0, 0, 175, 165], outline=FUSION + (255,))
d.rectangle([1, 1, 174, 164], outline=FUSION_DK + (255,))
def slot(x, y):
    d.rectangle([x, y, x + 17, y + 17], fill=(10, 14, 11, 255))
    d.rectangle([x, y, x + 17, y + 17], outline=(88, 104, 90, 255))
for r in range(3):
    for c in range(9): slot(8 + c * 18, 84 + r * 18)
for c in range(9): slot(8 + c * 18, 142)
for r in range(4): slot(8, 8 + r * 18)          # armour
slot(77, 62)                                     # offhand
for r in range(2):
    for c in range(2): slot(98 + c * 18, 18 + r * 18)  # crafting grid
slot(154, 28)                                    # crafting result
d.rectangle([115, 62, 145, 67], outline=FUSION_DK + (255,))  # recipe-book button hint box
save(img, G + "container/inventory.png")
# Panorama: 6 faces, 512x512 — cartoon skyline over a fusion-matter horizon (original silhouette art)
for face in range(6):
    img = Image.new("RGBA", (512, 512)); d = ImageDraw.Draw(img)
    for y in range(512):
        t = y / 512
        if y < 300:
            c = (int(46 + 60 * t), int(150 + 60 * t), int(215 - 40 * t))
        else:
            c = (int(30 - 10 * (t - 0.58)), int(120 + 90 * (t - 0.58)), int(40))
        d.line([(0, y), (511, y)], fill=c + (255,))
    rng = random.Random(400 + face)
    for _ in range(46):  # stars / sky dots upper area
        px(d, rng.randrange(512), rng.randrange(140), (255, 255, 255, 255))
    x = -10  # skyline silhouettes
    while x < 512:
        wdt, hgt = rng.randint(28, 70), rng.randint(50, 150)
        d.rectangle([x, 300 - hgt, x + wdt, 300], fill=(16, 34, 30, 255))
        for wy in range(300 - hgt + 8, 292, 14):
            for wx in range(x + 5, x + wdt - 5, 11):
                if rng.random() < 0.55: d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 110, 255))
        x += wdt + rng.randint(2, 12)
    for _ in range(260):  # fusion-matter ground speckle
        px(d, rng.randrange(512), rng.randint(305, 511), rng.choice([FUSION, FUSION_HI, FUSION_DK]) + (255,))
    save(img, G + f"title/background/panorama_{face}.png")
img = Image.new("RGBA", (512, 512), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
d.rectangle([0, 470, 511, 511], fill=(0, 0, 0, 90))
save(img, G + "title/background/panorama_overlay.png")

# ================= COLORMAPS =================
# 256x256 temperature/rainfall maps — kept HIGH-VALUE so multiplied grass/leaves read vivid fusion green.
img = Image.new("RGBA", (256, 256)); d = ImageDraw.Draw(img)
for y in range(256):
    for x in range(256):
        d.point((x, y), fill=(150 + x // 6, 255, 110 + y // 5, 255))
save(img, "assets/minecraft/textures/colormap/grass.png")
img = Image.new("RGBA", (256, 256)); d = ImageDraw.Draw(img)
for y in range(256):
    for x in range(256):
        d.point((x, y), fill=(140 + x // 6, 248, 100 + y // 5, 255))
save(img, "assets/minecraft/textures/colormap/foliage.png")

# ================= PACK ICON =================
img = Image.new("RGBA", (128, 128), (12, 26, 14, 255)); d = ImageDraw.Draw(img)
d.ellipse([24, 24, 104, 104], fill=FUSION_DK + (255,)); d.ellipse([30, 30, 98, 98], fill=FUSION + (255,))
d.ellipse([44, 40, 66, 62], fill=FUSION_HI + (255,))
for (x, y) in [(78, 66), (60, 82), (86, 44)]:
    d.ellipse([x, y, x + 12, y + 12], fill=FUSION_DEEP + (255,))
d.rectangle([58, 108, 70, 118], fill=DEX_ORANGE + (255,))
save(img, "pack.png")

print("textures done")
