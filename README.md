# FusionFall Resource Pack for Minecraft 1.18.2

A fan-made FusionFall theme for Minecraft Java Edition 1.18.2 (pack_format 8).

**Download the ready-to-play pack from [Releases](https://github.com/aeon01100101/fusionfall-resourcepack/releases)** — drop the zip into your `resourcepacks` folder, no unzipping. For the full green sky, use OptiFine and turn on **Video Settings → Details → Custom Sky: ON**. Pairs well with the FusionView mod.

## What's inside

- **Green Fusion sky** (OptiFine/MCPatcher custom skyboxes) with the real **Planet Fusion** looming in it — as its own layer files, separate from the sky gradients
- **Planet Fusion rotates with the time of day**: 9 rotation layers scheduled across the 24-hour game clock, crossfading every 2h40m, dim at night and full at noon
- Planet Fusion is also the **sun** (upright) and the **moon** (all 8 phases, tumbling through the lunar cycle)
- **Lava is Fusion Matter** — built from the actual FusionFall fusion matter texture: animated still + flowing lava, magma blocks as the same goo cooled dark with glowing cracks
- Fusion-matter grass/dirt with custom colormaps, fusion-mortar cobble/bricks, all ores + deepslate variants, DexLabs workbench/furnace/bookshelf
- Nano/Fusion item renames + textures (52 language overrides), 34 FusionFall splash texts
- Fusion Creeper / Zombie / Enderman / Spider / Pig, green hotbar + dark inventory GUI, cartoon-city menu panorama

## Repo layout

- `pack/` — the resource pack source tree (this is what gets zipped for releases)
- `tools/` — the Python builders that generate the pack art and sky layers
- `rotations/` — Planet Fusion as 9 standalone transparent rotation PNGs (0–320°)
- `separate/` — standalone copies of the separated sky / planet layer files

## Credits & honesty notes

Fan-made, unofficial. Most art is original, drawn programmatically. Planet Fusion and the fusion matter texture are © Cartoon Network, included at the owner's request for personal fan use — do not sell or redistribute commercially. The pack is structure-validated end to end but has not been play-tested inside a Minecraft client by the author; the first sunrise is the real test.
