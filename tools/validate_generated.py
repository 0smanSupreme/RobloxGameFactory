#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED_MANIFEST_KEYS = {
    "title",
    "description",
    "hazard_name",
    "hazard_concept",
    "visual_theme",
    "difficulty",
    "generation_notes",
}

def fail(msg):
    print(f"VALIDATION ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)

def main():
    generated = Path("generated/current")
    manifest_path = generated / "manifest.json"
    script_path = generated / "apply_hazard.luau"

    if not manifest_path.exists():
        fail("manifest.json was not generated")
    if not script_path.exists():
        fail("apply_hazard.luau was not generated")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"manifest.json is invalid JSON: {exc}")

    missing = REQUIRED_MANIFEST_KEYS - set(manifest)
    if missing:
        fail(f"manifest.json missing keys: {sorted(missing)}")

    text = script_path.read_text(encoding="utf-8", errors="replace")

    forbidden = [
        "ROBLOX_API_KEY",
        "OPENAI_API_KEY",
        ".ROBLOSECURITY",
        "master/SurviveTemplate_FIXED.rbxl\"",  # discourage hardcoded output back to master
    ]
    for token in forbidden:
        if token in text:
            fail(f"apply_hazard.luau contains forbidden token: {token}")

    if "@lune/roblox" not in text:
        fail("apply_hazard.luau does not appear to use Lune Roblox APIs")
    if "serializePlace" not in text or "deserializePlace" not in text:
        fail("apply_hazard.luau must deserialize and serialize a place file")

    print("Generated files passed basic validation.")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
