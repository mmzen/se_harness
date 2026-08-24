# WO-LRE-001 Implementation Evidence

Date: 2026-08-24

Authority: non-authoritative retained implementation evidence. This file does not approve an artifact, authorize a diff, verify work, release software, commit, push, tag, publish, or deploy. `VER-LRE-001` classifies commit-bound verification as `required`, so nothing here substitutes for a later accountable verification record bound to a reviewed candidate commit.

## Candidate under measurement

- Branch: `feat/reb-legacy-release-evidence-declaration`
- Governance commit: `c930c447ced2be940d6a10255deef4acc228a2e4`
- Merge base with `origin/main`: `1cdc75259da8156e93ad8c32110ee196296b8cea`
- Platform: `Windows-11-10.0.26200-SP0`
- Python: `3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)]`

Every figure below was measured in this checkout at that commit with the implementation present in the working tree. The baseline figures were measured at the same commit in a separate clean worktree, so the only difference between baseline and post-change is the implementation itself, not the governing packet.

## Implemented behaviour

A record that was released before evaluator-evidence enforcement existed can never be rewritten to carry a binding. `SPEC-LRE-001` therefore declares such records instead. The declaration is one optional array, `legacy_releases_without_evaluator_evidence`, in the authorizing work order's own `[evaluator_upgrade]` packet. It is honoured only for a record that is `released`, carries neither `evaluator_evidence_path` nor `evaluator_evidence_sha256`, and was released strictly before the declaring work order left `draft` for `approved` under a work-order state that grants authority. A partially bound record is never exempt, and an unresolvable member is a governance error on the declaring work order rather than a widened exemption.

One semantics is implemented twice, as `VER-LRE-001` requires:

- `se_harness/legacy_release_evidence.py` for the package, consumed by `se_harness/installer.py`, `se_harness/cli.py`, and `se_harness/upgrade_authorization.py`;
- a self-contained copy inside `templates/repository/standard/scripts/validate_engineering_artifacts.py`, which is the candidate validator a consumer repository runs.

Authority is derived at runtime from `WORKFLOW_LIFECYCLES["work_order"]` through `row.grants_authority`; no state name is hardcoded on either side. `.github/scripts/publish_dashboard.py` consumes the frozen self-hosting rule for its release view and owns no rule of its own; this change adds only the comments that say so.

An accepted exemption raises exactly one `W024` maintenance warning naming the record and its declarer, so the outstanding binding stays visible and validation still passes. `upgrade --apply` refuses an evaluator identity transition before its first write when the repository holds an undeclared unbound released record. Read-only `harnessctl upgrade` prints the same list as a planning notice and still exits `0`.

## Repository error and warning counts, before and after

Measured with the frozen root validator (released 0.6.0 managed copy) and with the candidate validator, over this repository:

| Validator | Baseline at `c930c44` | With the implementation |
| --- | --- | --- |
| `scripts/validate_engineering_artifacts.py` (root, frozen) | PASS; 755 artifacts, 0 errors, 50 warnings | PASS; 755 artifacts, 0 errors, 50 warnings |
| `templates/repository/standard/scripts/validate_engineering_artifacts.py` (candidate) | PASS; 755 artifacts, 0 errors, 50 warnings | PASS; 755 artifacts, 0 errors, 56 warnings |

Plane split with the implementation, candidate validator: `structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W56`.

The entire delta is six new `W024` warnings, one per member of the frozen self-hosting compatibility set. No error count moved and no other warning appeared or disappeared:

```
- [W024] [maintenance] docs/engineering/release-0.2.0/releases/RLS-SEH-001.md: released record 'RLS-SEH-001' predates evaluator-evidence enforcement and is exempt through self-hosting-compatibility-set; the binding remains outstanding
- [W024] [maintenance] docs/engineering/release-0.2.1/releases/RLS-SEH-002.md: released record 'RLS-SEH-002' predates evaluator-evidence enforcement and is exempt through self-hosting-compatibility-set; the binding remains outstanding
- [W024] [maintenance] docs/engineering/release-0.2.2/releases/RLS-SEH-004.md: released record 'RLS-SEH-004' predates evaluator-evidence enforcement and is exempt through self-hosting-compatibility-set; the binding remains outstanding
- [W024] [maintenance] docs/engineering/release-0.3.0/releases/RLS-SEH-005.md: released record 'RLS-SEH-005' predates evaluator-evidence enforcement and is exempt through self-hosting-compatibility-set; the binding remains outstanding
- [W024] [maintenance] docs/engineering/release-0.4.0/releases/RLS-SEH-006.md: released record 'RLS-SEH-006' predates evaluator-evidence enforcement and is exempt through self-hosting-compatibility-set; the binding remains outstanding
- [W024] [maintenance] docs/engineering/release-0.4.1/releases/RLS-SEH-007.md: released record 'RLS-SEH-007' predates evaluator-evidence enforcement and is exempt through self-hosting-compatibility-set; the binding remains outstanding
```

`python scripts/validate_release_distributions.py --root .`: `SE Harness release distribution validation: PASS (1 distribution-bearing record)`. Unchanged from baseline.

## Full test result, before and after

`python -m unittest discover -s tests -p "test_*.py"` from the checkout root:

| | Tests | Failures | Skipped | Duration |
| --- | --- | --- | --- | --- |
| Baseline at `c930c44`, clean worktree | 592 | 4 | 12 | 314.505s |
| With the implementation | 635 | 4 | 12 | 291.293s |

Both runs fail the same four tests, by name:

```
FAIL: test_contract_rejects_duplicate_and_unknown_fields (test_agentic_execution.SkillContractTests.test_contract_rejects_duplicate_and_unknown_fields)
FAIL: test_manifest_normalizes_line_endings_and_detects_content_changes (test_agentic_execution.SkillContractTests.test_manifest_normalizes_line_endings_and_detects_content_changes)
FAIL: test_declaration_is_data_only (test_hash_bound_integrity.DeclarationShapeTests.test_declaration_is_data_only)
FAIL: test_non_promotable_ephemeral_wheel_carries_and_fresh_installs_one_skill_core (test_release_build.DeterministicSdistTests.test_non_promotable_ephemeral_wheel_carries_and_fresh_installs_one_skill_core)
```

These four are pre-existing Windows checkout line-ending failures in files this work order does not touch. They are present at the same commit without the implementation, so this change introduces no regression: the delta is exactly `+43` tests and `0` new failures. The twelve skips are the repository's Windows-only platform guards and are identical in both runs.

`python -m unittest tests.test_legacy_release_evidence`: `Ran 43 tests in 3.765s` / `OK`. Nine classes: `ResolutionVectorTests` (4), `AuthorityMatrixTests` (4), `DeclarationBoundTests` (3), `ReasonTextTests` (2), `SelfHostingCompatibilitySetTests` (3), `RepositoryResolutionTests` (10), `UpgradePacketTests` (7), `InstallerRefusalTests` (4), `ValidatorDiagnosticTests` (6).

`python -m se_harness --help`: exits `0`. `git diff --check`: clean.

## Shared vector fixture and both implementations' result

`tests/fixtures/legacy_release_evidence/resolution_vectors.json`

- schema: `se-harness-legacy-release-evidence-vectors-v1`
- specification: `SPEC-LRE-001`
- 27 named cases, each tagged with the rule it exercises; rules `1` through `11` are all covered
- 17831 bytes, LF only (0 CR), SHA-256 `cb046d48224ab09ae2804f4d5097619fe57e409fa07f18562b36be9e62e4617d`

`ResolutionVectorTests` resolves every case through `se_harness.legacy_release_evidence.resolve(...).as_dict()` and through the candidate script's `resolve_legacy_release_evidence(...)` and asserts each equals the fixture's expected resolution. Both implementations match all 27 cases with no exception. `ReasonTextTests` additionally asserts that all ten reason strings and the packet identity constants are byte-identical across the two implementations, and `AuthorityMatrixTests` asserts both read the same authority-granting state set out of the managed lifecycle registry: granting is exactly `{approved, in_progress, implemented, verified, released}`, and `{draft, ready, superseded, rejected}` plus an unknown state never grant.

The two new implementation files are LF-only as well: `se_harness/legacy_release_evidence.py`, 13000 bytes, SHA-256 `1dae650b6995de474f2716a01fff577a2600daebef1e64197af9f2e7234680d4`; `tests/test_legacy_release_evidence.py`, 37045 bytes, SHA-256 `6e0321f5cf669893d4f70dea53795c3a96ed5408477e7178c3f7c03220b9b32a`.

## Complete diagnostic text of every negative case

Rendered through the candidate validator's `validate_type_specific_metadata` over a synthetic two-artifact graph, one case per fixture, filtered to diagnostics naming the declaration field. Every case is a single governance error attributed to the declaring work order, never to the release record:

```
# declaration is not an array
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence: declaration must be an array of strings

# declaration holds a non-string member
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence: declaration must be an array of strings

# declaration exceeds the bound
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence: declaration exceeds 512 entries

# declarer has no approval instant
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence: declaring work order has no draft-to-approved lifecycle event

# declared identifier is invalid
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence 'rls-con-001': invalid release record identifier

# declared identifier is unknown
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence 'RLS-CON-404': no release record has this identifier

# declared identifier is ambiguous
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence 'RLS-CON-001': more than one release record has this identifier

# record is not released
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence 'RLS-CON-001': release record status is not released

# record is already bound
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence 'RLS-CON-001': release record already carries evaluator evidence

# record has no canonical released_at
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence 'RLS-CON-001': release record has no valid released_at timestamp

# record is newer than the approval
- [E012] [governance] docs/engineering/sample/work-orders/WO-CON-001.md: legacy_releases_without_evaluator_evidence 'RLS-CON-001': release record was released after the declaring work order was approved
```

The packet loader refuses the same malformed shapes earlier, at authorization load time: a non-string array, an invalid identifier, more than 512 entries, and any key beyond the nine required fields plus this one permitted optional key. An empty array is accepted and declares nothing. `UpgradePacketTests` covers each.

Two further fail-closed paths carry no declaration text because they abort the assessment itself: an artifact file with invalid TOML front matter and an artifact file above the 256 KiB bound both raise `LegacyReleaseEvidenceError`, which the installer converts into a refusal rather than into an empty exemption set.

## Refused-upgrade transcript with before-and-after tree digests

An evaluator identity transition was authorized onto the identity the installed root already carried, so the only thing that could stop the apply was the refusal under test. The repository held one released record, `RLS-XYZ-001`, with no binding and no declaration. The tree digest is SHA-256 over every file's repository-relative path and content digest, in sorted path order.

```
tree digest before   : b68ec5b5ce17bb0c3ab78322f8fc7b210e09bb0068f14eab0879de5dff704365
HarnessError: released records predate evaluator-evidence enforcement and are not declared; no files were written: RLS-XYZ-001; declare them in WO-XYZ-001 under [evaluator_upgrade].legacy_releases_without_evaluator_evidence
tree digest after    : b68ec5b5ce17bb0c3ab78322f8fc7b210e09bb0068f14eab0879de5dff704365
byte-identical       : True
evidence file created: False
```

The refusal happens before `target.mkdir(...)`, so no directory, temporary file, managed file, lock, or evaluator-evidence JSON is produced. `InstallerRefusalTests` proves the same property over a recursive path-and-bytes snapshot, and separately proves that a declared record lets the transition proceed with the declaration carried into the evidence payload, that an unassessable tree refuses, and that a repository holding no released records is unaffected with its evidence shape unchanged.

## Planning-path transcript

`python -m se_harness upgrade <repository> --work-order WO-XYZ-001`, exit status `0`:

```
notice: these released records predate evaluator-evidence enforcement and are not declared; applying an evaluator identity transition would be refused:
  RLS-XYZ-001
declare them in WO-XYZ-001 under [evaluator_upgrade].legacy_releases_without_evaluator_evidence
summary: 39 files, 39 unchanged
```

The read-only path never refuses and never changes its exit status. It only names the records and the field, so the declaration can be prepared before anyone attempts the apply.

## End-to-end reproduction against the issue #126 repository

Consumer: `mmzen/Mokiterions`, a throwaway clone at commit `2a939149af77dfd8b08c44aa886620ffdcd861a9`, whose managed root had already been advanced to the enforcing 0.6.0 copies. It holds one pre-enforcement release record, `RLS-MOK-001`, released `2026-08-19T17:53:05Z` under an earlier schema.

Its own installed root validator reproduces the reported freeze:

```
Engineering artifact validation: FAIL
Artifacts: 156 | Errors: 1 | Warnings: 0
Planes: structure E0/W0 | governance E1/W0 | policy E0/W0 | maintenance E0/W0
- [E012] [governance] docs/engineering/simulation/releases/RLS-MOK-001.md: field 'evaluator_evidence_path' must be a non-empty string
```

The declaration was written into the authorizing work order's own packet, and nowhere else:

```toml
[evaluator_upgrade]
schema = "se-harness-evaluator-upgrade-v1"
scope = "standard-root-only"
legacy_releases_without_evaluator_evidence = ["RLS-MOK-001"]
```

`WO-MOK-024` carries a `draft` → `approved` event at `2026-08-22T09:00:00Z`, which is after the record's `released_at`, and reaches `implemented` through two further events. The candidate validator from this branch, run over that repository, then reports:

```
Engineering artifact validation: PASS
Artifacts: 156 | Errors: 0 | Warnings: 1
Planes: structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W1
- [W024] [maintenance] docs/engineering/simulation/releases/RLS-MOK-001.md: released record 'RLS-MOK-001' predates evaluator-evidence enforcement and is exempt through WO-MOK-024; the binding remains outstanding
```

The error is gone, exactly one maintenance warning replaces it, and it names both the record and its declarer. `git status --porcelain=v1 -- docs/engineering/simulation/releases/RLS-MOK-001.md` reports nothing, so the released record is byte-unchanged. Its front matter still reads:

```toml
+++
id = "RLS-MOK-001"
type = "release_record"
title = "Release candidate 0.1.0"
status = "released"
owners = ["release owner"]
created = "2026-08-19"
updated = "2026-08-19"
version = "0.1.0"
commit = "755db7297aa993f00d42f9c9794584b5d061f03d"
git_object_format = "sha1"
released_at = "2026-08-19T17:53:05Z"
authorized_by = "release owner"
tag = "v0.1.0"

[relations]
satisfies = ["REL-MOK-001"]
includes_verification = ["VREC-MOK-009"]
releases_work = ["WO-MOK-001", "WO-MOK-002", "WO-MOK-003", "WO-MOK-004", "WO-MOK-005", "WO-MOK-006", "WO-MOK-007", "WO-MOK-009"]
+++
```

This is one real consumer, not a population. `VER-LRE-001` records that limit as residual uncertainty.

## Governing evaluator and boundary checks

The exact published 0.6.0 evaluator was run from a virtual environment outside this checkout, with `-I`, from a working directory that is not the checkout, so the candidate source was never on `sys.path`:

- `doctor <checkout>`: 87 PASS, 0 FAIL. The remaining output is pre-existing `W013` canonical-location warnings.
- `preflight <checkout> --work-order WO-LRE-001 --phase start`: `Harness preflight: PASS`.
- `preflight <checkout> --work-order WO-LRE-001 --phase review`: `Harness preflight: PASS`. Both report `WO-LRE-001 (in_progress)` and commit-bound verification `required`.

The in-tree `python -m se_harness doctor .` reports 8 FAIL — five `distribution:` skews including `scripts/validate_engineering_artifacts.py`, and three missing `lock-entry:.agents/skills/harness-orient/*` items. The identical 8 FAIL were measured at the same commit without the implementation, so this change adds no new skew. That skew is candidate-versus-released boundary evidence, not authorization to overwrite root managed files; the frozen root copy of the validator was not edited.

## Changed implementation surface

`git diff --stat` over tracked files, plus three new untracked files:

```
 .github/scripts/publish_dashboard.py               |  11 +
 docs/notes/harness-installation-and-upgrades.md    |  30 +++
 se_harness/cli.py                                  |  33 +++
 se_harness/installer.py                            |  35 +++
 se_harness/upgrade_authorization.py                |  33 ++-
 .../scripts/validate_engineering_artifacts.py      | 274 ++++++++++++++++++++-
 tests/test_release_bootstrap.py                    |   8 +
 7 files changed, 422 insertions(+), 2 deletions(-)

?? se_harness/legacy_release_evidence.py
?? tests/fixtures/legacy_release_evidence/resolution_vectors.json
?? tests/test_legacy_release_evidence.py
```

Every path is inside `WO-LRE-001`'s declared `[execution_scope]`. The change to `.github/scripts/publish_dashboard.py` is comments only: it explains that the frozen self-hosting set is closed to additions, that a consumer instead declares its records in the authorizing packet, and that resolving such a declaration belongs to the validator. That script publishes only this repository, whose own exemptions are the frozen set and nothing else, and the workflow that runs it installs no package, so it cannot import `se_harness`; introducing a third implementation of the semantics there would breach `SPEC-LRE-001`.

## Actions not performed

- Every figure above was measured over working-tree state on top of the governance packet commit `c930c44`. That exact content is what the commit carrying this file records; no candidate was amended after measurement. A file cannot name the hash of the commit that introduces it, so the candidate hash belongs to a later verification record, not here.
- No push, no pull request, no branch was published to any remote. The branch exists only in this local checkout.
- No tag was created.
- No distribution was built, bound, promoted, or published; no release record, release contract, or `RLS-*` artifact was written or advanced.
- No verification record was prepared, captured, or verified, and no artifact status was transitioned.
- No consumer repository was upgraded. The Mokiterions clone used for the end-to-end reproduction is a throwaway working copy with uncommitted changes; nothing in it was committed, pushed, or merged, and the real `mmzen/Mokiterions` repository was not touched.
- No root managed file was overwritten and no evaluator identity transition was applied to this repository or to any other.
- No external service was contacted beyond reading the already-published 0.6.0 evaluator that was installed before this work began.
- Issue #126 was not closed or edited.

Because `VER-LRE-001` classifies commit-bound verification as `required`, the next accountable action is owner review and authorization of a clean candidate commit for `WO-LRE-001`. Only after that commit exists may an authorized actor capture its ready verification record.
