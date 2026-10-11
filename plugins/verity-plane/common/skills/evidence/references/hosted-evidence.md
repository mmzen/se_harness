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

For each report claim, inspect its exact request/result or exported manifest.
Use the actual operation and outcome fields, not a filename, earlier summary or
remembered sequence. Distinguish `previewed`, `accepted` and `refused`.
Name identities in full: hosted input baseline B, source fixture commit S,
test Git candidate P, and actual implementation candidate C. If an identity is
not established by the cited evidence, report it as unknown. Never substitute
the fixture commit for the candidate bound in a VREC or RLS.

Keep the report short: outcome, exact evidence path/field, and remaining limit
for each required case. Keep detailed requests/results in their evidence files.
Do not infer missing reads, independent replay or complete coverage from a
successful operation or process exit. A later read does not prove that a required
procedure was read before the earlier action.
