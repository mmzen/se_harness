"""Resolve declared generation exemptions for architectures without a decision assessment.

`SPEC-DLC-001` replaces an inference from lifecycle status with an explicit
declaration. It defines one frozen closed self-hosting set, one declaration field
inside a work order's `[definition_generation]` packet, and one resolution from
either source to an accepted exemption. This module owns the package-side
implementation. The candidate validator script carries an equivalent
self-contained implementation because it must run inside a consumer repository
without importing this package; the two agree on a shared committed vector
fixture.

Resolution is a pure function of governed artifact content. It reads no lifecycle
status, no date, no lock, no installed evaluator identity, no environment value,
no command-line flag and no Git state, and it never writes, recomputes or
re-points any field. An architecture's status is deliberately not an input: rule
`DLC-GEN-005` removes that inference, and nothing here reintroduces it.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


DECLARATION_SCHEMA = "se-harness-definition-generation-v1"
DECLARATION_SCOPE = "architecture-decision-assessment"
DECLARATION_PACKET = "definition_generation"
DECLARATION_FIELD = "legacy_architectures_without_decision_assessment"
MAX_DECLARED_ARCHITECTURES = 512
SELF_HOSTING_DECLARER = "self-hosting-compatibility-set"

# Frozen self-hosting compatibility set. These are this repository's own
# architectures, authored before `decision_assessment` existed. SPEC-DLC-001 rule
# DLC-GEN-001 closes the set: no identifier is ever added to it, and every new
# exemption uses a declaration. The membership was measured, not asserted; the
# generating measurement and its comparison test stand behind it.
SELF_HOSTING_COMPATIBILITY_SET = frozenset(
    {
        "ARCH-AGR-001",
        "ARCH-DST-001",
        "ARCH-DST-002",
        "ARCH-DST-003",
        "ARCH-DST-004",
        "ARCH-DST-005",
        "ARCH-IAR-001",
        "ARCH-IAR-002",
        "ARCH-IAR-003",
        "ARCH-PMI-001",
        "ARCH-PYP-001",
        "ARCH-REV-001",
        "ARCH-VSP-001",
        "ARCH-WLC-001",
    }
)

ARCHITECTURE_PATTERN = re.compile(r"^ARCH-[A-Z][A-Z0-9-]*-\d{3}$")

REASON_DECLARATION_SHAPE = "declaration must be an array of strings"
REASON_DECLARATION_SIZE = f"declaration exceeds {MAX_DECLARED_ARCHITECTURES} entries"
REASON_NO_APPROVAL = "declaring work order has no draft-to-approved lifecycle event"
REASON_INVALID_ID = "invalid architecture identifier"
REASON_UNKNOWN_ARCHITECTURE = "no artifact has this identifier"
REASON_AMBIGUOUS_ARCHITECTURE = "more than one artifact has this identifier"
REASON_NOT_ARCHITECTURE = "declared artifact is not an architecture"
REASON_ALREADY_ASSESSED = "architecture already carries a decision_assessment"

MAX_ARTIFACT_BYTES = 256 * 1024
EXCLUDED_PARTS = {".git", "evidence", "node_modules", "target", "templates"}


class DefinitionGenerationError(ValueError):
    """The repository's architecture-generation state cannot be assessed."""


@dataclass(frozen=True)
class GenerationDefect:
    """One declaration member that does not resolve to an accepted exemption."""

    work_order: str
    architecture: str | None
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "work_order": self.work_order,
            "architecture": self.architecture,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class GenerationResolution:
    """Accepted exemptions, declaration defects, and architectures left enforcing."""

    exemptions: Mapping[str, str]
    defects: tuple[GenerationDefect, ...]
    enforced: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "exemptions": dict(sorted(self.exemptions.items())),
            "defects": [defect.as_dict() for defect in self.defects],
            "enforced": list(self.enforced),
        }

    def source(self, architecture: str) -> str | None:
        """Return the declarer that exempts `architecture`, or None when enforcing."""

        return self.exemptions.get(architecture)


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


UNDECLARED = object()


def _declaration(work_order: Mapping[str, Any]) -> Any:
    """Return the raw declaration value of an authoritative packet, or `UNDECLARED`."""

    packet = work_order.get(DECLARATION_PACKET)
    if not isinstance(packet, dict):
        return UNDECLARED
    if (
        packet.get("schema") != DECLARATION_SCHEMA
        or packet.get("scope") != DECLARATION_SCOPE
    ):
        return UNDECLARED
    if DECLARATION_FIELD not in packet:
        return UNDECLARED
    return packet[DECLARATION_FIELD]


def resolve(
    artifacts: Iterable[Mapping[str, Any]],
    work_orders: Iterable[Mapping[str, Any]],
) -> GenerationResolution:
    """Resolve declarations against architectures, per `SPEC-DLC-001` DLC-GEN-001..008.

    `artifacts` are normalized views with `id`, `type` and `assessed`, covering every
    artifact in the graph so that an unknown identifier is distinguishable from one
    naming a non-architecture. `work_orders` are normalized views with `id`,
    `approved` and the raw declaration packet. Both are untrusted repository content;
    every field is validated before use.

    A declared identifier resolves only through the approval precondition
    (`DLC-GEN-003`) and the target tests (`DLC-GEN-004`). No lifecycle status of any
    architecture is consulted at any point.
    """

    by_id: dict[str, list[Mapping[str, Any]]] = {}
    for artifact in artifacts:
        identifier = _text(artifact.get("id"))
        if identifier is not None:
            by_id.setdefault(identifier, []).append(artifact)

    exemptions: dict[str, str] = {}
    defects: list[GenerationDefect] = []

    for work_order in sorted(work_orders, key=lambda item: str(item.get("id", ""))):
        identifier = _text(work_order.get("id"))
        if identifier is None:
            continue
        declaration = _declaration(work_order)
        if declaration is UNDECLARED:
            continue
        if not isinstance(declaration, list) or not all(
            isinstance(member, str) for member in declaration
        ):
            defects.append(GenerationDefect(identifier, None, REASON_DECLARATION_SHAPE))
            continue
        if len(declaration) > MAX_DECLARED_ARCHITECTURES:
            defects.append(GenerationDefect(identifier, None, REASON_DECLARATION_SIZE))
            continue
        if not declaration:
            continue
        if not work_order.get("approved"):
            # DLC-GEN-003: a declaration in a work order with no recorded
            # draft-to-approved event resolves nothing, and that is a defect.
            defects.append(GenerationDefect(identifier, None, REASON_NO_APPROVAL))
            continue
        for member in sorted(set(declaration)):
            reason = _member_defect(member, by_id)
            if reason is not None:
                defects.append(GenerationDefect(identifier, member, reason))
                continue
            exemptions.setdefault(member, identifier)

    for identifier in sorted(SELF_HOSTING_COMPATIBILITY_SET):
        matches = by_id.get(identifier, ())
        if len(matches) == 1 and _unassessed_architecture(matches[0]):
            exemptions.setdefault(identifier, SELF_HOSTING_DECLARER)

    enforced = sorted(
        identifier
        for identifier, matches in by_id.items()
        if identifier not in exemptions
        and len(matches) == 1
        and _unassessed_architecture(matches[0])
    )
    return GenerationResolution(
        exemptions=dict(sorted(exemptions.items())),
        defects=tuple(
            sorted(
                defects,
                key=lambda item: (item.work_order, item.architecture or "", item.reason),
            )
        ),
        enforced=tuple(enforced),
    )


def _unassessed_architecture(artifact: Mapping[str, Any]) -> bool:
    return artifact.get("type") == "architecture" and not artifact.get("assessed")


def _member_defect(
    member: str,
    by_id: Mapping[str, Sequence[Mapping[str, Any]]],
) -> str | None:
    """Return why a declared member does not resolve, or None when it does."""

    if ARCHITECTURE_PATTERN.fullmatch(member) is None:
        return REASON_INVALID_ID
    matches = by_id.get(member, ())
    if not matches:
        return REASON_UNKNOWN_ARCHITECTURE
    if len(matches) > 1:
        return REASON_AMBIGUOUS_ARCHITECTURE
    artifact = matches[0]
    if artifact.get("type") != "architecture":
        return REASON_NOT_ARCHITECTURE
    if artifact.get("assessed"):
        # DLC-GEN-007: a stale declaration, naming an architecture that has since
        # gained an assessment, is reported and does not resolve.
        return REASON_ALREADY_ASSESSED
    return None


def _front_matter(path: Path) -> dict[str, Any] | None:
    try:
        if path.is_symlink():
            raise DefinitionGenerationError(f"artifact path is a symlink: {path.name}")
        if path.stat().st_size > MAX_ARTIFACT_BYTES:
            raise DefinitionGenerationError(f"artifact exceeds the size bound: {path.name}")
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except DefinitionGenerationError:
        raise
    except (OSError, UnicodeError) as exc:
        raise DefinitionGenerationError(f"cannot read artifact {path.name}: {exc}") from exc
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
        raise DefinitionGenerationError(f"invalid front matter in {path.name}: {exc}") from exc
    return value if isinstance(value, dict) else None


def _approved(metadata: Mapping[str, Any]) -> bool:
    """Return whether a recorded draft-to-approved lifecycle event is present."""

    events = metadata.get("lifecycle_events")
    if not isinstance(events, list):
        return False
    return any(
        isinstance(event, dict) and event.get("from") == "draft" and event.get("to") == "approved"
        for event in events
    )


def _views(repository: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    artifacts: list[dict[str, Any]] = []
    work_orders: list[dict[str, Any]] = []
    artifact_root = repository / "docs" / "engineering"
    if not artifact_root.is_dir():
        return artifacts, work_orders
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
        artifacts.append(
            {
                "id": identifier,
                "type": metadata.get("type"),
                "assessed": metadata.get("decision_assessment") is not None,
            }
        )
        if metadata.get("type") == "work_order":
            work_orders.append(
                {
                    "id": identifier,
                    "approved": _approved(metadata),
                    DECLARATION_PACKET: metadata.get(DECLARATION_PACKET),
                }
            )
    return artifacts, work_orders


def resolve_repository(repository: Path) -> GenerationResolution:
    """Resolve declarations from a repository's governed artifacts.

    Raises `DefinitionGenerationError` when an artifact cannot be read or parsed, so
    an unassessable tree fails closed rather than reading as an absence of
    architectures.
    """

    artifacts, work_orders = _views(repository)
    return resolve(artifacts, work_orders)


def enforcing_architectures(repository: Path) -> tuple[str, ...]:
    """Return architectures with no assessment and no accepted exemption."""

    return resolve_repository(repository).enforced
