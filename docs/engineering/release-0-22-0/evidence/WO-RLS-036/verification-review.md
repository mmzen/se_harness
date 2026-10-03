# Verification request: public delivery checks and current guidance

**Decision requested:** Verify VREC-PLG-033 for candidate
`4798b2f9b4c8227a017bd455842a0acb8fa1eb99`, covering WO-RLS-036 under VER-RLS-035.
This verifies the retained public checks and documentation changes. Overall
release delivery still needs this decision, documentation integration/readback,
and the authorized latest/last promotion.

## Result to review

Plugin 0.2.5 is public at marketplace commit
`7d30907f15bd7e06fb632e1ebf4e88e01b68726c`. Independent public readback matches
all 69 qualified files. Codex CLI fresh installation and an actual update from
the prior public 0.2.4 pass; each installed package matches all 29 qualified files.
Offline setup passes on both routes with the exact 0.22.0 evaluator.

Current guidance now names evaluator 0.22.0 and plugin 0.2.5, links these receipts,
and states the host limits below. Matching assertions in the existing guidance
test use the new public identities. Runtime, installer, immutable release files,
normal host profiles and repository evaluator selection are unchanged.

## Verification evidence

| Check | Observed result |
| --- | --- |
| Public package and route identities | All public package bytes match; Codex CLI fresh/update and offline setup pass. |
| Current source documentation links | All checked local paths and anchors resolve. |
| Existing documentation tests | 28 pass, including package-context links and invalid/stale identity cases. |
| Candidate capture | Repeated the receipt/hash checks, source links and 28 tests in a clean checkout of the exact candidate; exit 0. |
| Harness validation | 0 errors; 61 repository warnings retained separately. |
| Work-order scope, review preflight and handoff | Pass against the complete Git change set from the trusted PR base. |
| Public evaluator and demo | PyPI archive hashes match RLS-SEH-032; Pages identifies the released candidate and governance input. |
| Overall delivery checker | Correctly returns incomplete: documentation pending and observed old latest/last do not match the planned new markers. |

The [verification record](../../verification-records/VREC-PLG-033.md) binds the
candidate and evidence. Read the [public route report](public-routes.json),
[publication receipt](publication-receipt.json), [independent readback](public-readback.json),
[check summary](checks.json), and [delivery result](delivery-result-v4.json).
The retained ZIP files contain commands, raw outputs and failures with digest maps.

## Disclosed limits

**Claude Code installation/update and native sessions, and Codex Windows desktop,
were not tested and remain unverified.** DEC-RLS-005/006 record the human's
current-release acceptance of those omissions. They are not test passes.

Codex CLI native startup, activation, compaction, resume and isolation coverage
reuses the verified VREC-PLG-032 matrix after comparing the exact package file
hashes and Codex CLI 0.159.2 identity. No new authenticated model session in the
public fresh/update profiles is claimed.

RISK-RLS-006 remains an unfixed evaluator defect with a documented workaround in
the previous qualification evidence. This review does not claim it fixed or
independently accepted. Repository adoption and provider-configuration activation
remain separate work.

## Decision and subsequent actions

VREC-PLG-032 is already verified by mmzen. VREC-PLG-033 is ready and still requires
the reserved human assurance decision. If accepted, reply:

> I verify VREC-PLG-033 as assurance owner.

The agent will record and push that exact decision. Merge remains a human action.
After integration, the retained release-execution authorization covers matching
documentation readbacks and latest/last promotion when their checks pass. Final
observations will be retained separately without rewriting this candidate's evidence.
