# Historical release rehearsal correction — proposed

The 0.23.0 preparation can continue, but its required historical-record rehearsal
has a new unresolved failure. **R23-REHEARSAL-001 remains open and blocking**;
no final verification or release readiness is claimed.

The [manual CI run](https://github.com/mmzen/se_harness/actions/runs/38895333553)
passed candidate replay and simulated complete-delivery/recovery. Its earlier
RLS-SEH-033 qualification failed with `approved documentation differs: README.md`.
Local reproduction returned the same refusal. The current resolver compares the
approved documentation with three commits: the approved documentation commit,
the release's integration commit, and current main. That last condition belongs
to a live delivery check; later documentation can prevent historical rehearsal.

Proposed WO-RLS-055 separates these purposes within the existing tooling:
historical qualification validates immutable approved inputs; live publication
continues to require current-main consistency. Preserve all other provenance,
candidate, evidence, required-check and authority controls. No alternate publisher
or second build lane is proposed. Tests must prove both the historical success
case and unchanged live refusal, including tampered historical inputs.

The bounded scope is three existing resolver/workflow files, their regression
test, two existing release notes and this release domain. The exact linked
REL-SEH-036 proposal adds only WO-RLS-055. Its accepted bytes and unchanged
lifecycle history are retained. Neither code nor the REL amendment is applied.

Approval requested: WO-RLS-055, required commit-bound verification in the final
aggregate record, bounded manual activation of that exact REL revision, and
updates to existing draft PR #544 on codex/release-0-23-0 targeting main.
Human verification, merge, complete release, adoption and host changes remain
separate. DEC-RLS-010/011 remain limited to the original instruction findings
and unverified desktop; they do not dispose of this new rehearsal failure.
