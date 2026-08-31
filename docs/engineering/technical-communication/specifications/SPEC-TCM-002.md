+++
id = "SPEC-TCM-002"
type = "specification"
title = "The generated diagnostic-code index"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[relations]
specifies = ["REQ-TCM-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T10:02:12Z"
decided_by = "technical-owner"
reason = "Approved by the accountable owner on 2026-08-31 by selecting the presented option 'Approve, start, complete on green' for WO-TCM-003: TCM-DCI-001 to TCM-DCI-006; the string-literal scanner with the curated registry, the deterministic page, the pinning test and the two links."
+++

# Specification: The generated diagnostic-code index

## Scope

One generator script, one generated note, one pinning test, and two index
links. No product behavior changes; no diagnostic code changes.

## Terms

- **Diagnostic code:** a short prefixed identifier printed beside an error,
  warning, advisory or refusal (`MG001`, `WEX-ECP-030`, `W-AUT-002`).
- **Registry:** the ordered table inside the generator naming each
  diagnostic prefix, its component, and a one-sentence meaning.

## Behavioral rules

**TCM-DCI-001:** `repository_tools/diagnostic_code_index.py` scans
`se_harness/`, `repository_tools/` and
`templates/repository/standard/scripts/` (never the hash-locked root
`scripts/` copies), parsing each Python source and extracting codes only
from string literals, so comments and identifiers never contribute.

**TCM-DCI-002:** A code enters the index only when its longest-matching
prefix is registered. The registry covers the diagnostic families
(validator errors and warnings including their hyphenated rule-family
forms, workflow execution, preflight, mutation guard, runtime identity,
interpreter safety, journaled apply, evaluator facts, renumbering, release
qualification, and the retired reserved codes); artifact and specification
identifier prefixes are not registered.

**TCM-DCI-003:** The generated page is `docs/notes/diagnostic-codes.md`:
a generated-file marker naming the regeneration command, the standard
target-expertise comment, a Summary section, a prefix table (prefix,
component, meaning, code count), and one table per prefix with each code
and up to two of its message texts, whitespace-collapsed and bounded in
length, with the count of further messages when more exist.

**TCM-DCI-004:** Output is deterministic: prefixes in registry order, codes
in natural (numeric-suffix) order, messages sorted, LF line endings, no
timestamp or environment detail.

**TCM-DCI-005:** The script's `--write` mode writes the page; `--check`
exits non-zero when the committed page differs from a regeneration.
`tests/test_diagnostic_code_index.py` pins: the committed page equals the
regeneration; every registered prefix matches at least one code; a named
set of known codes is present; artifact and rule identifiers are absent.

**TCM-DCI-006:** `docs/notes/README.md` indexes the page in the operator
table, and `docs/notes/harnessctl-check.md` links to it beside its small
`WEX` table. No other note changes.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-TCM-005 | TCM-DCI-001 to TCM-DCI-006 |

## Failure behaviour

The generator fails closed on an unparseable source file, naming it. The
pinning test's failure output names the first differing line.

## Compatibility and migration

The page documents the candidate source; the released 0.11.0 root may emit
a slightly different set until the next root adoption, which the page's
Summary states. Regeneration is part of any change that touches a
diagnostic code, enforced by the test rather than by convention.

## Explicitly unspecified decisions

Exact prose of the Summary and prefix meanings; the message-count bound;
test names.
