FUSIONFALL THEME — Resource Pack for Minecraft 1.18.2
=====================================================
Fan-made and unofficial. Not affiliated with Cartoon Network or Mojang.
ALL artwork in this pack is original, drawn pixel-by-pixel for this pack.
No FusionFall / Cartoon Network game assets are included or copied.

INSTALL
1. Put FusionFall-ResourcePack-1.18.2.zip in your Minecraft
   resourcepacks folder (.minecraft/resourcepacks) — do NOT unzip it.
2. In Minecraft 1.18.2: Options > Resource Packs > move
   "FusionFall Theme" to the right (selected) side > Done.
3. It pairs great with the FusionView mod (Forge 1.18.2) for the
   FusionFall horizon haze + bigger view distances.

SUN & MOON (v1.6)
Planet Fusion is BOTH celestial bodies now:
- sun.png — the planet, upright, crosses the sky by day.
- moon_phases.png — the same planet as the moon, all 8 phases:
  lit side shrinks/grows like a real moon (new moon = faint
  ghost), and the planet is rotated a bit more in each phase,
  so it tumbles slowly through the 8-day lunar cycle.
Game limit, stated straight: the sun is a SINGLE texture in
Minecraft — no resource pack can rotate or swap it by time of
day. The moon's 8 phases are the only time-slots a pack gets,
which is why the rotations live there. True time-of-day
rotation would need a mod (e.g. FusionView).

TIME-OF-DAY PLANET (v1.7 — rotation tracks the game clock)
Layer stack in optifine/sky/world0/ and mcpatcher/sky/world0/:
  sky1        = sky_day.png    pure green day sky (base layer)
  sky2        = sky_night.png  pure night sky (fades over sky1)
  sky3..sky11 = Planet Fusion ONLY, one layer per rotation PNG
The 9 rotations are scheduled across the 24h Minecraft day,
one every 2h40m of game time, crossfading at the boundaries
so the planet turns smoothly instead of snapping:
  00:00->000  02:40->040  05:20->080  08:00->120  10:40->160
  13:20->200  16:00->240  18:40->280  21:20->320   (degrees)
Each slice also has brightness baked in: dim at night, full at
noon. Sky and planet are still separate files — delete the
sky3..sky11 .properties files to keep the green sky planet-free.

THE GREEN SKY (v1.1, planet swapped to the REAL one in v1.2)
NOTE ON THE PLANET: Planet Fusion in this pack is Isaiah's own
background-removed cutout of the official Planet Fusion artwork
((c) Cartoon Network), fetched byte-for-byte from his GitHub
(aeon01100101/Dump) in v1.4 and composited UNTOUCHED — no keying
or background work done here — into the skybox, the sun texture
and the menu panorama. (Earlier versions: v1.2 used a cutout of
the FusionFall Wiki render; v1.3 used a chat-uploaded copy whose
transparency had been flattened to black by the app, keyed here.)
The in-game Future screenshot from the FusionFall Wiki was the
colour reference for the teal-green sky. Everything else in the
pack is original art. Personal fan use only — do not sell or
redistribute this pack commercially.
FusionFall's sky is green because Planet Fusion — a giant green
planet — hangs over the world dripping Fusion Matter. This pack
recreates that two ways:
- WITH OptiFine (recommended): the full sky is replaced with a
  green skybox — deep-green zenith fading to a lime horizon, with
  Planet Fusion looming in it, a dark green starfield at night,
  and a green nebula sky in the End.
  You MUST switch it on: OptiFine Video Settings > Details >
  Custom Sky: ON. (Same files are included in both the optifine/
  and mcpatcher/ sky folders, so MCPatcher-style loaders and
  FabricSkyboxes read them too.)
- WITHOUT OptiFine: the sun IS Planet Fusion (a big cracked green
  planet), the moon is a small green planet with real phases,
  clouds are pale green, rain is acid-green, and the End sky is
  green — those are plain vanilla textures. Straight talk: the
  blue sky GRADIENT itself is hard-coded by the game, so no
  resource pack on Earth can recolour it without OptiFine or a
  mod. That's a game limit, not a pack limit. On Forge, the
  FusionView mod's green horizon haze gets you most of the way
  even without OptiFine.

WHAT'S INSIDE (150+ files)
- Sky: green OptiFine/MCPatcher skyboxes (day, night, End),
  Planet Fusion as the sun, green moon phases, pale-green clouds,
  acid-green rain, green End sky texture, green menu panorama.
- Blocks: fusion-matter dirt/grass (custom bright-green colormaps),
  fusion-mortar cobblestone & stone bricks, infected stone & bedrock,
  DexLabs workbench/furnace/bookshelf, all 7 ores + deepslate variants,
  glowing fusion glass, Fusion Barrel (TNT), Fusion-o'-Lantern,
  custom animated water (fusion-green streaks).
  v1.9: LAVA IS FUSION MATTER — built from the actual FusionFall
  fusion matter texture Isaiah supplied (CNUF-Fusion-Matter-
  Texture from his Dump repo, (c) Cartoon Network, fan use).
  Made seamlessly tileable, then animated: still lava rolls
  slowly with a gentle pulse (20 frames), flowing lava scrolls
  down (16 frames). Magma blocks are the same texture cooled
  dark, with glowing green cracks. Note: it still burns and
  behaves like lava — that's the game, only the look changed.
- Items: Nano Blade (diamond sword), Fusion Blade (netherite sword),
  DexLabs swords/bow, Nano pickaxe & axe, Fusion Orb (ender pearl),
  Nano Crystal (diamond), Fusion Matter Gem (emerald), Nano Totem,
  Fusion Apples, Fusion Dust (redstone), Fusion Star.
- Mobs: Fusion Creeper, Fusion Zombie (Dex-orange shirt), Fusion
  Enderman (glowing green visor + eyes layer), Fusion Spider, Fusion Pig.
- GUI: fusion-green hotbar, selector & menu buttons, dark DexLabs
  inventory screen, and a cartoon-city main-menu panorama over a
  fusion-matter horizon.
- Names & flavour: 50+ items/blocks/mobs renamed in-game
  (en_us), plus FusionFall splash texts on the title screen.

TECHNICAL
- pack_format 8 = Minecraft 1.18 / 1.18.1 / 1.18.2 (Java Edition).
- Works on vanilla and Forge — no mods required.
- Everything not retextured falls back to vanilla automatically.

Built for Isaiah — Oct 13, 2026.
