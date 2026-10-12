# Claude graph-read discovery and reporting diagnostic

All seven graph reads passed. Claude followed the new direct read-guide link and
constructed a successful relationship query. One instruction-discovery gap remains:
it did not read the evidence guide before writing its report. Full lifecycle
qualification remains incomplete; the longer run was not started.

Candidate: `24b83dda747de8476b3030d456d083025c6ce96c`. Claude Code 2.1.273 used
`claude-opus-4-6`, candidate plugin 0.2.7 and client 0.22.2 with released evaluator
0.22.1. This was a fresh private project, with the unchanged canonical fixture.
Git remains authoritative. These are test observations, not human verification.

| Assessment | Observed result |
| --- | --- |
| Instruction discovery | Setup, hosted selection and hosted reads were read before graph queries. The two public Cypher references were read. The required evidence guide was not read before reporting. |
| Seven read tools | `revision`, `work-context`, `compare`, `impact`, `lineage`, `check` and `cypher` succeeded. All seven responses exactly matched independent HTTP reads at the same immutable baseline. Each reported complete content and no continuation or unresolved reference. |
| Cypher | Claude selected a `DECLARES` traversal from WO-P3-900. It returned three actual relations and the requested column aliases. The earlier false claims that relationships are unsupported or aliases mandatory did not recur. |
| Report accuracy | The report identified its one failed native file read, the successful correction, zero MCP failures and the limited self-comparison. The pre-report call count was identified as a snapshot. It omitted the exact implementation candidate C and source links for general capability claims required by the unread guide. |
| Write boundary | Exactly one fixture import advanced the project from version 0 to 1. No draft, lifecycle, export or publication action was attempted. All indexed input bytes and monitored repository/host settings stayed unchanged. |
| Cost | 321.026 seconds, 33 native calls and 142,318 reported peak input-context tokens. This smaller diagnostic is not comparable to the previous full lifecycle run and does not establish a performance improvement. |

The supplied task named outcomes and boundaries. It supplied no query, completed
request, graph answer or workflow sequence. No corrective hint or proctor mutation
was given during the native session. Setup corrected a log-filename lookup and
exhausted private subnet pool before launch; these observations are retained.
The diagnostic containers are stopped and their volumes remain available.

The correction changes only two existing instruction references. The focused
checks passed, the source suite ran 1,337 tests with 24 reported skips, and
distribution checks, CLI smoke, released validation, scope and review preflight
passed. Two pinned builds matched. Both plugin archives contain the exact changed
guide bytes. All 27 service-wheel members and the relevant evaluator, runtime,
database, schema, protocols and dependency locks match the previous service
comparison to VREC-HAG-005. This reuses unchanged service evidence; it does not
claim those service scenarios were rerun or extend prior Codex qualification to
changed guidance.

Next: add a direct reporting handoff to the read procedure and repeat this focused
diagnostic on the new exact package. Run the affected full lifecycle scenario
only after the discovery and report assessment passes. WO-HAG-009/010/011 remain
in progress. No completion, real verification, merge, release, deployment or
host-plugin update is recorded.

## Evidence

- [Visible native transcript](claude-261-visible.md): actual messages and tool
  exchanges, excluding private reasoning and host/system events.
- [Native evidence archive](claude-261-evidence.zip) and
  [digest inventory](claude-261-inventory.json): exact task, input sources,
  requests/results, native reports, instruction reads, independent HTTP matches,
  final status, boundary checks and independent assessment.
- [Build and setup evidence](provenance.zip) and
  [digest inventory](provenance-inventory.json): exact command arrays, identities,
  package comparisons and test drivers. No provider credentials or raw auth logs.
- [Instruction correction and supporting checks](../../WO-HAG-011/discovery31/review.md).
- [Previous full-run and continuation findings](../functional30/assessment.md)
  remain unchanged.
