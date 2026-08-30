+++
id = "SPEC-HUP-012"
type = "specification"
title = "The lock-schema floor"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
specifies = ["REQ-HUP-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T19:20:01Z"
decided_by = "technical-owner"
reason = "Approved by the accountable owner on 2026-08-30 by selecting the presented option 'Approve, start, complete on green' for WO-HUP-012: HUP-LSF-001 to HUP-LSF-008; the floor refusal, schema-3-only writer, legacy machinery deletion, MG002 retired and reserved, and amendment records on REQ-PMI-004, SPEC-PMI-001 and ADR-PMI-001."
+++

# Specification: The lock-schema floor

## Scope

Makes schema 3 the only lock schema the harness reads or writes, and
deletes the schema-1 and schema-2 compatibility machinery from the
integrity, installer, doctor, hash-bound and mutation-guard components and
from the repository-owned transition assessment script. Changes nothing
about schema-3 semantics.

## Terms

- **Floor:** lock schema 3, the lowest (and only) schema the harness
  interprets, per the owner's decision of 2026-08-30.
- **Pre-3 lock:** a parseable lock JSON whose `schema` is 1 or 2.

## Behavioral rules

**HUP-LSF-001:** Lock validation accepts schema 3 only. A pre-3 lock fails
with one diagnostic stating that the lock predates the supported floor
(schema 3) and that the route is to remove the stale lock file and re-adopt
the repository with `harnessctl adopt`. Any other schema keeps the existing
unsupported-schema failure. The refusal happens before any write and leaves
the tree byte-identical.

**HUP-LSF-002:** The legacy digest machinery is deleted from the integrity
component: `LEGACY_CANONICAL_LOCK_SCHEMA`, `legacy_tracked_sha256`,
`matches_legacy_newline_variant`, the per-schema branch of the entry
digest, and the `exact` and `legacy-canonical` comparison labels. A raw
byte digest helper survives only where a non-lock caller still needs it.

**HUP-LSF-003:** The installer writes schema 3 only: the schema-1
preservation branch for a customized legacy root, the schema-1 acceptance
branches in seed migration and in the leaving-set plan, and the retained
schema-1 `sha256` helper are deleted. An absent lock file keeps its current
meaning, and no internal representation of that state synthesizes a pre-3
schema. Init and adopt behavior on a repository without a lock is
unchanged.

**HUP-LSF-004:** Doctor renders a pre-3 lock as one failing check carrying
the floor diagnostic of HUP-LSF-001. The `legacy exact` and `legacy
canonical match; upgrade recommended` advisory renderings are gone.

**HUP-LSF-005:** The mutation guard no longer keys on lock schema: a pre-3
lock already fails at read, so the guard's ordinary-mutation schema
condition is deleted and its diagnostic code `MG002` is retired and stays
reserved, never reused with another meaning.

**HUP-LSF-006:** The hash-bound component recognizes no
`legacy-newline-variant`: the match label and its acceptance in declared
digest comparison are deleted. A recorded digest matches canonically or
fails; a raw-mode class keeps its exact-byte rule.

**HUP-LSF-007:** `scripts/validate_governor_transition.py` accepts lock
schema 3 only.

**HUP-LSF-008:** Tests pin the floor: a schema-1 and a schema-2 lock are
each refused with the floor diagnostic and no write; an applied init,
adopt, or upgrade always emits schema 3; no deleted symbol, label, or
variant recognition survives anywhere under `se_harness/` or `scripts/`.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-HUP-024 | HUP-LSF-001 to HUP-LSF-008 |

## Failure behaviour

Every refusal is fail-closed and byte-identical, with bounded diagnostics.
No flag, environment variable, or configuration value overrides the floor.

## Compatibility and migration

This is the breaking change the floor decision states: a 0.2.x-to-0.5.x
consumer root (schema 1 or 2) can no longer be read, inspected, or upgraded
in place; its route is to remove the stale lock and re-adopt, after which
its customized files are governed by adopt's existing non-overwrite
behavior. `REQ-PMI-004`, `SPEC-PMI-001` and `ADR-PMI-001`, which committed
to conservative schema-1 reading and schema-2 writing in the 0.2.x era, are
amended by dated amendment records under `WO-HUP-012`; their history stays
valid as the record of why the machinery existed. Retained evidence citing
schema-1-era digests is data, not a read path, and is untouched. The root
copy of the managed validator is the released 0.11.0 one and already reads
the evaluator identity only from a schema-3 lock; it changes no byte here.

## Explicitly unspecified decisions

Exact diagnostic wording beyond the elements HUP-LSF-001 requires; internal
representation of the absent-lock state; test names.
