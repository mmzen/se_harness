# Claude adapter implementation evidence

WO-PLG-006 remains in progress. The native manifest, inline guards and focused
tests are implemented; live qualification is incomplete. No supported production
profile, completion, verification, release or merge is claimed by this evidence.

The accepted compatibility boundary remains Claude Code 2.1.266, Windows,
Python 3.14.6 and evaluator 0.16.0. Repository governance uses released 0.17.0
separately. The five packaged shared skills are explicitly namespaced; this work
does not qualify overlap with repository-managed skill copies or implement WO009.

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
- `governance/api-scope`: exact inspected payload inventory, automatic approval
  rejection and the subsequent specific operator authorization. No workaround
  was used to bypass that rejection.

Positive or negative case observation is distinct from qualification. C09-C12
still need real host timing, correlated denial/tool results and independent
target observations. The runner records final target hashes independently,
correlates Write ids/results, and labels its effect-count basis explicitly; it
does not claim a whole-session filesystem audit. Original failures remain retained.

Host debug/output is sanitized using the existing probe's capture policy.
Credential contents are neither read nor copied by the observer. Raw host debug
stays in disposable sandboxes outside the checkout; do not publish those files.
