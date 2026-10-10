# Native lifecycle round 26

Candidate: `d31e337425696c944ee61eda9957b6ac4bd2c82b`.
Review branch head before this round: `3d504f531d44b3bdcfa0a5a3269d2fd47ff418fd`.
Runtime and guidance bytes match that candidate. This is VER-HAG-007 full lifecycle
qualification, not the one-artifact efficiency benchmark.

| Trial | Observed result | Time | Visible calls/items | Peak input context |
| --- | --- | ---: | ---: | ---: |
| Codex 211 | Full synthetic lifecycle completed; 11 accepted operations and four native exports independently replayed | 1,363.792 s | 263 items, lower bound | Unavailable |
| Claude 211 | Failed before import: helper spelling did not match the approved shell prefix | 267.564 s | 25 | 118,977 tokens |
| Claude 212 | Failed: timeout before completed handoff, verification, release or exports | 1,800.206 s | 129 | 166,586 tokens |

Combined qualification remains incomplete. No actual verification or release
decision was applied. Both provider live authentication probes passed before
testing. Sessions used separate private projects and synthetic decisions.

## Codex

Independent released-evaluator replay passed for all 11 accepted lifecycle
operations. Four native exports reconstructed exact Git bytes and candidate
objects. All seven MCP tools were exercised; ten calls matched the corresponding
HTTP results exactly. Imported records and source bytes stayed unchanged.

The stale-preview refusal, out-of-scope handoff refusal, dropped accepted reply,
original-key recovery, identical retry and changed-key conflict were retained.
The retry returned the same receipt without another version increment.
Other recovered command, heading and chunk-size errors remain visible.

The synthetic candidate is `137b13490a1a86020e6739a133c4f79249859681`.
It does not verify the real implementation. The retained summary missed Codex
helper reads, so the agent rebuilt a read index through many extra calls.
Visible command output totalled 1,363,879 characters. Read-result calls alone
returned 593,609 characters; text reads returned 356,733. These measurements are
output volume, not billed tokens or model reasoning time.

## Claude

Trial 211 quoted `-I`, while the exact approved Bash prefix left it unquoted.
Its denied `ls` was also outside the tool boundary. Its two MCP requests used
unknown identities and returned 404; they do not establish an empty graph.
The project remained at version zero. The agent's broad claim that all Bash was
blocked is preserved as a failed observation, not adopted as a diagnosis.

Trial 212 changed only the operator task's shell-prefix presentation. Permissions,
candidate, model and criteria stayed the same. Shell commands then worked.
Four accepted operations replayed independently. The project ended at version 20.
There were no native exports or MCP calls. The independent assessor exited 1
because its two-export criterion was unmet; its intermediate `state: running`
record is preserved alongside the terminal assessment.

The handoff used imported source commit
`5820415917e87b64d80bad2f7c39c6d18d692829` as `from_git`. That commit is absent
from the service's separate test Git history. Three sub-commands passed, but the
final check failed `WEX-ECP-003`. The action was refused and committed no effects.
The agent followed an intermediate next step and then tried completion without
retained handoff evidence. Further preview/digest errors remain recorded.

Observed instruction reads did not include the setup entry or the authority,
execution and reporting prerequisites. This is a gap in the visible trace, not
proof about hidden host context. Automatic compaction occurred; this run makes
no automatic instruction-delivery qualification claim.

## Boundaries and retained evidence

The real repository's tracked diff stayed empty during the native sessions.
Codex's workspace/network boundary probes passed. During/after hashes of the
three selected noncredential settings files agree. Claude settings also match
the earlier retained baseline. Codex's earlier baseline differs; its current
last-write timestamp predates this round. A fresh pre-run settings snapshot was
not taken. Therefore this round cannot prove that exact before/after comparison.

All three disposable service/graph pairs are stopped; their volumes remain.
No real host plugin, global settings, account, lifecycle decision or permission
was changed. Archives retain required inputs, visible transcripts, command
results, independent comparisons and read traces. Their inventories give byte
hashes. Provider credentials, raw private reasoning, virtual environments and
whole temporary trees are excluded. Historical archives are unchanged.

See each `*-inventory.json`, `*-evidence.zip` and `*-visible.md` in this directory.
The separate cost files were produced after the archives and are retained beside
them. `boundary-after-native.json` states the settings-evidence limit.

## Authorized correction

WO-HAG-009 permits bounded test-driver/guidance corrections. WO-HAG-011 permits
concise exact result handling and instruction discovery. The next correction
adds an explicit setup entry pointer, preserves the existing shell-prefix
spelling, exposes the failed sub-command, explains the retained test Git base,
and records observed reads without rereading source files. It changes no service
protocol, evaluator policy, criteria or permissions. A new unassisted native run
is required; these failures are not relabelled as passes.
