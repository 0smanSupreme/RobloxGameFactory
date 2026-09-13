#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-index", type=int, required=True)
    parser.add_argument("--previous-limit", type=int, default=30)
    args = parser.parse_args()

    generated = Path("generated/current")
    if generated.exists():
        shutil.rmtree(generated)
    generated.mkdir(parents=True, exist_ok=True)

    prev_path = Path("state/previous_ideas.json")
    previous = []
    if prev_path.exists():
        try:
            previous = json.loads(prev_path.read_text(encoding="utf-8")).get("ideas", [])
        except Exception:
            previous = []

    context = {
        "game_index": args.game_index,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "instruction": (
            "Create one new hazard variant for a fresh copy of the repaired master template. "
            "Do not rewrite the core game."
        ),
        "recent_hazard_ideas_to_avoid_repeating": previous[-args.previous_limit:],
    }

    (generated / "job_context.json").write_text(
        json.dumps(context, indent=2),
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
