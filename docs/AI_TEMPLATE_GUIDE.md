# AI TEMPLATE GUIDE — PLACEHOLDER

REPLACE THIS FILE with the guide produced by Codex after the master template is fully repaired.

The final guide should document the ACTUAL fixed place, including:

## Required map markers
Exact paths for:
- hazard start/spawn
- hazard end/destination
- safe zone
- item area
- player spawn(s)

## Required generated-content location
Exact path of the Model/Folder that automated generations may clear and replace.

Recommended example:
`Workspace/GeneratedHazardAssets`

## Core hazard integration
Document the exact stable API/lifecycle exposed by the fixed master.

For example only:
- which ModuleScript is replaced/configured
- how the RoundService starts a hazard
- expected functions such as Create / Start / Stop / Destroy
- where runtime hazard code should be inserted
- expected attributes/config values

## Core systems that MUST NOT be changed
List exact paths for:
- RoundService
- speed system
- item/grab system
- reward/data systems
- UI framework
- anti-exploit
- monetization

## Cleanup requirements
Explain how the fixed master expects the generated hazard to clean up between rounds.

## Known constraints
Anything the generator must not do.

Until this guide is replaced, the automated workflow should be treated as scaffolding only.
