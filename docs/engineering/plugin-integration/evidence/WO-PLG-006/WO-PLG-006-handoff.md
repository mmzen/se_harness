```toml
artifact = "WO-PLG-006"
checkpoint = "handoff"
formal_snapshot_sha256 = "d486c36a30fdc1eeec9d0169de12a6a270105cdb20f874ce5f788496fb30742e"
rebound_at = "2026-09-11T19:45:48Z"
```

# WO-PLG-006 handoff evidence

This checkpoint records an in-progress draft implementation for review. It does
not assert completion, verification, qualification, release or merge.

At candidate `4549f19f562841f461961a21a83c02bd194a9d36`, the native adapter and
ten focused tests are retained. Earlier attempts and their limitations are
described in [README.md](README.md). The fresh `acceptance-04` collection has
observed C01-C08 and is still collecting C09-C12; final independent assessment
and retained final case verdicts remain pending. No unrun case counts as passing.

PR #456's initial required `validate` check failed because this checkpoint packet
was absent. Scope and preflight passed. The initial check metadata/log and this
correction are retained in [governance/handoff-correction/](governance/handoff-correction/).
The released 0.17.0 evaluator generated this packet for the current formal
snapshot. The work order remains `in_progress`; no lifecycle action occurred.

The later evidence update completes C01-C12 collection and sixteen focused
tests. C10/C11 have observed effects without required refusal and remain failed
and unqualified; C12 passes only the rejection obligation. The current matrix,
exact package/blob mapping and qualification limit are in README.md and its
linked canonical case records. This supersedes the collection-pending status
above while preserving the original draft correction history. Engineering
disposition, assurance and completion remain pending.
