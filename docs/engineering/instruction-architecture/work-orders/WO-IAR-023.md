+++
id = "WO-IAR-023"
type = "work_order"
title = "Correct template and newline test assumptions"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-28"
updated = "2026-09-28"

[assurance]
commit_bound_verification = "required"
rationale = "Human-approved commit-bound assurance for source instruction and owner-byte preservation checks."
decided_by = "mmzen"

[execution_scope]
paths = [
  "tests/test_artifact_catalog.py",
  "tests/test_installer.py",
  "docs/engineering/instruction-architecture/proposals/instruction-cleanup/",
  "docs/engineering/instruction-architecture/acceptance/instruction-cleanup/",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-023.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-023/",
]

[relations]
implements = ["REQ-IAR-023", "REQ-IAR-027"]
specifications = ["SPEC-IAR-014"]
verification = ["VER-IAR-015"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T08:14:20Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"Approve WO-IAR-023 and required verification\". Explicit permission includes legacy engineering-owner encoding; Codex applies the recorded decision. Reviewed SHA-256 d8deef8e4b812231ac7e244cd99e2430d0842cd24ddb9888bc4fe8fa2db455d7."
scope_paths = ["tests/test_artifact_catalog.py", "tests/test_installer.py", "docs/engineering/instruction-architecture/proposals/instruction-cleanup/", "docs/engineering/instruction-architecture/acceptance/instruction-cleanup/", "docs/engineering/instruction-architecture/work-orders/WO-IAR-023.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-023/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-28T08:15:57Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the exact approved two-file test correction after passing start preflight."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-28T08:27:09Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Codex applied the exact approved test correction. Focused cases and full Windows/Linux suites pass; original failures and baseline comparison are retained."
+++

# Correct template and newline test assumptions

## Objective

Make two existing checks assess their stated contracts while WO-IAR-021 changes
product instructions without adopting them into this repository.

## In scope

1. In test_artifact_catalog.py, replace equality between the installed 0.19.0
   template's complete metadata and candidate metadata with checks of their
   shared architecture, relation and scope contracts. Check the candidate's
   actual-human assurance prompt and current authority route explicitly.
2. In test_installer.py, normalize the released fixture's CRLF to LF before
   constructing the requested LF or CRLF test input. Preserve all owner-byte
   assertions and migration refusal checks. A Windows-converted fixture must
   not become CR-CR-LF through a second conversion.

The exact proposed patch and tested file digests are in
`proposals/instruction-cleanup/test-correction.patch` and
`test-correction-review.json`. They have not been applied to repository tests.
Both focused cases pass with that patch in a disposable candidate copy.

## Evidence for the correction

The current full Windows run reports one failure and one error among 1,134 tests.
The catalog equality fails on the deliberately changed assurance prompt.
The newline case also fails on baseline fd05dc9f28452c906e764a37570342acbabd09b9;
it is a pre-existing test-input problem. The installer correctly refuses its
unrecognized AGENTS.md and CLAUDE.md fragments. Product installer behavior does
not need to change for this correction.

## Out of scope and stop conditions

No installer, evaluator, template, accepted definition, existing lifecycle
history, installed managed file or real host change. No test skip or weakened
owner-content protection. Stop if either failure requires product behavior
changes or another path. WO-IAR-022's retirement remains dependent on verified
WO-IAR-021 and is not started by this correction.

## Authorized decision envelope

After approval, apply the reviewed two-file test correction, run its required
checks, retain observed failures and passes, record completion and prepare
commit-bound verification through the selected released evaluator. The agent
may adjust test wording within these exact contracts. Human verification
acceptance and any external action remain separate.

## Required verification and evidence

Apply VER-IAR-015 alongside WO-IAR-021. Rerun the two focused checks, the affected
instruction suites, and the complete test runner on Windows and Linux. Preserve
the original failures, baseline comparison, proposed/applied diff, runtime
identities, commands, results and complete path set under evidence/WO-IAR-023/.
Use an exact clean candidate for supported VREC preparation; include both work
orders in its selected scope when assessing their combined result.

## Assurance and completion

The human repository owner mmzen confirmed **required** commit-bound assurance
with: "Approve WO-IAR-023 and required verification". The approved request also
permits the selected 0.19.0 evaluator encoding as engineering-owner, with the
actual human identity and decision retained in the reason.

Completion reports the two corrected test assumptions, actual verification
results, remaining gaps and the evaluator's next typed step. A passing isolated
proposal test does not authorize implementation or supply verification acceptance.
