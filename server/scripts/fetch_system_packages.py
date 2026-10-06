"""Fetch the exact Debian packages resolved for the immutable runtime image."""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path


def fetch(lock, destination):
    destination.mkdir(parents=True, exist_ok=False)
    for item in json.loads(lock.read_text(encoding="utf-8"))["packages"]:
        with urllib.request.urlopen(item["url"], timeout=120) as response:
            raw = response.read(item["bytes"] + 1)
        if len(raw) != item["bytes"] or hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError("Pinned system package differs: " + item["file"])
        (destination / item["file"]).write_bytes(raw)


if __name__ == "__main__":
    fetch(Path(sys.argv[1]), Path(sys.argv[2]))
