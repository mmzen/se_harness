"""Measure committed evidence bundles and find their historical record references."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tomllib


def inventory(repository: Path, ref: str = "HEAD") -> dict:
    def git(*args: str) -> bytes:
        return subprocess.check_output(["git", *args], cwd=repository)

    commit = git("rev-parse", "--verify", ref + "^{commit}").decode().strip()
    entries = {}
    for entry in git("ls-tree", "-rlz", commit).split(b"\0"):
        if not entry:
            continue
        details, path = entry.split(b"\t", 1)
        mode, kind, oid, size = details.split()
        if kind == b"blob":
            entries[path.decode("utf-8")] = (int(size), oid.decode())
    bundles = {}
    for path, (size, _) in entries.items():
        if not path.startswith("docs/engineering/") or "/evidence/" not in path:
            continue
        prefix, rest = path.split("/evidence/", 1)
        key = prefix + "/evidence/" + rest.split("/", 1)[0]
        item = bundles.setdefault(key, dict(path=key, bytes=0, files=0, records=[]))
        item["bytes"] += size
        item["files"] += 1

    records = {}
    for path, (_, oid) in entries.items():
        if not path.startswith("docs/engineering/") or not re.fullmatch(r"(?:VREC|RLS)-.+\.md", PurePosixPath(path).name):
            continue
        # Read committed blobs, not working copies or copied fixture repositories.
        if "/evidence/" in path:
            continue
        text = git("cat-file", "blob", oid).decode("utf-8")
        metadata = tomllib.loads(text.split("+++", 2)[1])
        records[metadata["id"]] = dict(path=path, status=metadata.get("status"), text=text)
    for record_id, record in records.items():
        references = set(re.findall(r"docs/engineering/[^\s\"'`<>\]\)]+", record["text"]))
        for bundle in bundles.values():
            if any(p.rstrip("/.,") == bundle["path"] or p.startswith(bundle["path"] + "/")
                   or bundle["path"].startswith(p.rstrip("/") + "/") for p in references):
                bundle["records"].append(record_id)
    # A release also depends on bundles cited by its verification records.
    for record_id, record in records.items():
        if record_id.startswith("RLS-"):
            verification_ids = set(re.findall(r"\bVREC-[A-Z0-9-]+-\d{3}\b", record["text"]))
            for bundle in bundles.values():
                if verification_ids.intersection(bundle["records"]):
                    bundle["records"].append(record_id)
    for bundle in bundles.values():
        bundle["records"] = sorted(set(bundle["records"]))
    return dict(candidate=commit, measurement="uncompressed committed blob bytes; excludes .git and untracked files",
                tracked_bytes=sum(size for size, _ in entries.values()),
                evidence_bytes=sum(item["bytes"] for item in bundles.values()),
                bundles=sorted(bundles.values(), key=lambda b: (-b["bytes"], b["path"])),
                records={key: {k: v for k, v in value.items() if k != "text"} for key, value in records.items()},
                limitations="Direct path references in VREC/RLS text plus RLS-to-VREC links only. No reference found does not authorize deletion; sidecar and indirect dependencies need review.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--ref", default="HEAD")
    args = parser.parse_args()
    print(json.dumps(inventory(args.repository, args.ref), indent=2))


if __name__ == "__main__":
    main()
