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

- `REQ-HUP-014`, `REQ-HUP-015`, `SPEC-HUP-007`, `ARCH-HUP-005` (no significant decision) and `VER-HUP-007` are drafted for the adoption of exact public 0.7.1 the simple way, deriving from `CAP-HUP-002`; `WO-HUP-007` is the successor to the rejected `WO-HUP-006` and is drafted (2026-08-27).

- `REQ-HUP-016`, `REQ-HUP-017`, `SPEC-HUP-008`, `ARCH-HUP-006` (no significant decision) and `VER-HUP-008` are drafted for the adoption of exact public 0.8.0 (`RLS-SEH-017`, wheel `e08aab8a…`, payload `ea75cc53…`) as the standard root the simple way, from the 0.7.1 lock `6739fef0…`, deriving from `CAP-HUP-002`; `WO-HUP-008` is drafted (2026-08-28). Rehearsed on a throwaway export of `main` at `2628627`: 9 managed updates, replay 61 unchanged, 0.8.0 validate 0 errors and doctor 0 FAIL; the root copies become byte-identical to the candidate templates, the candidate moves to `0.9.0` (`PRE008` otherwise), and nine test modules carry root or candidate pins. Approval, start, the transaction, completion, verification and merge are separate acts.

- `REQ-HUP-018`, `REQ-HUP-019`, `SPEC-HUP-009`, `ARCH-HUP-007` (no significant decision) and `VER-HUP-009` are drafted for the adoption of exact public 0.9.0 (`RLS-SEH-018`, wheel `c4b56175…`, payload `e74ad2ae…`) as the standard root the simple way, from the 0.8.0 lock `174db6dc…`, deriving from `CAP-HUP-002`; `WO-HUP-009` is drafted (2026-08-29). Rehearsed on a throwaway clone of `main` at `7291602`: 5 managed updates, replay 61 unchanged, 0.9.0 validate 0 errors, doctor 0 FAIL and released-root 143/143; the candidate moves to `0.10.0` (`PRE008` otherwise), and the full suite on the moved root differs from the same-commit control by exactly four tests, all resolved by owner content, the candidate version and one test literal. Approval, start, the transaction, completion, verification and merge are separate acts.

- `REQ-HUP-020`, `REQ-HUP-021`, `SPEC-HUP-010`, `ARCH-HUP-008` (no significant decision) and `VER-HUP-010` are drafted for the adoption of exact public 0.10.0 (`RLS-SEH-019`, wheel `e2f80772…`, payload `723c98ec…`) as the standard root the simple way, from the 0.9.0 lock `fb61f1fe…`, deriving from `CAP-HUP-002`; `WO-HUP-010` is drafted (2026-08-29). Rehearsed on a throwaway clone of `main` at `47f67de`: 6 managed updates, replay 61 unchanged, 0.10.0 validate 0 errors, doctor 0 FAIL and released-root 143/143; the candidate moves to `0.11.0` (`PRE008` otherwise), and the full suite on the moved root differs from the same-commit control by exactly three tests, all resolved by owner content, the candidate version and one test literal. Approval, start, the transaction, completion, verification and merge are separate acts.
- `REQ-HUP-022`, `REQ-HUP-023`, `SPEC-HUP-011`, `ARCH-HUP-009` (no significant decision) and `VER-HUP-011` are drafted for the adoption of exact public 0.11.0 (`RLS-SEH-020`, wheel `ba26ab7b…`, payload `71b4b5b6…`) as the standard root the simple way, from the 0.10.0 lock `aeb73cc7…`, deriving from `CAP-HUP-002`; `WO-HUP-011` is drafted (2026-08-29). Rehearsed on a throwaway clone of `main` at `896f8fa`: plan 46 files, 9 `update`, 37 unchanged; the fifteen retired skill files stay on disk unmanaged (issue #271) and the work order removes them; the scope names no `verification-records/` directory because the 0.11.0 gate admits the work order's own record by construction.

`REQ-HUP-024`, `SPEC-HUP-012`, `VER-HUP-012` and `WO-HUP-012` are drafted and approved on 2026-08-30 for [issue #285](https://github.com/mmzen/se_harness/issues/285) item #285a, on the owner's floor decision of the same day: locks older than schema 3 are not read, taken as the hard floor by the owner's selection. Lock validation accepts schema 3 only and refuses a schema-1 or schema-2 lock before any write with one diagnostic naming the route — remove the stale lock and re-adopt; the installer writes schema 3 only and its schema-1 preservation branch is gone; the legacy digest machinery (`LEGACY_CANONICAL_LOCK_SCHEMA`, the schema-1 raw and fragment digests, the newline-variant recognition, the `exact` and `legacy-canonical` labels) is deleted from the integrity, installer, doctor and hash-bound components; the mutation guard's schema condition is deleted and `MG002` is retired and reserved; `scripts/validate_governor_transition.py` accepts schema 3 only. `REQ-PMI-004`, `SPEC-PMI-001` and `ADR-PMI-001` carry dated amendment records for the 0.2.x-era commitments the floor supersedes. This closes [issue #224](https://github.com/mmzen/se_harness/issues/224), whose keep-schema-2-reading proposal the floor decision overrode.

- `REQ-HUP-027`, `REQ-HUP-028`, `SPEC-HUP-014`, `ARCH-HUP-011` (no significant decision) and `VER-HUP-014` are drafted for the adoption of exact public 0.13.0 (`RLS-SEH-022`, wheel `1bbf3b74…`, payload `9b4cdb5f…`) as the standard root the simple way, from the 0.12.0 lock `4d8f9d37…`, deriving from `CAP-HUP-002`; `WO-HUP-014` is approved, started and executed on 2026-09-02: the root is exact public 0.13.0 and the candidate 0.14.0. Rehearsed on a throwaway clone of `main` at `09aa69f`: 5 managed updates (the two Explorer scripts among them), replay 46 unchanged, 0.13.0 validate 0 errors / 67 warnings / 0 advisories, doctor 0 FAIL, released-root 113/113, the designed Explorer generated identically twice; the candidate moves to `0.14.0` (`PRE008` otherwise). Approval, start, the transaction, completion, verification and merge are separate acts.
