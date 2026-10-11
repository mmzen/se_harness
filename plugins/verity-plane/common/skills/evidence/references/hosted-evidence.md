## Private lifecycle test copy

Test VRECs and RLSs belong only to the explicit hosted rehearsal. Keep the hosted
baseline B, source fixture commit S, disposable Git candidate P and actual
implementation candidate C distinct. A test record binds P; it does not verify C.
Use `remote export --test-copy --destination NEW_DIRECTORY` with the exact immutable
baseline request. Preserve the exported bytes and Git bundle. An incomplete marker
or failed hash check prevents replay. Report independent replay separately from
download success; real assurance still requires its own Git record and human decision.

Before preparing or assessing a test record, use the exact current-action selector
in [Lifecycle instructions](../../change/references/hosted-test-lifecycle.md#read-the-current-procedure).
Read that released section and its applicable prerequisites. Use the current
evaluator result; do not reconstruct lifecycle rules or load all later stages.
When a supplied helper restricts commands, its tool index gives the export
spelling; the direct-client example above does not add permission or helper flags.

Before release preparation, read the selected REL and final verified VREC.
Compare the REL's `candidate_commit`, if present, with the VREC's exact candidate.
A mismatch blocks preparation. Preserve both accepted records and report the
required contract correction; do not edit either binding to make them agree.

### Report observed results

Before reporting, inspect the exact request/result or exported manifest for each
claim. Use its operation key, action and outcome fields. Keep approval, start,
verification and release as separate observations when their requests are separate.
Distinguish `previewed`, `accepted` and `refused`. A receipt lookup proves that
lookup; an identical retry requires a recorded resubmission and matching receipt.

State observed behavior separately from supported behavior. A refused query
establishes the refusal of that query. Read the public query contract before
claiming that a label, property or relationship is unsupported, or that a clause
is required. Link the source for a general capability claim; otherwise omit it.

Include material failures, recovered errors, permission denials and uncertain
effects. Identify whether the host, client or service refused the action. Use a
captured call summary for counts when available; do not estimate from memory.
If the capture is incomplete, say which result or count remains unassessed.

Name identities in full: hosted input baseline B, source fixture commit S,
test Git candidate P, and actual implementation candidate C. If an identity is
not established by the cited evidence, report it as unknown. Never substitute
the fixture commit for the candidate bound in a VREC or RLS.

Keep one short row per assessed case: outcome, exact evidence path/field, and
remaining limit. Keep detailed requests/results in their evidence files. When
correcting an earlier report, check each affected claim and preserve its original
bytes. A corrected claim does not make other unchecked claims accurate.
Do not infer missing reads, independent replay or complete coverage from a
successful operation or process exit. A later read does not prove that a required
procedure was read before the earlier action.
