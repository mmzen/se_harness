+++
id = "VER-HAG-006"
type = "verification"
title = "Independent qualification of the private lifecycle rehearsal"
status = "approved"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"

[relations]
verifies = ["REQ-HAG-011", "REQ-HAG-012", "REQ-HAG-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-06T18:40:36Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the Phase 3 package published in PR #542 at 689dee3b1929e5c58338df1331a0eb9df484ce25. Approves the nine governing definitions and WO-HAG-008, including required commit-bound verification under VER-HAG-006 and its bounded local execution. Git remains authoritative; this is a private test-copy lifecycle rehearsal. Authentication and database ACL implementation remain deferred; existing controls stay. Includes the reviewed bounded publication grant to mmzen/se_harness, source codex/hosted-artifact-phase3, target main, draft PR #542, including the ready record and a later separately supplied verification-decision push. No risk acceptance, actual assurance decision, merge, real authority cutover, release, deployment or host-plugin update is granted."
+++

# Independent qualification of the private lifecycle rehearsal

## Independence

Expected behavior comes from REQ-HAG-011 through 013 and SPEC-HAG-007. Before
implementing the new handlers, retain a small complete test-change fixture and
an operation matrix with expected success/refusal outcomes. Obtain reference
results from separately installed released 0.22.1 on an ordinary disposable Git
repository. Never derive expected lifecycle answers from the candidate service.

The reference run and service use identical starting bytes, source/evaluator
identities and requests. Compare semantic results with only explicitly listed
timestamp/temporary-path exclusions. Exact stored/exported artifact and evidence
bytes are compared by digest with the corresponding command output; they are
never normalized. Preserve all accepted Phase 2 fixture bytes and historical
candidate evidence.

## Environment and invocation

- Primary hosted environment: Linux x86_64 containers, a real Memgraph engine,
  the pinned released evaluator 0.22.1 and separately installed candidate client.
  Windows Docker hosting qualifies this Linux container surface; it is not a
  Windows desktop host-delivery test.
- Record actual Git, Python, operating system, dependency lock, image digest,
  client wheel, service, protocol and database identities. Use separate test
  projects/volumes and synthetic credentials; retain no secrets.
- Extend the existing `server/scripts/qualify.py` and hosted test runner with a
  documented Phase 3 entry. Its concrete command and full argument array belong
  in the retained run evidence. Do not invent an already available CLI flag.
- Build only local non-promotable qualification packages under the proposed work
  order. No public release, registry push or host-plugin installation is required.
- Run `python scripts/run_tests.py`, distribution checks from AGENTS.md, CLI
  smoke, and `python -m unittest tests.test_remote_client tests.test_hosted_artifact_graph tests.test_cli_shape`.
  These support the actual hosted checks below; they do not replace them.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-HAG-011 | test, demonstration, inspection | P3-01, P3-02, P3-08 | Closed released operations complete the walkthrough; explicit test boundary and real-record/publication refusals hold |
| REQ-HAG-012 | test | P3-03, P3-04, P3-05, P3-07 | Full result is atomic, stale inputs fail, retries recover exact results and compatibility holds |
| REQ-HAG-013 | test, demonstration, inspection | P3-01, P3-05, P3-06, P3-08 | Test candidate/history and exact bytes survive capture, export and independent replay |

## Acceptance scenarios

### P3-01 — Complete lifecycle parity

Run the closed operation matrix through the installed client and real service,
and independently through 0.22.1 against the same test fixture. Cover definition
acceptance, work approval/start/completion, open/decided decision, raised risk,
handoff evidence, ready VREC and verification decision, ready RLS and release
decision. Exercise one failing required gate and one unsupported state edge.
Pass only when both runs agree on selected states, exact failed predicates and
required next actions; all side effects are explicitly accounted for. Test
decisions remain test inputs, not human acceptance of the product.

### P3-02 — Authority and operation boundaries

Attempt a lifecycle action without test selection, against imported real records,
with an unknown operation/schema, arbitrary command/`--test-command` input and
unsafe output path. Require refusal with unchanged graph state and no real Git
or external publication effect. Inspect request parsing and subprocess argv;
tests must not invoke a real external publication to prove it is forbidden.
Confirm existing API-key/principal checks, private network restrictions and
constrained Cypher still function. Do not claim authenticated-human or DB-ACL
qualification.

### P3-03 — Complete-result rollback

Exercise a command that produces a record plus evidence and one that affects
multiple linked records. Compare their exact output lists to the released run.
Inject faults after staging, during transactional writes and before receipt
commit. No partial revision, head, evidence or successful receipt may survive.
An unexpected generated path also rejects the whole result.

### P3-04 — Staleness and competing writers

Preview an action, then change an input artifact or dependency. Apply must fail
with no writes. Race two incompatible applies using the same expected versions:
exactly one commits. Repeat its key with identical inputs and then changed inputs;
expect original receipt and explicit conflict respectively. Compare all resulting
versions and byte sets, not only HTTP success codes.

### P3-05 — Unknown reply, restart and restore

Drop a reply after a successful complete-result commit. Recover the same receipt
without rerunning the released mutation. Restart the service and database, then
repeat reconciliation. Restore the test volume into a separate disposable stack
using the documented procedure. Exact records, evidence, Git objects and receipts
must remain available. This proves the tested recovery procedure, not production
power-loss guarantees or RPO/RTO.

### P3-06 — Provenance and exact export

Capture a VREC at clean test commit P and prepare its RLS through the released
commands. Retain the B/S/P manifest and distinguish actual product candidate C.
Make a later rehearsal revision, then export both the earlier and later snapshots.
For each, compare every selected byte and digest, reconstruct Git objects from
the bundle in a fresh directory, and run released validation and selected-record
checks. The original VREC/RLS still names its original candidate.

Remove one required Git object; corrupt an evidence byte; supply an unsafe path
and an existing destination. Each case must fail without overwriting operator
files or claiming a successful export/replay.

### P3-07 — Compatibility and bounded failures

Run the retained Phase 2 v1 wire fixtures, draft/read/MCP regression checks and
the applicable original hosted scenarios on the new candidate. Preserve their
expected behavior. V1 cannot invoke the new lifecycle operations; unsupported
versions fail. Exercise configured input/output bounds and evaluator timeout;
none may leave partial state. Publish the chosen bounds and measured results.

### P3-08 — Packaged operator walkthrough and review

From the documented fresh setup, use the packaged client/service to complete the
single test change, reconcile one uncertain reply, export and replay. Record
the exact command sequence, output, elapsed observations and any intervention.
Review that guidance names the test boundary, retained Git authority and deferred
security. Review complexity against ARCH-HAG-003/ADR-HAG-003; remove unneeded
generality before qualification. No credentials for live Codex/Claude are needed.

## Evidence retention

Retain small manifests, commands, exits, requests/responses, comparison reports,
original failures, retries, all eight scenario outcomes and the final assessment
under `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-008/`. Large packages,
Git bundles or backups need durable immutable locations and digests in those
manifests. Temporary-only paths do not qualify as durable evidence.

Record test Git history and payloads as test fixtures or evidence, never as real
formal repository decisions. Prepare the actual implementation VREC later using
released capture on the clean candidate C and WO-HAG-008. Its ID and evaluator
sidecar path are allocated then. The human must separately verify that result.

## Acceptance and residual uncertainty

All eight scenarios and applicable repository checks must pass for a completion
claim. A skipped, unavailable or unperformed scenario is not a pass. Report any
failed or missing criterion and stop its dependent completion; a different
criterion or deferral requires a reviewed decision.

Authentication, database ACLs, real authority cutover, production operation,
public delivery, host startup/compaction and Codex/Claude desktop qualification
remain excluded. RISK-HAG-001 remains raised. No rehearsal decision accepts it.
