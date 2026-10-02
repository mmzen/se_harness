# Release preparation observations

The selected 0.20.1 evaluator passed identity and doctor. Human mmzen approved the
seven-file release package and required assurance. The evaluator applied exactly
those seven approvals, then started WO-RLS-031. WO-RLS-032/033 remain approved.

The first scope call mistakenly supplied a directory as a changed file. It failed
QGP-G4I-PATHS with WEX201. A corrected call supplied actual and planned files and
passed, without changing approved scope. The original and corrected outputs are
retained outside the repository under work/reconcile-minimal-20261001 as
release021-planned-scope.json and release021-planned-files-scope.json.

The delivery plan is a preparation plan. Future RLS, candidate and package hashes
are null until produced. It is not yet a valid completion-check input. Preserve
this version when a later bound plan is retained. No result is fabricated.

The twelve product/correction work orders and WO-RLS-031 will require one final
aggregate VREC. Prior VRECs retain their candidate identities. VER-IAR-021's Codex
Windows desktop criterion remains unverified and required. No waiver is recorded.

The adoption drafts were committed separately on work/adopt-0-21-0 at 7efaac96.
They are not release-member work or part of this candidate diff. No root adoption,
instruction deletion, plugin publication or release action has occurred.

## Local review and checks

The final local Windows source run passed 1,211 tests with 20 skips. The first
run failed only the README size limit (671 words against 650). The approved
paragraph was shortened to 643 words; 16 onboarding and 20 progressive-documentation
tests then passed, followed by the full rerun. Eight package-guidance tests,
delivery checks (one platform skip), distribution validation and artifact
validation also pass. The original and retry commands and outputs are in
[local-checks.json](local-checks.json). These are worktree observations before
commit-bound capture, not final assurance.

Diff review found no runtime or workflow changes. Both manifests select 0.2.4;
current public facts remain 0.20.1/0.2.3. The marketplace README's activation
links now target the actual packaged setup guides. The existing guide test
asserts the approved identities; no new test framework or behavior was added.
The required desktop observation remains pending.

An integration-procedure override was refused with WEX220 because this work
is in progress. Fresh focus selected PROC-WO-IMPLEMENT. Its pre-action check
then required an evidence header (QGP-G4I-EVIDENCE). The evaluator wrote the
handoff and pre-action headers at the approved evidence paths; the matching
pre-action and proposed PR checks passed. No work-completion transition was
applied. Headers and a passing scope check do not establish missing host evidence.
The original results remain in work/reconcile-minimal-20261001 with the
release021-push-preaction and release021-selected-preaction prefixes.

The chat host directory has no selected installation. The explicitly selected
release030-main checkout and its exact external 0.20.1 evaluator were confirmed
again before continuation. Manual reading does not prove automatic host delivery.

GitHub readback confirms repository mmzen/se_harness, main at the preparation
base, and no existing work/release-0-21-0 ref or PR. Active main rules require a
PR and validate check, disallow deletion and non-fast-forward updates, and permit
role bypass only through PRs. Classic branch-protection returned 404 because
this protection is a ruleset. Workflow defaults are read-only; approval of PR
reviews by workflows is disabled. The authorized push creates only the review
branch, and the PR remains draft. Manual rehearsals have contents:read and no
publication credentials. These controls do not authorize merge or publication.
