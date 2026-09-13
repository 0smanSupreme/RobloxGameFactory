# Roblox Daily Game Factory

This repository is the automation shell for generating multiple Roblox games from one repaired master template.

## Intended flow

1. Keep one **fixed master template** at:
   `master/SurviveTemplate_FIXED.rbxl`
2. GitHub Actions starts the factory on schedule.
3. Each factory job creates a clean working directory.
4. Codex invents **one incoming hazard/entity** for that game.
5. Codex writes:
   - `generated/current/apply_hazard.luau`
   - `generated/current/manifest.json`
6. Lune loads the fixed `.rbxl`, applies the hazard to a COPY, and saves:
   `build/generated_game.rbxl`
7. Structural validation runs.
8. The place is published to one private Roblox staging experience using Open Cloud.
9. The next game starts again from the untouched fixed master template.

The uploaded file in `master/SurviveTemplate_UNFIXED.rbxl` is only a reference. The automated workflow intentionally refuses to run until `master/SurviveTemplate_FIXED.rbxl` exists.

---

# Phase 1 — what you need to do manually

## A. Finish the master template

When Codex becomes available again, have it finish/fix the game and make the template modular.

The fixed template should contain obvious replaceable hooks/markers such as:

- `Workspace/HazardSpawn`
- `Workspace/HazardEnd`
- `Workspace/GeneratedHazardAssets`
- `ReplicatedStorage/GameFramework`
- a hazard lifecycle/service that can call a generated hazard
- a central GameConfig
- an `AI_TEMPLATE_GUIDE.md` describing the exact paths and contract

After the fix:

1. Save the fixed place file as:
   `master/SurviveTemplate_FIXED.rbxl`
2. Replace `docs/AI_TEMPLATE_GUIDE.md` with the guide Codex created for the actual fixed game.
3. Commit both to GitHub.

## B. Create FIVE private staging experiences under your Roblox group

For the first version, do not create hundreds of experiences.

Create five blank/private group-owned experiences:

- Factory Staging 1
- Factory Staging 2
- Factory Staging 3
- Factory Staging 4
- Factory Staging 5

Copy each Universe ID and starting Place ID.

Then copy:

`config/staging_slots.example.json`

to:

`config/staging_slots.json`

and enter the IDs.

`staging_slots.json` contains IDs only, not secrets, so it may be committed.

## C. Create a Roblox Open Cloud API key

Create a Roblox API key with permission to publish/write the five staging experiences.

The account that owns the key must have the required group permission to edit/publish those group experiences.

Add the key to GitHub:

Repository → Settings → Secrets and variables → Actions → New repository secret

Name:

`ROBLOX_API_KEY`

Do NOT commit the key.

## D. Create an OpenAI API key

The GitHub Codex Action is designed for CI automation with an OpenAI API key.

Add another GitHub repository secret:

`OPENAI_API_KEY`

Do NOT put this key in a file or environment block that repository scripts can read.

## E. Enable GitHub Actions

Push the repository to GitHub.

The workflow has:

- a manual `workflow_dispatch` trigger
- a scheduled trigger
- five jobs, run sequentially by default

Start with the manual button first.

---

# Important architecture

The AI should NOT edit the master `.rbxl` in place.

Each generation starts from:

`master/SurviveTemplate_FIXED.rbxl`

and produces a new:

`build/generated_game.rbxl`

This protects the clean template from corruption.

---

# What Codex is allowed to generate

Codex should normally change only:

`generated/current/`

The key file is:

`generated/current/apply_hazard.luau`

This is a Lune script. It:

1. reads the master `.rbxl`,
2. deserializes it,
3. removes any old generated hazard content,
4. inserts the new hazard,
5. installs any hazard-specific runtime ModuleScript/Script code needed by the fixed framework,
6. writes a new `.rbxl`.

The actual core round, speed, grab, reward, UI, data, and other framework systems stay in the master.

---

# Why Lune is used

Lune can read and write Roblox `.rbxl` place files headlessly on Linux. That means GitHub Actions can manipulate a Roblox place while your computer is off.

It is NOT a full Roblox runtime, so structural validation is not the same as a real multiplayer playtest.

The first production version should therefore:
- publish privately,
- validate structure automatically,
- keep a human review step before making a generated game public.

Later you can add Roblox cloud-side Luau execution or more advanced test infrastructure.

---

# First test

Before enabling the daily schedule:

1. Put the repaired master at `master/SurviveTemplate_FIXED.rbxl`.
2. Complete `config/staging_slots.json`.
3. Add both secrets.
4. GitHub → Actions → `Daily Roblox Game Factory`.
5. Choose `Run workflow`.
6. Set `games_to_generate` to `1`.
7. Keep `publish` enabled only if your staging slot is ready.

Then increase to 5.

---

# Scaling after the factory works

Phase 2 can replace the five rotating staging slots with a large pre-created pool of unused private group experiences.

The allocator can then reserve a fresh Universe/Place for every generated game.

Do not build that part until generation + injection + publishing is stable.
