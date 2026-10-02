# Public 0.21.0 / plugin 0.2.4 delivery observations

WO-RLS-033 is in progress. The marketplace is public at
`7e366438165a40a14783bac650a2887e7ec8bc75`. Its 69 files match the qualified
package; see [publication.json](publication.json).

Fresh installation and update from the preserved public 0.2.3 package passed
on Codex CLI 0.159.2 and Claude Code 2.1.273. Each of the four routes matches
all 29 installed files, the public revision and the bundled 0.21.0 wheel.
These are package installation observations, not proof of a complete model session.
See [routes.json](routes.json) and the original command receipts in `commands/`.
All four [setup checks](setup.json) passed: isolated evaluator identity, two-file
initialization, doctor, resource lookup and repeated environment reuse.

Fresh [Codex CLI/app-server tests](public-codex-native.json) of the exact public
distribution passed startup, explicit activation, manual and automatic compaction,
and resume. The existing trusted disposable profile supplied authentication and
hook trust. Its 29 package files and host version match both public installation
routes. The fixture repository was preserved and the prior plugin restored.

Human mmzen accepted the missing Claude native session tests through
[DEC-RLS-003](../../decisions/DEC-RLS-003.md). [RISK-RLS-003](../../risks/RISK-RLS-003.md)
is accepted. Claude remains unverified; no authentication refresh or missing
test pass is inferred. The acceptance covers WO-RLS-033 and this exact package.
Codex Windows desktop remains unverified, with its separate boundary awaiting
[DEC-RLS-004](../../decisions/DEC-RLS-004.md). Earlier decisions remain unchanged.

The [native observations](native.json) record registered but untrusted Codex hooks
in both disposable profiles. Claude's init-only bootstrap callback passed in
both profiles; it did not run an authenticated model session. No hook trust or
credentials were changed. The [updated assessment](native-v2.json) distinguishes
these installation profiles from the trusted profile used for the new Codex
session tests. Native traces are retained under `native/codex-public/`.

Current guidance is being corrected. The already-published package retains its
original source bytes, including pre-publication wording in its bundled READMEs.
Source documentation corrections do not alter those published bytes.
The [updated review](review-v2.json) and [initial review](review.json) retain the correction and unresolved findings. All
28 documentation tests pass; the original failed link check is also retained.

The [current delivery check](checks-v3.json) reports valid inputs and incomplete
delivery. Evaluator publication and Pages provenance are satisfied. Marketplace
desktop disposition and documentation integration remain pending. The first check
in [checks.json](checks.json) also recorded a URL spelling mismatch; the second
observation records its normalization from native marketplace readback without
altering original route receipts. `latest` is still `v0.20.1`; `last` is still
`b9af631b850c495eace9807361ed3ec3e36a10b2`. Neither marker was moved.

Overall delivery remains incomplete: the desktop evidence decision, documentation
verification/integration/readback, and separately authorized latest/last observations
remain outstanding. This repository still selects evaluator 0.20.1; no adoption occurred.
