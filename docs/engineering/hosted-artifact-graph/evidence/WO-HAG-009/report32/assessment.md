# Claude reporting-route correction

Claude read the required graph and evidence guides in this fresh diagnostic.
All seven read tools succeeded, but the report still made a false claim about
Cypher relationship support. The full lifecycle rerun remains pending.

Candidate: `1e9a1a10a3f1fab5b71ea29476c6f0d12ff27556`. Claude Code 2.1.273 used
`claude-opus-4-6`, plugin 0.2.7, client 0.22.2 and released evaluator 0.22.1.
The task, fixture and permissions match claude-261 except for fresh run paths.
The guidance correction adds a direct link from hosted reads to the evidence
guide. It changes no service behavior, permissions or qualification criterion.

| Assessment | Observation |
| --- | --- |
| Discovery | Passed for this read/report task. Setup, hosted selection, hosted reads, hosted evidence and both public Cypher references were read before their selected actions. |
| Graph reads | Seven successful tool responses and one Cypher refusal exactly matched independent HTTP. Every successful response was complete. Self-comparison does not test a non-empty diff. |
| Report | Failed. Claude claimed that Cypher only supports single-node matches. Its rejected query omitted the required relationship variable: `-[:DECLARES]->`. The implemented grammar admits named relationships, and the previous fresh diagnostic successfully traversed `-[d:DECLARES]->`. A syntax refusal does not establish a general capability limit. |
| Failure counts | One native file read and two instruction lookups failed; one service query was refused. The final reply called these three failures while listing all four. The captured summary's three tool-level errors exclude the service refusal returned as ordinary MCP content. |
| Boundary | Only one fixture import advanced the project from version 0 to 1. No lifecycle, draft, export or publication action was attempted. Indexed inputs and monitored host/repository state stayed unchanged. |
| Cost | 325.133 seconds, 35 native calls, 146,202 reported peak input-context tokens. No performance success is claimed. |

Unlike the previous report, this report names the exact implementation candidate C,
fixture S and baseline B, and identifies test candidate P as unknown. Its observed
data and recovered error categories are retained. Its unsupported general claim
still fails the independent content assessment.

The public query guide describes a labelled path but does not explain that
relationships require variable names. The next bounded correction will state
that existing syntax and clarify the meaning of error counts. No parser, query
permission or service change is needed. Repeat the focused native case before
starting the longer lifecycle run.

Supporting checks passed: 40 focused tests; source suite with 1,337 tests and 24
reported skips; distribution checks, CLI smoke, released validation, scope and
review preflight. Two pinned builds matched. Exact packaged guide bytes and the
unchanged service components were checked. Earlier service evidence is reused
through the retained comparison to VREC-HAG-005; it was not rerun here.

No live corrective hint, supplied query, operator mutation or workflow sequence
was given. The diagnostic containers are stopped, with their volumes preserved.
WO-HAG-009/010/011 remain in progress. This result grants no real verification,
merge, release, deployment or host-plugin update. Git remains authoritative.

## Evidence

- [Visible native transcript](claude-271-visible.md).
- [Native evidence archive](claude-271-evidence.zip) and
  [digest inventory](claude-271-inventory.json): task, reports, exact calls and
  results, instruction reads, independent HTTP comparisons and boundary checks.
- [Build/setup evidence](provenance.zip) and
  [digest inventory](provenance-inventory.json).
- [Two-line correction and checks](../../WO-HAG-011/report32/review.md).
- [Prior diagnostic and successful relationship query](../discovery31/assessment.md).

Private reasoning, host/system events and credentials are excluded from published
evidence. Original observed report bytes and prior verdicts remain unchanged.
