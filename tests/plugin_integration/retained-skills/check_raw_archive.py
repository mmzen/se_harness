"""Check the losslessly packed WO012 helper observations against their frozen inventory."""
from pathlib import Path
import argparse
import hashlib
import json
import stat
import zipfile

INVENTORY_SHA256 = "332a379e7fc242ab869998495de624135718115743ebffe145d9b3cb42800119"
SOURCE_COMMIT = "5aba54143d43d1b64be4b6cb2529c30570cabc26"
LOOSE = {"REPORT.md", "audit.json", "inventory.json", "source-path-map.json"}


def check(root: Path) -> dict:
    folder = root / "docs/engineering/plugin-integration/evidence/WO-PLG-012/acceptance/helpers"
    digest = lambda data: hashlib.sha256(data).hexdigest()
    raw_inventory = (folder / "inventory.json").read_bytes()
    if digest(raw_inventory) != INVENTORY_SHA256:
        raise ValueError("Original helper inventory changed")
    inventory = json.loads(raw_inventory)["files"]
    index = json.loads((folder / "raw-index.json").read_bytes())
    if (index["source_commit"] != SOURCE_COMMIT
            or index["original_inventory_sha256"] != INVENTORY_SHA256
            or index["archive"] != "raw.zip"
            or set(index["retained_loose_files"]) != LOOSE):
        raise ValueError("Raw archive provenance changed")
    expected = {name: row for name, row in inventory.items() if name not in LOOSE}
    rows = index["entries"]
    if len(rows) != len(expected) or {r["path"]: {"sha256": r["sha256"], "bytes": r["bytes"]} for r in rows} != expected:
        raise ValueError("Raw index does not match original inventory")
    if {p.name for p in folder.iterdir()} != LOOSE | {"raw.zip", "raw-index.json"}:
        raise ValueError("Unexpected or missing helper retention files")
    for name in LOOSE - {"inventory.json"}:
        data = (folder / name).read_bytes()
        if len(data) != inventory[name]["bytes"] or digest(data) != inventory[name]["sha256"]:
            raise ValueError(f"Retained report or map changed: {name}")
    archive = folder / "raw.zip"
    if archive.is_symlink() or archive.stat().st_size != index["archive_bytes"] or archive.stat().st_size > 8 * 1024 * 1024:
        raise ValueError("Archive size or type is invalid")
    if digest(archive.read_bytes()) != index["archive_sha256"]:
        raise ValueError("Raw ZIP hash changed")
    with zipfile.ZipFile(archive) as zipped:
        infos = zipped.infolist()
        if len(infos) != len(expected) or {i.filename for i in infos} != set(expected):
            raise ValueError("Missing, duplicate or extra ZIP entries")
        for info in infos:
            name = info.filename
            if (Path(name).name != name or "/" in name or "\\" in name
                    or info.is_dir() or stat.S_ISLNK(info.external_attr >> 16)
                    or info.file_size != expected[name]["bytes"]):
                raise ValueError(f"Unsafe ZIP entry: {name}")
            data = zipped.read(info)
            if digest(data) != expected[name]["sha256"]:
                raise ValueError(f"Raw payload changed: {name}")
    return {"passed": True, "raw_entries": len(expected), "retained_loose_files": len(LOOSE),
            "original_inventory_sha256": INVENTORY_SHA256, "source_commit": SOURCE_COMMIT,
            "payload_bytes_unchanged": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.root.resolve()), indent=2))
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as exc:
        parser.exit(1, f"helper retention: {exc}\n")
