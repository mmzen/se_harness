"""Open the real /hooks UI in an existing authenticated disposable profile.

The invoking terminal shows the host interaction. Login output and credentials
are never retained by this helper. It does not set or bypass hook trust.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe import isolated_environment, run
from processes import close_owned_tree, spawn, stop_owned_tree


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', required=True, type=Path)
    parser.add_argument('--sandbox', required=True, type=Path)
    args = parser.parse_args()
    sandbox = args.sandbox.resolve()
    checkout = Path(__file__).resolve().parents[3]
    if sandbox == checkout or checkout in sandbox.parents:
        parser.error('The disposable sandbox must remain outside the checkout.')
    config = sandbox / 'profile/codex/config.toml'
    if not config.is_file() or 'cli_auth_credentials_store = "file"' not in config.read_text():
        parser.error('Expected existing disposable file-auth configuration.')
    env = isolated_environment(sandbox / 'profile')
    status = run([str(args.codex), 'login', 'status'], sandbox / 'repo', env, timeout=20)
    if status['exit_status'] != 0 or status['timed_out']:
        parser.error('The isolated profile is not signed in; no interactive session started.')
    process = spawn([str(args.codex), '--no-alt-screen', '--sandbox', 'read-only',
                     '--ask-for-approval', 'on-request'], cwd=sandbox / 'repo', env=env)
    try:
        code = process.wait()
        close_owned_tree(process)
        return code
    finally:
        if process.poll() is None:
            stop_owned_tree(process)


if __name__ == '__main__':
    raise SystemExit(main())
