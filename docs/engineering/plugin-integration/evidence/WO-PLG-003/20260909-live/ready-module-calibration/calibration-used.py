from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess

work = Path(__file__).resolve().parent
checkout = work / "se-harness-plugin-codex-probe"
source = checkout / "tests/plugin_integration/codex_probe/observe_ready_runtime.py"
repo = work / "plugin-probe-sandboxes/readiness-input-20260909/repository"
data = work / "plugin-probe-sandboxes/codex/readiness-module-calibration"
data.mkdir(exist_ok=False)
evidence = checkout / "docs/engineering/plugin-integration/evidence/WO-PLG-003/20260909-live/ready-module-calibration"
evidence.mkdir(exist_ok=False)
env = os.environ.copy()
env.pop("PYTHONPATH", None)
env["PLUGIN_DATA"] = str(data)
argv = [str(work / "se-harness-plugin-eval-016/Scripts/python.exe"), "-I", "-B", str(source)]
event = {"cwd": str(repo), "hook_event_name": "SessionStart", "source": "startup"}
result = subprocess.run(argv, input=json.dumps(event).encode(), env=env, capture_output=True, timeout=90)
for name, value in (("stdout", result.stdout), ("stderr", result.stderr)):
    (evidence / (name + ".txt")).write_bytes(value)
record = {"argv": argv, "input": event, "exit_code": result.returncode,
          "fixture_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
          "kind": "Direct observer calibration; not a host event or acceptance result."}
(evidence / "command.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf8")
shutil.copyfile(source, evidence / source.name)
shutil.copyfile(__file__, evidence / "calibration-used.py")
events = data / "runtime-readiness-observations.jsonl"
if events.exists():
    shutil.copyfile(events, evidence / events.name)
    reading = json.loads(events.read_text())
    print(json.dumps({"exit": result.returncode, "ready": reading["governance_readiness"],
                      "checks": {key: value["exit_status"] for key, value in reading["checks"].items()},
                      "manifest_files": len(reading.get("manifest_files", []))}))
else:
    print(json.dumps({"exit": result.returncode, "record_missing": True, "stderr": result.stderr.decode("utf8", "replace")}))
raise SystemExit(result.returncode)
