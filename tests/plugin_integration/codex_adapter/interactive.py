"""Prepared, separately approved hook-review UI with an external stop marker.

This does not grant authorization to run UI. No menu command is sent by this
helper. Use one tool navigation action, inspect, then act; after the one reviewed
hook, create the exact marker from an external shell instead of navigating away.
"""
import argparse
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).absolute().parent))
from fixture import ROOT, SANDBOX, host_argv, host_environment, sha, write
from processes import spawn, stop_owned_tree


def review_until_stopped(argv, repo, env, marker, deadline_seconds, *, record, factory=spawn, cleanup=stop_owned_tree):
    process = factory(argv, cwd=repo, env=env)
    try:
        record.update(pid=process.pid, started_monotonic=time.monotonic(), argv=argv)
        deadline = time.monotonic() + deadline_seconds
        while process.poll() is None:
            if marker.exists():
                record["stop_reason"] = "external marker"
                break
            if time.monotonic() >= deadline:
                record["stop_reason"] = "fixed review deadline"
                break
            time.sleep(.05)
    finally:
        record["cleanup"] = cleanup(process)
        record["finished_monotonic"] = time.monotonic()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stop-file", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    marker, destination = args.stop_file.absolute(), args.evidence.absolute()
    allowed = ROOT / "docs/engineering/plugin-integration/evidence/WO-PLG-005"
    if (marker.parent != SANDBOX or marker.exists() or allowed not in destination.parents or destination.exists()):
        parser.error("use a fresh stop marker directly in the selected sandbox and a fresh WO-PLG-005 evidence directory")
    destination.mkdir(parents=True)
    argv = host_argv("--no-alt-screen", "--sandbox", "read-only", "--ask-for-approval", "on-request")
    record = {"marker": str(marker), "deadline_seconds": 180, "source_sha256": sha(Path(__file__)),
              "purpose": "One separately approved native hook review only; no setup/menu exit navigation"}
    write(destination / "launch.json", {**record, "argv": argv})
    try:
        review_until_stopped(argv, SANDBOX / "repo with spaces", host_environment(), marker, 180, record=record)
    finally:
        write(destination / "outcome.json", record)


if __name__ == "__main__":
    main()
