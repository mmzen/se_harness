"""Freeze a revised product core in new test inputs; never change the target."""
import argparse
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boundary_runner import sha, snapshot

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--settings", type=Path, required=True)
parser.add_argument("--product-root", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
settings = json.loads(args.settings.read_text())
before = snapshot(Path(settings["target"]))
output = args.output.resolve()
output.mkdir(parents=True, exist_ok=False)
shutil.copyfile(__file__, output / "executed-refresh_product_inputs.py")
shutil.copyfile(args.settings, output / "original-settings.json")
settings["product_sha256"] = {}
for name, script, short in (("harness-orient", "orient.py", "orient"), ("harness-operator-brief", "check_brief.py", "brief")):
    source = args.product_root.resolve() / name
    destination = output / name
    shutil.copytree(source, destination)
    original = Path(settings["helpers"][short]).parents[1]
    for relative in ("scripts/" + script, "skill-contract.json"):
        assert sha(source / relative) == sha(original / relative), "Helper/contract changed"
    settings["helpers"][short] = str(destination / "scripts" / script)
    settings["product_sha256"].update({str(path): sha(path) for path in destination.rglob("*") if path.is_file()})
settings["read_roots"].append(str(output))
(output / "settings.json").write_text(json.dumps(settings, indent=2) + "\n")
assert snapshot(Path(settings["target"])) == before
(output / "refresh-record.json").write_text(json.dumps({"classification": "Explicit final product SKILL snapshot; unchanged actual helpers/contracts and target", "before": before, "after": snapshot(Path(settings["target"])), "source_sha256": sha(Path(__file__))}, indent=2) + "\n")
print(json.dumps({"settings": str(output / "settings.json")}))
