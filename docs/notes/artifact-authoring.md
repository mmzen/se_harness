# Artifact authoring

Write what someone needs to understand, implement and check the change. The harness
does not count words, sentences or code references, and does not require `SHALL`.
Candidate checklists live in `templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md`.
The installed root policies remain governed by the currently released checker.

A requirement needs a non-empty statement and an acceptance condition: an example,
a measure, verification notes or a linked verification contract. An intent explains
the desired outcome; a capability says what the actor can do; a specification gives
the behavior and meaningful failure cases. Draft hints about missing summaries or
ambiguous rule references help review but do not block approval.

Unfilled placeholders, invalid references and unresolved blocking decisions still
need attention. Owner approval remains an explicit lifecycle decision.

For handoff evidence, a work order may list ordinary repository files in top-level
`evidence_paths = ["docs/engineering/product/evidence/WO-PRD-001/checks.md"]`.
Files must exist, contain evidence and stay inside the repository. No special header
is required. Generated headers still work and may include descriptive text fields.

`harnessctl check . --artifact WO-PRD-001` shows the next action. A `pre-action`
checkpoint selects the procedure automatically; `--procedure` is only an optional
override among the selected rule's alternatives. PR declarations accept LF and CRLF.
Literal filenames such as `src/check[1].py` are accepted; native path separators are
normalized at the CLI boundary. Paths outside the repository are refused.

Keep owner instructions brief enough to read easily. Length is review advice,
not a byte limit or a failing test; the managed fragment is checked independently.
