+++
id = "VER-PLG-027"
type = "verification"
title = "Verify public installation, update and delivery closeout"
status = "draft"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"

[relations]
verifies = ["REQ-PLG-041"]
+++

# Verify public installation, update and delivery closeout

## Independence

Expected results derive from REQ-PLG-041 and SPEC-PLG-023,
the human-verified package identities, and the separately authorized public
operation. Do not derive expected identities from the live cache being assessed.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-041 | inspection, demonstration, test | Candidate phase: PUB-01, PUB-02, PUB-03 candidate, PUB-04 pending result | Public native routes work; proposed status text is accurate; the report correctly leaves unmerged documentation incomplete. |
| REQ-PLG-041 | inspection, demonstration | Delivery phase: PUB-03 public readback, PUB-04 final result | Public source guidance matches the accepted candidate and all five surfaces have matching evidence. This later receipt is not a condition for the earlier VREC. |

## Entry conditions

Package and guidance work have eligible human-verified coverage. The public
operation has separate explicit authorization and an observed remote result.
Readback uses that exact commit. These conditions do not arise from approving
this contract or its work order. Public tests are later acceptance obligations,
not a circular condition for the earlier local qualification decision.

## Cases

- **PUB-01 — Publication identity.** Read the public branch commit, parentage,
  PACKAGE-IDENTITY.json, both catalogs and package digests. Confirm an ordinary
  descendant of the reviewed old public ref and exact equality with the accepted
  assembled content. Record moved refs or mismatches as failures.
- **PUB-02 — Public native routes.** For Codex and Claude Code, install from the
  actual public ref in a fresh disposable profile. In another profile seeded
  with the retained public 0.1.0 distribution, follow the documented update path.
  All four routes must actively load 0.2.1/0.19.0 with matching package bytes.
  On both hosts, retain real startup and compaction root delivery. A local source,
  cached package or reported version alone does not pass. Record actual versions,
  login/trust prerequisites, model overrides, failures and bounded claims.
- **PUB-03 — Availability.** Inspect current public instructions against PUB-01
  and PUB-02. Update only allowed status/availability text and evidence links.
  Run public-onboarding checks. Source updates require their own authorized PR;
  observe that integration before claiming the documentation surface complete.
- **PUB-04 — Completion.** Finalize the existing delivery plan and hash-bound
  observations. Include public fresh/update proof for both hosts, documentation
  readback and demonstration evidence. Read back the unchanged 0.19.0 evaluator
  and release markers and record compatibility review. Run the existing
  `check_release_delivery.py` with its three file/path arguments and `--json`.
  Before status-text integration, expect an incomplete result naming the missing
  documentation readback. After that integration, all five surfaces must be
  satisfied. Removing one required observation or
  supplying a conflicting identity must prevent completion. Preserve previous
  results; never turn a missing host run into a pass or a quiet deferral.

## Retention and authority

Retain actual arguments, output, timestamps, Git identities, installed digests,
native root delivery, final plan bytes, observations and result under the selected
public-confirmation WO. Use the released 0.19.0 evaluator for graph, scope,
handoff and exact-commit VREC preparation. Human verification and any later Git
write remain separate decisions. A supplied-evidence summary is not an independent
authentication of remote observations or human review.

The VREC may assess the status-text candidate before its merge. Keep overall
delivery explicitly incomplete until the public documentation readback in PUB-03
exists. Retain that final readback as the separately authorized delivery receipt;
do not rewrite an accepted VREC or its bound evidence to append it.
