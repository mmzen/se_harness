# Project connection and maintenance

The owner approved the revised packet and explicitly authorized WO-PLG-009 on
2026-09-15. The released 0.17.0 evaluator recorded its definition approvals and
start. WO-PLG-022 completion is recorded on the parent branch; no VREC is inferred.

## Result against VER-PLG-009

| Outcome | Observed result |
| --- | --- |
| Connect a project | A real-wheel walkthrough prepares the checker, previews/applies init, replaces an edited disposable skill copy and gets a passing doctor. Owner notes remain unchanged; the provider is portable. |
| Repair and explicitly upgrade | Reuse and repair keep the same environment and project configuration/lock. A project initialized by released 0.17.0 is explicitly upgraded to the development 0.18.0 checker, then switched to plugin skills with a passing doctor. |
| Actual failure boundaries | Existing ownership/setup tests retain missing replacements, prerequisite failures, interrupted work and unsafe-path refusal. A new regression covers a real Windows wheel metadata failure found during this walkthrough. |

The walkthrough ran 16 real commands. Expected initial missing-harness and pre-upgrade
version-mismatch results are retained as nonzero; they were not counted as healthy
project checks. The final doctor calls pass. The independent expectations are the
requested provider, preserved owner bytes and explicit version-change boundary.

The full suite passed 1,068 tests (15 skipped), including the CRLF regression;
the focused subset passed 22 tests (2 skipped). Distribution validation, released
doctor/graph/review preflight and CLI help passed. The setup skill passed structural
validation. Native host acceptance belongs to WO-PLG-016.

## Simplicity and findings

The common setup skill routes to short connection and maintenance references.
No setup runtime change was needed: existing init, skill-ownership, upgrade and
repair commands provide the behavior. The only production edit accepts ordinary
CRLF wheel metadata in the existing development assembler. The selected scope
records why that compatibility repair was necessary. One regression checks the
actual build result, rather than the metadata parser's internal implementation.

The first local build attempt lacked setuptools in the chosen Python installation;
the available bundled build Python produced the non-promotable test wheel. The first
assembly rejected its CRLF metadata; the fixed assembly and complete walkthrough
then passed. No test or required check was disabled.

The wheel uses committed runtime/template inputs from the parent candidate. Plugin
instructions and assembly use this implementation's working files. Both hosts receive
those same common files. This is development acceptance, not a released plugin or
a live repository migration. See [commands and results](checks.json). Raw local
logs and disposable fixtures remain under work/plugin-remaining-checks and
work/plugin-connect-acceptance-20260915 outside Git; hosted checks remain on the PR.

The owner approved completion and the released evaluator recorded WO-PLG-009
as implemented. Required verification preparation follows; no assurance, release
or live adoption is recorded.

## Completion approval

The owner said: "i approve WO-PLG-009 and WO-PLG-016" after the completed
implementation handoff. That approval is recorded for this work order.
[Hosted results](ci-implementation.json) identify the tested implementation PR
head; subsequent completion/preparation edits change engineering records only.
