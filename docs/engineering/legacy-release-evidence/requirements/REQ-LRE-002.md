+++
id = "REQ-LRE-002"
type = "requirement"
title = "Refuse an evaluator upgrade that would leave an undeclared unbound released record"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN an evaluator upgrade would write a schema-3 lock, THE SYSTEM SHALL refuse the transaction before any write if the repository holds a released release record that carries neither evaluator-evidence field and is neither declared by an authority-granting upgrade work order nor a member of the self-hosting compatibility set, and SHALL name every such record and the work order that must declare it."
verification_method = "automated-installer-refusal-test"

[relations]
derives_from = ["CAP-LRE-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:44:00Z"
decided_by = "repository-owner"
+++

# Requirement: Refuse an evaluator upgrade that would leave an undeclared unbound released record

## Rationale

The measured failure mode in issue #126 is not that the upgrade broke. The
upgrade succeeded: the plan applied, the lock moved to schema 3, the replay
postcondition held, and `doctor` reported 87 PASS with no warnings or failures.
The repository was nevertheless dead, and it learned this only on the next
`validate`, from an error on a record it is forbidden to edit.

An upgrade whose only possible outcome is a frozen repository must not be a
successful transaction. The installer already knows everything needed to see it
coming: it has the repository root, it has the authorizing work order, and the
records are ordinary artifacts. Refusing before the first write costs nothing and
converts an unrecoverable state into an actionable message.

Refusing is also the honest place for the check. `REQ-LRE-001` makes a declared
record valid; this requirement makes the absence of a declaration something the
operator is told about at the moment they can still fix it, rather than something
their CI discovers.

## Preconditions and trigger

- An evaluator upgrade is invoked against a repository root and will write a lock
  whose schema enforces the evaluator-evidence binding.
- An `[evaluator_upgrade]` authorization packet has been loaded and matched.
- The repository's artifact tree is readable.

## Required response

- Before the first write of the transaction, enumerate release records whose
  status is `released` and which carry neither `evaluator_evidence_path` nor
  `evaluator_evidence_sha256`.
- Subtract those accepted under `REQ-LRE-001` by any authority-granting upgrade
  work order in the repository, and those in the self-hosting compatibility set.
- Refuse the transaction when the remainder is non-empty. The refusal names every
  remaining identifier in deterministic order and names the authorizing work order
  as the artifact whose `[evaluator_upgrade]` table must declare them.
- Leave the repository byte-identical when refusing. No managed file, lock,
  configuration file or evidence file is written.
- Report the same finding as a notice, without refusing, when the invocation only
  plans and does not apply.
- Apply no other new condition. An upgrade whose remainder is empty behaves
  exactly as it does today, including every existing authorization, mutation-guard
  and replay postcondition.

## Failure and boundary behavior

An unreadable or malformed artifact in the tree is not treated as an absence of a
released record; the enumeration fails closed and the transaction is refused with
the reason. An artifact tree that does not exist yields no records and no
refusal, because a repository with no governed history cannot hold an unbound
released record.

The refusal is advice about governance state, not a lifecycle decision. It grants
no authority, approves nothing, and never edits an artifact to make itself pass.
It does not consult, and cannot be overridden by, an environment variable, a
command-line flag or a local configuration value.

## Constraints

The check runs on the repository being upgraded, reads only tracked artifact
content and the loaded authorization, is deterministic for a given tree, and is
bounded in the number and size of artifacts it will read. Its acceptance logic and
the validator's must agree; the agreement is asserted against a shared fixture
rather than assumed from the two implementations reading alike.

## Acceptance examples

### Example: normal behavior

**Given** a repository holding one `released` record with no evaluator-evidence
fields, and an approved upgrade work order whose `[evaluator_upgrade]` table
declares that record,

**When** the upgrade is applied,

**Then** the transaction proceeds exactly as it does today and the repository
validates after the upgrade.

**Given** a repository with no `released` record at all,

**When** the upgrade is applied,

**Then** no new condition applies and the transaction proceeds unchanged.

### Example: failure behavior

**Given** the same repository with the declaration removed from the work order,

**When** the upgrade is applied,

**Then** the command fails before writing, the message names the record and the
authorizing work order, and the repository tree and lock are byte-identical to
their pre-invocation state.

**Given** the same repository,

**When** the upgrade is only planned,

**Then** the plan is reported together with a notice naming the same record, and
no refusal occurs.

## Open decisions

None.
