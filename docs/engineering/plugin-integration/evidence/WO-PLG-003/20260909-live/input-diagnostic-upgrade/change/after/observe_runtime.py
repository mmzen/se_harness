"""Record supplied runtime and exact source bytes; never determine authority."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time

data = Path(os.environ["PLUGIN_DATA"])
raw = sys.stdin.buffer.read()
try:
    event = json.loads(raw.decode('utf-8-sig'))
except (UnicodeError, ValueError) as error:
    with (data / 'runtime-input-errors.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps({'timestamp': time.time(), 'stage': 'input decode',
            'error_type': type(error).__name__, 'error': str(error),
            'byte_length': len(raw), 'prefix_hex': raw[:4].hex(),
            'stdin_encoding': sys.stdin.encoding}) + '\n')
    raise
repo = Path(event["cwd"])
identity_argv = [sys.executable, "-I", "-m", "se_harness", "identity", "--role",
                 "released-evaluator", "--expected-version", "0.16.0", "--expected-root",
                 sys.prefix, "--checkout-root", str(repo), "--require-isolated-python", "--json"]
doctor_argv = [sys.executable, "-I", "-m", "se_harness", "doctor", str(repo), "--json"]
checks = []
for argv in (identity_argv, doctor_argv):
    result = subprocess.run(argv, cwd=data, capture_output=True, text=True, timeout=20)
    checks.append({"argv": argv, "exit_status": result.returncode,
                   "stdout": result.stdout, "stderr": result.stderr})
sources = {}
for name in ("AGENTS.md", "ENGINEERING_HARNESS.md"):
    path = repo / name
    if path.is_file():
        content = path.read_bytes()
        sources[name] = {"sha256": hashlib.sha256(content).hexdigest(),
                         "text": content.decode("utf-8")}
record = {"timestamp": time.time(), "event": event.get("hook_event_name"),
          "source": event.get("source"), "python": sys.executable,
          "version": importlib.metadata.version("se-harness"), "checks": checks,
          "sources": sources, "production_readiness_claim": False}
with (data / "runtime-observations.jsonl").open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(record)+"\n")
if event.get("hook_event_name") == "SessionStart":
    if all(c["exit_status"] == 0 for c in checks) and len(sources) == 2:
        print("CODEX_PROBE_CONTEXT_003: Fixture-only runtime/source observations follow.")
        print("\n".join(v["text"] for v in sources.values()))
    else:
        print("CODEX_PROBE_CONTEXT_003: Setup required; fixture runtime/source checks failed.")
