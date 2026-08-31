+++
id = "WO-TCM-003"
type = "work_order"
title = "Generate the diagnostic-code index"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[assurance]
commit_bound_verification = "required"
rationale = "The change adds a repository tool and a test the suite depends on; the index's no-drift guarantee is trusted state later documentation relies on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "repository_tools/diagnostic_code_index.py",
  "tests/test_diagnostic_code_index.py",
  "docs/notes/diagnostic-codes.md",
  "docs/notes/README.md",
  "docs/notes/harnessctl-check.md",
  "docs/engineering/technical-communication/README.md",
  "docs/engineering/technical-communication/evidence/",
  "docs/engineering/technical-communication/requirements/REQ-TCM-005.md",
  "docs/engineering/technical-communication/specifications/SPEC-TCM-002.md",
  "docs/engineering/technical-communication/verification/VER-TCM-002.md",
]

[relations]
implements = ["REQ-TCM-005"]
specifications = ["SPEC-TCM-002"]
verification = ["VER-TCM-002"]
+++

# Work Order: Generate the diagnostic-code index

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Add `repository_tools/diagnostic_code_index.py`, the string-literal scanner
with the curated prefix registry (`TCM-DCI-001`, `TCM-DCI-002`); generate
`docs/notes/diagnostic-codes.md` deterministically (`TCM-DCI-003`,
`TCM-DCI-004`); pin it with `tests/test_diagnostic_code_index.py` and a
`--check` mode (`TCM-DCI-005`); and link it from the notes index and the
`check` note (`TCM-DCI-006`). Issue #281 item #281b, the last piece of the
assessment's FA-2, unblocked by WO-ECP-022's code normalization.

## Why now

The developer note counts hundreds of diagnostic codes across dozens of
prefixes; only seven `WEX` codes are tabulated anywhere, and `MG`, `RID`,
`EPS` and `PRE` codes are readable only in source. Discoverability scored
3/10 partly for this.

## In scope

- The generator script (standard-library only, honoring the
  `repository_tools` import barrier).
- The generated note, committed.
- The pinning test module.
- One index row in `docs/notes/README.md`; one link sentence in
  `docs/notes/harnessctl-check.md`.
- This domain's index and the evidence packet.

## Out of scope

Any change to a diagnostic code, message, or emitting module; the
hash-locked root `scripts/` copies (not scanned, not edited); every other
note; the release carrying this change.

## Authorized decision envelope

The registry's prefix meanings and the Summary prose; the message-count
bound; test names; the exact table layout.

## Constraints

- Deterministic output: sorted, LF, no timestamps.
- The page follows the owner's writing standard of 2026-08-30 (Summary
  first, plain language).
- The word "governor" is not introduced into `docs/notes/`.

## Expected change surface

One new repository tool, one new test module, one generated note, two
edited notes, the domain index and the packet.

## Required verification

Execute `VER-TCM-002` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/technical-communication/evidence/WO-TCM-003/`.

## Stop and escalate conditions

Any need to change a diagnostic code or message to make the index
generable; any hash-locked file in the change set; a scan that cannot be
made deterministic across platforms.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
