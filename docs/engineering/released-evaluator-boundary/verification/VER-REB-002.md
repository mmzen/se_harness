+++
id = "VER-REB-002"
type = "verification"
title = "Predecessor-evaluator bootstrap assurance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
verifies = ["REQ-REB-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T15:40:28Z"
decided_by = "quality-owner"
+++

# Verification Contract: Predecessor-evaluator bootstrap assurance

## Independence

The implementation actor may build fixtures and raw results, but the assurance and security owners independently select negative tuples, reconcile the public 0.5.0 wheel digest, review the canonical `utf8-text-lf-v1` schema-2 lock binding, inspect zero-write snapshots, and verify that candidate code never performs predecessor lifecycle work. Candidate results cannot substitute for exact released-0.5 preparation and validation.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-REB-008` | Schema and contract tests | Complete approved bootstrap; draft/rejected/missing/extra/duplicate/wrong-type fields; alternate RLS/version | Only the exact active contract tuple enables the path |
| `REQ-REB-008` | Lock and evaluator identity tests | Exact canonical schema-2 lock; CRLF/LF equivalence; non-line-ending content drift; config drift; public wheel match/mismatch; installed payload and origin attacks | Exact predecessor passes; all material drift fails before writes |
| `REQ-REB-008` | Atomic binder tests | New/occupied sidecar, changed RLS, symlink/traversal, injected failures at each replacement boundary | Success writes only canonical evidence/binding; every failure preserves the complete before map |
| `REQ-REB-008` | Dual-validator compatibility | Released 0.5 and candidate 0.6 against bound/unbound/tampered RLS fixtures | Bound bootstrap passes both; missing or changed evidence fails candidate validation |
| `REQ-REB-008` | Publication replay | Exact governance commit and every contract/lock/evidence/candidate/bundle mismatch | Exact plan resolves public 0.5; every mismatch stops before simulated credentials |
| `REQ-REB-008` | Integrated candidate qualification | C2 source, wheel, sdist, two runtimes, verifier-owned acceptance, hosted lanes | All replacement release gates pass and produce new exact identities |

## Acceptance scenarios

1. Public 0.5.0 prepares the exact ready RLS; the binder verifies the approved tuple and creates canonical evidence plus binding atomically.
2. Released-0.5 validation passes the resulting graph and candidate validation passes through the one bootstrap rule.
3. The same ready RLS without a sidecar, with changed evidence, or under a different contract fails candidate validation.
4. A different ready RLS under schema 2 cannot use the bootstrap and still requires a schema-3 lock.
5. Publication replay hashes the public predecessor wheel, validates its external installed identity, and produces a no-credential plan for the exact released RLS.
6. Moving any candidate, VREC, RLS, release-contract, work-set, version, bundle, lock, or evaluator identity causes deterministic rejection.
7. Later schema-3 lock rotation preserves validation of the released historical RLS evidence without enabling a second bootstrap.

## Property and invariant tests

- Contract parsing rejects duplicate and unknown security-critical fields and is deterministic under key order.
- Canonical evidence and lock-identity bytes are deterministic across supported line endings and platforms.
- Every negative binder injection leaves recursive path, kind, link target, and file bytes unchanged.
- Expected identity is never sourced from runtime claims or evidence under test.
- One contract can authorize at most one exact RLS/version pair.
- Candidate, VREC, RLS, work-set, and distribution equality are exact full-object identities.

## Static and architecture checks

- Trace the binder to a repository-only surface and prove it cannot call lifecycle transition, tag, push, publication, deployment, or root-upgrade code.
- Trace normal validator/publication behavior to schema-3 lock identity and the special path only to the approved contract tuple.
- Prove no generic schema-2, ID-only, version-only, or missing-evidence fallback exists.
- Review conformance to `ARCH-REB-002` and accepted `ADR-REB-002`.

## Security and privacy checks

- Reconcile canonical `utf8-text-lf-v1` lock SHA-256 and wheel SHA-256 independently from retained evidence.
- Exercise current-directory import, `PYTHONPATH`, user site, editable install, wrong entry point, cross-environment roots, symlink/junction, path traversal, case ambiguity, archive substitution, and partial evidence.
- Confirm evidence contains only normalized roots and bounded facts with no secrets, usernames, home paths, repository bodies, or environment dumps.
- Confirm publication failure occurs before OIDC/write permissions and binder failure before root/RLS mutation.

## Performance and resilience checks

- Measure bounded public-wheel/payload validation at current package size.
- Inject read, hash, parse, exclusive-create, temporary-write, flush, replace, rollback, Git-read, install, and publisher-stage failures.
- Run supported Python 3.11 and current qualification runtime; retain exact versions, counts, skips, and deviations.

## Manual assessments

- Product and requirements owners confirm the bootstrap is necessary and limited to the first evidence-format release.
- Technical and security owners accept or revise `ARCH-REB-002` and `ADR-REB-002`.
- Assurance owner judges the evidence independent and complete.
- Release owner confirms the bootstrap does not imply RLS transition, tag, publication, or later root adoption.

## Evidence retention

`WO-REB-004` evidence retains the approved manifest; exact changed paths; old-lock and public-wheel hashes; binder plans and atomic snapshots; complete positive/negative matrix; released-evaluator, candidate-source, and candidate-package identities; dual-validator output; full regression; reproducible build and bundle hashes; verifier-owned dual-runtime acceptance; hosted runs; graph, inspection, distribution, dashboard, diff, secret/path review; deviations; and all unperformed external/lifecycle actions.

## Residual uncertainty

- Automation cannot determine whether accepting a one-release bootstrap is a wise product or security decision.
- Public hosting and protected environments remain external dependencies.
- The binder can prove exact observations but cannot turn candidate code into released authority or exercise human decision rights.

## Canonical-LF correction

The accountable owners authorized the bounded correction on 2026-08-21 at `2026-08-21T16:31:42Z`. Verification now treats LF, CRLF, and CR serialization as equivalent only through the declared `utf8-text-lf-v1` canonicalization and still rejects every other lock-content change. Status and all remaining assurance scope are unchanged.
