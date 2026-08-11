# Verification Evidence: WO-DST-004

## Authorization and candidate scope

The accountable user approved the `REQ-DST-015..018` governing chain and bounded implementation on 2026-08-11 with `go for implementation`. Work remained on branch `feature/canonical-artifact-layout-packet`. No commit, push, pull request, verification transition, release action, package build, publication, external configuration, or consumer-repository mutation was performed.

The active `C:\Users\mathi\RustroverProjects\Mokiterions` repository was used only as previously reported context and was not read or written during implementation or verification.

## Implemented behavior

- Added one package-level canonical registry for 12 supported formal artifact types, their prefixes, templates, domain-local directories, supporting directories, slug rules, and reserved names.
- Added a byte-identical portable registry beside installed repository scripts so the validator remains independently runnable without importing the package; deterministic parity tests prevent drift between that registry, the canonical template, and package constants.
- Added `harnessctl scaffold-domain TARGET --domain DOMAIN [--title TITLE] [--dry-run]` with complete-plan validation, safe parent/link checks, rollback of only empty directories created by the invocation, exclusive index creation, existing-index preservation, and no managed-lock ownership for domain content.
- Added `harnessctl create-artifact TARGET --domain DOMAIN --type TYPE --id ID [--dry-run]` with canonical template and destination routing, type-prefix and duplicate-ID checks, safe parent/link checks, atomic exclusive creation, and explicit incomplete-`draft` output.
- Added explicit `--domain` and common-work-order-domain inference to verification capture and release preparation. Explicit `--output` remains highest precedence; cross-domain, domainless, and ambiguous work uses the repository-wide aggregate record directories.
- Added deterministic validator diagnostic `W013` for valid artifacts outside the expected canonical location. It does not affect validity or exit status, and it is projected by `doctor` and Harness Explorer.
- Preserved recursive metadata-based discovery and all typed relation, lifecycle, evidence, commit, and release authority checks.
- Updated managed guidance, fresh owner-index seed guidance, public onboarding and command reference, package data, canonical template copies, self-hosted copies, and the schema-2 managed lock.

## Canonical mapping coverage

Table-driven tests cover `intent`, `capability`, `requirement`, `specification`, `architecture`, `adr`, `verification`, `work_order`, `verification_record`, `release_contract`, `release_record`, and `operating_contract`. They also cover `evidence/`, `acceptance/`, and the repository-owned domain `README.md` without treating those supporting paths as formal authority.

Every generated formal path is `docs/engineering/<domain>/<canonical-type-directory>/<ID>.md`. Repository-wide `docs/engineering/verification-records/` and `docs/engineering/releases/` remain the aggregate fallback.

## Boundary and failure verification

- Dry runs resolve and report the same destinations without writing.
- Invalid case, whitespace, traversal, path separators, overlength slugs, and reserved domains are rejected.
- Unknown artifact types, malformed identifiers, and type-prefix mismatches are rejected.
- Existing destinations and duplicate IDs are preserved and rejected.
- Existing repository-owned domain indexes remain byte-identical.
- Injected index-write failure rolls back the otherwise empty scaffold created by that invocation.
- Link escape is tested when the host permits unprivileged symlink creation; the current Windows host skipped that case rather than claiming it.
- Atomic output uses a same-directory temporary file and exclusive hard-link creation; concurrent content is never overwritten.
- Upgrade tests retain flat artifacts, canonical artifacts, and domain indexes byte-for-byte and never add them to the managed lock.
- A temporary 0.2.1-style flat intent remains graph-valid, receives exactly one `W013`, appears in `doctor`, and is not moved.
- Canonical placement never repairs invalid metadata or relations.

## Provenance routing verification

- One or multiple work orders below the same `product` domain default new VREC and RLS records to that domain.
- Explicit safe domains route verification and release records to their requested domain.
- Explicit safe `--output` overrides a simultaneous valid domain.
- An invalid explicit domain fails even when an output is provided.
- Moving one selected work order to a temporary `billing` domain makes the aggregate VREC default to the repository-wide directory; no domain is guessed.
- Existing clean-tree, Git identity, evidence, selection, release gating, exact-coverage, exclusive output, and no-tag/no-commit tests continue to pass.

## Exact verification results

### Start preflight

Command:

```text
python -m se_harness preflight . --work-order WO-DST-004
```

Result: PASS with work order `approved` and the complete `INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-015..018` -> definition/architecture/verification -> `WO-DST-004` reading manifest.

### Focused behavior

Command:

```text
python -m unittest tests.test_artifact_authoring tests.test_revision_provenance.RevisionCliTests
```

Result: PASS, 19 tests, 1 skipped host-link case.

### Complete regression suite

Command:

```text
python -m unittest discover -s tests -p "test_*.py"
```

Initial and final runs passed. The final result was 90 tests in 39.678 seconds, 3 skips, 0 failures, and 0 errors.

### Managed installation integrity

Commands:

```text
python -m se_harness upgrade .
python -m se_harness upgrade . --apply
python -m se_harness doctor .
```

Results: upgrade plan and apply each reported 33 template files unchanged relative to the new canonical distribution; schema-2 lock was regenerated; every required, distribution, managed, seed, runtime, and script check passed. Doctor additionally emitted the seven `W013` layout advisories listed below without changing its successful exit status.

### Artifact graph

Command:

```text
python scripts/validate_engineering_artifacts.py --root .
```

Result: PASS, 198 artifacts, 0 errors, 7 nonblocking `W013` warnings.

The warnings identify historical organizational differences without changing authority:

- domain-local records whose selected work spans domains: `VREC-PMI-001`, `VREC-SEH-001`, `RLS-SEH-001`, `VREC-SEH-002`, and `RLS-SEH-002` now advise the repository-wide aggregate location;
- repository-wide records whose work belongs unambiguously to `harness-distribution`: `VREC-DOC-003` and `VREC-DOC-005` now advise the domain-local location.

No historical record was moved or rewritten.

### Explorer and CLI

Commands:

```text
python scripts/generate_harness_dashboard.py --root .
python -m se_harness --help
```

Results: CLI help PASS. Explorer PASS with 198 artifacts, 680 relations, 0 errors, and 8 warnings. Seven are the new nonblocking layout advisories; the eighth is the pre-existing `W-REV-004` review observation for ready `VREC-AGR-001`. Final snapshot: `daf303b27d2c8677ffb15d362a0b30712e94dfefe43533ceab9183d4bee00c9c`.

### Review preflight

Command:

```text
python -m se_harness preflight . --work-order WO-DST-004 --phase review
```

Result: PASS with `WO-DST-004` in `implemented` state and the complete governing manifest. A loader-boundary defect discovered during the first review attempt was corrected by making the validator load its sibling portable registry explicitly by file path; the final preflight and full regression suite cover that path.

### Static change checks

`git diff --check` passed for tracked changes. Final whitespace, protected-path, graph, review-preflight, and deterministic Explorer checks are repeated after evidence and lifecycle updates.

## Ownership and protected surfaces

Changed surfaces are bounded to the approved artifact packet, authoring and provenance control plane, validator/doctor projection, managed canonical guidance and templates, package data metadata, self-hosted integrity lock, deterministic tests, public documentation, acceptance scenarios, and this evidence.

Protected and unchanged surfaces include the consumer repository, historical VREC/RLS contents, package version `0.2.1`, release contracts and records, workflow baseline pins, release workflows, tags, build outputs, PyPI/GitHub state, installation profiles, and external configuration.

## Deviations and residual risks

There is no requirement deviation. The portable validator keeps a local registry mirror because repository-local validation must run without package import availability; parity tests make the two physical representations one deterministic logical contract.

Filesystem link and reparse-point behavior remains platform-dependent. Portable containment and Windows reparse checks are implemented, while one unprivileged symlink case was skipped on the current host. A `W013` is guidance, not proof that a migration is safe under concurrent editing. Existing historical layout advisories remain until an accountable owner separately authorizes any repository moves.
