```toml
artifact = "WO-ECP-030"
checkpoint = "handoff"
formal_snapshot_sha256 = "0000000000000000000000000000000000000000000000000000000000000000"
rebound_at = "2026-09-07T00:00:00Z"
```

# WO-ECP-030 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The dormant surface the owner retired on 2026-09-07 (issue #381) is gone.
`se_harness/renumber.py`, `se_harness/recovery_rehearsal.py` and
`se_harness/journaled_apply.py` are deleted with their three test modules;
`renumber-artifacts` and `rehearse-recovery` are no longer registered, and
argparse refuses both as any unknown command, exit 2, with no guard. The
mutation guard's operation set lost `renumber-artifacts-apply`; the
diagnostic-code registry lost the `REN` and `JNL` families and
`docs/notes/diagnostic-codes.md` was regenerated. The two contract entries
no checkpoint could reach are gone from `quality_gates_contract.json`
(`QG-G0-INTENT` with `QGP-G0-GRAPH` and `QGP-G0-INTEGRITY`) and
`workflow_contract.json` (`PROC-CANDIDATE-COMMIT` with
`STEP-CANDIDATE-COMMIT-AUTHORIZE`), removed textually so the hand-formatted
files keep their layout; the candidate template copies `QUALITY_GATES.json`,
`QUALITY_GATES.md`, `WORKFLOW.json` and `WORKFLOW.md` match, and the
`QG-G0` row left `harnessctl-check.md`. The command reference lost both
commands' rows, synopses and sections, and the recovery runbook states the
retirement and describes a hand-run rehearsal. Thirteen dated amendment
records close the definitions that named the retired surface, two of them
correcting the packet's own rule `ECP-DEL-022`, which had listed release
qualification's live `RR` family among the prefixes to drop. The root
copies of the four managed documents are the released 0.16.0 files and are
untouched; this repository sees the template change at its next root
adoption.

## Evaluators

- Governing: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/mathi/se-harness-eval-0160`), `-I`, wheel-installed, for every
  governing reading, this packet and the handoff check. Its candidate
  acceptance invokes neither retired command.
- Candidate: this checkout, branch `wo/ecp-030-dormant` off `main` at
  `34193ca` (the merge of PR #390, group B).

## Readings (VER-ECP-024, group C)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.16.0 | Errors: 0, Warnings: 73 (the `main` baseline), Advisories: 0 |
| `doctor` | exact 0.16.0 | 0 FAIL: the root managed set is untouched |
| review preflight `--work-order WO-ECP-030` | exact 0.16.0 | PASS |
| `harnessctl --help` before | candidate | `renumber-artifacts` and `rehearse-recovery` listed; the three modules present in the package tree |
| `harnessctl --help` after | candidate | neither listed; `harnessctl renumber-artifacts .` and `harnessctl rehearse-recovery .` exit 2 with the usage error (`ECP-DEL-021`, `-032`) |
| `load_validated_contracts()` | candidate | loads; `PROC-CANDIDATE-COMMIT` and `QG-G0-INTENT` absent from both package contracts (`ECP-DEL-024`, `-025`) |
| `cmp` package contract against candidate template | candidate | byte-equal for both contracts (`ECP-DEL-024`, `-025`) |
| `python -m repository_tools.diagnostic_code_index --check` | candidate | the committed page equals the regeneration; no `REN`, no `JNL`, `RR` retained (`ECP-DEL-022` as corrected, `-023`) |
| `python -m unittest` over the ten affected modules | candidate, Windows 11 | 343 tests, OK after the two pin updates below |
| `python scripts/run_tests.py` | candidate, Windows 11 | section below |
| `check --checkpoint handoff --from-git 34193ca` | exact 0.16.0 | section below |

### Pins that moved

- `tests/test_cli_shape.py`: both names out of the pinned sets; the two
  through-`main()` tests of the retired commands deleted (`ECP-CLI-008` as
  amended).
- `tests/test_mutation_guard.py`: the `apply_renumber_plan` mutator and the
  `renumber-artifacts-apply` inventory entry out.
- `tests/test_release_build.py`: the `journaled_apply.py` wheel-membership
  assertion out.
- `tests/test_diagnostic_code_index.py`: `JNL001` and `REN010` out of the
  known-code list.
- `tests/test_validation_taxonomy.py`: a declared divergence branch, as the
  file already carries for earlier roots: while the root `QUALITY_GATES.md`
  still carries the two `QG-G0-INTENT` rows, the candidate template equals
  the root minus those rows (`ECP-DEL-028`).

### The Windows suite

`python scripts/run_tests.py` on this Windows 11 workstation (CPython 3.14,
CRLF checkout) after the change: 1,256 tests (thirty fewer: the three
deleted modules and the two through-`main()` tests), 26 skipped, 1 error
and 1 failure, both the names of this machine's baseline on `main`
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a `PermissionError` on a temporary `.git` object;
`test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`,
the `AGENTS.md` owner region measured on a CRLF checkout, recorded on a fresh
worktree of `main` under `WO-ECP-027`). No other name differs.

### Handoff check

`check . --artifact WO-ECP-030 --checkpoint handoff --from-git 34193ca`,
exact 0.16.0: Completed; every `QGP-G4I-*` predicate passes; every changed
path inside the declared scope; `complete: true`; the self-binding result
retained as `handoff.json` beside this packet.

## Material non-effects

The root managed documents, the lock and every other registered command are
unchanged; `RR` and every other live code family stays in the registry; the
`hash_bound` declared-digest chain stays for #377; the three deleted modules
had no product caller (`renumber` and `recovery_rehearsal` only their CLI
entries, `journaled_apply` none).

## Hosted lanes

Read on the pull request at the completion decision; recorded in the
completion event's reason.
