+++
id = "VER-IAR-019"
type = "verification"
title = "Verify glossary alignment with adopted instruction policy"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[relations]
verifies = ["REQ-IAR-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T07:14:21Z"
decided_by = "mmzen"
reason = "Human mmzen: I approve both. Approval of the reviewed VER-IAR-019 and WO-IAR-027, including required verification against the exact commit. Reviewed VER SHA-256 902f6cc5ad040140a4098f37ef361aa5ef15ac32c0119f237a1fbe6dafa56030."
+++

# Verify glossary alignment with adopted instruction policy

## Independence

Expected meanings come from approved REQ-IAR-027 and SPEC-IAR-014, especially
IAR-DIS-010 through IAR-DIS-013, and the installed 0.20.0 instructions. Do not
derive expected authority from the proposed glossary. The glossary is explanatory
owner content; this work changes no harness rule or formal lifecycle.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-IAR-027 | inspection | Authority and lifecycle wording | Each selected entry agrees with AUTHORITY.md, VERIFY_OUTCOME.md and WORK_AND_EVIDENCE.md. Human decisions and agent application are distinct; historic role/delegation labels do not grant new rights; bound candidate and evidence are preserved during permitted lifecycle transitions. |
| REQ-IAR-027 | inspection, test | Current destinations | New links resolve to actual current files and headings. No selected entry points at the retired DECISION_RIGHTS.md or QUALITY_GATES.md. Reuse the existing glossary and documentation tests. |
| REQ-IAR-027 | inspection | Results and exceptions | Digest explanations agree with RESULTS.md and PULL_REQUEST.md: current machine fields are hashed; a PR digest does not independently prove unchanged inputs. Upkeep follows EXCEPTIONS.md's unavailable-capability fallback, without inventing an exemption. |
| REQ-IAR-027 | inspection, test | Preservation and scope | Only the exact selected GLOSSARY.md paragraphs change outside the new package and its evidence. Existing term names, other paragraphs, current instructions, templates and historical artifacts remain unchanged. |

## Checks

Use Windows with Python 3.14 and the independently installed released evaluator
0.20.0 selected by this repository. Record actual versions, argument arrays,
working directory, exit codes and failures.

1. Compare every proposed replacement with its cited current source. Report
   any semantic conflict rather than changing that source or a harness rule.
2. Check all newly added glossary Markdown destinations and heading anchors.
   Confirm that unrelated paragraphs and all existing term names are unchanged.
3. Run `python -m unittest tests.test_glossary tests.test_workflow_documentation_contract`.
   No new test module, source change or broad regression suite is required for
   this owner-prose correction unless a concrete failure calls for it.
4. Run released identity, doctor, artifact validation, selected start/review
   preflight and complete Git-derived scope/handoff checks.
5. Prepare VREC-IAR-017 against one exact clean committed candidate. Rerun the
   focused tests and glossary link/content comparison in that captured checkout.
   Do not replace observed candidate results with tests from an uncommitted tree.

Existing hosted checks remain required at integration. Native host delivery,
installer behavior and package contents do not change and need no new
qualification for this work.

## Evidence retention

Retain the source-to-replacement review, before/after glossary comparison,
resolved links, unchanged paragraph checks and actual commands/results under
docs/engineering/instruction-architecture/evidence/WO-IAR-027/.
The generated VREC-IAR-017 and its evaluator companion bind the exact candidate.
Human acceptance of that record remains a separate decision.

## Residual uncertainty

These checks establish the selected wording and references. They do not claim
that all other glossary entries or historical documents have been reassessed.
An additional defect outside the reviewed paragraph set needs separate scope.
