"""Prove a corrupted replay input is rejected before a target is created."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--bundle", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=False)
copy = args.output / "corrupt-bundle"
shutil.copytree(args.bundle, copy)
path = copy / "raw-assets/src/feature.py"
path.write_bytes(path.read_bytes() + b"# injected raw fixture corruption\n")
target = args.output / "must-not-be-created"
argv = [sys.executable, "-I", "-B", str(Path(__file__).with_name("run_replay.py")),
        "--bundle", str(copy), "--output", str(target), "--batch", "rejected-input"]
result = subprocess.run(argv, capture_output=True, timeout=30)
row = {"classification": "Test-runner input integrity, not a candidate skill failure", "argv": argv,
       "exit_code": result.returncode, "stdout": result.stdout.decode("utf8", "replace"),
       "stderr": result.stderr.decode("utf8", "replace"), "target_created": target.exists()}
row["passed"] = result.returncode == 1 and not target.exists() and "Fixture input mismatch: raw-assets/src/feature.py" in row["stderr"]
(args.output / "result.json").write_text(json.dumps(row, indent=2) + "\n", encoding="utf8", newline="\n")
print(json.dumps(row, indent=2))
raise SystemExit(0 if row["passed"] else 1)
