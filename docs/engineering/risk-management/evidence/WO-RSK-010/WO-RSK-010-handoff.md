```toml
artifact = "WO-RSK-010"
checkpoint = "handoff"
formal_snapshot_sha256 = "1194004262e0a40fe3595d01335f825431c33130d000f75b05fafeacf29c8e45"
rebound_at = "2026-09-07T22:02:54Z"
```

# WO-RSK-010 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored. The
schema-2 handoff result of the Git-derived checkpoint is retained beside this
file as `handoff.json`; the measurements it summarises are in
`../WO-RSK-010-verification.md`.

## Outcome

A threat to governed work is a governed file. `harnessctl raise-risk`
computes the five-by-five score, writes the risk in `raised` and, with
`--with-decision`, the open decision that blocks the threatened artifacts with
the options `accept`, `avoid` and `mitigate`. No gate reads risks: the stop on
a threatened artifact is the paired decision's `QGP-*-DECISION` predicate,
unchanged, and its refusal names the decision and its options, never the risk.
`harnessctl decide` moves every raised risk the decision concerns in the same
journalled act, copies the option, its label, the role, the time and the
verbatim reason onto the risk, records `mitigated_by` or `avoided_by`, and
leaves the risk `raised` on a deferral. `harnessctl risks` lists the threats to
an artifact and its governing chain and writes nothing. The scope check admits
an added risk file of the work order's own domain to an in-progress work
order's change set, and only an added one. No configuration key exists; the
installed template keeps its five keys.

## Rules and their covering tests

Every rule assigned to this work order, RSK-MGT-001 to RSK-MGT-021,
RSK-MGT-026, RSK-MGT-027, RSK-MGT-031, RSK-MGT-033, RSK-MGT-034 and
RSK-MGT-036, has a case in `tests/test_risk_management.py` that cites it; the
rule-to-case map is the first section of `../WO-RSK-010-verification.md`. For
RSK-MGT-036 the module was run unchanged against `main`'s code in a clean
worktree and every case failed there; the counts are recorded in that file.

## Diagnostics added

`E-RSK-001` (a declared field missing or invalid), `E-RSK-002` (a measurement
outside 1 to 5, or a score that is not the product), `E-RSK-003` (a raised
risk named by no, or more than one, pending decision), `E-RSK-004` (the paired
decision's `blocks` differs from the risk's `threatens`), `E-RSK-005` (a
disposition typed by hand, missing, or not naming the state) and `W-RSK-001`
(an accepted risk past its revisit with no pending decision). The refusals of
`raise-risk` and of a bare `transition` on a risk carry the generic `WEX201`
code of the transition planner; no new `WEX` code was registered. `E-RSK-006`
to `E-RSK-008` are `WO-RSK-011`'s.

## Files changed against the declared scope

Twenty-nine files in the implementation commit and the two evidence files;
every one is within `[execution_scope].paths` after the two amendments the
owner approved under `DR-REMEDIATION-SCOPE`. The scope checkpoint against
`origin/main` reads `QGP-G4I-SCOPE pass`, `QGP-G4I-COMPLETE pass`,
`QGP-G4I-PATHS pass` with a complete change set. Both quality-gates contract
copies and both workflow contract copies are byte-identical pairs.

## Configuration and predicate-set readings

The installed configuration template declares five keys and no risk table.
The predicate identifier sets of both quality-gates contract copies equal
`main`'s (45 identifiers; 11 gate groups). The `risk` lifecycle family has
exactly the specification's edges, and no risk state grants authority.

## Governing readings

Released se-harness 0.16.0, `-I`, from outside the checkout, Windows 11, at
candidate `b6843d8`: `validate .` reads `Artifacts: 1384 | Errors: 0 |
Warnings: 73 | Advisories: 0`; `preflight --phase review` reads `PASS`; the
scope checkpoint passes; the handoff checkpoint's result is `handoff.json`.
The test suite on Windows reads 1318 tests, 26 skipped, 2 failures that a
control run on a clean `main` worktree also shows and that this work does not
touch. The hosted Linux lane is the record and its identifiers are added to
the verification evidence when its runs complete.

After merging live `main` (`34193ca`, seven commits of `WO-ECP-029`) into the
branch at `7d531be`, re-measured with the same evaluator: `validate .` reads
`Artifacts: 1385 | Errors: 0 | Warnings: 73 | Advisories: 0`; `preflight
--phase review` PASS; the scope and handoff checkpoints pass every predicate
with a complete change set of 33 paths; the suite reads 1317 tests, 26
skipped, the same two control-confirmed failures and no other.

## The decision now due

`DR-WO-COMPLETE`, for `WO-RSK-010` alone. The work order carries
`[delegation] class = "execution"` at the base of its pull request, so the
`delegated-executor` role applies it while the required check `validate`
reads `success` for the candidate head; otherwise the engineering owner. The
assurance decision on the record that follows stays with the human assurance
owner.
