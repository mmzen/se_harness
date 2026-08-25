+++
id = "WO-RLS-011"
type = "work_order"
title = "Qualify the integrated se-harness 0.7.0 candidate"
status = "implemented"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, managed-policy upgrade, recipe-bound build replay, credential-free publication, governor succession, and future evaluator decisions will rely on the exact integrated candidate, retained evidence, and reproducible distributions."
decided_by = "repository-owner"

[execution_scope]
paths = ["README.md", "pyproject.toml", "se_harness/__init__.py", "docs/notes/developing-se-harness.md", "docs/engineering/README.md", "docs/engineering/release-0-7-0/", "tests/test_release_qualification.py"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T12:35:00Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-25, as a decision distinct from the rejection of WO-RLS-010 and separate from any decision on REL-SEH-015, which the owner has deliberately left in draft until immediately before the candidate commit. Approval authorizes start preflight and then only the declared versioning, integration, qualification, recipe-bound reproducible-build, index-maintenance and retained-evidence work inside the six declared execution-scope paths: README.md, pyproject.toml, se_harness/__init__.py, docs/notes/developing-se-harness.md, docs/engineering/README.md and docs/engineering/release-0-7-0/. It fixes no census: the release unit is exactly what REL-SEH-015 names in gates at its approval, and every derived aggregate is re-measured at the candidate, which is why this work order can survive a further landing without being re-issued. Measured immediately before this transition over merged branch state 5acccdebac50f1fe2bbeca9774c9ad110bac6c91 carrying main 701e456: thirty-five historical members implemented with verified coverage and zero uncovered; twenty-one verification contracts, a forty-eight-requirement union and thirty-seven keyed evidence paths on the whole-gates basis; validate PASS at 887 artifacts with 0 errors and 50 maintenance warnings; doctor 87 PASS, 0 FAIL. Two human assessment gaps are carried as disclosed accepted residual risk, VER-TCM-001's two reviewer judgments and VER-ADS-001's Scenario 8 classifications, and this work order must report both rather than imply clean coverage. Approval authorizes no contract approval, no candidate commit, no VREC-SEH-013 or RLS-SEH-013 work, no tag, no publication, no deployment, no maintenance-line mutation, no credential use and no root-evaluator upgrade. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-25T13:29:18Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-25, taken after the governance packet reached main. Start preflight PASS at phase start over clean branch state 826c72cfdaa3401cccf06c67943c5315221c3f72, the true merge of pull request 154, run with the governing exact public 0.6.0 evaluator outside the checkout; commit-bound verification is required and decided by the repository owner. REL-SEH-015 is approved, so the thirty-six-work-order allow-list in its gates array is fixed authority and this work order's deferred aggregate census resolves to it: twenty-one verification contracts, a forty-eight-requirement union and thirty-seven keyed evidence paths on the whole-gates basis, which is the basis VREC-SEH-013 must match. Two consequences of that freeze bind this work: keeping the contract's gates current in place is no longer available, so a work order reaching implemented with bytes in the packaged surface during this work is a stop condition to report rather than an edit; and WO-AEX-006's exclusion is a branch-point boundary that this work order must confirm at the candidate, the owner having decided to hold open pull request 155 until 0.7.0 is tagged. Bounded to the six declared execution-scope paths. This start authorizes no candidate commit, no promotable build beyond the declared recipe-bound reproducibility work, no VREC-SEH-013 or RLS-SEH-013 preparation or transition, no tag, no publication, no Pages deployment, no maintenance-line mutation, no credential use and no root-evaluator change."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-25T18:43:37Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-08-25 under DR-WO-COMPLETE, on the handoff gate reading Completed for WO-RLS-011 over candidate commit f76da5727e86fc53375bfa5cafcfcbf168c7456e, tree 52fdae8c6e090f62341df8b87c52fc308d5132f7, change set asserted complete over the eight declared paths of the amended execution scope. Exact-candidate readings, governing exact public 0.6.0 evaluator outside the checkout in isolated mode: validate PASS at 887 artifacts, 0 errors, 50 pre-existing maintenance warnings, every plane E0; inspect 167 findings at 0 errors and 64 warnings; doctor 87 PASS 0 FAIL; review preflight PASS; managed-root upgrade plan 36 files 36 unchanged; release-distribution validation PASS; portable release surface PASS; governor-succession plan PASS with transition required false, so the released 0.6.0 evaluator governs the 0.7.0 candidate without succession; verifier-owned black-box acceptance of an ephemeral non-promotable 0.7.0 wheel passed all ten scenarios against verifier 0.6.0; recovery rehearsal PASS; Explorer generation deterministic over two runs at 1037 files; qualify complete-candidate PASS on four checks; byte-rule inventory 57 declared paths at zero carriage returns. Census re-derived from the approved gates array here is unchanged from approval: 36 unique entries, zero uncovered, 21 verification contracts, a 48-requirement union, 37 keyed evidence paths. Credential-free publication rehearsal on Windows: REHEARSED on CPython 3.14.6 with the suite green at 1002 tests, FAILED on CPython 3.11.9 solely on the two pre-existing teardown tests routed to WO-RLO-006; both runtimes built 0.7.0 twice byte-identically and the divergence seam read EXACT. No digest measured on this workstation is bindable: the normalized digest differs by interpreter. This authorizes no further act."
+++

# Work Order: Qualify the integrated se-harness 0.7.0 candidate

## Lifecycle

This work order requires the accountable owners' approval before start preflight
or any declared work. Its authoritative state, and the timestamp and reason of
every decision taken on it, are the front matter and `[[lifecycle_events]]`
above; read those rather than this prose. It is the second successor in this
release, issued on 2026-08-25 after `WO-RLS-009` and `WO-RLS-010`, and it is
governed by `REL-SEH-015`.

On 2026-08-25, after reviewing the `v0.6.0`-to-`main` ledger, the proposed public
release content, the exact historical allow-list, the exclusions, and the
measured readiness state, the repository owner instructed `objective is to make
the 0.7.0 release, you can start the release process`, then `additional content
landed on main, can you refresh, and integrate the newly implemented work
orders`. Those instructions authorized deriving the ledger and drafting a release
packet for accountable review, and nothing else.

The owner then stated `I approve: REL-SEH-012 and WO-RLS-009, the
docs/engineering/README.md should be added to the scope. For WO-TCM-001 i accept
it, you can transition it to implemented`. That decision approved the first
release work order, added `docs/engineering/README.md` to the execution scope as
the sixth declared path, admitted `WO-TCM-001` to the release unit, and
authorized its `in_progress` to `implemented` transition, which the engineering
owner applied at 2026-08-25T10:21:06Z. The six declared paths carry forward to
this work order unchanged, and no path has been added or removed since.

The owner then accepted `VREC-TCM-002` and authorized its transition to
`verified`, which the assurance owner applied at 2026-08-25T10:51:11Z, and merged
pull request #151 into `main` as a true merge at
`73b7b5437637bc2ac2d9af2c8c9295b4d4475d68`. `WO-TCM-001` therefore holds verified
coverage, subject to a disclosed limitation: the two independent reviewer
judgments `VER-TCM-001`'s manual-assessment section requires do not exist, and
the owner verified with that gap as accepted residual risk.

Three contract successions have happened, all for the same reason, and this work
order is shaped by that history.

`REL-SEH-012` was approved at 2026-08-25T10:28:10Z. `WO-AEX-005` reached
`implemented` at 2026-08-25T10:29:40Z, ninety seconds later. The owner chose to
reject and re-issue rather than widen an approved allow-list in place, and to
ship 0.7.0 without waiting for `WO-AEX-006` through `WO-AEX-008`. `REL-SEH-013`
carried the corrected unit and was approved at 2026-08-25T11:38:12Z.

`WO-RLS-009`'s amended aggregate scope was put to the owner in that same decision
and was not answered, so it was never approved. The governing exact public 0.6.0
evaluator refuses an `approved` to `approved` transition (`WEX201`), so no
re-approval event could be recorded on it. Shown three measured routes, the owner
chose to reject `WO-RLS-009` and issue `WO-RLS-010`. Because `REL-SEH-013` named
`WO-RLS-009` in `gates`, that left an approved contract naming a rejected member,
so `REL-SEH-013` and `WO-RLS-009` were rejected in one atomic transaction at
2026-08-25T11:47:44Z. `REL-SEH-014` and `WO-RLS-010` succeeded them and were both
approved at 2026-08-25T11:53:28Z.

Forty-six seconds later, at 2026-08-25T11:54:14Z, `WO-ADS-002` reached
`implemented`. Together with `WO-ADS-001`, implemented at 2026-08-25T11:15:03Z,
it reached `main` through the true merges of pull requests #152 and #153 at
`701e456794636e83ff78eb9910df55dfc1eedd9c`. Both change `se_harness/` runtime
modules and distributed managed templates, so both belong in the release unit,
and `REL-SEH-014`'s approved allow-list stopped describing the release for the
second time in two hours.

Shown the measured cost of each route, the owner decided on 2026-08-25 to break
the cycle rather than repeat it: `REL-SEH-014` and `WO-RLS-010` are rejected,
`REL-SEH-015` is issued and deliberately held in `draft` until immediately before
the candidate commit, and this work order defers its aggregate census instead of
fixing one in approved prose. A `draft` contract is edited in place as work
lands; only approval freezes `gates`. The governing workflow contract ties this
work order's start to no approved release contract, and `focus` names only start
preflight and the engineering owner, so nothing is lost by approving the contract
last.

`WO-RLS-009`, `WO-RLS-010`, `REL-SEH-012`, `REL-SEH-013`, and `REL-SEH-014` are
all preserved as immutable rejected history. None of their recorded lifecycle
events was rewritten, and the owner's real approval of `REL-SEH-014` and
`WO-RLS-010` at 11:53:28Z stands in the record rather than being erased.

No work was started under `WO-RLS-009` or `WO-RLS-010`. No start preflight was
run, no version identity was moved, no distribution was built, and no candidate
commit exists, so this successor inherits no partial state.

This work order declares `REQ-DST-006`, `SPEC-DST-001`, `ARCH-DST-001`,
`ADR-DST-001`, and `VER-DST-001` in its relations, and deliberately not a release
contract. Further contract succession therefore breaks no graph edge that points
at this work order, and this work order does not have to be re-issued when the
contract is.

Approval authorizes start preflight followed by only the declared versioning,
integration, qualification, reproducible-build, index-maintenance, and
retained-evidence work within the six declared execution-scope paths.

Approval explicitly does not authorize the candidate commit, `REL-SEH-015`'s
approval, `VREC-SEH-013` or `RLS-SEH-013` preparation or transition, branch push,
tag creation or movement, GitHub or PyPI publication, Pages deployment,
maintenance-line mutation, credential use, external policy change, or
root-evaluator upgrade.

Commit-bound verification is classified `required` because the release owner, the
assurance owner, consumers, publication automation, the recipe interpreter, and
future repository upgrades will rely on the exact integrated executable package,
standard template, evaluator boundary, provenance, and distribution bytes. This
classification is not inferred from a default.

### Implementation and the implemented transition

Start preflight passed and implementation ran under this work order from
2026-08-25T13:29:18Z to the candidate commit
`f76da5727e86fc53375bfa5cafcfcbf168c7456e`, whose tree is
`52fdae8c6e090f62341df8b87c52fc308d5132f7` and whose parent is the true merge of
pull request #154 at `826c72cfdaa3401cccf06c67943c5315221c3f72`. The candidate is
exactly that parent plus eight changed files, all of which fall inside the seven
declared execution-scope paths; `docs/engineering/release-0-7-0/` is a directory
and covers two of the eight.

The accountable engineering owner then marked this work order `implemented` under
`DR-WO-COMPLETE` at 2026-08-25T18:43:37Z, on the `handoff` gate reading
`Completed` over that candidate. The reason recorded on that lifecycle event is
the decision record and the readings behind it are in the keyed evidence. **One
noun in that reason is imprecise and is corrected here rather than rewritten
there:** it says the change set was asserted complete over "the eight declared
paths of the amended execution scope", where the amended scope declares seven
paths and the candidate changes eight files. The set of bytes is exactly the one
intended; only the count's label is wrong. A recorded lifecycle reason is
immutable history, so the correction is stated and the event is left untouched.

Two further owner decisions were taken on 2026-08-25 after the exact-candidate
readings were put to the owner, and neither is carried by this work order's
approval. First, the working branch is authorized to be pushed, so the hosted
`windows-2022` and `ubuntu-latest` lanes can read the candidate; that push is an
explicit later exception to the approval-time exclusion of branch push, and it
merges nothing, creates or moves no tag, builds no distribution and publishes
nothing. Second, `WO-RLO-006` is authorized to start, which is where the Windows
plus CPython 3.11 junction defect in the publication rehearsal is repaired; that
work is governed by its own work order and not by this one. `VREC-SEH-013`,
`RLS-SEH-013`, build authority, the tag, GitHub or PyPI publication, Pages
deployment, the `release/0.7` maintenance line, and any root-evaluator change all
remain unauthorized.

## Objective

Produce one clean and fully qualified 0.7.0 candidate containing exactly the
historical work orders `REL-SEH-015` names in `gates` plus this
release-integration work order, with consistent version identity, one standard
installation, independently proven evaluator, candidate-source, and
candidate-package roles, recipe-bound reproducible distributions, complete
retained evidence, and exact aggregate verification inputs. Stop after an
implemented candidate and retained evidence unless later authority permits the
candidate commit and `VREC-SEH-013` preparation.

## Aggregate scope: governed by the contract, measured at the candidate

**This work order fixes no census.** The release unit is exactly what
`REL-SEH-015` names in `gates` at the moment the release owner approves it, and
every derived aggregate — the verification-contract set, the requirement union,
and the keyed evidence paths — is derived from that `gates` array and re-measured
against the candidate commit. No count in this work order is binding, and a count
appearing anywhere in this prose is a dated observation, not scope.

This is deliberate. `WO-RLS-009` had to be rejected because its approved prose
stated a census that a later landing falsified, and the harness has no
re-approval transition with which to correct it. Deferring the census is what
lets this work order survive further landings without succession.

What this work order does fix, and what approval binds, is the execution scope:
the six declared paths in `[execution_scope]`, being `README.md`,
`pyproject.toml`, `se_harness/__init__.py`,
`docs/notes/developing-se-harness.md`, `docs/engineering/README.md`, and
`docs/engineering/release-0-7-0/`.

### Dated observation, not scope

Measured on 2026-08-25 against `main` at
`701e456794636e83ff78eb9910df55dfc1eedd9c` merged into this packet's branch, the
unit stood at thirty-five historical work orders plus this one, twenty-two
verification contracts, a forty-eight-requirement union, and thirty-seven
work-order-keyed evidence paths, being thirty-six existing paths plus the one
this work order will retain. Those figures are recorded so a reviewer can see the
shape of the work, and they are expected to move. `REL-SEH-015` carries the
authoritative enumeration while it is `draft`, and re-derivation at the candidate
is a required verification step below, not a confirmation of these numbers.

### Fixed regardless of the census

- New evidence after approved execution:
  `docs/engineering/release-0-7-0/evidence/WO-RLS-011-verification.md`.
- Planned aggregate VREC after an authorized clean candidate commit:
  `docs/engineering/release-0-7-0/verification-records/VREC-SEH-013.md`.
- Planned release record after verified assurance and separate
  release-preparation authority:
  `docs/engineering/release-0-7-0/releases/RLS-SEH-013.md`.
- Proposed public version and immutable tag: `0.7.0` and `v0.7.0`.
- The combined-evidence file
  `technical-communication/evidence/WO-TCM-001/WO-TCM-002-verification.md` is
  keyed by the directory-position attribution rule to both `WO-TCM-001` and
  `WO-TCM-002` and is counted once, whatever the total.

Historical VRECs support lineage and evidence discovery but bind different
commits and do not replace the new candidate-bound aggregate VREC.

## In scope

After separate approval of this work order:

- Reconfirm the `v0.6.0...candidate` ledger from the candidate itself and retain
  the exact inclusion and exclusion rationale, including the classification calls
  `REL-SEH-015` puts to the release owner, the recorded admission and transition
  of `WO-TCM-001`, and the admission of `WO-AEX-005` with the fact that its four
  new runtime modules are unreachable from `se_harness/cli.py` and therefore
  inert in 0.7.0.
- Re-derive the release unit from `REL-SEH-015`'s `gates` at the candidate and
  prove the two agree exactly. Stop if any member does not read `implemented`
  with verified coverage at the candidate, and stop if any work order whose bytes
  are in the packaged surface is unnamed. This replaces carrying any count
  forward.
- Report to the release owner, before the contract's approval is sought, every
  work order that reached `implemented` after this packet was written, so the
  `draft` contract can be corrected in place rather than approved stale. This is
  the mechanism that replaces succession, and it is an explicit obligation of
  this work order.
- Confirm before any build that `WO-TCM-001`, `WO-AEX-005`, `WO-ADS-001`, and
  `WO-ADS-002` all read `implemented` in the candidate tree. Stop if any does
  not.
- Confirm before aggregate capture that `WO-TCM-001`'s assurance route was
  decided by the assurance owner, and record which route was taken. Measured on
  2026-08-25: route two, verify with the missing manual-assessment judgments
  disclosed as accepted residual risk. Re-read `VREC-TCM-002` at the candidate
  rather than carrying that forward, and stop if the record's state differs.
- Carry forward, without softening, the disclosed manual gaps in `VREC-ADS-001`
  and `VREC-ADS-002`: `VER-ADS-001`'s Scenario 8 independent-reviewer
  classification was not run, and both records were verified with the Linux
  figure pending the pull-request lane. Record which of those the candidate
  resolves and which remain residual risk.
- Add `release-0-7-0/` to the repository-owned engineering domain index at
  `docs/engineering/README.md`, as that index's own maintenance rule requires
  when a domain is added. Record whether the standing absence of `release-0-6-0/`
  is corrected in the same edit or left to its own decision, and change nothing
  else in that file.
- Set candidate product identity to 0.7.0 in `pyproject.toml`,
  `se_harness/__init__.py`, and the current public installation example in
  `README.md`.
- Update `docs/notes/developing-se-harness.md` so it names candidate 0.7.0 as the
  current candidate version while continuing to name the exact root evaluator
  version recorded in `.engineering-harness.toml`. Both identities are required
  by the existing documentation contract; neither may replace the other. That
  file now also carries the release-build, release-binding, and last-mile
  publication sequences that the repository-context document `WO-ADS-002` retired
  used to hold, so preserve those sequences while changing the version
  statements.
- Preserve historical 0.5.0, 0.5.0a1, and 0.6.0 incident, evaluator, recovery,
  bootstrap, test-fixture, and governance references whose meaning is not the
  current candidate version.
- Preserve the root `.engineering-harness.toml`, `.engineering-harness.lock`,
  `ENGINEERING_HARNESS.md`, and managed
  `.github/workflows/engineering-harness.yml` as the exact released 0.6.0
  installation until a later, separately authorized post-publication upgrade.
- Reconcile candidate package data and standard-template parity for workflow and
  quality-gate JSON, evaluator identity, hash-bound class declarations, Git
  attributes, mutation guards, agent and skill contracts, the managed
  technical-communication policy and its router row, all five installed skills,
  recovery, authoring, provenance, CLI, validator, Explorer, and documentation
  surfaces. This now includes the distributed managed surfaces `WO-ADS-001` and
  `WO-ADS-002` changed: the new `docs/engineering/OPERATING_CARD.md` managed
  file, the amended `ENGINEERING_HARNESS.md` router template,
  `docs/engineering/WORKFLOW.json` and `WORKFLOW.md`, the pull-request template
  seed, the managed CI workflow, and `scripts/select_harness_work_order.py`.
- Run formal graph, release-distribution, managed-integrity, identity, byte-rule
  inventory, workflow, CLI, package-surface, archive-safety, reproducibility,
  Explorer, recovery, and full supported-runtime verification.
- Exercise the five `qualify` operations from the candidate in their applicable
  roles and record the boundary refusals of the operations that do not apply to a
  candidate root, together with the released-evaluator observations that stand in
  for them.
- Under explicit build authority granted by later approval, replay the
  recipe-bound build twice from exact exported candidate source at one epoch
  through `repository_tools.release_build replay` and prove byte identity, safe
  archives, and reconstruction equivalence.
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
  lifecycle. The contract's approval, the candidate commit, aggregate capture,
  verification, release preparation, release, and external actions remain
  separate stages.

## Out of scope

- Approving `REL-SEH-015`. Holding it in `draft` until immediately before the
  candidate is the owner's recorded decision; its approval is the release owner's
  separate act and is not carried by approving this work order.
- Adding product behavior, or admitting a work order into the unit by any route
  other than editing the `draft` contract and having the release owner approve
  the result. While the contract is `draft` it is corrected in place; once
  approved it is never widened, and `REL-SEH-012`, `REL-SEH-013`, and
  `REL-SEH-014` were each rejected for exactly that reason.
- Capturing, preparing, or verifying a commit-bound record for `WO-TCM-001`,
  `WO-ADS-001`, or `WO-ADS-002`. Their coverage is already decided, and their
  disclosed limitations are carried, not re-litigated, here.
- Recording `VER-TCM-001`'s two reviewer judgments or running `VER-ADS-001`'s
  Scenario 8 classification. Both are later governed work requiring successor
  verification records.
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
- Removing the independent package lane's documented `accept-candidate` bootstrap
  exception, which exact public 0.6.0 still requires.
- Rewriting historical VREC, RLS, evidence, release, tag, incident, publication,
  or evaluator facts, or rewriting the rejected history of the three contracts
  and two work orders this packet supersedes.
- Using candidate source or an editable or contaminated install as the root
  evaluator or independent verifier.
- Weakening mutation guards, path safety, transactional rollback, evidence
  binding, workflow gates, archive checks, reproducibility, byte rules, or
  authority boundaries to obtain a pass.
- Preparing or transitioning `VREC-SEH-013` before one separately authorized
  clean candidate commit.
- Preparing or transitioning `RLS-SEH-013`, or binding its distribution table,
  before verified aggregate assurance and separate release-preparation authority.
- Merge, branch push, tag, GitHub Release, PyPI publication, Pages deployment,
  maintenance-line mutation, credential use, external policy change, force push,
  or history rewrite.

## Authorized decision envelope

After separate approval, the implementation agent may choose deterministic
temporary directories outside the checkout, the candidate epoch, the
evidence-table layout, safe mechanical version edits within the declared paths,
and test helpers required by existing contracts. It may not reinterpret the
allow-list, decide what the contract names, change accepted product behavior,
widen changed paths, add dependencies or build profiles, alter the root evaluator
identity or lock, decide historical VREC disposition, make accountable
transitions, or perform external release actions. Uncertainty escalates rather
than resolving into a local default.

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
  requires, and do not disturb the owner-region byte rules that `WO-HBI-003` and
  `WO-HBI-004` established.
- Do not write the literal token of the repository-context path `WO-ADS-002`
  retired into any file in this packet, including this work order, the contract,
  the domain index, and the retained evidence. That work order's suite asserts an
  exact allow-list of the files permitted to name it, and `tests/` is outside this
  work order's execution scope, so a mention would turn the suite red on both
  platforms with no in-scope repair available. Describe the retirement in prose
  instead.
- Derive the selected work-order, requirement, and verification-contract unions
  from the contract's `gates` at the candidate. Do not infer scope from commits
  or dates, and do not carry a union forward from this prose.
- Make no candidate mutation after exact-commit replay or aggregate capture.
- Preserve unrelated user changes and stop if the reviewed packet or candidate
  changes underneath execution.

## Scope amendment, 2026-08-25

Amended on 2026-08-25 by the engineering owner, during implementation and on an
explicit request put with the measurement in front of it.
`tests/test_release_qualification.py` is added to `[execution_scope]` as the
seventh declared path, for one purpose only: retargeting the version-coupled
fixture in
`ReleaseQualificationTests.test_public_install_binds_released_record_wheel_and_payload`
from `0.6.0` to `0.7.0`.

The reason is that `qualify public_install` requires
`wheel_version == version == installed.version == __version__`, so the test's
mocked released record, wheel name, metadata, installed version, and subprocess
output must all carry the candidate version for the assertion to hold. The bump
this work order exists to make therefore breaks that fixture by construction: it
passes in a control worktree at `826c72cfdaa3401cccf06c67943c5315221c3f72` and
fails against the bumped tree, so the red is caused by the declared change and
not by a defect the release should carry.

The owner was asked rather than told because the alternative reading is real: the
mechanic that binds the published wheel is exactly the one going red, so
retargeting the fixture without an accountable decision would look like adjusting
the evidence to fit the result. The amendment authorizes the version values in
that one test method and nothing else. No production behaviour changes, no other
test file is opened, and it widens no other constraint: the out-of-scope list, the
stop conditions, the required verification, and the actions listed as separately
unauthorized are all untouched by it.

Two other blockers were put to the owner in the same exchange and neither is
amended into this work order. The Windows-plus-Python-3.11 junction defect in
`.github/scripts/rehearse_publication.py` is routed to its own work order, to be
fixed before 0.7.0 ships; `.github/` stays outside this scope. The open pull
request carrying `WO-RSK-001` is held until 0.7.0 is tagged, on the same reasoning
as the standing hold on the pull request carrying `WO-AEX-006`, so `REL-SEH-015`'s
`gates` is not reopened. Both decisions are recorded in this work order's retained
evidence with the readings they were taken on.

## Expected change surface

- `pyproject.toml`, `se_harness/__init__.py`, and the current install-version
  example in `README.md`.
- The current-candidate-version statements in
  `docs/notes/developing-se-harness.md`.
- One domain-list addition in `docs/engineering/README.md`, and no other change
  to that repository-owned index.
- `docs/engineering/release-0-7-0/` for the contract, this work order, the domain
  index, the retained evidence, and later separately prepared records. Editing
  the `draft` `REL-SEH-015` to keep its `gates` current is inside this path and
  inside this work order; approving it is not.
- The version values in the one amended fixture method of
  `tests/test_release_qualification.py`, under the scope amendment above.
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
- Complete supported-runtime suites, including Python 3.11, with exact counts and
  only explained conditional skips. Windows platform-guard skips are expected;
  the hosted Linux lane is expected to run the same suite without them.
- Candidate-source identity from the exact candidate checkout, with distribution
  metadata resolving within the checkout as required.
- Candidate-package identity and verifier-owned black-box acceptance from a fresh
  exact-wheel installation outside the checkout.
- Released-evaluator identity and isolation with no candidate or editable import
  fallback.
- Exact version inventory: current candidate-bearing surfaces equal 0.7.0 while
  historical and root-evaluator identities remain truthful, including the
  documentation contract's simultaneous 0.7.0 candidate and 0.6.0 evaluator
  statements.
- Exact package and template parity, payload manifest, wheel archive identity,
  mutation-guard coverage, hash-bound class completeness, byte-rule inventory
  coverage, workflow and gate contract parity, operating-card bound, and
  active-surface retired-role checks.
- Doctor, init, adopt, validate, focus, check, transition plan, inspect,
  dashboard, upgrade plan and refusal, artifact authoring, renumber plan and
  refusal, verification-capture refusal and success boundary,
  release-preparation refusal and success boundary, `qualify` operation
  boundaries, `migrate` rehearsal, and recovery rehearsal scenarios.
- Governor-succession assessment proving the released 0.6.0 evaluator governs the
  0.7.0 candidate root without a version-specific exception.
- Credential-free publication rehearsal on both runner platforms with no
  credential present and no external write attempted.
- Deterministic Explorer generation within the declared resource budgets.
- Two recipe-bound replays produce byte-identical wheels and normalized sdists at
  one epoch; archives are safe and equivalent; the reconstructed wheel equals the
  direct wheels and passes fresh Python 3.11 operation.
- Release-distribution bundle manifest, checksums, source manifest, candidate
  commit, tree and epoch, Git ancestry, changed-path ledger, protected-control
  diff, secret and private-path scan, and `git diff --check` pass.
- Aggregate VREC inputs contain exactly the work-order set `REL-SEH-015` names in
  `gates`, its derived verification contracts, its keyed evidence paths, one
  clean candidate commit, one artifact snapshot, and matching evaluator evidence.
  Measure the work-order count, the verification-contract count, and the keyed
  evidence-path count against the candidate and record all three as measured
  figures. Do not carry any figure forward from this work order or from a
  superseded one.
- The engineering domain index names `release-0-7-0/`.

## Evidence to record

Retain preliminary working-tree checks and later exact-candidate replay
separately at
`docs/engineering/release-0-7-0/evidence/WO-RLS-011-verification.md`. Record the
baseline and candidate commit, tree and epoch; the complete allow-list and
exclusions as the contract names them at approval, with the classification calls
as decided; every work order that landed after this packet was written and how it
was dispositioned; the version inventory; the released-evaluator payload, archive
and origin; the candidate source and package origins; commands and exit results;
test counts per platform; graph planes; inspection queues; Explorer manifests and
byte budgets; changed paths; managed-root integrity; recipe identity and both
replay hash sets; reproducibility; the acceptance manifest; the bundle manifest
identities; hosted run, job and artifact identities; warnings; deviations;
residual risks; and every unperformed transition or external action.

## Stop and escalate conditions

Stop on packet or scope change, a work order whose bytes are in the packaged
surface and which the contract does not name or which holds no verified coverage
at aggregate capture, an approved contract whose `gates` no longer describes the
unit, missing keyed evidence, an unresolved historical `ready` record, an invalid
graph, failed preflight, version drift, root evaluator or lock change, candidate
contamination, cross-role import, unsafe path or archive, incomplete mutation or
byte-rule coverage, a failed required check, an unexplained warning,
nondeterminism between the two replays, package or template divergence, candidate
mutation after exact evidence, a hosted lane that does not run on the expected
event, or a need for authority beyond the approved stage.

## Completion report format

Report the work-order scope and exclusions as measured from the contract's
`gates` at the candidate; every work order that landed during execution and its
disposition; `WO-TCM-001`'s state and the assurance route taken; the disclosed
`VER-ADS-001` Scenario 8 and pull-request-lane gaps and their disposition; the
baseline and candidate identity; the version inventory; the engineering index
edit; evaluator, source and package origins; root integrity; exact commands and
test results with their platforms; graph planes and warnings; workflow and gate,
mutation, byte-rule, governor succession, publication rehearsal, recovery,
Explorer, package, archive and reproducibility results; hashes and manifests; the
evidence path; the planned aggregate VREC inputs; deviations and residual risks;
and every unperformed commit, push, verification transition, release preparation
and transition, merge, tag, publication, deployment, maintenance-line,
credential, and root-upgrade action.
