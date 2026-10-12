+++
id = "VER-IPK-002"
type = "verification"
title = "Verify a fixed 1 GiB source archive budget with existing protections"
status = "approved"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

[relations]
verifies = ["REQ-IPK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T07:49:46Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Ok continue\" after the explicit request to approve WO-IPK-002 and VER-IPK-002, required commit-bound verification and inclusion in draft PR #543. Approves the reviewed three-line correction: fixed source-archive/expanded-total cap from 512 MiB to 1 GiB and two matching test lines, preserving all other protections and historical evidence. Authorizes bounded local execution, checks, evidence, completion and verification preparation, and ordinary review pushes/updates in mmzen/se_harness from codex/hosted-agent-qualification to main, including the ready record and later separately supplied verification decision. Keep PR #543 draft while qualification or verification is incomplete. Human verification, merge, release, deployment and changes beyond this scope remain separate."
+++

# Verify the integration archive capacity correction

## Independence

REQ-IPK-001 and SPEC-IPK-001 define exact-commit extraction, independent builds
and provenance. WO-IPK-002 proposes the explicit 1 GiB capacity within that design.
Tests use declared sizes and independently constructed TAR members, not candidate
output as their expected result. Historical 512 MiB observations remain unchanged.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-IPK-001 | test, inspection, demonstration | CAP1-CAP4 | The complete exact source builds within a fixed 1 GiB limit; unsafe/oversized input remains refused and the same wheel passes independent platform checks |

## Acceptance cases

| Case | Procedure | Pass condition |
| --- | --- | --- |
| CAP1: fixed capacity | Run tests/test_integration_package.py on Windows; inspect the two-file diff | MAX_ARCHIVE_TOTAL is exactly 1,073,741,824 bytes; both file and expanded-size checks use it; no override or automatic growth |
| CAP2: preserved boundaries | Run existing hostile archive, member-count, member-size, file-budget and expanded-budget tests | Archive > bound and expanded total > bound fail before extraction; 128 MiB member, 20,000 entries, links, traversal, duplicate and empty-archive rules keep their existing behavior |
| CAP3: real exact source | Count/hash the final committed Git archive and run the existing PR candidate workflow | Archive and expanded total are <=1 GiB, members <=20,000; source export includes all committed evidence; both deterministic builds match and same-byte Windows/Linux integration verification and retention pass |
| CAP4: regression and scope | Run source suite, distribution and CLI checks, released validation, scope/review/handoff checks | Required checks pass; only approved paths change; original failures/evidence and governing definitions retain their exact bytes |

Use declared large sizes in small fixtures rather than allocating a GiB merely
to exercise the refusal. The real candidate supplies the actual >512 MiB success
case. Candidate CI is the Linux/Python 3.11 build and Windows/Linux verification
environment; local Windows Python checks are supporting evidence, not a substitute.
Released evaluator 0.22.1 governs the real work outside the checkout.

## Evidence retention

Keep concise reports, command arrays/cwd/exits, exact commits and CI run/job IDs,
archive counts/digests and check logs in evidence/WO-IPK-002/. Large disposable TARs,
environments and copied repositories remain outside Git. Retain original failure
and prototype setup failures beside later passes. No credentials or environment dump.

Prepare commit-bound verification for the exact implementation candidate. The
record's human acceptance is separate from tests, implementation or publication.

## Limits and simplicity review

Worst-case source extraction disk capacity doubles. This does not promise faster
builds or solve indefinite evidence growth. Reuse the existing parser, tests and
workflow; add no framework, source-selection mode, new gate or production surface.
A skipped or unavailable required CI leg remains pending.
