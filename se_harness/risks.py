"""The risk artifact: one measured threat, raised for an answer (SPEC-RSK-010).

A risk (`RISK-`) records one cause, one effect, the stage it threatens and a
five-by-five measurement (RSK-MGT-002 to RSK-MGT-006). `raise-risk` computes
the score, writes the file and raises it in one act (RSK-MGT-009); with
`--with-decision` it writes the paired decision beside it (RSK-MGT-015). A
raised risk stops nothing by itself: the decision that names it in `concerns`
blocks the artifacts the risk threatens, and the decision family's own stop
holds them (RSK-MGT-012 to RSK-MGT-014). Disposing that decision moves the
risk in the same journalled act and copies the answer onto it (RSK-MGT-016 to
RSK-MGT-020). The dependency runs one way: this module reads decisions, and
`decisions.py` never reads risks (ARCH-RSK-010).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from se_harness import mutation_guard
from se_harness.artifact_layout import (
    DOMAIN_PATTERN,
    ID_PATTERN,
    REF_ARTIFACT_PATTERN,
    AuthoringChange,
    _atomic_create,
    _existing_artifact_path,
    _rollback_directories,
    _validate_existing_chain,
    allocate_artifact_id,
    canonical_artifact_relative_path,
    reachable_artifact_ids,
    validate_artifact_id,
    validate_domain,
)
from se_harness.decisions import declared_options
from se_harness.installer import HarnessError, ensure_target
from se_harness.codes import E001, E003

#: SPEC-DCM-001 rule 4: the six types a decision may block. The validator enforces the
#: set (`E011`); `raise-risk` reads it first so a threatened record is refused with the
#: reason, before any file is written.
BLOCKABLE_TYPES = frozenset({"requirement", "specification", "verification", "architecture", "adr", "work_order"})

#: RSK-MGT-004 and RSK-MGT-005: the closed stage and category sets.
RISK_STAGES = ("definition", "architecture", "implementation", "verification", "release", "operation")
RISK_CATEGORIES = ("safety", "security", "compliance", "process", "schedule", "quality")
#: RSK-MGT-003: each measurement is an integer from 1 to 5; the score is their product.
MEASUREMENT = range(1, 6)
#: RSK-MGT-015: the three answers a paired decision declares, and RSK-MGT-016: the
#: risk state each one names.
RISK_OPTIONS = (
    ("accept", "Accept the threat; record a residual and a revisit trigger."),
    ("avoid", "Avoid the threat by a design change recorded in an ADR or a decision."),
    ("mitigate", "Mitigate the threat through a work order; the risk closes under verified coverage."),
)
OPTION_TARGETS = {"accept": "accepted", "avoid": "avoided", "mitigate": "mitigating"}
WITHDRAWN_LABEL = "Withdrawn with the decision that concerned it."
PENDING = frozenset({"open", "deferred"})
_TOKEN = re.compile(r"^[A-Z][A-Z0-9]*$")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
_SENTENCE_BREAK = re.compile(r"[.!?]\s+\S")


@dataclass(frozen=True)
class RaiseResult:
    risk_id: str
    decision_id: str | None
    score: int
    changes: tuple[AuthoringChange, ...] = field(default_factory=tuple)


def compute_score(likelihood: object, impact: object) -> int:
    """RSK-MGT-003: the product of two integers from 1 to 5."""

    for name, value in (("likelihood", likelihood), ("impact", impact)):
        if type(value) is not int or value not in MEASUREMENT:
            raise HarnessError(f"{name} must be an integer from 1 to 5, not {value!r}")
    return int(likelihood) * int(impact)  # type: ignore[call-overload]


def _text(value: object, label: str, *, limit: int = 2000, one_sentence: bool = False) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HarnessError(f"{label} must be non-empty text")
    text = value.strip()
    if len(text) > limit or _CONTROL.search(text):
        raise HarnessError(f"{label} must be single-line text of at most {limit} characters")
    if one_sentence and _SENTENCE_BREAK.search(text):
        raise HarnessError(f"{label} must be one sentence")
    return text


def _toml(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(json.dumps(item) for item in value) + "]"
    return json.dumps(str(value))


def _domain_tokens(root: Path) -> dict[str, set[str]]:
    engineering = root / "docs" / "engineering"
    tokens: dict[str, set[str]] = {}
    if not engineering.is_dir():
        return tokens
    for directory in sorted(engineering.iterdir()):
        if not directory.is_dir():
            continue
        try:
            domain = validate_domain(directory.name)
        except HarnessError:
            continue
        found = {match.group(2) for match in map(REF_ARTIFACT_PATTERN.match, (path.name for path in directory.rglob("*.md"))) if match}
        if found:
            tokens[domain] = found
    return tokens


def resolve_domain(root: Path, value: object) -> str:
    """The domain slug, given the slug or the identifier token of exactly one domain."""

    if isinstance(value, str) and DOMAIN_PATTERN.fullmatch(value):
        return validate_domain(value)
    if isinstance(value, str) and _TOKEN.fullmatch(value):
        matches = sorted(domain for domain, tokens in _domain_tokens(root).items() if value in tokens)
        if len(matches) == 1:
            return matches[0]
        if not matches:
            raise HarnessError(f"no engineering domain carries the identifier token {value}; pass the domain slug")
        raise HarnessError(f"the identifier token {value} is used by {', '.join(matches)}; pass the domain slug")
    raise HarnessError("domain must be a domain slug (lowercase letters, numbers, hyphens) or the identifier token of one domain")


def _relation(artifact: Any, name: str) -> list[str]:
    relations = artifact.relations if isinstance(getattr(artifact, "relations", None), Mapping) else {}
    values = relations.get(name, [])
    return [item for item in values if isinstance(item, str)] if isinstance(values, list) else []


def paired_decisions(catalog: Mapping[str, Any], risk_id: str) -> list[Any]:
    """RSK-MGT-012: the pending decisions that name the risk in `concerns`."""

    return sorted(
        (
            item for item in catalog.values()
            if getattr(item, "artifact_type", None) == "decision" and item.status in PENDING and risk_id in _relation(item, "concerns")
        ),
        key=lambda item: item.artifact_id,
    )


def raised_risks_of(catalog: Mapping[str, Any], decision: Any) -> list[Any]:
    """The raised risks a decision concerns; disposing it moves each one (RSK-MGT-016)."""

    return sorted(
        (
            catalog[item] for item in _relation(decision, "concerns")
            if item in catalog and getattr(catalog[item], "artifact_type", None) == "risk" and catalog[item].status == "raised"
        ),
        key=lambda item: item.artifact_id,
    )


def _owners_of(catalog: Mapping[str, Any], artifact_ids: Iterable[str]) -> list[str]:
    roles: set[str] = set()
    for artifact_id in artifact_ids:
        target = catalog.get(artifact_id)
        if target is None:
            continue
        owners = target.metadata.get("owners") if isinstance(target.metadata, Mapping) else None
        if isinstance(owners, list):
            roles.update(item for item in owners if isinstance(item, str) and item.strip())
        if target.artifact_type == "work_order":
            roles.add("engineering-owner")
    return sorted(roles)


def _free_identifier(root: Path, artifact_id: str, artifact_type: str) -> str:
    """RSK-MGT-010: an explicit identifier declared anywhere, on any local ref, is refused."""

    selected = validate_artifact_id(artifact_id, artifact_type)
    existing = _existing_artifact_path(root, selected)
    if existing is not None:
        raise HarnessError(f"artifact ID already exists: {selected} at {existing.relative_to(root).as_posix()}")
    if (root / ".git").exists():
        try:
            on_refs = sorted(reachable_artifact_ids(root).get(selected, set()) - {"worktree"})
        except HarnessError:
            on_refs = []
        if on_refs:
            raise HarnessError(f"artifact ID already exists: {selected} on local ref {on_refs[0]}")
    return selected


def _render_risk(
    *,
    risk_id: str,
    title: str,
    owners: list[str],
    today: str,
    now: str,
    stage: str,
    category: str,
    cause: str,
    effect: str,
    likelihood: int,
    impact: int,
    score: int,
    raised_by: str,
    threatens: list[str],
) -> bytes:
    front = [
        "+++",
        f"id = {_toml(risk_id)}",
        'type = "risk"',
        f"title = {_toml(title)}",
        'status = "raised"',
        f"owners = {_toml(owners)}",
        f"created = {_toml(today)}",
        f"updated = {_toml(today)}",
        f"stage = {_toml(stage)}",
        f"category = {_toml(category)}",
        f"cause = {_toml(cause)}",
        f"effect = {_toml(effect)}",
        f"likelihood = {likelihood}",
        f"impact = {impact}",
        f"score = {score}",
        f"raised_by = {_toml(raised_by)}",
        'residual = ""',
        "",
        "[relations]",
        f"threatens = {_toml(threatens)}",
        "",
        "[[lifecycle_events]]",
        'from = "identified"',
        'to = "raised"',
        f"decided_at = {_toml(now)}",
        f"decided_by = {_toml(raised_by)}",
        f"reason = {_toml(f'Recorded by harnessctl raise-risk; the score is likelihood {likelihood} times impact {impact}.')}",
        "+++",
        "",
        f"# Risk: {title}",
        "",
        "## Threat",
        "",
        f"- Cause: {cause}",
        f"- Effect: {effect}",
        "",
        "## Measurement",
        "",
        f"Likelihood {likelihood} of 5 and impact {impact} of 5: score {score} of 25, on the",
        "five-by-five scale.",
        "",
        "## Answer",
        "",
        "Written by `harnessctl decide` on the decision that names this risk in",
        "`concerns`; the disposition table repeats the option, the role, the time and",
        "the verbatim reason. Do not edit it by hand.",
        "",
    ]
    return "\n".join(front).encode("utf-8")


def _render_decision(
    *,
    decision_id: str,
    risk_id: str,
    title: str,
    owners: list[str],
    today: str,
    score: int,
    raised_by: str,
    recommendation: str,
    threatens: list[str],
) -> bytes:
    question = f"How is the threat '{title}' (score {score}) answered: accept, avoid or mitigate?"
    front = [
        "+++",
        f"id = {_toml(decision_id)}",
        'type = "decision"',
        f"title = {_toml(f'Answer to the threat {title}')}",
        'status = "open"',
        f"owners = {_toml(owners)}",
        f"created = {_toml(today)}",
        f"updated = {_toml(today)}",
        'kind = "question"',
        f"question = {_toml(question)}",
        f"raised_by = {_toml(raised_by)}",
        f"recommendation = {_toml(recommendation)}",
        "",
    ]
    for option_id, label in RISK_OPTIONS:
        front.extend(["[[options]]", f"id = {_toml(option_id)}", f"label = {_toml(label)}", ""])
    front.extend([
        "[relations]",
        f"concerns = {_toml([risk_id, *threatens])}",
        f"blocks = {_toml(threatens)}",
        "+++",
        "",
        f"# Decision: Answer to the threat {title}",
        "",
        "## Question",
        "",
        f"{question} The measurement and the threatened artifacts are on {risk_id}.",
        "",
        "## Options",
        "",
    ])
    for option_id, label in RISK_OPTIONS:
        front.append(f"- `{option_id}`: {label}")
    front.extend([
        "",
        "## Recommendation",
        "",
        f"The raiser recommends `{recommendation}`.",
        "",
        "## Disposition",
        "",
        "Written by `harnessctl decide`; do not edit by hand. Disposing this decision",
        f"moves {risk_id} to the state the chosen option names, in the same act.",
        "",
    ])
    return "\n".join(front).encode("utf-8")


def raise_risk(
    repository: Path,
    *,
    domain: str,
    title: str,
    stage: str,
    category: str,
    cause: str,
    effect: str,
    likelihood: object,
    impact: object,
    threatens: Iterable[str],
    raised_by: str,
    owners: Iterable[str] = (),
    artifact_id: str | None = None,
    with_decision: bool = False,
    decision_id: str | None = None,
    recommendation: str = "mitigate",
    dry_run: bool = False,
) -> RaiseResult:
    """RSK-MGT-009: compute the score, write the risk and raise it in one act.

    With `with_decision` the paired decision is written beside it (RSK-MGT-015).
    Every refusal happens before any file is written (RSK-MGT-010); the raise
    needs no decision right and reads no configuration key (RSK-MGT-011).
    """

    from se_harness.repository_graph import artifact_catalog, validated_repository

    root = ensure_target(repository, must_exist=True)
    selected_domain = resolve_domain(root, domain)
    selected_title = _text(title, "title", limit=128)
    if stage not in RISK_STAGES:
        raise HarnessError(f"stage must be one of {', '.join(RISK_STAGES)}, not {stage!r}")
    if category not in RISK_CATEGORIES:
        raise HarnessError(f"category must be one of {', '.join(RISK_CATEGORIES)}, not {category!r}")
    selected_cause = _text(cause, "cause", one_sentence=True)
    selected_effect = _text(effect, "effect", one_sentence=True)
    selected_raiser = _text(raised_by, "raised-by", limit=128)
    if recommendation not in OPTION_TARGETS:
        raise HarnessError(f"recommend must be one of {', '.join(OPTION_TARGETS)}, not {recommendation!r}")
    score = compute_score(likelihood, impact)
    threatened: list[str] = []
    for item in threatens:
        if not isinstance(item, str) or ID_PATTERN.fullmatch(item.strip()) is None:
            raise HarnessError(f"threatens must name artifact identifiers, not {item!r}")
        if item.strip() not in threatened:
            threatened.append(item.strip())
    if not threatened:
        raise HarnessError("a risk threatens at least one artifact; pass --threatens")

    _, report = validated_repository(root)
    if any(item.code in {E001, E003} for item in report.errors):
        first = next(item for item in report.errors if item.code in {E001, E003})
        raise HarnessError(f"the artifact graph cannot be read [{first.code}]: {first.message}")
    catalog = artifact_catalog(report)
    for item in threatened:
        target = catalog.get(item)
        if target is None:
            raise HarnessError(f"threatened artifact {item} is unknown")
        if with_decision and target.artifact_type not in BLOCKABLE_TYPES:
            raise HarnessError(
                f"a decision cannot block the {target.artifact_type} {item}; threaten the work order it covers, or raise without --with-decision"
            )
    selected_owners = [item.strip() for item in owners if isinstance(item, str) and item.strip()]
    if not selected_owners:
        selected_owners = _owners_of(catalog, threatened)
    if not selected_owners:
        raise HarnessError("the threatened artifacts name no owner; pass --owner")

    allocated: str | None = None
    allocation_refs: tuple[str, ...] = ()
    if artifact_id is None:
        allocated, allocation_refs = allocate_artifact_id(root, domain=selected_domain, artifact_type="risk")
        risk_id = allocated
    else:
        risk_id = _free_identifier(root, artifact_id, "risk")
    risk_relative = canonical_artifact_relative_path(selected_domain, "risk", risk_id)
    risk_path = _validate_existing_chain(root, risk_relative, final_kind="file")
    if risk_path.exists():
        raise HarnessError(f"artifact destination already exists: {risk_relative.as_posix()}")
    changes = [AuthoringChange("create", risk_relative.as_posix(), allocated, allocation_refs)]

    paired_id: str | None = None
    decision_path: Path | None = None
    if with_decision:
        if decision_id is None:
            paired_id, _ = allocate_artifact_id(root, domain=selected_domain, artifact_type="decision")
        else:
            paired_id = _free_identifier(root, decision_id, "decision")
        decision_relative = canonical_artifact_relative_path(selected_domain, "decision", paired_id)
        decision_path = _validate_existing_chain(root, decision_relative, final_kind="file")
        if decision_path.exists():
            raise HarnessError(f"artifact destination already exists: {decision_relative.as_posix()}")
        changes.append(AuthoringChange("create", decision_relative.as_posix()))
    elif decision_id is not None:
        raise HarnessError("--decision-id applies only with --with-decision")

    stamp = datetime.now(UTC)
    now = stamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    today = now[:10]
    risk_bytes = _render_risk(
        risk_id=risk_id, title=selected_title, owners=selected_owners, today=today, now=now, stage=stage,
        category=category, cause=selected_cause, effect=selected_effect, likelihood=int(likelihood),  # type: ignore[call-overload]
        impact=int(impact), score=score, raised_by=selected_raiser, threatens=threatened,  # type: ignore[call-overload]
    )
    decision_bytes = (
        _render_decision(
            decision_id=paired_id, risk_id=risk_id, title=selected_title, owners=selected_owners, today=today,
            score=score, raised_by=selected_raiser, recommendation=recommendation, threatens=threatened,
        )
        if paired_id is not None
        else None
    )
    result = RaiseResult(risk_id, paired_id, score, tuple(changes))
    if dry_run:
        return result

    # The raise creates artifacts, so it acquires the authority every non-dry-run
    # artifact authoring acquires; it grants nothing and reads no configuration.
    mutation_guard.require_mutation_authority(root, operation="create-artifact")
    created_directories: list[Path] = []
    written: list[Path] = []
    try:
        for destination in [risk_path, *([decision_path] if decision_path is not None else [])]:
            probe = root
            for part in destination.parent.relative_to(root).parts:
                probe = probe / part
                if not probe.exists():
                    probe.mkdir()
                    created_directories.append(probe)
        _atomic_create(risk_path, risk_bytes)
        written.append(risk_path)
        if decision_path is not None and decision_bytes is not None:
            _atomic_create(decision_path, decision_bytes)
            written.append(decision_path)
    except (OSError, HarnessError) as exc:
        for path in reversed(written):
            path.unlink(missing_ok=True)
        _rollback_directories(created_directories)
        if isinstance(exc, HarnessError):
            raise HarnessError(f"raise-risk wrote nothing: {exc}") from exc
        raise HarnessError(f"raise-risk wrote nothing: {exc}") from exc
    return result


def validate_risk_disposition_request(
    risk: Any,
    catalog: Mapping[str, Any],
    *,
    target: str,
    request: Mapping[str, Any],
    actor: str,
    reason: str | None,
) -> dict[str, Any]:
    """RSK-MGT-016 to RSK-MGT-020: the answer copied from the paired decision onto the risk."""

    if risk.status != "raised":
        raise HarnessError(f"{risk.artifact_id} is {risk.status}; only a raised risk is answered")
    if not reason or not reason.strip():
        raise HarnessError(f"answering {risk.artifact_id} requires the verbatim reason")
    option = request.get("option")
    fields: dict[str, Any] = {"decided_by": actor, "reason": reason}
    mitigated_by = [item for item in request.get("mitigated_by") or [] if isinstance(item, str)]
    avoided_by = [item for item in request.get("avoided_by") or [] if isinstance(item, str)]
    if target == "withdrawn":
        if option != "withdrawn":
            raise HarnessError(f"withdrawing {risk.artifact_id} records the option withdrawn, not {option!r}")
        fields.update({"option": "withdrawn", "label": WITHDRAWN_LABEL})
        return fields
    if option not in OPTION_TARGETS or OPTION_TARGETS[option] != target:
        raise HarnessError(f"the option {option!r} names no risk state {target}; a raised risk is answered with accept, avoid or mitigate")
    label = request.get("label")
    fields["option"] = option
    fields["label"] = label if isinstance(label, str) and label.strip() else dict(RISK_OPTIONS)[option]
    revisit = request.get("revisit")
    if option == "accept":
        # RSK-MGT-019: acceptance is time-bounded; the trigger is copied onto the risk.
        if not isinstance(revisit, str) or not revisit.strip():
            raise HarnessError(f"accepting the threat {risk.artifact_id} requires --revisit naming a release, a date, or an artifact state")
        fields["revisit"] = revisit
    elif isinstance(revisit, str) and revisit.strip():
        fields["revisit"] = revisit
    if option == "mitigate":
        if not mitigated_by:
            raise HarnessError(f"mitigating {risk.artifact_id} requires --mitigated-by WO-... naming the work order that reduces the threat")
        for item in mitigated_by:
            found = catalog.get(item)
            if found is None or found.artifact_type != "work_order":
                raise HarnessError(f"--mitigated-by must name a work order; {item} is {'unknown' if found is None else found.artifact_type}")
        fields["mitigated_by"] = mitigated_by
    elif mitigated_by:
        raise HarnessError("--mitigated-by applies to the mitigate answer only")
    if option == "avoid":
        if len(avoided_by) != 1:
            raise HarnessError(f"avoiding {risk.artifact_id} records exactly one ADR or decision in --avoided-by")
        found = catalog.get(avoided_by[0])
        if found is None or found.artifact_type not in {"adr", "decision"}:
            raise HarnessError(f"--avoided-by must name an ADR or a decision; {avoided_by[0]} is {'unknown' if found is None else found.artifact_type}")
        fields["avoided_by"] = avoided_by
    elif avoided_by:
        raise HarnessError("--avoided-by applies to the avoid answer only")
    return fields


def validate_risk_edge(
    risk: Any,
    catalog: Mapping[str, Any],
    *,
    target: str,
    actor: str,
    reason: str | None,
    disposition: Mapping[str, Any] | None,
) -> Mapping[str, Any] | None:
    """The fields a risk transition records: the copied answer when `decide` supplies one.

    Without a disposition only the lifecycle edge is checked, as for a decision; the
    planner then decides whether a bare `transition` may apply it
    (`refuse_bare_risk_transition`).
    """

    if disposition is None:
        return None
    return validate_risk_disposition_request(risk, catalog, target=target, request=disposition, actor=actor, reason=reason)


def refuse_bare_risk_transition(risk: Any, target: str, reason: str | None) -> None:
    """RSK-MGT-021: a risk's state is written by `raise-risk`, `decide` or `transition` only.

    A bare `transition` may withdraw a risk, with a reason, and may close one
    (RSK-MGT-022); it never raises or answers one, because the answer is the paired
    decision's and is written by `decide` in the same act.
    """

    if target == "raised" or target in OPTION_TARGETS.values():
        raise HarnessError(
            f"transition {risk.artifact_id}: a risk is raised with harnessctl raise-risk and answered by disposing the decision that names it, "
            f"with harnessctl decide . --artifact DEC-... --option accept|avoid|mitigate --decision ROLE --reason TEXT"
        )
    if target == "withdrawn" and (reason is None or not reason.strip()):
        raise HarnessError(f"withdrawing {risk.artifact_id} requires --reason")


def dispose_decision_with_risks(
    repository: Path,
    decision_id: str,
    *,
    option: str | None,
    actor: str,
    reason: str | None,
    defer: bool = False,
    withdraw: bool = False,
    scope: tuple[str, ...] = (),
    revisit: str | None = None,
    mitigated_by: tuple[str, ...] = (),
    avoided_by: tuple[str, ...] = (),
    apply: bool = False,
) -> Any:
    """Plan or apply one disposition and, in the same act, the risk moves it names (RSK-MGT-016).

    A decision that concerns no raised risk is disposed exactly as `decisions.dispose_decision`
    disposes it. A deferral leaves every risk in `raised` (RSK-MGT-017); a withdrawal
    withdraws them; a decided option moves each to the state it names.
    """

    from se_harness.repository_graph import artifact_catalog, validated_repository
    from se_harness.workflow import plan_transition

    if defer and withdraw:
        raise HarnessError("--defer and --withdraw are exclusive")
    target = "withdrawn" if withdraw else "deferred" if defer else "decided"
    root = ensure_target(repository, must_exist=True)
    transitions: dict[str, str] = {decision_id: target}
    actors: dict[str, str] = {decision_id: actor}
    reasons: dict[str, str] = {decision_id: reason} if reason is not None else {}
    dispositions: dict[str, Mapping[str, Any]] = {
        decision_id: {"target": target, "option": option, "revisit": revisit, "scope": tuple(scope)},
    }
    _, report = validated_repository(root)
    catalog = artifact_catalog(report) if not any(item.code in {E001, E003} for item in report.errors) else {}
    decision = catalog.get(decision_id)
    risks = raised_risks_of(catalog, decision) if decision is not None and decision.artifact_type == "decision" else []
    if not risks and (mitigated_by or avoided_by):
        raise HarnessError("--mitigated-by and --avoided-by apply only when the decision concerns a raised risk")
    labels = {item["id"]: item["label"] for item in declared_options(decision)} if decision is not None else {}
    for risk in risks:
        if target == "deferred":
            continue
        if target == "withdrawn":
            request: dict[str, Any] = {"option": "withdrawn", "label": WITHDRAWN_LABEL}
            risk_target = "withdrawn"
        else:
            if option not in OPTION_TARGETS:
                raise HarnessError(
                    f"{decision_id} concerns the raised risk {risk.artifact_id}; its answer is accept, avoid or mitigate, not {option!r}"
                )
            risk_target = OPTION_TARGETS[option]
            request = {
                "option": option,
                "label": labels.get(option),
                "revisit": revisit,
                "mitigated_by": list(mitigated_by),
                "avoided_by": list(avoided_by) or ([decision_id] if option == "avoid" else []),
            }
        transitions[risk.artifact_id] = risk_target
        actors[risk.artifact_id] = actor
        if reason is not None:
            reasons[risk.artifact_id] = reason
        dispositions[risk.artifact_id] = request
    return plan_transition(root, transitions, actors, reasons, apply=apply, dispositions=dispositions)


def risks_threatening(repository: Path, artifact_id: str) -> list[dict[str, Any]]:
    """RSK-MGT-033: the risks threatening one artifact and its governing chain; reads only."""

    from se_harness.repository_graph import PRIMARY_TYPES, artifact_catalog, project_scope, validated_repository

    root = ensure_target(repository, must_exist=True)
    _, report = validated_repository(root)
    if any(item.code in {E001, E003} for item in report.errors):
        first = next(item for item in report.errors if item.code in {E001, E003})
        raise HarnessError(f"the artifact graph cannot be read [{first.code}]: {first.message}")
    catalog = artifact_catalog(report)
    primary = catalog.get(artifact_id)
    if primary is None:
        raise HarnessError(f"unknown artifact ID: {artifact_id}")
    chain = {artifact_id}
    if primary.artifact_type in PRIMARY_TYPES:
        governing, _ = project_scope(catalog, primary)
        chain.update(governing)
    rows: list[dict[str, Any]] = []
    for item in catalog.values():
        if getattr(item, "artifact_type", None) != "risk":
            continue
        threatened = sorted(set(_relation(item, "threatens")) & chain)
        if not threatened:
            continue
        pending = paired_decisions(catalog, item.artifact_id)
        rows.append({
            "id": item.artifact_id,
            "title": str(item.metadata.get("title", "")),
            "status": item.status,
            "stage": str(item.metadata.get("stage", "")),
            "category": str(item.metadata.get("category", "")),
            "score": item.metadata.get("score"),
            "threatens": threatened,
            "decision": pending[0].artifact_id if pending else None,
        })
    return sorted(rows, key=lambda row: (-(row["score"] if isinstance(row["score"], int) else 0), row["id"]))


__all__ = [
    "MEASUREMENT",
    "OPTION_TARGETS",
    "RISK_CATEGORIES",
    "RISK_OPTIONS",
    "RISK_STAGES",
    "RaiseResult",
    "compute_score",
    "dispose_decision_with_risks",
    "paired_decisions",
    "raise_risk",
    "raised_risks_of",
    "refuse_bare_risk_transition",
    "resolve_domain",
    "risks_threatening",
    "validate_risk_disposition_request",
    "validate_risk_edge",
]
