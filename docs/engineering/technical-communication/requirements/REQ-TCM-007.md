+++
id = "REQ-TCM-007"
type = "requirement"
title = "A repository-owned glossary that follows its own corpus"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"
statement = "THE SYSTEM SHALL keep the glossary repository-owned: installed once as an empty seed, grown from the repository's own artifacts, reported when it lags them, and never carried by the distribution."
verification_method = ["test", "inspection"]
priority = "must"
source = "docs/notes/assessment-requirement-readability-2026-09-04.md, recommendation 4 as amended on 2026-09-04: the glossary is written from the repository's own corpus and context; se_harness's vocabulary must never travel in the templates"

[relations]
derives_from = ["CAP-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T16:14:37Z"
decided_by = "product-owner"
reason = "Approved by the accountable repository owner on 2026-09-04 with the instruction 'i approve the packet, the work orders can be start with execution delegation', after reviewing PR #335 (REQ-TCM-006..008, SPEC-TCM-003, VER-TCM-003, WO-TCM-005, WO-TCM-006)."
+++

# Requirement: A repository-owned glossary that follows its own corpus

## In plain words

Every repository that uses the harness gets an empty glossary file once,
and owns it from the first byte. A read-only report tells the owner which
frequent words have no definition and which definitions no longer match a
word in use. No term written in se_harness ever ships to another repository.

## Why

Two vocabularies meet in a requirement. Harness terms such as work order and
decision right are the same everywhere and are already defined in the
managed instructions. Project terms belong to one repository: `candidate`,
`digest` and `evaluator` are se_harness's words, and a payment service has
other words. A glossary is therefore content the repository writes, and the
harness may only install the place for it and measure how well it keeps up.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| `init` or `adopt` runs | `docs/notes/glossary.md` is written from a seed that carries the structure and the two-vocabulary rule and zero terms; an existing file is never overwritten | Not applicable |
| `upgrade` runs | The glossary is not a managed file; it is neither hashed nor rewritten | Not applicable |
| `inspect` runs | A `vocabulary` section lists project terms above an occurrence threshold with no glossary entry, and glossary entries whose term appears in no artifact; harness terms and common English are excluded | Findings are informational; nothing blocks |
| A distribution is built | No glossary term, definition or se_harness project vocabulary is in the templates; the seed has no entries | The test suite fails the build |

## Examples

### Normal

**Given** a freshly initialised repository with twelve requirements that
use the word `ledger` eighty times,

**When** the owner runs `inspect`,

**Then** the vocabulary section names `ledger` as a frequent term without a
glossary entry, and names no harness term.

### Failure

**Given** a candidate template that carries a glossary entry for
`candidate`,

**When** the suite runs,

**Then** the distribution-boundary test fails naming the entry.

## Open decisions

None.
