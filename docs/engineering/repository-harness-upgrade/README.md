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

## Successor of 0.6.0 (draft)

- `REQ-HUP-010`: prove the exact released successor carrying `WO-ADS-001`, `WO-ADS-002`, and `WO-RSK-001`.
- `REQ-HUP-011`: adopt it through one bounded schema-3 root transaction and prove complete-graph operation, retiring the interim test exceptions.
- `SPEC-HUP-005`, `VER-HUP-005`, `WO-HUP-005`: contract, evidence, and the transaction work order. `WO-HUP-005` cannot be approved until a released record covers the three work orders and its digests are copied into the work order.
