+++
id = "WO-TCM-003"
type = "work_order"
title = "Generate the diagnostic-code index"
status = "implemented"
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

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T10:02:12Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-31 by selecting the presented option 'Approve, start, complete on green', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: the generator, the generated note, the pinning test, the two note links, this domain's index and the evidence packet; and authorizes marking the work order implemented once the declared evidence is green. It authorizes no change to any diagnostic code or message, no hash-locked root file, no verification record, no release and no publication; the pull request's merge remains the owner's decision. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-31T10:02:36Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's decision of 2026-08-31, made by selecting the presented option 'Approve, start, complete on green'. Start preflight PASS with no diagnostics over the approval commit 61ccb53 carrying main 1ba3009, run with the governing exact public 0.11.0 evaluator outside the checkout, on this Windows checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-31T10:14:59Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner under the decision of 2026-08-31, made by selecting the presented option 'Approve, start, complete on green', which authorized this transition once the declared evidence was green. The evidence packet at docs/engineering/technical-communication/evidence/WO-TCM-003/ records: the string-literal scanner with the curated registry and the derived composed codes (TCM-DCI-001, TCM-DCI-002), the deterministic generated page with 256 codes across 28 prefixes (TCM-DCI-003, TCM-DCI-004), the eight pinning tests and the --check mode (TCM-DCI-005), the two note links (TCM-DCI-006); the new suite with the progressive-documentation suite 26 OK and the full Windows suite at its baseline (1171 tests, the one known test_artifact_authoring error, 26 skips); validate 1207 artifacts 0 errors, doctor 0 FAIL, distributions PASS under the 0.11.0 root, whose environment was recreated during execution with an unchanged identity; the handoff check complete:true at its fixed point result a0099b4d over the packet head 1a81819, from-git origin/main 1ba3009. No deviations. This decision authorizes no verification record, no release and no publication; the pull request's merge remains the owner's decision."
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
