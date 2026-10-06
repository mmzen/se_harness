# Hosted sandbox qualification — incomplete

WO-HAG-001 and WO-HAG-007 remain `in_progress`. No hosted verification record
has been prepared or accepted. PR #535 remains an unfinished-work draft against
`codex/hosted-artifact-graph-inputs`.

## Tested combination

Product candidate: `7290af984337e122b193981a187e58c29de41a16`. The client, plugin archives and service image
derive from this clean commit. Later evidence/index commits do not change this
tested identity. [Component identities](protocol04-combination.json) record
client 0.22.2, unpublished plugin 0.2.7 for both CLIs, service 0.1.0.dev1,
CPython 3.13.16, Memgraph 3.13.1 and separately installed public evaluator 0.22.1.
The current combination ID is `sha256:e997637ecfee3ab4e7514239cb3006254d52afc0181f68ae98fc95e1ca374168`.

Qualification ran on Linux/amd64 containers under Windows Docker Desktop.
All running image identities, dependency pins, source/byte bindings, commands,
exits and observed times are retained. Matching core wheel/sdist outputs came
from the repository's two-build pinned recipe. No component was published.

## Observed results

| VER-HAG-001 case | Current evidence | Assessment |
| --- | --- | --- |
| SC-01 Import fidelity | Exact original 1,909 Git artifact hashes and blob identities; duplicate IDs, unresolved targets, changed declared bytes and Explorer input refused. | Automated checks pass. |
| SC-02 Repetition and immutability | Same-key import returns the identical receipt; baseline B is unchanged after body/relation edits; canonical vectors remain fixed. | Observed checks pass. |
| SC-03 Work context | Packaged CLI matches twelve governing IDs, eleven paths and two dependency IDs; independent released output equals hosted output. Separate active fixture reports DEC-RLS-999 at QGP-G4I-DECISION; missing evidence produces `complete=false` and `binding_unavailable`. | Automated checks pass. |
| SC-04 Read consistency | Seven shared HTTP/MCP read operations, explicit views, unknown identities and row/byte/depth limits. | Automated checks pass. |
| SC-05 Valid drafts | Released template, incomplete requirement, body and valid relation revision, distinct immutable revisions. | Packaged CLI checks pass. |
| SC-06 Invalidity and protected input | Malformed TOML, duplicate metadata, invalid type/relation, imported decision/state/evidence, forged actor and wrong server rights refused without partial changes. | Live checks pass. |
| SC-07 Concurrency | Independent writers, identical keys and changed dependency with stale prepared input. | Current candidate passes. Earlier unexplained failure retained below. |
| SC-08 Receipt recovery | Actual client loses a committed response; identical retry returns the original receipt with one increment. Injected pre-commit faults roll back. | Live checks pass. |
| SC-09 Query boundaries | Allowed parsed Cypher, twelve unsupported forms, selected-view binding, row/byte/depth limits and rollback. Direct read transaction stops at about five seconds with resource-limit refusal. | Observed controls pass; direct time stress is not a public-grammar/HTTP exhaustion test. Database authorization remains unresolved. |
| SC-10 Agent walkthrough | Eighteen real packaged-client steps pass. Native Claude invocation stops before model work because OAuth expired. Earlier native Codex session could not read plugin guidance under its tool policy. | **Incomplete. Scripted checks do not replace the native-agent path.** |
| SC-11 Historical bindings | Exact released oracle; independent legacy digest; moved paths and changed scoped code alter it; CRLF follows legacy normalization; substituted evaluator/archive/payload and candidate-as-governor refused. | Automated checks pass. |
| SC-12 Package and recovery | Exact candidate ZIPs discovered by both CLIs; installed files match every ZIP entry. Actual restart/restore match the cutoff; stored schema mismatch and missing index refuse readiness/init/import without repair. | **Partial. Native plugin qualification remains incomplete; desktop unperformed.** |

The source suite passed: 1,319 tests, 23 reported skips, exit 0. Installed
service tests passed: four tests. Distribution checks passed for 23 records;
CLI smoke passed. Released validation found 1,970 artifacts, zero errors and
63 warnings. These results do not mean skipped cases passed.

The missing-evidence fixture does not invent a human approval. Its synthetic
active work also reports missing approval/completeness inputs at their own
predicates. The test asserts the exact decision predicate and separately checks
missing evidence. It does not claim the synthetic work is authorized.

## Corrections and retained failures

WO-HAG-007 applies the reviewed three-file command-documentation and candidate
plugin regression correction. Its approval, exact patch and checks are retained
under [WO-HAG-007](../../WO-HAG-007/correction-assessment.json).

Within WO-HAG-001, actual tests exposed missing deployed-configuration/installed
contract checks and incomplete BASED_ON edge checks. Candidate 8cd302dca19397d4c5bc85d1955454d5eca1c99b
corrected them. Its import tests then exposed wrong refusal codes for Explorer
input and duplicate document IDs. The present candidate fixes those codes and
returns a resource-limit refusal for the pinned database's read timeout.
Both earlier failures and successful reruns are retained, without rewriting
their original candidate identities.

The first synthetic decision fixture targeted already implemented historical
work. Its handoff request correctly returned WEX210; it did not test the intended
decision predicate. The second fixture adds a separate explicitly synthetic
active work order. Both fixture scripts and observations remain available.

Candidate c067608f71503f62fa6c9aa2f081515545bc350e once returned unknown for
both concurrent equal-key requests, with no committed effect. Its cause was not
established. Later normal-service concurrency checks on candidates 03 and 04
passed. Safe class/location logging now supports investigation. This is residual
uncertainty, not a claimed causal fix; the original evidence remains in
`c067-observations.zip` and `c067-assessment.json`.

An older onboarding runner refused the external-resource layout at its obsolete
skill-ownership check. Its working-tree-built plugin ZIPs also differed from the
Git-blob-built candidate. Those attempts do not qualify this combination. The
later exact-ZIP native discovery checks use fresh profiles and preserve both
failures. Native CLI discovery and an earlier Claude guidance read prove only
their stated subsets; they do not prove the hosted walkthrough or desktop.

The Claude wrapper process completed, but the nested Claude process exited 1
with `Failed to authenticate: OAuth session expired and could not be refreshed`.
No model or hosted operation ran in that attempt. Credentials were never retained
in this evidence archive. No permission bypass was used for either host.

## Recovery and performance

The packaged-client observations retain individual timings for import, context,
draft changes and each refusal. There is no production latency claim. Restart
took 5.315 seconds; consistent restore took
7.52 seconds. The restored logical store, baselines and
accepted receipts equal the recorded cutoff. The backup is retained at:

`C:\Users\mathi\Documents\Codex\2026-09-20\verity-plane-plugin-verity-plane-se\work\hag-phase2-20261005\protocol04-recovery\graph-data.tar`

Backup SHA-256: `029ef7e682db5142e73c87dfec5f5fbccc14d8d99fc457961232936759ae0cae`.
Size: 183080960 bytes. The backup and original volumes stay
outside Git; the archive contains their identities and actual recovery commands.
This observation does not establish power-loss durability, HA or production RPO/RTO.

## Review and limits

The implementation retains one service, one Memgraph store, one guarded commit
path, one shared HTTP/MCP read handler and a separate released evaluator. The
immutable source resolver supports legacy paths and evidence; it is not a second
mutable authority. No lifecycle policy, hosted human decision engine, queue or
public deployment was added. The materialization cost is visible in per-command
timings. Contract and identity checks refuse changed inputs before mutation.

RISK-HAG-001 remains raised. Application-side Cypher controls do not supply
Memgraph read-only authorization. Authenticated human decisions, authoritative
pilot use, repository cutover and production/release qualification remain outside
this package. Earlier VREC-HAG-001/002/003 bindings are unchanged and do not verify
the hosted implementation.

## Continue

Restore native authentication and resolve the Codex read-tool issue without
bypassing host policy. Execute and retain the required native plugin/agent cases
against these exact packages, then assess remaining host coverage. Keep failed,
unperformed and passing cases distinct. If code or the selected combination
changes, rerun affected qualification. Only then perform final handoff and use
released capture to allocate a ready VREC, followed by human verification.

[Raw observations](protocol04-observations.zip) are indexed by
[exact bytes and hashes](protocol04-inventory.json).
[Continuation inputs](protocol04-continuation.json) retain local paths and
boundaries. This report records observed engineering evidence, not a new decision.
