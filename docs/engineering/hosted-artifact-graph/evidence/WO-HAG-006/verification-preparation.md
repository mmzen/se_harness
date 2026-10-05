# Aggregate verification preparation

Released evaluator 0.22.1 prepared VREC-HAG-003 in ready for candidate `4414eaf5d9739978654c55390b96aeac32699ed4`.
It covers implemented WO-HAG-005/006 and VER-HAG-004/005. The sidecar binds
21 retained evidence files; each matches its exact candidate blob.
The public evaluator is outside the checkout. The capture command used a fresh
candidate check in a separate temporary checkout and an empty source-test venv.
Its retained checks prove unchanged tested files, original-base assessment,
old verification bindings and successful complete-candidate qualification.

See preparation.zip for exact commands and results and review.md for the
criterion assessment. Capture applies no assurance decision. The later review
commit contains this record, its evaluator evidence and preparation material;
it does not alter the assessed candidate or bound evidence.

WO-HAG-001 remains in_progress. Hosted service scenarios remain unperformed.
The next operation is authorized publication to existing draft PR #535,
then the separate human verification decision. Required CI must pass before merge.

The generated VREC retains one CRLF in captured Windows command stdout.
The whitespace check accepts CR at line end for that protected log; no captured
record or evidence byte was normalized or rewritten.
