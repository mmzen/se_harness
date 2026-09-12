+++
id = "WO-CIP-010"
type = "work_order"
title = "Prevent background Git maintenance from racing disposable repository cleanup"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-12"
updated = "2026-09-12"

[assurance]
commit_bound_verification = "required"
rationale = "CI and fixture cleanup behavior affect the reliability of candidate evidence used by later assurance and integration decisions."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "repository_tools/upgrade_rehearsal.py",
  "tests/git_support.py",
  "tests/test_git_support.py",
  "tests/test_upgrade_rehearsal.py",
  "docs/engineering/ci-pipeline/work-orders/WO-CIP-010.md",
  "docs/engineering/ci-pipeline/verification/VER-CIP-006.md",
  "docs/engineering/ci-pipeline/evidence/WO-CIP-010/",
]

[relations]
implements = ["REQ-ECP-012", "REQ-TST-004"]
specifications = ["SPEC-ECP-007", "SPEC-TST-002"]
verification = ["VER-CIP-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T10:11:29Z"
decided_by = "engineering-owner"
reason = "Approve both and proceed"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-12T10:12:25Z"
decided_by = "engineering-owner"
reason = "Approve both and proceed: explicit approval response authorized implementation of WO-CIP-010, hosted Linux/Windows CI, and the separate repair PR."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-12T11:17:25Z"
decided_by = "engineering-owner"
reason = "mark **WO-CIP-010 implemented**."
+++

# Work Order: Prevent background Git maintenance from racing disposable repository cleanup

## Lifecycle

The operator approved this WO and VER-CIP-006 and authorized implementation,
Linux/Windows CI, publishing the repair branch and opening its separate PR:
"Approve both and proceed". The released evaluator applied approval and start.
The operator then explicitly requested "mark **WO-CIP-010 implemented**."
The released evaluator applied that completion decision after passing gates
and confirming all 17 checks on candidate bed6b2a96ae22bb4deabe143a923b99e7b26e45a.
Verification-record preparation and assurance remain separate decisions.

## Objective

Prevent automatically launched Git maintenance from outliving disposable CI
repositories, while retaining strict cleanup and the real evaluator handover.

## In scope

Baseline: main `0114707723f565bfdef85e8e74f7e0fef5f402a9`.
[Issue #269](https://github.com/mmzen/se_harness/issues/269) records the same
Linux teardown symptom and was closed as unreproducible. PR #456 reproduced
the `.git` directory-not-empty failure in both attempts of run 34686202700,
jobs 103533661141 and 103533878695. Preserve those failures as observations;
their logs alone do not establish the responsible process.

1. Diagnose Git process lifetime on disposable exports and retain a controlled
   positive control that actually launches automatic maintenance.
2. Disable automatic maintenance and automatic garbage collection only in the
   rehearsal's newly initialized repository and the shared fixture Git launcher.
   Apply the rehearsal configuration before staging or committing any file.
3. Add deterministic regression coverage for inherited maintenance settings,
   no post-command maintenance writers, setup failures and strict cleanup.
4. Exercise the existing local checks and normal Linux/Windows candidate lanes.
   Candidate wheels, if needed, are ephemeral, explicitly non-promotable, and
   built outside the checkout solely for existing package acceptance.
5. Prepare a separate repair PR and retain compact evidence under this WO.
   Publishing the repair branch and opening its PR require the repository
   owner's explicit instruction; they are included in the approval request.

## Out of scope

No cleanup retry, swallowed exception, ignored cleanup error, removed test,
changed evaluator verdict, background process kill, machine Git configuration,
replay reduction, release, merge, or historical evidence rewrite. Plugin
qualification and the accepted C10/C11 limitation remain separate scopes.
Do not modify the verified candidates or VREC-PLG-012 and VREC-PLG-013.

## Authorized decision envelope

After approval and start, choose bounded helper and regression-test details.
Use `gc.auto=0` and `maintenance.auto=false` as disposable Git settings.
Keep shared fixture behavior in its existing support module. No architecture
relation applies: no active architecture addresses the selected requirements.

## Constraints

Temporary-directory cleanup errors continue to propagate and remain measured
as failures. Keep command timeouts, evaluator isolation, exported HEAD,
semantic result/digest, two replays and cross-platform agreement unchanged.
Only disposable Git setup and the corresponding timing stages may change.
No secret-bearing environment dump or user configuration write is allowed.

## Expected change surface

The rehearsal module, shared fixture Git helper, their two test modules,
this WO, VER-CIP-006, and this WO's evidence directory.

## Required verification

Pass VER-CIP-006 with the isolated released 0.17.0 evaluator governing the
checkout. Execute AGENTS.md's required checks. Record candidate-source managed
template skew separately from released evaluator integrity.

## Evidence to record

Record exact source heads, tested merges, run/job/attempt identities, commands,
runtime versions, process traces, positive controls, test results and failures.
Keep large raw logs and exports outside the checkout; retain hashes and links.
Before/after observations must distinguish Windows local analysis from Linux CI.

## Stop and escalate conditions

Stop before exceeding these paths or changing cleanup/error semantics. Stop
on a required failure or evidence contradicting the proposed mechanism, and
retain the observations. Historical release replays may still run old fixture
code; report that limitation rather than rewriting a released commit.

## Completion report format

Report the mechanism established by each control, actual platform results,
remaining uncertainty, exact candidate identity and WO state. Obtain the
released evaluator's handoff. Completion, VREC preparation, verification and
integration remain distinct decisions.
