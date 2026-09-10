```toml
artifact = "WO-DST-027"
checkpoint = "handoff"
formal_snapshot_sha256 = "17281e268d3afb253972695e4a780741c8159c62176a9f2341447d4ab6b24545"
rebound_at = "2026-09-10T12:24:04Z"
```

# WO-DST-027 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`TRC-008` of the standard `TRACEABILITY.md` says `ARCH.constrains` is
retired, that a validator refuses every `constrains` relation with `E016`
whatever the architecture's status, that it classifies no historical
relation and reports no migration, and that `ARCH.addresses` and
`ARCH.conforms_to` are the only form; its last sentence, that installation
and upgrade never rewrite repository-owned artifacts, is unchanged, and no
other line of the file moved. The "Completion report format" heading of the
standard `WORK_ORDER.template.md` carries one guidance paragraph: the
completion decision follows from the front matter, the engineering owner's
by default, the `delegated-executor`'s under `[delegation] class =
"execution"` while the required pull-request check is `success`.
`docs/notes/harness-uml-model.md` says the relation is retired and refused
instead of "older completed artifacts may still carry" it. The parity test
in `tests/test_artifact_catalog.py` declares both changes as candidate
exceptions against the 0.17.0 root and reaches its existing equality
branches once a root carries them; `tests/test_managed_template_texts.py`
pins the rule, the guidance, the note and, as scenario B, a work order
drafted from the candidate template. No root managed byte, the lock or any
existing work order changed. Rules `DST-TPL-001` to `DST-TPL-008` of
`SPEC-DST-028` are mapped to evidence in `WO-DST-027-verification.md`;
`DST-TPL-009` is carried to the root-adoption work order of the carrying
release.

## Evaluators

- Governing: released `se-harness 0.17.0` installed from the wheel file
  outside the checkout (`C:/Users/hok/se-harness-eval-0170`), run `-I`, for
  `validate`, `doctor`, `preflight`, `evidence` and the handoff check.
- Candidate: the worktree `C:/Users/hok/repos/se_harness_dst027`, branch
  `wo/dst-027-managed-templates`, off `main` at `f36c8bf1` (the merge of
  #437, this work order's packet). The start event was taken by the
  `delegated-executor` role at `18129f2a` under the `validate` check that
  was `success` for the base.

## Readings

- Released 0.17.0 `validate`: PASS, 1,485 artifacts, 0 errors, 46 warnings
  (all `W013`), 0 advisories.
- Released 0.17.0 `doctor`: 99 `PASS`, no `FAIL`; every managed path
  matches its distribution.
- Released 0.17.0 `preflight --work-order WO-DST-027`: PASS at phase
  `start`, the work order `in_progress`.
- `git diff origin/main --stat` over `docs/engineering/TRACEABILITY.md`,
  `docs/engineering/templates/`, `.engineering-harness.lock`,
  `.engineering-harness.toml` and `ENGINEERING_HARNESS.md`: empty; every
  root managed byte is identical to `main`.
- `python -m unittest tests.test_managed_template_texts
  tests.test_artifact_catalog`: 11 tests OK before scenario B was added,
  then 7 tests OK in the new module with it, on Windows 11 with
  Python 3.13. The local full suite is the control recorded in the
  completion reason; the hosted Linux lane is the record.
- Managed lane at `18129f2a` (the start commit): blocked on
  `QGP-G4I-EVIDENCE` only, before this packet existed; the 16 other lanes
  `success`.

## Disclosures

1. Scenario B could not be run with either evaluator as a consumer would run
   it: the candidate's `create-artifact` from the source tree is refused by
   the mutation guard (`MG005`, `RID003`, `RID004`), and the released 0.17.0
   evaluator refuses a target the candidate initialized (`RID002`, `RID021`).
   It runs instead as `DraftedWorkOrderTests` in the new test module, through
   the suite's own `patch_mutation_authority` and `invoke` helpers, which is
   how the suite exercises every candidate write; `init` from the candidate
   into a scratch directory did succeed and installed the template with the
   guidance.
2. The UML note's third sentence, "Historical records are not rewritten to
   modernize their words", now reads "not otherwise rewritten": the fifteen
   `constrains` architectures were rewritten by `WO-AUT-005`, so the
   unqualified sentence was no longer true beside the new one.
3. The parity test's two new declared exceptions match the 0.17.0 root by
   construction; whether they reach the equality branch is first observed at
   the root adoption of the carrying release (`DST-TPL-009`).

## Changed paths

- `templates/repository/standard/docs/engineering/TRACEABILITY.md`
- `templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md`
- `docs/notes/harness-uml-model.md`
- `tests/test_artifact_catalog.py`
- `tests/test_managed_template_texts.py` (new)
- `docs/engineering/harness-distribution/README.md`
- `docs/engineering/harness-distribution/evidence/WO-DST-027-verification.md`
- `docs/engineering/harness-distribution/evidence/WO-DST-027/` (this packet,
  `handoff.json`)
- `docs/engineering/harness-distribution/work-orders/WO-DST-027.md`
  (lifecycle events only)
