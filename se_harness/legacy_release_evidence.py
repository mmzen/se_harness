"""Resolve declared exemptions for releases that predate evaluator evidence.

`SPEC-LRE-001` defines one declaration, `legacy_releases_without_evaluator_evidence`
inside a work order's `[evaluator_upgrade]` packet, and one resolution from it to an
accepted exemption. This module owns the package-side implementation. The candidate
validator script carries an equivalent self-contained implementation because it must
run inside a consumer repository without importing this package; the two agree on a
shared committed vector fixture.

Resolution is a pure function of governed artifact content. It reads no lock, no
installed evaluator identity, no environment value and no command-line flag, and it
never writes, recomputes or repoints any record field.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from se_harness.workflow_contract import load_lifecycle_registry


UPGRADE_AUTHORIZATION_SCHEMA = "se-harness-evaluator-upgrade-v1"
UPGRADE_AUTHORIZATION_SCOPE = "standard-root-only"
DECLARATION_FIELD = "legacy_releases_without_evaluator_evidence"
MAX_DECLARED_RECORDS = 512
SELF_HOSTING_DECLARER = "self-hosting-compatibility-set"

# Frozen self-hosting compatibility set. These are this repository's own releases,
# cut before evaluator-evidence enforcement existed. SPEC-LRE-001 rule 11 closes the
# set: no identifier is ever added to it, and every new exemption uses a declaration.
SELF_HOSTING_COMPATIBILITY_SET = frozenset(
    {"RLS-SEH-001", "RLS-SEH-002", "RLS-SEH-004", "RLS-SEH-005", "RLS-SEH-006", "RLS-SEH-007"}
)

RELEASE_RECORD_PATTERN = re.compile(r"^RLS-[A-Z][A-Z0-9-]*-\d{3}$")
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

REASON_DECLARATION_SHAPE = "declaration must be an array of strings"
REASON_DECLARATION_SIZE = f"declaration exceeds {MAX_DECLARED_RECORDS} entries"
REASON_NO_APPROVAL = "declaring work order has no draft-to-approved lifecycle event"
REASON_INVALID_ID = "invalid release record identifier"
REASON_UNKNOWN_RECORD = "no release record has this identifier"
REASON_AMBIGUOUS_RECORD = "more than one release record has this identifier"
REASON_NOT_RELEASED = "release record status is not released"
REASON_ALREADY_BOUND = "release record already carries evaluator evidence"
REASON_NO_RELEASED_AT = "release record has no valid released_at timestamp"
REASON_NOT_YET_RELEASED = "release record was released after the declaring work order was approved"

MAX_ARTIFACT_BYTES = 256 * 1024
EXCLUDED_PARTS = {".git", "evidence", "node_modules", "target", "templates"}

_LIFECYCLE_REGISTRY = load_lifecycle_registry()


def authority_granting_work_order_statuses() -> frozenset[str]:
    """Return the work-order states the managed lifecycle marks as granting authority."""

    return frozenset(
        state for state, row in _LIFECYCLE_REGISTRY["work_order"].items() if row.grants_authority
    )


class LegacyReleaseEvidenceError(ValueError):
    """The repository's legacy release-evidence state cannot be assessed."""


@dataclass(frozen=True)
class LegacyEvidenceDefect:
    """One declaration member that does not resolve to an accepted exemption."""

    work_order: str
    record: str | None
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {"work_order": self.work_order, "record": self.record, "reason": self.reason}


@dataclass(frozen=True)
class LegacyEvidenceResolution:
    """Accepted exemptions, declaration defects, and records left enforcing."""

    exemptions: Mapping[str, str]
    defects: tuple[LegacyEvidenceDefect, ...]
    undeclared: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "exemptions": dict(sorted(self.exemptions.items())),
            "defects": [defect.as_dict() for defect in self.defects],
            "undeclared": list(self.undeclared),
        }


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _released_unbound(record: Mapping[str, Any]) -> bool:
    return (
        record.get("status") == "released"
        and not record.get("path_present")
        and not record.get("digest_present")
    )


UNDECLARED = object()


def _declaration(work_order: Mapping[str, Any]) -> Any:
    """Return the raw declaration value of an authoritative packet, or `UNDECLARED`."""

    packet = work_order.get("evaluator_upgrade")
    if not isinstance(packet, dict):
        return UNDECLARED
    if (
        packet.get("schema") != UPGRADE_AUTHORIZATION_SCHEMA
        or packet.get("scope") != UPGRADE_AUTHORIZATION_SCOPE
    ):
        return UNDECLARED
    if DECLARATION_FIELD not in packet:
        return UNDECLARED
    return packet[DECLARATION_FIELD]


def resolve(
    records: Iterable[Mapping[str, Any]],
    work_orders: Iterable[Mapping[str, Any]],
) -> LegacyEvidenceResolution:
    """Resolve declarations against release records, per `SPEC-LRE-001` rules 1-11.

    `records` are normalized release-record views with `id`, `status`, `released_at`,
    `path_present` and `digest_present`. `work_orders` are normalized work-order views
    with `id`, `status`, `approved_at` and the raw `evaluator_upgrade` table. Both are
    untrusted repository content; every field is validated before use.
    """

    authoritative = authority_granting_work_order_statuses()

    by_id: dict[str, list[Mapping[str, Any]]] = {}
    for record in records:
        identifier = _text(record.get("id"))
        if identifier is not None:
            by_id.setdefault(identifier, []).append(record)

    exemptions: dict[str, str] = {}
    defects: list[LegacyEvidenceDefect] = []

    for work_order in sorted(work_orders, key=lambda item: str(item.get("id", ""))):
        identifier = _text(work_order.get("id"))
        if identifier is None or work_order.get("status") not in authoritative:
            # Rule 3: a work order whose status does not grant authority declares
            # nothing, and its declaration is neither honoured nor reported.
            continue
        declaration = _declaration(work_order)
        if declaration is UNDECLARED:
            continue
        if not isinstance(declaration, list) or not all(
            isinstance(member, str) for member in declaration
        ):
            defects.append(LegacyEvidenceDefect(identifier, None, REASON_DECLARATION_SHAPE))
            continue
        if len(declaration) > MAX_DECLARED_RECORDS:
            defects.append(LegacyEvidenceDefect(identifier, None, REASON_DECLARATION_SIZE))
            continue
        if not declaration:
            continue
        approved_at = _text(work_order.get("approved_at"))
        if approved_at is None or TIMESTAMP_PATTERN.fullmatch(approved_at) is None:
            # Rule 4: an undated declarer declares nothing, and that is a defect.
            defects.append(LegacyEvidenceDefect(identifier, None, REASON_NO_APPROVAL))
            continue
        for member in sorted(set(declaration)):
            reason = _member_defect(member, approved_at, by_id)
            if reason is not None:
                defects.append(LegacyEvidenceDefect(identifier, member, reason))
                continue
            exemptions.setdefault(member, identifier)

    for identifier in sorted(SELF_HOSTING_COMPATIBILITY_SET):
        matches = by_id.get(identifier, ())
        if len(matches) == 1 and _released_unbound(matches[0]):
            exemptions.setdefault(identifier, SELF_HOSTING_DECLARER)

    undeclared = sorted(
        identifier
        for identifier, matches in by_id.items()
        if identifier not in exemptions
        and len(matches) == 1
        and _released_unbound(matches[0])
    )
    return LegacyEvidenceResolution(
        exemptions=dict(sorted(exemptions.items())),
        defects=tuple(
            sorted(defects, key=lambda item: (item.work_order, item.record or "", item.reason))
        ),
        undeclared=tuple(undeclared),
    )


def _member_defect(
    member: str,
    approved_at: str,
    by_id: Mapping[str, Sequence[Mapping[str, Any]]],
) -> str | None:
    """Return why a declared member does not resolve, or None when it does."""

    if RELEASE_RECORD_PATTERN.fullmatch(member) is None:
        return REASON_INVALID_ID
    matches = by_id.get(member, ())
    if not matches:
        return REASON_UNKNOWN_RECORD
    if len(matches) > 1:
        return REASON_AMBIGUOUS_RECORD
    record = matches[0]
    if record.get("status") != "released":
        return REASON_NOT_RELEASED
    if record.get("path_present") or record.get("digest_present"):
        # Rule 7: a partially bound record is never exempt.
        return REASON_ALREADY_BOUND
    released_at = _text(record.get("released_at"))
    if released_at is None or TIMESTAMP_PATTERN.fullmatch(released_at) is None:
        return REASON_NO_RELEASED_AT
    if not released_at < approved_at:
        # Rule 5: strictly after, so a declaration can never reach a future release.
        return REASON_NOT_YET_RELEASED
    return None


def _front_matter(path: Path) -> dict[str, Any] | None:
    try:
        if path.is_symlink():
            raise LegacyReleaseEvidenceError(f"artifact path is a symlink: {path.name}")
        if path.stat().st_size > MAX_ARTIFACT_BYTES:
            raise LegacyReleaseEvidenceError(f"artifact exceeds the size bound: {path.name}")
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except LegacyReleaseEvidenceError:
        raise
    except (OSError, UnicodeError) as exc:
        raise LegacyReleaseEvidenceError(f"cannot read artifact {path.name}: {exc}") from exc
    if not lines or lines[0].strip() != "+++":
        return None
    try:
        closing = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "+++"
        )
        value = tomllib.loads("\n".join(lines[1:closing]))
    except StopIteration:
        return None
    except tomllib.TOMLDecodeError as exc:
        raise LegacyReleaseEvidenceError(f"invalid front matter in {path.name}: {exc}") from exc
    return value if isinstance(value, dict) else None


def _approved_at(metadata: Mapping[str, Any]) -> str | None:
    """Return the last draft-to-approved decision instant, or None."""

    events = metadata.get("lifecycle_events")
    if not isinstance(events, list):
        return None
    latest: str | None = None
    for event in events:
        if not isinstance(event, dict) or event.get("from") != "draft" or event.get("to") != "approved":
            continue
        decided_at = _text(event.get("decided_at"))
        if decided_at is not None and (latest is None or decided_at > latest):
            latest = decided_at
    return latest


def _views(repository: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    work_orders: list[dict[str, Any]] = []
    artifact_root = repository / "docs" / "engineering"
    if not artifact_root.is_dir():
        return records, work_orders
    for path in sorted(artifact_root.rglob("*.md"), key=lambda item: item.as_posix()):
        relative = path.relative_to(artifact_root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        metadata = _front_matter(path)
        if metadata is None:
            continue
        identifier = _text(metadata.get("id"))
        if identifier is None:
            continue
        if metadata.get("type") == "release_record":
            records.append(
                {
                    "id": identifier,
                    "status": metadata.get("status"),
                    "released_at": metadata.get("released_at"),
                    "path_present": metadata.get("evaluator_evidence_path") is not None,
                    "digest_present": metadata.get("evaluator_evidence_sha256") is not None,
                }
            )
        elif metadata.get("type") == "work_order":
            work_orders.append(
                {
                    "id": identifier,
                    "status": metadata.get("status"),
                    "approved_at": _approved_at(metadata),
                    "evaluator_upgrade": metadata.get("evaluator_upgrade"),
                }
            )
    return records, work_orders


def resolve_repository(repository: Path) -> LegacyEvidenceResolution:
    """Resolve declarations from a repository's governed artifacts.

    Raises `LegacyReleaseEvidenceError` when an artifact cannot be read or parsed, so
    an unassessable tree fails closed rather than reading as an absence of records.
    """

    records, work_orders = _views(repository)
    return resolve(records, work_orders)


def undeclared_legacy_releases(repository: Path) -> tuple[str, ...]:
    """Return released records with no evaluator-evidence binding and no exemption."""

    return resolve_repository(repository).undeclared
