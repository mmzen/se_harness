"""Derive the root-evaluator facts candidate CI needs from the declared root.

`WO-CIP-003` (`REQ-CIP-006`, `SPEC-CIP-001` CIP-PRE), renamed from
`predecessor_facts` under `WO-ECP-010` (repository issue #210) when the
migration scenario it once required was retired. The repository-owned
candidate-evidence workflow used to restate the predecessor's version, wheel
name, wheel digest, payload digest and acceptance-contract digest as
literals, restated again in tests, so a version bump was several hand edits
and a silent skip when one was missed. This module derives every one of them
from `.engineering-harness.toml`, `.engineering-harness.lock`, the released
record binding the root version, and the candidate's own version, and fails
closed, naming what is missing, when any of them cannot be derived. Nothing
here mutates the lock, the toml, or the checkout.

This module is standard-library only; `repository_tools` may not widen its
pinned import crossing into `se_harness` (the import-barrier tests pin it).
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

TOML_NAME = ".engineering-harness.toml"
LOCK_NAME = ".engineering-harness.lock"

# Exact public releases that predate the `qualify` namespace accept a candidate
# through their fixed, digest-bound `accept-candidate` contract. The contract
# digest is a fact of that release, not of this repository's lock, so it is
# declared here once and asserted by tests, never restated in a workflow.
LEGACY_ACCEPTANCE_CONTRACT_SHA256 = {
    "0.6.0": "a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75",
    # 0.7.1 ships the same accept-candidate contract bytes; CONTRACT_SHA256 read
    # from the installed evaluator under WO-HUP-007.
    "0.7.1": "a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75",
}

RELEASE_RECORDS = Path("docs/engineering")


class EvaluatorFactsError(RuntimeError):
    """The declared root does not yield one complete set of evaluator facts."""


#: Retained name: the tests and notes of `WO-CIP-003` know the error by it.
PredecessorFactsError = EvaluatorFactsError


def _front_matter(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    if not text.startswith("+++"):
        return None
    end = text.find("\n+++", 3)
    if end < 0:
        return None
    try:
        return tomllib.loads(text[3:end])
    except tomllib.TOMLDecodeError:
        return None


def released_evaluator_archive(repository: Path, version: str) -> tuple[str, str]:
    """Return (wheel, wheel_sha256) from the one released record whose version is `version`."""

    matches: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted((repository / RELEASE_RECORDS).rglob("RLS-*.md")):
        value = _front_matter(path)
        if not value or value.get("type") != "release_record":
            continue
        if value.get("status") == "released" and value.get("version") == version:
            matches.append((path, value))
    if len(matches) != 1:
        names = ", ".join(str(item[1].get("id")) for item in matches) or "none"
        raise EvaluatorFactsError(
            f"PRE014: {LOCK_NAME} records no evaluator archive identity and exactly one released "
            f"release record for {version} is required to supply it; found {names}"
        )
    path, record = matches[0]
    distribution = record.get("distribution")
    if not isinstance(distribution, dict):
        raise EvaluatorFactsError(f"PRE015: {record.get('id')} binds no distribution table")
    return (
        _require_string(distribution.get("wheel"), f"{record.get('id')} distribution.wheel"),
        _require_sha256(distribution.get("wheel_sha256"), f"{record.get('id')} distribution.wheel_sha256"),
    )


def _evaluator_archive(repository: Path, evaluator: dict[str, Any], version: str) -> tuple[str, str]:
    """Return the root evaluator's (archive_name, archive_sha256) from the lock, or from the released record.

    A root adopted by the simple upgrade from an index install records no archive
    identity (REQ-REB-028); the wheel that release published is bound in this
    repository's own released record (owner decision of 2026-08-27, WO-HUP-007).
    """

    name = evaluator.get("archive_name")
    digest = evaluator.get("archive_sha256")
    if name is None and digest is None:
        return released_evaluator_archive(repository, version)
    return (
        _require_string(name, f"{LOCK_NAME} evaluator.archive_name"),
        _require_sha256(digest, f"{LOCK_NAME} evaluator.archive_sha256"),
    )


def canonical_json(value: Any) -> bytes:
    """Sorted keys, ASCII, minimal separators, one trailing LF."""

    return (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


@dataclass(frozen=True)
class EvaluatorFacts:
    schema: str
    version: str
    wheel: str
    wheel_sha256: str
    payload_sha256: str
    acceptance_contract_sha256: str | None
    candidate_version: str

    def github_output_lines(self) -> str:
        lines = []
        for key, value in asdict(self).items():
            if key == "schema":
                continue
            lines.append(f"{key}={'' if value is None else value}")
        return "\n".join(lines) + "\n"


#: Retained name for the `WO-CIP-003` tests.
PredecessorFacts = EvaluatorFacts


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise EvaluatorFactsError(f"PRE001: {label} is missing or not a non-empty string")
    return value


def _require_sha256(value: Any, label: str) -> str:
    text = _require_string(value, label)
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise EvaluatorFactsError(f"PRE002: {label} is not a lowercase SHA-256 hex digest")
    return text


def _candidate_version(repository: Path) -> str:
    pyproject = repository / "pyproject.toml"
    try:
        declared = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["version"]
    except (OSError, KeyError, tomllib.TOMLDecodeError) as exc:
        raise EvaluatorFactsError(f"PRE003: cannot read the candidate version from {pyproject}: {exc}") from exc
    return _require_string(declared, "pyproject project.version")


def derive(repository: Path) -> EvaluatorFacts:
    """Read the declared root and return the complete fact set, or raise."""

    repository = repository.resolve()
    toml_path = repository / TOML_NAME
    lock_path = repository / LOCK_NAME
    try:
        declared = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise EvaluatorFactsError(f"PRE004: cannot read {toml_path}: {exc}") from exc
    try:
        lock = json.loads(lock_path.read_bytes())
    except (OSError, ValueError) as exc:
        raise EvaluatorFactsError(f"PRE005: cannot read {lock_path}: {exc}") from exc
    tool_version = _require_string(declared.get("harness", {}).get("tool_version"), f"{TOML_NAME} harness.tool_version")
    evaluator = lock.get("evaluator")
    if not isinstance(evaluator, dict):
        raise EvaluatorFactsError(f"PRE006: {LOCK_NAME} carries no evaluator identity; the root predates schema 3")
    version = _require_string(evaluator.get("version"), f"{LOCK_NAME} evaluator.version")
    if version != tool_version or lock.get("tool_version") != tool_version:
        raise EvaluatorFactsError(
            f"PRE007: declared root versions disagree: {TOML_NAME} says {tool_version}, "
            f"{LOCK_NAME} says tool_version={lock.get('tool_version')} evaluator.version={version}"
        )
    wheel, wheel_sha256 = _evaluator_archive(repository, evaluator, version)
    payload_sha256 = _require_sha256(evaluator.get("payload_sha256"), f"{LOCK_NAME} evaluator.payload_sha256")
    candidate_version = _candidate_version(repository)
    if candidate_version == version:
        raise EvaluatorFactsError(
            f"PRE008: the candidate version {candidate_version} equals the declared root version; there is no predecessor pair to rehearse"
        )
    return EvaluatorFacts(
        schema="se-harness-evaluator-facts-v1",
        version=version,
        wheel=wheel,
        wheel_sha256=wheel_sha256,
        payload_sha256=payload_sha256,
        acceptance_contract_sha256=LEGACY_ACCEPTANCE_CONTRACT_SHA256.get(version),
        candidate_version=candidate_version,
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="python -m repository_tools.evaluator_facts", description=__doc__.split("\n\n")[0])
    commands = root.add_subparsers(dest="command", required=True)
    derive_parser = commands.add_parser("derive", help="print the derived facts; fail closed when any is missing")
    derive_parser.add_argument("--repository", default=".", help="checkout root (default: .)")
    derive_parser.add_argument("--github-output", help="append key=value lines for a GitHub Actions step")
    derive_parser.add_argument("--json", action="store_true", help="print the facts as canonical JSON")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        facts = derive(Path(args.repository))
    except EvaluatorFactsError as exc:
        sys.stderr.write(f"{exc}\n")
        return 2
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(facts.github_output_lines())
    if args.json or not args.github_output:
        sys.stdout.write(canonical_json(asdict(facts)).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
