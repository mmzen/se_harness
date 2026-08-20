+++
id = "VER-DST-020"
type = "verification"
title = "Verify topology headroom without boundary regression"
status = "approved"
owners = ["quality-owner", "security-owner", "repository-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
verifies = ["REQ-DST-062", "REQ-DST-063", "REQ-DST-064"]
+++

# Verification Contract: Verify topology headroom without boundary regression

## Independence

Verification reads serialized output and public runtime identities rather than trusting implementation-internal success flags. The public 0.5.0 evaluator validates root governance and managed integrity; separately labeled candidate-source and candidate-package lanes assess the changed product contract.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-DST-062 | exact constant and serialized-size tests | current repository, below/equal/above target fixtures | target is exactly 2,097,152; current repository passes; excess remains explicit and nontruncating |
| REQ-DST-063 | repeat, cross-runtime, push and pull-request observations | Windows/default, Python 3.11, hosted branch and merge ref | identical inputs/history are deterministic; all executions use the same target; merge-ref acceptance passes |
| REQ-DST-064 | origin, managed-integrity and unchanged-budget audit | external evaluator identity, doctor, candidate package install, changed paths | root remains exact public 0.5.0; candidate package carries 2 MiB; every other boundary is unchanged |

## Acceptance scenarios

- Reproduce baseline 525,689 > 524,288 on merged `af0eaa0` before implementation.
- Generate the implemented current repository twice; recursively compare paths and bytes and prove topology is at most 2,097,152.
- Exercise deterministic fixtures immediately below, equal to, and above 2,097,152 without allocating unbounded memory.
- Run the exact candidate on a branch push and pull-request merge ref and retain both topology observations.
- Install a nonpromotable candidate wheel into a disposable environment and initialize a standard repository whose installed generator declares 2,097,152.
- Run public-0.5.0 doctor on the implementation repository and prove the active root generator and lock remain unchanged.

## Property and invariant tests

- `TOPOLOGY_ACCEPTANCE_BYTES == 2_097_152` in the candidate canonical template.
- `topology_target_exceeded` is true if and only if serialized topology bytes are greater than the target.
- Topology nodes, relations, findings, revision provenance, detail descriptors, schemas, paths, ordering, and digests are unchanged for the same projection.
- Shell, summary, per-document, and total-content constants remain exactly 262,144, 262,144, 262,144, and 16,777,216.
- Existing body-exclusion, manifest, deterministic, transaction, publisher, browser, and safe-render tests remain green.

## Static and architecture checks

- Validate the formal graph with zero structure, governance, or policy errors/warnings.
- Confirm `ARCH-DST-013` addresses all three requirements, conforms to `SPEC-DST-020`, and has an approved no-significant-decision assessment before work-order approval.
- Confirm existing 524,288 references are amended only on the authorized contract surfaces and no stale executable assertion remains.
- Confirm no new ADR relation is fabricated and `ARCH-DST-010`/`ADR-DST-010` remain unchanged.

## Security and privacy checks

- Compare manifest path/size/digest, exact-set, duplicate-key, invalid UTF-8, traversal, symlink, oversized source, hostile Markdown, and publication tests before/after.
- Scan changed files for credentials, private paths, new origins, dependencies, permissions, persistence, and network behavior.
- Prove no artifact, relation, finding, provenance, or evidence reference is removed to reduce size.

## Performance and resilience checks

- Record baseline and candidate topology bytes before compression and absolute/percentage headroom.
- Assert current candidate topology remains below 2 MiB after adding this packet and its later VREC integration history.
- Retain repeat-generation digests and role totals.
- Exercise above-target observation without failed bundle promotion or formal-graph error.
- Treat a future approach to 2 MiB as a trigger for separately governed topology sharding, not silent threshold drift.

## Manual assessments

- Product owner confirms fourfold headroom is intentional and significant.
- Technical owner accepts the no-significant-decision assessment.
- Repository/security owners confirm the active root remains governed by public 0.5.0 and candidate bytes were not used as evaluator.
- Assurance owner reviews exact branch and merge-ref evidence before VREC transition.

## Evidence retention

Retain owner approval, preflight manifests, baseline commit/graph/bytes, exact changed paths, old/new constants, amended definition ledger, deterministic hashes, boundary fixtures, local runtime versions, public evaluator identity, doctor/validation/inspection/dashboard results, candidate package origins, branch and pull-request run URLs, topology observations, full test counts, deviations, residual risks, and every unperformed lifecycle/release/external action at `docs/engineering/harness-distribution/evidence/WO-DST-020-verification.md`.

## Residual uncertainty

Repository topology will continue to grow and valid Git integration history can increase provenance bytes. Two MiB provides substantial headroom but is not permanent proof against arbitrary growth. Static hosting, compression, browser hardware, and future graph shape remain environment-dependent; a later sharding decision requires separate authority.
