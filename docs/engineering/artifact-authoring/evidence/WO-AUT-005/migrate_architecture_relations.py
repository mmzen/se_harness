#!/usr/bin/env python3
"""Migrate the fifteen legacy architectures to typed relations and assessments.

Retained evidence for `WO-AUT-005`, rules `AUT-MIG-001` to `AUT-MIG-004` of
`SPEC-AUT-003`. For each architecture whose relations carry `constrains`:
requirement targets move to `addresses`, specification targets to
`conforms_to`, `conforms_to` also names every active specification that
specifies an addressed requirement, the fourteen without one gain a
`[decision_assessment]`, `updated` is bumped, and an amendment record naming
the work order is appended. Title, status, statement and ADR relations are
never touched. ``--apply`` writes; the default is a dry run that prints the
plan as JSON. The script refuses to write if any post-condition of
`AUT-MIG-001`, `AUT-MIG-002` or the validator's typed-relation rules fails.

Two cases the rules do not cover literally were decided by the engineering
owner on 2026-09-08, by selecting the presented options 'Address the whole
specification' and 'Omit them from addresses':

- three architectures whose `constrains` names a specification only take
  `addresses` from that specification's `specifies` set, matching the
  convention of 55 of the 67 already-typed architectures;
- two `superseded` requirements are left out of `addresses`, because an
  active architecture addressing an inactive requirement reads `E016`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

# Definition-family statuses that grant authority, read from the released
# 0.16.0 evaluator's WORKFLOW_LIFECYCLES["definition"].
DEFINITION_AUTHORITY = frozenset({"approved", "implemented", "in_progress", "released", "verified"})
AMENDED = "2026-09-08"
WORK_ORDER = "WO-AUT-005"

# Architectures whose legacy relation names no requirement: `addresses` comes
# from the conforming specification's `specifies` set.
ADDRESSES_FROM_SPECIFICATIONS = frozenset({"ARCH-AGR-001", "ARCH-PMI-001", "ARCH-VSP-001"})
# Superseded requirements an active architecture may not address.
OMITTED_ADDRESSES = {
    "ARCH-DST-002": ("REQ-DST-008",),
    "ARCH-IAR-001": ("REQ-IAR-005",),
}

ASSESSMENTS: dict[str, dict[str, object]] = {
    "ARCH-AGR-001": {
        "triggers": [
            "public-interface-or-protocol",
            "data-ownership-or-persistence",
            "difficult-to-reverse",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-AGR-001 chose one aggregate verification record at the final release candidate "
            "over four rejected models. It changed the public record relations, the persisted "
            "provenance of every release, and a boundary that published records make hard to reverse."
        ),
    },
    "ARCH-DST-001": {
        "triggers": [
            "system-boundary",
            "data-ownership-or-persistence",
            "difficult-to-reverse",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-DST-001 chose one canonical template with hash-based ownership over minimal and "
            "offline installation modes. It fixed the distribution boundary, what the lock persists "
            "about tool-owned content, and an ownership model installed repositories cannot cheaply leave."
        ),
    },
    "ARCH-DST-002": {
        "triggers": [
            "public-interface-or-protocol",
            "responsibility-or-dependency-direction",
            "difficult-to-reverse",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-DST-002 chose root AGENTS.md as the cross-agent contract with a CLAUDE.md import, "
            "over duplicating the contract and over a Windows-sensitive symbolic link. It also seeds "
            "repository context once per installation lineage, a lock fact later installs cannot retract."
        ),
    },
    "ARCH-DST-003": {
        "triggers": [
            "public-interface-or-protocol",
            "technology-framework-vendor-or-external-service",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-DST-003 chose one README serving as repository entry point and PyPI long description, "
            "over a separate package README and over build-time generation. It binds public packaging "
            "metadata to an external index and its rendering."
        ),
    },
    "ARCH-DST-004": {
        "triggers": [
            "public-interface-or-protocol",
            "technology-framework-vendor-or-external-service",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-DST-004 chose paired narrative, inline semantic Mermaid and a complete textual "
            "fallback over four alternatives. It adds a renderer-dependent element to the same file "
            "PyPI publishes as package metadata."
        ),
    },
    "ARCH-DST-005": {
        "triggers": [
            "cross-cutting-policy",
            "responsibility-or-dependency-direction",
            "difficult-to-reverse",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-DST-005 chose advisory canonical paths with safe authoring commands, over validation "
            "errors, a repository-wide type tree and automatic reorganization. It keeps authority in "
            "typed relations and lifecycle state rather than in paths, across every domain."
        ),
    },
    "ARCH-IAR-001": {
        "triggers": [
            "system-boundary",
            "responsibility-or-dependency-direction",
            "cross-cutting-policy",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-IAR-001 chose a thin AGENTS.md fragment, one fully managed router and focused policy "
            "modules over seven rejected alternatives. It fixed the instruction system boundary and "
            "where authority is defined for every actor reading the repository."
        ),
    },
    "ARCH-IAR-002": {
        "triggers": [
            "responsibility-or-dependency-direction",
            "cross-cutting-policy",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-IAR-002 chose to keep non-waivable invariants in the router and ordered procedure in "
            "WORKFLOW.md, over three alternatives. It set a responsibility boundary every managed "
            "policy file now depends on."
        ),
    },
    "ARCH-IAR-003": {
        "triggers": [
            "responsibility-or-dependency-direction",
            "cross-cutting-policy",
        ],
        "rationale": (
            "ADR-IAR-003 assigned review preflight, dashboard generation and candidate inspection to "
            "WORKFLOW.md, leaving routing and the evidence-versus-authority invariant in the router. "
            "It continues one modular boundary for every mandatory review instruction."
        ),
    },
    "ARCH-PMI-001": {
        "triggers": [
            "public-interface-or-protocol",
            "security-privacy-or-trust-boundary",
            "difficult-to-reverse",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-PMI-001 chose versioned canonical UTF-8 LF integrity in lock schema 2, over raw byte "
            "digests, enforced Git attributes and per-platform digests. It changed a cryptographic "
            "integrity contract whose migration runs one way only."
        ),
    },
    "ARCH-PYP-001": {
        "triggers": [
            "security-privacy-or-trust-boundary",
            "deployment-or-operating-model",
            "technology-framework-vendor-or-external-service",
            "difficult-to-reverse",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-PYP-001 chose manual promotion of exact GitHub release assets through OIDC trusted "
            "publishing, over three build-and-publish alternatives. It ties production distribution to "
            "an external index whose published filenames are immutable."
        ),
    },
    "ARCH-REV-001": {
        "triggers": [
            "public-interface-or-protocol",
            "data-ownership-or-persistence",
            "cross-cutting-policy",
            "difficult-to-reverse",
        ],
        "rationale": (
            "ADR-REV-001 added the verification record and release record artifact types, separating "
            "reusable contracts from records that bind one clean candidate commit to evidence. Every "
            "later governance commit reads that schema and provenance boundary."
        ),
    },
    "ARCH-VSP-001": {
        "triggers": [
            "public-interface-or-protocol",
            "data-ownership-or-persistence",
            "difficult-to-reverse",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-VSP-001 chose a terminal superseded state with one typed human-authorized successor, "
            "over five alternatives including deletion and automatic supersession. The lifecycle value "
            "and record edge preserve immutable provenance and cannot be walked back."
        ),
    },
    "ARCH-WLC-001": {
        "triggers": [
            "public-interface-or-protocol",
            "cross-cutting-policy",
            "material-alternatives",
        ],
        "rationale": (
            "ADR-WLC-001 chose implemented as the completed state for governance work no record covers, "
            "over a new completed value, per-work-order records and a derived warning only. It makes "
            "blocking policy of what every repository's lifecycle reading assumes."
        ),
    },
}

AMENDMENTS: dict[str, str] = {
    "ARCH-AGR-001": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-AGR-001`).** The legacy
relation named only `SPEC-AGR-001`, which becomes the conformance target;
`addresses` takes the eight requirements that specification specifies, all of
them active. The assessment reads the drivers and rejected options of
`ADR-AGR-001`, the one active ADR that decides this architecture. Title,
status, statement and ADR relations are unchanged.""",
    "ARCH-DST-001": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-DST-001`).** The six
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-DST-001`, the active specification that specifies them. The assessment
reads the decision and consequences of `ADR-DST-001`, the one active ADR that
decides this architecture. Title, status, statement and ADR relations are
unchanged.""",
    "ARCH-DST-002": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-DST-002`).** `REQ-DST-007`
becomes the addressed requirement and `conforms_to` names `SPEC-DST-002`, the
active specification that specifies it. `REQ-DST-008` is left out of
`addresses`: it is `superseded`, and an active architecture may not address an
inactive requirement. `SPEC-DST-002` still specifies it, so the historical
edge remains readable in the graph. The assessment reads the decision and
consequences of `ADR-DST-002`, the one active ADR that decides this
architecture. Title, status, statement and ADR relations are unchanged.""",
    "ARCH-DST-003": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-DST-003`).** The five
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-DST-003`, the active specification that specifies them. The assessment
reads the drivers and rejected options of `ADR-DST-003`, the one active ADR
that decides this architecture. Title, status, statement and ADR relations are
unchanged.""",
    "ARCH-DST-004": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-DST-004`).** The addressed
requirement becomes `REQ-DST-014` and `conforms_to` names `SPEC-DST-004`, the
active specification that specifies it. The assessment reads the drivers and
rejected options of `ADR-DST-004`, the one active ADR that decides this
architecture. Title, status, statement and ADR relations are unchanged.""",
    "ARCH-DST-005": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-DST-005`).** The four
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-DST-005`, the active specification that specifies them. The assessment
reads the drivers and rejected options of `ADR-DST-005`, the one active ADR
that decides this architecture. Title, status, statement and ADR relations are
unchanged.""",
    "ARCH-IAR-001": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-IAR-001`).** Eight of the
nine requirements of the legacy relation become `addresses`; `conforms_to`
names `SPEC-IAR-001`, the active specification that specifies them.
`REQ-IAR-005` is left out of `addresses`: it is `superseded`, and an active
architecture may not address an inactive requirement. `SPEC-IAR-001` still
specifies it, so the historical edge remains readable in the graph. The
assessment reads the rationale and seven rejected alternatives of
`ADR-IAR-001`, the one active ADR that decides this architecture. Title,
status, statement and ADR relations are unchanged.""",
    "ARCH-IAR-002": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-IAR-002`).** The addressed
requirement becomes `REQ-IAR-010` and `conforms_to` names `SPEC-IAR-002`, the
active specification that specifies it. The assessment reads the drivers and
four considered options of `ADR-IAR-002`, the one active ADR that decides this
architecture. Title, status, statement and ADR relations are unchanged.""",
    "ARCH-IAR-003": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-IAR-003`).** The addressed
requirement becomes `REQ-IAR-011` and `conforms_to` names `SPEC-IAR-003`, the
active specification that specifies it. The assessment reads the drivers and
decision of `ADR-IAR-003`, the one active ADR that decides this architecture;
that ADR records no enumerated alternatives, so no alternatives trigger is
claimed. Title, status, statement and ADR relations are unchanged.""",
    "ARCH-IAR-004": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation, amended 2026-09-08 under `WO-AUT-005`
(`SPEC-AUT-003`).** The addressed requirement becomes `REQ-IAR-012` and
`conforms_to` names `SPEC-IAR-004`, the active specification that specifies
it. This architecture already carried a `[decision_assessment]` before this
work order; it is unchanged. Title, status, statement and ADR relations are
unchanged.""",
    "ARCH-PMI-001": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-PMI-001`).** The legacy
relation named only `SPEC-PMI-001`, which becomes the conformance target;
`addresses` takes the seven requirements that specification specifies, all of
them active. The assessment reads the drivers and four considered options of
`ADR-PMI-001`, the one active ADR that decides this architecture. Title,
status, statement and ADR relations are unchanged.""",
    "ARCH-PYP-001": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-PYP-001`).** The five
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-PYP-001`, the active specification that specifies them. The assessment
reads the drivers and four considered options of `ADR-PYP-001`, the one active
ADR that decides this architecture. Title, status, statement and ADR relations
are unchanged.""",
    "ARCH-REV-001": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-REV-001`).** The eight
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-REV-001`, the active specification that specifies them. The assessment
reads the decision and consequences of `ADR-REV-001`, the one active ADR that
decides this architecture; that ADR records no enumerated alternatives, so no
alternatives trigger is claimed. Title, status, statement and ADR relations
are unchanged.""",
    "ARCH-VSP-001": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-VSP-001`).** The legacy
relation named only `SPEC-VSP-001`, which becomes the conformance target;
`addresses` takes the seven requirements that specification specifies, all of
them active. The assessment reads the drivers and six considered options of
`ADR-VSP-001`, the one active ADR that decides this architecture. Title,
status, statement and ADR relations are unchanged.""",
    "ARCH-WLC-001": """**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-WLC-001`).** The six
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-WLC-001`, the active specification that specifies them. The assessment
reads the rationale and four rejected alternatives of `ADR-WLC-001`, the one
active ADR that decides this architecture. Title, status, statement and ADR
relations are unchanged.""",
}

EXCLUDED = {"templates", "evidence", ".git", "target", "node_modules"}
CONSTRAINS_LINE = re.compile(r"^constrains = \[[^\]]*\]\n", re.MULTILINE)
UPDATED_LINE = re.compile(r'^updated = "\d{4}-\d{2}-\d{2}"$', re.MULTILINE)


class Refusal(Exception):
    """A post-condition of SPEC-AUT-003 or of the typed-relation rules failed."""


def read_artifacts(root: Path) -> dict[str, dict[str, object]]:
    catalog: dict[str, dict[str, object]] = {}
    for path in sorted((root / "docs" / "engineering").rglob("*.md")):
        if EXCLUDED & set(path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        if not text.startswith("+++"):
            continue
        closing = text.find("\n+++", 3)
        if closing < 0:
            continue
        metadata = tomllib.loads(text[4:closing])
        artifact_id = metadata.get("id")
        if isinstance(artifact_id, str):
            catalog[artifact_id] = {"path": path, "metadata": metadata}
    return catalog


def active(catalog: dict[str, dict[str, object]], artifact_id: str) -> bool:
    entry = catalog.get(artifact_id)
    return bool(entry) and entry["metadata"].get("status") in DEFINITION_AUTHORITY


def specifies(catalog: dict[str, dict[str, object]], specification_id: str) -> list[str]:
    entry = catalog.get(specification_id, {})
    relations = entry.get("metadata", {}).get("relations", {}) if entry else {}
    return list(relations.get("specifies") or [])


def plan_one(
    architecture_id: str,
    catalog: dict[str, dict[str, object]],
) -> dict[str, object]:
    metadata = catalog[architecture_id]["metadata"]
    legacy = sorted(set(metadata["relations"]["constrains"]))
    for target in legacy:
        kind = catalog.get(target, {}).get("metadata", {}).get("type")
        if kind not in {"requirement", "specification"}:
            raise Refusal(f"{architecture_id}: legacy target {target} has type {kind!r}")
    addresses = [t for t in legacy if catalog[t]["metadata"]["type"] == "requirement"]
    conforms_to = {t for t in legacy if catalog[t]["metadata"]["type"] == "specification"}
    omitted = list(OMITTED_ADDRESSES.get(architecture_id, ()))
    addresses = [t for t in addresses if t not in omitted]
    for requirement_id in addresses:
        for specification_id, entry in catalog.items():
            if entry["metadata"].get("type") != "specification":
                continue
            if requirement_id in specifies(catalog, specification_id) and active(catalog, specification_id):
                conforms_to.add(specification_id)
    if architecture_id in ADDRESSES_FROM_SPECIFICATIONS:
        if addresses:
            raise Refusal(f"{architecture_id}: derivation requested but addresses is not empty")
        derived = {r for s in conforms_to for r in specifies(catalog, s)}
        addresses = sorted(r for r in derived if active(catalog, r))
    conforms_to_final = sorted(conforms_to)

    if not addresses:
        raise Refusal(f"{architecture_id}: addresses would be empty")
    if not conforms_to_final:
        raise Refusal(f"{architecture_id}: conforms_to would be empty")
    for requirement_id in addresses:
        if not active(catalog, requirement_id):
            raise Refusal(f"{architecture_id}: addresses inactive requirement {requirement_id}")
    for specification_id in conforms_to_final:
        if not active(catalog, specification_id):
            raise Refusal(f"{architecture_id}: conforms to inactive specification {specification_id}")
    transitive = {r for s in conforms_to_final for r in specifies(catalog, s)}
    unspecified = sorted(set(addresses) - transitive)
    if unspecified:
        raise Refusal(f"{architecture_id}: addressed requirements without a conforming specification: {unspecified}")
    if architecture_id not in AMENDMENTS:
        raise Refusal(f"{architecture_id}: no amendment record is declared")
    has_assessment = metadata.get("decision_assessment") is not None
    if not has_assessment and architecture_id not in ASSESSMENTS:
        raise Refusal(f"{architecture_id}: no decision assessment is declared")
    return {
        "path": catalog[architecture_id]["path"].as_posix(),
        "legacy_constrains": legacy,
        "addresses": sorted(addresses),
        "conforms_to": conforms_to_final,
        "omitted_from_addresses": omitted,
        "addresses_derived_from_specification": architecture_id in ADDRESSES_FROM_SPECIFICATIONS,
        "assessment_added": not has_assessment,
        "triggers": list(ASSESSMENTS.get(architecture_id, {}).get("triggers", [])),
    }


def render_array(values: list[str]) -> str:
    return "[" + ", ".join(json.dumps(value) for value in values) + "]"


def rewrite_text(text: str, architecture_id: str, plan: dict[str, object]) -> str:
    closing = text.find("\n+++", 3)
    if closing < 0:
        raise Refusal(f"{architecture_id}: front matter is not closed")
    front, body = text[: closing + 1], text[closing + 1 :]
    typed = (
        f"addresses = {render_array(plan['addresses'])}\n"
        f"conforms_to = {render_array(plan['conforms_to'])}\n"
    )
    front, count = CONSTRAINS_LINE.subn(typed, front, count=1)
    if count != 1:
        raise Refusal(f"{architecture_id}: the constrains line was not found exactly once")
    front, count = UPDATED_LINE.subn(f'updated = "{AMENDED}"', front, count=1)
    if count != 1:
        raise Refusal(f"{architecture_id}: the updated line was not found exactly once")
    if plan["assessment_added"]:
        assessment = ASSESSMENTS[architecture_id]
        front = front.rstrip("\n") + "\n\n[decision_assessment]\n"
        front += 'outcome = "adr_required"\n'
        front += f"triggers = {render_array(list(assessment['triggers']))}\n"
        front += f"rationale = {json.dumps(assessment['rationale'])}\n"
        front += 'assessed_by = "technical-owner"\n'
    migrated = front + body
    if "## Amendment record" in migrated:
        raise Refusal(f"{architecture_id}: an amendment record section already exists")
    return migrated.rstrip("\n") + "\n\n## Amendment record\n\n" + AMENDMENTS[architecture_id] + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true", help="write the migrated files; default is a dry run")
    parser.add_argument("--report", type=Path, help="write the JSON plan to this path")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    catalog = read_artifacts(root)
    legacy_ids = sorted(
        artifact_id
        for artifact_id, entry in catalog.items()
        if entry["metadata"].get("type") == "architecture"
        and "constrains" in (entry["metadata"].get("relations") or {})
    )
    report: dict[str, object] = {
        "schema": "se-harness-architecture-relation-migration-v1",
        "work_order": WORK_ORDER,
        "applied": bool(args.apply),
        "architectures": {},
    }
    try:
        plans = {architecture_id: plan_one(architecture_id, catalog) for architecture_id in legacy_ids}
    except Refusal as refusal:
        print(f"refusing: {refusal}", file=sys.stderr)
        return 2
    for architecture_id, plan in plans.items():
        path = root / plan["path"]
        raw = path.read_bytes()
        newline = "\r\n" if b"\r\n" in raw else "\n"
        text = raw.decode("utf-8").replace("\r\n", "\n")
        try:
            migrated = rewrite_text(text, architecture_id, plan)
        except Refusal as refusal:
            print(f"refusing: {refusal}", file=sys.stderr)
            return 2
        if args.apply:
            path.write_bytes(migrated.replace("\n", newline).encode("utf-8"))
        report["architectures"][architecture_id] = plan
    report["counts"] = {
        "architectures": len(plans),
        "assessments_added": sum(1 for plan in plans.values() if plan["assessment_added"]),
        "addresses_derived": sum(1 for plan in plans.values() if plan["addresses_derived_from_specification"]),
        "omitted_addresses": sum(len(plan["omitted_from_addresses"]) for plan in plans.values()),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report is not None:
        # LF bytes: `.gitattributes` declares `docs/engineering/**/evidence/*.json`
        # as `text eol=lf`, and text mode would write CRLF on Windows.
        args.report.write_bytes(rendered.encode("utf-8"))
    else:
        print(rendered, end="")
    counts = report["counts"]
    print(
        f"{counts['architectures']} architectures, {counts['assessments_added']} assessments added, "
        f"{counts['addresses_derived']} derived address sets, {counts['omitted_addresses']} omitted targets",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
