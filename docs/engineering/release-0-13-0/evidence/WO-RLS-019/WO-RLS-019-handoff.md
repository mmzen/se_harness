```toml
artifact = "WO-RLS-019"
checkpoint = "handoff"
formal_snapshot_sha256 = "e4eddb3abdab93d202986908f4ab5f08667a99b799cb00139cd9dccf02c411fa"
rebound_at = "2026-09-02T06:46:22Z"
```

# WO-RLS-019 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The one clean 0.13.0 candidate commit exists on `release/0.13.0` off `main`
at `75d1902`, with the packaged bytes of `main`: this commit. No trace
commit is needed; the census from `v0.12.0` is clean. Qualification
readings, the census at the candidate, the hosted build of record and the
hosted lanes are recorded in the sections below as they complete.

## Evaluators

- Governing: released `se-harness 0.12.0` outside the checkout, `-I`,
  installed at `C:/Users/hok/se-harness-eval-0120` from the wheel file
  whose SHA-256 `639edbee…` equals the distribution table of
  `RLS-SEH-021`, on this Windows checkout for every reading, the packet and
  the handoff check included.
- Candidate: this checkout, branch `release/0.13.0` off `main` at
  `75d1902`; `pyproject.toml` reads 0.13.0 (moved by `WO-HUP-013`).
- Build host: the hosted GitHub runner running the pinned linux/amd64
  producer image through Docker inside `release-qualification.yml`
  (`candidate` mode), because this workstation has no Docker engine.

## Section 1: the candidate

This commit is the candidate: it retains this packet and the release-note
line, and the branch already carries the packet drafting, the approvals
and the start. Every commit on this branch carries the
`Harness-Work-Order: WO-RLS-019` trailer in its final block, so the census
at the candidate needs no exemption.

## Section 2: readings at the candidate

Recorded in the next commit, taken at this commit.

## Section 3: census re-run at the candidate

Recorded in the next commit.

## Section 4: build of record

Recorded when the hosted Publication Rehearsal completes at the bound
candidate.

## Section 5: hosted lanes

Recorded when the lanes complete at the bound candidate head.
