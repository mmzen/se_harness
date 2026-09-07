+++
id = "SPEC-HUP-017"
type = "specification"
title = "Standard-root adoption of released 0.16.0, the simple way, with the retired scripts leaving"
status = "draft"
owners = ["technical-owner", "engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"
contract = "A conforming adoption moves the root to released 0.16.0 in one verified transaction, removes the eight retired script copies, and redirects their last consumers to the evaluator."

[relations]
specifies = ["REQ-HUP-033", "REQ-HUP-034"]
+++

# Specification: Standard-root adoption of released 0.16.0, the simple way, with the retired scripts leaving

## In plain words

The published 0.16.0 evaluator, installed outside the checkout, upgrades the
managed files in one transaction that also removes the eight script copies
it no longer installs. Everything here that still read those copies reads
the evaluator afterwards, and the readings prove the move.

## Scope

The transaction, its evidence, the readings under the new root, the version
move, the bound owner content and workflows, and the identity-aware test
edits. The release itself is
`REL-SEH-027`; the engine relocation is `SPEC-DST-025`. Every rule carries a
normative keyword and an identifier a test, a work order or a deviation can
cite.

## Terms

- **Root copy.** A file the 0.15.0 evaluator installed under `scripts/`
  and hash-locked; 0.16.0 installs none.
- **Engine copy.** The same program inside the installed package, at
  `se_harness/engine/` in candidate source.
- **Control.** The suite run on the same commit's tests under the 0.15.0
  root, whose failure set the moved root must match.

## Rules

**HUP-ADP-001.** The applying runtime MUST be exact public 0.16.0 installed
outside the checkout from the wheel file and run as `python -I -m se_harness`.

**HUP-ADP-002.** The wheel file's SHA-256 MUST equal the digest `RLS-SEH-025`
binds before install, and the written lock's `archive_sha256` MUST equal it.

**HUP-ADP-003.** A guard refusal or a `null` archive pair MUST stop the work
order and MUST NOT be worked around.

**HUP-ADP-004.** The plan MUST contain only `update` actions inside the
managed set and `remove` actions for the eight retired copies
`SPEC-DST-025` names.

**HUP-ADP-005.** A `customized`, `conflict`, `add` or `adopt` action, or a
`remove` beyond the eight, MUST stop the work order for review.

**HUP-ADP-006.** The transaction MUST be applied with `harnessctl upgrade .
--apply --evidence-output` retaining exactly one transaction document under
`docs/engineering/repository-harness-upgrade/evidence/`.

**HUP-ADP-007.** The transaction document MUST record prior `tool_version`
0.15.0, a prior lock digest equal to the committed lock blob, and a target
identity equal to the new lock.

**HUP-ADP-008.** A second `upgrade .` MUST read every remaining managed file
unchanged, and the written lock MUST carry no `scripts/` entry.

**HUP-ADP-009.** Directly after apply, exact 0.16.0 MUST pass `validate
--advisories` with 0 errors and 0 advisories, `doctor` with 0 FAIL, `qualify
released-root`, `inspect` and the review preflight.

**HUP-ADP-010.** Two `dashboard` generations MUST agree on every resource
digest outside the generation summary and the manifest.

**HUP-ADP-011.** The candidate MUST move to 0.17.0 in `pyproject.toml` and
`se_harness/__init__.py`, so that `evaluator_facts derive` yields the 0.16.0
to 0.17.0 pair.

**HUP-ADP-012.** The owner region of `AGENTS.md` MUST name the evaluator's
`validate` as the Graph command, state that no `scripts/` path is managed,
name `se_harness/engine/`, and read `se-harness==0.16.0`.

**HUP-ADP-013.** `docs/notes/developing-se-harness.md` MUST state the 0.16.0
root, the 0.17.0 candidate and the departed root copies, and `SPEC-IAR-012`
MUST receive a dated amendment record.

**HUP-ADP-014.** `release-qualification.yml` and `release-candidate-replay.yml`
MUST validate the graph with `python -m se_harness validate .` and MUST
change nothing else.

**HUP-ADP-015.** `pages-publication.yml` MUST generate the Explorer with the
proven released evaluator's `dashboard` over the generation snapshot and
MUST change nothing else.

**HUP-ADP-016.** A test that reads a root copy MUST read it only when the
lock names it and MUST otherwise read the engine copy or assert the copy's
absence.

**HUP-ADP-017.** The suite's failure set on the moved root MUST equal the
control's beyond the workstation baseline error.

**HUP-ADP-018.** Candidate template bytes under `templates/` and product
bytes under `se_harness/` other than the version MUST NOT change.

**HUP-ADP-019.** Every pull-request lane MUST pass, the governor-transition
lane assessing the real 0.15.0 to 0.16.0 move with `RLS-SEH-025` supplying
the wheel.

**HUP-ADP-020.** The work order MUST stop before merge, verification,
release or publication, each of which is a separate decision.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| The runtime resolves inside the checkout | the guard refuses and nothing is written (HUP-ADP-003) | `MG005` |
| A retired copy differs from its lock entry | the plan reads `customized` and the transaction refuses (HUP-ADP-005) | `customized` |
| The candidate is still 0.16.0 after the move | the derivation fails closed (HUP-ADP-011) | `PRE008` |
| A workflow still names a root copy | the next release's lane fails on a missing file (HUP-ADP-014, HUP-ADP-015) | none |
| The suite differs from the control beyond the baseline | the work order stops for amendment (HUP-ADP-017) | none |

## Examples

**Given** the rehearsal clone of `main` at `5df10aa9`, **when** 0.16.0 plans
the upgrade, **then** 48 files read 6 `update`, 8 `remove` and 34 unchanged
(HUP-ADP-004).

**Given** the applied rehearsal, **when** it replays, **then** 40 files read
40 unchanged and the lock names forty files, none under `scripts/`
(HUP-ADP-008).

**Given** the applied rehearsal, **when** 0.16.0 reads it, **then** 1,346
artifacts, 0 errors, 73 warnings, 0 advisories, 97 managed checks and
`RR001` to `RR004` pass (HUP-ADP-009).

**Given** the applied rehearsal, **when** the Explorer generates twice,
**then** 1,601 of 1,603 resources carry one digest (HUP-ADP-010).

**Given** the rehearsal with no test edit, **when** the suite runs, **then**
six modules fail to import and 27 names fail, all on root copies
(HUP-ADP-016).

**Given** the wheel downloaded from PyPI, **when** its digest is read,
**then** it equals `a969d6ab…` and the payload reads `51712fcf…`
(HUP-ADP-002).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-HUP-033` | HUP-ADP-001, HUP-ADP-002, HUP-ADP-003, HUP-ADP-004, HUP-ADP-005, HUP-ADP-006, HUP-ADP-007, HUP-ADP-008, HUP-ADP-018, HUP-ADP-020 |
| `REQ-HUP-034` | HUP-ADP-009, HUP-ADP-010, HUP-ADP-011, HUP-ADP-012, HUP-ADP-013, HUP-ADP-014, HUP-ADP-015, HUP-ADP-016, HUP-ADP-017, HUP-ADP-019 |

## Not decided here

- The name of the external environment and the order of the readings.
- The wording of the owner-content statements and of the amendment record.
- The exact identity-aware form of each test edit.
- The exact form of each workflow line, provided it invokes the evaluator.
