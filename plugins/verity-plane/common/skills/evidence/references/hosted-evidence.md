## Private lifecycle test copy

Test VRECs and RLSs belong only to the explicit hosted rehearsal. Keep the hosted
baseline B, source fixture commit S, disposable Git candidate P and actual
implementation candidate C distinct. A test record binds P; it does not verify C.
Use `remote export --test-copy --destination NEW_DIRECTORY` with the exact immutable
baseline request. Preserve the exported bytes and Git bundle. An incomplete marker
or failed hash check prevents replay. Report independent replay separately from
download success; real assurance still requires its own Git record and human decision.

Before preparing or assessing a test record, read the current released section:
`docs/engineering/harness/VERIFY_OUTCOME.md` for a VREC, or
`docs/engineering/harness/RELEASE.md` for an RLS, with its applicable
`AUTHORITY.md` prerequisite. For a refusal or uncertain reply, read
`docs/engineering/harness/RESULTS.md`. Resolve these from the selected released
resources. Use the current evaluator result; do not reconstruct lifecycle rules.

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

