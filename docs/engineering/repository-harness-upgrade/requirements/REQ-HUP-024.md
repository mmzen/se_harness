+++
id = "REQ-HUP-024"
type = "requirement"
title = "Only a schema-3 lock is read, and only schema 3 is written"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-30"
updated = "2026-08-30"
statement = "WHEN the harness reads .engineering-harness.lock, THE SYSTEM SHALL interpret only a schema-3 lock, refusing a lower schema before any write with one diagnostic naming the floor and the re-adoption route, and SHALL never write a lock whose schema is not 3."
verification_method = ["test"]
priority = "must"
source = "issue #285 (functional assessment FA-6, item #285a) on the owner's floor decision of 2026-08-30: 'locks older than schema 3 are not read', hardened to the hard floor by the owner's selection of the same day; issue #224 (complexity audit P1-12), whose schema-1 inventory this executes and whose keep-schema-2-reading proposal the floor supersedes"

[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T19:20:01Z"
decided_by = "repository-owner"
reason = "Approved by the accountable owner on 2026-08-30 by selecting the presented option 'Approve, start, complete on green' for WO-HUP-012: only a schema-3 lock is read and only schema 3 is written, on the owner's floor decision of 2026-08-30 that locks older than schema 3 are not read, taken as the hard floor by the owner's selection of the same day (issue #285, item #285a)."
+++

# Requirement: Only a schema-3 lock is read, and only schema 3 is written

## Rationale

Lock schema 2 landed the same day as v0.2.0 and schema 3 has been the only
schema any supported release writes on a completed operation, yet every read
path still parses schemas 1 and 2, doctor passes on them with advisory
strings, the installer carries legacy-newline digest variants and four-way
match labels, and one branch still re-writes schema 1 for a customized
legacy root — freezing such a root on the dead schema forever. The owner's
floor decision of 2026-08-30 ends the ambiguity: a lock below schema 3 is
not data the tool interprets. A repository carrying one gets one clear
refusal naming the route back — remove the stale lock and re-adopt — instead
of a silently degraded compatibility mode no release has needed since 0.6.0.

## Preconditions and trigger

Any operation that reads `.engineering-harness.lock`: doctor, validate's
evaluator binding, upgrade planning and apply, qualification, and the
repository-owned transition assessment script.

## Required response

- A lock whose `schema` is 1 or 2 fails at read, before any write, with one
  diagnostic stating that the lock predates the supported floor (schema 3)
  and that the route is to remove the stale lock and re-adopt the
  repository. Any other unsupported schema keeps its existing failure.
- No operation writes a lock whose `schema` is not 3. The schema-1
  preservation branch of the installer is gone.
- The legacy digest machinery — the legacy-canonical schema constant, the
  schema-1 raw and fragment digests, the legacy-newline variant recognition
  in the integrity and hash-bound components, and the `exact` and
  `legacy-canonical` comparison labels — is deleted.
- An absent lock file keeps its current meaning (a repository without an
  installation); no internal representation of that state synthesizes a
  pre-3 schema.
- The refusal leaves the repository byte-identical and is not overridable
  by any flag, environment variable, or configuration value.

## Failure and boundary behavior

A pre-3 root can run no operation, including upgrade: the floor is a read
boundary, not a compatibility mode. Doctor reports the refusal as a failing
check naming the floor. The mutation guard's lock-schema condition becomes
unreachable and is retired with its code reserved.

## Constraints

The current schema-3 semantics — canonical digests, evaluator identity,
fragment modes — change in no way. Retained historical evidence recording
schema-1-era digests stays untouched.

## Acceptance examples

### Example: normal behavior

**Given** this repository, whose lock is schema 3,

**When** doctor, validate, upgrade planning and the transition assessment
run,

**Then** every reading is unchanged.

### Example: failure behavior

**Given** a repository whose lock declares `"schema": 2` (or 1),

**When** doctor or upgrade runs,

**Then** the operation fails before any write with the one floor
diagnostic, and the tree and lock are byte-identical afterward.

## Open decisions

None.
