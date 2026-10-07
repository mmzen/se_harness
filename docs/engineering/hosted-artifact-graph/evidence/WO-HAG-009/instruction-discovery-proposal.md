# Instruction discovery and context-load correction

The native Claude trials completed useful service operations but omitted required
procedure reads and produced inaccurate reports. Opus05 also exceeded a native
file-read limit on a 603 KiB event index. Repeating that input layout does not
address the observed failures.

The user requested a proposal and then the affected Claude reruns. WO-HAG-009
already permits bounded test-driver and explanatory guidance corrections.
WO-HAG-010's approved startup fix remains unchanged. This review records the
implementation choice; it supplies no new lifecycle or verification decision.

## Proposed changes

| Change | Files | Intended effect |
| --- | --- | --- |
| Put hosted reading rules before local repository procedures | `plugins/verity-plane/common/skills/change/SKILL.md`, `evidence/SKILL.md`, `setup/SKILL.md` | The agent sees the current-task instruction route before command construction; preserve the released evaluator as lifecycle authority |
| Read agent-selected JSON fields from retained files | `tests/hosted_artifact_graph/native_call.py` and `test_native_support.py` | Avoid loading entire receipts or event indexes; return exact values and file hashes, with bounded output and no command execution or workflow selection |
| Keep one small transient progress note | Guidance and disposable native task | Recover result paths, exact identities and remaining work after compaction; read original evidence and current evaluator context before acting |
| Narrow session-local shell rules | Disposable qualification settings | Deny the observed non-helper listing routes; preserve the existing fixed helper grant and normal hook/permission checks |

The JSON reader uses an explicit JSON pointer selected by the agent. It can list
an object's keys or an array's length without loading values into context. It
rejects paths outside the selected test directory, linked paths, missing fields,
credential-bearing inputs and oversized results. It does not choose an operation,
interpret a gate, rewrite an outcome, summarize evidence or send a service request.
The complete original stdout and command record remain unchanged.

The temporary note is not repository content or a new source of authority. The
agent chooses its location within the permitted test output directory. It contains
references, not an unreviewed replacement for a receipt or procedure.

## Verification and rerun

1. Check the reader's containment, pointer traversal, exact values, absent fields,
   size limits, credential refusal and absence of subprocess effects.
2. Run the changed plugin's existing package checks and the required source,
   distribution and CLI checks. Build exact new candidate packages. Retain the
   source/component tuple and runtime equality or changes.
3. Run Claude in a new private project from the original fixture. Give outcomes,
   schemas, synthetic decisions and exact paths, but no completed requests,
   corrective commands or workflow sequence. Preserve ordinary hooks and review.
4. Reassess NQ-01 and NQ-05 and rerun their affected lifecycle/refusal/read/recovery
   operations under NQ-02/03/04. Verify actual procedure reads before actions,
   observed calls, complete raw receipts, exact exports and final report facts.
5. Retain failures and interventions. A token reduction or successful exit alone
   is not a pass. Compare only actual host-reported metrics. Keep prior Codex
   observations tied to their original tuple; do not silently qualify changed
   guidance with old evidence.

## Review boundaries

The service, evaluator, wire schemas, gates, decision rights, acceptance criteria
and real repository authority stay as approved. No opaque end-to-end launcher,
new actor permission or model-specific workaround is introduced. Required human
verification remains separate. PR #543 stays draft while qualification is incomplete.
