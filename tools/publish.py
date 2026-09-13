#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slot-index", type=int, required=True)
    parser.add_argument("--place-file", required=True)
    parser.add_argument("--slots-file", default="config/staging_slots.json")
    args = parser.parse_args()

    api_key = os.environ.get("ROBLOX_API_KEY")
    if not api_key:
        print("ROBLOX_API_KEY is not set", file=sys.stderr)
        raise SystemExit(1)

    slots_path = Path(args.slots_file)
    if not slots_path.exists():
        print(f"Missing {slots_path}. Copy staging_slots.example.json and enter your IDs.", file=sys.stderr)
        raise SystemExit(1)

    data = json.loads(slots_path.read_text(encoding="utf-8"))
    matches = [s for s in data.get("slots", []) if int(s["index"]) == args.slot_index]
    if not matches:
        print(f"No staging slot configured for index {args.slot_index}", file=sys.stderr)
        raise SystemExit(1)

    slot = matches[0]
    universe_id = str(slot["universe_id"])
    place_id = str(slot["place_id"])

    if "REPLACE_ME" in (universe_id, place_id):
        print(f"Staging slot {args.slot_index} still contains REPLACE_ME", file=sys.stderr)
        raise SystemExit(1)

    place_file = Path(args.place_file)
    body = place_file.read_bytes()

    url = (
        f"https://apis.roblox.com/universes/v1/{universe_id}"
        f"/places/{place_id}/versions?versionType=Published"
    )

    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/octet-stream",
            "User-Agent": "RobloxDailyGameFactory/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            print(f"Published to staging slot {args.slot_index}: {slot.get('name')}")
            print(text)
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        print(f"Roblox publish failed: HTTP {exc.code}\n{details}", file=sys.stderr)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
