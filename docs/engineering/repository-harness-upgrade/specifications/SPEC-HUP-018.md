+++
id = "SPEC-HUP-018"
type = "specification"
title = "Standard-root adoption of released 0.17.0, the simple way, taking the carried obligations"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-09-09"
updated = "2026-09-09"
contract = "A conforming adoption moves the root to released 0.17.0 in one verified transaction, takes the carried obligations into the root, and proves the graph under the new evaluator."

[relations]
specifies = ["REQ-HUP-035", "REQ-HUP-036"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T09:04:33Z"
decided_by = "technical-owner"
reason = "Approved by the accountable repository owner on 2026-09-09 by selecting the presented option 'Approve all five (Recommended)', after reviewing PR #426 (REQ-HUP-035, REQ-HUP-036, SPEC-HUP-018, VER-HUP-018, WO-HUP-018) and the rehearsal of the 0.17.0 root adoption on a throwaway LF clone of main at e855cc9a."
+++

# Specification: Standard-root adoption of released 0.17.0, the simple way, taking the carried obligations

## In plain words

The published 0.17.0 evaluator, installed outside the checkout, upgrades the
managed files in one transaction and adds the risk template. The readings
prove the move and discharge the two obligations wave 5 carried here.

## Scope

The transaction, its evidence, the readings under the new root, the version
move, the bound owner content and the identity-aware test edits. The release
itself is `REL-SEH-028`; the template changes are `SPEC-DST-026` and
`SPEC-DST-027`. Every rule carries a normative keyword and an identifier a
test, a work order or a deviation can cite.

## Terms

- **Managed file.** A file the lock names and the installer writes; 0.17.0
  names forty-one, one more than 0.16.0.
- **Carried obligation.** A rule of a wave 5 specification that binds the
  root adoption of the carrying release: `DST-CFG-015`, `DST-MWF-014`.
- **Control.** The suite run on the same commit's tests under the 0.16.0
  root, whose failure set the moved root must match.

## Rules

**HUP-ADS-001.** The applying runtime MUST be exact public 0.17.0 installed
outside the checkout from the wheel file and run as `python -I -m se_harness`.

**HUP-ADS-002.** The wheel file's SHA-256 MUST equal the digest `RLS-SEH-026`
binds before install, and the written lock's `archive_sha256` MUST equal it.

**HUP-ADS-003.** A guard refusal or a `null` archive pair MUST stop the work
order and MUST NOT be worked around.

**HUP-ADS-004.** The plan MUST contain only the ten `update` actions inside
the managed set and the one `add` of `RISK.template.md`.

**HUP-ADS-005.** A `customized`, `conflict`, `adopt` or `remove` action, or an
`add` beyond the one, MUST stop the work order for review.

**HUP-ADS-006.** The transaction MUST be applied with `harnessctl upgrade .
--apply --evidence-output` retaining exactly one transaction document under
`docs/engineering/repository-harness-upgrade/evidence/`.

**HUP-ADS-007.** The transaction document MUST record prior `tool_version`
0.16.0, the committed lock's digest as the prior lock, and the new lock's
identity as the target.

**HUP-ADS-008.** A second `upgrade .` MUST read every managed file unchanged,
and the written lock MUST name forty-one files.

**HUP-ADS-009.** Directly after apply, exact 0.17.0 MUST pass `validate
--advisories` with 0 errors and 0 advisories, `doctor` with 0 FAIL, `qualify
released-root`, `inspect` and the review preflight.

**HUP-ADS-010.** Two `dashboard` generations MUST agree on every resource
digest outside the generation summary and the manifest.

**HUP-ADS-011.** The candidate MUST move to 0.18.0 in `pyproject.toml` and
`se_harness/__init__.py`, so that `evaluator_facts derive` yields the 0.17.0
to 0.18.0 pair.

**HUP-ADS-012.** The owner region of `AGENTS.md` MUST read `se-harness==0.17.0`
and MUST keep its statements that no `scripts/` path is managed.

**HUP-ADS-013.** `docs/notes/developing-se-harness.md` MUST state the 0.17.0
root and the 0.18.0 candidate, and `SPEC-IAR-012` MUST receive a dated
amendment record for the forty-one-file managed set.

**HUP-ADS-014.** The root `.engineering-harness.toml` MUST take the five-key
form the release writes, and the evidence MUST record its new digest.

**HUP-ADS-015.** The root `engineering-harness.yml` MUST take the release's
template and the root `.gitignore` block MUST sit between hash markers.

**HUP-ADS-016.** A test that pins the 0.16.0 root's shape MUST key on the
lock's identity or hold that shape as a fixture.

**HUP-ADS-017.** The suite's failure set on the moved root MUST equal the
control's beyond the workstation baseline error.

**HUP-ADS-018.** Candidate template bytes under `templates/` and product
bytes under `se_harness/` other than the version MUST NOT change.

**HUP-ADS-019.** Every pull-request lane MUST pass, the governor-transition
lane assessing the real 0.16.0 to 0.17.0 move with `RLS-SEH-026` supplying
the wheel.

**HUP-ADS-020.** The work order MUST stop before merge, verification,
release or publication, each of which is a separate decision.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| The runtime resolves inside the checkout | the guard refuses and nothing is written (HUP-ADS-003) | `MG005` |
| A managed file differs from its lock entry | the plan reads `customized` and the transaction refuses (HUP-ADS-005) | `customized` |
| The evidence path resolves outside the repository | the command refuses before writing (HUP-ADS-006) | `upgrade evidence path must be repository-relative` |
| The candidate is still 0.17.0 after the move | the derivation fails closed (HUP-ADS-011) | `PRE008` |
| The suite differs from the control beyond the baseline | the work order stops for amendment (HUP-ADS-017) | none |

## Examples

**Given** the rehearsal clone of `main` at `e855cc9a`, **when** 0.17.0 plans
the upgrade, **then** 41 files read 10 `update`, 1 `add` and 30 unchanged
(HUP-ADS-004).

**Given** the applied rehearsal, **when** it replays, **then** 41 files read
41 unchanged and the lock names forty-one files (HUP-ADS-008).

**Given** the applied rehearsal, **when** 0.17.0 reads it, **then** 1,437
artifacts, 0 errors, 46 warnings, 0 advisories and 99 managed checks
(HUP-ADS-009). `RR001` to `RR004` pass.

**Given** the applied rehearsal, **when** the Explorer generates twice,
**then** 1,720 of 1,722 resources carry one digest (HUP-ADS-010).

**Given** the applied rehearsal, **when** its configuration is read, **then**
it holds `tool_version`, `installed_at`, `project_name`,
`required_for_verified_work` and `required_for_release` (HUP-ADS-014).

**Given** the wheel downloaded from the GitHub release, **when** its digest is
read, **then** it equals `305c7cbc…` and the payload reads `dd48b16b…`
(HUP-ADS-002).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-HUP-035` | HUP-ADS-001, HUP-ADS-002, HUP-ADS-003, HUP-ADS-004, HUP-ADS-005, HUP-ADS-006, HUP-ADS-007, HUP-ADS-008, HUP-ADS-018, HUP-ADS-020 |
| `REQ-HUP-036` | HUP-ADS-009, HUP-ADS-010, HUP-ADS-011, HUP-ADS-012, HUP-ADS-013, HUP-ADS-014, HUP-ADS-015, HUP-ADS-016, HUP-ADS-017, HUP-ADS-019 |

## Not decided here

- The name of the external environment and the order of the readings.
- The wording of the owner-content statements and of the amendment record.
- The exact identity-aware form of each test edit.
- Whether the root `.gitignore` lines duplicating the fragment are dropped,
  which `DST-MWF-014` leaves to the work order.
