#!/usr/bin/env python3
import json
from pathlib import Path

manifest_path = Path("generated/current/manifest.json")
history_path = Path("state/previous_ideas.json")

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
history = {"ideas": []}

if history_path.exists():
    try:
        history = json.loads(history_path.read_text(encoding="utf-8"))
    except Exception:
        pass

ideas = history.setdefault("ideas", [])
ideas.append({
    "title": manifest.get("title"),
    "hazard_name": manifest.get("hazard_name"),
    "hazard_concept": manifest.get("hazard_concept"),
})

# Keep repository state small.
history["ideas"] = ideas[-100:]
history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")
