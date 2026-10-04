+++
id = "VER-RLS-004"
type = "verification"
title = "Verify transition snapshots with absent draft evidence"
status = "draft"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
verifies = ["REQ-WEX-002"]
+++

# Verify transition snapshots with absent draft evidence

## Independence

Expectations come from REQ-WEX-002 and SPEC-WEX-001, not candidate output.
Use the retained actual failing fixture: approved WO-FLW-001 plus unrelated
draft WO-FLW-002 declaring absent future evidence. Preserve that declaration.
Released 0.22.0 governs; candidate packages run in isolated environments.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-WEX-002 | Public CLI probes, stale-input tests, existing rollback failure injection, complete byte comparisons | Legal selected actions return structured results and only permitted writes; missing required evidence and stale/unsafe input refuse without partial writes. |

## Cases

1. The unrelated draft declares an absent evidence file. Validation and start
   preflight pass. Start preview returns a structured permitted plan without
   writes. Apply changes only the selected work order; the draft stays unchanged.
2. Evidence required by the selected completion/checkpoint remains a required
   gate. Missing evidence refuses the action and leaves the state unchanged.
3. A planned absent evidence file appears before apply. Reject the stale plan
   without writes. Also test disappearance and changed existing bytes.
4. Unreadable files, directory inputs and unsafe links remain structured
   refusals, not absence or unhandled tracebacks. Preserve path-safety checks.
5. Existing stale unselected graph input and replacement/rollback cases pass.
   Do not reduce input coverage to avoid the missing file.
6. Actual installed-wheel CLI probes reproduce the corrected case on Windows
   and Linux. Retain original failed-wheel and corrected identities separately.
7. Repeat the interrupted Claude walkthrough without removing the draft's
   evidence declaration. Complete the second-checkout cycle and retain the
   stop before publication. CLI results do not verify Codex Windows desktop.

## Checks and retention

Run focused regression and atomicity tests, applicable full source suites,
distribution/CLI checks and changed-payload release qualification under
VER-RLS-036/037. A CI merge commit or earlier candidate is not interchangeable
with the corrected exact candidate.

Retain actual argument arrays, cwd, runtimes, output/exit codes, input/result
digests, installed identities, review and handoff under evidence/WO-RLS-043/.
No credentials or fabricated evidence files. Bind verification to the exact
clean candidate and leave acceptance to the human.

## Limits

These checks cover tested Windows/Linux filesystem and workflow behavior.
They do not establish missing desktop results, hosted service behavior or
public delivery. Preserve every skip and unrun case.
