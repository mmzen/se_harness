# 0.23.0 / 0.2.7 qualification: progress and blocker

**Release preparation is not ready for verification or merge.** The exact candidate
is `464034e8f0b189d330c3a8c5d8ce64c090b5cc86`. The required first Claude drafting diagnostic failed. Its accepted
contract stops further native repetitions on this candidate. Existing approvals
remain valid for their scope; no completion, verification or release was recorded.

## Checks observed

| Check | Actual result |
| --- | --- |
| Windows source suite | 1,339 tests, 24 reported skips, exit 0. |
| Exact release recipe | Two pinned builds produced identical wheel/sdist bytes. |
| Windows and Linux packages | Released package verifier and installed wheel checks passed. Index-selected source archive, CLI surface, init and doctor passed on both platforms. |
| Windows upgrades | Two actual 0.22.1 to 0.23.0 rehearsals passed with the same semantic digest. |
| Plugin staging | Both 0.2.7 archives built from the exact candidate/bundle; inventories retained. Local staging only. |
| Private service | Packaged client walkthrough, transaction/refusal/concurrency/HTTP-MCP checks and restart/consistent restore passed. |
| Client compatibility | Actual service accepts matching 0.22.2 and 0.23.0 tuples; nine incompatible combinations refused. |
| Claude EFF-04A2 | **Failed independent content/report review.** 163.93 seconds, two native calls, peak input context 32,679. This was a clarification stop, not artifact creation. |

The live service keeps evaluator 0.22.1 separate from client 0.23.0 and plugin
0.2.7. It is private and source-built; Git remains authoritative. Source suites
and CI do not establish native agent correctness. Current PR checks passed at
this candidate; RLS-dependent rehearsal legs were skipped because no ready record
exists. PR merge-commit CI and the exact local candidate builds remain distinct.

## Claude findings

1. The reply asks for the audience and success observation, but does not resolve
   the user's problem or agreed improvement. Its proposed statement supplies an
   unsupported reason for the change. The required input remains missing.
2. A Read of `inputs/selection.json` failed. The correct selected file was at the
   native root and was supplied to the agent. Its final reply nevertheless says
   “No failures or denials.” The later successful status call does not erase that
   failed read.

The complete paired calls and a separate service read establish that no hosted
mutation was attempted and the fresh project remains at version zero. All staged
input bytes and inspected host-setting hashes are unchanged. The full visible
reply, failed read, status result and independent review are retained. Private
reasoning and credentials are excluded from publication with the omission method
and original capture digest recorded.

The applicable rules were present in the assembled entry. This is not an absent
file or stale-package explanation. The observed agent did not follow those rules.
Instruction ordering may contribute, but a single run cannot prove that cause.
The proposed correction must pass a fresh diagnostic; wording alone is no proof.

## Preserved setup failures and limits

- The first Windows upgrade setup exceeded path limits. A shorter disposable
  location and process-only Git long-path setting enabled two passing runs.
- The first Linux package test lacked a test-script mount; the retry supplied
  the exact committed helper.
- Direct-path sdist installation creates PEP 610 metadata refused by the existing
  wheel-archive identity rule. The established index-selected sdist route passes.
  This is a retained existing limitation, not a claim that direct-path installation
  is qualified. No identity rule was weakened.
- Read-only assessment recovery encountered sandbox socket denial, then a wrong
  assessor status URL. The final read uses the supported `/v1/status` endpoint.
  Those assessor setup errors are separate from the native agent's failed Read.

## Remaining work

Review the [one-file correction proposal](../WO-RLS-049/review.md). After approval,
produce a new candidate and rerun the required diagnostic before the remaining
Codex/Claude cases. Preserve this failed candidate. Native entry/delivery cases,
the separate Codex Windows desktop evidence, exact final integration assessment,
marketplace review staging, aggregate verification and ready-RLS rehearsals remain
pending. No earlier desktop omission or risk acceptance applies to this release.

The evidence index is [candidate-464034e8-evidence-index.json](candidate-464034e8-evidence-index.json).
Package checks, actual service checks and the native diagnostic have separate
archives, with complete included-file digests. Skips and unperformed cases are
not passes. No public release, marketplace, host installation or provider setting
was changed.
