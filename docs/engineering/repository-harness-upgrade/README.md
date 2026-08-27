# Repository harness upgrade

This domain governs separately authorized standard-root evaluator upgrades and
their bounded post-adoption qualification.

- `INT-HUP-001` through `VER-HUP-001` are approved. `WO-HUP-001` is
  `implemented`, and verified `VREC-HUP-001` retains its commit-bound evidence.
  That transaction moved the root from released bootstrap `0.5.0a1` to exact
  public `0.5.0`.
- `INT-HUP-002` through `VER-HUP-002` are approved, and `WO-HUP-002` is
  `implemented`. Candidate `ea7b837438a0fb32b8f6b51c630e98b9706ea039`
  adopts exact public `0.6.0`; `VREC-HUP-003` is a later `ready` proposal bound
  to that candidate.
- Hosted qualification of that candidate exposed two remaining integration
  gaps: one raw-byte inequality assertion is LF/CRLF-dependent, and the
  repository-owned predecessor workflow still evaluates the current checkout
  as a 0.5.0 root. Managed validation itself passes.
- `INT-HUP-003`, `CAP-HUP-003`, `REQ-HUP-008`, `REQ-HUP-009`, `SPEC-HUP-004`,
  `ARCH-HUP-003`, `ADR-HUP-001`, and `VER-HUP-004` are approved.
  `WO-HUP-004` is `in_progress`. Its implementation replaces the
  version-specific predecessor check with a version-independent governor-
  transition assessment and replaces the LF/CRLF-sensitive evaluator-role
  assertion with path, lock, and candidate-semantics checks. The HUP-003
  identifiers are intentionally not reused because they are reserved on
  another fetched repository ref.
- Local qualification passes under Python 3.11 and the default runtime, exact
  public 0.6.0 validates the complete root, and real-history replay resolves
  the 0.5.0-to-0.6.0 transaction without a compatibility view. Hosted evidence,
  work-order completion, commit, push, and disposition of `VREC-HUP-003` remain
  separate governed actions. No managed root, product, release, publication,
  deployment, maintenance, or external policy was changed.

- `INT-HUP-004`, `REQ-HUP-012`, `REQ-HUP-013`, `SPEC-HUP-006`, `ARCH-HUP-004` (no significant decision) and `VER-HUP-006` are drafted, deriving from the existing `CAP-HUP-002`. `WO-HUP-006` is drafted to adopt exact public `0.7.0` (`RLS-SEH-015`, wheel `e8f4fdc9…`, payload `26c11ec5…`) as the standard root, from the 0.6.0 lock `978cebb7…`. Measured on 2026-08-27 over `main` at `7284743`: the 0.7.0 plan reads 61 files, 18 unchanged, 43 add or update, no customization. Approval, start, the transaction, completion, verification and merge are separate acts. A rehearsal of the transaction in a throwaway worktree (apply, no-op replay, 0.7.0 doctor and validate clean) showed eleven root-assumption test pins in six modules and one coupling: with the root and the candidate both at `0.7.0`, `predecessor_facts derive` raises `PRE008`, so the work order also moves the candidate to development version `0.8.0` with its scenario, on the owner's 2026-08-27 decision.

`WO-HUP-006` is `rejected` (2026-08-27). The transaction ran on the branch of pull request #196 and was abandoned there: 0.7.0's managed workflow installs its evaluator from the index and then requires a PEP 610 archive digest (`RID022`), so the managed lane cannot pass, and the owner directed that the wheel-digest (`MG004`) and work-order-packet (`MG007`) requirements on `harnessctl upgrade --apply` be removed rather than worked around. The root stays at exact public 0.6.0 until a release carries the simplified upgrade.
