+++
id = "VER-IAR-015"
type = "verification"
title = "Verify current instruction references and reading cost"
status = "approved"
owners = ["quality-owner", "repository-owner"]
created = "2026-09-28"
updated = "2026-09-28"

[relations]
verifies = ["REQ-IAR-022", "REQ-IAR-023", "REQ-IAR-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T07:51:40Z"
decided_by = "quality-owner"
reason = "Human repository owner mmzen: \"I approve, you can start the work orders\". Approval covers the reviewed instruction-cleanup package and required commit-bound assurance. Legacy evaluator role quality-owner records that human decision; Codex applies it. Reviewed SHA-256 afad1e04732d8a4cdee475602b7963a3d94c1645f54054929bdfb4e62e37ac81."
+++

# Verify current instruction references and reading cost

## Independence

Expected behavior comes from REQ-IAR-022, REQ-IAR-023, REQ-IAR-027 and
SPEC-IAR-014. The reassessment at fd05dc9f28452c906e764a37570342acbabd09b9
is a measured baseline, not an assurance verdict. Do not derive expected routes
from the candidate mapping being tested.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence and pass condition |
| --- | --- | --- |
| REQ-IAR-022 | inspection, test, analysis | Root retains all nine invariants and its router. Measure the complete injection envelope with a declared long repository path and real encoding. The supported helper returns the full root within its actual limit; oversize input reports a delivery gap without claiming success. Do not equate unrelated host limits or infer native delivery from this test. |
| REQ-IAR-023 | inspection, test, demonstration | Markdown links, code-formatted document anchors, generated WO templates, README seed and Explorer destinations all resolve. An agent can identify the current heading and its prerequisites without following old pointer anchors or loading later stages. A deliberately broken active anchor is detected. |
| REQ-IAR-027 | inspection, analysis, test | Review F2-F8 dispositions against SPEC-IAR-014. Commands, authority, provider controls, decision identities and confirmation boundaries retain meaning. Six task traces and before/after counts include COMMUNICATION.md and required references; formal artifact reads are listed separately. |

## Checks

1. Generate a work-order template in an isolated repository. Verify that its
   approval route is AUTHORITY.md#authority-from-work-approval. Its authoring
   prompt asks for the actual human who confirmed assurance, not a role used
   to satisfy validation. No evaluator rights or old lifecycle events change.
2. Exercise new drafting, resumed execution after compaction, a verification
   decision, PR preparation, failed-check recovery and evaluator setup. Retain
   exact files/headings and each read trigger. Current instructions retained
   in context may be reused; changed or lost required inputs are read again.
   Every required governing artifact and fresh lifecycle check remains required.
3. Review the external-action procedure and both skill routes. The applicable
   provider requirement has a clear owner and read trigger. No independent
   enforcement or human decision requirement disappears through editing.
4. Keep the complete CONTINUE index required by SPEC-IAR-014. Outcome and scope
   may share one clarification exchange only when both receive the required
   confirmation. A new heading, index removal or policy change needs separate
   accepted-definition review.
5. Compare full-envelope units and per-task unique whitespace words with the
   report baseline. Report changed counts and their reasons. No score target,
   percentage reduction or unmeasured token saving is a gate.

## Platforms and commands

Use the candidate source in isolated test environments on Windows and Linux.
Run the focused instruction/discovery, documentation, Explorer and plugin
conformance suites affected by the diff, then `python scripts/run_tests.py`,
`python scripts/validate_release_distributions.py --root .` and CLI help.
Run the repository-selected released evaluator's validation and the selected
WO start/handoff checks separately. Record actual interpreter and evaluator
versions. The current governing evaluator is 0.19.0; candidate 0.20.0 is not
automatically adopted. Existing unrelated failures are identified, not hidden.

## Evidence retention and acceptance

Retain commands, exit codes, expected/actual comparisons, complete change set,
reference dispositions and reading-cost results under evidence/WO-IAR-021/.
Use supported commands to prepare the VREC for the exact clean candidate commit.
Human verification acceptance is separate. This contract does not qualify a
native host, approve release or delete installed compatibility files.
