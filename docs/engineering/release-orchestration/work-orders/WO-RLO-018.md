+++
id = "WO-RLO-018"
type = "work_order"
title = "Restore publication with the adopted schema-5 lock"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[assurance]
commit_bound_verification = "required"
rationale = "Required commit-bound verification confirmed by mmzen: publication depends on this trusted parser; verify the correction under VER-RLO-012 in VREC-RLO-015."
decided_by = "mmzen"

[execution_scope]
paths = [
  ".github/scripts/publish_dashboard.py",
  "tests/test_dashboard_publication.py",
  "tests/test_release_orchestration.py",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-018.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-012.md",
  "docs/engineering/release-orchestration/evidence/WO-RLO-018/",
  "docs/engineering/release-orchestration/verification-records/VREC-RLO-015.md",
  "docs/engineering/release-orchestration/evidence/VREC-RLO-015-evaluator.json"
]

[relations]
implements = ["REQ-RLO-001"]
specifications = ["SPEC-RLO-001"]
verification = ["VER-RLO-012"]
architecture = ["ARCH-RLO-001", "ADR-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T03:03:59Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved the reviewed WO-RLO-018 and VER-RLO-012 package, required commit-bound verification and correction review PR. Reviewed hashes WO 4dbc7a9827b2153c0e893b5025c4cc3c42299e9185e6148f1dd88cc7c828fc29 and VER 86a0748254fd8047b76ca4b38acaa75b9accec5727e8d10fceaa8aa199b56ba3. Only confirmed assurance metadata added before preview. Verification acceptance and merge remain separate."
scope_paths = [".github/scripts/publish_dashboard.py", "tests/test_dashboard_publication.py", "tests/test_release_orchestration.py", "docs/engineering/release-orchestration/work-orders/WO-RLO-018.md", "docs/engineering/release-orchestration/verification/VER-RLO-012.md", "docs/engineering/release-orchestration/evidence/WO-RLO-018/", "docs/engineering/release-orchestration/verification-records/VREC-RLO-015.md", "docs/engineering/release-orchestration/evidence/VREC-RLO-015-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-03T03:04:44Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-03T03:54:10Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Restore publication with the adopted schema-5 lock

## Objective

Let the release and Pages publishers resolve the exact authorized release
when the repository uses its already adopted schema-5 evaluator lock.
The RLS-SEH-032 publication preflight currently refuses that valid lock.

Baseline: merged main 01ec43c86c9d30949295c07ac91c742be91e713a.
RLS-SEH-032 stays released at candidate
abbec12ac5524c8adfb28693f846dd59de88f759 with its approved archives.
This is a repository publication-tool correction, not a change to that package.

## In scope

1. Extend the shared lock reader in publish_dashboard.py to recognize integer
   schema 5 with resource_layout = "released-resources-v1" and no conflicting
   skill_ownership declaration. Preserve valid schema-3 and schema-4 support.
2. Keep evaluator version, payload, archive identity, integrity semantics,
   retained evidence, main-history and maintenance fallback checks effective.
   Invalid schema-5 metadata must fail before publication and must not trigger
   a fallback to less reliable inputs.
3. Adjust obsolete tests that classify every schema-5 lock as unsupported.
   Add focused positive and negative cases through the evaluator descriptor,
   evidence binding and both publication resolvers.
4. Rehearse the actual merged release resolution and disposable Pages path,
   retain the original failures and prove all accepted release inputs unchanged.
5. Publish the correction review, obtain verification of its exact commit,
   and hand the integrated correction back to the existing release procedure.

## Expected change surface

One shared publication helper and its two existing publication test files.
No new abstraction, library, workflow or bypass switch is needed. Both entry
points already use the helper, so changing the caller scripts would duplicate
the correction. The named artifacts and evidence paths cover its review,
handoff, generated verification record and exact evaluator companion.

## Authority and assurance

Propose required commit-bound verification because publication relies on this
trusted parser. The human must confirm that classification with approval;
no assurance decision is recorded by this draft.

Proposed approval authorizes local implementation, tests, evidence, completion
and VREC preparation within this scope. It also authorizes ordinary correction
branch pushes and a draft PR to mmzen/se_harness:main, plus the existing
read-only publication rehearsals. Publish the review before requesting human
verification. The exact assurance decision and merge remain separate.

The prior release-execution authorization remains usable for RLS-SEH-032 after
this correction is verified and merged and its publication checks pass. This
draft neither repeats nor broadens that release authorization.

## Out of scope

No changes to evaluator/package source, released RLS/VREC records, bound
evidence, candidate, version, tag, distribution hashes, build recipe, adopted
lock/configuration, workflow permissions, provider settings or ownership policy.
No implementation of the separate release-record owner/preparer issue. No
production publication, tag or deployment by a test. No new release required
solely for these main-owned publication tools. New complete-route activation
and downstream plugin qualification remain separate work.

## Constraints and decision envelope

Use selected released 0.21.0 outside the checkout for real governance.
Use source scripts only as the system under test. Keep preparation material
and disposable repositories outside the checkout; retain only required evidence.
The implementer may choose the smallest parser/test changes meeting the cases.
Do not weaken provenance checks, invent evidence or edit accepted artifacts to
make the publication preflight pass.

## Required verification and evidence

Meet VER-RLO-012. Preserve both observed failure paths. Cover valid and invalid
schema-5 input and legacy compatibility, run Windows/Linux focused tests,
the full Windows suite, the real release and disposable Pages rehearsals, and
the existing hosted read-only release replay. Retain inputs, runtimes, results,
preservation hashes and the implementation review under evidence/WO-RLO-018/.
Capture proposed VREC-RLO-015 only after checking its availability again.

## Stop and escalate conditions

Stop the affected action if another implementation file is needed, the accepted
release identity must change, a required check fails, source code must run with
publication credentials, or the correction would need a new policy exception.
Inspect uncertain remote effects before retrying. Preserve all failed checks.

## Completion report format

Report the exact correction commit, the supported lock formats, actual tests
and resolver/replay results, preserved release identity, remaining publication
conditions and the evaluator's next human decision. A passing rehearsal is
not a claim that the evaluator or plugin has been published.
