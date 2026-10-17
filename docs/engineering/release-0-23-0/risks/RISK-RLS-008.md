+++
id = "RISK-RLS-008"
type = "risk"
title = "Open instruction findings in the 0.23.0 release"
status = "accepted"
owners = ["mmzen"]
created = "2026-10-16"
updated = "2026-10-16"
description = "R23-NATIVE-010: Codex read communication instructions after its first English update in one read-only trial. R23-NATIVE-011: two disposable new-work drafts omitted generated verification-evidence destinations. These defects can produce an explanation before required guidance is read or another scope correction before verification. Functional graph, package and seeded execution checks passed; neither finding is fixed."
action = "Keep both findings open for mmzen, retain the exact failures and compensating evidence, and prepare a bounded correction before the next plugin release or any claim that these cases pass. Do not treat incomplete work-order scope as authority to write outside approved paths."
raised_by = "operator"

[relations]
threatens = ["WO-RLS-046", "WO-RLS-054"]

[disposition]
option = "accept"
label = "Carry only the stated qualification limitations in evaluator 0.23.0 / plugin 0.2.7; preserve failed and unverified results and open follow-up."
decided_by = "mmzen"
decided_at = "2026-10-16T11:21:40Z"
reason = "Human mmzen: \"continue the release, mark the findings as open items\". Applies to disclosed R23-NATIVE-010 and R23-NATIVE-011 for evaluator 0.23.0 / plugin 0.2.7 only. Continue preparation with both remediation items open and original failures unchanged; carry their residual risk for this release. Desktop omission, final verification, merge and exact complete-release approval remain separate. Decision SHA-256 6df7709f84d1935d50db11092c4d4a808d9f3b4224fdcbd798b7702e1282db45; risk SHA-256 03eba8b5e8f432709fcb83b32f60987d636cb068c4f96d78fdd6ab16b3c4d276."
revisit = "Before the next plugin release or any claim that these cases pass, whichever occurs first; changed product bytes, versions or scope require renewed review."


[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-16T11:13:24Z"
decided_by = "operator"
reason = "Recorded by harnessctl raise-risk."

[[lifecycle_events]]
from = "raised"
to = "accepted"
decided_at = "2026-10-16T11:21:40Z"
decided_by = "mmzen"
reason = "Human mmzen: \"continue the release, mark the findings as open items\". Applies to disclosed R23-NATIVE-010 and R23-NATIVE-011 for evaluator 0.23.0 / plugin 0.2.7 only. Continue preparation with both remediation items open and original failures unchanged; carry their residual risk for this release. Desktop omission, final verification, merge and exact complete-release approval remain separate. Decision SHA-256 6df7709f84d1935d50db11092c4d4a808d9f3b4224fdcbd798b7702e1282db45; risk SHA-256 03eba8b5e8f432709fcb83b32f60987d636cb068c4f96d78fdd6ab16b3c4d276."
+++

# Risk: Open instruction findings in the 0.23.0 release

## Description

R23-NATIVE-010: Codex read communication instructions after its first English update in one read-only trial. R23-NATIVE-011: two disposable new-work drafts omitted generated verification-evidence destinations. These defects can produce an explanation before required guidance is read or another scope correction before verification. Functional graph, package and seeded execution checks passed; neither finding is fixed.

## Next action

Keep both findings open for mmzen, retain the exact failures and compensating evidence, and prepare a bounded correction before the next plugin release or any claim that these cases pass. Do not treat incomplete work-order scope as authority to write outside approved paths.
