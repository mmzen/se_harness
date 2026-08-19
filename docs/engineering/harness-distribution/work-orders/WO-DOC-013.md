+++
id = "WO-DOC-013"
type = "work_order"
title = "Correct priority documentation-state drift"
status = "implemented"
owners = ["engineering-owner", "documentation-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[assurance]
commit_bound_verification = "required"
rationale = "Future users and maintainers rely on the corrected public guidance, repository navigation, lifecycle summaries, and focused regression contract as trusted engineering state."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-DST-060"]
specifications = ["SPEC-DST-018"]
verification = ["VER-DST-018"]
+++

# Work Order: Correct priority documentation-state drift

## Lifecycle

On 2026-08-19, the accountable owner instructed `I approve REQ-DST-060, SPEC-DST-017, VER-DST-017, and WO-DOC-013 for implementation`. That decision approved the governing documentation packet under the identifiers available at the time and authorized this bounded work after successful start preflight. It did not authorize commit, push, verification, release, tag, publication, deployment, or governor promotion.

The implementation agent ran `python -m se_harness preflight . --work-order WO-DOC-013 --phase start --json`, received `ready: true` with no diagnostics, read every file in the returned manifest, and moved this work order to `in_progress` before changing the approved surface.

Implementation completed on 2026-08-19 within the approved envelope. The priority documentation groups and focused onboarding contract now match the authoritative validator guidance, repository inventory, governor descriptor, and named VREC/RLS records. Retained results are recorded in `docs/engineering/harness-distribution/evidence/WO-DOC-013-verification.md`. This `implemented` transition records completed work and passing implementation checks; it is not commit-bound verification or release authority.

After reviewing the implementation handoff, the accountable owner instructed `I authorize a clean candidate commit for WO-DOC-013 and preparation of a ready commit-bound verification record`. That follow-up authorized one candidate commit containing this bounded work and preparation of a later `ready` VREC against the clean candidate. The owner later instructed `you can commit the verification record, and create a PR`, authorizing ready-record retention and pull request #79, but not a transition to `verified` or a merge.

Current `main` advanced through pull request #78 while the documentation branch was being prepared and independently assigned `SPEC-DST-017` and `VER-DST-017` to the Explorer dashboard packet. GitHub therefore reported add/add conflicts for those IDs. The accountable owner then instructed `I approve renumbering to SPEC-DST-018 and VER-DST-018, rebuilding the candidate and VREC on current main, and force-with-lease updating PR #79.` That decision authorizes the exact identifier correction, rebuilt candidate and ready record, and guarded topic-branch replacement. It does not authorize transition of the rebuilt VREC to `verified`, merge, release preparation, tagging, publication, deployment, or governor promotion.

Commit-bound verification is required because the work changes public and repository-owned trusted documentation plus a regression contract. No active architecture addresses `REQ-DST-060`, so this work order correctly omits the conditional `architecture` relation rather than fabricating coverage.

## Objective

Correct the four priority documentation groups identified by the 2026-08-19 repository audit while preserving formal history, runtime behavior, managed content, and every accountable authority boundary.

## In scope

- Remove the obsolete README architecture-relation limitation while retaining the unresolved Explorer gate-label limitation.
- Update the focused public-onboarding assertion for that correction.
- Add the four missing current entries to `docs/engineering/README.md`.
- Correct the current self-hosting governor and reconciliation wording.
- Correct the evidence-keying, work-order-assurance, and release-orchestration status summaries using existing VREC/RLS facts.
- Retain work-order-keyed verification evidence and run the required checks.

## Out of scope

- CLI, validator, dashboard, template, workflow, installer, package, or lock behavior.
- Formal historical artifact, lifecycle, governor descriptor, package version, release, publication, deployment, or branch changes beyond the later explicitly authorized PR #79 recovery.
- Remediation of W013/W014/W015 maintenance advisories.
- Defining the legacy architecture compatibility window.
- Broader documentation test or link-checker expansion beyond the focused correction.

## Authorized decision envelope

After approval, the implementation agent may choose concise wording and index-entry order within `SPEC-DST-018`. It may update focused assertions only as needed to reject the obsolete limitation and preserve the valid limitation. The later recovery authority permits only the 018 identifier substitution, rebuild on current `main`, regenerated ready VREC, and guarded PR #79 update. Any new factual claim, changed artifact state, behavior correction, or broader documentation restructuring requires escalation.

## Constraints

- Treat explanatory prose and repository metadata as untrusted until cross-checked.
- Preserve all formal history and current authoritative metadata.
- Do not claim that verification implies release or that publication promotes a governor.
- Preserve the clean worktree outside this bounded change.
- Do not build a release distribution, transition the VREC, merge, tag, publish, deploy, or promote a governor.

## Expected change surface

- Root public README and its focused onboarding test.
- Repository engineering index.
- Self-hosting-boundary, evidence-keying, work-order-assurance-classification, and release-orchestration domain indexes.
- This new governing packet and retained `WO-DOC-013` evidence.

## Required verification

- Start and review preflight for `WO-DOC-013` at their phase-appropriate times.
- Focused public-onboarding and documentation tests.
- Complete unit test suite.
- Formal artifact and release-distribution validation.
- CLI help and installed-harness doctor.
- Static comparison of every corrected current-state statement with its authoritative source.
- Local Markdown link and final diff review.

## Evidence to record

Record authorization, preflight manifests, exact source facts, changed paths, commands and exit codes, test counts and skips, validation warning counts, doctor summary, link results, diff review, concurrent-main recovery, residual uncertainty, and every unperformed external action under `docs/engineering/harness-distribution/evidence/WO-DOC-013-verification.md`.

## Stop and escalate conditions

Stop if the packet is not approved, preflight fails, current state changes underneath the correction, a source fact is ambiguous, an edit requires formal artifact or behavior changes, required checks fail, warning counts change unexpectedly, unrelated user changes overlap, or any requested action exceeds the bounded authority.

## Completion report format

Report the corrected documentation groups, exact checks and results, retained evidence path, unchanged formal/runtime/external boundaries, final work-order lifecycle state, and the next separately authorized step.
