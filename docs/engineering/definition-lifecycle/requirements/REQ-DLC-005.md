+++
id = "REQ-DLC-005"
type = "requirement"
title = "Preserve every existing governing record and diagnostic outcome"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN any definition-lifecycle increment is applied to this repository or planned for a consumer repository, THE SYSTEM SHALL leave every existing artifact status, lifecycle event, relation, and byte unchanged, SHALL keep the released-lineage validation verdict at zero errors, and SHALL change no diagnostic outcome for any artifact that existed before the increment except by moving an unchanged diagnostic's cause from an inferred lifecycle status to an explicit declaration."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DLC-001"]
+++

# Requirement: Preserve every existing governing record and diagnostic outcome

## Rationale

Every part of this domain touches machinery that decides whether 890 artifacts
are valid. Two of the three increments could plausibly be implemented in a way
that looks correct and is catastrophic:

- Removing the `LEGACY_ARCHITECTURE_STATUSES` proxy before the replacing
  declaration resolves converts 14 maintenance warnings into 14 governance
  errors, and the repository stops validating.
- Requiring a recorded decision past `draft` without the pre-contract
  declaration converts 449 valid definitions into 449 errors.

A silently *reduced* warning count is the mirror-image failure and is worse,
because it looks like progress. If the 14 `W014` diagnostics disappear rather
than change cause, the change has not replaced the grandfathering mechanism, it
has forgiven the debt.

The measured baseline is therefore part of the requirement rather than a note
about it.

## Preconditions and trigger

- Any of the three increments is implemented, reviewed, or planned as a
  managed-file upgrade for a consumer repository.

## Required response

- Measure the released-lineage verdict at the merge base and at the candidate,
  in the same way, and record both. At `c189b58` the baseline is 890 artifacts,
  0 errors, 50 warnings, comprising 21 `W013`, 14 `W014`, and 15 `W015`.
- After the first increment, keep the count and the identifier set of `W014`
  identical, keep `W015` at 15 including `ARCH-IAR-004`, keep `W013` at 21, and
  keep errors at 0. Assert the exact `W014` identifier set, not only its
  cardinality.
- After the second increment, keep every count identical again. That increment
  removes a transition and re-points a recommendation; it must move no
  diagnostic.
- After the third increment, keep errors at 0 and add exactly the declared
  pre-contract maintenance diagnostics, whose count is asserted exactly.
- Change no artifact file. The exact changed-path inventory of each increment
  contains no path under `docs/engineering/` other than that increment's own
  evidence directory and this domain's own artifacts.
- Provide a governance-migration scenario for the version pair the release
  lands in, so a consumer upgrading across the boundary is planned rather than
  surprised.

## Failure and boundary behavior

- A reduced warning count is a failure, not an improvement, and the test asserts
  equality rather than an upper bound.
- A changed `W014` identifier set with an unchanged count is a failure.
- Any modification to an existing artifact's status, `lifecycle_events`,
  relations, or bytes is a failure, whatever its intent.
- A consumer repository whose managed files are customized blocks before any
  partial replacement, through existing upgrade behavior. No special bypass is
  added.
- A predecessor evaluator that cannot express the new boundary is handled by the
  migration contract's adapter path. If the boundary cannot be expressed, the
  increment stops and the constraint is escalated rather than approximated.

## Constraints

- The baseline figures are a checkpoint at one commit, not constants. They are
  re-measured at the actual merge base of each increment, and the recorded pair
  is what the increment is judged against.
- Both the package implementation and the self-contained validator script are
  measured. A governor-versus-candidate warning gap is expected and is not
  skew, so each is compared against its own baseline.
- Windows and Linux readings are labelled separately. A green reading on one
  platform is not evidence about the other.
- No verified verification record and no released release record is read,
  rewritten, re-pointed, or superseded by any increment.

## Acceptance examples

### Example: normal behavior

**Given** the candidate for the first increment

**When** the released-lineage evaluator validates the repository at the merge
base and at the candidate

**Then** both report 0 errors and 50 warnings, and the `W013`, `W014`, and
`W015` identifier sets are identical between the two runs.

### Example: cause moves, outcome does not

**Given** the candidate for the first increment

**When** each of the 14 architectures in the frozen set is temporarily removed
from that set in a fixture

**Then** each reports `E014` in the fixture, proving the declaration and not the
lifecycle status is what suppresses the error in the real run.

### Example: failure behavior

**Given** a candidate in which the frozen set is empty

**When** the graph is validated

**Then** 14 governance errors are reported, the increment fails its own
acceptance, and no reviewer can read the result as a passing run.

## Recorded decisions

Decided 2026-08-26 by the repository owner: exact-equality assertions on
diagnostic identifier sets are a required gate for all three increments, and a
reduced warning count fails the contract. Permitting a documented reduction, and
asserting count equality only, were both considered and declined — the first
reintroduces judgement at the point the gate exists to remove it, and the second
passes a candidate where the count matches while membership changed. The accepted
cost is that a legitimate unrelated warning fix landing concurrently turns the
gate red and forces a re-measured baseline.

Decided 2026-08-26 by the repository owner: every work order in this domain
carries `commit_bound_verification = "required"`. Each increment changes a managed
contract or a managed validator that consumers pin, so each needs its own
verification record bound to a commit where the evidence is tracked.
