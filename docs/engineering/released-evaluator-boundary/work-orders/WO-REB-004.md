+++
id = "WO-REB-004"
type = "work_order"
title = "Implement and requalify the predecessor-evaluator bootstrap"
status = "implemented"
owners = ["engineering-owner", "repository-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "required"
rationale = "The correction changes security-sensitive release validation, provenance binding, and credential-gated publication behavior, and the 0.6.0 release decision will rely on its exact candidate implementation."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-008"]
specifications = ["SPEC-REB-003"]
architecture = ["ARCH-REB-002", "ADR-REB-002"]
verification = ["VER-REB-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T15:40:28Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-21T15:40:28Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-21T17:09:35Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement and requalify the predecessor-evaluator bootstrap

## Lifecycle

Bounded implementation is complete at candidate `b033827cc9f8357a7afb1d82f336c6fe2fc16e26`, with local and hosted qualification retained at `docs/engineering/released-evaluator-boundary/evidence/WO-REB-004-verification.md`. This implemented state does not prepare or transition a VREC or RLS and does not authorize another push, tag, publication, deployment, maintenance mutation, credential use, external policy change, or root-evaluator upgrade.

## Objective

Implement one contract-bound predecessor-evaluator evidence adapter, retire candidate C from 0.6.0 promotion without rewriting it, and produce complete local qualification evidence for a new C2 that can be assessed by both the released 0.5.0 authority and candidate 0.6.0 compatibility rules.

## In scope

- Add strict parsing and validation of the approved `se-harness-release-bootstrap-v1` release-contract tuple.
- Add a repository-only plan/apply binder that verifies the exact canonical `utf8-text-lf-v1` schema-2 lock, public predecessor wheel, external predecessor identity, ready RLS, and immutable relations before atomically binding canonical evaluator evidence.
- Add candidate-validator compatibility for only that complete tuple while retaining schema-3 matching for every ordinary ready RLS.
- Add publication and release-bound Pages resolution of the exact predecessor evaluator for only the declared bootstrap RLS, with verification before credentials.
- Add the preparation-schema compatibility rule for released-0.5 legacy ready metadata without treating it as a release decision.
- Add deterministic positive, tamper, ambiguity, path, isolation, atomicity, historical, and publisher tests from `VER-REB-002`.
- Update candidate templates, package surface, repository publication tooling, CLI/operator documentation, and 0.6.0 release notes needed for the bounded behavior.
- Re-run exact full source regression, candidate/source/package identities, dual-runtime verifier-owned acceptance, reproducible wheel/sdist/offline reconstruction, bundle creation, formal graph, release-distribution, doctor, inspection, dashboard, parity, archive, lock, recovery, and secret/path/diff checks for C2.
- Retain one `WO-REB-004` evidence file containing the full C2 integrated requalification needed by a new aggregate VREC.

## Out of scope

- Modifying the operational `.engineering-harness.toml`, `.engineering-harness.lock`, managed root, maintenance branch, or current released evaluator.
- Repointing, editing, transitioning, committing, or publishing candidate C, `VREC-SEH-008`, or the current uncommitted `RLS-SEH-008`.
- Creating a candidate commit before separate reviewed-commit authority.
- Pushing a C2 branch or using credentials before exact action-time authority.
- Preparing or transitioning `VREC-SEH-009` or `RLS-SEH-009` without their separate authorities.
- Tagging, publishing, deploying, changing external policy, or performing post-publication root adoption.
- A generic legacy profile, missing-evidence allowlist, candidate evaluator, or emergency bypass.

## Authorized decision envelope

After this packet is approved, the implementation agent may choose internal helper names, deterministic diagnostic suffixes, temporary-file layout, and bounded test-fixture organization. It may not broaden the bootstrap tuple, infer expected identity, weaken normal schema-3 enforcement, exercise lifecycle or external authority, or treat candidate evidence as released-evaluator assurance.

## Constraints

- Preserve Python 3.11+, standard-library runtime behavior, and exactly one standard installation.
- Preserve owner content, historical records, current root bytes, and all C/VREC/RLS captured facts.
- Treat repository, Git, paths, symlinks, TOML/JSON, wheel/archive, runtime, workflow, and external inputs as untrusted.
- Fail before target writes or credentials on every mismatch and prove before/after byte equality.
- Keep candidate source, candidate package, and exact external released evaluator separately identified.
- A change after C2 aggregate capture invalidates the candidate and requires a new evidence/VREC/RLS sequence.

## Expected change surface

- Candidate standard artifact validator and templates.
- Evaluator-evidence and release-contract parsing helpers where portable behavior belongs.
- Repository-only bootstrap binder and release/publication resolvers.
- Release orchestration, Pages provenance, and candidate-evidence workflow checks as required by the approved design.
- Focused validation, publication, provenance, mutation-boundary, release-orchestration, distribution, and architecture tests.
- Operator guidance, 0.6.0 release documentation, and `WO-REB-004` retained evidence.

The installed root's released-0.5 managed copies are not an expected change surface.

## Required verification

- Execute every method and scenario in `VER-REB-002` and the unchanged `VER-REB-001` regression surface.
- Run released 0.5 identity, doctor, validation, inspection, preflight, and preparation in an isolated external environment.
- Prove candidate source/package never imports into the evaluator environment or mutates the operational root.
- Run full supported source tests and exact candidate-package acceptance on Python 3.11 and the current qualification runtime.
- Build twice from exact exported C2 at its commit epoch; require identical wheels/normalized sdists and identical offline reconstructed wheel.
- Validate safe equivalent archives, wheel RECORD, source/checksum/bundle manifests, package surface, managed parity, and release-distribution policy.
- Retain hosted candidate-source/package and standard evaluator results only after separate branch-push authority.
- Run released and candidate formal validation, review preflight, inspection, dashboard, `git diff --check`, and bounded secret/path review.

## Evidence to record

- Exact approval/preflight manifest and changed paths.
- Current canonical `utf8-text-lf-v1` lock SHA-256 and independently reconciled public 0.5.0 wheel identity.
- Bootstrap parser/binder/publisher positive and exhaustive negative results, injected failures, and recursive before/after digests.
- Released-evaluator, candidate-source, candidate-package, wheel, sdist, bundle, verifier, runtime, hosted-run, and candidate Git identities.
- Exact test counts, skips, warnings, deviations, and resolution of every required failure.
- Formal graph, inspection, dashboard, distribution, archive, parity, diff, and secret/path results.
- Explicit statement of every lifecycle, credential, external, maintenance, and root action not performed.

## Stop and escalate conditions

- Exact old-lock or public-wheel identity cannot be independently reconciled.
- The design would accept missing evidence, more than one record, version-only trust, candidate authority, or a non-approved contract.
- Binding cannot be atomic and zero-write on failure.
- Released-0.5 and candidate compatibility cannot both be retained without reinterpreting a release decision.
- Publication cannot stop before credentials on mismatch.
- Any required local or hosted qualification fails or produces nondeterministic distributions.
- Work requires root, maintenance, credential, external policy, lifecycle, tag, publication, or deployment authority not separately granted.

## Completion report format

Report the exact bootstrap tuple and trust direction, changed surfaces, zero-write proofs, released/candidate identities, full qualification and distribution identities, retained evidence, lifecycle state, unresolved risks, unperformed actions, and the single next accountable decision.

## Canonical-LF correction

The accountable owners authorized the bounded correction on 2026-08-21 at `2026-08-21T16:31:42Z`. Local implementation and qualification bind canonical `utf8-text-lf-v1` lock SHA-256 `08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3`. The separately authorized local and hosted qualification completed successfully, and the work order transitioned from `in_progress` to `implemented` at `2026-08-21T17:09:35Z`; every other scope and authority boundary is preserved.
