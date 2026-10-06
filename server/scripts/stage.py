"""Stage an exact, read-only Git snapshot outside the checkout; no archive filters."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path, PurePosixPath


def stage(repository, manifest_path, output):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    commit = manifest["source"]["commit"]
    if output.exists():
        raise ValueError("Use a new staging directory; existing sources are preserved.")
    entries = subprocess.check_output(["git", "ls-tree", "-rz", commit], cwd=repository).split(b"\0")
    files = []
    for entry in entries:
        if not entry:
            continue
        header, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = header.decode().split()
        path = raw_path.decode("utf-8")
        if (kind != "blob" or mode not in {"100644", "100755"} or "\\" in path or ":" in path
                or any(p in ("", ".", "..") for p in path.split("/"))):
            raise ValueError("Unsupported source tree entry: " + path)
        files.append((path, oid))
    output.mkdir(parents=True)
    archive = output / "source"
    archive.mkdir()
    inventory = []
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repository, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for path, oid in files:
            process.stdin.write(oid.encode() + b"\n")
            process.stdin.flush()
            actual, kind, size = process.stdout.readline().decode().split()
            raw = process.stdout.read(int(size))
            if actual != oid or kind != "blob" or process.stdout.read(1) != b"\n":
                raise ValueError("Git batch source mismatch")
            target = archive / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            inventory.append({"path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "blob_oid": oid})
    finally:
        process.stdin.close()
        process.wait(timeout=20)
    observed = {i["path"]: i for i in inventory}
    for entry in manifest["artifacts"]:
        value = observed[entry["path"]]
        if any(value[k] != entry[k] for k in ("bytes", "blob_oid")) or value["sha256"] != entry["raw_sha256"]:
            raise ValueError("Reference fixture differs from Git blob: " + entry["path"])
    (output / "source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (output / "source-inventory.json").write_text(json.dumps({"source": manifest["source"], "files": inventory}, indent=2) + "\n", encoding="utf-8")
    return {"source": manifest["source"], "files": len(files), "bytes": sum(i["bytes"] for i in inventory),
            "formal_artifacts": len(manifest["artifacts"]), "output": str(output)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(stage(args.repository, args.manifest, args.output), indent=2))
