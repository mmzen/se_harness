# HAG reconciliation progress — correction required

WO-HAG-005 remains in_progress. This is observed progress, not a completed
assessment or verification request.

- The exact reviewed main release/adoption commit was merged, retaining both histories.
- SPEC-HAG-003 and VER-HAG-001 use public evaluator 0.22.1 through the exact
  explicitly approved linked revisions. Their earlier bytes and lifecycle histories are preserved.
- DEC-HAG-001 now records mmzen's existing extend-evaluator choice with actual
  decided_by=mmzen and authority_owner=engineering-owner. WO-HAG-001 ownership is unchanged.
- The Windows integrated source suite passed: 1,311 tests, 23 reported skips.
  The tested source commit is in progress.json. Subsequent changes are decision,
  index and evidence material; no test result is claimed for the proposed CI correction.
- All seven actual released validate-draft probes passed against the exact
  historical source projection. Root-selection overlay bytes are separately recorded.
- Distribution checks, CLI smoke, evaluator identity and artifact validation passed.
- 134 pre-existing HAG files and 180 reviewed transport paths match their required bytes.
  VREC-HAG-001/002 and their bound evidence remain unchanged.

## Required checks still blocked

1. Local replay of the repository's predecessor-assessment plan fails at the
   original PR base: `trusted base must contain exactly one released distribution
   for the target version`. That base predates 0.22.1. Merely changing it would
   change the reviewed boundary. A read-only comparison confirms that main's
   existing transaction binds the original base lock to the selected target.
   This comparison is design evidence, not a passing full assessment.
2. Combined check-pr refuses `QGP-G4I-EVIDENCE` for WO-HAG-001. The exact reviewed
   definition changes make its old snapshot header stale. No historical packet
   has been overwritten. Proposed DEC-HAG-003/WO-HAG-006 preserve its complete
   prior bytes before a supported rebind and explicitly amend VER-HAG-004's
   preservation wording for that single live packet.

WO-HAG-005's individual scope check passed. Complete PR scope/handoff is not
reported as passed while the combined check is blocked. The draft correction
package validates with zero errors and has no uncovered planned paths.

## Retained failures

The first merge had two extra add/add conflicts because the approved revisions
had already changed the HAG copies. The two sides were proved to be the exact
reviewed replacement and its preserved original; the reviewed replacement was
retained. The index retained both sets of entries. No new behavioral conflict
resolution was invented. Imported historical CRLF/patch whitespace findings
were preserved with exact main bytes; newly authored whitespace checks passed.

The initial reference projection was not a Git checkout. Released artifact
creation refused WEX-ECP-013. Adding actual local source refs and the historical
HEAD/index to the disposable projection allowed supported ID allocation; all
seven probe results then passed. The first predecessor invocation correctly
refused an uncommitted evidence file; its clean committed rerun exposed the
separate missing-base-release issue above. Original command failures remain
in reconciliation-checks.zip alongside corrected runs.

## Limits and continuation

Zero hosted scenarios have run. WO-HAG-001 remains in_progress and RISK-HAG-001
remains raised. No VREC was created, no completion was recorded, and no remote
branch or PR was changed. PR #535 remains draft at its existing target.
Approve the separate bounded correction before implementation of that scope;
then rerun applicable gates and prepare aggregate verification for review.
