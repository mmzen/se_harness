"""Direct fixture calibration only; these are not Codex host observations."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe import INLINE_GUARD, digest, isolated_environment, retain, run, write

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--root", type=Path, required=True)
parser.add_argument("--wheel", type=Path, required=True)
parser.add_argument("--evidence", type=Path, required=True)
parser.add_argument("--inline", action="store_true")
args = parser.parse_args()
root = args.root.resolve()
if root.exists():
    parser.error("Calibration requires a fresh directory; retained data is never overwritten.")
home, repo, data = root / "home", root / "repo", root / "plugin-data"
for path in (home, repo, data, home / "tmp"):
    path.mkdir(parents=True)
env = isolated_environment(home)
plugin = root / "plugin with spaces"
plugin.mkdir()
for name in ("observe.ps1", "observe_runtime.py"):
    shutil.copy2(Path(__file__).with_name(name), plugin / name)
env.update(PLUGIN_ROOT=str(plugin), PLUGIN_DATA=str(data))
event = json.dumps({"hook_event_name": "SessionStart", "source": "startup", "cwd": str(repo)})
ps = Path(os.environ["SYSTEMROOT"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"

def hook(name):
    command = [str(ps), "-NoProfile", "-NonInteractive", "-File", str(plugin / "observe.ps1")]
    if args.inline:
        command = [str(ps), "-NoProfile", "-NonInteractive", "-Command", INLINE_GUARD]
    result = run(command, repo, env, timeout=30, input_text=event)
    retain(args.evidence, name, {"layer": "direct fixture calibration, not host",
        "stdin": event, **result})

hook("missing-runtime")
runtime = data / "environment"
commands = [("create-venv", [sys.executable, "-I", "-m", "venv", str(runtime)])]
python = runtime / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
commands += [("install-wheel", [str(python), "-I", "-m", "pip", "install", "--no-index", "--no-deps", str(args.wheel.resolve())]),
             ("init-fixture", [str(python), "-I", "-m", "se_harness", "init", str(repo), "--project-name", "codex-probe", "--json"])]
for name, command in commands:
    result = run(command, home, env, timeout=60)
    retain(args.evidence, name, result)
    if result["exit_status"] != 0:
        raise SystemExit(f"Calibration stopped: {name} exited {result['exit_status']}")
write(data / "runtime-path.txt", str(python))
hook("prepared-runtime")
# Rename only the disposable executable; preserve it for audit/recovery.
saved = python.with_name("python.removed-for-probe.exe" if os.name == "nt" else "python.removed-for-probe")
python.rename(saved)
try:
    hook("removed-runtime")
finally:
    saved.rename(python)
for name in ("events.jsonl", "inline-events.jsonl", "runtime-observations.jsonl"):
    path = data / name
    if path.exists():
        shutil.copy2(path, args.evidence / name)
write(args.evidence / "inputs.json", json.dumps({"layer": "direct fixture calibration, not host",
    "provided_python": sys.executable, "provided_python_version": sys.version,
    "wheel": str(args.wheel.resolve()), "wheel_sha256": digest(args.wheel),
    "fixture_digests": {p.name: digest(p) for p in plugin.iterdir() if p.is_file()}}, indent=2)+"\n")
print("Direct calibration retained; no Codex event-delivery claim.")
