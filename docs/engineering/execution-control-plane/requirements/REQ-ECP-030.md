+++
id = "REQ-ECP-030"
type = "requirement"
title = "A removed command name outlives its removal by one release only"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-02"
updated = "2026-09-02"
statement = "WHEN one release has shipped after a command name was removed from harnessctl, THE SYSTEM SHALL carry no guard for that name, so that the parser refuses it as it refuses any unknown command."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #310 (functional assessment item #285c: the tombstone guards are kept for exactly one release after their removal shipped); REQ-ECP-022, REQ-ECP-024 and REQ-ECP-025, whose assumptions each promise the later removal; REQ-REB-031, which left the accept-candidate guard to this item"
measure = "main() in se_harness/cli.py carries no pre-parse guard for focus, next, accept-candidate or prepare-release --authorized-by; each name is refused by argparse with its usage error and exit status 2; --help lists none of them; the three refusal tests are gone and the absence assertions remain; the notes state the plain refusal"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T14:38:23Z"
decided_by = "repository-owner"
reason = "Approved on 2026-09-02 by the accountable owner by selecting the presented options 'Include the --authorized-by guard too' and 'Delegated route (the delegation class)' for WO-ECP-025: the four CLI tombstone guards (focus, next, accept-candidate, prepare-release --authorized-by) leave main() three releases after their removals shipped (issue #310, assessment item #285c)."
+++

# Requirement: A removed command name outlives its removal by one release only

## Rationale

Three command names left `harnessctl` in quick succession: `focus` folded
into `check` (`REQ-ECP-022`, `REQ-ECP-024`, removed after 0.10.0), `next`
folded into the checkpoint-less `check` (`REQ-ECP-025`, removed after
0.11.0), and `accept-candidate` replaced by `qualify candidate-package`
(`REQ-REB-022`, removed after 0.11.0). Each left a pre-parse guard at the
head of `main()` that exits with status 2 and names the replacement, so a
consumer's script written against the previous release fails loudly once,
during the one upgrade in which it could still be surprised. The
requirements that introduced each guard promise its removal "by a later
work order after one release has shipped". Since then 0.12.0, 0.13.0 and
0.14.0 have shipped. The guards are now dead weight at the entry of every
invocation and the last place the three words survive in the CLI.

## Behavior

- Trigger: the candidate after 0.14.0 is built.
- Response: `main()` parses its arguments directly; `harnessctl focus`,
  `harnessctl next` and `harnessctl accept-candidate` are refused by the
  parser as unknown choices, with argparse's usage error and exit status 2,
  exactly as any misspelled command is; `--help` lists none of them.
- On failure: none introduced; every registered command behaves as today.

## Assumptions and dependencies

- `REQ-ECP-024`'s clause "refuse focus with a message naming check" and
  the guard rules `ECP-RMV-002` (`SPEC-ECP-013`), `ECP-CTX-004` and
  `ECP-CTX-006` (`SPEC-ECP-014`) described the one-release window; they are
  closed by dated amendment under this requirement, not deleted.
- The `--authorized-by` guard on `prepare-release` (`ECP-CLI-002`,
  `SPEC-ECP-016`, renamed after 0.11.0) is the same kind of tombstone and
  is retired under this requirement on the owner's decision of 2026-09-02.

## Acceptance examples

### Example: normal behavior

**Given** the candidate after this change,

**When** `harnessctl next --artifact WO-001 --json` runs,

**Then** the exit status is 2, standard output is empty, standard error
carries argparse's "invalid choice" usage error, and no code of the product
ran.

### Example: failure behavior

**Given** a reintroduced pre-parse guard for any of the three names,

**When** the suite runs,

**Then** the test that reads `main()`'s source for the three names fails.
