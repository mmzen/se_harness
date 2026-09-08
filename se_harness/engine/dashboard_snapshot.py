"""The generator's snapshot seam (SPEC-ECP-024 ECP-ENG-018): the repository projection from a validation report to the Explorer snapshot, with the path resolvers, the Git readers and the content budget the bundle shares.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter, defaultdict, deque
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Sequence

from se_harness.codes import (
    I_REV_001,
    W_HEX_001,
    W_HEX_002,
    W_HEX_003,
    W_HEX_004,
    W_HEX_005,
    W_HEX_006,
    W_REB_001,
    W_REB_002,
    W_REB_003,
    W_REV_002,
    W_REV_003,
    W_REV_004,
)
from se_harness.engine.validate_engineering_artifacts import (
    ACTIVE_COVERAGE_STATUSES,
    Artifact,
    Diagnostic,
    ValidationReport,
    architecture_traceability_state,
    coverage_rows,
    decision_assessment_state,
    evidence_work_order_keys,
    load_revision_policy,
    specification_rules,
    standing_deviations,
)
from se_harness.workflow_contract import IMPLEMENTED_OR_LATER_STATUSES


SNAPSHOT_SCHEMA = "harness-dashboard-snapshot-v1"


EXPERIMENT_SCHEMA = "harness-experiment-result-v1"


FINDING_RULES_VERSION = "harness-findings-v9"


QUALITY_GATES_VERSION = "quality-gates-2026-08-10"


DEFAULT_ARTIFACT_ROOT = Path("docs") / "engineering"


DEFAULT_OUTPUT_ROOT = Path("target") / "harness-dashboard"


DEFAULT_EXPERIMENT_ROOT = Path("docs") / "engineering" / "experiments" / "results"


MAX_EXPERIMENT_BYTES = 1_000_000


MAX_CONTENT_DOCUMENT_BYTES = 262_144


MAX_CONTENT_TOTAL_BYTES = 16_777_216


ALLOWED_EVIDENCE_SUFFIXES = {".md", ".markdown", ".txt"}


ACTIVE_WORK_ORDER_STATUSES = ACTIVE_COVERAGE_STATUSES


INACTIVE_GOVERNING_STATUSES = {"draft", "rejected", "superseded"}


SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


WORK_ORDER_RELATIONS = ("implements", "specifications", "architecture", "verification")


TEMPORAL_REASSESSMENT_RELATIONS = {
    "capability": frozenset({"derives_from"}),
    "requirement": frozenset({"derives_from"}),
    "specification": frozenset({"specifies"}),
    "architecture": frozenset({"addresses", "conforms_to", "constrains"}),
    "adr": frozenset({"decides"}),
    "verification": frozenset({"verifies"}),
    "release_contract": frozenset({"gates"}),
    "operating_contract": frozenset({"assures"}),
    "work_order": frozenset(WORK_ORDER_RELATIONS),
}


TEMPORAL_REASSESSMENT_INACTIVE_STATUSES = frozenset({"rejected", "superseded"})


TEMPORAL_REASSESSMENT_WORK_ORDER_STATUSES = frozenset({"draft", "approved", "in_progress"})


EXPERIMENT_MEASURES = (
    "clarifications",
    "retries",
    "evaluator_defects",
    "wall_seconds",
    "tokens",
    "cost",
)


class GenerationError(RuntimeError):
    """A bounded configuration or generation failure."""


class ContentBudget:
    """Apply deterministic whole-document limits to projected Markdown."""

    def __init__(self) -> None:
        self.projected_bytes = 0
        self.included_documents = 0
        self.omitted_documents = 0

    def project(self, value: str) -> dict[str, Any]:
        markdown = value.replace("\r\n", "\n").replace("\r", "\n")
        payload = markdown.encode("utf-8")
        digest = hashlib.sha256(payload).hexdigest()
        base: dict[str, Any] = {
            "format": "markdown",
            "bytes": len(payload),
            "sha256": digest,
        }
        if len(payload) > MAX_CONTENT_DOCUMENT_BYTES:
            self.omitted_documents += 1
            return {**base, "state": "omitted", "reason": "document_too_large"}
        if self.projected_bytes + len(payload) > MAX_CONTENT_TOTAL_BYTES:
            self.omitted_documents += 1
            return {**base, "state": "omitted", "reason": "total_content_budget_exceeded"}
        self.projected_bytes += len(payload)
        self.included_documents += 1
        return {**base, "state": "included", "markdown": markdown}

    def omit(
        self,
        reason: str,
        *,
        observed_bytes: int | None = None,
    ) -> dict[str, Any]:
        self.omitted_documents += 1
        return {
            "format": "markdown",
            "state": "omitted",
            "reason": reason,
            "bytes": observed_bytes,
            "sha256": None,
        }


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _paths_overlap(first: Path, second: Path) -> bool:
    return is_within(first, second) or is_within(second, first)


def resolve_repository_root(value: Path) -> Path:
    root = value.resolve()
    if not root.exists() or not root.is_dir():
        raise GenerationError("repository root must be an existing readable directory")
    return root


def resolve_artifact_root(repository_root: Path, value: Path | None) -> Path:
    candidate = value or DEFAULT_ARTIFACT_ROOT
    resolved = candidate.resolve() if candidate.is_absolute() else (repository_root / candidate).resolve()
    if not is_within(resolved, repository_root):
        raise GenerationError("artifact root must resolve within the repository root")
    return resolved


def resolve_output_root(
    repository_root: Path,
    artifact_root: Path,
    value: Path | None,
) -> Path:
    candidate = value or DEFAULT_OUTPUT_ROOT
    resolved = candidate.resolve() if candidate.is_absolute() else (repository_root / candidate).resolve()
    if _paths_overlap(resolved, repository_root) and not is_within(resolved, repository_root):
        raise GenerationError("output root must not contain the repository root")
    if resolved == repository_root or _paths_overlap(resolved, artifact_root):
        raise GenerationError("output root must not overlap the repository or artifact root")
    if resolved.exists() and resolved.is_symlink():
        raise GenerationError("output root must not be a symbolic link")
    if resolved.exists() and not resolved.is_dir():
        raise GenerationError("output root collides with a non-directory path")
    return resolved


def repository_relative(path: Path, repository_root: Path) -> str:
    try:
        return path.resolve().relative_to(repository_root).as_posix()
    except ValueError:
        raise GenerationError("a repository source path resolved outside the repository root") from None


def _safe_repository_reference(value: Any, repository_root: Path) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = Path(value.strip())
    if candidate.is_absolute():
        return None
    resolved = (repository_root / candidate).resolve()
    if not is_within(resolved, repository_root):
        return None
    return resolved.relative_to(repository_root).as_posix()


def git_revision(repository_root: Path) -> str | None:
    git = shutil.which("git")
    if git is None:
        return None
    try:
        completed = subprocess.run(
            [git, "-C", str(repository_root), "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    revision = completed.stdout.strip()
    if completed.returncode != 0 or not re.fullmatch(r"[0-9a-fA-F]{7,64}", revision):
        return None
    return revision.lower()


def git_object_format(repository_root: Path) -> str | None:
    git = shutil.which("git")
    if git is None:
        return None
    try:
        completed = subprocess.run(
            [git, "-C", str(repository_root), "rev-parse", "--show-object-format"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    value = completed.stdout.strip().lower()
    return value if completed.returncode == 0 and value in {"sha1", "sha256"} else None


GITHUB_REMOTE = re.compile(
    r"^(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)"
    r"(?P<owner>[A-Za-z0-9_.-]+)/(?P<name>[A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)


def git_source_url(repository_root: Path) -> str | None:
    """A normalized public GitHub URL for the origin remote, or None.

    Only a recognized GitHub remote is admitted, and every accepted spelling
    of the same repository normalizes to one https form so the generated
    bundle stays byte-deterministic for one repository regardless of the
    remote protocol a checkout uses. Anything else is unknown and omitted.
    """
    git = shutil.which("git")
    if git is None:
        return None
    try:
        completed = subprocess.run(
            [git, "-C", str(repository_root), "remote", "get-url", "origin"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    match = GITHUB_REMOTE.match(completed.stdout.strip())
    if match is None:
        return None
    return f"https://github.com/{match.group('owner')}/{match.group('name')}"


def git_commit_availability(repository_root: Path, commits: Sequence[str]) -> dict[str, bool | None]:
    unique = sorted({commit for commit in commits if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit)})
    if not unique:
        return {}
    git = shutil.which("git")
    if git is None or git_revision(repository_root) is None:
        return {commit: None for commit in unique}
    try:
        completed = subprocess.run(
            [git, "-C", str(repository_root), "cat-file", "--batch-check=%(objectname) %(objecttype)"],
            input="".join(f"{commit}^{{commit}}\n" for commit in unique),
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return {commit: None for commit in unique}
    if completed.returncode != 0:
        return {commit: None for commit in unique}
    lines = completed.stdout.splitlines()
    result: dict[str, bool | None] = {}
    for index, commit in enumerate(unique):
        line = lines[index] if index < len(lines) else ""
        result[commit] = bool(re.fullmatch(r"[0-9a-f]{40,64} commit", line.strip()))
    return result


def text_value(value: Any, fallback: str = "") -> str:
    return value.strip() if isinstance(value, str) and value.strip() else fallback


def text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def distribution_table(value: Any) -> dict[str, str | int] | None:
    """The scalar fields of a release record's ``[distribution]`` table."""
    if not isinstance(value, dict):
        return None
    table: dict[str, str | int] = {}
    for key in sorted(value):
        item = value[key]
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9_]{1,64}", key):
            continue
        if isinstance(item, bool):
            continue
        if isinstance(item, int):
            table[key] = item
        elif isinstance(item, str) and len(item) <= 512:
            table[key] = item
    return table or None


def normalize_artifacts(
    report: ValidationReport,
    repository_root: Path,
    content_budget: ContentBudget | None = None,
) -> list[dict[str, Any]]:
    budget = content_budget or ContentBudget()
    catalog = {
        artifact.artifact_id: artifact
        for artifact in report.artifacts
        if artifact.artifact_id != "<unknown>"
    }
    active_decisions_by_architecture: dict[str, set[str]] = defaultdict(set)
    for decision in report.artifacts:
        if decision.artifact_type != "adr" or decision.status not in ACTIVE_COVERAGE_STATUSES:
            continue
        for architecture_id in text_list(decision.relations.get("decides")):
            active_decisions_by_architecture[architecture_id].add(decision.artifact_id)

    # SPEC-DCM-001 rule 13: the decision trail of every concerned artifact and
    # the standing deviations projected by the validator (rule 9).
    standing = standing_deviations(list(report.artifacts))
    decision_trail: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for decision in sorted(report.artifacts, key=lambda item: item.artifact_id):
        if decision.artifact_type != "decision":
            continue
        disposition = decision.metadata.get("disposition")
        disposition = disposition if isinstance(disposition, dict) else {}
        entry = {
            "id": decision.artifact_id,
            "kind": text_value(decision.metadata.get("kind")) or None,
            "status": decision.status,
            "question": text_value(decision.metadata.get("question")) or None,
            "option": text_value(disposition.get("option")) or None,
            "decided_by": text_value(disposition.get("decided_by")) or None,
            "decided_at": text_value(disposition.get("decided_at")) or None,
        }
        for concerned in text_list(decision.relations.get("concerns")):
            decision_trail[concerned].append(entry)

    # SPEC-TCM-005 TCM-RFC-005: what derives from a capability is read from the graph.
    deriving_requirements: dict[str, list[str]] = defaultdict(list)
    for requirement in report.artifacts:
        if requirement.artifact_type != "requirement" or requirement.artifact_id == "<unknown>":
            continue
        for capability_id in text_list(requirement.relations.get("derives_from")):
            if capability_id.startswith("CAP-"):
                deriving_requirements[capability_id].append(requirement.artifact_id)

    # SPEC-TCM-006 TCM-RFS-017: which rules cover a requirement is read from the
    # coverage tables of the specifications, the same source the record panel shows.
    covered_by: dict[str, list[dict[str, str]]] = defaultdict(list)
    for specification in report.artifacts:
        if specification.artifact_type != "specification" or specification.artifact_id == "<unknown>":
            continue
        for requirement_id, rule_ids in coverage_rows(specification.body) or []:
            for rule_id in rule_ids:
                covered_by[requirement_id].append({"specification": specification.artifact_id, "rule": rule_id})

    normalized: list[dict[str, Any]] = []
    for artifact in sorted(report.artifacts, key=lambda item: (item.artifact_id, str(item.path))):
        item: dict[str, Any] = {
            "id": artifact.artifact_id,
            "type": artifact.artifact_type,
            "title": text_value(artifact.metadata.get("title"), "<untitled>"),
            "status": artifact.status,
            "owners": text_list(artifact.metadata.get("owners")),
            "created": text_value(artifact.metadata.get("created")) or None,
            "updated": text_value(artifact.metadata.get("updated")) or None,
            "path": repository_relative(artifact.path, repository_root),
            "authority": "formal",
            "content": budget.project(artifact.body),
        }
        if artifact.artifact_type == "requirement":
            item["statement"] = text_value(artifact.metadata.get("statement")) or None
            # ECP-COR-018: the closed-vocabulary array and the legacy string both reach the Explorer.
            method = artifact.metadata.get("verification_method")
            if isinstance(method, list):
                item["verification_method"] = ", ".join(text_list(method)) or None
            else:
                item["verification_method"] = text_value(method) or None
            plain_words = _plain_words(artifact.body)
            if plain_words:
                item["plain_words"] = plain_words
            item["covered_by"] = sorted(covered_by.get(artifact.artifact_id, []), key=lambda entry: (entry["specification"], entry["rule"]))
        if artifact.artifact_type == "specification":
            # SPEC-TCM-006 TCM-RFS-016: the contract line, the plain words, the rules by
            # identifier and the coverage table of a specification.
            contract = text_value(artifact.metadata.get("contract")) or None
            if contract:
                item["contract"] = contract
            plain_words = _plain_words(artifact.body)
            if plain_words:
                item["plain_words"] = plain_words
            item["rules"] = [
                {"id": identifier, "text": text}
                for identifier, text in specification_rules(artifact.body)
                if identifier is not None
            ]
            item["coverage"] = [
                {"requirement": requirement_id, "rules": list(rule_ids)}
                for requirement_id, rule_ids in coverage_rows(artifact.body) or []
            ]
        if artifact.artifact_type == "intent":
            # SPEC-TCM-004 TCM-RFI-006: the outcome line and the plain words of an intent.
            outcome = text_value(artifact.metadata.get("outcome")) or None
            if outcome:
                item["outcome"] = outcome
            plain_words = _plain_words(artifact.body)
            if plain_words:
                item["plain_words"] = plain_words
            item["success_measure_rows"] = _success_measure_row_count(artifact.body)
        if artifact.artifact_type == "capability":
            # SPEC-TCM-005 TCM-RFC-005 and TCM-RFC-006: the ability line, the plain words
            # and the requirements that derive from the capability, from the graph.
            ability = text_value(artifact.metadata.get("ability")) or None
            if ability:
                item["ability"] = ability
            plain_words = _plain_words(artifact.body)
            if plain_words:
                item["plain_words"] = plain_words
            item["derived_requirements"] = sorted(set(deriving_requirements.get(artifact.artifact_id, [])))
        if artifact.artifact_type == "architecture":
            item["architecture_traceability"] = architecture_traceability_state(
                artifact,
                catalog,
            )
            assessment = decision_assessment_state(artifact)
            deciding_adrs = sorted(active_decisions_by_architecture.get(artifact.artifact_id, set()))
            if assessment["state"] == "valid":
                if assessment["outcome"] == "adr_required":
                    state = "adr_required_covered" if deciding_adrs else "adr_required_missing"
                else:
                    state = "no_significant_decision_justified"
            elif assessment["state"] == "legacy_missing":
                state = "legacy_adr_covered" if deciding_adrs else "legacy_adr_missing"
            else:
                state = f"assessment_{assessment['state']}"
            item["decision_assessment"] = {
                "state": state,
                "outcome": assessment["outcome"],
                "triggers": assessment["triggers"],
                "rationale": assessment["rationale"],
                "assessed_by": assessment["assessed_by"],
                "deciding_adrs": deciding_adrs,
            }
        if artifact.artifact_type == "work_order":
            assurance = artifact.metadata.get("assurance")
            if isinstance(assurance, dict):
                item["assurance_classification"] = {
                    "commit_bound_verification": text_value(assurance.get("commit_bound_verification")) or None,
                    "rationale": text_value(assurance.get("rationale")) or None,
                    "decided_by": text_value(assurance.get("decided_by")) or None,
                }
        lifecycle_events = artifact.metadata.get("lifecycle_events")
        item["lifecycle_events"] = [
            {
                key: text_value(event.get(key)) or None
                for key in ("from", "to", "decided_at", "decided_by", "reason")
            }
            for event in lifecycle_events
            if isinstance(event, dict)
        ] if isinstance(lifecycle_events, list) else []
        item["rejected_at"] = text_value(artifact.metadata.get("rejected_at")) or None
        item["rejected_by"] = text_value(artifact.metadata.get("rejected_by")) or None
        item["rejection_reason"] = text_value(artifact.metadata.get("rejection_reason")) or None
        if artifact.artifact_type == "verification_record":
            item["commit"] = text_value(artifact.metadata.get("commit")) or None
            item["git_object_format"] = text_value(artifact.metadata.get("git_object_format")) or None
            item["worktree_state"] = text_value(artifact.metadata.get("worktree_state")) or None
            item["prepared_at"] = text_value(artifact.metadata.get("prepared_at")) or None
            item["prepared_by"] = text_value(artifact.metadata.get("prepared_by")) or None
            item["verified_at"] = text_value(artifact.metadata.get("verified_at")) or None
            item["verified_by"] = text_value(artifact.metadata.get("verified_by")) or None
            item["artifact_snapshot_sha256"] = text_value(artifact.metadata.get("artifact_snapshot_sha256")) or None
            item["evidence_paths"] = text_list(artifact.metadata.get("evidence_paths"))
            item["superseded_at"] = text_value(artifact.metadata.get("superseded_at")) or None
            item["supersession_authorized_by"] = text_value(artifact.metadata.get("supersession_authorized_by")) or None
            item["evaluator_evidence_path"] = text_value(artifact.metadata.get("evaluator_evidence_path")) or None
            item["evaluator_evidence_sha256"] = text_value(artifact.metadata.get("evaluator_evidence_sha256")) or None
        if artifact.artifact_type == "decision":
            item.update(_decision_projection(artifact, catalog))
        if decision_trail.get(artifact.artifact_id):
            item["decisions"] = decision_trail[artifact.artifact_id]
        if standing.get(artifact.artifact_id):
            item["standing_deviations"] = standing[artifact.artifact_id]
        if artifact.artifact_type == "release_record":
            item["commit"] = text_value(artifact.metadata.get("commit")) or None
            item["git_object_format"] = text_value(artifact.metadata.get("git_object_format")) or None
            item["version"] = text_value(artifact.metadata.get("version")) or None
            item["tag"] = text_value(artifact.metadata.get("tag")) or None
            item["prepared_at"] = text_value(artifact.metadata.get("prepared_at")) or None
            item["prepared_by"] = text_value(artifact.metadata.get("prepared_by")) or None
            item["released_at"] = text_value(artifact.metadata.get("released_at")) or None
            item["authorized_by"] = text_value(artifact.metadata.get("authorized_by")) or None
            item["evaluator_evidence_path"] = text_value(artifact.metadata.get("evaluator_evidence_path")) or None
            item["evaluator_evidence_sha256"] = text_value(artifact.metadata.get("evaluator_evidence_sha256")) or None
            item["distribution"] = distribution_table(artifact.metadata.get("distribution"))
        normalized.append(item)
    return sorted(normalized, key=lambda item: (item["id"], item["path"]))


def _decision_projection(artifact: Artifact, catalog: dict[str, Artifact]) -> dict[str, Any]:
    """The decision's own fields (SPEC-DCM-001 rules 2-3, 6) and its deciding roles.

    A deviation is decided by the owners of the specification it departs from;
    a question by the owners of the artifacts it blocks. The projection restates
    the declared owners; it infers no decision.
    """

    options = artifact.metadata.get("options")
    disposition = artifact.metadata.get("disposition")
    disposition = disposition if isinstance(disposition, dict) else None
    against = text_value(artifact.metadata.get("against")) or None
    blocked = text_list(artifact.relations.get("blocks"))
    deciding: set[str] = set()
    if artifact.metadata.get("kind") == "deviation" and against:
        target = catalog.get(against.split("#", 1)[0])
        if target is not None:
            deciding.update(text_list(target.metadata.get("owners")))
    else:
        for blocked_id in blocked:
            target = catalog.get(blocked_id)
            if target is not None:
                deciding.update(text_list(target.metadata.get("owners")))
    if not deciding:
        deciding.update(text_list(artifact.metadata.get("owners")))
    projection: dict[str, Any] = {
        "kind": text_value(artifact.metadata.get("kind")) or None,
        "question": text_value(artifact.metadata.get("question")) or None,
        "raised_by": text_value(artifact.metadata.get("raised_by")) or None,
        "recommendation": text_value(artifact.metadata.get("recommendation")) or None,
        "against": against,
        "observed": text_value(artifact.metadata.get("observed")) or None,
        "options": [
            {"id": text_value(option.get("id")), "label": text_value(option.get("label"))}
            for option in options
            if isinstance(option, dict)
        ] if isinstance(options, list) else [],
        "blocks": blocked,
        "deciding_roles": sorted(deciding),
        "disposition": None,
    }
    if disposition is not None:
        projection["disposition"] = {
            "option": text_value(disposition.get("option")) or None,
            "label": text_value(disposition.get("label")) or None,
            "decided_by": text_value(disposition.get("decided_by")) or None,
            "decided_at": text_value(disposition.get("decided_at")) or None,
            "reason": text_value(disposition.get("reason")) or None,
            "revisit": text_value(disposition.get("revisit")) or None,
            "scope": text_list(disposition.get("scope")),
        }
    return projection


_PLAIN_WORDS_HEADING = "## In plain words"


_SUCCESS_MEASURES_HEADING = "## Success measures"


def _success_measure_row_count(body: Any) -> int:
    """Data rows of an intent's `Success measures` table (SPEC-TCM-004 TCM-RFI-006); 0 when absent or malformed."""

    if not isinstance(body, str):
        return 0
    inside = False
    header_seen = False
    rows = 0
    for line in body.replace("\r\n", "\n").split("\n"):
        if line.strip() == _SUCCESS_MEASURES_HEADING:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        stripped = line.strip()
        if not inside or not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not header_seen:
            header_seen = True
            continue
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        if len(cells) < 4:
            return 0
        rows += 1
    return rows


def _plain_words(body: Any) -> str | None:
    """The text of a requirement's `In plain words` section (SPEC-TCM-003 TCM-RFR-004), or None."""

    if not isinstance(body, str):
        return None
    lines = body.replace("\r\n", "\n").split("\n")
    collected: list[str] = []
    inside = False
    for line in lines:
        if line.strip() == _PLAIN_WORDS_HEADING:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside and line.strip():
            collected.append(line.strip())
    text = " ".join(collected).strip()
    return text or None


def build_declared_relations(artifacts: Sequence[Artifact]) -> list[dict[str, Any]]:
    catalog = {artifact.artifact_id for artifact in artifacts if artifact.artifact_id != "<unknown>"}
    relations: list[dict[str, Any]] = []
    for artifact in artifacts:
        for relation_name, targets in sorted(artifact.relations.items()):
            if not isinstance(targets, list):
                continue
            for target in targets:
                if not isinstance(target, str) or not target.strip():
                    continue
                clean_target = target.strip()
                relations.append(
                    {
                        "source": artifact.artifact_id,
                        "relation": relation_name,
                        "target": clean_target,
                        "authority": "declared",
                        "target_exists": clean_target in catalog,
                    }
                )
    return sorted(
        relations,
        key=lambda item: (item["source"], item["relation"], item["target"], not item["target_exists"]),
    )


def build_architecture_transitive_relations(artifacts: Sequence[Artifact]) -> list[dict[str, Any]]:
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>"
    }
    paths: dict[tuple[str, str], set[str]] = defaultdict(set)
    for architecture in artifacts:
        if architecture.artifact_type != "architecture":
            continue
        traceability = architecture_traceability_state(architecture, catalog)
        if traceability["state"] not in {"typed", "dual_declared"}:
            continue
        for specification_id in traceability["conforms_to"]:
            specification = catalog.get(specification_id)
            if specification is None or specification.artifact_type != "specification":
                continue
            for requirement_id in text_list(specification.relations.get("specifies")):
                if requirement_id in catalog:
                    paths[(architecture.artifact_id, requirement_id)].add(specification_id)
    return [
        {
            "source": source,
            "relation": "conforms_transitively_to_requirement",
            "target": target,
            "authority": "derived",
            "target_exists": True,
            "via": sorted(via),
        }
        for (source, target), via in sorted(paths.items())
    ]


def _diagnostic_payload(
    diagnostic: Diagnostic,
    severity: str,
    artifacts_by_path: dict[str, list[str]],
) -> dict[str, Any]:
    return {
        "code": diagnostic.code,
        "severity": severity,
        "path": diagnostic.path,
        "message": diagnostic.message,
        "artifacts": sorted(artifacts_by_path.get(diagnostic.path, [])),
        "authority": "validator",
    }


def normalize_diagnostics(
    report: ValidationReport,
    normalized_artifacts: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    artifacts_by_path: dict[str, list[str]] = defaultdict(list)
    for artifact in normalized_artifacts:
        artifacts_by_path[artifact["path"]].append(artifact["id"])
    diagnostics = [
        *(_diagnostic_payload(item, "error", artifacts_by_path) for item in report.errors),
        *(_diagnostic_payload(item, "warning", artifacts_by_path) for item in report.warnings),
    ]
    return sorted(
        diagnostics,
        key=lambda item: (
            SEVERITY_ORDER[item["severity"]],
            item["code"],
            item["path"],
            item["message"],
        ),
    )


def discover_evidence(repository_root: Path) -> dict[str, list[str]]:
    engineering_root = repository_root / "docs" / "engineering"
    evidence: dict[str, list[str]] = defaultdict(list)
    if not engineering_root.exists():
        return {}
    for path in sorted(engineering_root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = repository_relative(path, repository_root)
        if (
            "evidence" not in PurePosixPath(relative_path).parts
            or _evidence_path_has_symlink(repository_root, Path(relative_path))
        ):
            continue
        for work_order_id in evidence_work_order_keys(relative_path):
            evidence[work_order_id].append(relative_path)
    return {key: sorted(set(paths)) for key, paths in sorted(evidence.items())}


def _evidence_path_has_symlink(repository_root: Path, relative: Path) -> bool:
    current = repository_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink() or bool(
            getattr(current, "is_junction", lambda: False)()
        ):
            return True
    return False


def project_evidence_document(
    repository_root: Path,
    path_value: str,
    associations: Sequence[str],
    budget: ContentBudget,
) -> dict[str, Any]:
    normalized_value = path_value.replace("\\", "/")
    relative = Path(normalized_value)
    base = {
        "path": normalized_value,
        "associations": sorted(set(associations)),
    }
    if (
        relative.is_absolute()
        or not relative.parts
        or ".." in relative.parts
        or relative.parts[:2] != ("docs", "engineering")
        or "evidence" not in relative.parts
    ):
        return {**base, **budget.omit("unsafe_evidence_path")}
    if relative.suffix.lower() not in ALLOWED_EVIDENCE_SUFFIXES:
        return {**base, **budget.omit("unsupported_evidence_format")}
    source = repository_root.joinpath(*relative.parts)
    try:
        if _evidence_path_has_symlink(repository_root, relative):
            return {**base, **budget.omit("symlink_not_allowed")}
        resolved = source.resolve(strict=True)
        engineering_root = (repository_root / "docs" / "engineering").resolve(strict=True)
        resolved_relative = resolved.relative_to(engineering_root)
        if "evidence" not in resolved_relative.parts or not source.is_file():
            return {**base, **budget.omit("unsafe_evidence_path")}
        before = source.stat()
        observed_bytes = before.st_size
        if observed_bytes > MAX_CONTENT_DOCUMENT_BYTES:
            return {
                **base,
                **budget.omit("document_too_large", observed_bytes=observed_bytes),
            }
        raw = source.read_bytes()
        after = source.stat()
        resolved_after = source.resolve(strict=True)
        if (
            resolved_after != resolved
            or _evidence_path_has_symlink(repository_root, relative)
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            or len(raw) != after.st_size
        ):
            return {
                **base,
                **budget.omit(
                    "evidence_changed_during_generation",
                    observed_bytes=len(raw),
                ),
            }
        markdown = raw.decode("utf-8-sig")
    except FileNotFoundError:
        return {**base, **budget.omit("evidence_unavailable")}
    except UnicodeDecodeError:
        return {**base, **budget.omit("evidence_not_utf8")}
    except (OSError, RuntimeError, ValueError):
        return {**base, **budget.omit("evidence_unreadable")}
    projected = budget.project(markdown)
    if projected["state"] == "included":
        projected["raw_path"] = f"content/{projected['sha256']}.txt"
    return {**base, **projected}


def build_evidence_documents(
    report: ValidationReport,
    repository_root: Path,
    evidence_by_work_order: dict[str, list[str]],
    budget: ContentBudget,
) -> list[dict[str, Any]]:
    associations_by_path: dict[str, set[str]] = defaultdict(set)
    for work_order, paths in sorted(evidence_by_work_order.items()):
        for path in paths:
            associations_by_path[path].add(work_order)
    for artifact in report.artifacts:
        if artifact.artifact_type != "verification_record":
            continue
        for path in text_list(artifact.metadata.get("evidence_paths")):
            associations_by_path[path.replace("\\", "/")].add(artifact.artifact_id)
    return [
        project_evidence_document(
            repository_root,
            path,
            sorted(associations),
            budget,
        )
        for path, associations in sorted(associations_by_path.items())
    ]


def _valid_relations(relations: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return [relation for relation in relations if relation["target_exists"]]


def _strongly_connected_components(
    artifact_ids: Sequence[str],
    relations: Sequence[dict[str, Any]],
) -> list[list[str]]:
    adjacency: dict[str, list[str]] = {artifact_id: [] for artifact_id in artifact_ids}
    reverse: dict[str, list[str]] = {artifact_id: [] for artifact_id in artifact_ids}
    self_loops: set[str] = set()
    for relation in relations:
        if not relation.get("target_exists", True):
            continue
        source = relation["source"]
        target = relation["target"]
        if source not in adjacency or target not in adjacency:
            continue
        adjacency[source].append(target)
        reverse[target].append(source)
        if source == target:
            self_loops.add(source)
    for graph in (adjacency, reverse):
        for node in graph:
            graph[node] = sorted(set(graph[node]))

    visited: set[str] = set()
    finish_order: list[str] = []
    for start in sorted(adjacency):
        if start in visited:
            continue
        visited.add(start)
        stack: list[tuple[str, int]] = [(start, 0)]
        while stack:
            node, index = stack[-1]
            neighbors = adjacency[node]
            if index < len(neighbors):
                neighbor = neighbors[index]
                stack[-1] = (node, index + 1)
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, 0))
            else:
                stack.pop()
                finish_order.append(node)

    assigned: set[str] = set()
    components: list[list[str]] = []
    for start in reversed(finish_order):
        if start in assigned:
            continue
        component: list[str] = []
        stack = [start]
        assigned.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            for neighbor in reverse[node]:
                if neighbor not in assigned:
                    assigned.add(neighbor)
                    stack.append(neighbor)
        component.sort()
        if len(component) > 1 or component[0] in self_loops:
            components.append(component)
    return sorted(components)


def _finding(
    rule: str,
    severity: str,
    message: str,
    artifacts: Iterable[str] = (),
    paths: Iterable[str] = (),
    evidence: Iterable[str] = (),
    *,
    authority: str = "derived",
) -> dict[str, Any]:
    return {
        "rule": rule,
        "severity": severity,
        "message": message,
        "artifacts": sorted(set(artifacts)),
        "paths": sorted(set(paths)),
        "evidence": sorted(set(evidence)),
        "authority": authority,
    }


def _supports_temporal_reassessment(
    source: dict[str, Any],
    relation: dict[str, Any],
) -> bool:
    """Return whether a declared edge has governed reassessment meaning."""

    if relation.get("authority") != "declared":
        return False
    supported = TEMPORAL_REASSESSMENT_RELATIONS.get(source["type"], frozenset())
    if relation["relation"] not in supported:
        return False
    if source["status"] in TEMPORAL_REASSESSMENT_INACTIVE_STATUSES:
        return False
    if source["type"] == "work_order":
        return source["status"] in TEMPORAL_REASSESSMENT_WORK_ORDER_STATUSES
    return True


def build_findings(
    normalized_artifacts: Sequence[dict[str, Any]],
    relations: Sequence[dict[str, Any]],
    diagnostics: Sequence[dict[str, Any]],
    evidence_by_work_order: dict[str, list[str]],
    revision_provenance: Sequence[dict[str, Any]],
    revision_policy: dict[str, bool],
) -> list[dict[str, Any]]:
    artifacts = {artifact["id"]: artifact for artifact in normalized_artifacts}
    findings = [
        _finding(
            diagnostic["code"],
            diagnostic["severity"],
            diagnostic["message"],
            diagnostic["artifacts"],
            [diagnostic["path"]],
            authority="validator",
        )
        for diagnostic in diagnostics
    ]

    for artifact in normalized_artifacts:
        if (
            artifact["type"] == "work_order"
            and artifact["status"] in IMPLEMENTED_OR_LATER_STATUSES
            and not evidence_by_work_order.get(artifact["id"])
        ):
            findings.append(
                _finding(
                    W_HEX_001,
                    "warning",
                    f"{artifact['id']} is {artifact['status']} but has no evidence document keyed to its ID.",
                    [artifact["id"]],
                    [artifact["path"]],
                )
            )

    relations_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in relations:
        relations_by_source[relation["source"]].append(relation)

    for artifact in normalized_artifacts:
        if artifact["type"] != "work_order" or artifact["status"] not in ACTIVE_WORK_ORDER_STATUSES:
            continue
        invalid_governing: set[str] = set()
        for relation in relations_by_source.get(artifact["id"], []):
            if relation["relation"] not in WORK_ORDER_RELATIONS or not relation["target_exists"]:
                continue
            target = artifacts.get(relation["target"])
            if target is not None and target["status"] in INACTIVE_GOVERNING_STATUSES:
                invalid_governing.add(target["id"])
        if invalid_governing:
            findings.append(
                _finding(
                    W_HEX_002,
                    "warning",
                    f"{artifact['id']} references inactive governing artifacts: {', '.join(sorted(invalid_governing))}.",
                    [artifact["id"], *invalid_governing],
                    [artifact["path"], *(artifacts[item]["path"] for item in invalid_governing)],
                )
            )

    stale_relations: set[tuple[str, str, str]] = set()
    for relation in relations:
        if not relation["target_exists"]:
            continue
        source = artifacts.get(relation["source"])
        target = artifacts.get(relation["target"])
        if source is None or target is None or not source["updated"] or not target["updated"]:
            continue
        relation_key = (source["id"], relation["relation"], target["id"])
        if (
            _supports_temporal_reassessment(source, relation)
            and source["updated"] < target["updated"]
            and relation_key not in stale_relations
        ):
            stale_relations.add(relation_key)
            findings.append(
                _finding(
                    W_HEX_003,
                    "warning",
                    f"{source['id']} predates newer declared {relation['relation']} target {target['id']} and may require reassessment.",
                    [source["id"], target["id"]],
                    [source["path"], target["path"]],
                    [
                        f"relation={relation['relation']}",
                        f"{source['updated']} < {target['updated']}",
                    ],
                )
            )

    components = _strongly_connected_components(sorted(artifacts), _valid_relations(relations))
    for component in components:
        findings.append(
            _finding(
                W_HEX_004,
                "warning",
                f"Declared dependency traversal contains a cycle among: {', '.join(component)}.",
                component,
                [artifacts[item]["path"] for item in component if item in artifacts],
            )
        )

    connected: set[str] = set()
    for relation in relations:
        if relation["target_exists"]:
            connected.add(relation["source"])
            connected.add(relation["target"])
    for artifact in normalized_artifacts:
        if artifact["type"] != "intent" and artifact["id"] not in connected:
            findings.append(
                _finding(
                    W_HEX_005,
                    "warning",
                    f"{artifact['id']} has no valid declared edge after invalid targets are removed.",
                    [artifact["id"]],
                    [artifact["path"]],
                )
            )

    relation_counts = Counter(
        (relation["source"], relation["relation"], relation["target"])
        for relation in relations
    )
    for (source, relation_name, target), count in sorted(relation_counts.items()):
        if count > 1:
            paths = [artifacts[source]["path"]] if source in artifacts else []
            findings.append(
                _finding(
                    W_HEX_006,
                    "warning",
                    f"{source} repeats target {target} {count} times in relation {relation_name}.",
                    [source, target],
                    paths,
                    [f"duplicate_count={count}"],
                )
            )

    verified_by_work: dict[str, set[str]] = defaultdict(set)
    released_by_work: dict[str, set[str]] = defaultdict(set)
    for entry in revision_provenance:
        for work_order in entry["work_orders"]:
            if entry["kind"] == "verification" and entry["status"] in {"verified", "released"}:
                verified_by_work[work_order].add(entry["id"])
            if entry["kind"] == "release" and entry["status"] == "released":
                released_by_work[work_order].add(entry["id"])
        if entry["match_state"] == "different" and entry["status"] != "superseded":
            findings.append(
                _finding(
                    I_REV_001,
                    "info",
                    f"Observed checkout differs from declared candidate commit on {entry['id']}; this can be expected in a later governance commit.",
                    [entry["id"]],
                    evidence=[f"declared={entry['commit']}", f"observed={entry['observed_revision'] or 'unavailable'}"],
                )
            )
        if entry["commit_available"] is False:
            findings.append(
                _finding(
                    W_REV_003,
                    "warning",
                    f"Declared candidate commit on {entry['id']} is unavailable in the current clone.",
                    [entry["id"]],
                    evidence=[f"declared={entry['commit']}"],
                )
            )

    verification_entries = [entry for entry in revision_provenance if entry["kind"] == "verification"]
    for source in verification_entries:
        source_work = set(source["work_orders"])
        if source["status"] != "ready" or not source_work or source["superseded_by"]:
            continue
        possible_successors = sorted(
            target["id"]
            for target in verification_entries
            if target["id"] != source["id"]
            and target["status"] in {"verified", "released"}
            and source_work <= set(target["work_orders"])
        )
        if possible_successors:
            findings.append(
                _finding(
                    W_REV_004,
                    "warning",
                    f"{source['id']} is ready but its work is fully covered by verified or released records; review possible supersession without inferring authority.",
                    [source["id"], *possible_successors],
                    [artifacts[source["id"]]["path"], *(artifacts[item]["path"] for item in possible_successors)],
                    [f"possible_successors={','.join(possible_successors)}"],
                )
            )

    release_entries = [entry for entry in revision_provenance if entry["kind"] == "release"]
    proposed_releases = [
        entry for entry in release_entries if entry["status"] in {"draft", "ready"} and entry["version"]
    ]
    proposals_by_version: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in proposed_releases:
        proposals_by_version[str(entry["version"])].append(entry)
    for version, proposals in sorted(proposals_by_version.items()):
        if len(proposals) < 2:
            continue
        proposals = sorted(proposals, key=lambda item: item["id"])
        findings.append(
            _finding(
                W_REB_001,
                "warning",
                f"Multiple draft or ready release records declare version {version}; accountable release review is required without automatic selection.",
                [entry["id"] for entry in proposals],
                [artifacts[entry["id"]]["path"] for entry in proposals],
                [
                    f"version={version}",
                    *(f"{entry['id']}:commit={entry['commit'] or 'unavailable'}" for entry in proposals),
                ],
            )
        )

    ready_verifications = sorted(
        (entry for entry in verification_entries if entry["status"] == "ready"),
        key=lambda item: item["id"],
    )
    for index, left in enumerate(ready_verifications):
        for right in ready_verifications[index + 1 :]:
            overlap = sorted(set(left["work_orders"]) & set(right["work_orders"]))
            if not overlap or not left["commit"] or not right["commit"] or left["commit"] == right["commit"]:
                continue
            findings.append(
                _finding(
                    W_REB_002,
                    "warning",
                    "Ready verification records at different commits overlap work-order coverage without a governed supersession disposition.",
                    [left["id"], right["id"], *overlap],
                    [artifacts[left["id"]]["path"], artifacts[right["id"]]["path"]],
                    [
                        f"{left['id']}:commit={left['commit']}",
                        f"{right['id']}:commit={right['commit']}",
                        f"overlap={','.join(overlap)}",
                    ],
                )
            )

    active_contract_ids = {
        artifact["id"]
        for artifact in normalized_artifacts
        if artifact["type"] == "release_contract"
        and artifact["status"] not in {"rejected", "superseded"}
    }
    gates_by_contract: dict[str, set[str]] = defaultdict(set)
    for relation in relations:
        if (
            relation["target_exists"]
            and relation["relation"] == "gates"
            and relation["source"] in active_contract_ids
            and artifacts.get(relation["target"], {}).get("type") == "work_order"
        ):
            gates_by_contract[relation["source"]].add(relation["target"])
    for index, left in enumerate(proposed_releases):
        for right in proposed_releases[index + 1 :]:
            work_overlap = sorted(set(left["work_orders"]) & set(right["work_orders"]))
            if not work_overlap or left["version"] != right["version"]:
                continue
            competing: list[str] = []
            for left_contract in left["contracts"]:
                for right_contract in right["contracts"]:
                    gate_overlap = sorted(
                        gates_by_contract[left_contract] & gates_by_contract[right_contract]
                    )
                    if left_contract != right_contract and gate_overlap:
                        competing.append(
                            f"{left_contract}/{right_contract}:gates={','.join(gate_overlap)}"
                        )
            if not competing:
                continue
            contract_ids = sorted(set(left["contracts"]) | set(right["contracts"]))
            findings.append(
                _finding(
                    W_REB_003,
                    "warning",
                    "Active release contracts and associated proposals compete for the same version and governed work.",
                    [left["id"], right["id"], *contract_ids, *work_overlap],
                    [
                        artifacts[item]["path"]
                        for item in [left["id"], right["id"], *contract_ids]
                        if item in artifacts
                    ],
                    [
                        f"version={left['version']}",
                        f"work_overlap={','.join(work_overlap)}",
                        *competing,
                    ],
                )
            )

    for artifact in normalized_artifacts:
        if artifact["type"] != "work_order":
            continue
        if (
            revision_policy["required_for_release"]
            and artifact["status"] == "released"
            and not released_by_work.get(artifact["id"])
        ):
            findings.append(
                _finding(
                    W_REV_002,
                    "warning",
                    f"{artifact['id']} is released but has no released commit-bound release record.",
                    [artifact["id"]],
                    [artifact["path"]],
                )
            )

    return sorted(
        findings,
        key=lambda item: (
            SEVERITY_ORDER[item["severity"]],
            item["rule"],
            item["artifacts"],
            item["message"],
        ),
    )


def build_coverage(
    normalized_artifacts: Sequence[dict[str, Any]],
    relations: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    artifacts = {artifact["id"]: artifact for artifact in normalized_artifacts}
    active_specs: dict[str, set[str]] = defaultdict(set)
    active_verifications: dict[str, set[str]] = defaultdict(set)
    for relation in relations:
        if not relation["target_exists"]:
            continue
        source = artifacts.get(relation["source"])
        target = artifacts.get(relation["target"])
        if source is None or target is None or target["type"] != "requirement":
            continue
        if relation["relation"] == "specifies" and source["type"] == "specification" and source["status"] in ACTIVE_COVERAGE_STATUSES:
            active_specs[target["id"]].add(source["id"])
        if relation["relation"] == "verifies" and source["type"] == "verification" and source["status"] in ACTIVE_COVERAGE_STATUSES:
            active_verifications[target["id"]].add(source["id"])

    coverage: list[dict[str, Any]] = []
    for artifact in normalized_artifacts:
        if artifact["type"] != "requirement":
            continue
        active = artifact["status"] in ACTIVE_COVERAGE_STATUSES
        specifications = sorted(active_specs.get(artifact["id"], set()))
        verifications = sorted(active_verifications.get(artifact["id"], set()))
        missing: list[str] = []
        if active and not specifications:
            missing.append("specification")
        if active and not verifications:
            missing.append("verification")
        coverage.append(
            {
                "requirement": artifact["id"],
                "status": artifact["status"],
                "active": active,
                "specifications": specifications,
                "verifications": verifications,
                "specified": bool(specifications),
                "verified": bool(verifications),
                "missing": missing,
            }
        )
    return sorted(coverage, key=lambda item: item["requirement"])


def _condition(
    condition_id: str,
    label: str,
    state: str,
    evidence: Iterable[str] = (),
) -> dict[str, Any]:
    return {
        "id": condition_id,
        "label": label,
        "state": state,
        "evidence": sorted(set(evidence)),
    }


def _gate(gate_id: str, label: str, conditions: Sequence[dict[str, Any]]) -> dict[str, Any]:
    states = {condition["state"] for condition in conditions}
    state = "unsatisfied" if "unsatisfied" in states else "not_assessable" if "not_assessable" in states else "satisfied"
    return {"gate": gate_id, "label": label, "state": state, "conditions": list(conditions)}


def build_readiness(
    normalized_artifacts: Sequence[dict[str, Any]],
    relations: Sequence[dict[str, Any]],
    diagnostics: Sequence[dict[str, Any]],
    evidence_by_work_order: dict[str, list[str]],
    revision_policy: dict[str, bool],
) -> list[dict[str, Any]]:
    artifacts = {artifact["id"]: artifact for artifact in normalized_artifacts}
    valid_relations = _valid_relations(relations)
    outbound: dict[str, list[dict[str, Any]]] = defaultdict(list)
    inbound: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in valid_relations:
        outbound[relation["source"]].append(relation)
        inbound[relation["target"]].append(relation)
    diagnostic_artifacts = {
        artifact_id
        for diagnostic in diagnostics
        if diagnostic["severity"] == "error"
        for artifact_id in diagnostic["artifacts"]
    }

    readiness: list[dict[str, Any]] = []
    for work_order in normalized_artifacts:
        if work_order["type"] != "work_order":
            continue
        by_relation: dict[str, list[str]] = defaultdict(list)
        for relation in outbound.get(work_order["id"], []):
            by_relation[relation["relation"]].append(relation["target"])
        for relation_name in by_relation:
            by_relation[relation_name] = sorted(set(by_relation[relation_name]))

        reachable: set[str] = set()
        queue = deque([work_order["id"]])
        while queue:
            current = queue.popleft()
            for relation in outbound.get(current, []):
                if relation["target"] not in reachable:
                    reachable.add(relation["target"])
                    queue.append(relation["target"])
        intents = sorted(
            artifact_id
            for artifact_id in reachable
            if artifacts.get(artifact_id, {}).get("type") == "intent"
            and artifacts[artifact_id]["status"] in ACTIVE_COVERAGE_STATUSES
        )
        # SPEC-TCM-004 TCM-RFI-006: a derived observation, never a gate result.
        measured_intents = [
            artifact_id
            for artifact_id in intents
            if artifacts[artifact_id].get("outcome") and artifacts[artifact_id].get("success_measure_rows", 0) > 0
        ]
        requirements = by_relation.get("implements", [])
        required_contracts = [
            artifact_id
            for relation_name in ("specifications", "architecture", "verification")
            for artifact_id in by_relation.get(relation_name, [])
        ]
        governing_active = bool(required_contracts) and all(
            artifacts.get(artifact_id, {}).get("status") in ACTIVE_COVERAGE_STATUSES
            for artifact_id in required_contracts
        )
        requirements_active = bool(requirements) and all(
            artifacts.get(artifact_id, {}).get("status") in ACTIVE_COVERAGE_STATUSES
            for artifact_id in requirements
        )
        requirements_clean = requirements_active and not any(
            artifact_id in diagnostic_artifacts for artifact_id in requirements
        )
        release_ids = sorted(
            {
                relation["source"]
                for relation in inbound.get(work_order["id"], [])
                if relation["relation"] == "gates"
                and artifacts.get(relation["source"], {}).get("type") == "release_contract"
            }
        )
        release_active = bool(release_ids) and all(
            artifacts[item]["status"] in ACTIVE_COVERAGE_STATUSES for item in release_ids
        )
        assured_targets = set(release_ids) | set(requirements)
        operations_ids = sorted(
            {
                relation["source"]
                for target in assured_targets
                for relation in inbound.get(target, [])
                if relation["relation"] == "assures"
                and artifacts.get(relation["source"], {}).get("type") == "operating_contract"
            }
        )
        operations_active = bool(operations_ids) and all(
            artifacts[item]["status"] in ACTIVE_COVERAGE_STATUSES for item in operations_ids
        )
        evidence_paths = evidence_by_work_order.get(work_order["id"], [])
        verification_record_ids = sorted(
            {
                relation["source"]
                for relation in inbound.get(work_order["id"], [])
                if relation["relation"] == "verifies_work_order"
                and artifacts.get(relation["source"], {}).get("type") == "verification_record"
                and artifacts[relation["source"]]["status"] in {"verified", "released"}
            }
        )
        release_record_ids = sorted(
            {
                relation["source"]
                for relation in inbound.get(work_order["id"], [])
                if relation["relation"] == "releases_work"
                and artifacts.get(relation["source"], {}).get("type") == "release_record"
                and artifacts[relation["source"]]["status"] in {"ready", "released"}
            }
        )
        released_record_ids = [
            artifact_id for artifact_id in release_record_ids if artifacts[artifact_id]["status"] == "released"
        ]

        gates = [
            _gate(
                "G0",
                "Intent ready",
                [
                    _condition("intent_chain", "Approved intent is reachable", "satisfied" if intents else "unsatisfied", intents),
                    _condition(
                        "intent_quality",
                        "Outcome stated with a success measure",
                        "satisfied" if measured_intents else "not_assessable",
                        measured_intents,
                    ),
                ],
            ),
            _gate(
                "G1",
                "Requirement ready",
                [
                    _condition("requirements_declared", "In-scope requirements are active", "satisfied" if requirements_active else "unsatisfied", requirements),
                    _condition("requirement_metadata", "Requirement metadata has no validator error", "satisfied" if requirements_clean else "unsatisfied", requirements),
                    _condition("requirement_semantics", "Domain meaning and examples are adequate", "not_assessable"),
                ],
            ),
            _gate(
                "G2",
                "Engineering ready",
                [
                    _condition("governing_contracts", "Specification, architecture, and verification are active", "satisfied" if governing_active else "unsatisfied", required_contracts),
                    _condition("work_authorization", "Work order is active", "satisfied" if work_order["status"] in ACTIVE_WORK_ORDER_STATUSES else "unsatisfied", [work_order["id"]]),
                ],
            ),
            _gate(
                "G3",
                "Implementation complete",
                [
                    _condition("implementation_status", "Work order records implementation completion", "satisfied" if work_order["status"] in IMPLEMENTED_OR_LATER_STATUSES else "unsatisfied", [work_order["id"]]),
                    _condition("verification_evidence", "Work-order evidence is retained", "satisfied" if evidence_paths else "unsatisfied", evidence_paths),
                    _condition(
                        "verified_revision",
                        "A verified record binds the candidate commit",
                        "satisfied" if verification_record_ids else "unsatisfied" if revision_policy["required_for_verified_work"] else "not_assessable",
                        verification_record_ids,
                    ),
                    _condition("repository_checks", "All required implementation checks passed", "not_assessable"),
                ],
            ),
            _gate(
                "G4",
                "Release ready",
                [
                    _condition("release_contract", "An active release contract gates the work", "satisfied" if release_active else "unsatisfied", release_ids),
                    _condition(
                        "release_revision",
                        "A release record identifies the verified commit",
                        "satisfied" if release_record_ids else "unsatisfied" if revision_policy["required_for_release"] else "not_assessable",
                        release_record_ids,
                    ),
                    _condition("promotion_evidence", "Security, provenance, compatibility, and rollback evidence passed", "not_assessable"),
                ],
            ),
            _gate(
                "G5",
                "Operationally accepted",
                [
                    _condition("operating_contract", "An active operating contract assures the chain", "satisfied" if operations_active else "unsatisfied", operations_ids),
                    _condition(
                        "released_revision",
                        "An authorized release record binds the released commit",
                        "satisfied" if released_record_ids else "unsatisfied" if revision_policy["required_for_release"] and work_order["status"] == "released" else "not_assessable",
                        released_record_ids,
                    ),
                    _condition("observation_window", "Post-release operating evidence is within bounds", "not_assessable"),
                ],
            ),
        ]
        readiness.append(
            {
                "work_order": work_order["id"],
                "status": work_order["status"],
                "gates": gates,
            }
        )
    return sorted(readiness, key=lambda item: item["work_order"])


def build_revision_provenance(
    normalized_artifacts: Sequence[dict[str, Any]],
    relations: Sequence[dict[str, Any]],
    observed_revision: str | None,
    commit_availability: dict[str, bool | None],
) -> list[dict[str, Any]]:
    relations_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    relations_by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in relations:
        if relation["target_exists"]:
            relations_by_source[relation["source"]].append(relation)
            relations_by_target[relation["target"]].append(relation)
    result: list[dict[str, Any]] = []
    for artifact in normalized_artifacts:
        if artifact["type"] not in {"verification_record", "release_record"}:
            continue
        commit = artifact.get("commit")
        match_state = (
            "not_assessable"
            if not commit or not observed_revision
            else "exact"
            if commit == observed_revision
            else "different"
        )
        relation_names = {relation["relation"]: [] for relation in relations_by_source[artifact["id"]]}
        for relation in relations_by_source[artifact["id"]]:
            relation_names[relation["relation"]].append(relation["target"])
        work_relation = "verifies_work_order" if artifact["type"] == "verification_record" else "releases_work"
        supersedes = sorted(
            {
                relation["source"]
                for relation in relations_by_target[artifact["id"]]
                if relation["relation"] == "superseded_by"
            }
        )
        lifecycle_class = (
            "historical"
            if artifact["status"] == "superseded"
            else "active_candidate"
            if artifact["status"] == "ready"
            else "assured"
        )
        result.append(
            {
                "id": artifact["id"],
                "kind": "verification" if artifact["type"] == "verification_record" else "release",
                "status": artifact["status"],
                "commit": commit,
                "git_object_format": artifact.get("git_object_format"),
                "observed_revision": observed_revision,
                "match_state": match_state,
                "commit_available": commit_availability.get(commit),
                "work_orders": sorted(set(relation_names.get(work_relation, []))),
                "verification_records": sorted(set(relation_names.get("includes_verification", []))),
                "contracts": sorted(set(relation_names.get("conforms_to", []) + relation_names.get("satisfies", []))),
                "superseded_by": sorted(set(relation_names.get("superseded_by", []))),
                "supersedes": supersedes,
                "superseded_at": artifact.get("superseded_at"),
                "supersession_authorized_by": artifact.get("supersession_authorized_by"),
                "prepared_at": artifact.get("prepared_at"),
                "prepared_by": artifact.get("prepared_by"),
                "decided_at": artifact.get("verified_at") or artifact.get("released_at"),
                "decided_by": artifact.get("verified_by") or artifact.get("authorized_by"),
                "lifecycle_class": lifecycle_class,
                "version": artifact.get("version"),
                "tag": artifact.get("tag"),
                "authority": "declared",
            }
        )
    return sorted(result, key=lambda item: (item["kind"], item["id"]))


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _sanitize_treatment(
    value: Any,
    dimensions: Sequence[dict[str, Any]],
    repository_root: Path,
    issues: list[str],
    label: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        issues.append(f"treatment '{label}' must be an object")
        value = {}
    raw_scores = value.get("scores", {})
    if not isinstance(raw_scores, dict):
        issues.append(f"treatment '{label}' scores must be an object")
        raw_scores = {}
    scores: dict[str, int | float | None] = {}
    for dimension in dimensions:
        dimension_id = dimension["id"]
        score = raw_scores.get(dimension_id)
        if score is None:
            scores[dimension_id] = None
        elif not _is_number(score) or score < 0 or score > dimension["maximum"]:
            issues.append(f"treatment '{label}' score '{dimension_id}' is outside 0..{dimension['maximum']}")
            scores[dimension_id] = None
        else:
            scores[dimension_id] = score

    sanitized: dict[str, Any] = {"scores": scores}
    for measure in EXPERIMENT_MEASURES:
        raw = value.get(measure)
        if raw is None:
            sanitized[measure] = None
        elif not _is_number(raw) or raw < 0:
            issues.append(f"treatment '{label}' measure '{measure}' must be a non-negative number or null")
            sanitized[measure] = None
        else:
            sanitized[measure] = raw

    evidence: list[str] = []
    raw_evidence = value.get("evidence", [])
    if not isinstance(raw_evidence, list):
        issues.append(f"treatment '{label}' evidence must be an array")
    else:
        for entry in raw_evidence:
            safe = _safe_repository_reference(entry, repository_root)
            if safe is None:
                issues.append(f"treatment '{label}' contains an unsafe evidence path")
            else:
                evidence.append(safe)
    sanitized["evidence"] = sorted(set(evidence))
    return sanitized


def _import_experiment(path: Path, repository_root: Path) -> dict[str, Any]:
    relative_path = repository_relative(path, repository_root)
    issues: list[str] = []
    try:
        if path.stat().st_size > MAX_EXPERIMENT_BYTES:
            raise GenerationError("experiment result exceeds the one-megabyte input limit")
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError, GenerationError) as exc:
        return {
            "path": relative_path,
            "status": "invalid",
            "issues": [str(exc)],
        }
    if not isinstance(payload, dict):
        return {
            "path": relative_path,
            "status": "invalid",
            "issues": ["experiment result must be a JSON object"],
        }

    def required_string(field: str) -> str | None:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            issues.append(f"field '{field}' must be a non-empty string")
            return None
        return value.strip()

    schema = required_string("schema")
    if schema is not None and schema != EXPERIMENT_SCHEMA:
        issues.append(f"unsupported experiment schema '{schema}'")
    trial_id = required_string("trial_id")
    protocol = required_string("protocol")
    base_revision = required_string("base_revision")
    work_order = required_string("work_order")
    evaluator = required_string("evaluator")

    rubric = payload.get("rubric")
    dimensions: list[dict[str, Any]] = []
    rubric_id: str | None = None
    if not isinstance(rubric, dict):
        issues.append("field 'rubric' must be an object")
    else:
        raw_rubric_id = rubric.get("id")
        if isinstance(raw_rubric_id, str) and raw_rubric_id.strip():
            rubric_id = raw_rubric_id.strip()
        else:
            issues.append("field 'rubric.id' must be a non-empty string")
        raw_dimensions = rubric.get("dimensions")
        if not isinstance(raw_dimensions, list) or not raw_dimensions:
            issues.append("field 'rubric.dimensions' must be a non-empty array")
        else:
            seen_dimensions: set[str] = set()
            for index, dimension in enumerate(raw_dimensions):
                if not isinstance(dimension, dict):
                    issues.append(f"rubric dimension {index} must be an object")
                    continue
                dimension_id = dimension.get("id")
                maximum = dimension.get("maximum")
                if not isinstance(dimension_id, str) or not dimension_id.strip():
                    issues.append(f"rubric dimension {index} has an invalid id")
                    continue
                clean_id = dimension_id.strip()
                if clean_id in seen_dimensions:
                    issues.append(f"rubric dimension '{clean_id}' is duplicated")
                    continue
                if not _is_number(maximum) or maximum <= 0:
                    issues.append(f"rubric dimension '{clean_id}' has an invalid maximum")
                    continue
                seen_dimensions.add(clean_id)
                dimensions.append({"id": clean_id, "maximum": maximum})

    treatments = payload.get("treatments")
    if not isinstance(treatments, dict):
        issues.append("field 'treatments' must be an object")
        treatments = {}
    sanitized_treatments = {
        label: _sanitize_treatment(treatments.get(label), dimensions, repository_root, issues, label)
        for label in ("baseline", "harness")
    }
    result = {
        "path": relative_path,
        "status": "valid" if not issues else "invalid",
        "issues": sorted(set(issues)),
        "schema": schema,
        "trial_id": trial_id,
        "protocol": protocol,
        "base_revision": base_revision,
        "work_order": work_order,
        "rubric": {"id": rubric_id, "dimensions": dimensions},
        "treatments": sanitized_treatments,
        "evaluator": evaluator,
    }
    return result


def import_experiments(repository_root: Path) -> list[dict[str, Any]]:
    experiment_root = repository_root / DEFAULT_EXPERIMENT_ROOT
    if not experiment_root.exists():
        return []
    return sorted(
        (_import_experiment(path, repository_root) for path in experiment_root.glob("*.json") if path.is_file()),
        key=lambda item: (item.get("trial_id") or "", item["path"]),
    )


def build_snapshot(
    repository_root: Path,
    artifact_root: Path,
    report: ValidationReport,
) -> dict[str, Any]:
    content_budget = ContentBudget()
    normalized_artifacts = normalize_artifacts(report, repository_root, content_budget)
    relations = sorted(
        [
            *build_declared_relations(report.artifacts),
            *build_architecture_transitive_relations(report.artifacts),
        ],
        key=lambda item: (
            item["source"],
            item["relation"],
            item["target"],
            item["authority"],
        ),
    )
    diagnostics = normalize_diagnostics(report, normalized_artifacts)
    observed_revision = git_revision(repository_root)
    revision_policy = load_revision_policy(repository_root)
    commit_availability = git_commit_availability(
        repository_root,
        [artifact.get("commit") for artifact in normalized_artifacts if isinstance(artifact.get("commit"), str)],
    )
    revision_provenance = build_revision_provenance(
        normalized_artifacts,
        relations,
        observed_revision,
        commit_availability,
    )
    evidence_by_work_order = discover_evidence(repository_root)
    evidence_documents = build_evidence_documents(
        report,
        repository_root,
        evidence_by_work_order,
        content_budget,
    )
    evidence = [
        {"work_order": work_order, "paths": paths}
        for work_order, paths in sorted(evidence_by_work_order.items())
    ]
    findings = build_findings(
        normalized_artifacts,
        relations,
        diagnostics,
        evidence_by_work_order,
        revision_provenance,
        revision_policy,
    )
    return {
        "schema": SNAPSHOT_SCHEMA,
        "finding_rules_version": FINDING_RULES_VERSION,
        "quality_gates_version": QUALITY_GATES_VERSION,
        "repository": {
            "name": repository_root.name,
            "revision": observed_revision,
            "git_object_format": git_object_format(repository_root),
            "artifact_root": repository_relative(artifact_root, repository_root),
            "source_url": git_source_url(repository_root),
            "valid": report.valid,
        },
        "artifacts": normalized_artifacts,
        "relations": relations,
        "diagnostics": diagnostics,
        "findings": findings,
        "coverage": build_coverage(normalized_artifacts, relations),
        "readiness": build_readiness(
            normalized_artifacts,
            relations,
            diagnostics,
            evidence_by_work_order,
            revision_policy,
        ),
        "revision_provenance": revision_provenance,
        "revision_policy": revision_policy,
        "experiments": import_experiments(repository_root),
        "evidence": evidence,
        "evidence_documents": evidence_documents,
    }
