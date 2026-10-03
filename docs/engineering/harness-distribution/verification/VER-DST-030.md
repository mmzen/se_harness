+++
id = "VER-DST-030"
type = "verification"
title = "Verify the four-mebibyte topology amendment"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[relations]
verifies = ["REQ-DST-062", "REQ-DST-063"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T03:35:59Z"
decided_by = "mmzen"
reason = "mmzen explicitly authorized the reviewed bounded manual amendment to exactly 4 MiB, preservation and links for the previous accepted definitions, the two-file correction and required verification. This records that supplied instruction; the manual amendment exception does not waive lifecycle gates or human assurance. The approved RLS-SEH-032 candidate and archives remain unchanged."
+++

# Verify the four-mebibyte topology amendment

## Independence

The expected target is the owner's exact 4,194,304-byte decision. Use the
retained 2,099,060-byte failure and 2,097,049-byte merged-main baseline as prior
observations. Selected released 0.21.0 governs lifecycle outside the checkout;
source tests assess the candidate. Read predecessor hashes from the reviewed
proposal and approved release hashes from the unchanged records.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-DST-062 | test | Candidate constant is exactly 4,194,304. Below/equal/above boundary observations remain strict. Real topology is within that target without removed fields or data. |
| REQ-DST-062 | inspection, test | All eleven predecessor byte digests and archive links match. Only the reviewed topology target, candidate assertions and bounded capacity wording change. Shell, summary, content, schema, integrity and publication boundaries remain unchanged. |
| REQ-DST-063 | test | Dashboard tests pass on Windows and Linux. Repeated generation at one commit is byte-identical. Full source suite and applicable PR CI pass; branch and PR-merge measurements are retained. |

## Checks

Run python -m unittest tests.test_dashboard_webui on Windows and Linux.
Run python scripts/run_tests.py --workers 4 --scale full on Windows and
retain hosted source-suite results. Use the existing topology boundary tests
and deterministic whole-bundle test; do not replace the current repository
with a smaller fixture. Generate the bundle twice at the branch candidate,
retain exact sizes and hashes, and inspect the hosted PR-merge result.

The existing installed-package CI must pass. In a disposable installation of
the candidate package, assert the installed target equals 4,194,304 and exercise
the below/equal/above boundary. This package is test material, not a release.

Compare RLS-SEH-032, VREC-SEH-032, both evaluator companions, bundle, lock and
configuration against their original hashes. Preserve all prior evidence.
Run released validation, complete scope, review preflight and handoff for the
combined correction. Capture VREC-RLO-015 at a clean exact candidate only after
all required checks pass. Publish the review before requesting human verification.

## Evidence retention and residual uncertainty

Retain compact command/result summaries, actual runtimes/import origins, tested
commits, predecessor/archive digests, topology measurements, preserved release
hashes and CI artifact links/expiry under evidence/WO-DST-028/. Keep raw CI logs
in their declared downloadable artifacts. The 4 MiB target provides headroom,
not proof of unbounded scale or browser performance. A further increase or
topology partitioning needs a new decision.
