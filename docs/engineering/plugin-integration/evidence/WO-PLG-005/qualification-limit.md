# WO-PLG-005 qualification limit

**Operator acceptance recorded:** the operator accepted hook failure as a [documented local limitation](local-limitation-acceptance/README.md). The failed observations remain unchanged. Formal decision recording and any required contract changes are separate; this evidence update changes no lifecycle state.

The Codex adapter remains **unqualified**. On the tested profile, a missing
before-tool refusal allowed the reviewed synthetic edit to proceed after
ordinary one-time file approval. Successful healthy-path checks do not cover
these failure conditions.

This evidence concerns DEC-PLG-001's Windows route: Codex CLI 0.153.4,
Python 3.14.6 and released evaluator 0.16.0. The loaded production payload
matches checked package-04 from source
`400cf3d5d669e239d046cc640ac94e962a6e731d`. Fault runtimes are deliberately
instrumented disposable fixtures, with no separate runtime qualification.

| Condition | Actual native observation | Enforcement result |
| --- | --- | --- |
| [C10: dispatcher stalls](C10/host-timeout-01/observations.json) | Hook timed out after 30,012 ms; one exact approved update followed | Failed; no supported handler refusal |
| [C11: output missing](C11/missing-output-01/observations.json) | Zero output at exit 0; hook reported completed; one exact approved update followed | Failed; no supported handler refusal |
| [C11: output invalid](C11/invalid-output-01/observations.json) | Truncated JSON at exit 0; hook reported invalid output; one exact approved update followed | Failed; no supported handler refusal |
| [C11: active binding lost](C11/lost-active-binding-01/observations.json) | After proven readiness, a fresh session had PreToolUse disabled; no before-tool hook ran and one exact approved update followed | Failed; missing required binding |
| Literal OS shell-start failure | No native capture; neither dispatcher injection nor disabled bindings emulate it | Unavailable |

The one-edit observer preserved the ordinary read-only/on-request profile and
accepted only the exact predeclared synthetic update. Each completed effect is
supported by the actual request, one-time acceptance, native completed file item
and final SHA-256. A completed negative observation can return runner exit 0;
its enforcement conclusion still fails. No independent control prevented these
observed test effects.

All completed fault runs confirm owned-process cleanup and restoration of their
selected configuration and binding. Injected runtimes also confirm their original
inventory and removal of the active fault configuration. The changed sentinel
is retained as the observed effect; the other target hashes remain unchanged.
The binding-loss case restores active native inventory and covers a fresh
host/session after readiness, without claiming same-process hot reload or
literal guard-file deletion.

SPEC-PLG-005 PLG-CDXA-007/010 and SPEC-PLG-008 PLG-HOOK-004/009 require these
missing-enforcement results to remain unqualified. VER-PLG-005 C10/C11 and
VER-PLG-008 C08/C09 distinguish effect observation from passing enforcement.
This note waives no case, changes no approved definition and makes no assurance
decision. WO-PLG-005 stays **in_progress**; completion, verification, release and
merge are separate decisions.

The [report](report.md) retains earlier failed attempts, the initial C11 preview
decoding failure, exact-profile limits and the unresolved historical effects of
the native-menu incident. Full case indexes preserve the original nested evidence.
