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
import sys
import tomllib


MAX_INPUT_BYTES = 64 * 1024
MAX_CONTEXT_CHARACTERS = 10000  # The smaller documented host context limit.
MAX_ROOT_BYTES = 64 * 1024
MAX_CONFIG_BYTES = 1024 * 1024
SOURCES = {"codex": {"startup", "resume", "clear", "compact"},
           "claude": {"startup", "resume", "clear", "compact", "fork"}}


class DeliveryError(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise DeliveryError("duplicate JSON field in the delivery inputs")
        result[name] = value
    return result


def read_regular(path: Path, limit: int) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise DeliveryError(f"required regular file is unavailable: {path.name}")
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise DeliveryError(f"input exceeds the delivery size limit: {path.name}")
    return raw


def selected_repository(cwd: object) -> Path:
    if not isinstance(cwd, str) or not cwd or any(ord(c) < 32 for c in cwd):
        raise DeliveryError("the host did not supply an unambiguous absolute repository directory")
    requested = Path(cwd)
    if not requested.is_absolute() or not requested.is_dir():
        raise DeliveryError("the host working directory is unavailable or not absolute")
    current = requested.resolve(strict=True)
    for directory in (current, *current.parents):
        config, lock = directory / ".engineering-harness.toml", directory / ".engineering-harness.lock"
        if config.exists() or lock.exists():
            # Stop at the nearest selected installation. Never bypass a damaged
            # nested selection by borrowing a parent's otherwise valid root.
            return directory
        if (directory / ".git").exists():
            break
    raise DeliveryError("the host directory has no selected SE Harness installation")


def context_for(event: dict, host: str) -> str:
    if event.get("input_error"):
        raise DeliveryError(event["input_error"])
    if event.get("hook_event_name") != "SessionStart" or event.get("source") not in SOURCES[host]:
        raise DeliveryError("unsupported host event or SessionStart source")
    root = selected_repository(event.get("cwd"))
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
    context = (f"SE Harness instruction source: {root / 'ENGINEERING_HARNESS.md'}\n"
               f"Selected release: {version}; entry SHA-256: {digest}.\n"
               "This delivery changes no lifecycle state and grants no decision authority.\n\n" + text)
    if len(context.encode("utf-16-le")) // 2 > MAX_CONTEXT_CHARACTERS:
        raise DeliveryError("the complete root exceeds the host delivery limit; no truncated policy was sent")
    return context


def respond(event: dict, host: str) -> dict:
    try:
        context = context_for(event, host)
    except (DeliveryError, OSError, UnicodeError, ValueError, TypeError, AttributeError, RecursionError) as exc:
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
