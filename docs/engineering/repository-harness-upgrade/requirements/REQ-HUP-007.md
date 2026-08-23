+++
id = "REQ-HUP-007"
type = "requirement"
title = "Reconcile self-hosting checks after released-root adoption"
status = "approved"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN the repository adopts its own released 0.6.0 standard root, THE SYSTEM SHALL reconcile owner instructions and boundary tests so that exact released-root/package content convergence is accepted while origin isolation, managed integrity, evaluator evidence, retired-context ownership, and all external-action controls remain fail closed."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Reconcile self-hosting checks after released-root adoption

## Rationale

Before root adoption, several repository tests used byte inequality between the
installed 0.5.0 root and the packaged 0.6.0 policy as evidence of role
separation. The exact 0.6.0 transaction legitimately removes that byte skew.
Role separation must continue to be proved by paths, runtime origins, lock
identity, and mutation boundaries rather than by requiring current released
bytes to remain different from themselves.

The repository-owned `AGENTS.md` region also describes the predecessor root and
does not name the two schema-3 JSON contracts. Updating those owner facts is a
separate repository action; it must not be folded into or represented as an
installer write.

## Required response

- Update only the repository-owned region of `AGENTS.md` to identify released
  0.6.0, the two managed JSON contracts, and the correct post-adoption
  candidate/evaluator boundary.
- Replace stale byte-inequality assertions with exact equality plus independent
  path/origin/lock assertions where released 0.6.0 now matches the packaged
  standard root.
- Update the retired-context mention inventory for the exact HUP-002 records
  that necessarily prove owner-byte preservation, and remove the retired path's
  withdrawn managed-router mention.
- Make revision-provenance fixtures satisfy the released schema-3 evaluator
  evidence contract instead of relying on legacy released-record exemptions.
- Preserve every negative test for contamination, corruption, missing evidence,
  unauthorized mutation, credential use, publication, and external action.

## Prohibited response

Do not modify `se_harness/`, `templates/repository/standard/`, any managed root
file, lock or transaction evidence, package/version/build metadata, release or
verification records, publisher or Pages behavior, credentials, Git history,
or external state. Do not add a production legacy exemption for test fixtures.

## Acceptance examples

### Example: equal bytes, distinct roles

**Given** the installed root and packaged standard root both contain released
0.6.0 policy bytes

**When** boundary tests execute

**Then** they accept the exact equality and still prove that the governing
runtime originates outside the checkout and the candidate source remains
inside it.

### Example: evaluator evidence fixture

**Given** a temporary released-record fixture evaluated by schema-3 policy

**When** revision provenance validation runs

**Then** the fixture supplies canonical released-evaluator evidence bound to
its temporary schema-3 lock, without weakening production validation.
