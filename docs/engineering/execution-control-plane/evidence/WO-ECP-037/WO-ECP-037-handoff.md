```toml
artifact = "WO-ECP-037"
checkpoint = "handoff"
formal_snapshot_sha256 = "885e4190ac8de39268734700ead1c99da33d157c87b975d25969cc0d3c2a7676"
rebound_at = "2026-09-09T11:50:14Z"
```

# WO-ECP-037 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`SPEC-ECP-023` carries a dated amendment record stating that `ECP-PRM-027`
is met as written since `WO-ECP-034` and that the deviation `DEC-ECP-002`
accepted against it is discharged; `DEC-ECP-002` carries a dated revisit
record stating that its trigger, the merge of wave 3 (#378), fired on
2026-09-08 and what the reading found; the domain index closes the wave 3
line with `WO-ECP-036` implemented, `VREC-ECP-040` verified, the three pull
requests merged and #378 closed. No rule text, identifier or coverage row
of the specification changed; the decision's front matter, its disposition
and its lifecycle are unchanged; no code, template, test or note changed.

## The reading the records cite

The duplication scan (`pylint --enable=duplicate-code
--min-similarity-lines=8` in a scratch environment outside the checkout)
read 3 blocks at the base of `WO-ECP-034` and 0 at its head, retained in
`docs/engineering/execution-control-plane/evidence/WO-ECP-034/WO-ECP-034-handoff.md`
and bound by the verified `VREC-ECP-038`; `WO-ECP-035`'s and `WO-ECP-036`'s
packets read 0 again at their heads. No new measurement was taken: the
records cite the retained readings, as the work order requires.

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.17.0 (`C:/Users/hok/se-harness-eval-0170`, wheel `305c7cbc…`) | 1,445 artifacts, 0 errors, 46 warnings (all `W013`, pre-existing), 0 advisories |
| `preflight --work-order WO-ECP-037 --phase start` | exact 0.17.0 | PASS |
| rules section of `SPEC-ECP-023` | workstation | byte-identical before and after (`git diff` touches only the new amendment paragraph) |
| front matter of `DEC-ECP-002` | workstation | byte-identical before and after (`git diff` touches only the new body section) |
| handoff check | exact 0.17.0 | completed over the Git-derived change set; the schema-2 result is retained beside this packet as `handoff.json` |

## Material non-effects

No rule of `SPEC-ECP-023` changed. No disposition or lifecycle event of
`DEC-ECP-002` changed. No code, template, test, note or managed byte
changed. No record is prepared: commit-bound verification is
`not_required`. The `release_build.canonical_json_bytes` alias for
`scripts/replay_release_build.py` stays a release-domain follow-up.
