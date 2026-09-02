```toml
artifact = "WO-RLS-020"
checkpoint = "handoff"
formal_snapshot_sha256 = "24100c9f2ba91fb982236cf0f0ba0e7444e0b53da16046544b0a4295dd7607d0"
rebound_at = "2026-09-02T09:17:58Z"
```

# WO-RLS-020 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The one clean 0.14.0 candidate commit exists on `release/0.14.0` off `main`
at `d005b98`, with the packaged bytes of `main`: this commit. The census
from `v0.13.0` is clean; no trace commit is needed. Qualification
readings, the census at the candidate, the hosted build of record and the
hosted lanes are recorded in the sections below as they complete.

## Evaluators

- Governing: released `se-harness 0.13.0` outside the checkout, `-I`,
  installed at `C:/Users/hok/se-harness-eval-0130` from the wheel file
  whose SHA-256 `1bbf3b74…` equals the distribution table of
  `RLS-SEH-022`, on this Windows checkout for every reading, the packet and
  the handoff check included.
- Candidate: this checkout, branch `release/0.14.0` off `main` at
  `d005b98`; `pyproject.toml` reads 0.14.0 (moved by `WO-HUP-014`).
- Build host: the hosted GitHub runner running the pinned linux/amd64
  producer image through Docker inside `release-qualification.yml`
  (`candidate` mode), dispatched on this branch at the bound candidate.

## Section 1: the candidate

This commit is the candidate: it retains this packet, and the branch
already carries the packet drafting, the approvals and the start. Every
commit on this branch carries the `Harness-Work-Order: WO-RLS-020` trailer
in its final block, so the census at the candidate needs no exemption.

## Section 2: readings at the candidate

Recorded in the next commit, taken at this commit.

## Section 3: census re-run at the candidate

Recorded in the next commit.

## Section 4: build of record

Recorded when the dispatched Publication Rehearsal completes at the bound
candidate.

## Section 5: hosted lanes

Recorded when the lanes complete.
