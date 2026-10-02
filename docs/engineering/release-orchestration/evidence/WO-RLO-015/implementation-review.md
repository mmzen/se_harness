# Complete-release implementation review

Implementation source: `7cf08306f0bf87c3f14ec8a2a328de91fa0a67af`.
Base: `745884fd6c6b7dd0c7185b7427efcf9bd33c7e0d`.
Scope: WO-RLO-014, WO-RLO-015 and WO-RLO-016 under VER-RLO-011.
Prepared by Codex. Human implementation verification has not been supplied.

## Result for the owner

An explicitly selected complete-release route prepares and verifies all candidate
deliverables before one final release approval. The operator reuses that decision
for the named publication, integration and recovery actions. The existing publisher
can promote the exact staged marketplace commit and moving markers. Required public
tests and retained receipts determine completion; they do not become extra approvals.

The route is prospective. This implementation does not publish a release, apply the
provider configuration, adopt an evaluator or claim any native host test passed.
The existing 0.21.0 evaluator continues to govern this work.

## Verification mapping

| Case | Evidence and observed result |
| --- | --- |
| ONE01 | Workflow procedure/instruction tests pass. Release and external rights stay distinct and reuse a matching explicitly selected plan. |
| ONE02 | CompleteReleaseTests, delivery-plan tests and real Git resolver fixture pass. Legacy inputs retain their original route; changed plans, source, destination, action or human binding refuse. |
| ONE03 | Staging/legacy package tests pass on Windows and Linux. Candidate source tree, recipe, manifest and wheel are checked without a released RLS. Both native formats remain unchanged. |
| ONE04 | Inert Git marketplace fixtures pass exact-tree and public-wheel comparisons; later governance changes do not rebuild staged packages. Mismatches stop before writes. |
| ONE05 | Existing publisher/qualification/maintenance/Pages tests and all five delivery-surface fixtures pass. The existing Publication Rehearsal now includes these credential-free delivery tests. Hosted PR checks are pending at this review snapshot. |
| ONE06 | Interrupted marketplace and marker tests preserve completed effects. Unknown HTTP responses are not treated as absence. Unexpected refs stop; matching replay does not duplicate writes. |
| ONE07 | Workflow boundary tests pass. Candidate code stays outside credential jobs. The WO-RLO-016 directory contains read-only control snapshots and a reviewer-only proposal/recovery. Live PyPI account-side binding remains unverified. |
| ONE08 | Legacy plan/record tests and incomplete observation fixtures pass. Marker readiness is distinct from full completion. The source guide states the separate release/adoption/activation prerequisites. |

`implementation-checks.zip` and `check-index.json` retain raw results, commands,
exits and digests, including failures. Linux tests at the source commit above pass
the focused suite, package staging and full suite. Windows full source tests pass
(1,254 tests, 22 skips), with the subsequent provider-observation correction covered
by 112 focused tests. Final capture will run tests again at its exact committed
candidate. Platform skips remain visible in raw results.

## Review findings and resolutions

- An early staging fixture omitted the committed build-toolchain lock. The builder
  correctly refused it; the fixture now supplies both declared recipe inputs.
- The original test helper trimmed whitespace, defeating the changed-plan-digest
  test. The corrected fixture writes exact bytes and confirms refusal.
- The workflow text test omitted job IDs with underscores. Its parser now includes
  valid IDs, so the existing dependency check covers all jobs.
- Reused the existing JSON parser instead of duplicating the CI parsing helper.
- Kept the README within its 650-word budget by linking the maintainer procedure.
- The first Linux full run used a bundle path as `origin`, which failed the existing
  dashboard source-URL assertion. The disposable clone now restores the real origin
  URL without fetching or pushing; the repeated full suite passes.
- Existing GitHub discovery treated every failed request as absence. The changed
  path now distinguishes explicit 404 from authentication, rate-limit and provider
  errors before any release/tag write. Tests cover those refusal cases.

## Simplicity and remaining limits

No service, new formal artifact type, new lifecycle state or credential store was
added. The new staging path, versioned existing plan, exact-ref reconciliation and
diff checks are needed to remove the actual dependency on post-publication assurance.
Combining prompt wording alone would leave that dependency and the provider reviewer.
The code reuses the existing publisher, JSON helpers, maintenance API adapter,
package builder and completion checker.

One-time activation still needs verified/integrated implementation, a released and
adopted evaluator/plugin, the exact provider change decision and current PyPI binding
readback. Public host tests for a future release still need working host credentials.
No unsupported host result or future credential readiness is inferred here.

GitHub latest-release updates have no compare-and-swap endpoint. The workflow
serializes its complete-delivery writers and checks/readbacks the expected value;
other writers must not move markers concurrently. `last` uses an exact Git lease.
Historical grants and published bytes retain their original meaning.
