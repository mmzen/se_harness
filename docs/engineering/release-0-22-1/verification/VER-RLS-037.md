+++
id = "VER-RLS-037"
type = "verification"
title = "Qualify plugin 0.2.6 before release"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
verifies = ["REQ-PLG-002", "REQ-IAR-030", "REQ-RLO-018", "REQ-RLO-021"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T18:24:52Z"
decided_by = "mmzen"
reason = "mmzen answered \"Approve preparation and review publication\" to the exact seven-artifact evaluator 0.22.1 / plugin 0.2.6 proposal: REL-SEH-035, WO-RLS-040/041/042 and VER-RLS-036/037/038, with required commit-bound verification. This approves bounded preparation and qualification of the two HAG fixes and main already-approved dashboard correction, ordinary review pushes/draft PRs from codex/release-0-22-1 to mmzen/se_harness:main, later verification-decision updates, read-only CI rehearsals and the codex/plugin-0-2-6-staging review ref. Human verification, merge, the exact complete-release decision, adoption and provider-setting changes remain separate. Reviewed draft hashes matched; only the human-confirmed assurance fields were added before preview. Reviewed SHA-256 75c5078408f98f4da8beae33450dd9c663ce92ea989fb0bceaf3296d458d904a."
+++

# Qualify plugin 0.2.6 before release

## Independence and inputs

Use SPEC-PLG-001, SPEC-IAR-016 and SPEC-RLO-006/007 as expected behavior.
Use the exact schema-2 candidate bundle for 0.22.1 and both 0.2.6 manifests.
This is candidate staging under the existing complete-release route, not a
fictional public-wheel or released-RLS input.

## Requirement-to-evidence matrix

| Requirement | Method and evidence | Pass condition |
| --- | --- | --- |
| REQ-PLG-002 | Existing staging builder/checker, archive tests and host inventories on Windows/Linux | Both checked packages contain the identical qualified wheel and shared assets, with complete hashes and no runtime. |
| REQ-IAR-030 | Actual native events and walkthrough under VER-IAR-021 | Applicable startup, activation after clone, resume, manual/automatic compaction, isolation and delivery-gap criteria pass for the exact host inputs. CLI evidence does not substitute for desktop evidence. |
| REQ-RLO-018 | Inspect the staged marketplace commit, tree and plan | Proposed public tree is an ordinary child of the observed parent; exact commit/tree and both inventory digests are retained before approval. |
| REQ-RLO-021 | Inspect candidate-to-final delivery binding | Staged identities are frozen before release approval; later release/governance receipts do not rebuild or rebind payloads. |

## Procedure and retention

Use the existing build_plugin_marketplace.py staging/check procedures and package
tests. Run disposable Codex and Claude profiles with valid authentication; never
retain credentials. Assess the Codex Windows desktop criterion and Claude
walkthrough/long-path limitations explicitly. Prior release-specific deferrals
do not carry forward. Missing required results remain pending for a distinct
human decision, not implicit acceptance within package approval.

Retain actual tool/component identities, native traces, package/source hashes,
staging parent/tree and outcomes under evidence/WO-RLS-041/. Stage before the
aggregate final-candidate verification. If needed, qualify again after packaging
inputs change. Public fresh/update tests belong to VER-RLS-038.
