+++
id = "VER-HAG-007"
type = "verification"
title = "Qualify Codex and Claude on the hosted lifecycle"
status = "approved"
owners = ["mmzen"]
created = "2026-10-07"
updated = "2026-10-07"

[relations]
verifies = ["REQ-HAG-011", "REQ-HAG-012", "REQ-HAG-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-07T01:50:55Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the reviewed WO-HAG-009 and VER-HAG-007 package at 540bd9fb3a79cf7d8cfaccf01c52b9e8f7b0f133 in PR #543, confirming required commit-bound verification and bounded local Codex CLI/Claude Code qualification. The grant includes ordinary review pushes and PR updates in mmzen/se_harness from codex/hosted-agent-qualification to main, the ready record and the later separately supplied human verification decision, and marking the same PR ready only after that decision is recorded and remote. Git remains authoritative. This grants no verification acceptance, merge, release, public deployment, host-plugin update or risk acceptance."
+++

# Qualify Codex and Claude on the hosted lifecycle

## Outcome and scope

Qualify a native Codex CLI session and a native Claude Code session on Windows
using the hosted Phase 3 lifecycle. Each agent must choose and execute the next
steps from the supplied task, candidate guidance and actual evaluator results.
The outcome is a qualified host path or a specific, reproducible gap for each host.

This adds host evidence for unchanged REQ-HAG-011 through REQ-HAG-013 and
SPEC-HAG-007. VREC-HAG-005 remains the independent functional qualification;
this contract does not reopen or rewrite it. Git remains authoritative.
Authentication and database ACL implementation remain deferred.

## Independence and starting inputs

Use the existing synthetic greeting task and clean source fixture described in
`tests/hosted_artifact_graph/lifecycle_fixture.py`. Its expected greeting, required
relations and lifecycle semantics come from the task and accepted contracts,
not from model prose or candidate service output. A small realistic task is enough
to expose instruction, command-selection and recovery gaps; adding another product
or test framework is unnecessary.

Prepare two separate disposable projects/volumes from the same exact fixture.
Retain both initial identities. Do not let the second host inherit the first
host's completed artifacts, decisions, session memory or receipts. The supplied
task states the desired result and boundaries, not a list of answers or completed
mutation requests. The agents author new draft content and construct their own
bounded requests. A supplied test-actor decision is explicitly a synthetic test
input; it is never an actual assurance or release decision.

The independent reviewer compares actual requests, receipts, exported Git blobs
and ordinary released-evaluator replay with the contract. Agent summaries cannot
prove a pass. A helper may supply paths, protect credentials, record events or drop
a response. A helper that selects and executes the whole workflow for the agent
does not satisfy the agent-driven criteria.

## Exact environment

- Windows native Codex CLI and Claude Code; Linux x86_64 service/Memgraph in
  private Docker containers. Record exact CLI executable/version, model reported
  by the host, operating system and execution settings. Preparation observed
  Codex CLI 0.159.2 and Claude Code 2.1.273; these observations are not test passes.
  Record any version change before a run and compare the actual paired runs.
- Select one clean candidate and its exact client wheel, both plugin archives,
  service image, dependencies, protocols, schema and source fixture. Verify all
  digests before use. Reuse the qualified Phase 3 tuple only when all relevant
  runtime/guidance bytes match; otherwise rebuild the affected local packages.
- Use released evaluator 0.22.1 in its separate environment with the pinned
  archive/payload identity from SPEC-HAG-007 and SPEC-HAG-003. Invoke the absolute
  Python with `-I -m se_harness` outside the real checkout. Candidate client 0.22.2
  supplies remote commands only; it never governs real work.
- Use candidate plugin guidance 0.2.7 through session-local loading where
  supported, or explicit reads of the digest-checked package resources. Record
  which route actually occurred. Explicit reads do not prove native automatic
  discovery, startup, resume or compaction delivery. Those claims are outside this
  contract, as are marketplace installation and changes to the real host plugin.
- Check existing provider authentication, then make a small live request before
  the long session. Status alone is not proof. A failed live request leaves that
  host pending. Do not print, commit or pass account credentials in prompts.
  Obtain user input if an actual sign-in step requires it; do not replace accounts
  or change credential stores as an incidental test action.
- Keep normal host permission review and existing private API-key/principal,
  path, network and Cypher controls. Request only specific test-directory and
  loopback-service access. Do not bypass approvals, sandboxing or hook trust.
  Retain any denial and stop the denied action without changing route to evade it.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-HAG-011 | demonstration, inspection | NQ-01, NQ-02, NQ-03, NQ-05 | Both real agents use exact instructions and released results, complete the test lifecycle, and keep real Git authority unchanged |
| REQ-HAG-012 | demonstration, test | NQ-03, NQ-04 | Both hosts recover a stale request and an unknown reply without a partial or duplicate accepted effect |
| REQ-HAG-013 | demonstration, test, inspection | NQ-02, NQ-05 | Both hosts export exact selected bytes/history; independent replay confirms original candidate bindings and clear test-only reporting |

## Acceptance scenarios — run separately for each host

### NQ-01 — Instructions and selected context

Start a fresh native session with the requested task, exact environment paths and
test limits. Retain the initial prompt and native event stream. Identify the
candidate skills/resources actually read, their hashes and what triggered each
read. The agent must identify the test project, source/baseline and evaluator,
state that Git governs real work, and distinguish checkpoint-free context from
passed gates. Record setup assistance separately. No success may be inferred
from a host's paraphrase of an unread file.

### NQ-02 — Agent-driven lifecycle

Ask the agent to author the test definitions and work order, validate them,
obtain the fixture's supplied test decisions, approve/start test work, inspect the
existing greeting source and run its exact assertion. Retain the real local test
output as bounded evidence. The source task uses the existing implementation;
the graph does not acquire an arbitrary code-edit or command-execution endpoint.

The agent must then retain handoff evidence, complete the test work, prepare and
assess a test VREC, and prepare and assess a test RLS with no publication. Include
one recorded test risk and its paired decision using supported commands. The
agent builds its own CLI requests from the documented closed schemas and reads
the actual results before proceeding. Preserve B (hosted input), S (fixture),
P (test Git candidate) and C (actual qualification candidate) separately.

Pass requires observed tool calls and complete receipts for every required
stage, with independent released replay confirming states, next steps, selected
paths and candidate bindings. Calling `qualify_pilot.py` or another end-to-end
launcher as one opaque tool call is a scripted smoke result, not this pass.

### NQ-03 — Refusals and bounded reads

Supply one out-of-scope test handoff and one stale preview caused by a changed
selected draft. The agent must identify the actual failed condition, stop that
action and recover through fresh context and a valid corrected request. Compare
versions and receipts to prove the rejected requests committed no effects.

Use each of the seven actual read-only MCP tools against selected test views;
compare the native responses with independent HTTP requests for those exact
views. Retain completeness/continuation flags. The agent must describe a partial
or saved response accurately, read the saved result when permitted, and never
treat missing content as a complete governing set. No writable MCP tool is added.

### NQ-04 — Unknown reply recovery

After one accepted write, a local test transport drops only its reply. Require
the agent to report the result as unknown, inspect the original operation key,
and recover the retained receipt. An identical retry must return that result
without another version increment; a changed request under the same key must
conflict. The fault helper must not choose the recovery commands for the agent.
This checks native recovery behavior; VREC-HAG-005 retains the separate service
restart, restore and atomic-rollback qualification.

### NQ-05 — Export, assessment and honest limits

The agent exports an earlier and a later selected snapshot into new directories.
Independently reconstruct each bundle in a fresh ordinary Git repository, compare
every selected file digest and candidate object, and run released validation and
selected checks. Confirm that the test VREC/RLS still names its original P.

The final host report names the actual outcomes, evidence, interventions, refused
actions and limitations. It must distinguish test decisions from actual human
acceptance, and describe no real release, deployment or authority switch. Compare
the real repository and host settings before/after to detect unintended changes.

## Interventions and verdicts

For each host retain: completed/failed/pending cases, command refusals, wrong
commands, retries, manual interventions, elapsed time and reported token usage
where available. Do not fabricate missing metrics or compare unreported usage.
Ordinary synthetic test decisions and specific tool permission approvals are
expected inputs and are counted separately from procedural help.

Record every procedural hint, supplied corrective command, direct operator
mutation and guidance correction. A run that needs such help remains an assisted
observation. After an in-scope correction, rerun the affected native scenario
from a recorded clean point using the final packaged guidance. A successful final
pass needs no supplied step sequence, hidden script-driven completion or direct
operator mutation on behalf of the agent. Unrelated passing tests cannot replace
a failed host. Both hosts must pass all five cases for the combined claim.

## Supporting checks and evidence reuse

Run repository validation, full source tests, distribution checks and CLI smoke
on the final clean candidate, as required by AGENTS.md. Exercise changed native
drivers or plugin guidance with their focused checks. Preserve all failures.
Reuse VREC-HAG-005's unchanged service qualification with explicit source and
component equality; do not claim those scenarios were newly rerun. A runtime or
protocol defect stops the affected host and needs bounded correction authority.

## Evidence retention

Retain a concise per-host assessment, independent comparisons, actual argument
arrays, working directories, exits, timestamps, runtime/package identities,
instruction-read trace and corrected/uncorrected observations under the selected
work order's `evidence/` directory. Retain the submitted task and native
tool-call/event transcripts. Remove credentials before durable retention; record
the redaction method and hashes of retained bytes. Do not record private account
tokens or full environments. No copied repository, virtual environment, host
profile or entire temporary run tree belongs in Git.

Use a bounded archive of required transcripts and test exports when necessary,
with a file inventory, byte digests and a durable review-accessible location.
Temporary-only output is insufficient. Preserve earlier evidence and VREC
bindings. Capture a new actual VREC later through released 0.22.1 for the clean
candidate and approved qualification work. Synthetic records do not verify it.

## Residual uncertainty

This qualifies the observed Windows CLI/model/component combinations, not every
model or future CLI version. Desktop, automatic startup/compaction/resume delivery,
public installation, production service operation, real authority cutover,
authentication and database ACL implementation remain outside scope.
RISK-HAG-001 and RISK-HAG-002 remain raised; no risk acceptance is implied.
