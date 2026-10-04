+++
id = "WO-HAG-002"
type = "work_order"
title = "Implement and qualify standalone draft validation in the evaluator"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"
[assurance]
commit_bound_verification = "required"
rationale = "Later hosted acceptance and release decisions rely on the changed validator, shared relationship rules and managed instructions. mmzen explicitly confirmed required commit-bound verification with approval of this reviewed package."
decided_by = "mmzen"

[execution_scope]
paths = ["se_harness/relation_policy.py", "se_harness/draft_validation.py", "se_harness/engine/validation_architecture.py", "se_harness/engine/validation_evidence.py", "se_harness/engine/validation_core.py", "se_harness/engine/validation_lifecycle.py", "se_harness/engine/validation_authoring.py", "se_harness/engine/validate_engineering_artifacts.py", "se_harness/preflight.py", "se_harness/cli.py", "se_harness/codes.py", "tests/test_draft_validation.py", "tests/test_relation_policy.py", "tests/test_artifact_authoring.py", "tests/test_authoring_gate.py", "tests/test_cli_shape.py", "tests/test_validation_taxonomy.py", "tests/test_one_validation.py", "templates/repository/standard/docs/engineering/harness/DRAFT_DEFINITIONS.md", "templates/repository/standard/docs/engineering/harness/DEFINITION_LINKS.md", "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md", "docs/notes/harnessctl-reference.md", "docs/notes/diagnostic-codes.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-002/"]

[relations]
implements = ["REQ-HAG-009"]
specifications = ["SPEC-HAG-004"]
verification = ["VER-HAG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T13:24:31Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved REQ-HAG-009, SPEC-HAG-004, VER-HAG-002 and WO-HAG-002 for local implementation with required commit-bound verification in this conversation. Reviewed manifest SHA-256: e36a47fb59f1bf1f856aa8a47c20189bc84d9d53d787fce505e6bc0f895eabe8. All complete reviewed bytes matched; only the confirmed assurance table was completed before preview. This approval grants bounded local implementation and required verification preparation, not verification acceptance, publication, release or governor adoption. DEC-HAG-001 remains unchanged."
scope_paths = ["se_harness/relation_policy.py", "se_harness/draft_validation.py", "se_harness/engine/validation_architecture.py", "se_harness/engine/validation_evidence.py", "se_harness/engine/validation_core.py", "se_harness/engine/validation_lifecycle.py", "se_harness/engine/validation_authoring.py", "se_harness/engine/validate_engineering_artifacts.py", "se_harness/preflight.py", "se_harness/cli.py", "se_harness/codes.py", "tests/test_draft_validation.py", "tests/test_relation_policy.py", "tests/test_artifact_authoring.py", "tests/test_authoring_gate.py", "tests/test_cli_shape.py", "tests/test_validation_taxonomy.py", "tests/test_one_validation.py", "templates/repository/standard/docs/engineering/harness/DRAFT_DEFINITIONS.md", "templates/repository/standard/docs/engineering/harness/DEFINITION_LINKS.md", "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md", "docs/notes/harnessctl-reference.md", "docs/notes/diagnostic-codes.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-002/"]
+++

# Implement and qualify standalone draft validation in the evaluator

## Objective

Deliver the evaluator correction in REQ-HAG-009: one read-only standalone draft
check, shared typed relations and the necessary regression/package evidence.
This work order is proposed implementation scope, not an already approved change.

## Proposed assurance classification

Propose `commit_bound_verification = "required"`: later hosted acceptance and
release decisions rely on changed validation code, relationship rules and
managed instructions. Record the accountable human's confirmation in the
assurance table before approval. No confirmation is inferred from draft authorship.

## In scope

The classifier, shared relation table, missing normal-validation refusals,
preflight reuse, CLI, documentation, meaningful tests, local candidate package
qualification and retained evidence specified by SPEC-HAG-004 and VER-HAG-002.
Use the existing parser, template source, catalog and package mechanisms.

## Out of scope

Hosted service/transaction implementation; amendments to the accepted hosted
definitions or evaluator pin; a public release/version selection; registry
publication, push, PR, merge or deployment; modifications to the private 0.22.0
governor; new authenticated decision mechanisms; fixing the separate legacy
decision-role/actual-human mismatch; historical artifact migrations.

## Authorized decision envelope

Upon package and work-order approval, Codex may select routine implementation
details within the named paths, run tests, retain evidence, make bounded local
commits, record implementation completion and prepare required verification.
Human verification acceptance, release, installation as governor and external
delivery remain separate decisions. Proposed commit-bound verification is
required; its human confirmation is not yet recorded in assurance.decided_by.

## Constraints and dependencies

Keep repository lifecycle evaluation on the selected released 0.22.0 environment.
Candidate testing uses disposable environments only. Preserve the original
approved HAG definitions, existing work and raw failed observations. No new
runtime dependency, storage system or lifecycle state is needed.

The accepted correction choice is mmzen's conversation response, "OK, i accept
your recommended correction". The attempt to record DEC-HAG-001 using that
actual human identity was refused with WEX201: the release expects the literal
engineering-owner label on WO-HAG-001. DEC-HAG-001 therefore remains open.
This limitation does not grant permission to substitute a role for the human,
alter approved ownership, or hand-write a disposition. It blocks the dependent
WO-HAG-001 transition, not preparation of this new bounded correction.

## Expected change surface

| Path | Reason |
| --- | --- |
| `se_harness/relation_policy.py` | New small shared relation contract; no external policy engine. |
| `se_harness/draft_validation.py` | Read-only selected-draft classification and structured result. |
| `se_harness/engine/validation_architecture.py` | Use the shared endpoint contract and enforce missing typed pairs. |
| `se_harness/engine/validation_evidence.py` | Reuse required-relation declarations and structured predicate detail. |
| `se_harness/engine/validation_core.py` | Structured field context only where needed for reliable classification. |
| `se_harness/engine/validation_lifecycle.py` | Reuse common metadata predicates; retain ordinary validation semantics. |
| `se_harness/engine/validation_authoring.py` | Reuse authoring findings without English-message filtering. |
| `se_harness/engine/validate_engineering_artifacts.py` | Connect shared validators without duplicating repository scans. |
| `se_harness/preflight.py` | Consume shared typed endpoints; retain selected governing-chain semantics. |
| `se_harness/cli.py` | Add the read-only command and its human/JSON rendering. |
| `se_harness/codes.py` | Allocate only necessary stable draft refusal codes without reusing codes. |
| `tests/test_draft_validation.py` | New independent admission, refusal, scope and no-write tests. |
| `tests/test_relation_policy.py` | New independent declared-pair and validation/preflight regression tests. |
| `tests/test_artifact_authoring.py` | Generated-template compatibility coverage. |
| `tests/test_authoring_gate.py` | Prove draft admissibility does not waive approval. |
| `tests/test_cli_shape.py` | Include the command in the existing parser/output contract. |
| `tests/test_validation_taxonomy.py` | Retain diagnostic-plane and code contracts if new structured details need coverage. |
| `tests/test_one_validation.py` | Preserve existing shared-validation behavior. |
| `templates/repository/standard/docs/engineering/harness/DRAFT_DEFINITIONS.md` | Document draft check and distinction from approval, as candidate released resources. |
| `templates/repository/standard/docs/engineering/harness/DEFINITION_LINKS.md` | Document shared typed-link evaluation and unchanged graph meaning. |
| `templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md` | Document exact draft incompleteness boundary; no new approval right. |
| `docs/notes/harnessctl-reference.md` | New command syntax, result and limitation examples. |
| `docs/notes/diagnostic-codes.md` | Regenerate the existing diagnostic index if codes are added. |
| `docs/engineering/hosted-artifact-graph/README.md` | Correction navigation and actual state. |
| `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-002/` | Durable test, inspection and package identity evidence. |

The new module paths are proposed destinations after inspecting their existing
callers and validation seams. Existing package discovery includes se_harness
modules; no version or pyproject change is currently needed. Existing test runner
discovers test_*.py; no CI, plugin, Memgraph, Docker or service change is needed.
Read the existing release-build recipe before a local distribution build and
retain generated archives outside tracked source. A future VREC and its exact
evaluator-evidence destinations are unresolved until the released preparation
command allocates them; assess its returned relationship-based scope then.

## Required verification

Run VER-HAG-002 EV-01 through EV-08 and the repository-required checks. Inspect
every changed behavior against the expected table, especially generated drafts,
mixed placeholder/invalid links, ambiguity, unaffected approval and package use.
No candidate test result can supply approval, human identity or release authority.

## Evidence to record

Use the declared WO-HAG-002 evidence directory. Retain exact commands, exit codes,
independent expected outcomes, package SHA-256/payload identity and the final
candidate. Preserve the original 0.22.0 probe and WEX201 failure under WO-HAG-001.

## Stop and escalate conditions

Stop the affected change if it needs a new policy interpretation, broader source
paths, an accepted-definition rewrite, weakened approval gates, historical graph
repair, extra dependencies or a governor/pin replacement. Report any inability
to preserve a trustworthy catalog or classify without broad error suppression.
No implicit decision-identity correction is part of this work order.

## Completion report format

Report implemented behavior, exact source/package checks and identities, retained
evidence, compatibility differences, unresolved limitations and the released
evaluator's actual current step. Preparing this draft does not start work or
claim that the hosted service can resume.
