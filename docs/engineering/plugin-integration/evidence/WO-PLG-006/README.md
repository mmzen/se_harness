# Claude adapter implementation evidence

WO-PLG-006 remains in progress. The native manifest, inline guards and focused
tests are implemented, and all C01-C12 observations have been collected. C10 and
C11 failed enforcement and remain unqualified. No supported production profile,
completion, verification, release or merge is claimed by this evidence.

The [path-validation correction](path-validation/README.md) changes production
guard bytes. The current matrix and canonical records use the complete fresh
`acceptance-06` run against committed correction `fd2419f4`; earlier attempts
remain historical. Ambiguous paths now refuse before interpreter invocation.
The separate [Linux rehearsal failure](governance/linux-rehearsal-failure/README.md)
occurred in shared scratch cleanup outside this work order's correction scope.
The later source head passes both platform rehearsals; the earlier failure and
its unconfirmed cause remain retained, with no cleanup policy change or waiver.

The accepted compatibility boundary remains Claude Code 2.1.266, Windows,
Python 3.14.6 and evaluator 0.16.0. Repository governance uses released 0.17.0
separately. The five packaged shared skills are explicitly namespaced; this work
does not qualify overlap with repository-managed skill copies or implement WO009.

## Current case results

Each canonical `Cnn/` directory contains the required actions, stdout, stderr and
observations. It points back to immutable attempt captures. The current
`wire_assessment` uses actual structured hook responses and correlated tool ids;
earlier `reassessment.json` corrections remain with their original attempts.

| Case | Conclusion | Observed boundary |
| --- | --- | --- |
| C01 | pass | Native discovery resolves all five packaged skill names/paths; active bindings and package identity retained. |
| C02 | pass | Startup, resume and real compaction deliver complete 7902-byte context; exact body hash and isolated argv checked. |
| C03 | pass | Checked hook precedes one exact successful Write; correlated denial precedes the refused Write result and target stays unchanged. |
| C04 | pass | Direct accepted inline-command tests refuse missing fields and malformed JSON. |
| C05 | pass | Disabled binding has no receipt; shared script failure produces actual UNREADY context. |
| C06 | pass | Space-containing native paths and unsupported Read observed; exact quotes/Unicode receiving-side transport is separate focused calibration. |
| C07 | pass | Unsupported profile/negative decision rejected; audited helper-spawn log empty and repository Markdown hashes unchanged. |
| C08 | pass | Missing/removed interpreter and both ambiguous path forms invoke no Python; wrong evaluator produces identity refusal, not setup-required. |
| C09 | pass | Failed/interrupted/stalled evaluator trees stop; native denial intervals 2.764/2.608/36.106 seconds precede tool errors; no target effects. |
| C10 | fail | Native hook cancellation at 60.161 seconds produces no refusal; exact Write succeeds. |
| C11 | fail | Launch failure, missing output, invalid output and removed binding after prior readiness each allow an exact Write effect. |
| C12 | pass for rejection | Timeout=1 and async bindings are actually loaded and rejected. Both permit Write effects; async check returns after the effect. |

Completing a negative experiment does not make failed enforcement pass. See
[qualification-limit.md](qualification-limit.md) for the concrete blocker,
documented host behavior and the boundary of available remediation.
The collection driver's exit 0 means its requested observations were written;
case verdicts and qualification are recorded separately.

## Candidate and methods

Current attempt 06 packages source
`fd2419f4c26b9ba4d4a97f85b7d2b08da72b8626` as
`f11d94139ad7e6194147c32a80a070f34f6761900a8c737aec354ec9b447d7f6`.
All 23 source-to-package-to-loaded baseline mappings in
[candidate-binding.json](candidate-binding.json) match. The earlier 46 mappings
for attempts 04/05 remain in `path-validation/prior-candidate-binding.json` and
those attempts' inventories. They do not qualify the corrected guard. Mutated
fault fixtures are labeled separately; accepted assemblies remain unchanged.
The inert Codex companion is only a builder fixture and grants no Codex support.

Explicit focused discovery is required because top-level unittest discovery does
not recurse into these directories:

```
../se-harness-plugin-eval-017/Scripts/python.exe -X utf8 -B -m unittest discover -s tests/plugin_integration/claude_adapter -v
```

Direct protocol calibration is distinct from the real native observations in
C01-C03, C05-C06 and C08-C12. The outside observer records target hashes before
launch and after exit, and counts correlated successful native Write results;
that count is not a low-level filesystem write count or a whole-session audit.
The inspected normal-profile metadata is unchanged across all 26 native calls
in attempt 06, and all 24 earlier calls in attempts 04/05. The API authorization
and payload inventory are retained. Seventeen focused tests pass; small required
repository checks and honest candidate/released skew are retained in
`governance/path-correction-checks/`. The parent owns broader CI checks.

## Retained attempts

- `acceptance-01`: default-sandbox API connection failure; its subsequent runner
  was stopped after that network restriction was established. It is incomplete.
- `acceptance-02`: fixture initialization followed by a Git ownership refusal
  under the network-enabled account; no host acceptance result.
- `acceptance-03`: committed-package C01 discovery/context observed. Both C03
  Write calls failed Claude's read-before-write precondition before PreToolUse;
  they establish neither permitted adapter effects nor adapter denial. The
  corrected runner requests the previously demonstrated Read-then-Write sequence.
- `protocol-01`: C04 malformed/missing-input denial and C07 unsupported-profile
  rejection pass against the committed package. These are inline-command/static
  observations, not replacements for required live-host cases.
- `acceptance-04`: complete initial C01-C12 collection. Structured reassessments
  correct the old C05/C06/C08 debug-substring flags, including C08's incorrect
  `setup_required=true` for the wrong installed evaluator. C10/C11 effects remain
  failed and unqualified.
- `acceptance-05`: C11 guard-removal extension after a verified startup, with an
  explicit subsequent activation; C07 adds actual spawn auditing and before/after
  repository state hashes. This does not claim same-process hook hot reload.
- `acceptance-06`: complete repeat on the corrected committed package, including
  both ambiguous environment-path cases and C11 removal after verified startup.
  Current canonical case records project this attempt. C10/C11 remain failed;
  C12's pass remains only a configuration-rejection result.
- `governance/api-scope`: exact inspected payload inventory, automatic approval
  rejection and the subsequent specific operator authorization. No workaround
  was used to bypass that rejection.

Positive or negative case observation is distinct from qualification. The final
engineering disposition and any future assurance must bind the exact candidate;
the current failed routes cannot be promoted by successful unrelated tests.

Host debug/output is sanitized using the existing probe's capture policy.
Credential contents are neither read nor copied by the observer. Raw host debug
stays in disposable sandboxes outside the checkout; do not publish those files.
