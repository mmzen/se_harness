# Verification requested: evaluator 0.22.0

The release candidate combines clear approval and verification requests,
complete scope preparation, review publication before verification, and the
prospective complete-release procedure. Plugin source manifests select 0.2.5.

Candidate: `abbec12ac5524c8adfb28693f846dd59de88f759`. Record: VREC-SEH-032, ready.
Review PR: https://github.com/mmzen/se_harness/pull/528

## Evidence

- The final Linux full source suite, package-assembly tests and distribution
  checks pass. Windows capture uses a temporary checkout of that same candidate.
  Complete-candidate qualification and the 1,255-test source suite passed there.
  The successful retry retains those exact source results and reruns the affected
  package-assembly checks, qualification, distribution validation and CLI smoke.
- Hosted checks pass for the review candidate. The manual branch-head run
  passes both release rehearsal legs and delivery/recovery fixtures. The exact
  pinned recipe produces identical wheel and source archives twice.
- Installed wheel and named/index-selected source-distribution checks pass.
  Two local and both hosted platform upgrade runs have the same semantic digest.
  Their package/source inputs match the final candidate; only release evidence
  and the work-order completion event were added after package qualification.
- qualification-review.md maps the five required contracts. The final record
  covers exactly the ten work orders named by REL-SEH-034. Its capture output
  binds the final hosted/Linux receipt, and the raw archive retains the driver
  and commands. Earlier failures remain in qualification-raw.zip.

## Limits

The first two capture attempts used interpreters with installed SE Harness metadata
outside the candidate checkout (the governing evaluator and an older global package).
The identity check correctly refused that metadata (RID018). The corrected test
command uses a fresh isolated environment with no installed SE Harness package;
released 0.21.0 still governs capture itself. Both failed attempts remain in the
archive and created no verification record.

The third attempt passed source qualification and all 1,255 source tests, then
package-assembly tests correctly refused the clean interpreter's lack of an
installed evaluator. Those fixtures require the selected released interpreter
for their isolated wheel-payload checks. The retry uses that interpreter for
package tests and preserves the clean source environment for source qualification.
It retains the already-passed source results at the same immutable commit;
no product file or accepted test was changed. The third refusal is also retained.

Windows source tests retain 22 skips and Linux retains 2. The platform-specific
link checks run on Linux. No skipped result is called a pass.

Installing a local `.tar.gz` file directly still hits the existing wheel-only
PEP 610 provenance restriction. Installing the same sdist by name/version from
a package index passes; wheel installation also passes. This release does not
claim direct-file sdist support or fix that existing restriction.

Native Codex/Claude, desktop and public marketplace qualification remain in
WO-RLS-035/036 after evaluator publication. They are not claimed here and earlier
release-specific accepted omissions are not reused. The new complete-release
route requires separate adoption and reviewed provider activation.

## Decision

“Verify result” accepts this exact candidate and retained evidence against the
agreed release verification contracts. It does not merge the PR or decide the
release record. After verification, the agent will apply and push that decision,
then prepare and replay RLS-SEH-032 for the separate release decision already
specified in the approved package.
