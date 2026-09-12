"""Disposable evaluator-failure injection; never shipped with the plugin."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

mode, folder = sys.argv[1], Path(sys.argv[2])
folder.mkdir(parents=True, exist_ok=True)
(folder / "partial-check.txt").write_text("partial evaluator write retained\n")
child = subprocess.Popen([sys.executable, "-I", "-c", "import time; time.sleep(90)"],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
(folder / "pids.json").write_text(json.dumps({"parent": os.getpid(), "child": child.pid}))
if mode == "failed":
    raise SystemExit(3)
if mode == "interrupted":
    os.kill(os.getpid(), signal.SIGTERM)
time.sleep(90)
