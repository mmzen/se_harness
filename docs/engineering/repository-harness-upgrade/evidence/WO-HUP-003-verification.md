# WO-HUP-003 implementation verification evidence

Date: 2026-08-23

## Result

The exact eight-path post-adoption compatibility implementation is locally
complete. The ten formerly failing tests pass, all seven affected modules pass,
and the complete source suite passes. Released 0.6.0 doctor, graph validation,
review preflight, inspection, dashboard, distribution validation, and no-op
upgrade also pass. The final complete-suite replay with this evidence path in
the retired-context inventory also passes, so every authorized local check is
complete.

This work changes no product runtime, canonical package template, managed root,
lock, release record, publisher, external service, or Git history.

## Authority and scope

At `2026-08-23T08:06:31Z`, the accountable repository owner approved
`REQ-HUP-007`, `SPEC-HUP-003`, `VER-HUP-003`, `WO-HUP-003`, and the exact
eight-path compatibility plan. Released 0.6.0 start preflight then passed and
the workflow engine atomically moved only `WO-HUP-003` to `in_progress`.

The implementation changed exactly:

1. `AGENTS.md` owner-controlled region.
2. `tests/test_artifact_catalog.py`.
3. `tests/test_context_routing_retirement.py`.
4. `tests/test_dashboard_webui.py`.
5. `tests/test_instruction_architecture.py`.
6. `tests/test_predecessor_assessment_contract.py`.
7. `tests/test_revision_provenance.py`.
8. `tests/test_validation_taxonomy.py`.

The HUP-003 definition packet, domain index, this evidence, and accountable
lifecycle metadata are the only additional governance changes.

## Compatibility corrections

- Owner guidance now identifies released 0.6.0, `WORKFLOW.json`, and
  `QUALITY_GATES.json`, and explains that role separation depends on origins,
  paths, the lock, and authority rather than mandatory byte skew.
- Adopted policy, router, topology threshold, and taxonomy tests require exact
  equality with the packaged released 0.6.0 root while retaining independent
  source-path and runtime-origin checks.
- The retired-context inventory removes the withdrawn managed-router mention
  and records only the exact HUP evidence and contracts that necessarily name
  the preserved owner path.
- The installed engineering workflow is compared with the rendered packaged
  0.6.0 workflow. The historical predecessor-assessment workflow remains
  unchanged, read-only, credential-free, and pinned to its exact 0.5.0 wheel.
- Revision-provenance temporary fixtures now write canonical LF-only evaluator
  evidence with SHA-256
  `885f4c9433c34afe2b397d175723165356c11077f8f4d4c3ba870d934c933991`
  and a matching schema-3 lock. Production validator behavior and legacy
  exemptions are unchanged.

## Test results

| Check | Result |
| --- | --- |
| Python syntax for all seven changed modules | PASS |
| Exact formerly failing set | PASS: 10 tests |
| Seven affected modules | PASS: 110 tests, 2 skips |
| Complete clean source suite | PASS: 452 tests, 7 skips, zero failures or errors, 247.395 seconds |
| Final evidence-aware complete suite | PASS: 452 tests, 7 skips, zero failures or errors, 250.863 seconds |
| Scale cases | PASS at 100, 500, and 1,000 artifacts |

The first focused attempt exposed two fixture facts and changed no scope: the
schema-3 lock contains 30 managed-mode entries, and canonical evaluator JSON
must be written as LF bytes on Windows. Both were corrected inside the already
authorized test modules before the passing reruns.

## Owner and immutable-root checks

| Item | Result |
| --- | --- |
| `AGENTS.md` owner region | 5,236 UTF-8 LF bytes, below the 6,000-byte bound |
| `AGENTS.md` owner-region SHA-256 | `cd2357d390b02176f3eccbe45c797437401c0e6f13a329feba48033fb2f5c393` |
| `AGENTS.md` managed fragment | unchanged; doctor and lock digest pass |
| Schema-3 lock SHA-256 | `abcb1fe70b0eab96b106378bc1549b11e65cf5fe23d9c4cafccfdd28a3bf3f79`, unchanged from HUP-002 |
| `docs/engineering/REPOSITORY_CONTEXT.md` SHA-256 | `4cf02b35174e95b25b785ae6b93175b86197e473173e9fb12eab92268b468d94`, unchanged and absent from the lock |
| HUP-002 transaction evidence SHA-256 | `83398eb76d73a96a0aef2bc40e1d9045a8e14cf5bf74b89afe2ecbf39350c284`, unchanged |
| Product/runtime/template forbidden surface | PASS: no changed path |
| `git diff --check` | PASS; only host line-ending conversion notices |
| Combined HUP-002/HUP-003 scope audit | PASS: exactly 43 changed or untracked paths; none missing or unexpected |
| Evidence host/secret scan | PASS |

## Released-governor checks

| Check | Result |
| --- | --- |
| Released 0.6.0 doctor | PASS; every distribution and managed-integrity check passes; 21 inherited W013 advisories |
| Complete graph validation | PASS: 685 artifacts; structure E0/W0, governance E0/W0, policy E0/W0, maintenance E0/W50 |
| HUP-003 review preflight | PASS at `in_progress`, no diagnostics, 14-file reading manifest |
| Repository inspection | PASS observation: 685 artifacts, 2,489 relations, 135 findings, no decisions or definitions pending, two active HUP work orders |
| Harness Explorer | PASS: 685 artifacts, 2,489 relations, zero errors, 60 warnings; manifest `aee0f9b5f3e34871ccd3c29ed4be7f594d032673bb8a979fce5fe4902b6e96af` |
| Released upgrade replay | PASS: 36 managed paths unchanged |
| Release-distribution validation | PASS: one distribution-bearing record |

The 50 validator maintenance warnings and 21 doctor placement advisories are
the same inherited compatibility observations present before HUP-003; no new
warning or error was introduced.

## Completion checks and non-effects

The evidence-aware retired-context test, complete suite, exact 43-path union,
evidence scan, forbidden-product-surface audit, released validation, and review
preflight all pass. The engineering owner subsequently transitioned
`WO-HUP-003` to `implemented`.

No candidate commit, VREC preparation or transition, push, pull request, merge,
tag, GitHub Release, PyPI publication, Pages deployment, credential use,
protected-environment decision, issue mutation, force push, or history rewrite
was performed.
