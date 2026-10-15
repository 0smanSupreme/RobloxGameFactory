# SURVIVE A Template Compatibility Guide

This is the build contract for variations made from `master/SurviveTemplate_FIXED.rbxl`.

Every generated game must be a close variation of the existing **SURVIVE A** experience. Copy the immutable master, preserve its builds and systems, and add one isolated hazard variation to the copy.

## Allowed idea family

Every concept must:

- Use the title format **SURVIVE A [HAZARD / ENTITY / EVENT]**.
- Use the genre **Survival / Collection**.
- Reuse the existing arena, lobby, spawns, route, collection/grab loop, movement and speed progression, rounds, HUD/UI, shop, rewards, data, monetization, and multiplayer systems.
- Add exactly one incoming hazard, entity, or environmental event.
- Limit changes to hazard behavior, difficulty, timing, VFX/SFX, lighting, signs, and small decorative theme changes.
- Be implementable mainly as configuration, an overlay, and one hazard behavior.

Compatible variations include a themed wave, flood, lava surge, storm, rolling object, pursuing creature, or similar incoming event. Do not propose an obby, race, tycoon, tower defense, target-shooting game, vehicle or weapon framework, replacement map, replacement UI, new economy, or unrelated progression loop.

## Immutable source and preserved systems

Never edit, rename, move, or overwrite the master file. Run transformations only on a copied place. Preserve unknown instances and scripts. Never delete, rename, reparent, or replace template content outside the generated-content folder.

Discover legacy objects recursively. Reuse existing arena geometry, player routes, collection systems, movement and speed systems, round state, UI, rewards, persistence, monetization, multiplayer, anti-exploit, and identifiable hazard/event configuration. Prefer exposed configuration or a narrow adapter over replacing working code.

## Generated content

All new hazard assets belong under `Workspace/GeneratedHazardAssets`. Create this Folder on the copied place when absent. Future generations may clear its children; nothing outside it may be cleared.

## Compatibility markers

The copied result must expose:

- A descendant named `HazardSpawn`.
- A descendant named `HazardEnd`.
- A descendant named `GeneratedHazardAssets`.
- A direct child named `GameFramework` under `ReplicatedStorage`.

Reuse existing markers. If either hazard marker is absent, create an anchored, transparent, non-collidable marker Part inside `Workspace/GeneratedHazardAssets`. Derive positions from existing arena bounds, player routes, spawns, or hazard direction. Never leave both markers at the world origin or move existing geometry to fit them.

If `ReplicatedStorage/GameFramework` is absent, create a Folder with that name as a compatibility container. Do not move, rename, or replace legacy modules; they remain authoritative in their original locations.

## Hazard integration

The generated hazard must be self-contained and round-safe:

1. Discover arena and hazard objects recursively.
2. Reuse an existing controller or configuration when the change remains additive.
3. Otherwise create one isolated hazard controller without changing unrelated scripts.
4. Put round-created objects in the generated-content folder.
5. Apply the threat from `HazardSpawn` toward `HazardEnd`, or use those markers as its bounds.
6. Connect to round state and UI through discovered public values, events, attributes, or narrow adapters.
7. Keep damage and rewards server-authoritative.
8. Preserve mobile and PC support and the existing control scheme.

When integration is uncertain, preserve the legacy system and isolate the new hazard. A conservative additive result is preferred over a broad rewrite.

## UI, map, thumbnail, and cleanup

Reuse the existing map and UI hierarchy. UI changes are limited to existing text, icons, colors, and hazard status messaging. Do not add a replacement HUD, store, inventory, rewards screen, or menu. Small hazard props, effects, sounds, lighting, textures, and signs are allowed inside the generated layer. Do not build a new map.

The thumbnail must show the real existing gameplay layout with the new hazard clearly visible.

At round end, disconnect temporary events, stop loops/tweens/sounds/emitters, remove only objects created for that round, and restore existing properties changed temporarily. Repeated rounds must not accumulate duplicate scripts, connections, damage zones, parts, or effects.

## Generated files and acceptance

Automation may generate only:

- `generated/manifest.json`
- `generated/apply_hazard.luau`

The transformation must be deterministic for the same spec, fail clearly when safe arena bounds cannot be established, and never modify the source place.

A result is accepted only when the source hash is unchanged, existing builds and systems remain, exactly one hazard variation was added, all compatibility markers exist, cleanup is repeatable, no unrelated game loop/map/UI was introduced, and repository static validation passes before artifact publication.
