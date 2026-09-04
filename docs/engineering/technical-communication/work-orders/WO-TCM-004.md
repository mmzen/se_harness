+++
id = "WO-TCM-004"
type = "work_order"
title = "Register the decision-management diagnostic families in the code index"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[assurance]
commit_bound_verification = "required"
rationale = "The change edits the generator registry, the pinning test the suite depends on, and the generated page that operators read to interpret a refusal; the no-drift and coverage guarantees are trusted state, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "repository_tools/diagnostic_code_index.py",
  "tests/test_diagnostic_code_index.py",
  "docs/notes/diagnostic-codes.md",
  "docs/notes/decision-artifacts.md",
  "docs/engineering/technical-communication/README.md",
  "docs/engineering/technical-communication/evidence/",
]

[relations]
implements = ["REQ-TCM-005"]
specifications = ["SPEC-TCM-002"]
verification = ["VER-TCM-002"]
+++

# Work Order: Register the decision-management diagnostic families in the code index

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

`WO-DCM-001` added the validator families `E-DCM-001..004` and
`W-DCM-001..002` to the candidate source, but its execution scope did not
include `repository_tools/diagnostic_code_index.py`, so the generated
`docs/notes/diagnostic-codes.md` does not list them (disclosure 3 of the
`VREC-DCM-001` evidence). Register the two prefixes in the generator's
registry (`TCM-DCI-002`), regenerate the page (`TCM-DCI-003`,
`TCM-DCI-004`), and extend the pinning test's known-code set with one code
of each family (`TCM-DCI-005`).

`VER-TCM-002` records one residual uncertainty: a new diagnostic prefix
added without registration is invisible to the index, and review is the
only control. This work order closes it for the hyphenated rule-family
forms: the generator gains a guard that fails `--check` and the pinning
test when a string literal carries a code of the shape `E-XXX-nnn`,
`W-XXX-nnn` or `WEX-XXX-nnn` whose family is not registered. The single-
letter and artifact-identifier shapes are out of the guard's reach by
construction and stay under review.

## In scope

- Two registry rows in `repository_tools/diagnostic_code_index.py`:
  `E-DCM` and `W-DCM`, installed validator, decision-management error and
  warning.
- The unregistered-family guard in the same module, reported by `--check`
  and by a new test; no other behavior of the scanner or renderer changes.
- `docs/notes/diagnostic-codes.md` regenerated and committed.
- `tests/test_diagnostic_code_index.py`: `E-DCM-001` and `W-DCM-001` in the
  known-code set; the guard test.
- One sentence in `docs/notes/decision-artifacts.md` pointing from its
  diagnostics table to the generated index.
- This domain's index and the evidence packet.

## Out of scope

Any change to a diagnostic code, message or emitting module; any change to
`SPEC-TCM-002` or `VER-TCM-002`; the hash-locked root `scripts/` copies (not
scanned, not edited); every other note; the release carrying this change.

## Authorized decision envelope

The two prefix meanings; the guard's wording and exit path; test names; the
placement of the link sentence.

## Constraints

- Deterministic output: sorted, LF, no timestamps.
- Standard library only; the `repository_tools` import barrier stands.
- The word "governor" is not introduced into `docs/notes/`.

## Expected change surface

One repository tool, one test module, one regenerated note, one edited
note, the domain index and the packet.

## Required verification

Execute `VER-TCM-002` in full against the changed registry;
repository-required checks; the pull request's lanes; the handoff check over
the Git-derived change set.

## Evidence to record

`docs/engineering/technical-communication/evidence/WO-TCM-004/`.

## Stop and escalate conditions

Any need to change a diagnostic code or message; any hash-locked file in
the change set; a guard that cannot separate diagnostic families from
artifact or rule identifiers without registering the latter.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
