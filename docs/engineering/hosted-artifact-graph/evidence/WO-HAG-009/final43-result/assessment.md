# C43 native lifecycle qualification

Both hosts pass NQ-01 through NQ-05 at candidate `f0d042d69e025bdab284695e7e17667eeb38eaf3`.
The earlier C42 failures remain unchanged. This is evidence for this exact candidate,
not acceptance of a later package or a real verification decision.

| Observation | Claude Opus 5.5 | Codex CLI |
| --- | --- | --- |
| Native wall time | 1,435.934 seconds | 1,574.220 seconds |
| Native calls / observed items | 188 calls, complete capture | 239 observed items; attempted-call total unavailable |
| Provider peak input context | 631,067 tokens | unavailable |
| Accepted lifecycle operations independently replayed | 12 | 12 |
| Native exports independently reconstructed | 2 | 4, including two intermediate review exports |
| Exact MCP/HTTP comparisons | 7 tools | 7 tools |
| Captured failed items, retained and reported | 8 | 8 |

Both agents authored their own definitions, included the generated decision path
in approved work scope, used test-owner for REL definition approval, and kept
release-owner for the RLS decision. Both completed assertion, risk/decision,
handoff, work completion, verification and test release. Original imported records
and source bytes were preserved. Stale/out-of-scope requests committed no effects.
Lost replies were recovered by original key; identical retries retained the receipt
and changed requests were refused. Exact export/replay preserved the original test
candidate in each VREC/RLS. Repository and monitored host settings were unchanged.

The independent assessments are inside the per-host archives. They separate
manual content review from automated receipt, file and released-evaluator replay.
All previous errors remain in the visible transcripts. No procedural hints,
operator workflow mutations or hidden workflow completion were supplied.

The separate focused first Claude diagnostic still fails; see
[focused assessment](../../WO-HAG-011/focused43-result/assessment.md).
It prevents the remaining focused sequence. Do not infer overall completion.

CI at this candidate also fails the deterministic integration-package build:
its exact source tar is 542,105,600 bytes, above the configured 536,870,912-byte
limit. Retained CI and size evidence are in provenance.zip. No evidence was deleted
and no limit or build-source selection was changed. A separate bounded correction
requires scope approval. Harness handoff remains incomplete while qualification
and required checks remain unfinished.

Costs are observations from concurrent disposable sessions, not isolated benchmarks.
Desktop, automatic instruction delivery, public installation, production service,
authentication/database ACL work and real Git authority cutover remain outside scope.
No human verification, merge, release or deployment is claimed.
