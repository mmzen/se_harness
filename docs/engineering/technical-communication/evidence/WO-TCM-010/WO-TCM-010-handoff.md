```toml
artifact = "WO-TCM-010"
checkpoint = "handoff"
formal_snapshot_sha256 = "e949125e9a74381eb827ec4a47235b661a361e89b34824242ff7131fabd281ee"
rebound_at = "2026-09-06T13:52:59Z"
```

# WO-TCM-010 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The first example of `SPEC-TCM-006` is a true statement again: it now
describes a draft in the prescribed shape within every budget, which the
tests of `VER-TCM-006` prove, instead of "a draft written as this
specification is", which the approved specification itself does not
satisfy. An `## Amendment record` on `SPEC-TCM-006` names the finding, this
work order, and the five rules and one `Scope` sentence left as written
under `TCM-RFS-023`. No rule, identifier, coverage row, template, code or
test changed.

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | released 0.15.0 | PASS, 1,332 artifacts, 0 errors, 71 warnings, 0 advisories |
| `preflight --work-order WO-TCM-010` at start | released 0.15.0 | PASS |
| rules section of `SPEC-TCM-006` | workstation | byte-identical before and after the amendment (`git diff` touches only the `Examples` entry and the new `Amendment record`) |
| corrected example against the candidate | candidate | `test_a_reader_first_draft_within_every_budget_raises_no_advisory` passes on a draft in the prescribed shape within every budget, which is what the example now states |
| handoff check | released 0.15.0 | completed over the Git-derived change set; two runs so `handoff.json` joins the change set |

## Disclosure

The work order as drafted declared no evidence path and its `Evidence to
record` section said none was needed beyond the amendment record. The
handoff gate's `QGP-G4I-EVIDENCE` predicate requires a bound packet at the
handoff checkpoint for every work order, whatever its assurance
classification, and the check writes `handoff.json` beside it. The owner
amended the execution scope to admit
`docs/engineering/technical-communication/evidence/WO-TCM-010/` before this
packet was committed; the drafting error is recorded here.

## Material non-effects

No rule of `SPEC-TCM-006` changed. No template, validator, generator,
Explorer, test or note changed. No record is prepared: commit-bound
verification is `not_required`.
