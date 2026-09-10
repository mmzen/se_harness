```toml
artifact = "WO-PLG-010"
checkpoint = "handoff"
formal_snapshot_sha256 = "f0ff2e1e62b6ecdb5cf68ae9a66cd2b22f4e237229b594e22bf08bdc25cd719f"
rebound_at = "2026-09-10T19:19:54Z"
```

# WO-PLG-010 handoff evidence

## Delivered implementation

The `change` skill and three operation references guide artifact packages and
bounded work orders through the existing released evaluator. Current verified
context, exact decision applicability, scoped continuation and interrupted-write
readback are explicit. No evaluator command or authority store is introduced.

## Observed validation

The independent Windows report and raw traces cover CHG01–06 and CHG08–10,
including corrected repeats and zero duplicate approval/start prompts. Linux
replay completed 75 real calls with released 0.16.0. Live guard probes on both
platforms admitted only the three execution rights and refused branch-only or
unpublished-head delegation. The actual delegated start is retained separately.

Skill validation and distribution validation pass. Linux CI passes the 1,134
source tests. The Windows run and its unsandboxed retry retain an unchanged
Git-object cleanup error; expected candidate 0.18.0 versus managed 0.17.0 doctor
differences are also retained. Released doctor and graph validation pass.

## Remaining decisions and limits

See [the evidence index](README.md) for all observations and limits. Native host
activation and independent external enforcement are not qualified by these
instruction tests. CHG07 completion and ready-VREC capture are the subsequent
live delivery steps, not effects of the guard probes. This packet reports
implemented content and observed checks; it does not apply a lifecycle state,
verify a record, release software or merge a PR.
