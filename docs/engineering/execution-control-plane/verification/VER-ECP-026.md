+++
id = "VER-ECP-026"
type = "verification"
title = "Verify wave 3: one imported engine, one validation per command, the splits"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-ECP-035"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:13:26Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all six (Recommended)', given after the stacked packet pull requests #404, #405 and #406 and their summary were presented: wave 3 of the code health assessment of 2026-09-07 (issue #378) and the revisit triggers of DEC-ECP-001 and DEC-ECP-002, the engine as an import surface, one validation per governance command, the three largest modules split along their seams, every recorded output byte-identical. Approval of a definition authorizes no work."
+++

# Verification Contract: Verify wave 3: one imported engine, one validation per command, the splits

## Independence

Expected values come from `REQ-ECP-035` and the rules of `SPEC-ECP-024`;
the twin list, the repeated-validation sites and the eleven functions above
60 are those the assessment of 2026-09-07 recorded and the before readings
are compared with them. Every byte-identity expectation is read from `main`
or from a committed record, never from the changed code.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-035` import surface | test: every engine module imported under `se_harness.engine`; grep of `spec_from_file_location` and `ENGINE_ROOT` in the package; `python -m se_harness.engine.<name> --help` for the three entry modules | no path load in the package; each entry module runs with its arguments and exit codes unchanged (`ECP-ENG-001` to `-003`) |
| `REQ-ECP-035` twins | test: the layout tables, the lifecycle loader, the evidence validator, the status set and the body parser each imported from one module; grep of the former copies | one definition each; the copies are gone; the duplication scan reports none of the three engine blocks (`ECP-ENG-004` to `-008`) |
| `REQ-ECP-035` codes | test: no code literal in `se_harness/engine/`; the regenerated code page equals the committed one | the registry names every engine code; the page matches (`ECP-ENG-009`) |
| `REQ-ECP-035` one validation | test: each governance command run on a fixture repository under a patch that counts `validate_repository` | exactly one call for a command that validates, none for one that does not (`ECP-ENG-010` to `-015`) |
| `REQ-ECP-035` byte identity | comparison on this repository at each group's completion: the formal snapshot digest of every work order in `check --checkpoint handoff`, the dashboard manifest digest, `result_sha256` of `check` on three artifacts, `validate --json` and the human rendering | every value equals `main`'s (`ECP-ENG-016`) |
| `REQ-ECP-035` structure | `radon cc -j` over the package; an import test over every module's `from se_harness.<module> import` names; `wc -l` of the split modules | no function above 60; no private name crosses modules; the three modules are split as the rules name (`ECP-ENG-017` to `-022`) |
| `REQ-ECP-035` digests | the release-qualification, hash-bound, installer and evidence suites; `CONTRACT_SHA256`; `git diff --name-only` | every recorded digest equals `main`'s; no contract JSON or template byte changes (`ECP-ENG-023`, `-024`) |
| `SPEC-ECP-024` records | inspection | every amendment record `ECP-ENG-025` requires is present, dated and names the specification |
| `REQ-ECP-035` regression | the full suite; `validate`; `doctor`; the hosted lanes | suite at its baseline; graph 0 errors; every lane green (`ECP-ENG-026`) |

## Acceptance scenarios

- Run the byte-identity comparison at the base of each group and at its
  candidate; record both readings in the group's evidence.
- Run every governance command on the fixture repository under the counting
  patch and record the count per command.
- Run `radon cc` and the duplication scan on `main` and on the group C
  candidate; record both readings.

## Evidence retention

One evidence packet per work order under
`docs/engineering/execution-control-plane/evidence/`, holding the
byte-identity readings, the call counts, the complexity and scan readings,
the suite reading, `validate` and `doctor` readings and the hosted lane ids.

## Pass criteria

Every row of the matrix passes for every group; the pull requests' lanes are
green through completion and the record heads; no managed path moves.

## Residual uncertainty

The byte-identity comparison runs on this repository's own graph, which
exercises every pass the validator has today but not every branch of every
pass; the suite's fixtures cover the rest. `radon` runs in a scratch
environment on this workstation, not in a lane.
