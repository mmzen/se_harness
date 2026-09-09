"""Operator-only device login for an existing disposable probe profile.

No output capture, no credential copying, no evidence writes. The device code
and login URL stay in the invoking terminal, outside the public evidence.
"""
import argparse
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe import isolated_environment

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--codex", type=Path, required=True)
parser.add_argument("--sandbox", type=Path, required=True)
args = parser.parse_args()
sandbox = args.sandbox.resolve()
config = sandbox / "profile/codex/config.toml"
if not config.exists() or 'cli_auth_credentials_store = "file"' not in config.read_text():
    parser.error("Expected existing disposable file-auth configuration.")
raise SystemExit(subprocess.call([str(args.codex), "login", "--device-auth"],
    cwd=sandbox / "repo", env=isolated_environment(sandbox / "profile")))
