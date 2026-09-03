+++
id = "REQ-HUP-011"
type = "requirement"
title = "Adopt the successor through one bounded schema-3 root transaction and prove complete-graph operation"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN the exact released successor is proven, THE SYSTEM SHALL apply one approved evaluator-upgrade work order bound to the prior lock and the target evaluator through the reviewed standard-root plan atomically, SHALL retain canonical evidence, SHALL fail closed on customization, plan drift, or postcondition failure, and afterwards SHALL prove doctor with zero failures, complete-graph validation with zero errors, and the operating card, closed reading manifest, corrective forms, router scope, and risk gates in effect at the root."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T17:15:22Z"
decided_by = "requirements-steward"
+++

# Requirement: Adopt the successor through one bounded schema-3 root transaction and prove complete-graph operation

## Rationale

`REQ-HUP-005` and `REQ-HUP-006` defined this for 0.6.0; the same transaction
shape applies to the successor. The postconditions are extended to the
capabilities the successor carries, and to the test suite: five test modules
currently declare "candidate differs from root" exceptions; after adoption
those differences vanish and the exceptions must be retired, or the tests
rewritten to compare template to template permanently.

## Preconditions and trigger

`REQ-HUP-010` satisfied; the evaluator-upgrade work order approved with its
`[evaluator_upgrade]` table naming the prior lock digest, the target version,
payload digest, archive name, and archive digest from the release record.

## Required response

- One `upgrade --apply` from the isolated successor against the standard
  root; the plan reviewed before apply; managed, fragment, and seed modes
  respected; owner content outside markers preserved.
- Postconditions: `doctor` 0 FAIL under the successor; `validate` 0 errors;
  `docs/engineering/OPERATING_CARD.md` present and managed; the preflight
  manifest for a selected work order closed to router, card, `AGENTS.md`,
  and chain; a blocked `check` renders a corrective form; the router carries
  its scope section; `[risk]` present in `.engineering-harness.toml`;
  `raise-risk` creates a risk that the root validator accepts.
- Test exceptions in `test_artifact_catalog`, `test_validation_taxonomy`,
  `test_dashboard_webui`, `test_artifact_authoring`, and
  `test_lifecycle_state_contract` retired or converted.
- `.engineering-harness.toml` `tool_version` and the CI workflow's evaluator
  pin equal the successor version.

## Failure and boundary behavior

Any postcondition failure rolls the transaction back or, if applied, blocks
integration until remediated under a new decision.

## Constraints

Candidate source never performs the upgrade; the root copies are replaced by
the installed successor's payload only.

## Acceptance examples

### Example: normal behavior

**Given** the proven successor and the approved work order

**When** the reviewed plan is applied

**Then** every postcondition above holds and the evidence records the plan,
the prior and new lock digests, and the identity.

### Example: failure behavior

**Given** a customized managed file at the root

**When** the plan is applied

**Then** the transaction refuses that file and writes nothing partial.

## Open decisions

None beyond the version and digests supplied by the release record.
