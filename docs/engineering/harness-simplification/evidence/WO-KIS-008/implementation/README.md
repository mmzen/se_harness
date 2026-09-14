# WO-KIS-008 implementation evidence

Source candidate: `fd91636743ab7c8e8cd8df3395a438a1e14ef566`. Base: `e1eb96bf0909d9fdb62a177657af343dc24e9286`.
The owner explicitly approved completion of WO-KIS-008 and the released evaluator
recorded it as `implemented`. All hosted checks for PR head `fe33643d7300a5c9cb4e63c72bf75e8f2220cbb8`
passed or were intentionally skipped; `ci-implementation.json` retains their URLs.
Verification preparation follows this completion decision; no assurance decision is recorded.

## Result against VER-KIS-002

| Check | Observation |
| --- | --- |
| A: policy and routes | One candidate ARTIFACT_AUTHORING.md owns the generic rule and questions. Existing templates, router and common skills route to it. Review covers necessary requirements as well as implementation. |
| B: installed behavior | Disposable-target CLI tests print the installed policy's type checklist, observe a seed edit in later output, and distinguish requirement from specification questions. Start and review list the installed policy; preflight remains read only. |

The shared rule respects each project's agreed users, scale and quality constraints.
It accepts justified prevention, weighs costs to users and operations, and asks for a
proportionate rationale. In the CSV example, direct export can meet the small need;
agreed large resumable exports can justify background work. The rule therefore permits
different designs without prescribing one technology or relying on prior plugin mistakes.

Review found no need for a new component or abstraction. The runtime diff adds one
existing-policy path to the reading list. Template and skill links reuse the current
checklist reader. The verification template makes unused sections optional. There is
no new score, field, receipt, CI job, gate, lifecycle state or review actor.

The work-order template regression now compares unchanged metadata instead of carrying
historical wording exceptions. Existing authoring tests check the actual installed
route, and the preflight test covers both normal phases. No new test method or scenario
matrix was introduced. Common plugin sources serve both host packages; both affected
skills passed the skill-creator validator. That validator checks structure, not review
quality; the content inspection above supplies the latter assessment.

## Validation

- Expanded focused suite: 53 tests passed.
- Final full Windows suite: 1,063 tests passed, 15 platform/capability skips.
- Candidate and released graph validation passed; existing maintenance warnings remain.
- All 14 release distribution records validated; CLI help passed.
- Released 0.17.0 doctor, start/review preflight and scope checks passed.

`checks.json` retains commands and result summaries. Local raw output remains under
`work/kis008-checks` in the task workspace. The existing CI workflow retains its own raw
artifacts; no source tree or new raw-log archive is added to Git.

## Findings fixed during verification

The first focused run found an HTML guidance comment interpreted as an unfinished
placeholder by a test and an old router-reading expectation. Guidance became an ordinary
template pointer and the test now expects the explicit policy route.
The first full run found the old routing label and work-order prose comparison, plus
three fixture failures because a wording edit overlapped the run. After those corrections,
the complete suite ran again on the settled source commit above and passed. The failed
full-run output and summary remain in local `full.attempt-1.*` files.

## Adoption and remaining decision

Candidate source is 0.18.0; the real root remains governed by isolated released 0.17.0.
The policy reaches existing projects, including SE Harness itself, through a later
ordinary release and explicit upgrade. Editable guidance/templates require an explicit
replacement choice; a plugin update alone does not adopt the policy.

The owner approved the proposal, explicitly started implementation, and then approved
completion after reviewing the finished change and passing checks. The released 0.17.0
evaluator recorded that completion decision. Its next step requests the preparation
decision for one ready VREC. No VREC or assurance decision has yet been recorded;
merge, release and live adoption remain separate.
