# Phase 3 lifecycle rehearsal — verification assessment

The implementation passes all eight scenarios in VER-HAG-006. It completes the
engineering lifecycle in an explicit private test copy. **Git remains authoritative
for real work.** Human verification of this implementation is pending.

Tested product source: `345557d20e83f1c6ed72e11460ee4ba451cf3d91`. The client is unpublished 0.22.2, service
0.1.0.dev1 and plugin guidance 0.2.7. The service uses the unchanged public
evaluator 0.22.1 in its separate environment. [Component identities](component-manifest.json)
bind the exact wheel, service image, dependency locks, plugin archives and two
matching pinned Linux client builds. The later actual verification record also
contains the assessment/evidence and implementation-completion state; the [source
binding report](source-binding.json) checks that these later changes do not alter tested product bytes.

## Delivered behavior

- Closed typed requests inspect gates, change selected test lifecycle states,
  record risk/decision effects and prepare test verification/release records.
- Complete artifact, evidence, Git snapshot, head and receipt effects commit in
  one Memgraph transaction. Failed or stale requests expose no partial result.
- Exact retained receipts recover uncertain replies. Export reproduces selected
  history and bytes in a new destination and preserves the test candidate.
- Existing v1 authoring/reads and the seven read-only MCP tools remain supported.

## Qualification

The installed Windows client called real Linux service and Memgraph containers.
Independent reference commands used the same released evaluator on ordinary Git
clones of each exact input. [Starting-input proof](starting-inputs.json) also
compares the first clone's 19 files with independent source/draft fixture bytes.
No candidate service supplied the expected lifecycle answers.

| Scenario | Result and evidence |
| --- | --- |
| P3-01 — Complete lifecycle parity | **Pass.** Eleven accepted lifecycle operations and two independent refusals agree on states, exact predicate results, next typed actions and complete changed-path sets. Archive: `walkthrough04/; replay04/parity.json; replay04/commands.json` |
| P3-02 — Authority and operation boundaries | **Pass.** Missing test selection, imported state change, reader write, unknown schema/operation, arbitrary command input and unauthenticated v2 calls refuse. Seven HTTP/MCP reads match and are explicitly labeled test data. Archive: `commands/p3-store04.json; commands/store04.json; extra04/; walkthrough04/` |
| P3-03 — Complete-result rollback | **Pass.** Record-plus-sidecar and paired risk/decision mutations each roll back at five injected points. Missing sidecar and unexpected output refuse. Whole-store fingerprints and absent receipts prove no partial effects. Archive: `commands/store04.json` |
| P3-04 — Staleness and competing writers | **Pass.** Exactly one competing write wins; identical key returns the original receipt and changed content conflicts. Changing a selected draft invalidates the earlier preview even with refreshed version numbers. Archive: `commands/store04.json; commands/stale-artifact04.json` |
| P3-05 — Unknown reply, restart and restore | **Pass.** A dropped post-commit response is unknown; receipt recovery and identical retry do not rerun it. Process restart and quiesced backup/restore preserve logical state, exact records, history and receipts at the recorded cutoff. Archive: `transport04/; recovery04/; commands/recovery-receipts.json` |
| P3-06 — Provenance and exact export | **Pass.** Older and later snapshots reconstruct exact Git trees with original candidate objects. Released validation/checks pass. Corrupt evidence, truncated Git history, unsafe paths, existing destinations and Linux link parents refuse. Archive: `walkthrough04/early-export/; walkthrough04/final-export/; replay04/; commands/store04.json; commands/p3-export-negative-linux.json` |
| P3-07 — Compatibility and bounded failures | **Pass.** All 60 retained v1 wire checks, 18 installed-client steps and 52 additional live boundary observations pass. Seven legacy MCP reads match HTTP. Input, output, projection and evaluator time limits refuse without partial writes. Archive: `v1compat02/; commands/p3-v1-wire.json; commands/store04.json; commands/p3-runtime-packaged02.json` |
| P3-08 — Packaged walkthrough and review | **Pass.** Exact packaged service/client completes the 61-step walkthrough, uncertain-reply recovery and independent replay. Both candidate plugin archives contain the selected guidance. No live host-delivery claim. Archive: `walkthrough04/; transport04/; replay04/; commands/p3-focused03.json; package02/` |


All archive paths in the table refer to [qualification-observations.zip](qualification-observations.zip).
[Its inventory](observation-inventory.json) lists each member's exact digest.
[Machine assessment](verification-results.json) maps every scenario to evidence.
The retained bundle contains selected required observations and test Git bundles,
not copied working checkouts or environments. It also includes the quiesced test
database backup. [qualification-packages.zip](qualification-packages.zip) preserves
the exact client wheel/sdist, service wheel and two non-promotable plugin archives.
Credentials were excluded and the retained bytes were scanned for test tokens.

Comparison asserts released command arguments, exits, selected states, predicate
IDs/results, next typed actions and complete changed-path sets. Incidental generated
timestamps and temporary absolute paths differ between independent commands;
their derived record digests are not semantic equality assertions. Stored/exported
bytes are never normalized: their hashes match the actual hosted command result
and ordinary Git tree, including original verification candidate objects.

## Checks and measurements

- Source suite: 1,323 tests, 23 reported skips, exit 0; the skips are unperformed.
- Focused client/CLI/package checks: 60 tests, one configured real-setup skip.
- Installed service runtime: nine tests pass, including snapshot immutability.
- v1 wire contract: 60 checks pass; distribution checks: 23 records pass; CLI smoke passes.
- Released validation before retention: 1,983 artifacts, zero errors, 63 existing warnings.
- Two pinned Linux client builds produce identical wheel and sdist bytes.
- Walkthrough: 61 command steps; 88.530 seconds summed command time.
- Fault/boundary suite: 25 cases; evaluator timeout observed at 121.124 seconds.
- Restart: 3.217 seconds; restore: 3.353 seconds.
  Both match the acknowledged cutoff at project version 29.
  A separate changed-artifact refusal test runs afterward, explicitly outside that cutoff.

## Review findings and corrections

1. Prototype source `c46de689385e8349f50d3b422294f1b6aedf8ca1` reached capture,
   but a shared candidate list changed the earlier snapshot after hashing. The
   transaction refused and rolled back. The corrected snapshot copies those inputs;
   the regression checks both hashes and the final live capture passes.
2. The prototype Git bundle lacked a default HEAD. Explicit branch selection
   worked, but ordinary clone did not. The corrected bundle retains HEAD and its
   branch. Independent ordinary clones and object checks now pass.
3. The first test expected work approval to require accepted definitions; released
   0.22.1 did not refuse that preview. The test now uses a real out-of-scope handoff
   and unsupported state edge, each independently reproduced. No gate policy changed.
4. Early local test placement required service dependencies in the standard-library
   suite; those cases now run with the installed service runtime. A package assertion
   also required identical headings unnecessarily; package tests check exact source
   guidance bytes instead. Original failed outputs remain in the archive.
5. Docker's automatic address pool was exhausted. Fresh task-owned stacks use
   inspected unused private subnets. Other stacks/volumes were preserved. A local
   inventory helper initially assumed every network had IPAM entries; it was corrected
   before creating the stack. The initial failed observation remains retained.
6. Windows could not create the link fixture or copy back a Linux symlink. The test
   passed in the Linux container; its JSON result was copied separately. The Windows
   unperformed observation and failed copy remain visible; neither is counted as a pass.

Review traced each operation through a closed schema, fixed released command,
complete file-effect comparison and one guarded transaction. Imported records
remain immutable. No evaluator source, lifecycle policy, arbitrary-command endpoint,
queue, worker or writable MCP tool was added. Whole snapshots and a project-wide
version guard are deliberate bounded choices: 2 MiB snapshot/output, 4 MiB request,
128 snapshots, two projections, and conservative competing-write conflicts.
The added storage/Git cost is needed to preserve multi-file results and existing
file-based verification provenance. This makes no production throughput claim.

## Limits and human decision

RISK-HAG-001 and RISK-HAG-002 remain raised. Existing private API-key/principal,
path and constrained-Cypher controls were exercised. Authenticated human identity,
database ACLs, real authority cutover, production operation, power-loss durability,
host startup/compaction/desktop, public release and deployment remain outside scope.
Plugin archives were inspected; no live Codex or Claude session was qualified.

The VREC/RLS records inside test bundles are synthetic and authorize nothing in
the real repository. Only the later actual VREC for WO-HAG-008 under VER-HAG-006
can be presented for the separate human verification decision. PR #542 remains
draft from `codex/hosted-artifact-phase3` to `main`; merge is not authorized here.
