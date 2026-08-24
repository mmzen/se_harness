# WO-IPK-001 implementation verification evidence

Date: 2026-08-24

Authority: non-authoritative implementation and local-qualification evidence.
This file does not approve implementation, verify a candidate, authorize a
workflow run, retain an external artifact, release, publish, select a governing
evaluator, or authorize repository integration.

Work order: `WO-IPK-001`, currently `in_progress`. Commit-bound verification is
`required`. The exact package bytes and Linux/Windows installation evidence can
therefore be completed only after a later exact candidate commit and separately
authorized hosted workflow run.

## Start authority and evaluator boundary

- Base commit observation:
  `1cdc75259da8156e93ad8c32110ee196296b8cea`.
- Exact released evaluator: `se-harness 0.6.0`, invoked through the isolated
  external environment at `../se-harness-eval` rather than candidate source.
- Released wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Released payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.
- Exact evaluator runtime identity passed with isolated Python, disabled user
  site, absent inherited `PYTHONPATH`, exact module/template/entry-point roots,
  and matching wheel and installed-payload digests.
- Exact evaluator `doctor` passed managed-root integrity before work started.
- Exact evaluator start preflight passed with 18 required reading-manifest
  paths and commit-bound verification `required`.
- The engineering owner then authorized and applied only
  `WO-IPK-001: approved -> in_progress` at `2026-08-24T11:17:45Z`.

## Implemented result

- Added `.github/scripts/build_integration_package.py`, one standard-library
  script with `build`, `verify`, and `install-test` interfaces.
- The build interface resolves one exact 40- or 64-character commit, obtains a
  structured `git archive`, rejects unsafe or ambiguous members, and creates
  two independent disposable exports outside the checkout.
- It requires matching committed versions, derives
  `<base>+main.g<sha12>` or `<base>+pr<number>.g<sha12>`, changes only
  `pyproject.toml` and `se_harness/__init__.py` in both exports, and proves the
  two changed-path sets and overlay hashes are identical.
- It requires exact installed versions of `build==1.2.2.post1`,
  `setuptools==75.8.0`, and `wheel==0.45.1`, fixes reproducibility environment
  inputs, builds twice with `python -m build --wheel --no-isolation`, and
  requires identical wheel names and bytes.
- It validates the pure-Python wheel without extraction and emits exactly one
  wheel, canonical `se-harness-integration-package-v1` manifest, and canonical
  `SHA256SUMS` through an exclusive temporary-to-final directory transaction.
- The independent verifier rejects duplicate/unknown/missing JSON fields,
  noncanonical bytes, invalid identities, links, unsafe paths, unexpected
  inventory, malformed or oversized members, metadata/version/tag drift, and
  checksum mismatch.
- Installed verification uses a fresh virtual environment, installs only the
  exact wheel with `--no-index --no-deps`, leaves the checkout, checks imported,
  distribution, and entry-point versions, and exercises init, doctor, validate,
  managed upgrade, doctor, and validate on a disposable repository. Pre/post
  tracked/untracked file and Git-reference manifests must agree.
- Extended candidate evidence with an eligible downstream build/staging job,
  a fail-independent Linux/Windows verification matrix, and a final retention
  job that runs only after both platforms pass.
- New workflow actions use exact commit pins, least-privilege inherited
  `contents: read`, bounded timeouts, one-day staging, 14-day `main` retention,
  and 3-day pull-request retention. Existing candidate gates remain unchanged.
- Added operator documentation for run selection, `gh run download`, inventory
  and checksum verification, manifest inspection, isolated file installation,
  disposable testing, cleanup, expiration, and separately authorized reruns.
- Added explicit public and contributor links and preserved the distinction
  between integration packages, releases, and governing evaluators.

## Implementation identities

| Path | SHA-256 at local handoff preparation |
| --- | --- |
| `.github/scripts/build_integration_package.py` | `6e69affd6f3e685003d53426211192082de39a1bd9c57c0364bb9355dfa611dd` |
| `.github/workflows/candidate-evidence.yml` | `1d719a4d6b16b3c3395d25569a7680dc0415055566500704f7380c2e09a6e091` |
| `tests/fixtures/integration_package/canonical_vectors.json` | `5898e9b28d4e1955e036f2442265680e5f652dae2122e60f6d496d445c5ef281` |
| `tests/test_integration_package.py` | `bc3ebbf22a3927c6c869725abb5d907b2bbc3022a410d40516ca3a7990bfd3e9` |

These are working-tree implementation identities, not commit-bound candidate
identities. They must be regenerated if any named byte changes.

## Local commands and results

| Check | Result |
| --- | --- |
| Python AST parse of script and focused tests | Passed |
| script top-level help | Passed; exactly `build`, `verify`, and `install-test` |
| `python -B -m unittest tests.test_integration_package -v` | Passed: 14 tests, including subprocess CLI verification |
| `python -B -m unittest tests.test_standard_repository_lifecycle -v` | Passed: 21 tests |
| `python -B -m unittest tests.test_release_build -v` | Passed: 5 tests |
| complete `python -B -m unittest discover -s tests -p "test_*.py"` | Ran 601 tests in 348.980 seconds; 11 platform skips; 19 errors and 4 failures, all confined to the pre-existing hash-bound-integrity module and explained below |
| hash-bound module with process-local Git safe-directory configuration | 67 effective passes, 1 expected host-materialization failure, 1 symlink-capability skip |
| candidate-source formal validation | Passed: 759 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| exact released 0.6.0 formal validation | Passed: 759 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| exact released 0.6.0 review preflight for `WO-IPK-001` | Passed; work order `in_progress`, commit-bound verification required, no diagnostics |
| independent YAML parse of `candidate-evidence.yml` | Passed; all seven expected job IDs present |
| release/publication workflow integration-reference scan | Passed; no integration artifact name or schema appears in either workflow |
| committed `pyproject.toml` and `se_harness/__init__.py` diff check | Passed; neither version file changed |
| `git diff --check` on the declared implementation paths | Passed; line-ending materialization warnings only |

### Full-suite host deviations

The first full run's 19 errors and three of its four failures came from child
Git commands refusing this Codex sandbox identity as a dubious owner. Rerunning
only that module with `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_0=safe.directory`, and
`GIT_CONFIG_VALUE_0=<exact checkout>` set for the process—without writing Git
configuration—made every affected case pass.

The remaining failure reads the existing
`se_harness/hash_bound_classes.json` worktree bytes directly and requires LF;
this Windows checkout materializes that unchanged committed file as CRLF. Git
reports no diff for the file, exact managed integrity passes, and the failure is
outside the IPK change surface. The Linux candidate runner checks committed LF
bytes. No out-of-scope rewrite of that product file was performed.

Candidate-source `doctor` is supplementary and intentionally fails against this
development checkout because candidate templates already diverge from the
selected released 0.6.0 root, the installed root lacks candidate-only managed
skill additions, and child Git sees the same sandbox ownership boundary. Exact
released-evaluator `doctor`, which governs the root, passed.

## Focused negative and boundary coverage

- Main, pull-request, 40-character, 64-character, release, and pre-release
  identity vectors; uppercase/short commits; local base versions; invalid
  events, refs, and pull-request IDs.
- Missing, mismatched, and duplicate version declarations; unrelated version
  text preserved; exact two-path changed set and before/after hashes.
- Absolute, traversal, dot, backslash, control, case-collision, reserved-device,
  link, duplicate, special, oversized, and non-portable archive/payload/wheel
  members in implementation or verifier logic.
- Duplicate keys, BOM, noncanonical JSON, missing/unknown fields, invalid types,
  incorrect non-promotable marker, manifest/workflow mismatch, altered wheel,
  extra payload, malformed checksums, metadata drift, non-pure wheel, and wrong
  tag.
- Exclusive output collision that preserves existing owner bytes.
- Static workflow assertions for all prerequisite gates, exact action and build
  pins, event eligibility, staging/final names, Linux/Windows matrix, retention,
  least privilege, no dispatch input, and absence of publication/release or
  credential surfaces in the integration lane.
- Documentation assertions for discovery, download, checksum, isolated install,
  non-promotable identity, retention, disposable targets, ordinary-index
  warning, and governing-evaluator separation.

## Changed implementation paths

- `.github/scripts/build_integration_package.py`
- `.github/workflows/candidate-evidence.yml`
- `README.md`
- `docs/engineering/README.md`
- `docs/engineering/integration-package/evidence/WO-IPK-001-verification.md`
- `docs/notes/README.md`
- `docs/notes/developing-se-harness.md`
- `docs/notes/integration-packages.md`
- `tests/fixtures/integration_package/canonical_vectors.json`
- `tests/test_integration_package.py`

Every implementation path is admitted by `WO-IPK-001`. The IPK definition
artifacts, their accountable lifecycle events, and the definition-review note
preceded implementation and are not relabeled as implementation changes.
Concurrent uncommitted AEX Phase 2 files belong to another workstream and were
not edited, tested as IPK output, or included in this path manifest.

## Open commit-bound verification

1. The local host has none of the exact pinned `build`, `setuptools`, and
   `wheel` distributions installed. No network access or environment mutation
   was authorized, so a real backend build was not performed locally.
2. No exact candidate commit yet contains this evidence file and implementation.
   The working-tree digests above are not a substitute for a commit identity.
3. No hosted workflow was dispatched. Deterministic real-backend double build,
   exact action execution, staged/final payload equality, and installed
   Linux/Windows results remain open.
4. The Windows symlink-capability case is represented in logic and fixtures but
   requires a host that can create the link; capable CI remains required.
5. Final artifact discovery, download-command rehearsal against the real run,
   expiration behavior, and exact retained artifact digest remain open.

These items are expected consequences of `commit_bound_verification =
"required"` and the explicit prohibition on Git and external workflow actions.
They do not authorize weakening or deleting the corresponding gates.

## Intentionally not performed

No dependency download, package installation outside disposable test fixtures,
workflow dispatch, artifact upload/download, branch, commit, push, pull request,
merge, tag, GitHub Release, PyPI/TestPyPI operation, credential use, release
environment, RLS/REL/VREC preparation or transition, governing-evaluator
selection, managed-root upgrade, publication, deployment, or other external
action was performed.

The engineering owner must review this implementation and its open
commit-bound items before deciding whether `WO-IPK-001` becomes `implemented`.
That later decision does not verify the candidate or authorize a hosted run.
