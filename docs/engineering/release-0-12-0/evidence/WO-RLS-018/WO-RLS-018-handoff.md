```toml
artifact = "WO-RLS-018"
checkpoint = "handoff"
formal_snapshot_sha256 = "fcd8bba6843c53d979abe5a09bb53e0cfd86828dc78249220014a73b14f2f9b5"
rebound_at = "2026-08-31T11:26:12Z"
```

# WO-RLS-018 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The one clean 0.12.0 candidate commit exists on `release/0.12.0` off `main`
at `2761f89`, with the packaged bytes of `main`: this commit. The five
trace commits of `REL-SEH-023`'s trace repair precede it. Qualification
readings, the census at the candidate, the recipe-bound build of record
and the hosted lanes are recorded in the sections below as they complete.

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`,
  installed from the digest-verified wheel (`ba26ab7b…`), on this Windows
  checkout for every reading, the packet and the handoff check included.
- Candidate: this checkout, branch `release/0.12.0` off `main` at
  `2761f89`; `pyproject.toml` reads 0.12.0 (moved by `WO-HUP-011`).

## Section 1: the candidate

This commit is the candidate: it retains this packet's skeleton and the
branch already carries the packet drafting, the approvals, the start and
the five empty trace commits. Every subsequent branch commit carries the
`Harness-Work-Order: WO-RLS-018` trailer in its final block; the three
governance commits before this one (draft, approve, start) predate that
convention on this branch and are exempted in the recorded census
alongside the contract's fourteen.

## Section 2: readings

Recorded below as they complete.
