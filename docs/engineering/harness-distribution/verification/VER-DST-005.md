+++
id = "VER-DST-005"
type = "verification"
title = "Verify canonical layout and safe domain-aware authoring"
status = "approved"
owners = ["quality-owner", "security-owner", "documentation-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-DST-015", "REQ-DST-016", "REQ-DST-017", "REQ-DST-018"]
+++

# Verification Contract: Verify canonical layout and safe domain-aware authoring

## Independence

Verification derives assertions from `REQ-DST-015` through `REQ-DST-018` and uses disposable repository fixtures. It does not treat successful creation, canonical placement, a clean graph, or a generated record as approval, assurance, or release authority. It must not inspect or mutate an active consumer repository as test data.

## Requirement-to-evidence matrix

| Requirement behavior | Method | Pass condition |
| --- | --- | --- |
| Canonical domain-and-type layout is complete | table-driven unit tests and installed-guidance inspection | every supported formal type has exactly one approved domain-local directory and filename rule |
| Paths remain organizational | legacy and canonical graph comparison | equivalent metadata produces equivalent graph meaning and a path never supplies missing authority |
| Domain and artifact creation are safe | CLI integration, path-adversary, conflict, and failure-atomicity tests | valid drafts are created exclusively; invalid or conflicting plans leave no partial writes |
| Creation never authorizes | rendered-template and lifecycle inspection | the new artifact is an incomplete `draft` and normal validation and accountable transitions remain required |
| Provenance is domain-aware | precedence and single-/multi-domain integration tests | output, explicit domain, inferred domain, and aggregate destinations follow the specified order |
| Legacy repositories remain valid | flat-layout fixture, validator, doctor, and dashboard checks | artifacts remain in the graph, validation succeeds, and deterministic nonblocking guidance names the canonical path |
| Upgrades preserve owner content | byte-level init/adopt/upgrade scenarios | existing flat and canonical artifacts and domain indexes are neither moved nor rewritten |

## Automated checks

- Exercise the canonical registry for `intent`, `capability`, `requirement`, `specification`, `architecture`, `adr`, `verification`, `work_order`, `verification_record`, `release_contract`, `release_record`, and `operating_contract`.
- Verify supporting `evidence/`, `acceptance/`, and domain-index guidance without misclassifying those locations as formal authority.
- Test minimum, maximum, and representative domain slugs; reject uppercase, whitespace, separators, absolute and drive paths, traversal, reserved names, normalization ambiguity, and overlength input.
- Test valid identifiers for every supported type and reject unsafe stems, unknown types, invalid grammar, and prefix/type mismatches.
- Test file, directory, symlink, junction, existing-destination, and parent-chain conflicts on the available platforms.
- Verify dry-run and write mode use identical resolution and checks, while dry-run produces no filesystem changes.
- Inject a bounded write failure and verify no partial scaffold or artifact is reported or retained.
- Verify scaffolding preserves an existing domain index byte-for-byte and does not create product artifacts or lock entries.
- Verify artifact creation uses the canonical template, correct destination, UTF-8, ID, type, dates, and `draft` state, and leaves accountable prompts incomplete.
- Verify explicit `--output` takes precedence over `--domain`, explicit domain takes precedence over inference, and unsafe explicit values fail before writing.
- Verify one canonical-domain work order and one legacy-flat work order each yield the correct domain-local verification and release destinations.
- Verify work spanning two domains, repository-wide work, missing source attribution, and ambiguity yield repository-wide aggregate destinations.
- Verify established clean-tree, exact-commit, work-order selection, verification state, release-gating, and exclusive-create protections are unchanged.
- Verify a legacy flat-layout fixture produces stable actual/expected-path advisories while returning the same graph-validation success as its canonical equivalent.
- Verify malformed metadata and graph errors remain errors independent of path, and path advice never repairs or suppresses them.
- Verify intentional repository-wide aggregate verification and release records do not receive false noncanonical warnings.
- Verify `init`, `adopt`, and `upgrade` under the existing managed-lock rules; ensure upgrade never moves, rewrites, deletes, or begins tracking owner artifacts or domain indexes.
- Verify canonical guidance and command references in fresh installed `AGENTS.md` and engineering documentation, self-hosted files, package data, and lock parity where each surface is managed.
- Run the full unit suite on Python 3.11 and the available local runtime, CLI help smoke tests, formal graph validation, `doctor`, start and review preflight as phase-appropriate, and deterministic dashboard generation.
- Confirm no build, version, release, workflow-pin, tag, publication, external configuration, or consumer-repository change.

## Acceptance scenarios

Execute the scenarios in `acceptance/artifact-layout.feature` through deterministic integration tests or equivalent assertions. Retain mapping from each scenario to exact test cases in the work-order evidence.

## Manual assessments

- Review the installed guidance as a coding agent and confirm the correct destination can be selected without reconstructing repository conventions.
- Review command output as a repository owner and confirm it distinguishes file creation from artifact completion, validation, approval, verification, and release.
- Review a flat-layout advisory and confirm it is actionable but does not pressure an unsafe migration during concurrent work.
- Inspect the Explorer/dashboard for canonical and legacy fixtures and confirm the same five governance questions remain metadata-driven.

## Pass criteria

All mapped automated checks pass; adversarial cases create no unsafe or partial writes; legacy layouts remain graph-valid; advisories are deterministic and nonblocking; aggregate exceptions are correct; upgrade preserves owner bytes and paths; installed and packaged guidance is coherent; and no path is treated as governance authority.

## Evidence retention

Retain exact commands, runtime versions, test names and counts, temporary-fixture definitions, canonical mapping coverage, adversarial-path results, failure-injection result, provenance-routing matrix, validator and doctor diagnostics, dashboard snapshots, byte-preservation hashes, installed/package parity results, changed and protected paths, deviations, and residual risks under `WO-DST-004`.

## Residual uncertainty

Filesystem link and path semantics vary across supported platforms. Tests must exercise available Windows behavior and portable path logic, while any platform-specific limitation is documented rather than overstated. Advisory guidance cannot prove that an owner-selected migration time is free of concurrent writers.
