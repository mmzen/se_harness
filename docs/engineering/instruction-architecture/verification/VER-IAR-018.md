+++
id = "VER-IAR-018"
type = "verification"
title = "Verify repository pointer cleanup after 0.20.0 adoption"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[relations]
verifies = ["REQ-IAR-028"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T06:17:22Z"
decided_by = "mmzen"
reason = "Human mmzen: I approve, in response to the explicit WO-IAR-026 / VER-IAR-018 and required commit-bound verification request. Reviewed draft SHA-256 59e5a3108ac56a6b2b43465d4d41e04b09f161c6ac72d81064a81aa01ad4e69b"
+++

# Verify repository pointer cleanup after 0.20.0 adoption

## Independence

Derive the removal set and expected replacement routes from approved
SPEC-IAR-015, not from the candidate's output. Use the public 0.19.0 fixture
provenance to establish stock pointer content; use WO-IAR-026's reviewed exact
byte hashes to authorize removal. Use the independently installed released
0.20.0 evaluator for identity, integrity, lifecycle and work-scope checks.

This contract covers the separately authorized repository-cleanup case of
REQ-IAR-028. VER-IAR-017 and its accepted evidence cover product retirement,
fresh installations and supported upgrades. Preserve those tests and evidence;
this cleanup changes none of that accepted product behavior.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-IAR-028 | inspection | Six-file byte review | Every path is regular, within the checkout, matches its reviewed exact hash, and has only stock content confirmed against public fixture provenance. All six pass before the first deletion. |
| REQ-IAR-028 | inspection, demonstration | Active consumers and native delivery | Inventory actual Codex and Claude host/plugin versions and package hashes. Current skills, templates, scripts, Explorer and instruction routes do not require the six files. Required replacement headings resolve. Matching native startup/compaction evidence passes before deletion; disclose the tested surface. |
| REQ-IAR-028 | test, inspection | Cleanup and preservation | Exactly the six reviewed pointers disappear. The approved catalog-test correction is the only executable change. AGENTS.md, current instructions, authoring guide, machine contracts, historical records and supported fixtures/adapters remain byte-identical. |
| REQ-IAR-028 | test | Installer reconciliation and repeat preview | Released 0.20.0 preview/apply do not recreate pointers, alter owner content or write unexpected files. Doctor passes and a repeat preview is unchanged. The lock contains none of the six paths. |
| REQ-IAR-028 | test, inspection | Refusal boundaries | Review the execution's all-file precheck. Reuse preserved tests for customized owner files, unsafe destinations, supported 0.18.0 migration and retry. A changed file or unresolved live consumer prevents deletion; missing evidence is never recorded as a pass. |
| REQ-IAR-028 | test, demonstration | Post-cleanup routes and regression | Current catalog/root routes and actual-host discovery still work without the files. Applicable tests, full suite, distribution validator, CLI smoke and released work-order checks pass. |

## Checks and platform

Use Windows on the current workstation with Python 3.14 and the exact released
0.20.0 evaluator selected by the repository. Record actual versions, commands,
exit codes and failures. Run native host probes in read-only sessions under the
identified profiles. Authentication success alone is not delivery evidence.
Do not infer desktop delivery from CLI or app-server observations.

Run at least tests.test_artifact_catalog, tests.test_installer,
tests.test_instruction_architecture, tests.test_progressive_instruction_discovery
and tests.test_workflow_documentation_contract. Existing legacy fixture tests
must remain intact. Then run python scripts/run_tests.py --scale full,
python scripts/validate_release_distributions.py --root ., and
python -m se_harness --help with the source test interpreter.

Run the released evaluator's identity, doctor, validate, selected-work readiness,
Git-derived complete scope and handoff separately. Inspect installer upgrade
preview before apply and run a repeat preview. Any unexpected write requires
review before apply. Windows/Linux hosted CI remains an integration prerequisite;
local success does not claim that hosted runs have completed.

## Evidence retention and assessment

Retain actual observations under
docs/engineering/instruction-architecture/evidence/WO-IAR-026/.
Keep the reviewed deletion inputs, consumer dispositions (current, historical,
conditional), package/host identities, native context observations, owner-byte
comparison, installer results, complete change set and check logs. Preserve
accepted prerequisite qualification evidence rather than rewriting it.

Prepare VREC-IAR-016 through capture-verification against one exact clean
candidate commit with all retained evidence and generated evaluator companion.
Rerun applicable automated verification in that captured candidate. A human
assurance decision is required to mark the resulting record verified.

## Residual uncertainty

At drafting, actual Codex app-server startup/manual-compaction checks pass for
plugin 0.2.2 and root 0.20.0. Normal Claude plugin 0.2.0 still needs matching
native evidence to be reviewed or renewed before deletion. The current desktop
chat uses a parent directory with no selected installation; it supplies no
desktop delivery qualification. Stop removal if this leaves an active consumer
unresolved. No host/plugin upgrade or newly supported host surface is authorized.
