"""Activate or clear one host session's exact checkout, without repository writes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_runtime import (DeliveryError, exact_repository, private_data, session_file,
    read_regular, exclusive, atomic_json)
from inject_instructions import bootstrap, bounded_context, repository_context, session_guidance


def activate(host: str, session: str, data: Path, target: Path | None) -> str:
    root = exact_repository(str(target)) if target is not None else None
    data = private_data(host, data, root)
    path = session_file(host, session, data)
    # Lock before resolving resources; delivery refuses while a switch is underway.
    # A refused target leaves the old locator byte-for-byte unchanged.
    with exclusive(path.with_suffix(".lock")):
        if root is None:
            context = bootstrap(host, session, data)
            if path.exists():
                read_regular(path, 16384)
                path.unlink()
            return context
        context = bounded_context(session_guidance(host, session, data) + "\n" + repository_context(root, data), host)
        atomic_json(path, {"schema":"se-harness-session-v1", "host":host,
                           "session_id":session, "repository":str(root)})
    return context


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=("codex", "claude"), required=True)
    parser.add_argument("--session-id", required=True, help="Use the identity delivered by the host hook.")
    parser.add_argument("--data-root", type=Path, required=True)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--target", type=Path)
    selection.add_argument("--clear", action="store_true")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        context = activate(args.host, args.session_id, args.data_root, args.target)
    except (ValueError, OSError, KeyError, TypeError, AttributeError, UnicodeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status":"unavailable", "error":str(exc),
            "action":"Stop work on the requested target, resolve its setup or selection gap, then activate again. The previous session record is unchanged."}))
        return 1
    print(json.dumps({"status":"available", "host":args.host, "session_id":args.session_id, "content":context}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
