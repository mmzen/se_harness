"""Derive a release unit's work-order census from the commits between two refs.

`WO-CIP-004` (`REQ-CIP-004`, `SPEC-CIP-001` CIP-RLU, `ADR-CIP-002`). A release
contract names one candidate commit and the previous release tag; the work
orders in the unit are what the commits between them carry, read from their
`Harness-Work-Order:` trailers. This module measures that census. It mutates
nothing, needs no network, and holds no authority: the release owner's approval
of the contract is still the act that freezes the unit.

The walk follows the first-parent history from the tag to the candidate, oldest
first. A
non-merge commit contributes its own trailer; a merge commit contributes the
trailers of the commits it merged (its second-parent range), because the
repository's merges are created by the forge without a trailer. A commit that
carries no trailer anywhere is `untraced` and fails the derivation unless it is
exempted explicitly.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from se_harness.installer import HarnessError

RELEASE_UNIT_SCHEMA = "se-harness-release-unit-v1"
TRAILER = "Harness-Work-Order"
WORK_ORDER_PATTERN = re.compile(r"WO-[A-Z0-9]+-[0-9]{3}")
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?")
#: Paths whose bytes reach the distributed surface (pyproject: packages, package-data, data-files).
PACKAGED_SURFACE_PREFIXES = ("se_harness/", "templates/repository/standard/", "pyproject.toml")
SEPARATOR = "\x1f"


@dataclass(frozen=True)
class WorkOrderEntry:
    id: str
    status: str | None
    packaged_surface: bool | None
    commits: tuple[str, ...]


@dataclass(frozen=True)
class ReleaseUnit:
    schema: str
    from_ref: str
    from_commit: str
    to_ref: str
    to_commit: str
    work_orders: tuple[WorkOrderEntry, ...]
    untraced: tuple[str, ...]
    exempted: tuple[str, ...]
    gates: tuple[str, ...]
    complete: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["work_orders"] = [asdict(entry) for entry in self.work_orders]
        return value


StatusLookup = Callable[[str], tuple[str | None, bool | None]]


def _git(root: Path, *arguments: str) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments], capture_output=True, text=True, encoding="utf-8", check=False, timeout=120
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise HarnessError(f"git is unavailable: {exc}") from exc
    if completed.returncode != 0:
        raise HarnessError(f"git {' '.join(arguments[:2])} failed: {completed.stderr.strip() or completed.returncode}")
    return completed.stdout


def _resolve(root: Path, ref: str) -> str:
    return _git(root, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()


def _trailers(root: Path, revision_range: str, *, first_parent: bool) -> list[tuple[str, tuple[str, ...]]]:
    arguments = ["log", "--no-color", "--reverse", f"--format=%H{SEPARATOR}%P{SEPARATOR}%(trailers:key={TRAILER},valueonly,separator=;)"]
    if first_parent:
        arguments.append("--first-parent")
    arguments.append(revision_range)
    entries = []
    for line in _git(root, *arguments).splitlines():
        if not line.strip():
            continue
        sha, parents, raw = line.split(SEPARATOR, 2)
        found = tuple(sorted({item.strip() for item in raw.split(";") if WORK_ORDER_PATTERN.fullmatch(item.strip())}))
        entries.append((sha, parents.split(), found))
    return entries


def _catalog_lookup(root: Path) -> StatusLookup:
    from se_harness.workflow import _catalog, _validation

    _, report = _validation(root)
    catalog = _catalog(report)

    def lookup(work_order: str) -> tuple[str | None, bool | None]:
        artifact = catalog.get(work_order)
        if artifact is None:
            return None, None
        status = artifact.metadata.get("status")
        scope = artifact.metadata.get("execution_scope", {})
        paths = scope.get("paths", []) if isinstance(scope, dict) else []
        packaged = any(isinstance(item, str) and item.startswith(PACKAGED_SURFACE_PREFIXES) for item in paths)
        return (status if isinstance(status, str) else None), packaged

    return lookup


def derive_release_unit(
    repository: Path,
    *,
    from_ref: str,
    to_ref: str,
    exempt: Iterable[str] = (),
    lookup: StatusLookup | None = None,
) -> ReleaseUnit:
    """Measure the work-order census of `from_ref..to_ref` on the first-parent history."""

    root = repository.resolve()
    from_commit = _resolve(root, from_ref)
    to_commit = _resolve(root, to_ref)
    exempted = tuple(sorted({item.strip() for item in exempt if item.strip()}))
    for item in exempted:
        if not COMMIT_PATTERN.fullmatch(item):
            raise HarnessError(f"an exemption must be a full commit id: {item}")
    if lookup is None:
        lookup = _catalog_lookup(root)

    commits_by_work_order: dict[str, list[str]] = {}
    untraced: list[str] = []
    for sha, parents, own in _trailers(root, f"{from_commit}..{to_commit}", first_parent=True):
        found = set(own)
        if len(parents) > 1:
            for _merged, _parents, merged_trailers in _trailers(root, f"{parents[0]}..{parents[1]}", first_parent=False):
                found.update(merged_trailers)
        if not found:
            if sha not in exempted:
                untraced.append(sha)
            continue
        for work_order in sorted(found):
            commits_by_work_order.setdefault(work_order, []).append(sha)

    entries = []
    reasons: list[str] = []
    for work_order in sorted(commits_by_work_order):
        status, packaged = lookup(work_order)
        entries.append(WorkOrderEntry(work_order, status, packaged, tuple(commits_by_work_order[work_order])))
        if status is None:
            reasons.append(f"{work_order} has no artifact in the catalog")
        elif status != "implemented":
            reasons.append(f"{work_order} is {status}, not implemented")
    if untraced:
        reasons.append(f"{len(untraced)} commit(s) on the first-parent path carry no {TRAILER} trailer and are not exempted")
    return ReleaseUnit(
        schema=RELEASE_UNIT_SCHEMA,
        from_ref=from_ref,
        from_commit=from_commit,
        to_ref=to_ref,
        to_commit=to_commit,
        work_orders=tuple(entries),
        untraced=tuple(untraced),
        exempted=exempted,
        gates=tuple(entry.id for entry in entries),
        complete=not reasons,
        reasons=tuple(reasons),
    )


def compare_with_contract(unit: ReleaseUnit, contract: Mapping[str, Any]) -> list[str]:
    """Return E-CIP-001 findings: the declared unit differs from the measured one."""

    findings: list[str] = []
    declared_commit = contract.get("candidate_commit")
    if declared_commit != unit.to_commit:
        findings.append(f"E-CIP-001: contract candidate_commit {declared_commit!r} is not the derived candidate {unit.to_commit}")
    declared_tag = contract.get("previous_release_tag")
    if declared_tag != unit.from_ref:
        findings.append(f"E-CIP-001: contract previous_release_tag {declared_tag!r} is not the derivation's {unit.from_ref!r}")
    relations = contract.get("relations", {})
    declared = relations.get("gates", []) if isinstance(relations, dict) else []
    declared_work_orders = sorted(item for item in declared if isinstance(item, str) and WORK_ORDER_PATTERN.fullmatch(item))
    if declared_work_orders != list(unit.gates):
        missing = sorted(set(unit.gates) - set(declared_work_orders))
        extra = sorted(set(declared_work_orders) - set(unit.gates))
        findings.append(
            "E-CIP-001: contract gates differ from the derived census"
            + (f"; missing from gates: {', '.join(missing)}" if missing else "")
            + (f"; not in the derivation: {', '.join(extra)}" if extra else "")
        )
    if not unit.complete:
        findings.append("E-CIP-001: the derivation is incomplete: " + "; ".join(unit.reasons))
    return findings


def render_gates_toml(unit: ReleaseUnit) -> str:
    return "gates = [" + ", ".join(json.dumps(item) for item in unit.gates) + "]\n"


def render_release_unit(unit: ReleaseUnit, findings: list[str] | None = None) -> str:
    lines = [
        f"Release unit: {'COMPLETE' if unit.complete else 'INCOMPLETE'}",
        f"Range: {unit.from_ref} ({unit.from_commit[:12]}) .. {unit.to_ref} ({unit.to_commit[:12]})",
        f"Work orders: {len(unit.work_orders)} | untraced commits: {len(unit.untraced)} | exempted: {len(unit.exempted)}",
        "",
    ]
    for entry in unit.work_orders:
        surface = "packaged" if entry.packaged_surface else ("no packaged bytes" if entry.packaged_surface is False else "unknown scope")
        lines.append(f"- {entry.id}: {entry.status or 'not in catalog'}; {surface}; {len(entry.commits)} commit(s)")
    for sha in unit.untraced:
        lines.append(f"- untraced: {sha}")
    if unit.reasons:
        lines.append("")
        lines.append("Blockers")
        lines.extend(f"- {reason}" for reason in unit.reasons)
    if findings:
        lines.append("")
        lines.append("Contract comparison")
        lines.extend(f"- {finding}" for finding in findings)
    lines.append("")
    lines.append(render_gates_toml(unit).rstrip())
    lines.append("")
    lines.append("Authority: measurement only; the release owner's approval of the contract freezes the unit.")
    return "\n".join(lines)
