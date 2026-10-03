+++
id = "VER-RLS-002"
type = "verification"
title = "Verify Claude post-release evidence and bounded coverage claims"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[relations]
verifies = ["REQ-IAR-030", "REQ-RLO-019", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T09:45:54Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" to the prepared package request: choose record-tested-subset for DEC-RLS-007 and DEC-RLS-008; approve WO-RLS-038 and VER-RLS-002 with required commit-bound verification; correct the six scoped guidance files while preserving remaining gaps and historical records; permit ordinary pushes from work/claude-025-evidence-followup and a draft PR to mmzen/se_harness:main, including the later verification-decision push. Verification acceptance and merge remain separate. Codex applies the human decision. Reviewed SHA-256 2f92bac11df66a13f8e9de86e9d60362c0b1bdffeda3cc8a0225dfd621874918; transition input SHA-256 2f92bac11df66a13f8e9de86e9d60362c0b1bdffeda3cc8a0225dfd621874918. Only confirmed assurance metadata was added to the WO."
+++

# Verify Claude post-release evidence and bounded coverage claims

## Independence

Expected behavior comes from SPEC-IAR-016 and SPEC-RLO-006. Expected package
identity comes from released RLS-SEH-032 and the retained independent package
qualification/publication receipts. Compare new observations with those inputs;
agreement between two new reports alone does not prove identity.

## Requirement-to-evidence matrix

| Requirement | Method and retained evidence | Pass condition |
| --- | --- | --- |
| REQ-IAR-030 | Inspect native-delivery and native-boundaries traces in observations-raw.zip. | SessionStart startup/resume/compact events and native manual/auto boundaries support each stated pass; checkout, release and entry digest match. Explicit switch/clear affects only the selected session. Missing checkout reports a gap, and restoration recovers the same entry. |
| REQ-RLO-019 | Compare public fresh/update command traces, inventories and immutable release inputs. | Public revision, starting 0.2.4 installation, resulting 0.2.5 package and all 29 files match the qualified package and released 0.22.0 wheel. Native test package bytes match those public bytes. |
| REQ-RLO-020 | Review current guidance, linked decisions, coverage table and original-record digests. | Statements name the tested subset, host/version and limits; no broad verified-host claim, fabricated risk closure or rewritten historical result. Current links resolve. |

## Procedure

1. Recompute the archive digest and every archived entry digest. Compare the
   retained originals with the transient source receipts before discarding them.
2. Inspect the raw events, not only the summary pass booleans. For each manual
   and automatic compaction require both its native boundary and the complete
   exact entry in a successful SessionStart:compact response.
3. Compare the public installed-file inventories with the independently
   qualified package inventory, and the wheel hash with RLS-SEH-032.
4. Confirm every protected historical record remains byte-identical to the
   baseline manifest. Review all updated current-coverage notices and their links.
5. Run `python -B -X utf8 -m unittest tests.test_progressive_documentation
   tests.plugin_integration.package_assembly.test_refresh_guidance` as one
   command. Retain output. Run released validation and the selected scope and
   handoff checks. Do not add tests that merely assert this prose.
6. Capture the exact clean evidence/documentation commit under evaluator 0.22.0.
   Request the human's verification decision after the review PR is available.

## Evidence retention

Use `docs/engineering/release-0-22-0/evidence/WO-RLS-038/`. Retain actual command
arrays, exit codes, timestamps, host identity, synthetic inputs, relevant outputs,
source/public identities and SHA-256 values. Keep credentials excluded. The
fixture runners are observation evidence, not changed product implementation.

## Residual uncertainty

This contract verifies the supplement and its tested subset. It does not replace
VER-IAR-021, VER-RLS-034 or VER-RLS-035 or certify their complete matrices.
Codex Windows desktop, the full Claude author/execute/delivery walkthrough and
the earlier long-path failure remain unverified. The accepted 0.2.4 omissions,
local hook-loss limitations and missing-draft-evidence crash remain unchanged.
No new human assurance verdict is supplied by retaining successful tests.
