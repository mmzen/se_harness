# Focused Claude diagnostic after the output-boundary correction

The test helper now restricts output to the selected `work/` directory before
executing a command. Focused boundary tests pass. Claude's fresh diagnostic
demonstrates a successful Cypher read and a changed-draft stale-preview refusal.
It still fails the required scope-refusal and procedure checks. Combined native
qualification remains incomplete; PR #543 stays draft.

## Exact candidate and correction

Candidate C: `cccc3546ed936fda5827f19b26032571c14a0a0e`.

The correction adds one shared output-path check for command records, companion
evidence, export destinations and observation records. Invalid paths are refused
before command execution. The tool index states the same `work/` boundary.
This fixes the misplaced records observed in the
[previous paired run](../context34-result/assessment.md). It does not change
service behavior, lifecycle policy or the qualification criteria.

The [implementation review](../boundary35/review.md) retains the diff review,
failed first test attempt and corrected checks. The first focused attempt could
not write its temporary fixtures under the default sandbox. A dedicated temporary
test directory and normal host execution resolved that infrastructure failure.

| Supporting check | Result |
| --- | --- |
| Focused driver tests | 47 tests, one reported skip, exit 0 |
| Five previously misplaced output paths | All refused before execution; originals preserved |
| Full source suite | 1,337 tests, 24 reported skips, exit 0 |
| Distribution validation and CLI smoke | Pass |
| Exact pinned build | Two producer builds match |
| Released validation | 1,991 artifacts, zero errors, 63 existing warnings |

The focused skip is the existing host-dependent symlink-creation test. The new
deterministic linked-path refusal check runs. These tests establish output
handling; they do not establish native qualification.

Client: 0.22.2, wheel SHA-256
`4ccd07cbfdd5748373bf535530441ca833f80343bfc53c8b00b898e6ec6ca99d`.
Candidate plugin: 0.2.7, loaded only for this disposable session.
Released evaluator: 0.22.1, archive SHA-256
`cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053`.
All 27 service-wheel members and the pinned runtime, evaluator, database,
protocol and dependency identities match the prior qualified service chain.
Archive/image identities differ. Restart and restore were not rerun here.
Exact identities and comparisons are in [provenance.zip](provenance.zip).

## Focused run and independent result

Claude Code 2.1.273 / claude-opus-4-6 ran in a fresh private project. It received
the desired result and boundaries, but no completed request, query, artifact
answer or operation sequence. The proctor supplied no procedural hints or
corrective commands and made no graph mutations on the agent's behalf.

The task stopped at handoff. Completion, VREC/RLS preparation, risk records,
native exports and publication were excluded. This was not another full NQ-01
through NQ-05 run and cannot replace one.

| Observation | Result |
| --- | --- |
| Duration | 1,200.078 seconds; reached the declared 20-minute limit |
| Native calls / failed tool items | 89 / 8 |
| Peak input context | 163,700 tokens reported |
| Accepted lifecycle operations | Three: approval, start and handoff |
| Independent released replay | All three accepted operations pass |
| Cypher MCP / independent HTTP | One successful request; exact HTTP 200 match |
| Changed-draft stale preview | Mechanism confirmed; refused receipt absent |
| Out-of-scope handoff | Not demonstrated; different protection refused the request |
| Required procedure reads | Incomplete |
| Required greeting assertion | Not executed |
| Native outputs outside `work/` | None observed |
| Final native reporting | Markdown report saved; observations file absent at timeout |

The generic observation helper also prints authoring-efficiency goals. Those
goals do not assess this focused lifecycle diagnostic. Performance improvements
remain deferred; these measurements establish no speed improvement.

## What the evidence proves

**The changed-draft case now uses the required trigger.** Claude previewed
approval at project/context versions 14/12, changed the selected INT-P3-001
document, then submitted the old preview digest with current versions 15/13.
The service returned `HAG_REMOTE_STALE_PREVIEW`. The old and changed document
bytes differ. The request's operation key also changed, but that field is
excluded from preview binding. The action and selected artifacts remained the
same. Fresh preview and approval then succeeded.

Independent receipt lookup returns 404 for the refused operation. The next
accepted operation still starts at project version 15. The proctor retained
this comparison; Claude did not itself retain an explicit no-effects comparison.
An early progress message missed this request; this final assessment uses the
complete retained trace.

**Cypher succeeds.** Claude read the product's physical representation and
bounded-query guidance after two wrong attempts to use the released-resource
reader for product references. Its query returns WO-P3-001's three declared
relations. An independent request against the exact same view matches the MCP
response, with `complete: true`, no continuation and no unresolved references.

**The accepted service operations replay correctly.** The independent observer
retrieved their receipts and exact input Git snapshots, then invoked released
0.22.1 outside those disposable repositories. All three operations match the
expected states, checks and file effects. The observer's exports support this
replay; they are not native-agent export qualification. The original handoff
comparison base is preserved. No test VREC or test candidate P was created.

## Remaining failures

1. **The wrong refusal is called a scope pass.**
   `work/handoff-oos-req.json` selects imported WO-P3-900 with an empty file list.
   The service refuses it with `HAG_REMOTE_PROTECTED_FIELD` before invoking the
   scope evaluator. This proves imported-record protection, not rejection of a
   changed file outside an approved work scope. The native report nevertheless
   labels the required out-of-scope case demonstrated. Independent lookup finds
   no receipt, and the next accepted operation starts at unchanged version 17.

2. **Required instruction reads remain missing.**
   The trace shows the selected approval, start and handoff sections. It does
   not show their `before-this-action` sections, decision rights, work-approval
   authority, approval-package assessment, or the capability/requirement/
   specification authoring checklists before those actions. Reading the routing
   table and receiving correct pointers did not establish these reads.

3. **Accepted evidence does not satisfy the authored verification contract.**
   Claude reads the source and writes `work/assertion.json` with
   `method: inspection`. No `assert-greeting` call occurs. Its own VER-P3-001
   and WO-P3-001 require executing the assertion. A service-accepted handoff and
   a successful replay do not prove that this test ran. Source inspection is
   useful evidence, but is not the required executed check.

4. **Record discovery and reporting are unreliable.**
   Claude treats the observation record as a directory, tries an unsupported
   argument, then attempts a prohibited `ls` command, which the host denies.
   It eventually reads the actual record file. The native report omits these
   later failures and the full qualification candidate C and imported baseline B.
   It claims a COMMUNICATION read through `task.md`, which that task does not
   contain. The session times out after writing the Markdown report and before
   writing the requested `native-observations.json`.

The supplied test work remains `in_progress`; handoff is not completion.
Its output Git head is `f6b6d906c3373f9680abd87ed3798d14ef65ccc1`.
Source fixture S is `5820415917e87b64d80bad2f7c39c6d18d692829`.
The imported baseline B is
`se-harness-artifact-baseline/v1:sha256:4b4545cfb61393a51a64ff85b9005eb4d424e9e6ac04dcb39249422ca3c4ae28`.
These are separate from C above.

## Boundaries and next correction

All 18 observed native file writes and 25 command captures are under `work/`.
The native root contains only the driver's expected control files. Staged input
digests and the monitored real repository/host-setting snapshots are unchanged.
This checks the selected surfaces, not every file on the machine. Legacy host
permission exceptions for root-level report names remain configured; the new
helper check is not a claim of work-only OS isolation. This native run made no
invalid helper-output attempt; deterministic tests establish those refusals.
The completed test containers are stopped and their volumes preserved.

The next bounded correction should make the current procedure's entry conditions
and applicable prerequisites available with its selected section, using canonical
released content. It should also make the observation result's file path clear.
Keep workflow choices with the agent. Do not add a hidden workflow runner or
supply the negative-test answer. Repeat the focused scope, procedure and actual
assertion checks before spending another full qualification run.

WO-HAG-009/010/011 remain in progress. No real verification record, verification
decision, completion, release, deployment or host-plugin update occurred.
The released next step for selected implementation work remains
`STEP-WO-IMPLEMENT-CHECK`. PR #543 retains target `main` and trusted comparison
base `55caaada508495bea7d97effd27644d1ce8373da`.

At the preceding remote head, Engineering Harness CI fails
`QGP-G4I-EVIDENCE` for WO-HAG-009's missing matching handoff evidence. All other
completed checks pass; three conditional release checks are skipped. This
unfinished-work report does not manufacture completion evidence. New-head CI
is checked separately after publication.

## Review material

- [Original visible native transcript](claude-301-visible.md).
- [Exact inputs, requests, reports, comparisons and replay](claude-301-evidence.zip),
  with [file inventory](claude-301-inventory.json).
- [Build, setup and observer provenance](provenance.zip),
  with [file inventory](provenance-inventory.json).
- [Earlier paired Codex/Claude assessment](../context34-result/assessment.md).

The original native report is retained unchanged, including its incorrect claims.
Private reasoning, raw account-authentication events, credentials and whole
environments are excluded. Known test tokens are checked absent. Exact retained
file bytes and the unchanged private event stream are identified by digest.
