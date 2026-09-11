"""Open the accepted host's real hooks review in its disposable profile."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).absolute().parent))
from fixture import SANDBOX, host_argv, host_environment
from processes import spawn, stop_owned_tree, close_owned_tree

process = spawn(host_argv("--no-alt-screen", "--sandbox", "read-only", "--ask-for-approval", "on-request"),
                cwd=SANDBOX / "repo with spaces", env=host_environment())
try:
    code = process.wait()
    close_owned_tree(process)
    raise SystemExit(code)
finally:
    if process.poll() is None:
        stop_owned_tree(process)
