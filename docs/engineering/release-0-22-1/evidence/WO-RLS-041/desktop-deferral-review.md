# Desktop qualification decision for plugin 0.2.6

**Recorded decision:** mmzen accepted DEC-RLS-009 and its paired RISK-RLS-007
for evaluator 0.22.1 / plugin 0.2.6 only: "Accept the bounded desktop omission and risk".

Codex Windows desktop tests have not run. A desktop-specific instruction or
checkout-selection defect could remain undetected. The released 0.22.0 evaluator recorded the decision as `decided` and the paired
risk as `accepted`. Neither result claims a passing desktop test.

| Accepted boundary | Still required |
| --- | --- |
| Continue qualification with desktop explicitly unverified. | Passing Codex CLI and Claude Code checks, portable tests and exact package identities. |
| Carry the known desktop uncertainty in verification and release reviews. | Human acceptance of the final commit-bound verification record. |
| Keep desktop outside verified-host claims. | Public fresh-install and update checks on Codex CLI and Claude Code; all delivery controls. |

Revisit before the next plugin release or before any verified-desktop claim,
whichever comes first. mmzen owns follow-up. Changed scope or versions require
new review. Acceptance does not approve verification, merge, publication or
adoption.

The formal [decision](../../decisions/DEC-RLS-009.md) is `decided`; its
[risk](../../risks/RISK-RLS-007.md) is `accepted`. The [acceptance observations](desktop-acceptance-observations.zip)
retain the exact preview, apply and readback. The original proposal remains in
[its preparation archive](desktop-proposal-preparation.zip).

## Other readiness items

The exact GitHub pypi reviewer-only change is applied and read back in
[the activation receipt](../WO-RLS-040/provider-configuration-applied.json).
The main-only deployment rule, main protections and workflow permissions are
unchanged. mmzen confirmed the four PyPI Trusted Publisher fields; that is a
human confirmation, not an authenticated browser read by the agent.

PR #536 at 36a8b8868d2584f2eab6a770ae64f69076a5bb5b has 17 passing checks;
two extra rehearsal jobs were skipped by the PR policy. The previous separate
manual rehearsal retains those two executed legs. This does not verify a new
final release candidate.
