+++
id = "VER-RLS-034"
type = "verification"
title = "Verify plugin 0.2.5 with public evaluator 0.22.0"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-02"

[relations]
verifies = ["REQ-PLG-002", "REQ-IAR-030", "REQ-RLO-018"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T22:07:58Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package and required verification\" to the reviewed evaluator 0.22.0 / plugin 0.2.5 package: REL-SEH-034, WO-RLS-034/035/036 and VER-RLS-033/034/035. This confirms required commit-bound verification and authorizes bounded preparation, qualification, review pushes/PRs and listed delivery work under the retained request \"Merged. Next: prepare and execute the release\". Human verification of exact results, the exact release-record decision and merge remain separate. Repository adoption and provider-setting changes are excluded. Selected released 0.21.0 governs; Codex applies the recorded human decision. Reviewed SHA-256 969e20abac5a0be3a7ecd71874c7cb577f83ab97110c74b7c5ddf2fc4c860f7a; transition-input SHA-256 969e20abac5a0be3a7ecd71874c7cb577f83ab97110c74b7c5ddf2fc4c860f7a. Only confirmed assurance fields were added."
+++

# Verify plugin 0.2.5 with public evaluator 0.22.0

## Independence

Use SPEC-PLG-001, SPEC-IAR-016 and SPEC-RLO-006. The expected wheel digest comes
from the released RLS and an independent public download. Expected shared files
come from the selected committed manifests and assembly inventory.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-002 | test, inspection | Existing builder/checker, inventories and native host validators | Both 0.2.5 packages carry the identical public 0.22.0 wheel and shared assets; archive/tree identities are complete and no runtime is bundled. |
| REQ-IAR-030 | demonstration, test | Native traces and resource acceptance under VER-IAR-021 | Applicable startup, activation, manual/automatic compaction, resume and session isolation criteria pass for the exact host/plugin/resource inputs. Missing desktop evidence remains missing. |
| REQ-RLO-018 | inspection | Versioned delivery plan and handoff | Exact source, wheel, package trees, claimed hosts and expected marketplace parent are recorded before publication. |

## Procedure

After evaluator publication, use the existing released-input marketplace build
and check commands. Run package assembly tests on Windows and Linux. Use disposable
native host profiles and existing valid authentication; retain no credentials.
Check native evidence from earlier work against the actual final inputs before
reusing it. A helper invocation or CLI trace cannot replace a required native
event or desktop result. No earlier release-specific omission is carried over.

Retain actual source, public wheel, host versions, commands, checks, inventories,
full required native traces, failures and limitation assessment in evidence/WO-RLS-035/.
Capture VREC-PLG-032 with this contract and VER-IAR-021; obtain human verification
before publishing the exact descendant marketplace commit. Recheck its parent
and independently read the generated public tree back. Public fresh/update tests
remain downstream under WO-RLS-036; local assembly does not satisfy them.
