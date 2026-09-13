# Roblox Game Factory Agent Rules

This repository produces games from ONE repaired master Roblox template.

## Absolute rules

1. NEVER overwrite or edit `master/SurviveTemplate_FIXED.rbxl`.
2. NEVER edit `master/SurviveTemplate_UNFIXED.rbxl`.
3. The core gameplay already exists in the master template.
4. The generated game's main variation is ONE new incoming hazard/entity/event.
5. This is NOT primarily an NPC pathfinding/monster game.
6. The hazard normally comes from the dangerous/far end of the arena toward players while players collect/grab items and escape using the existing movement/speed loop.
7. Preserve the existing game loop.
8. Work only inside `generated/current/` unless the task explicitly says otherwise.
9. Read `docs/AI_TEMPLATE_GUIDE.md` before generating anything.
10. Read `generated/current/job_context.json` for the current run.

## Required generated files

Create exactly these primary files:

- `generated/current/manifest.json`
- `generated/current/apply_hazard.luau`

You may create supporting files inside `generated/current/` if useful.

## `manifest.json`

It must contain at least:

- `title`
- `description`
- `hazard_name`
- `hazard_concept`
- `visual_theme`
- `difficulty`
- `generation_notes`

Keep title and description appropriate for Roblox and avoid copyrighted characters/brands.

## `apply_hazard.luau`

This script runs using Lune, not inside Roblox Studio.

It receives CLI args in this order:

1. master place file path
2. output place file path

It must use Lune's Roblox library to deserialize the master place, modify a COPY in memory, and serialize it to the output path.

It must NEVER write back to the master path.

The master should already contain the stable gameplay framework. The script should only create/configure the generated hazard and the clearly replaceable generated-content areas described by `docs/AI_TEMPLATE_GUIDE.md`.

## Hazard creativity

Do not repeatedly make recolored walls.

Possible concepts include, but are not limited to:

- giant wave
- speeding wall
- train
- avalanche
- boulder surge
- giant rolling object
- collapsing debris front
- stampede-like mass
- energy barrier
- expanding void front
- lava surge
- storm front
- moving crusher structure
- multi-lane incoming obstacles

A hazard can have special movement and visuals, but it must still integrate with the fixed template safely.

## Engineering rules

- server-authoritative damage/death/rewards
- no arbitrary Toolbox/free-model scripts
- no `loadstring`
- no external web dependencies at runtime unless the template explicitly supports them
- no hard-coded secrets
- no code that publishes the game
- no changes to Roblox credentials
- no changes to GitHub Actions
- no TODO placeholders
- clean up generated instances between rounds
- avoid unbounded loops/connections
- keep performance reasonable
- support repeated rounds
- use existing hazard lifecycle APIs instead of rewriting RoundService

## Before finishing

Check that:
- the script reads the master path from args,
- it writes only to the output path,
- the manifest is valid JSON,
- the generated hazard is meaningfully different from the prior ideas listed in `job_context.json`,
- the core game is not rewritten.
