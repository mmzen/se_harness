# Adoption acceptance assessment

Assessed by Codex under WO-HUP-003, WO-HUP-005 and WO-HUP-026 against
VER-HUP-003. Trusted change baseline:
695d6773dc86f25691a9799e969bcca014207837.
This assessment reports observations; it is not human verification acceptance.

| Criterion | Observed result | Retained evidence |
| --- | --- | --- |
| A0210-01: released identity and plan | Passed. Public wheel and payload match released 0.21.0. The reviewed migration names exactly the 44 retired copies. | target-identity.json; reviewed-migration-preview.json; review-inputs.json |
| A0210-02: replacement delivery before retirement | Passed for Codex CLI 0.159.2 with released plugin 0.2.4, using the isolated proposed-state copy and the exact target-bound receipt. Startup and compaction delivered the same entry; mmzen accepted the traces before apply. | native-delivery-v2.json; startup-trace.jsonl; compact-trace.jsonl; instruction-delivery.json; native-review-accepted.json |
| A0210-03: migration and preservation | Passed. Atomic installer receipt selects 0.21.0/schema 5/released-resources-v1; 28 managed and 16 explicitly selected stock copies retire. Other tracked bytes were preserved at apply. Later edits fit the separately approved union. No-op preview changes no content. | ../WO-HUP-003-evaluator-upgrade.json; preservation.json; preapply-files.json; postapply-noop.json; ../WO-HUP-026/preservation-after-correction.json |
| A0210-04: usable repository | Passed locally. Identity, doctor, validation, resource resolution, authoring preview, root qualification, distribution and CLI checks pass. 49 documentation/compatibility tests, 32 governor tests and the corrected 1,218-test full suite pass. The actual clean-commit predecessor assessment passes. | postapply-authoring-preview.json; corrected-source-summary.json; ../WO-HUP-005/corrected-predecessor-facts.json; ../WO-HUP-026/source-checks.json; ../WO-HUP-026/schema5-actual-assessment-result.json; ../WO-HUP-026/schema5-actual-doctor.json; ../WO-HUP-026/schema5-actual-validation.json; ../WO-HUP-026/schema5-actual-qualification.json; ../WO-HUP-026/schema5-distribution.json; ../WO-HUP-026/schema5-cli-smoke.json |
| A0210-05: exact candidate | Passed local scope/handoff and completion for all three work orders. The combined check covers 171 changed paths. Clean-candidate capture follows; its generated VREC and evaluator companion record the exact commit and full-suite result. Hosted Linux/Windows CI is not yet run for this unpublished branch and remains required before integration. Human acceptance remains separate. | adoption-combined-handoff-final.json; adoption-completion-apply.json; the three handoff packets; VREC-HUP-025 and its evaluator companion after capture. |

## Review of the combined change

The installer owns selection and copy retirement; no lock or lifecycle history
was edited manually. AGENTS.md, GLOSSARY.md, formal history, integrations other
than the approved CI version pin, and product templates remain intact. Current
owner guides use the selected resource lookup. Source tests inspect distribution
assets; separate released-resource checks prove adoption. Historical references
remain unchanged. The development version 0.21.1 is not published.

The two-line schema recognition extension plus layout checks preserves the
assessment trust boundary; the regression tests exercise supported predecessors,
invalid layout/ownership, wrong receipts, unknown schema and unexplained drift.
No new resolver, policy copy or dependency is introduced. Material findings were
the stale documentation/test assumptions and the schema-5 assessment refusal;
the approved corrections resolve both. Original failures remain retained.

## Applicability and limits

Migration/native receipts describe the earlier reviewed installation operation.
The subsequent guide, test, development-version and assessment-script changes
do not alter its selected lock, released resources, public plugin, startup entry
or canonical transaction. The final verification record binds retained evidence
to the complete candidate and includes a fresh full-suite capture.

Claude and Codex Windows desktop are unverified by this adoption. CLI traces do
not prove desktop delivery. The chat's parent-directory startup gap is not
relabeled as a passing native result. The exact checkout and released evaluator
were selected manually before governed continuation. The 21 suite skips and 58
unrelated validation warnings confer no waiver. No push, PR or merge has occurred.
