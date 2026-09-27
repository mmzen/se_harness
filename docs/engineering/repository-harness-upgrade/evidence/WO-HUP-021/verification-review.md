# Adoption verification assessment

The repository and its private evaluator now select released SE Harness 0.19.0.
The development source is 0.20.0. The implementation tested at full scale is
`0b40d1a1eb6994508fd9d629c0bdca16e2c6e0c2`. This assessment prepares verification; it is not human acceptance.

## Acceptance cases

| Case | Observed result | Evidence |
| --- | --- | --- |
| ADOPT01 | Passed: the root and all 25 conditional guides match the published wheel, and instruction routing tests pass. | checks/contract-inspection.json; checks/installed-entry-comparison.json; checks/corrected/full-suite.result.json |
| ADOPT02 | Passed for this adoption: exact public evaluator, integrity, formal graph, qualification and both selected review preflights pass. The named-human start defect and approved recovery are recorded below. | checks/corrected/doctor.result.json; checks/corrected/validate.result.json; checks/corrected/released-root-qualification.json; checks/corrected/review-preflight.result.json; checks/corrected/review-preflight-023.result.json |
| ADOPT03 | Passed: only recognized legacy fragments were retired by the installer; the reviewed owner edit was applied separately; the empty CLAUDE.md was removed; the second upgrade had no pending content writes. | owner-edit-map.md; AGENTS.proposed.md; AGENTS.after-installer.txt; upgrade-applied.json; adopt019-upgrade-noop.json; checks/contract-inspection.json |
| ADOPT04 | Passed on the declared Windows Codex CLI/app-server surface: native startup and manual compaction delivered the exact planned root before retirement. The isolated profile has the 0.2.0 plugin enabled and trusted for the actual repository. | native-delivery/observation.json; native-delivery/setup-summary.json; native-delivery/startup.events.json; native-delivery/compact.events.json; instruction-delivery.json; retirement-approval.json; checks/installed-entry-comparison.json |
| ADOPT05 | Passed: the single upgrade transaction binds the previous root to the released wheel; the predecessor assessor accepts it; accepted historical records remain unchanged. | ../WO-HUP-021-evaluator-upgrade.json; checks/corrected/predecessor-assessment.json; checks/contract-inspection.json |
| ADOPT06 | Source and evaluator checks passed. The complete change-set handoff is retained separately before completion. Hosted Linux and Windows checks remain required before integration. | checks/corrected/full-suite.result.json; checks/corrected/evaluator-facts.result.json; checks/corrected/distributions.result.json; checks/corrected/candidate-cli.result.json; completion-change-inventory.json; combined-handoff.json |

All paths in the table are relative to this evidence directory. The preserved
32-check inspection and native evidence apply to the corrected candidate:
the correction changes only the CI version, one test link, and governance/evidence
records. No installed instruction, native trace or delivery asset changed.

## Implementation review

The owner edit removes the harness instructions while preserving repository
commands and source facts from the reviewed proposal. Installation uses the
public wheel and its existing migration; no new installer behavior was added.
The two development version declarations preserve the existing requirement
that the candidate version is newer than its governing evaluator.

The three adoption test corrections keep legacy fixtures and replace only old
root assumptions. The full suite then exposed the stale CI pin and fourth test
link. The approved correction changes those two lines without weakening a test,
job, gate or permission. Updating the two references is the smallest complete
implementation. No new abstraction or product feature is needed.

The first full run failed two of 1,125 tests, with 16 skips. It is retained in
checks/full-suite-before-correction.json. The successful full rerun and the
57 targeted correction tests are retained separately. Earlier qualification
and command-invocation failures are also retained with their successful retries.

## Approval recovery and released limitation

The agent followed AUTHORITY.md by recording WO-HUP-022's approver as the
requesting human. Released 0.19.0 accepted that approval but refused start:
QGP-G3-SCOPE / WEX-ECP-022 requires the literal engineering-owner value.
There is no supported correction or repeated approval transition.

The human explicitly authorized rejection of WO-HUP-022 and approval of
WO-HUP-023 with required assurance. The evaluator applied both decisions.
WO-HUP-022's earlier approval and failed start remain unchanged. WO-HUP-023's
approval uses the required legacy encoding and identifies the actual human
and decision in its reason. Start passed under that recorded approval.
The two-line implementation belongs to WO-HUP-023. The rejected order is not
claimed as completed or included as verified work. See ../WO-HUP-023/ for the
exact decision, transition and failure evidence. This work does not fix the
released instruction/evaluator identity mismatch.

## Limits

Native evidence proves Windows Codex CLI/app-server startup and manual
compaction in the isolated rehearsal. The installed entry was compared locally
with the proven bytes. No Codex desktop, automatic threshold-compaction, macOS,
or new Claude demonstration is claimed. The global plugin remains unchanged.
An additional native probe against the actual checkout was not run: automatic
approval review rejected possible transmission of repository context to an
external service. The required isolated proof and local byte comparison were used.

The 16 platform skips remain visible. Hosted Linux and Windows checks have not
run for this branch and must pass before integration. The 52 unrelated graph
warnings are not adoption findings or accepted risks. Published locked guide
whitespace is preserved; no formatter is configured as a required check.

No verification decision, push, pull request, merge or publication is recorded
by this assessment.
