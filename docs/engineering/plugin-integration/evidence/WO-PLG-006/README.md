# Claude adapter implementation evidence

WO-PLG-006 remains in progress. The native manifest, inline guards and focused
tests are implemented, and all C01-C12 observations have been collected. C10 and
C11 failed enforcement and remain unqualified. No supported production profile,
completion, verification, release or merge is claimed by this evidence.

The accepted compatibility boundary remains Claude Code 2.1.266, Windows,
Python 3.14.6 and evaluator 0.16.0. Repository governance uses released 0.17.0
separately. The five packaged shared skills are explicitly namespaced; this work
does not qualify overlap with repository-managed skill copies or implement WO009.

## Current case results

Each canonical `Cnn/` directory contains the required actions, stdout, stderr and
observations. It points back to immutable attempt captures. `reassessment.json`
uses actual structured hook responses and correlated tool ids; it supersedes
the explicitly identified early debug-substring flags without rewriting them.

| Case | Conclusion | Observed boundary |
| --- | --- | --- |
| C01 | pass | Native discovery resolves all five packaged skill names/paths; active bindings and package identity retained. |
| C02 | pass | Startup, resume and real compaction deliver complete 7902-byte context; exact body hash and isolated argv checked. |
| C03 | pass | Checked hook precedes one exact successful Write; correlated denial precedes the refused Write result and target stays unchanged. |
| C04 | pass | Direct accepted inline-command tests refuse missing fields and malformed JSON. |
| C05 | pass | Disabled binding has no receipt; shared script failure produces actual UNREADY context. |
| C06 | pass | Space-containing native paths and unsupported Read observed; exact quotes/Unicode receiving-side transport is separate focused calibration. |
| C07 | pass | Unsupported profile/negative decision rejected; audited helper-spawn log empty and repository Markdown hashes unchanged. |
| C08 | pass | Missing/removed interpreter invokes no Python; wrong evaluator produces identity refusal, not setup-required. |
| C09 | pass | Failed/interrupted/stalled evaluator trees stop; native denial intervals 2.638/2.567/36.181 seconds precede tool errors; no target effects. |
| C10 | fail | Native hook cancellation at 60.162 seconds produces no refusal; exact Write succeeds. |
| C11 | fail | Launch failure, missing output, invalid output and removed binding after prior readiness each allow an exact Write effect. |
| C12 | pass for rejection | Timeout=1 and async bindings are actually loaded and rejected. Both permit Write effects; async check returns after the effect. |

Completing a negative experiment does not make failed enforcement pass. See
[qualification-limit.md](qualification-limit.md) for the concrete blocker,
documented host behavior and the boundary of available remediation.
The collection driver's exit 0 means its requested observations were written;
case verdicts and qualification are recorded separately.

## Candidate and methods

Baseline production bytes have not changed since `1f51da0b`. Attempt 04 packages
source `84c5987054cc0c38410f7ce31951ac2e9b93f242` as
`e7ce223f9a7996ec167313e1d054f8b72c583b72fc08a6e4cb02f6dfafb8eaee`.
Attempt 05 uses a later evidence-only source revision. The 46 source-to-package-
to-loaded comparisons in [candidate-binding.json](candidate-binding.json) all
match. Mutated fault fixtures are labeled separately; the accepted assemblies
remain unchanged. The inert Codex companion is only a builder fixture and grants
no Codex support.

Explicit focused discovery is required because top-level unittest discovery does
not recurse into these directories:

```
../se-harness-plugin-eval-017/Scripts/python.exe -X utf8 -B -m unittest discover -s tests/plugin_integration/claude_adapter -v
```

Direct protocol calibration is distinct from the real native observations in
C01-C03, C05-C06 and C08-C12. The outside observer records target hashes before
launch and after exit, and counts correlated successful native Write results;
that count is not a low-level filesystem write count or a whole-session audit.
The inspected normal-profile metadata is unchanged across all 24 native calls
in attempts 04/05. The API authorization and payload inventory are retained.

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
- `governance/api-scope`: exact inspected payload inventory, automatic approval
  rejection and the subsequent specific operator authorization. No workaround
  was used to bypass that rejection.

Positive or negative case observation is distinct from qualification. The final
engineering disposition and any future assurance must bind the exact candidate;
the current failed routes cannot be promoted by successful unrelated tests.

Host debug/output is sanitized using the existing probe's capture policy.
Credential contents are neither read nor copied by the observer. Raw host debug
stays in disposable sandboxes outside the checkout; do not publish those files.
