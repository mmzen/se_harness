+++
id = "WO-RLS-010"
type = "work_order"
title = "Qualify the integrated se-harness 0.7.0 candidate"
status = "rejected"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

rejected_at = "2026-08-25T12:34:51Z"
rejected_by = "engineering-owner"
rejection_reason = "Rejected by the accountable engineering owner on 2026-08-25, atomically with REL-SEH-014, and superseded by WO-RLS-011. Nothing is wrong with this work order's authorized scope. Its exact aggregate scope section fixed a thirty-four-work-order census that WO-ADS-001 and WO-ADS-002 falsified when they reached main at 701e456, and the governing exact public 0.6.0 evaluator refuses an approved to approved transition (WEX201), so that census cannot be corrected in place. Rejecting it together with REL-SEH-014, which names it in gates, keeps the graph from ever holding an approved contract naming a rejected member. WO-RLS-011 carries the identical six declared execution-scope paths and the identical relations, deliberately naming no release contract, and defers its aggregate census to whatever REL-SEH-015 names in gates at its approval and to measurement at the candidate, so a further landing needs no further succession. No work was started under this work order: no start preflight was run, no version identity was moved, no distribution was built, and no candidate commit exists, so the successor inherits no partial state. This rejection is terminal and rewrites nothing: the approval recorded at 2026-08-25T11:53:28Z stands as history."
[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, managed-policy upgrade, recipe-bound build replay, credential-free publication, governor succession, and future evaluator decisions will rely on the exact integrated candidate, retained evidence, and reproducible distributions."
decided_by = "repository-owner"

[execution_scope]
paths = ["README.md", "pyproject.toml", "se_harness/__init__.py", "docs/notes/developing-se-harness.md", "docs/engineering/README.md", "docs/engineering/release-0-7-0/"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T11:53:28Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable owners on 2026-08-25, in the same decision that approved REL-SEH-014. This work order is the successor to WO-RLS-009, which was rejected because its amended aggregate scope was never approved and the governing exact public 0.6.0 evaluator refuses an approved to approved transition (WEX201). This is therefore the first approval that scope has ever received: 34 work orders, 19 verification contracts, 41 requirements, and 35 work-order-keyed evidence paths, being the 34 existing paths measured now plus the one this work order will retain at docs/engineering/release-0-7-0/evidence/WO-RLS-010-verification.md. Every figure was re-derived from the graph immediately before this transition rather than inherited from WO-RLS-009. The execution scope is the same six declared paths approved on 2026-08-25, including docs/engineering/README.md which the owner added by name: README.md, pyproject.toml, se_harness/__init__.py, docs/notes/developing-se-harness.md, docs/engineering/README.md, and docs/engineering/release-0-7-0/. Commit-bound verification stays classified required by repository-owner decision, not by default. Approval authorizes start preflight followed by only the declared versioning, integration, qualification, recipe-bound reproducible-build, index-maintenance, and retained-evidence work inside those six paths. It authorizes no candidate commit, no branch push, no VREC-SEH-013 or RLS-SEH-013 preparation or transition, no tag creation or movement, no GitHub or PyPI publication, no Pages deployment, no maintenance-line mutation, no credential use, no external policy change, and no root-evaluator upgrade. Work must stop after an implemented candidate and retained evidence unless later authority permits more. The work order set is fixed by REL-SEH-014 and must be re-measured against the candidate rather than carried forward from this reason."

[[lifecycle_events]]
from = "approved"
to = "rejected"
decided_at = "2026-08-25T12:34:51Z"
decided_by = "engineering-owner"
reason = "Rejected by the accountable engineering owner on 2026-08-25, atomically with REL-SEH-014, and superseded by WO-RLS-011. Nothing is wrong with this work order's authorized scope. Its exact aggregate scope section fixed a thirty-four-work-order census that WO-ADS-001 and WO-ADS-002 falsified when they reached main at 701e456, and the governing exact public 0.6.0 evaluator refuses an approved to approved transition (WEX201), so that census cannot be corrected in place. Rejecting it together with REL-SEH-014, which names it in gates, keeps the graph from ever holding an approved contract naming a rejected member. WO-RLS-011 carries the identical six declared execution-scope paths and the identical relations, deliberately naming no release contract, and defers its aggregate census to whatever REL-SEH-015 names in gates at its approval and to measurement at the candidate, so a further landing needs no further succession. No work was started under this work order: no start preflight was run, no version identity was moved, no distribution was built, and no candidate commit exists, so the successor inherits no partial state. This rejection is terminal and rewrites nothing: the approval recorded at 2026-08-25T11:53:28Z stands as history."
+++

# Work Order: Qualify the integrated se-harness 0.7.0 candidate

## Lifecycle

This work order requires the accountable owners' approval before start preflight
or any declared work. Its authoritative state, and the timestamp and reason of
every decision taken on it, are the front matter and `[[lifecycle_events]]`
above; read those rather than this prose. It is the successor to `WO-RLS-009`,
issued on 2026-08-25 under the governing contract `REL-SEH-014`.

On 2026-08-25, after reviewing the `v0.6.0`-to-`main` ledger, the proposed
public release content, the exact historical allow-list, the exclusions, and the
measured readiness state, the repository owner instructed `objective is to make
the 0.7.0 release, you can start the release process`, then `additional content
landed on main, can you refresh, and integrate the newly implemented work
orders`. Those instructions authorized deriving the ledger and drafting a
release packet for accountable review, and nothing else.

The owner then stated `I approve: REL-SEH-012 and WO-RLS-009, the
docs/engineering/README.md should be added to the scope. For WO-TCM-001 i accept
it, you can transition it to implemented`. That decision approved the
predecessor work order, added `docs/engineering/README.md` to the execution
scope as the sixth declared path, admitted `WO-TCM-001` to the release unit, and
authorized its `in_progress` to `implemented` transition, which the engineering
owner applied at 2026-08-25T10:21:06Z. The six declared paths carry forward to
this work order unchanged.

The owner then accepted `VREC-TCM-002` and authorized its transition to
`verified`, which the assurance owner applied at 2026-08-25T10:51:11Z, and
merged pull request #151 into `main` as a true merge at
`73b7b5437637bc2ac2d9af2c8c9295b4d4475d68`. `WO-TCM-001` therefore holds
verified coverage, subject to a disclosed limitation: the two independent
reviewer judgments `VER-TCM-001`'s manual-assessment section requires do not
exist, and the owner verified with that gap as accepted residual risk.

Resuming release work, the owner chose to reject `REL-SEH-012` and issue a
successor contract rather than amend an approved allow-list in place, and to
ship 0.7.0 without waiting for `WO-AEX-006` through `WO-AEX-008`. `WO-AEX-005`
had reached `implemented` ninety seconds after `REL-SEH-012` was approved and
its bytes are in the packaged surface, so it joined the release unit. The
aggregate scope below was measured accordingly at thirty-four work orders,
nineteen verification contracts, forty-one requirements, and thirty-five keyed
evidence paths. `REL-SEH-013` was drafted with that unit and approved at
2026-08-25T11:38:12Z.

`WO-RLS-009`'s amended aggregate scope was put to the owner in that same
decision and was not answered, so it was never approved. The governing exact
public 0.6.0 evaluator refuses an `approved` to `approved` transition
(`WEX201`), so no re-approval event could be recorded on `WO-RLS-009`.
Presented with three measured routes, the owner chose to reject `WO-RLS-009` and
issue this successor rather than record the re-approval in prose alone or revert
the amendment. Because `REL-SEH-013` named `WO-RLS-009` in `gates`, and an
approved allow-list is not widened or repaired in place, `REL-SEH-013` was
rejected in the same atomic transaction at 2026-08-25T11:47:44Z and
`REL-SEH-014` succeeds it with `WO-RLS-010` in `gates`. `WO-RLS-009`,
`REL-SEH-012`, and `REL-SEH-013` are all preserved as immutable rejected
history and none of their recorded lifecycle events was rewritten.

No work was started under `WO-RLS-009`. No start preflight was run, no version
identity was moved, no distribution was built, and no candidate commit exists,
so this successor inherits no partial state.

This work order declares `REQ-DST-006`, `SPEC-DST-001`, `ARCH-DST-001`,
`ADR-DST-001`, and `VER-DST-001` in its relations, and deliberately not a
release contract. A later contract succession therefore breaks no graph edge
that points at this work order.

Approval authorizes start preflight followed by only the declared versioning,
integration, qualification, reproducible-build, index-maintenance, and
retained-evidence work within the six declared execution-scope paths.

Approval explicitly does not authorize the candidate commit, `VREC-SEH-013` or
`RLS-SEH-013` preparation or transition, branch push, tag creation or movement,
GitHub or PyPI publication, Pages deployment, maintenance-line mutation,
credential use, external policy change, or root-evaluator upgrade.

Commit-bound verification is classified `required` because the release owner,
the assurance owner, consumers, publication automation, the recipe interpreter,
and future repository upgrades will rely on the exact integrated executable
package, standard template, evaluator boundary, provenance, and distribution
bytes. This classification is not inferred from a default.

## Objective

Produce one clean and fully qualified 0.7.0 candidate containing the
thirty-three selected historical work orders plus this release-integration work
order, with
consistent version identity, one standard installation, independently proven
evaluator, candidate-source, and candidate-package roles, recipe-bound
reproducible distributions, complete retained evidence, and exact aggregate
verification inputs. Stop after an implemented candidate and retained evidence
unless later authority permits the candidate commit and `VREC-SEH-013`
preparation.

## Exact aggregate scope

- Work orders (thirty-four): `WO-REB-008`, `WO-REB-009`, `WO-REB-010`,
  `WO-REB-011`, `WO-REB-012`, `WO-REB-013`, `WO-REB-014`, `WO-REB-015`,
  `WO-REB-016`, `WO-REB-017`, `WO-REB-018`, `WO-REB-019`, `WO-REB-020`,
  `WO-REB-021`, `WO-REB-022`, `WO-HUP-004`, `WO-HBI-001`, `WO-HBI-002`,
  `WO-HBI-003`, `WO-HBI-004`, `WO-AEX-001`, `WO-AEX-002`, `WO-AEX-003`,
  `WO-AEX-004`, `WO-AEX-005`, `WO-VSP-007`, `WO-LRE-001`, `WO-IPK-001`,
  `WO-RLO-004`, `WO-RLO-005`, `WO-WEX-003`, `WO-TCM-001`, `WO-TCM-002`, and
  `WO-RLS-010`.
- Verification contracts (nineteen): `VER-REB-006`, `VER-REB-007`,
  `VER-REB-008`, `VER-REB-009`, `VER-REB-010`, `VER-HUP-004`, `VER-HBI-001`,
  `VER-AEX-001`, `VER-AEX-002`, `VER-AEX-003`, `VER-AEX-004`, `VER-VSP-002`,
  `VER-LRE-001`, `VER-IPK-001`, `VER-RLO-004`, `VER-RLO-005`, `VER-WEX-003`,
  `VER-TCM-001`, and `VER-DST-001`.
- Requirements implemented by the release unit (forty-one): `REQ-REB-015`
  through `REQ-REB-026`, `REQ-HUP-008`, `REQ-HUP-009`, `REQ-HBI-001`,
  `REQ-HBI-002`, `REQ-AEX-001` through `REQ-AEX-006`, `REQ-AEX-008`,
  `REQ-AEX-009`, `REQ-AEX-010`, `REQ-VSP-008`, `REQ-LRE-001`, `REQ-LRE-002`,
  `REQ-IPK-001` through `REQ-IPK-003`, `REQ-RLO-013` through `REQ-RLO-016`,
  `REQ-WEX-011`, `REQ-TCM-001` through `REQ-TCM-004`, and `REQ-DST-006`.
  `REQ-TCM-002`, `REQ-TCM-003`, and `REQ-TCM-004` entered the union when
  `WO-TCM-001` was admitted; `REQ-TCM-001` was already present through
  `WO-TCM-002`. `REQ-AEX-010` entered when `WO-AEX-005` was admitted;
  `REQ-AEX-002` and `REQ-AEX-004`, its other two declared requirements, were
  already present through `WO-AEX-001` through `WO-AEX-004`.
- Existing keyed evidence (thirty-four paths under `docs/engineering/`):
  `released-evaluator-boundary/evidence/WO-REB-008-publication-view.md`,
  `released-evaluator-boundary/evidence/WO-REB-009-candidate-validator.md`,
  `released-evaluator-boundary/evidence/WO-REB-010-git-aware-candidate.md`,
  `released-evaluator-boundary/evidence/WO-REB-011-candidate-doctor-boundary.md`,
  `released-evaluator-boundary/evidence/WO-REB-012-build-toolchain.md`,
  `released-evaluator-boundary/evidence/WO-REB-013-retained-build-platform.md`,
  `released-evaluator-boundary/evidence/WO-REB-014-windows-bash-path.md`,
  `released-evaluator-boundary/evidence/WO-REB-015-windows-test-temp.md`,
  `released-evaluator-boundary/evidence/WO-REB-016-pages-generation-view.md`,
  `released-evaluator-boundary/evidence/WO-REB-017-pages-step-output.md`,
  `released-evaluator-boundary/evidence/WO-REB-018-governance-migration.md`,
  `released-evaluator-boundary/evidence/WO-REB-019-lifecycle-state-contract.md`,
  `released-evaluator-boundary/evidence/WO-REB-020-role-specific-qualification.md`,
  `released-evaluator-boundary/evidence/WO-REB-021-entry-point-safety.md`,
  `released-evaluator-boundary/evidence/WO-REB-022-junction-predicate-capability.md`,
  `repository-harness-upgrade/evidence/WO-HUP-004-verification.md`,
  `hash-bound-integrity/evidence/WO-HBI-001-verification.md`,
  `hash-bound-integrity/evidence/WO-HBI-002-verification.md`,
  `hash-bound-integrity/evidence/WO-HBI-003-verification.md`,
  `hash-bound-integrity/evidence/WO-HBI-004-implementation.md`,
  `hash-bound-integrity/evidence/WO-HBI-004-verification.md`,
  `agentic-execution/evidence/WO-AEX-001-verification.md`,
  `agentic-execution/evidence/WO-AEX-002-verification.md`,
  `agentic-execution/evidence/WO-AEX-003-verification.md`,
  `agentic-execution/evidence/WO-AEX-004-verification.md`,
  `agentic-execution/evidence/WO-AEX-005-verification.md`,
  `verification-supersession/evidence/WO-VSP-007-verification.md`,
  `legacy-release-evidence/evidence/WO-LRE-001-implementation.md`,
  `integration-package/evidence/WO-IPK-001-verification.md`,
  `release-orchestration/evidence/WO-RLO-004-verification.md`,
  `release-orchestration/evidence/WO-RLO-005-implementation.md`,
  `release-orchestration/evidence/WO-RLO-005-verification.md`,
  `workflow-execution/evidence/WO-WEX-003-verification.md`, and
  `technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md`.
  The last path is a combined-evidence file that the directory-position
  attribution rule keys to both `WO-TCM-001` and `WO-TCM-002`; it is counted
  once.
- New evidence after approved execution:
  `docs/engineering/release-0-7-0/evidence/WO-RLS-010-verification.md`.
- Planned aggregate VREC after an authorized clean candidate commit:
  `docs/engineering/release-0-7-0/verification-records/VREC-SEH-013.md`.
- Planned release record after verified assurance and separate
  release-preparation authority:
  `docs/engineering/release-0-7-0/releases/RLS-SEH-013.md`.
- Proposed public version and immutable tag: `0.7.0` and `v0.7.0`.

The work-order set is fixed by `REL-SEH-014`. Historical VRECs support lineage
and evidence discovery but bind different commits and do not replace the new
candidate-bound aggregate VREC.

## In scope

After separate approval of `REL-SEH-014` and this work order:

- Reconfirm the `v0.6.0...candidate` ledger from the candidate itself and retain
  the exact inclusion and exclusion rationale, including the two classification
  calls `REL-SEH-014` puts to the release owner, the recorded admission and
  transition of `WO-TCM-001`, and the admission of `WO-AEX-005` with the fact
  that its four new runtime modules are unreachable from `se_harness/cli.py` and
  therefore inert in 0.7.0.
- Confirm before any build that `WO-TCM-001` and `WO-AEX-005` both read
  `implemented` in the candidate tree and that this work order's aggregate scope
  matches the `REL-SEH-014` allow-list exactly. Stop if either does not hold.
- Confirm before aggregate capture that `WO-TCM-001`'s assurance route was
  decided by the assurance owner, and record which route was taken. Measured on
  2026-08-25: route two, verify with the missing manual-assessment judgments
  disclosed as accepted residual risk. Re-read `VREC-TCM-002` at the candidate
  rather than carrying that forward, and stop if the record's state differs.
- Add `release-0-7-0/` to the repository-owned engineering domain index at
  `docs/engineering/README.md`, as that index's own maintenance rule requires
  when a domain is added. Record whether the standing absence of `release-0-6-0/`
  is corrected in the same edit or left to its own decision, and change nothing
  else in that file.
- Set candidate product identity to 0.7.0 in `pyproject.toml`,
  `se_harness/__init__.py`, and the current public installation example in
  `README.md`.
- Update `docs/notes/developing-se-harness.md` so it names candidate 0.7.0 as
  the current candidate version while continuing to name the exact root
  evaluator version recorded in `.engineering-harness.toml`. Both identities are
  required by the existing documentation contract; neither may replace the
  other.
- Preserve historical 0.5.0, 0.5.0a1, and 0.6.0 incident, evaluator, recovery,
  bootstrap, test-fixture, and governance references whose meaning is not the
  current candidate version.
- Preserve the root `.engineering-harness.toml`, `.engineering-harness.lock`,
  `ENGINEERING_HARNESS.md`, and managed `.github/workflows/engineering-harness.yml`
  as the exact released 0.6.0 installation until a later, separately authorized
  post-publication upgrade.
- Reconcile candidate package data and standard-template parity for workflow and
  quality-gate JSON, evaluator identity, hash-bound class declarations, Git
  attributes, mutation guards, agent and skill contracts, the managed
  technical-communication policy and its router row, all five installed skills,
  recovery, authoring, provenance, CLI, validator, Explorer, and documentation
  surfaces.
- Run formal graph, release-distribution, managed-integrity, identity, byte-rule
  inventory, workflow, CLI, package-surface, archive-safety, reproducibility,
  Explorer, recovery, and full supported-runtime verification.
- Exercise the five `qualify` operations from the candidate in their applicable
  roles and record the boundary refusals of the operations that do not apply to
  a candidate root, together with the released-evaluator observations that stand
  in for them.
- Under explicit build authority granted by later approval of this work order,
  replay the recipe-bound build twice from exact exported candidate source at
  one epoch through `repository_tools.release_build replay` and prove byte
  identity, safe archives, and reconstruction equivalence.
- Produce the release bundle manifest with
  `scripts/create_release_bundle_manifest.py` bound to the candidate's own
  `release/build-recipe.json`, and record the manifest identities the later
  schema-2 distribution binding will consume.
- Install the exact candidate wheel in fresh isolated environments and run
  verifier-owned black-box acceptance without checkout import fallback, on both
  supported runner platforms where the existing contracts require it.
- Retain exact commands, outcomes, identities, hashes, manifests, changed-path
  ledger, warnings, deviations, residual risks, and unperformed actions in the
  keyed release evidence.
- Transition only this work order through its authorized implementation
  lifecycle. Candidate commit, aggregate capture, verification, release
  preparation, release, and external actions remain separate stages.

## Out of scope

- Adding product behavior or admitting another work order without an accountable
  succession of `REL-SEH-014`. An approved allow-list is not widened in place;
  `REL-SEH-012` was rejected and re-issued precisely for that reason.
- Capturing, preparing, or verifying a commit-bound record for `WO-TCM-001`. Its
  `in_progress` to `implemented` transition was separately authorized by the owner
  and applied on 2026-08-25T10:21:06Z; its verified coverage is an assurance-owner
  decision that approving this work order does not grant and that may not be
  inferred from the fact that its bytes are already on `main`.
- Committing `WO-TCM-001`'s applied lifecycle transition. That governance commit
  is its own authorization, separate from this work order's execution.
- Treating `WO-HUP-002`, merge-only commits, VREC preparation or supersession
  bookkeeping, or governance transitions as release-bearing product work.
- Answering the open `build_recipe_sha256` hash-bound-class question recorded in
  issue #142, or changing `unbound_digest_fields`.
- Updating the root evaluator, root lock, or managed root to candidate 0.7.0
  before the exact 0.7.0 release is published and a separate upgrade packet is
  approved.
- Bumping the pinned `se-harness==0.6.0` evaluator instruction carried in the
  owner region of `AGENTS.md` and the repository-owned release sequences; the
  governing evaluator does not change during this candidate.
- Removing the independent package lane's documented `accept-candidate`
  bootstrap exception, which exact public 0.6.0 still requires.
- Rewriting historical VREC, RLS, evidence, release, tag, incident, publication,
  or evaluator facts.
- Using candidate source or an editable or contaminated install as the root
  evaluator or independent verifier.
- Weakening mutation guards, path safety, transactional rollback, evidence
  binding, workflow gates, archive checks, reproducibility, byte rules, or
  authority boundaries to obtain a pass.
- Preparing or transitioning `VREC-SEH-013` before one separately authorized
  clean candidate commit.
- Preparing or transitioning `RLS-SEH-013`, or binding its distribution table,
  before verified aggregate assurance and separate release-preparation
  authority.
- Merge, branch push, tag, GitHub Release, PyPI publication, Pages deployment,
  maintenance-line mutation, credential use, external policy change, force
  push, or history rewrite.

## Authorized decision envelope

After separate approval, the implementation agent may choose deterministic
temporary directories outside the checkout, the candidate epoch, the
evidence-table layout, safe mechanical version edits within the five declared
paths, and test helpers required by existing contracts. It may not reinterpret
the allow-list, change accepted product behavior, widen changed paths, add
dependencies or build profiles, alter the root evaluator identity or lock,
decide historical VREC disposition, make accountable transitions, or perform
external release actions. Uncertainty escalates rather than resolving into a
local default.

## Constraints

- Use Python 3.11+ standard-library runtime behavior and retain no runtime
  dependencies.
- Keep exactly one standard installation and preserve owner content outside
  managed markers.
- Treat every repository, filesystem, Git, archive, event, recipe, lock, policy,
  and evidence input as untrusted.
- Use the exact independently installed released 0.6.0 evaluator, outside the
  checkout and in isolated mode, for root doctor, preflight, validation, and any
  authorized root lifecycle mutation during this candidate.
- Keep candidate-source and candidate-package evidence separately identified and
  non-authoritative.
- Label every platform-dependent figure with the platform that produced it. A
  green Windows reading is not a statement about the hosted Linux lane, and the
  reverse also holds.
- Write evidence JSON with LF endings as the managed `.gitattributes` rule
  requires, and do not disturb the owner-region byte rules that
  `WO-HBI-003` and `WO-HBI-004` established.
- Preserve the complete selected work-order, requirement, and
  verification-contract unions; do not infer scope from commits or dates.
- Make no candidate mutation after exact-commit replay or aggregate capture.
- Preserve unrelated user changes and stop if the reviewed packet or candidate
  changes underneath execution.

## Expected change surface

- `pyproject.toml`, `se_harness/__init__.py`, and the current install-version
  example in `README.md`.
- The current-candidate-version statements in
  `docs/notes/developing-se-harness.md`.
- One domain-list addition in `docs/engineering/README.md`, and no other change to
  that repository-owned index.
- `docs/engineering/release-0-7-0/` for the approved contract, this work order,
  the domain index, the retained evidence, and later separately prepared
  records.
- Derived build, test, acceptance, replay, and dashboard output only in bounded
  disposable locations outside formal artifact discovery.
- No root evaluator, root lock, managed root policy, publication credential, or
  external state change.

## Required verification

- Released-0.6.0 start and review preflight, doctor, formal graph validation,
  inspection, and Explorer observations, all from outside the checkout in
  isolated mode.
- No structure, governance, or policy errors. Maintenance warnings are retained
  with their measured count and explicitly dispositioned.
- Complete supported-runtime suites, including Python 3.11, with exact counts
  and only explained conditional skips. Windows platform-guard skips are
  expected; the hosted Linux lane is expected to run the same suite without
  them.
- Candidate-source identity from the exact candidate checkout, with distribution
  metadata resolving within the checkout as required.
- Candidate-package identity and verifier-owned black-box acceptance from a
  fresh exact-wheel installation outside the checkout.
- Released-evaluator identity and isolation with no candidate or editable import
  fallback.
- Exact version inventory: current candidate-bearing surfaces equal 0.7.0 while
  historical and root-evaluator identities remain truthful, including the
  documentation contract's simultaneous 0.7.0 candidate and 0.6.0 evaluator
  statements.
- Exact package and template parity, payload manifest, wheel archive identity,
  mutation-guard coverage, hash-bound class completeness, byte-rule inventory
  coverage, workflow and gate contract parity, and active-surface retired-role
  checks.
- Doctor, init, adopt, validate, focus, check, transition plan, inspect,
  dashboard, upgrade plan and refusal, artifact authoring, renumber plan and
  refusal, verification-capture refusal and success boundary,
  release-preparation refusal and success boundary, `qualify` operation
  boundaries, `migrate` rehearsal, and recovery rehearsal scenarios.
- Governor-succession assessment proving the released 0.6.0 evaluator governs
  the 0.7.0 candidate root without a version-specific exception.
- Credential-free publication rehearsal on both runner platforms with no
  credential present and no external write attempted.
- Deterministic Explorer generation within the declared resource budgets.
- Two recipe-bound replays produce byte-identical wheels and normalized sdists
  at one epoch; archives are safe and equivalent; the reconstructed wheel equals
  the direct wheels and passes fresh Python 3.11 operation.
- Release-distribution bundle manifest, checksums, source manifest, candidate
  commit, tree and epoch, Git ancestry, changed-path ledger, protected-control
  diff, secret and private-path scan, and `git diff --check` pass.
- Aggregate VREC inputs contain exactly the approved `REL-SEH-014` work-order
  set, its verification contracts, its keyed evidence paths, one clean candidate
  commit, one artifact snapshot, and matching evaluator evidence: thirty-four
  work orders, nineteen verification contracts, and thirty-five keyed evidence
  paths. Re-measure all three against the candidate rather than carrying these
  figures forward.
- The engineering domain index names `release-0-7-0/`.

## Evidence to record

Retain preliminary working-tree checks and later exact-candidate replay
separately at
`docs/engineering/release-0-7-0/evidence/WO-RLS-010-verification.md`. Record the
baseline and candidate commit, tree and epoch; the complete allow-list and
exclusions with the two classification calls as decided; the version inventory;
the released-evaluator payload, archive and origin; the candidate source and
package origins; commands and exit results; test counts per platform; graph
planes; inspection queues; Explorer manifests and byte budgets; changed paths;
managed-root integrity; recipe identity and both replay hash sets;
reproducibility; the acceptance manifest; the bundle manifest identities; hosted
run, job and artifact identities; warnings; deviations; residual risks; and every
unperformed transition or external action.

## Stop and escalate conditions

Stop on packet or scope change, a work order whose bytes are in the packaged
surface and which the contract does not name or which holds no verified coverage
at aggregate capture, missing keyed evidence, an unresolved historical
`ready` record, an invalid graph, failed preflight, version drift, root
evaluator or lock change, candidate contamination, cross-role import, unsafe
path or archive, incomplete mutation or byte-rule coverage, a failed required
check, an unexplained warning, nondeterminism between the two replays, package
or template divergence, candidate mutation after exact evidence, a hosted lane
that does not run on the expected event, or a need for authority beyond the
approved stage.

## Completion report format

Report the approved work-order scope and exclusions; `WO-TCM-001`'s state and the
assurance route taken; the baseline and candidate identity; the version inventory;
the engineering index edit; evaluator, source and package
origins; root integrity; exact commands and test results with their platforms;
graph planes and warnings; workflow and gate, mutation, byte-rule, governor
succession, publication rehearsal, recovery, Explorer, package, archive and
reproducibility results; hashes and manifests; the evidence path; the planned
aggregate VREC inputs; deviations and residual risks; and every unperformed
commit, push, verification transition, release preparation and transition,
merge, tag, publication, deployment, maintenance-line, credential, and
root-upgrade action.
