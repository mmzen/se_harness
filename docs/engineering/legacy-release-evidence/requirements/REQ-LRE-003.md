+++
id = "REQ-LRE-003"
type = "requirement"
title = "A release record without evaluator evidence is not assessed"
status = "draft"
owners = ["repository-owner", "quality-owner", "security-owner"]
created = "2026-08-30"
updated = "2026-08-30"
statement = "WHEN validation or an evaluator upgrade examines a released release record that carries neither evaluator-evidence field, THE SYSTEM SHALL not assess it against the evaluator-evidence binding, raising no diagnostic, requiring no declaration, and refusing no transaction on its account."
verification_method = ["test"]
priority = "must"
source = "issue #285 (functional assessment FA-6, item #285a) on the owner's floor decision of 2026-08-30: 'releases without evaluator evidence are not assessed', taken literally by the owner's selection of the same day; issue #214 (complexity audit P1-2), whose double-implementation finding this closes by removing both implementations"

[relations]
derives_from = ["CAP-LRE-001"]
+++

# Requirement: A release record without evaluator evidence is not assessed

## Rationale

`REQ-LRE-001` and `REQ-LRE-002` built a declaration mechanism so that six of
this repository's own pre-enforcement releases could stay valid: a frozen
six-identifier set in three files, a 327-line package module, a mirrored
resolver in the installed validator, sixteen specification rules, a shared
vector fixture keeping two implementations equal, one `W024` warning per
record on every validation, and a pre-apply upgrade refusal. The owner's
floor decision of 2026-08-30 replaces all of it with one sentence: a
released record carrying neither `evaluator_evidence_path` nor
`evaluator_evidence_sha256` is simply not assessed against the binding. The
workflow gates on the way to `released` remain what forces evidence onto a
new release; validation stops re-litigating history it cannot change.

## Preconditions and trigger

Artifact validation examines a release record's evaluator-evidence binding;
or an evaluator upgrade examines the repository it is about to upgrade.

## Required response

- The evaluator-evidence binding is validated only when a released record
  carries at least one of the two evidence fields. A record with both
  fields absent raises no error, no warning, and no advisory.
- A record carrying exactly one of the two fields keeps its existing error:
  a partial binding is never valid.
- A record carrying both fields keeps every existing binding check,
  including current-lock matching for `ready` records and archive-identity
  checks.
- No resolver, frozen identifier set, declaration mechanism, or per-record
  debt warning exists. The diagnostic code `W024` is retired and stays
  reserved.
- An evaluator upgrade neither enumerates unbound released records, nor
  refuses on their account, nor writes any declaration into its evidence.
- The `[evaluator_upgrade]` packet continues to accept its optional
  `legacy_releases_without_evaluator_evidence` key as inert data, so a
  historical consumer work order carrying one stays valid; the key grants
  and changes nothing.

## Failure and boundary behavior

Nothing new fails. A repository whose history holds unbound released
records validates clean; one that holds a partially bound record fails
exactly as it does today. No flag or configuration re-enables the
assessment.

## Constraints

Retained release records are never edited; the six pre-enforcement
`RLS-SEH-*` records keep their bytes. The root copy of the managed
validator is the released 0.11.0 one and keeps its resolver until the next
root adoption.

## Acceptance examples

### Example: normal behavior

**Given** this repository, whose six pre-enforcement released records carry
neither evidence field,

**When** the candidate template validator runs,

**Then** it reports no error and no warning for them, and its warning count
drops by exactly the six retired `W024` entries.

### Example: failure behavior

**Given** a released record carrying `evaluator_evidence_path` but no
`evaluator_evidence_sha256`,

**When** validation runs,

**Then** the record fails with the existing partial-binding error.

## Open decisions

None.
