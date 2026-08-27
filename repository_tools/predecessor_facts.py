"""Derive the predecessor-evaluator facts candidate CI needs from the declared root.

`WO-CIP-003` (`REQ-CIP-006`, `SPEC-CIP-001` CIP-PRE). The repository-owned
candidate-evidence workflow used to restate the predecessor's version, wheel
name, wheel digest, payload digest, acceptance-contract digest and migration
scenario path as literals, restated again in tests, so a version bump was three
hand edits and a silent skip when one was missed. This module derives every one
of them from `.engineering-harness.toml`, `.engineering-harness.lock`, the
candidate's own version and `tests/fixtures/governance_migration/`, and fails
closed, naming the expected path, when any of them cannot be derived.

It also carries the canonical scenario writer: `write-scenario` takes an
existing scenario as its template, re-points it at a predecessor/successor pair
using the same declared facts, recomputes the digests the contract checks, and
writes the canonical bytes (`canonical_json`: sorted keys, ASCII, minimal
separators, one trailing LF). Writing the committed pair from the committed
scenario reproduces it byte for byte.

Nothing here mutates the lock, the toml, or the checkout outside `--output`.

This module is standard-library only. `repository_tools` may not widen its
pinned import crossing into `se_harness` (the import-barrier tests pin it),
so the canonical writer and the digest rules are restated here in the same
form the contract module uses, and the tests prove the two agree byte for
byte. The full contract validation of a scenario stays with `se_harness
rehearse-migration`, which refuses a defective scenario before any stage runs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

TOML_NAME = ".engineering-harness.toml"
LOCK_NAME = ".engineering-harness.lock"
SCENARIOS = Path("tests/fixtures/governance_migration")

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
        raise PredecessorFactsError(
            f"PRE014: {LOCK_NAME} records no evaluator archive identity and exactly one released "
            f"release record for {version} is required to supply it; found {names}"
        )
    path, record = matches[0]
    distribution = record.get("distribution")
    if not isinstance(distribution, dict):
        raise PredecessorFactsError(f"PRE015: {record.get('id')} binds no distribution table")
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


class PredecessorFactsError(RuntimeError):
    """The declared root does not yield one complete set of predecessor facts."""


def canonical_json(value: Any) -> bytes:
    """The scenario writer: sorted keys, ASCII, minimal separators, one trailing LF."""

    return (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, item in pairs:
        if key in result:
            raise PredecessorFactsError(f"PRE014: duplicate key in scenario: {key}")
        result[key] = item
    return result


def load_scenario(path: Path) -> tuple[dict[str, Any], bytes]:
    """Read a scenario and check the digests the writer is responsible for."""

    try:
        raw = path.read_bytes()
        scenario = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (OSError, ValueError) as exc:
        raise PredecessorFactsError(f"PRE015: cannot read scenario {path.as_posix()}: {exc}") from exc
    if not isinstance(scenario, dict):
        raise PredecessorFactsError(f"PRE015: scenario {path.name} is not an object")
    if canonical_json(scenario) != raw:
        raise PredecessorFactsError(f"PRE016: scenario {path.name} is not in canonical form")
    try:
        fixture = scenario["fixture"]
        if sha256_bytes(canonical_json(fixture)) != scenario["fixture_sha256"]:
            raise PredecessorFactsError(f"PRE017: scenario {path.name} fixture digest mismatch")
        for decision in scenario["decisions"]:
            body = {key: item for key, item in decision.items() if key != "sha256"}
            if sha256_bytes(canonical_json(body)) != decision["sha256"]:
                raise PredecessorFactsError(f"PRE017: scenario {path.name} decision {decision.get('id')} digest mismatch")
        scenario["versions"]["predecessor"], scenario["versions"]["successor"]
        scenario["runtime_expectations"]["predecessor"]["archive_sha256"]
        scenario["runtime_expectations"]["successor"]["version"]
        scenario["scenario_id"]
    except (KeyError, TypeError) as exc:
        raise PredecessorFactsError(f"PRE018: scenario {path.name} lacks a field the writer maintains: {exc}") from exc
    return scenario, raw


@dataclass(frozen=True)
class PredecessorFacts:
    schema: str
    version: str
    wheel: str
    wheel_sha256: str
    payload_sha256: str
    acceptance_contract_sha256: str | None
    candidate_version: str
    scenario: str
    scenario_sha256: str

    def github_output_lines(self) -> str:
        lines = []
        for key, value in asdict(self).items():
            if key == "schema":
                continue
            lines.append(f"{key}={'' if value is None else value}")
        return "\n".join(lines) + "\n"


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise PredecessorFactsError(f"PRE001: {label} is missing or not a non-empty string")
    return value


def _require_sha256(value: Any, label: str) -> str:
    text = _require_string(value, label)
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise PredecessorFactsError(f"PRE002: {label} is not a lowercase SHA-256 hex digest")
    return text


def _candidate_version(repository: Path) -> str:
    pyproject = repository / "pyproject.toml"
    try:
        declared = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["version"]
    except (OSError, KeyError, tomllib.TOMLDecodeError) as exc:
        raise PredecessorFactsError(f"PRE003: cannot read the candidate version from {pyproject}: {exc}") from exc
    return _require_string(declared, "pyproject project.version")


def derive(repository: Path) -> PredecessorFacts:
    """Read the declared root and return the complete fact set, or raise."""

    repository = repository.resolve()
    toml_path = repository / TOML_NAME
    lock_path = repository / LOCK_NAME
    try:
        declared = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise PredecessorFactsError(f"PRE004: cannot read {toml_path}: {exc}") from exc
    try:
        lock = json.loads(lock_path.read_bytes())
    except (OSError, ValueError) as exc:
        raise PredecessorFactsError(f"PRE005: cannot read {lock_path}: {exc}") from exc
    tool_version = _require_string(declared.get("harness", {}).get("tool_version"), f"{TOML_NAME} harness.tool_version")
    evaluator = lock.get("evaluator")
    if not isinstance(evaluator, dict):
        raise PredecessorFactsError(f"PRE006: {LOCK_NAME} carries no evaluator identity; the root predates schema 3")
    version = _require_string(evaluator.get("version"), f"{LOCK_NAME} evaluator.version")
    if version != tool_version or lock.get("tool_version") != tool_version:
        raise PredecessorFactsError(
            f"PRE007: declared root versions disagree: {TOML_NAME} says {tool_version}, "
            f"{LOCK_NAME} says tool_version={lock.get('tool_version')} evaluator.version={version}"
        )
    wheel, wheel_sha256 = _evaluator_archive(repository, evaluator, version)
    payload_sha256 = _require_sha256(evaluator.get("payload_sha256"), f"{LOCK_NAME} evaluator.payload_sha256")
    candidate_version = _candidate_version(repository)
    if candidate_version == version:
        raise PredecessorFactsError(
            f"PRE008: the candidate version {candidate_version} equals the declared root version; there is no predecessor pair to rehearse"
        )
    scenario_path = repository / SCENARIOS / f"candidate-{version}-to-{candidate_version}.json"
    if not scenario_path.is_file():
        raise PredecessorFactsError(
            f"PRE009: no migration scenario for the pair {version} -> {candidate_version}; expected {scenario_path.as_posix()}. "
            "Write it with: python -m repository_tools.predecessor_facts write-scenario"
        )
    scenario, raw = load_scenario(scenario_path)
    expected = scenario["runtime_expectations"]["predecessor"]
    if scenario["versions"] != {"predecessor": version, "successor": candidate_version}:
        raise PredecessorFactsError(f"PRE010: {scenario_path.name} declares versions {scenario['versions']}, not the declared pair")
    if (expected["version"], expected["archive_name"], expected["archive_sha256"]) != (version, wheel, wheel_sha256):
        raise PredecessorFactsError(f"PRE011: {scenario_path.name} pins a predecessor archive other than the lock's")
    if scenario["runtime_expectations"]["successor"]["version"] != candidate_version:
        raise PredecessorFactsError(f"PRE012: {scenario_path.name} expects successor {scenario['runtime_expectations']['successor']['version']}")
    return PredecessorFacts(
        schema="se-harness-predecessor-facts-v1",
        version=version,
        wheel=wheel,
        wheel_sha256=wheel_sha256,
        payload_sha256=payload_sha256,
        acceptance_contract_sha256=LEGACY_ACCEPTANCE_CONTRACT_SHA256.get(version),
        candidate_version=candidate_version,
        scenario=scenario_path.relative_to(repository).as_posix(),
        scenario_sha256=sha256_bytes(raw),
    )


def _retarget(template: dict[str, Any], *, predecessor: dict[str, str], successor: str) -> dict[str, Any]:
    scenario = json.loads(canonical_json(template))
    scenario["scenario_id"] = f"candidate-{predecessor['version']}-to-{successor}"
    scenario["versions"] = {"predecessor": predecessor["version"], "successor": successor}
    scenario["runtime_expectations"]["predecessor"] = {
        "archive_name": predecessor["archive_name"],
        "archive_sha256": predecessor["archive_sha256"],
        "version": predecessor["version"],
    }
    scenario["runtime_expectations"]["successor"]["version"] = successor
    fixture = scenario["fixture"]
    for key in ("initial_proposal", "replacement_proposal"):
        fixture[key]["version"] = successor
    # The adopt stage recomputes the simulated immutable publication identity from
    # the adopted proposal and the successor version (MIG413), so a re-pointed
    # scenario must carry the digest of the new pair, not the template's
    # (WO-RLS-013; first written under WO-HUP-006, which was rejected).
    publication = {
        "artifact_id": fixture["replacement_proposal"]["artifact_id"],
        "immutable": True,
        "version": successor,
    }
    fixture["simulated_publication_sha256"] = sha256_bytes(canonical_json(publication))
    scenario["fixture_sha256"] = sha256_bytes(canonical_json(fixture))
    for decision in scenario["decisions"]:
        decision["sha256"] = sha256_bytes(canonical_json({key: item for key, item in decision.items() if key != "sha256"}))
    return scenario


def write_scenario(repository: Path, *, template: Path, predecessor: str | None, successor: str | None, output: Path | None) -> tuple[Path, bytes]:
    """Re-point `template` at a pair and write the canonical bytes; returns (path, bytes)."""

    repository = repository.resolve()
    scenario, _ = load_scenario(template)
    lock = json.loads((repository / LOCK_NAME).read_bytes())
    evaluator = lock.get("evaluator") or {}
    predecessor_version = predecessor or _require_string(evaluator.get("version"), f"{LOCK_NAME} evaluator.version")
    if predecessor_version == evaluator.get("version"):
        archive_name, archive_sha256 = _evaluator_archive(repository, evaluator, predecessor_version)
        pinned = {
            "version": predecessor_version,
            "archive_name": archive_name,
            "archive_sha256": archive_sha256,
        }
    else:
        raise PredecessorFactsError(
            f"PRE013: the lock pins {evaluator.get('version')}, not {predecessor_version}; a scenario pins only the declared root's archive"
        )
    successor_version = successor or _candidate_version(repository)
    if successor_version == predecessor_version:
        raise PredecessorFactsError("PRE008: predecessor and successor are the same version")
    retargeted = _retarget(scenario, predecessor=pinned, successor=successor_version)
    raw = canonical_json(retargeted)
    destination = output or (repository / SCENARIOS / f"{retargeted['scenario_id']}.json")
    if json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object) != retargeted or canonical_json(retargeted) != raw:
        raise PredecessorFactsError("PRE016: the writer did not produce canonical bytes")
    destination.write_bytes(raw)
    return destination, raw


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="python -m repository_tools.predecessor_facts", description=__doc__.split("\n\n")[0])
    commands = root.add_subparsers(dest="command", required=True)
    derive_parser = commands.add_parser("derive", help="print the derived facts; fail closed when any is missing")
    derive_parser.add_argument("--repository", default=".", help="checkout root (default: .)")
    derive_parser.add_argument("--github-output", help="append key=value lines for a GitHub Actions step")
    derive_parser.add_argument("--json", action="store_true", help="print the facts as canonical JSON")
    write_parser = commands.add_parser("write-scenario", help="write a migration scenario for the declared pair from a template scenario")
    write_parser.add_argument("--repository", default=".")
    write_parser.add_argument("--template", required=True, help="an existing scenario to re-point")
    write_parser.add_argument("--predecessor", help="predecessor version; default: the lock's evaluator")
    write_parser.add_argument("--successor", help="successor version; default: the candidate's pyproject version")
    write_parser.add_argument("--output", help="destination; default: tests/fixtures/governance_migration/candidate-<p>-to-<s>.json")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "derive":
            facts = derive(Path(args.repository))
            if args.github_output:
                with open(args.github_output, "a", encoding="utf-8", newline="\n") as handle:
                    handle.write(facts.github_output_lines())
            if args.json or not args.github_output:
                sys.stdout.write(canonical_json(asdict(facts)).decode("utf-8"))
            return 0
        destination, raw = write_scenario(
            Path(args.repository),
            template=Path(args.template),
            predecessor=args.predecessor,
            successor=args.successor,
            output=Path(args.output) if args.output else None,
        )
        sys.stdout.write(canonical_json({"written": destination.as_posix(), "sha256": sha256_bytes(raw), "bytes": len(raw)}).decode("utf-8"))
        return 0
    except PredecessorFactsError as exc:
        sys.stderr.write(f"{exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
