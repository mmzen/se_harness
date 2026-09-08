"""The authoring seam: the reader-first budgets and the authoring pass (SPEC-TCM-003 to SPEC-TCM-006).
"""

from __future__ import annotations

import re
from pathlib import Path

from se_harness.artifact_layout import ID_PATTERN
from se_harness.codes import (
    E_AUT_001,
    E_AUT_002,
    W_AUT_001,
    W_AUT_002,
    W_AUT_003,
    W_AUT_004,
    W_AUT_005,
    W_AUT_006,
    W_AUT_007,
    W_AUT_008,
    W_AUT_009,
    W_AUT_010,
    W_AUT_011,
    W_AUT_012,
    W_AUT_013,
    W_AUT_014,
    W_AUT_015,
    W_AUT_016,
    W_AUT_017,
    W_AUT_018,
    W_AUT_019,
    W_AUT_020,
    W_AUT_021,
    W_AUT_022,
    W_AUT_023,
)
from se_harness.front_matter import body_sections
from se_harness.engine.validation_core import Artifact, Diagnostic, add_error, display_path


AUTHORING_OPENERS = ("THE SYSTEM SHALL", "WHEN ", "WHILE ", "IF ", "WHERE ")

AUTHORING_NAMED_SUBJECT = re.compile(r"^THE [A-Z][A-Za-z0-9 _-]{0,60} SHALL\b")

#: SPEC-TCM-003 TCM-RFR-003: the reader-first budgets, counted with code spans removed.
AUTHORING_STATEMENT_LIMIT = 30  # words

AUTHORING_BODY_LIMIT = 250  # words

AUTHORING_WHY_WORD_LIMIT = 120

AUTHORING_WHY_SENTENCE_LIMIT = 5

AUTHORING_SENTENCE_LIMIT = 25  # words

AUTHORING_CODE_IDENTIFIER_LIMIT = 3

AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT = 2

#: SPEC-TCM-004 TCM-RFI-002 to TCM-RFI-004: the reader-first intent budgets and the
#: acceptance vocabulary that marks a success-measure row as an acceptance check.
INTENT_OUTCOME_LIMIT = 30  # words

INTENT_BODY_LIMIT = 200  # words

INTENT_PROBLEM_WORD_LIMIT = 120

INTENT_PROBLEM_SENTENCE_LIMIT = 5

INTENT_CODE_IDENTIFIER_LIMIT = 2

#: SPEC-TCM-005 TCM-RFC-002 and TCM-RFC-003: the reader-first capability budgets. The
#: shared codes (W-AUT-005, -007, -008, -009) fire with these constants on a capability.
CAPABILITY_ABILITY_LIMIT = 30  # words

CAPABILITY_BODY_LIMIT = 150  # words

CAPABILITY_NEED_WORD_LIMIT = 60

CAPABILITY_NEED_SENTENCE_LIMIT = 3

CAPABILITY_CODE_IDENTIFIER_LIMIT = 2

#: SPEC-TCM-006 TCM-RFS-004 and TCM-RFS-006 to TCM-RFS-013: the reader-first specification
#: budgets and the rule grammar. The shared codes W-AUT-005, W-AUT-007 and W-AUT-009 fire
#: with these constants on a specification draft; W-AUT-008 never does (TCM-RFS-013).
SPECIFICATION_CONTRACT_LIMIT = 30  # words

SPECIFICATION_RULE_LIMIT = 30  # words, one sentence

SPECIFICATION_PROSE_LIMIT = 300  # words outside Rules, Failure behaviour, Examples and Coverage

SPECIFICATION_RULE_SECTIONS = ("Rules", "Behavioral rules")

SPECIFICATION_UNBUDGETED_SECTIONS = frozenset({"Rules", "Behavioral rules", "Failure behaviour", "Examples", "Coverage"})

SPECIFICATION_LEGACY_HEADINGS = ("Behavioral rules", "Open decisions", "Approval")

SPECIFICATION_KEYWORDS = re.compile(r"\b(MUST NOT|MUST|SHALL NOT|SHALL|MAY|refuses)\b")

RULE_IDENTIFIER = re.compile(r"\b[A-Z][A-Z0-9]*-[A-Z0-9]+-\d{3}\b")

_RULE_LEAD = re.compile(r"^\*\*([A-Z][A-Z0-9]*-[A-Z0-9]+-\d{3})(?:\s*\([^)]*\))?\.?\*\*\.?\s*")

_LEGACY_REQUIREMENT_LIST = ("Candidate requirements", "Derived requirements")

_REPOSITORY_PATH_SPAN = re.compile(r"`[^`\s]*/[^`\s]*\.[A-Za-z0-9]{1,6}(?::\d+(?:-\d+)?)?`")

_LINE_RANGE_SPAN = re.compile(r"`[^`]*:\d+(?:-\d+)?`")

_ACCEPTANCE_VOCABULARY = re.compile(
    r"\b(CI|tests?|validator|validate|verification|implementation review|acceptance run|regression run|transaction)\b", re.I
)


_CODE_SPAN = re.compile(r"`[^`]*`")

_FENCE = re.compile(r"```.*?```", re.S)

_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\-]*")

_SENTENCE_END = re.compile(r"[.!?](?:\s|$)")

_EVALUATION_EVENT = re.compile(r"^WHEN\s+[^,]*\b(is validated|is evaluated|is checked|runs|is run)\b[^,]*,", re.I)


def _prose(text: str) -> str:
    return _CODE_SPAN.sub(" ", _FENCE.sub(" ", text))


def _word_count(text: str) -> int:
    return len(_WORD.findall(_prose(text)))


def sentences(text: str) -> list[str]:
    prose = " ".join(line.strip() for line in _prose(text).split("\n") if line.strip() and not line.strip().startswith(("|", "#", "**Given", "**When", "**Then")))
    return [item.strip() for item in _SENTENCE_END.split(prose) if item.strip()]


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


VERIFICATION_METHODS = ("test", "analysis", "inspection", "demonstration")

REQUIREMENT_PRIORITIES = ("must", "should", "could")


def validate_authoring(artifacts: list[Artifact], report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic], list[Diagnostic]]:
    """Requirement-writing rules: statement shape signals, vocabulary, and optional attributes (SPEC-AUT-001).

    The statement and vocabulary signals are advisories (SPEC-AUT-002, AUT-ADV-001):
    they help the author of a draft and are raised only while the requirement is in
    `draft` (AUT-ADV-002). Errors and warnings are unchanged.
    """

    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    advisories: list[Diagnostic] = []
    catalog = {artifact.artifact_id for artifact in artifacts if artifact.artifact_id != "<unknown>"}
    for artifact in artifacts:
        if artifact.artifact_type == "intent":
            intent_errors, intent_advisories = _intent_authoring(artifact, report_root)
            errors.extend(intent_errors)
            advisories.extend(intent_advisories)
            continue
        if artifact.artifact_type == "capability":
            capability_errors, capability_advisories = _capability_authoring(artifact, report_root)
            errors.extend(capability_errors)
            advisories.extend(capability_advisories)
            continue
        if artifact.artifact_type == "specification":
            specification_errors, specification_advisories = _specification_authoring(artifact, report_root)
            errors.extend(specification_errors)
            advisories.extend(specification_advisories)
            continue
        if artifact.artifact_type != "requirement":
            continue
        draft = artifact.status == "draft"
        statement = artifact.metadata.get("statement")
        if isinstance(statement, str) and statement.strip() and draft:
            text = statement.strip()
            opener_ok = text.startswith(AUTHORING_OPENERS) or AUTHORING_NAMED_SUBJECT.match(text) is not None
            if text.startswith("IF ") and " THEN " not in text:
                opener_ok = False
            if not opener_ok:
                advisories.append(Diagnostic(display_path(artifact.path, report_root), W_AUT_001,
                    "statement does not open with one of the five shapes (THE SYSTEM SHALL, WHEN, WHILE, IF ... THEN, WHERE)", "maintenance"))
            shall_count = len(re.findall(r"\bSHALL\b", text))
            if shall_count > 1:
                advisories.append(Diagnostic(display_path(artifact.path, report_root), W_AUT_002,
                    f"statement carries {shall_count} SHALL obligations; one requirement states one obligation", "maintenance"))
            statement_words = _word_count(text)
            if statement_words > AUTHORING_STATEMENT_LIMIT:
                advisories.append(Diagnostic(display_path(artifact.path, report_root), W_AUT_003,
                    f"statement is {statement_words} words; the budget is {AUTHORING_STATEMENT_LIMIT}", "maintenance"))
            if _EVALUATION_EVENT.match(text) and " AND " not in text.split(",", 1)[0].upper():
                advisories.append(Diagnostic(display_path(artifact.path, report_root), W_AUT_010,
                    "statement opens WHEN on an event of evaluation with no other condition; an invariant reads THE SYSTEM SHALL", "maintenance"))
        if draft:
            advisories.extend(_reader_first_advisories(artifact, report_root))
        method = artifact.metadata.get("verification_method")
        if isinstance(method, str):
            if method.strip() and draft:
                advisories.append(Diagnostic(display_path(artifact.path, report_root), W_AUT_004,
                    "verification_method is a free-text string; the closed vocabulary is an array of test, analysis, inspection, demonstration", "maintenance"))
        elif isinstance(method, list):
            if not method or len(method) > len(VERIFICATION_METHODS) or len(set(method)) != len(method) or any(item not in VERIFICATION_METHODS for item in method):
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


def _reader_first_advisories(artifact: Artifact, report_root: Path) -> list[Diagnostic]:
    """SPEC-TCM-003 TCM-RFR-003: the body budgets of a requirement draft, advisories only."""

    body = artifact.body if isinstance(artifact.body, str) else ""
    path = display_path(artifact.path, report_root)
    found: list[Diagnostic] = []
    body_words = _word_count(body)
    if body_words > AUTHORING_BODY_LIMIT:
        found.append(Diagnostic(path, W_AUT_005, f"body is {body_words} words; the budget is {AUTHORING_BODY_LIMIT}", "maintenance"))
    sections = body_sections(body)
    why = sections.get("Why")
    if why is not None:
        why_words = _word_count(why)
        why_sentences = len(sentences(why))
        if why_words > AUTHORING_WHY_WORD_LIMIT or why_sentences > AUTHORING_WHY_SENTENCE_LIMIT:
            found.append(Diagnostic(path, W_AUT_006,
                f"Why is {why_words} words in {why_sentences} sentences; the budget is {AUTHORING_WHY_WORD_LIMIT} words or {AUTHORING_WHY_SENTENCE_LIMIT} sentences", "maintenance"))
    longest = max((len(_WORD.findall(sentence)) for sentence in sentences(body)), default=0)
    if longest > AUTHORING_SENTENCE_LIMIT:
        found.append(Diagnostic(path, W_AUT_007, f"a body sentence is {longest} words; the budget is {AUTHORING_SENTENCE_LIMIT}", "maintenance"))
    identifiers = len(_CODE_SPAN.findall(_FENCE.sub(" ", body)))
    if identifiers > AUTHORING_CODE_IDENTIFIER_LIMIT:
        found.append(Diagnostic(path, W_AUT_008,
            f"body cites {identifiers} code identifiers; the budget is {AUTHORING_CODE_IDENTIFIER_LIMIT}, the rest belongs in the specification", "maintenance"))
    plain = sections.get("In plain words")
    if body.strip() and plain is None:
        found.append(Diagnostic(path, W_AUT_009, "body has no In plain words section; the reader-first shape opens with one or two plain sentences", "maintenance"))
    elif plain is not None and (not plain.strip() or len(sentences(plain)) > AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT):
        found.append(Diagnostic(path, W_AUT_009,
            f"In plain words has {len(sentences(plain))} sentences; the budget is {AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT}", "maintenance"))
    return found


def _success_measure_rows(section: str) -> list[list[str]] | None:
    """The data rows of a Success measures table as cell lists; None when the table is malformed."""

    rows: list[list[str]] = []
    header_seen = False
    for line in section.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not header_seen:
            header_seen = True
            continue
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        if len(cells) < 4:
            return None
        rows.append(cells)
    return rows


def _intent_authoring(artifact: Artifact, report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic]]:
    """SPEC-TCM-004 TCM-RFI-002 to TCM-RFI-004: the outcome field and the intent draft advisories."""

    errors: list[Diagnostic] = []
    found: list[Diagnostic] = []
    outcome = artifact.metadata.get("outcome")
    if outcome is not None and (not isinstance(outcome, str) or not outcome.strip()):
        add_error(errors, artifact, report_root, E_AUT_002, "outcome must be a non-empty string when present", plane="structure")
    if artifact.status != "draft":
        return errors, found
    path = display_path(artifact.path, report_root)
    if not isinstance(outcome, str) or not outcome.strip():
        found.append(Diagnostic(path, W_AUT_011, "intent has no outcome; one sentence names who can do or observe what after delivery", "maintenance"))
    else:
        outcome_words = _word_count(outcome)
        if outcome_words > INTENT_OUTCOME_LIMIT:
            found.append(Diagnostic(path, W_AUT_011, f"outcome is {outcome_words} words; the budget is {INTENT_OUTCOME_LIMIT}", "maintenance"))
        outcome_spans = len(_CODE_SPAN.findall(outcome))
        if outcome_spans:
            found.append(Diagnostic(path, W_AUT_011, f"outcome cites {outcome_spans} code identifiers; the outcome names no solution", "maintenance"))
    body = artifact.body if isinstance(artifact.body, str) else ""
    body_words = _word_count(body)
    if body_words > INTENT_BODY_LIMIT:
        found.append(Diagnostic(path, W_AUT_005, f"body is {body_words} words; the budget is {INTENT_BODY_LIMIT}", "maintenance"))
    sections = body_sections(body)
    problem = sections.get("Problem")
    if problem is not None:
        problem_words = _word_count(problem)
        problem_sentences = len(sentences(problem))
        if problem_words > INTENT_PROBLEM_WORD_LIMIT or problem_sentences > INTENT_PROBLEM_SENTENCE_LIMIT:
            found.append(Diagnostic(path, W_AUT_012,
                f"Problem is {problem_words} words in {problem_sentences} sentences; the budget is {INTENT_PROBLEM_WORD_LIMIT} words or {INTENT_PROBLEM_SENTENCE_LIMIT} sentences", "maintenance"))
    longest = max((len(_WORD.findall(sentence)) for sentence in sentences(body)), default=0)
    if longest > AUTHORING_SENTENCE_LIMIT:
        found.append(Diagnostic(path, W_AUT_007, f"a body sentence is {longest} words; the budget is {AUTHORING_SENTENCE_LIMIT}", "maintenance"))
    unfenced = _FENCE.sub(" ", body)
    identifiers = len(_CODE_SPAN.findall(unfenced))
    if identifiers > INTENT_CODE_IDENTIFIER_LIMIT:
        found.append(Diagnostic(path, W_AUT_008,
            f"body cites {identifiers} code identifiers; the budget is {INTENT_CODE_IDENTIFIER_LIMIT}, the evidence belongs in a note, an RCA or an ADR", "maintenance"))
    citations = len({span for span in _CODE_SPAN.findall(unfenced) if _REPOSITORY_PATH_SPAN.fullmatch(span) or _LINE_RANGE_SPAN.fullmatch(span)})
    if citations:
        found.append(Diagnostic(path, W_AUT_015,
            f"body cites {citations} repository paths or source line ranges; evidence is cited by link to a note, an RCA or an ADR, not quoted", "maintenance"))
    plain = sections.get("In plain words")
    if body.strip() and plain is None:
        found.append(Diagnostic(path, W_AUT_009, "body has no In plain words section; the reader-first shape opens with one or two plain sentences", "maintenance"))
    elif plain is not None and (not plain.strip() or len(sentences(plain)) > AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT):
        found.append(Diagnostic(path, W_AUT_009,
            f"In plain words has {len(sentences(plain))} sentences; the budget is {AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT}", "maintenance"))
    measures = sections.get("Success measures")
    if measures is not None:
        rows = _success_measure_rows(measures)
        if not rows:
            found.append(Diagnostic(path, W_AUT_014, "Success measures has no row; a success measure is what an operator can count or time after delivery", "maintenance"))
        else:
            for cells in rows:
                match = _ACCEPTANCE_VOCABULARY.search(cells[3])
                if match is not None:
                    found.append(Diagnostic(path, W_AUT_013,
                        f"success measure '{cells[0]}' is observed by {match.group(0)}; an acceptance check belongs in the verification contract", "maintenance"))
    return errors, found


def _capability_authoring(artifact: Artifact, report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic]]:
    """SPEC-TCM-005 TCM-RFC-002 and TCM-RFC-003: the ability field and the capability draft advisories."""

    errors: list[Diagnostic] = []
    found: list[Diagnostic] = []
    ability = artifact.metadata.get("ability")
    if ability is not None and (not isinstance(ability, str) or not ability.strip()):
        add_error(errors, artifact, report_root, E_AUT_002, "ability must be a non-empty string when present", plane="structure")
    if artifact.status != "draft":
        return errors, found
    path = display_path(artifact.path, report_root)
    if not isinstance(ability, str) or not ability.strip():
        found.append(Diagnostic(path, W_AUT_016, "capability has no ability; one sentence names who can do what under which conditions", "maintenance"))
    else:
        ability_words = _word_count(ability)
        lowered = {word.lower() for word in _WORD.findall(_prose(ability))}
        if ability_words > CAPABILITY_ABILITY_LIMIT:
            found.append(Diagnostic(path, W_AUT_016, f"ability is {ability_words} words; the budget is {CAPABILITY_ABILITY_LIMIT}", "maintenance"))
        if "can" not in lowered:
            found.append(Diagnostic(path, W_AUT_016, "ability does not say what the actor can do; the sentence is actor, can, achievement, under conditions", "maintenance"))
        if "under" not in lowered:
            found.append(Diagnostic(path, W_AUT_016, "ability names no condition; say under which conditions the actor can do it", "maintenance"))
        ability_spans = len(_CODE_SPAN.findall(ability))
        if ability_spans:
            found.append(Diagnostic(path, W_AUT_016, f"ability cites {ability_spans} code identifiers; the ability names what an actor can do, not how", "maintenance"))
    body = artifact.body if isinstance(artifact.body, str) else ""
    body_words = _word_count(body)
    if body_words > CAPABILITY_BODY_LIMIT:
        found.append(Diagnostic(path, W_AUT_005, f"body is {body_words} words; the budget is {CAPABILITY_BODY_LIMIT}", "maintenance"))
    sections = body_sections(body)
    need = sections.get("Actor and need")
    if need is not None:
        need_words = _word_count(need)
        need_sentences = len(sentences(need))
        if need_words > CAPABILITY_NEED_WORD_LIMIT or need_sentences > CAPABILITY_NEED_SENTENCE_LIMIT:
            found.append(Diagnostic(path, W_AUT_017,
                f"Actor and need is {need_words} words in {need_sentences} sentences; the budget is {CAPABILITY_NEED_WORD_LIMIT} words or {CAPABILITY_NEED_SENTENCE_LIMIT} sentences", "maintenance"))
    longest = max((len(_WORD.findall(sentence)) for sentence in sentences(body)), default=0)
    if longest > AUTHORING_SENTENCE_LIMIT:
        found.append(Diagnostic(path, W_AUT_007, f"a body sentence is {longest} words; the budget is {AUTHORING_SENTENCE_LIMIT}", "maintenance"))
    identifiers = len(_CODE_SPAN.findall(_FENCE.sub(" ", body)))
    if identifiers > CAPABILITY_CODE_IDENTIFIER_LIMIT:
        found.append(Diagnostic(path, W_AUT_008,
            f"body cites {identifiers} code identifiers; the budget is {CAPABILITY_CODE_IDENTIFIER_LIMIT}, the how belongs in the specification", "maintenance"))
    plain = sections.get("In plain words")
    if body.strip() and plain is None:
        found.append(Diagnostic(path, W_AUT_009, "body has no In plain words section; the reader-first shape opens with one or two plain sentences", "maintenance"))
    elif plain is not None and (not plain.strip() or len(sentences(plain)) > AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT):
        found.append(Diagnostic(path, W_AUT_009,
            f"In plain words has {len(sentences(plain))} sentences; the budget is {AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT}", "maintenance"))
    legacy = [heading for heading in sections if heading in _LEGACY_REQUIREMENT_LIST]
    if legacy:
        found.append(Diagnostic(path, W_AUT_018,
            f"body carries a {legacy[0]} list; the requirements that derive from a capability are read from the graph and shown by the Explorer", "maintenance"))
    return errors, found


def _specification_authoring(artifact: Artifact, report_root: Path) -> tuple[list[Diagnostic], list[Diagnostic]]:
    """SPEC-TCM-006 TCM-RFS-004 and TCM-RFS-007 to TCM-RFS-014: the contract field and the specification draft advisories."""

    errors: list[Diagnostic] = []
    found: list[Diagnostic] = []
    contract = artifact.metadata.get("contract")
    if contract is not None and (not isinstance(contract, str) or not contract.strip()):
        add_error(errors, artifact, report_root, E_AUT_002, "contract must be a non-empty string when present", plane="structure")
    if artifact.status != "draft":
        return errors, found
    path = display_path(artifact.path, report_root)
    # TCM-RFS-007: the contract sentence.
    if not isinstance(contract, str) or not contract.strip():
        found.append(Diagnostic(path, W_AUT_019, "specification has no contract; one sentence says what an implementation must do to conform", "maintenance"))
    else:
        contract_words = _word_count(contract)
        contract_sentences = len(sentences(contract))
        contract_spans = len(_CODE_SPAN.findall(contract))
        if contract_words > SPECIFICATION_CONTRACT_LIMIT:
            found.append(Diagnostic(path, W_AUT_019, f"contract is {contract_words} words; the budget is {SPECIFICATION_CONTRACT_LIMIT}", "maintenance"))
        if contract_sentences > 1:
            found.append(Diagnostic(path, W_AUT_019, f"contract is {contract_sentences} sentences; the budget is one", "maintenance"))
        if contract_spans:
            found.append(Diagnostic(path, W_AUT_019, f"contract cites {contract_spans} code identifiers; the contract says what conformance is, the rules say how", "maintenance"))
    body = artifact.body if isinstance(artifact.body, str) else ""
    sections = body_sections(body)
    # TCM-RFS-008 and TCM-RFS-009: rule identity and rule shape.
    rules = specification_rules(body)
    seen: set[str] = set()
    for identifier, text in rules:
        if identifier is None:
            found.append(Diagnostic(path, W_AUT_020, f"a rule opens with no identifier: {text[:60]!r}; every rule leads with <PREFIX>-<AREA>-NNN in bold", "maintenance"))
            continue
        if identifier in seen:
            found.append(Diagnostic(path, W_AUT_020, f"rule identifier {identifier} is defined twice; an identifier names one rule and is never reused", "maintenance"))
        seen.add(identifier)
        rule_words = _word_count(text)
        rule_sentences = len(sentences(text))
        if rule_words > SPECIFICATION_RULE_LIMIT:
            found.append(Diagnostic(path, W_AUT_021, f"rule {identifier} is {rule_words} words; the budget is {SPECIFICATION_RULE_LIMIT}", "maintenance"))
        if rule_sentences > 1:
            found.append(Diagnostic(path, W_AUT_021, f"rule {identifier} is {rule_sentences} sentences; a rule is one testable sentence", "maintenance"))
        if SPECIFICATION_KEYWORDS.search(_prose(text)) is None:
            found.append(Diagnostic(path, W_AUT_021, f"rule {identifier} carries no MUST, MUST NOT, SHALL, SHALL NOT, MAY or refuses; a rule is a sentence someone can fail", "maintenance"))
    # TCM-RFS-010: the coverage table against `specifies`.
    specifies = [item for item in artifact.metadata.get("relations", {}).get("specifies", []) if isinstance(item, str)] if isinstance(artifact.metadata.get("relations"), dict) else []
    rows = coverage_rows(body)
    if rows is None:
        found.append(Diagnostic(path, W_AUT_022, "body has no Coverage table; each specified requirement maps to the rule identifiers that meet it", "maintenance"))
    else:
        covered = {requirement for requirement, _ in rows}
        for requirement in specifies:
            if requirement not in covered:
                found.append(Diagnostic(path, W_AUT_022, f"Coverage has no row for {requirement}, which this specification specifies", "maintenance"))
        for requirement, identifiers in rows:
            for identifier in identifiers:
                if identifier not in seen:
                    found.append(Diagnostic(path, W_AUT_022, f"Coverage row {requirement} names {identifier}, which the rules section does not define", "maintenance"))
    # TCM-RFS-011: legacy headings.
    legacy = [heading for heading in sections if heading in SPECIFICATION_LEGACY_HEADINGS]
    if legacy:
        found.append(Diagnostic(path, W_AUT_023, f"body carries a {legacy[0]} heading; the reader-first shape names the section Rules and records decisions and approvals in their own artifacts", "maintenance"))
    # TCM-RFS-012: the shared budgets with specification constants; TCM-RFS-013: no W-AUT-008.
    prose = "\n".join(text for heading, text in sections.items() if heading not in SPECIFICATION_UNBUDGETED_SECTIONS)
    prose_words = _word_count(prose)
    if prose_words > SPECIFICATION_PROSE_LIMIT:
        found.append(Diagnostic(path, W_AUT_005, f"body prose outside the rules, failure, examples and coverage sections is {prose_words} words; the budget is {SPECIFICATION_PROSE_LIMIT}", "maintenance"))
    outside_rules = "\n".join(text for heading, text in sections.items() if heading not in SPECIFICATION_RULE_SECTIONS)
    longest = max((len(_WORD.findall(sentence)) for sentence in sentences(outside_rules)), default=0)
    if longest > AUTHORING_SENTENCE_LIMIT:
        found.append(Diagnostic(path, W_AUT_007, f"a body sentence is {longest} words; the budget is {AUTHORING_SENTENCE_LIMIT}", "maintenance"))
    plain = sections.get("In plain words")
    if body.strip() and plain is None:
        found.append(Diagnostic(path, W_AUT_009, "body has no In plain words section; the reader-first shape opens with one or two plain sentences", "maintenance"))
    elif plain is not None and (not plain.strip() or len(sentences(plain)) > AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT):
        found.append(Diagnostic(path, W_AUT_009,
            f"In plain words has {len(sentences(plain))} sentences; the budget is {AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT}", "maintenance"))
    return errors, found
