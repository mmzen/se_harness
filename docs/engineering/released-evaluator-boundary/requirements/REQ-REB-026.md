+++
id = "REQ-REB-026"
type = "requirement"
title = "Use one declared interpreter-safety rule at every identity boundary"
status = "approved"
owners = ["requirements-steward", "technical-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN any evaluator-identity boundary validates an interpreter path, THE SYSTEM SHALL apply one declared interpreter-safety rule shared by the package runtime and the repository-tools runtime, and a conformance check shall fail when a boundary implements its own variant or omits a declared refusal."
verification_method = "automated-architecture-conformance-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:01:45Z"
decided_by = "requirements-steward"
+++

# Requirement: Use one declared interpreter-safety rule at every identity boundary

## Retirement amendment of 2026-08-28

Retired on 2026-08-28 by `REQ-REB-030` under `WO-REB-030`, on the owner's approval for issue #220. The obligation was one rule *shared by the package runtime and the repository-tools runtime*; `WO-REB-028` deleted the four `repository_tools` boundaries and `release_qualification.py`'s, and `WO-ECP-011` deleted the migration probe, so one boundary remains (`se_harness/runtime_identity.py`) in one runtime and there is no second runtime to share with. The rule itself, its `EPS` refusals (`REQ-REB-024`) and the terminal-link acceptance (`REQ-REB-023`) are unchanged and now stated in code under `REQ-REB-030`. The rationale, required response and boundary behaviour below record what the repository did while this requirement was active and are retained unchanged as history; they are no longer obligations.

The declared `superseded` status is not applied, for the reason `WO-REB-028` recorded for `REQ-REB-012`: the definition lifecycle admits no `approved` to `superseded` edge. The retirement is recorded here instead.

## Rationale

The 0.6.0 defect is not one wrong line. Six boundaries independently decide what a safe interpreter path is, and they disagree in ways that a passing test suite does not expose:

| Boundary | Lexical entry | Parent link refused | Junction refused | Resolved target checked against checkout |
| --- | --- | --- | --- | --- |
| `se_harness/runtime_identity.py` | yes | no | no | no |
| `se_harness/release_qualification.py` external evaluator | yes | no | no | no |
| `se_harness/governance_migration.py` runtime probe | yes | symbolic links only | no | yes |
| `repository_tools/predecessor_preparation.py` | yes | yes | yes | yes |
| `repository_tools/predecessor_assessment.py` origin normalizer | yes | yes | yes | not applicable |
| `repository_tools/release_bootstrap.py` bootstrap binding | no — refuses a terminal link and derives the root from the resolved target | yes | yes | not reached |

Two of these are already correct, one has a junction gap, two have no link checks at all, and one is fatal on POSIX. Fixing the fatal site alone would leave five different rules in place and would leave the next boundary free to invent a seventh. A single correction is not a durable one unless the rule itself becomes the shared, checked artifact.

The obstacle is real rather than stylistic: `repository_tools` imports only the standard library and its own package, and it deliberately does not import `se_harness`, because it operates on candidate source and must not depend on candidate package importability. Any single rule must therefore serve two runtimes without creating that dependency.

## Preconditions and trigger

The trigger is the addition or modification of any code path that validates an external or installed interpreter for an evaluator-identity purpose, in either runtime.

## Required response

- One declared rule shall define the accepted and refused interpreter path forms, including every refusal in `REQ-REB-024` and the terminal-link acceptance in `REQ-REB-023`.
- Both the package runtime and the repository-tools runtime shall obtain their behavior from that one declaration without either runtime importing the other.
- Every boundary listed in this requirement's rationale shall reach the declared rule rather than restating it. A boundary may add checks that its role requires; it may not weaken, reorder around, or duplicate the declared refusals.
- A conformance check shall enumerate the boundaries and fail when a boundary validates an interpreter without the declared rule, when a runtime's behavior diverges from the declaration, or when the two runtimes disagree on any declared case.
- The declared cases shall be exercised as data by both runtimes so that a case added to the declaration without an implementation, or an implementation change without a declaration change, fails.
- A new boundary added later shall be a conformance failure until it is registered against the declared rule.

## Failure and boundary behavior

- A conformance failure is a stop, not a warning. A boundary that cannot use the declared rule requires an amendment, not a local exception.
- The declaration is data. It shall not contain executable code, platform conditionals expressed as code, or a per-boundary waiver list.
- Divergence detected between the two runtimes shall name the case and both observed outcomes rather than reporting only a count.
- Establishing the shared rule authorizes no change to lifecycle policy, released bytes, or root managed files.

## Constraints

- `repository_tools` shall continue to import only the standard library and its own package.
- The declared rule shall be positioned so that changing it is visible in review as a policy change rather than as an incidental refactor.
- Any digest bound to a declaration or implementation file elsewhere in the repository shall be re-measured rather than assumed unchanged.

## Acceptance examples

### Example: normal behavior

**Given** the declared rule and its two conforming loaders

**When** the conformance check runs over every registered identity boundary on Windows and on Linux

**Then** all boundaries resolve to the declared rule, both runtimes agree on every declared case, and the check passes.

### Example: failure behavior

**Given** a change that adds a junction refusal to the package runtime only

**When** the conformance check runs

**Then** it fails naming the diverging case and both observed outcomes, even though every other test still passes.

### Example: unregistered boundary

**Given** a new function that validates an external interpreter path without using the declared rule

**When** the conformance check runs

**Then** it fails identifying the unregistered boundary.
