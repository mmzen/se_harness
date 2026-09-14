# WO-KIS-009 implementation evidence

Source candidate: `1bc5c67c1647080d6522dcf012c85ce356e277bf`. Base: `001612615191da499775cebb1a59f65480e9ce4a`.
WO-KIS-009 remains `in_progress` pending the currently installed workflow's
completion decision. No VREC, owner assurance, release or adoption is inferred.

## Result against VER-KIS-003

| Check | Observed result |
| --- | --- |
| A: one execution path | Public CLI tests start new approved work without a delegation table or network, keep the supplied human/agent actor, exercise completion and record capture, and apply approval/scope checks to every actor and selected WO. |
| A: retained boundaries | Missing approval, changed scope, failed gates and an older approval without execution permission refuse the operation. Existing explicit historical grants remain usable. Multi-WO preparation checks each WO and leaves the VREC ready. Owner assurance/release rights remain separate. |
| B: policy and skill review | Candidate DR-015 is the shared permission rule. Templates remove the route switch; machine procedures give direct commands; common skills follow the installed policy without a separate CI test or duplicate routine request. Existing projects use their old procedure until upgrade. |
| B: ordinary task walkthrough | Approve a bounded WO, inspect it, run start preflight, preview/apply start, implement and check it, then preview/apply completion. Required evidence preparation follows approved inputs; `not_required` work needs no new VREC. A person or agent follows this sequence without requiring another agent. |
| C: validation | The final full Windows run passed 1,067 tests with 15 platform/capability skips. The earlier focused run passed 205 tests with 2 skips. All 14 distribution records, CLI help, graph validation, released doctor and start/review preflight passed. Both edited common skills passed structural validation. |

## Simplicity and review

One existing approval check now serves all executors. Removed the optional-class
selector, the output-rewriting overlay, duplicated preparation authority check,
the actor-specific single-WO restriction and the obsolete live-delegation test
runner. The existing contracts, role/operation identifiers and capture machinery
remain in use; no extra service, mode, receipt, signature or CI job was added.
The small new workflow selector honors the existing assurance classification.

Manual review compared requirements with the accepted proposal and traced the
shared check through transition, checkpoint and capture callers. It also walked
both common skill references and the candidate policy/template links. The skill
validator checks structure, not content quality; this review supplies the latter.
This was an implementer review, not an independent agent assessment.

Useful checks were retained. Old tests that expected two routes now check the
single approved path and actual refusals. Test-only fixture approvals reproduce
valid lifecycle chains so unrelated tests reach the boundary they exercise;
production approval is covered separately through the real CLI transition.
Historical bound records and repository-managed installed policy remain unchanged.

## Findings fixed

Initial focused attempts exposed old fixture assumptions, inconsistent lifecycle
history in those fixtures and route-specific expectations. Corrected the fixtures
and preserved the underlying scope, state, coverage and provenance checks.
Removing the decision step also exposed missing corrective text when a transition
evaluated a target-specific structural predicate; it now reports the actual failure.

The first full run found seven failures from the removed delegation table,
completion guidance, the new no-VREC rule and the generated diagnostic index.
Updated the current notes/template tests and regenerated the index. Final review
found completion pointing at apply instead of preview; fixed the step selection
and checked the returned command. The full suite then passed on the final source.
Obsolete coordinator instructions were removed from the current command reference.

Raw outputs and prior attempts remain in the task workspace's `work/kis009-checks/`.
Definition approval/start/preflight and prospective-scope outputs remain in
`work/codebase-kiss-checks/kis009-*`. `checks.json` keeps commands and result summaries;
no new raw-log archive or source export is committed. Existing hosted CI supplies
the supported-platform package results, linked from the PR.

## Current governing boundary

The candidate is 0.18.0; the installed root remains on released 0.17.0. Candidate
doctor reports that expected template, mode, payload and version skew. The released
doctor passes. No candidate command was used to grant authority over this checkout.

Current DR-015 requires execution delegation in the PR base and a successful live
CI check. WO-KIS-009 is new on this branch, so the installed procedure still needs
the owner's completion decision. Its old rule is not replaced by the candidate's
new behavior before release and adoption. The new policy does not rewrite prior
approvals or automatically select all approved work.
