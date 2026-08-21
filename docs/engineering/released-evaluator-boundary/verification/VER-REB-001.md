+++
id = "VER-REB-001"
type = "verification"
title = "Released-evaluator boundary and recovery assurance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
verifies = ["REQ-REB-001", "REQ-REB-002", "REQ-REB-003", "REQ-REB-004", "REQ-REB-005", "REQ-REB-006", "REQ-REB-007"]
+++

# Verification Contract: Released-evaluator boundary and recovery assurance

## Independence

The implementation actor may create fixtures and raw results, but the assurance owner selects adversarial cases, reviews the standard lock and canonicalization contract, reconciles exact external wheel hashes independently, and assesses zero-write snapshots and recovery authority boundaries. Candidate-source and candidate-package results are separately labeled and never substitute for the exact released evaluator used for root preflight, doctor, validation, inspection, or readiness assessment.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-REB-001` | Boundary and injected-failure tests for every public mutator | Official external evaluator; candidate source; editable install; candidate wheel; wrong version/digest/payload; checkout path; symlink; user site; `PYTHONPATH`; interrupted guard | Exact evaluator passes; every invalid case fails before a recursive target snapshot changes |
| `REQ-REB-002` | Executable workflow-contract integration | Disposable standard snapshot, exact local/public wheel, PyPI and Pages workflow command extraction | Both workflows resolve standard identity, hash before install, use supported CLI options, validate externally, and stop before promotion on mismatch |
| `REQ-REB-003` | Schema, canonicalization, and provenance tests | Ready RLS with valid, missing, modified, candidate, duplicate-key, absolute-path, and wrong-digest evidence | Only canonical verified identity evidence is bound and replay validation detects every mutation |
| `REQ-REB-004` | Active-surface package and repository scan | Wheel members, CLI help, standard templates, active workflows/scripts, historical RCA and migration fixtures | No executable retired surface exists; explicit historical evidence remains accepted and unchanged |
| `REQ-REB-005` | Policy fixture and manual scope review | Separate N/N+1 release and upgrade packets; deliberately combined circular packet | Separate sequence passes; combined or unpublished-target adoption is rejected before apply |
| `REQ-REB-006` | Deterministic validator/inspection scenarios | Same-version draft RLSs; overlapping ready VRECs at different commits; valid supersession; normal historical releases | Closed conflict rules report exact affected IDs without false positives or automatic lifecycle action |
| `REQ-REB-007` | Disposable no-credential rehearsal and security review | Immutable selection, simulated publication, public-install equivalent, standard-root conversion, injected stage failures, restoration checks | Happy path restores all standard controls; each injected failure stops at the declared stage without operational or external mutation |

## Acceptance scenarios

1. An exact public wheel is downloaded, independently hashed, installed outside the checkout, and its payload/archive identity matches the standard lock; guarded draft creation succeeds.
2. Candidate source reports the same version and caller-provided official digest; guarded draft creation fails and creates no directory or temporary file.
3. A separately published target evaluator plans a schema-2-to-schema-3 upgrade; the exact plan is reviewed, apply is authorized, transaction succeeds, and replay is a no-op.
4. Current `publish-pypi.yml` and `publish-dashboard-pages.yml` commands are executed against a disposable standard snapshot and the actual CLI parser; no retired role or option remains.
5. A ready RLS binds normalized evaluator evidence; modifying one evidence byte causes validation and publication resolution to fail.
6. Historical RCA text containing `governor` passes while an active workflow using `--role governor` fails.
7. Competing drafts are reported without state transition, and an explicitly superseded ready VREC is not reported as unresolved overlap.
8. The recovery rehearsal converts a disposable deadlocked fixture to the standard root and proves normal evaluator, candidate, publisher, absence, and rollback controls.

## Property and invariant tests

- Canonical payload manifests are deterministic under file enumeration order and supported line endings and change for every changed protected byte, path, or mode.
- Lock and evidence JSON reject duplicate keys, unknown critical fields, unsafe basenames, malformed versions, non-lowercase or wrong-length hashes, partial archive pairs, and path traversal.
- For every negative identity diagnostic, before/after target maps are identical, including absent directories and recovery-state files.
- Artifact graph and inspection results are deterministic across repeated runs.
- Candidate acceptance never imports from the checkout or evaluator environment.

## Static and architecture checks

- Trace every guarded public mutator to the shared identity implementation.
- Prove dependency direction from standard lock to runtime, publication, and provenance; no candidate or legacy descriptor supplies expected identity.
- Search active code, workflow commands, package data, templates, CLI help, and distribution archives for prohibited executable surfaces.
- Review managed and repository-owned workflow permissions, action pinning, checkout refs, credential timing, and external environment boundaries.
- Validate all REB formal relations, decision assessment, ADR coverage, work-order specification/architecture/verification coverage, and assurance classification.

## Security and privacy checks

- Independently reconcile exact public wheel SHA-256 and installed PEP 610/archive observation.
- Exercise symlink/junction, case normalization, relative path, entry-point substitution, user-site, `PYTHONPATH`, current-directory import, and environment-crossing attacks.
- Confirm retained identity evidence contains normalized roots and bounded facts only—no usernames, home paths, tokens, environment dumps, or repository bodies.
- Confirm publication download and digest verification happen before any job receives write or OIDC permission.
- Confirm real recovery instructions require action-time authority and cannot be invoked by candidate content.

## Performance and resilience checks

- Measure payload-manifest time and memory at current package size and the maximum candidate-acceptance budget.
- Inject file-read, hash, temporary-write, replace, lock-migration, workflow-download, install, validation, and restoration failures.
- Prove transaction recovery and no-op replay on supported Windows and POSIX path semantics.
- Keep full regression and disposable rehearsal within the declared hosted CI timeout.

## Manual assessments

- Product and requirements owners confirm the packet prevents recurrence without creating a second installation profile.
- Technical and security owners accept or revise `ARCH-REB-001` and `ADR-REB-001`, including payload canonicalization and legacy migration.
- Assurance owner judges whether negative cases and normalized evidence are independent and complete.
- Release owner confirms publication and recovery retain protected-environment and decision boundaries.
- Documentation review confirms current terminology uses *released evaluator* and *candidate* while historical evidence remains accurate.

## Evidence retention

Each implemented work order retains evaluator identity and wheel digest; governing preflight manifests; exact changed paths; test commands and counts; zero-write snapshot digests; lock migration and no-op results; workflow contract outputs; active-surface scan; identity-evidence examples; graph and inspection reports; diff and secret/path review; manual assessments; deviations; residual risks; and every external or lifecycle action not performed. Evidence filenames are keyed to the applicable `WO-REB-*`.

## Residual uncertainty

- Automated checks cannot prove that a human approval, emergency declaration, or release decision is wise or authentic.
- Package managers and hosting services remain external dependencies during real acquisition and publication.
- Structural overlap rules cannot infer semantic intent outside declared relations.
- A repository writer can always edit files directly; this contract prevents harness-mediated authority substitution and makes reviewed state observable, but it is not a host access-control system.
