+++
id = "WO-RLS-008"
type = "work_order"
title = "Qualify the integrated se-harness 0.6.0 candidate"
status = "in_progress"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, managed-policy upgrade, workflow execution, mutation safety, public publication, and future evaluator decisions will rely on the exact integrated candidate, retained evidence, and reproducible distributions."
decided_by = "repository-owner"

[execution_scope]
paths = ["README.md", "pyproject.toml", "se_harness/__init__.py", "docs/notes/developing-se-harness.md", "docs/engineering/release-0-6-0/"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T13:48:00Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-21T13:49:23Z"
decided_by = "engineering-owner"
+++

# Work Order: Qualify the integrated se-harness 0.6.0 candidate

## Lifecycle

On 2026-08-21, after reviewing the `v0.5.0`-to-`main` ledger, proposed public release content, exact seven-work-order product scope, exclusions, and release-readiness gaps, the repository owner instructed `ok, launch the release process`. That instruction authorizes creation and completion of `REL-SEH-007` and this draft work order for review.

After reviewing the completed packet, the accountable owner stated `I approve REL-SEH-007 and WO-RLS-008 for bounded 0.6.0 versioning, integration, qualification, reproducible distribution builds, and retained evidence under their exact eight-work-order scope.` That decision transitions this work order to `approved` and authorizes start preflight followed by only the declared versioning, integration, qualification, reproducible build, and retained-evidence work.

The approval explicitly does not authorize the candidate commit, VREC or RLS preparation or transitions, tag creation or movement, GitHub or PyPI publication, Pages deployment, maintenance-line mutation, credential use, external policy change, or root-evaluator upgrade.

After preliminary qualification found that the existing documentation contract requires the current candidate version in `docs/notes/developing-se-harness.md`, the accountable owner amended this work order to add only that path and authorized the bounded 0.6.0 current-version correction. The same instruction separately authorized an assurance owner to review and explicitly disposition only `VREC-WEX-001`, `VREC-WEX-002`, and `VREC-WEX-003`; those governance decisions are isolated under `WO-VSP-006` and do not enter this release work order's execution scope or eight-work-order release-bearing allow-list.

Commit-bound verification is classified `required` because the release owner, assurance owner, consumers, publication automation, and future repository upgrades will rely on the exact integrated executable package, standard template, evaluator boundary, provenance, and distribution bytes.

Start preflight passed on 2026-08-21 with the isolated public 0.5.0 evaluator, and the implementation actor read every file in its 15-file manifest before changing candidate identity. The `in_progress` status records execution within the approved scope only and grants none of the excluded authorities.


## Objective

Produce one clean and fully qualified 0.6.0 candidate containing the seven selected historical product work orders plus this release-integration work order, with consistent version identity, one standard installation, independently proven evaluator/source/package roles, reproducible distributions, complete retained evidence, and exact aggregate verification inputs. Stop after an implemented candidate and retained evidence unless later authority permits the candidate commit and `VREC-SEH-008` preparation.

## Exact aggregate scope

- Work orders: `WO-DST-019`, `WO-DST-020`, `WO-WEX-001`, `WO-WEX-002`, `WO-REB-001`, `WO-REB-002`, `WO-REB-003`, and `WO-RLS-008`.
- Verification contracts: `VER-DST-001`, `VER-DST-019`, `VER-DST-020`, `VER-WEX-001`, `VER-WEX-002`, and `VER-REB-001`.
- Existing keyed evidence: `docs/engineering/harness-distribution/evidence/WO-DST-019-verification.md`, `docs/engineering/harness-distribution/evidence/WO-DST-020-verification.md`, `docs/engineering/workflow-execution/evidence/WO-WEX-001-verification.md`, `docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md`, `docs/engineering/released-evaluator-boundary/evidence/WO-REB-001-implementation.md`, `docs/engineering/released-evaluator-boundary/evidence/WO-REB-002-implementation.md`, and `docs/engineering/released-evaluator-boundary/evidence/WO-REB-003-verification.md`.
- New evidence after approved execution: `docs/engineering/release-0-6-0/evidence/WO-RLS-008-verification.md`.
- Planned aggregate VREC after an authorized clean candidate commit: `docs/engineering/release-0-6-0/verification-records/VREC-SEH-008.md`.
- Planned release record after verified assurance and separate release-preparation authority: `docs/engineering/release-0-6-0/releases/RLS-SEH-008.md`.
- Proposed public version and immutable tag: `0.6.0` and `v0.6.0`.

The work-order set is fixed by `REL-SEH-007`. Historical VRECs support lineage and evidence discovery but bind different commits and do not replace the new candidate-bound aggregate VREC.

## In scope

After separate approval of this contract and work order:

- Reconfirm the `v0.5.0...candidate` ledger and retain the exact inclusion/exclusion rationale.
- Explicitly disposition the three historical ready WEX records through separately accountable supersession decisions before final candidate qualification.
- Set candidate product identity to 0.6.0 in `pyproject.toml`, `se_harness/__init__.py`, and current public installation examples in `README.md`.
- Preserve historical 0.5.0 and 0.5.0a1 incident, evaluator, recovery, test-fixture, and governance references whose meaning is not the current candidate version.
- Preserve the root `.engineering-harness.toml`, `.engineering-harness.lock`, `ENGINEERING_HARNESS.md`, and managed `.github/workflows/engineering-harness.yml` as the exact released 0.5.0 installation until a later, separately authorized post-publication upgrade.
- Reconcile candidate package data and standard-template parity for workflow and quality-gate JSON, evaluator identity, Git attributes, mutation guards, recovery, authoring, provenance, CLI, validator, Explorer, and documentation surfaces.
- Correct or explicitly disposition the observed candidate-source origin and Windows CRLF/LF test failures within approved scope; stop if correction requires product behavior beyond release integration.
- Run formal graph, release-distribution, managed-integrity, identity, workflow, CLI, package-surface, archive-safety, reproducibility, Explorer, recovery, and full supported-runtime verification.
- Under explicit build authority granted by later approval of this work order, build two promotable wheels and normalized sdists from exact exported candidate source at one epoch and prove byte identity, safe archives, and reconstruction equivalence.
- Install the exact candidate wheel in fresh isolated environments and run verifier-owned black-box acceptance without checkout import fallback.
- Retain exact commands, outcomes, identities, hashes, manifests, changed-path ledger, warnings, deviations, residual risks, and unperformed actions in the keyed release evidence.
- Transition only this work order through its authorized implementation lifecycle. Candidate commit, aggregate capture, verification, release preparation, release, and external actions remain separate stages.

## Out of scope

- Adding product behavior or admitting another work order without accountable amendment of `REL-SEH-007`.
- Treating `WO-HUP-001`, `WO-RCA-001`, emergency publication history, merge-only commits, or governance transitions as release-bearing product work.
- Updating the root evaluator, root lock, or managed root to candidate 0.6.0 before the exact 0.6.0 release is published and a separate upgrade packet is approved.
- Rewriting historical VREC, RLS, evidence, release, tag, incident, publication, or evaluator facts.
- Using candidate source or an editable/contaminated install as the root evaluator or independent verifier.
- Weakening mutation guards, path safety, transactional rollback, evidence binding, workflow gates, archive checks, reproducibility, or authority boundaries to obtain a pass.
- Preparing or transitioning `VREC-SEH-008` before one separately authorized clean candidate commit.
- Preparing or transitioning `RLS-SEH-008` before verified aggregate assurance and separate release-preparation authority.
- Merge, tag, GitHub Release, PyPI publication, Pages deployment, maintenance-line mutation, credential use, external policy changes, force push, or history rewrite.

## Authorized decision envelope

After separate approval, the implementation agent may choose deterministic temporary directories, the candidate epoch, evidence-table layout, safe mechanical version edits within declared scope, and test helpers required by existing contracts. It may not reinterpret the allow-list, change accepted product behavior, widen changed paths, add dependencies or profiles, alter the root evaluator identity, decide historical VREC supersession, make accountable transitions, or perform external release actions.

## Constraints

- Use Python 3.11+ standard-library runtime behavior and retain no runtime dependencies.
- Keep exactly one standard installation and preserve owner content outside managed markers.
- Treat every repository, filesystem, Git, archive, event, policy, and evidence input as untrusted.
- Use the exact independently installed released 0.5.0 evaluator for root doctor, preflight, validation, and any authorized root lifecycle mutation during this candidate.
- Keep candidate-source and candidate-package evidence separately identified and non-authoritative.
- Preserve the complete selected work-order and verification-contract unions; do not infer scope from commits or dates.
- Make no candidate mutation after exact-commit replay or aggregate capture.
- Preserve unrelated user changes and stop if the reviewed packet or candidate changes underneath execution.

## Expected change surface

- `pyproject.toml`, `se_harness/__init__.py`, and the current install-version example in `README.md`.
- `docs/engineering/release-0-6-0/` for the approved contract, work order, retained evidence, and later separately prepared records.
- Derived build, test, acceptance, and dashboard output only in bounded disposable locations outside formal artifact discovery.
- No root evaluator, root lock, managed root policy, publication credential, or external state change.

## Required verification

- Released-0.5.0 start and review preflight, doctor, formal graph validation, inspection, and Explorer observations.
- No structure, governance, or policy errors or warnings; maintenance warnings are retained and explicitly dispositioned.
- Complete supported-runtime suites, including Python 3.11, with exact counts and only explained conditional skips.
- Candidate-source identity from the exact candidate checkout, with distribution metadata resolving within the checkout as required.
- Candidate-package identity and verifier-owned black-box acceptance from a fresh exact-wheel installation outside the checkout.
- Released-evaluator identity and isolation with no candidate or editable import fallback.
- Exact version inventory: current candidate-bearing surfaces equal 0.6.0 while historical and root-evaluator identities remain truthful.
- Exact package/template parity, payload manifest, wheel archive identity, mutation-guard coverage, workflow/gate contract parity, and active-surface retired-role checks.
- Doctor, init, adopt, validate, focus, check, transition plan, inspect, dashboard, upgrade plan/refusal, artifact authoring, renumber plan/refusal, verification capture refusal/success boundary, release preparation refusal/success boundary, and recovery rehearsal scenarios.
- Deterministic Explorer generation with the exact 2 MiB topology ceiling and unchanged other resource budgets.
- Two direct wheels and normalized sdists are reproducible at one epoch; archives are safe and equivalent; the reconstructed wheel equals direct wheels and passes fresh Python 3.11 operation.
- Release-distribution bundle manifest, checksums, source manifest, candidate commit/tree/epoch, Git ancestry, changed-path ledger, protected-control diff, secret/private-path scan, and `git diff --check` pass.
- Aggregate VREC inputs contain exactly eight work orders, six verification contracts, eight keyed evidence paths, one clean candidate commit, one artifact snapshot, and matching evaluator evidence.

## Evidence to record

Retain preliminary working-tree checks and later exact-candidate replay separately at `docs/engineering/release-0-6-0/evidence/WO-RLS-008-verification.md`. Record the baseline and candidate commit/tree/epoch, complete allow-list and exclusions, version inventory, released-evaluator payload/archive/origin, candidate source/package origins, commands and exit results, test counts, graph planes, inspection queues, Explorer manifests and byte budgets, changed paths, managed-root integrity, build and archive hashes, reproducibility, acceptance manifest, hosted CI, warnings, deviations, residual risks, and every unperformed transition or external action.

## Stop and escalate conditions

Stop on packet or scope change, missing keyed evidence, unresolved historical ready records, invalid graph, failed preflight, version drift, root evaluator or lock change, candidate contamination, cross-role import, unsafe path or archive, incomplete mutation coverage, failed required check, unexplained warning, nondeterminism, package/template divergence, candidate mutation after exact evidence, or need for authority beyond the approved stage.

## Completion report format

Report the eight-work-order scope and exclusions; baseline and candidate identity; version inventory; evaluator/source/package origins; root integrity; exact commands and test results; graph planes and warnings; workflow/gate, mutation, recovery, Explorer, package, archive, and reproducibility results; hashes and manifests; evidence path; planned aggregate VREC inputs; deviations and residual risks; and every unperformed commit, verification transition, release preparation/transition, merge, tag, publication, deployment, maintenance-line, credential, and root-upgrade action.
