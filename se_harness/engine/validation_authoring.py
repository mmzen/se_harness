"""Small authoring hints and checks for supplied metadata and references."""

from __future__ import annotations

import re
from pathlib import Path
from se_harness.artifact_layout import ID_PATTERN
from se_harness.codes import E_AUT_001, E_AUT_002, W_AUT_011, W_AUT_016, W_AUT_019, W_AUT_020, W_AUT_022
from se_harness.front_matter import body_sections
from se_harness.engine.validation_core import Artifact, Diagnostic, add_error, display_path

SPECIFICATION_RULE_SECTIONS = ("Rules", "Behavioral rules")
RULE_IDENTIFIER = re.compile(r"\b[A-Z][A-Z0-9]*-[A-Z0-9]+-\d{3}\b")
_RULE_LEAD = re.compile(r"^\*\*([A-Z][A-Z0-9]*-[A-Z0-9]+-\d{3})(?:\s*\([^)]*\))?\.?\*\*\.?\s*")
VERIFICATION_METHODS = ("test", "analysis", "inspection", "demonstration")
REQUIREMENT_PRIORITIES = ("must", "should", "could")


def specification_rules(body: str) -> list[tuple[str | None, str]]:
    """SPEC-TCM-006 TCM-RFS-006: the rule paragraphs of a specification.

    Each paragraph of the first present rules section (`Rules`, or `Behavioral rules`
    for a legacy file) is one rule: (identifier, sentence) when it opens with a bold
    rule identifier, (None, text) when it does not."""

    if not isinstance(body, str):
        return []
    sections = body_sections(body)
    section = next((sections[name] for name in SPECIFICATION_RULE_SECTIONS if name in sections), None)
    if section is None:
        return []
    rules: list[tuple[str | None, str]] = []
    # A paragraph is one rule; a numbered or bulleted list item is one paragraph of
    # its own, so a legacy numbered list reads as one rule per item.
    for paragraph in re.split(r"\n\s*\n|\n(?=\s*(?:\d+\.|[-*])\s)", section):
        text = " ".join(line.strip() for line in paragraph.strip().split("\n") if line.strip())
        if not text:
            continue
        lead = _RULE_LEAD.match(text)
        if lead is None:
            rules.append((None, text))
        else:
            rules.append((lead.group(1), text[lead.end():].strip()))
    return rules


def coverage_rows(body: str) -> list[tuple[str, list[str]]] | None:
    """SPEC-TCM-006 TCM-RFS-015: the rows of the `Coverage` table, or None when absent."""

    if not isinstance(body, str):
        return None
    section = body_sections(body).get("Coverage")
    if section is None:
        return None
    rows: list[tuple[str, list[str]]] = []
    for line in section.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= set("-: ") or cells[0].lower() == "requirement":
            continue
        rows.append((cells[0].strip("`"), RULE_IDENTIFIER.findall(cells[1])))
    return rows


def validate_authoring(artifacts: list[Artifact], report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic], list[Diagnostic]]:
    """Check supplied fields; offer draft hints without enforcing a writing style."""
    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    advisories: list[Diagnostic] = []
    catalog = {artifact.artifact_id for artifact in artifacts if artifact.artifact_id != "<unknown>"}
    summaries = {
        "intent": ("outcome", W_AUT_011),
        "capability": ("ability", W_AUT_016),
        "specification": ("contract", W_AUT_019),
    }
    for artifact in artifacts:
        path = display_path(artifact.path, report_root)
        if artifact.artifact_type in summaries:
            field, code = summaries[artifact.artifact_type]
            value = artifact.metadata.get(field)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                add_error(errors, artifact, report_root, E_AUT_002, f"{field} must be a non-empty string when present", plane="structure")
            if value is None and artifact.status == "draft":
                advisories.append(Diagnostic(path, code, f"Add an {field} summary so the reader knows what this artifact delivers.", "maintenance"))
        if artifact.artifact_type == "specification" and artifact.status == "draft":
            identifiers = [identifier for identifier, _ in specification_rules(artifact.body) if identifier]
            if len(identifiers) != len(set(identifiers)):
                advisories.append(Diagnostic(path, W_AUT_020, "A rule identifier is defined more than once; references would be ambiguous.", "maintenance"))
            for requirement, references in coverage_rows(artifact.body) or []:
                for identifier in references:
                    if identifier not in identifiers:
                        advisories.append(Diagnostic(path, W_AUT_022, f"Coverage row {requirement} names undefined rule {identifier}.", "maintenance"))
        if artifact.artifact_type != "requirement":
            continue
        method = artifact.metadata.get("verification_method")
        if isinstance(method, list):
            if not method or len(method) > len(VERIFICATION_METHODS) or any(not isinstance(item, str) for item in method) or len(set(method)) != len(method) or any(item not in VERIFICATION_METHODS for item in method):
                add_error(errors, artifact, report_root, E_AUT_001,
                    f"verification_method must list 1-4 distinct values from {', '.join(VERIFICATION_METHODS)}", plane="structure")
        notes = artifact.metadata.get("verification_notes")
        if notes is not None and (not isinstance(notes, str) or not notes.strip()):
            add_error(errors, artifact, report_root, E_AUT_002, "verification_notes must be a non-empty string when present", plane="structure")
        priority = artifact.metadata.get("priority")
        if priority is not None and priority not in REQUIREMENT_PRIORITIES:
            add_error(errors, artifact, report_root, E_AUT_002, f"priority must be one of {', '.join(REQUIREMENT_PRIORITIES)}", plane="structure")
        source = artifact.metadata.get("source")
        if source is not None:
            if not isinstance(source, str) or not source.strip():
                add_error(errors, artifact, report_root, E_AUT_002, "source must be a non-empty string when present", plane="structure")
            elif ID_PATTERN.fullmatch(source.strip()) is not None and source.strip() not in catalog:
                add_error(errors, artifact, report_root, E_AUT_002, f"source names an unknown artifact '{source.strip()}'", plane="structure")
        measure = artifact.metadata.get("measure")
        if measure is not None and (not isinstance(measure, str) or not measure.strip()):
            add_error(errors, artifact, report_root, E_AUT_002, "measure must be a non-empty string when present", plane="structure")
    return errors, warnings, advisories


def authoring_advisories(artifact: Artifact, report_root: Path | None = None) -> list[Diagnostic]:
    """Read the optional hints for one artifact as a draft. Hints do not grant or block approval."""
    draft = Artifact(path=artifact.path, metadata={**artifact.metadata, "status": "draft"}, body=artifact.body)
    _, _, advisories = validate_authoring([draft], report_root or artifact.path.parent)
    return sorted(set(advisories))
