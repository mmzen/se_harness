+++
id = "VER-PLG-024"
type = "verification"
title = "Verify bounded root cleanup and plugin ownership adoption"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-16"
updated = "2026-09-16"

[relations]
verifies = ["REQ-PLG-032", "REQ-PLG-033", "REQ-PLG-034", "REQ-KIS-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T09:05:14Z"
decided_by = "assurance-owner"
reason = "On 2026-09-16 the owner approved VER-PLG-024 and WO-PLG-024 in response to the exact reviewed draft package and named roles. Record assurance-owner approval of this verification contract, reviewed SHA-256 026aa850c7064f6081cc7a38c824df6beea1cfd217303ca4276125699fc0b798. No future VREC assurance decision is implied."
+++

# Verify bounded root cleanup and plugin ownership adoption

## Independence

Expected behavior comes from REQ-PLG-032/033/034, REQ-KIS-009,
SPEC-PLG-021 and SPEC-KIS-003. The baseline Git tree and pre-change lock fix
the preservation comparison; candidate output cannot define its own expected
inventory or successful result. This contract verifies adoption in WO-PLG-024,
not a new implementation or release of the ownership command.

Use the selected, isolated released SE Harness 0.18.0 evaluator for governance
and migration checks. Record candidate-source 0.19.0 tests separately. The
local acceptance platform is Windows with the available Python 3.13 runtime;
the existing CI retains its own platform checks if this work is later submitted.
Do not claim an unobserved Linux, native-host, CI or publication result.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-PLG-032 | Inspection and existing tests | C01 migration preview/application; C04 regression suite | The complete replacement is checked before removal; all seven selected root skill files disappear and their lock entries are removed. Existing missing-replacement checks pass. |
| REQ-PLG-033 | Inspection, demonstration and existing tests | C01 bounded diff; C02 disposable restoration/rerun; C04 regression suite | Only authorized paths change; restoration and repeat switching work in the fixture. Existing interrupted-operation and redirected-path rejection tests pass. |
| REQ-PLG-034 | Inspection and demonstration | C01 lock comparison; C02 plugin-independent check/upgrade | Schema 4 records only the portable provider choice; doctor and an ordinary same-release upgrade need no plugin path and do not restore duplicate skill copies. |
| REQ-KIS-009 | Inspection and released workflow checks | C03 current guidance; C04 selected procedure | The obsolete delegation configuration is absent; current guidance and actual execution follow the approved-WO route without a separate delegation class or live-PR authorization prerequisite. Reserved owner decisions remain explicit. |

## C01 — Actual root migration and preservation

Before execution, compare the checkout with WO-PLG-024's baseline and exact
scope. Inspect the installed Verity Plane native manifest and the six nonempty
replacement files specified by PLG-KIS-004. Run a fresh released
`skill-ownership --provider plugin --plugin-root PATH` preview. Check every
resolved deletion directory is inside this repository and contains only the
authorized files. This presence check proves neither native discovery nor
authenticity. Apply only under approved scope.

After application and removal of the obsolete TOML, inspect the full tracked
diff: exactly those eight files are removed. Compare parsed locks: the schema
and provider change, the seven skill entries disappear, and every unrelated
entry plus the selected evaluator identity is equal. No local plugin path,
version or fingerprint is stored. Root managed files and instruction fragments,
product templates, plugin/package inputs, source/tests, older formal records
and retained evidence are unchanged. Preserve the owner's README changes and
the already deleted value-proposition documents.

## C02 — Portability and restoration

Use a disposable copy outside the source checkout, scoped to this adoption
check. With the migrated lock and no plugin path supplied, released doctor
passes. Run the released ordinary same-version upgrade in that fixture; the
provider remains `plugin`, and none of the seven repository skill files returns.
Restore repository ownership using the released command, check the seven
template copies and ordinary lock inventory, then switch to plugin ownership
again and repeat the switch. Each operation reports its actual outcome and the
last two operations converge on the same portable provider/inventory. Never
exercise restoration or upgrade against the real checkout during this check.

Reuse the existing ownership test coverage for interrupted operations, unsafe
destinations and missing replacements; do not add an exhaustive fault matrix or
new production behavior. A necessary source fix exceeds this adoption WO.

## C03 — Contributor guidance and skill availability

Review the selected guidance as a contributor arriving at this repository.
It identifies the plugin provider, links the existing installation instructions,
explains per-host setup and the released restoration option, and distinguishes
plugin skill invocation from running the evaluator. It describes the current
root as released 0.18.0 with schema 4 and preserves candidate/released separation.
The execution note and index no longer present the obsolete delegation setting
or a green PR check as a prerequisite for routine approved execution.

The old plugin proposal and dated KISS plan are clearly labelled historical
and point to current guidance or recorded completion; their original dated
analysis remains readable. The domain index distinguishes this new work from
earlier verified or published work. Check edited links and AGENTS.md's managed
fragment against the baseline.

Observe native skill discovery on each already available host where a read-only
check or disposable profile can do so. Report Codex and Claude Code separately.
Earlier retained marketplace-installation/discovery evidence may cover an
unavailable host only when the relevant package and discovery inputs are shown
unchanged and its tested versions and limitations are named. A missing host
does not imply a fresh pass. Unchanged package acceptance can support this
root-only adoption; changed relevant inputs or unavailable matching evidence
leave discovery coverage incomplete and require owner resolution. Do not
alter persistent user profiles or install a plugin as an incidental check.

## C04 — Required checks, scope and review

Run the full repository-required source suite once, including its existing
ownership, onboarding and documentation checks. Run distribution validation and
the CLI smoke required by AGENTS.md. Use the external released evaluator for
doctor, graph validation and the phase-appropriate selected WO checks,
preflight, scope and handoff. Retain candidate/released identity differences
as observed; they do not authorize replacing root managed content.

Every required check must pass, with zero graph errors and no unresolved
selected-scope gate failures. Existing unrelated graph warnings are recorded
as baseline observations, not new blockers or waived checks. Inspect the
complete change set and apply ARTIFACT_AUTHORING.md's design and implemented
change review questions: each change serves this cleanup, existing behavior is
reused, and no extra approval protocol, build, test framework or historical
evidence rewrite has been introduced. Resolve material in-scope findings and
record the reasoning; escalate any necessary change outside this WO.

## Evidence retention

Retain one concise coverage/review summary and relevant actual command results
under `docs/engineering/plugin-integration/evidence/WO-PLG-024/`. Include the
baseline and candidate identities, before/after lock comparison, exact removal
list, evaluator identity, platform, checks, any reused evidence identities and
material limitations. Keep fixture trees and bulky diagnostics outside the
checkout. Reuse successful full-suite coverage instead of duplicating its tests.

Prepare VREC-PLG-021 through the released procedure only after the candidate
and required evidence are complete. The prepared record is a separate later
governance commit; preparation makes no assurance decision.

## Residual uncertainty

This verifies the local repository adoption and unchanged package compatibility.
It does not promise future host releases, authenticate marketplace provenance,
verify official catalog acceptance or assess historical evidence for deletion.
Scope is intentionally small; the expected storage saving is incidental.
