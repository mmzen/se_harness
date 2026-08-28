+++
id = "REQ-ECP-008"
type = "requirement"
title = "Decisions are authenticated records"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "WHEN `harnessctl transition --apply` is invoked, THE SYSTEM SHALL refuse the transition unless each decision is a decision record whose signer identity is verified against the configured identity source and whose role holds the decision right."
verification_method = ["test"]
priority = "must"
source = "review section 5, weakness 1; se_harness/workflow.py:606"

[relations]
derives_from = ["CAP-ECP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: Decisions are authenticated records

## Rationale

Human decisions are free-text role strings (`--decision WO=assurance-owner`)
validated for length and control characters only; no Git-author, `GITHUB_ACTOR`,
`CODEOWNERS`, or signature check exists anywhere in `se_harness/` or `scripts/`
(se_harness/workflow.py:606; docs/notes/agentic-execution-
review-2026-08.md:42-45, :139-142). The mutation guard proves which evaluator
wrote, never who decided (docs/notes/agentic-execution-
review-2026-08.md:205-208). Until decisions are bound to an identity,
"accountable humans retain authority" is a documentation claim
(docs/notes/agentic-execution-review-2026-08.md:413-417).

## Behavior

- Trigger: `harnessctl transition REPO --artifact ID --to STATE --apply`
  runs with one or more `--decision-record FILE`.
- Response: each record is parsed as a structured decision (decision right,
  artifact, outcome, reason, signer); the signer is verified against the
  identity source configured in `.engineering-harness.toml` (a commit or file
  signature, or the CI actor); the signer's role is looked up and must hold the
  named decision right in `DECISION_RIGHTS.md`; only then is the lifecycle event
  appended, and it names the verified signer.
- On failure: when a record is unsigned, its signature does not verify, the
  signer maps to no role, the role does not hold the right, or a required
  decision is missing, no artifact is modified and the result names the failing
  record and predicate.

## Assumptions and dependencies

- The identity source is repository configuration, not harness policy; a
  repository with none configured cannot apply transitions that require a
  decision, and the result says so.
- `--decision ID=ACTOR` as a bare string is retired in the same change.
- `DECISION_RIGHTS.md` stays the table of rights to roles; the mapping from
  identities to roles is the consumer's configuration.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-008.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `WO-X-004` is `implemented`, `VREC-X-002` is `ready`, and a record
signed by a key mapped to `assurance-owner` decides `DR-VREC-DECIDE` with
outcome `verified`.

**When** `harnessctl transition . --artifact VREC-X-002 --to verified
--decision-record dec.toml --apply` runs.

**Then** `VREC-X-002` becomes `verified` and the appended lifecycle event names
the verified signer and `assurance-owner`.

### Example: failure behavior

**Given** the same command, but the record is signed by a key mapped to
`engineering-owner`.

**When** the command runs.

**Then** no file changes, and the result names `dec.toml`, `engineering-owner`,
and `DR-VREC-DECIDE` as the right the role does not hold.

## Open decisions

None.
