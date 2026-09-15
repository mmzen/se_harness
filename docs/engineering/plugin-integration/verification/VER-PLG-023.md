+++
id = "VER-PLG-023"
type = "verification"
title = "Check native marketplace installation and publication contents"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-15"
updated = "2026-09-15"

[relations]
verifies = ["REQ-PLG-038"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T13:40:15Z"
decided_by = "assurance-owner"
reason = "The owner reviewed the four marketplace drafts and replied \"OK i approve the artifacts you can start\" on 2026-09-15. Record approval of this exact reviewed artifact in the named accountable role. This authorizes WO-PLG-023 execution under DR-015, not verification of a future candidate or a provider submission."
+++

# Check native marketplace installation and publication contents

## Independence

Expected catalog behavior comes from SPEC-PLG-022 and current provider formats.
Expected shared files come from the selected committed sources; expected wheel
bytes come from the published release and independent archive digest. An output
inventory does not establish its own correctness. Retain the actual source
commit and commands for every acceptance claim.

## Requirement-to-evidence matrix

| Requirement | Method and evidence | Pass condition |
| --- | --- | --- |
| REQ-PLG-038 | M01 package and catalog inspection | Both host validators accept the complete packages and catalog; committed assets, native inventories and wheel identities agree. |
| REQ-PLG-038 | M02 focused boundary tests | Missing or escaping catalog sources, modified output and unrelated existing destinations are refused without damaging an outside sentinel. Reuse existing builder tests for unchanged boundaries. |
| REQ-PLG-038 | M03 local native installation | Fresh Codex and Claude profiles add the distribution and install verity-plane through standard commands; cached package contents match; intended skills are discovered. Operator brief remains explicit-only. |
| REQ-PLG-038 | M04 submission review | Listing copy and reviewer cases identify the tested package, actual setup/data behavior, provider route and outstanding publisher inputs; no unobserved approval is claimed. |
| REQ-PLG-038 | M05 public observation, after authorized delivery | Both fresh profiles add the actual Git ref and install the same contents; retain remote commit and installed file comparison before calling that route publicly checked. |

## Scope and execution

M01-M04 are required before implementation completion and candidate assurance.
M05 follows the separately governed external publication action and cannot be
claimed in a pre-publication VREC. Retain M05 as subsequent publication evidence;
do not rewrite the earlier verification record.

Use the repository-selected released evaluator 0.18.0 outside the checkout for
graph, integrity, preflight and workflow checks. Run repository-required checks
and the focused assembly tests. Native marketplace acceptance begins on the
owner's Windows environment using available Codex and Claude Code versions.
Record versions as observations, not exact-version support allowlists. Other
platforms and model-driven skill sessions remain unclaimed unless exercised.

Apply VER-PLG-001 for unchanged wheel and shared-file boundaries and VER-PLG-016
for the installation walkthrough. Reference unchanged setup evidence only after
comparing its script, skill and wheel inputs. Rerun affected steps on the final
candidate. Earlier prototype results remain labeled preliminary, and cannot
substitute for acceptance of the committed marketplace composition.

## Evidence and remaining decisions

Keep commands, exit codes, concise results, relevant raw logs and input/output
identities under `evidence/WO-PLG-023/`. Reuse ordinary test fixtures and a short
requirements-to-results summary. No new test harness or CI lane is required.
The implementation VREC binds the exact clean candidate containing these inputs.
Owner assurance, external delivery and provider review remain separate decisions.
Missing publisher identity or legal URLs does not block preparation of a clearly
incomplete submission draft, but prevents submitting that draft as complete.
