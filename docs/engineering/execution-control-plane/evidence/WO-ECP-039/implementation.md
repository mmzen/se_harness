# WO-ECP-039 implementation and acceptance

The existing helper accepts schema-3 repository ownership and schema-4 plugin
ownership, checks that an upgrade preserves that selection, and retains the
six evaluator handover steps, version/payload assertions and result format.
No workflow, dependency, product code or root configuration changed.

## Observed results

- Final implementation: `2d79e0108084dfcd15efa16187e555a99ed70689`.
- Focused module: 34 tests passed. Review then added one positive combination
  covering retained earlier plugin metadata; the full suite below includes it.
- Full source suite: 1,081 tests passed, 15 skips, after the final implementation.
- The first full run had one Git-timeout failure; its output is retained with
  the passing single-test recheck and subsequent passing full-suite retry.
- Two real Windows 0.18.0-to-0.19.0 replays passed all six steps, preserved plugin
  ownership, and produced `62882e246417e780120ddf5c706e0c5a5d41d6425270707e9276cfac92f756f3` as the same lock digest.
- The initial path-length failure and first short-path retry's Git timeout
  happened before evaluator operations. Both are retained. The successful runs
  used a short temporary directory after the first suite finished, without code or timeout changes.
- Governing 0.18.0 doctor: 64 checks passed. Graph: zero errors, 49 existing
  warnings. Scope and review preflight passed. Distribution validation checked
  15 records; CLI help passed.
- Candidate doctor retains its three known 0.19.0/source versus 0.18.0/governor
  differences. This does not change the passing released integrity reading.

## Review and evidence reuse

The [implementation review](implementation-review.json) explains the small
classifier and regression coverage. [Results](verification-results.json) retain
commands, runtime and wheel identity, actual output, failed and successful
replays, and all 29 unchanged earlier evidence hashes. The CI wheel is reused
only after checking its SHA-256 and product-source equality with its build
commit. Earlier native observations retain their original host/version limits.
VREC-PLG-022, VREC-HUP-019 and their bound evidence remain unchanged.

The final candidate adds only completion/index/evidence facts to this tested
implementation. Final input comparisons and the exact CI planner/assessor
commands will be retained with VREC-ECP-041. Hosted CI remains pending later
delivery; no local result claims a new Linux/Windows hosted pass.
