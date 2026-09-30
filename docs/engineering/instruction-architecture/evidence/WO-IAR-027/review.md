# Glossary correction review

WO-IAR-027 changes exactly eleven glossary entries and Upkeep under approved
REQ-IAR-027 and SPEC-IAR-014. The before/after text and unchanged current policy
sources are retained in wording-review.json. No harness rule changed.

| VER-IAR-019 criterion | Assessment |
| --- | --- |
| Authority and lifecycle | Pass: Human approval, agent execution, actual identity and legacy labels match AUTHORITY.md. VREC and RLS descriptions retain exact candidate binding and separate human decisions. Permitted later lifecycle changes preserve evidence history. |
| Current destinations | Pass: all 14 glossary links resolve to files and heading anchors. The selected entries no longer refer to DECISION_RIGHTS.md or QUALITY_GATES.md. |
| Results and exceptions | Pass: machine-field digest, optional PR reference, checkpoint-free context and lack of a supported documentation exception match the unchanged 0.20.0 guides. |
| Preservation and scope | Pass: reverse substitution reconstructs the complete original bytes. All term names, unselected paragraphs and line endings are preserved. Only GLOSSARY.md changes among previously tracked files. |
| Focused tests | Pass: 17 tests from tests.test_glossary and tests.test_workflow_documentation_contract. Actual invocation and outputs are in checks.json. |
| Governing checks | Released identity, doctor, validation and start checks pass. Review preflight and full Git-derived handoff are retained separately before completion. |
| Exact candidate | Required before human acceptance: capture reruns the focused tests and approved-text/link checks in the committed candidate. VREC-IAR-017 binds that result and these evidence files. |

The direct paragraph replacements are sufficient. No source changes, new test
module, compatibility mechanism or native host qualification is needed. This
review covers the selected entries only; it does not claim a complete reassessment
of every historical document or other glossary entry. Hosted CI remains required
at integration. Preparation does not supply human verification or push authority.
