# Master template files

`SurviveTemplate_UNFIXED.rbxl`
- Current uploaded template.
- Reference only.
- The workflow will NOT use it.

`SurviveTemplate_FIXED.rbxl`
- Add this after Codex finishes the repair/modularization task.
- This must be the clean immutable source for every generated game.

The generation workflow always reads the fixed master and writes a new file under `build/`.
