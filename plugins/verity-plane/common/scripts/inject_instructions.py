#!/usr/bin/env python3
"""Read the selected repository's locked root for a native SessionStart event.

No repository writes, lifecycle selection, evaluator installation or cached
policy fallback occur here. The selected evaluator still assesses governed acts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

# Only the adjacent reviewed plugin helper is added, never the target checkout.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_runtime import (DeliveryError, unique_object, read_regular, selected_repository,
    private_data, session_file, read_selection, unchanged_selection, release_selection,
    installed_python, match_identity)


MAX_INPUT_BYTES = 64 * 1024
MAX_CONTEXT_CHARACTERS = 10000  # The smaller documented host context limit.
MAX_ROOT_BYTES = 64 * 1024
MAX_CONFIG_BYTES = 1024 * 1024
SOURCES = {"codex": {"startup", "resume", "clear", "compact"},
           "claude": {"startup", "resume", "clear", "compact", "fork"}}


def repository_context(root: Path, data: Path) -> str:
    config, lock, inputs = release_selection(root)
    private_data("codex", data, root)
    version = config["harness"]["tool_version"]
    if lock["schema"] == 5:
        python = installed_python(data, lock["evaluator"])
        result = subprocess.run([str(python), "-I", "-m", "se_harness", "resources", str(root),
            "--resource", "ENGINEERING_HARNESS.md", "--content", "--json"], cwd=data,
            capture_output=True, text=True, encoding="utf-8", timeout=7)
        if result.returncode:
            raise DeliveryError("selected resources are unavailable or fail integrity; run the selected evaluator's resources command to inspect")
        value = json.loads(result.stdout, object_pairs_hook=unique_object)
        if value.get("schema") != "se-harness-resources-v1" or value.get("resource_layout") != "released-resources-v1":
            raise DeliveryError("the evaluator returned an incompatible resource result")
        match_identity(lock["evaluator"], value["release"])
        text, digest = value["content"], value["content_sha256"]
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != digest:
            raise DeliveryError("the delivered entry content digest does not match")
        entry = value["resources"][0]
        if entry["resource"] != "ENGINEERING_HARNESS.md":
            raise DeliveryError("the evaluator did not return the selected entry")
        for name, raw in inputs.items():
            if read_regular(root/name, MAX_CONFIG_BYTES) != raw:
                raise DeliveryError("selected instruction inputs changed during delivery")
        return (f"Selected checkout: {root}\nEntry resource: ENGINEERING_HARNESS.md\n"
                f"Selected release: {version}; entry SHA-256: {digest}.\n"
                f"Evaluator Python: {python}\n"
                "Use -I -m se_harness outside the checkout. Resolve instruction IDs through resources; "
                "formal artifacts against the checkout.\n\n" + text)
    config_path, lock_path = root / ".engineering-harness.toml", root / ".engineering-harness.lock"
    config_raw = read_regular(config_path, MAX_CONFIG_BYTES)
    lock_raw = read_regular(lock_path, MAX_CONFIG_BYTES)
    config = tomllib.loads(config_raw.decode("utf-8"))
    lock = json.loads(lock_raw, object_pairs_hook=unique_object)
    version = config.get("harness", {}).get("tool_version")
    if (not isinstance(version, str) or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version) is None
            or not isinstance(lock, dict) or lock.get("schema") not in {3, 4}
            or lock.get("tool_version") != version or lock.get("evaluator", {}).get("version") != version):
        raise DeliveryError("configuration and installation record do not select the same supported release")
    if lock.get("hash_algorithm") != "sha256" or lock.get("hash_mode") != "utf8-text-lf-v1":
        raise DeliveryError("unsupported installed-root hash convention")
    entry = lock.get("files", {}).get("ENGINEERING_HARNESS.md", {})
    if entry.get("mode") != "managed" or not isinstance(entry.get("sha256"), str):
        raise DeliveryError("the installation record does not own the instruction entry")
    raw = read_regular(root / "ENGINEERING_HARNESS.md", MAX_ROOT_BYTES)
    text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if digest != entry["sha256"]:
        raise DeliveryError("ENGINEERING_HARNESS.md does not match its installed digest")
    if f"This repository uses SE Harness {version}." not in text.splitlines():
        raise DeliveryError("the instruction entry does not name the selected release")
    # Refuse a concurrent selection change instead of mixing two installations.
    if (read_regular(config_path, MAX_CONFIG_BYTES) != config_raw
            or read_regular(lock_path, MAX_CONFIG_BYTES) != lock_raw
            or read_regular(root / "ENGINEERING_HARNESS.md", MAX_ROOT_BYTES) != raw):
        raise DeliveryError("selected instruction inputs changed during delivery; inspect before retrying")
    return (f"SE Harness instruction source: {root / 'ENGINEERING_HARNESS.md'}\n"
               f"Selected release: {version}; entry SHA-256: {digest}.\n"
               "This delivery changes no lifecycle state and grants no decision authority.\n\n" + text)


def session_guidance(host: str, session: str, data: Path) -> str:
    return (f"Host: {host}; session_id: {session}\nPlugin data: {data}\n"
            "Select or switch through verity-plane:setup (scripts/activate.py in this plugin).\n")


def bounded_context(context: str) -> str:
    if len(context.encode("utf-16-le")) // 2 > MAX_CONTEXT_CHARACTERS:
        raise DeliveryError("the complete root exceeds the host delivery limit; no truncated policy was sent")
    return context


def bootstrap(host: str, session: str, data: Path) -> str:
    text = read_regular(Path(__file__).resolve().parents[1]/"assets/bootstrap.md", MAX_ROOT_BYTES).decode("utf-8")
    return bounded_context(session_guidance(host, session, data) + "\n" + text)


def context_for(event: dict, host: str) -> str:
    if event.get("input_error"):
        raise DeliveryError(event["input_error"])
    if event.get("hook_event_name") != "SessionStart" or event.get("source") not in SOURCES[host]:
        raise DeliveryError("unsupported host event or SessionStart source")
    data = private_data(host)
    session = event.get("session_id")
    path = session_file(host, session, data)
    root, saved = read_selection(path, host, session)
    if root is None:
        root = selected_repository(event.get("cwd"))
    context = (bootstrap(host, session, data) if root is None else
               bounded_context(session_guidance(host, session, data) + "\n" + repository_context(root, data)))
    unchanged_selection(path, saved)
    return context


def respond(event: dict, host: str) -> dict:
    try:
        context = context_for(event, host)
    except (DeliveryError, OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError, RecursionError, subprocess.TimeoutExpired) as exc:
        # Both supported hosts deliver SessionStart additionalContext. A hook
        # error exit can discard it, so report the bounded gap through that channel.
        reason = str(exc).replace("\n", " ").replace("\r", " ")[:700]
        context = ("SE Harness instruction delivery is unavailable: " + reason + ". "
                   "Stop the affected governed action and report this gap. Confirm the selected "
                   "repository and released evaluator before continuing. Do not reuse another "
                   "repository's instructions, invent lifecycle authority, silently upgrade, "
                   "or restore an AGENTS managed gate. Read-only discussion is still available.")
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=tuple(SOURCES), required=True)
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise DeliveryError("host event exceeds the input limit")
        event = json.loads(raw, object_pairs_hook=unique_object)
        if not isinstance(event, dict):
            raise DeliveryError("host event is not a JSON object")
    except (ValueError, UnicodeError, RecursionError) as exc:
        event = {"input_error": str(exc)}
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(respond(event, args.host), ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
