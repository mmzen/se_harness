# WO-RSK-003 Delegated Skill Amendments Evidence

Date: 2026-08-27

Authority: non-authoritative retained implementation evidence. This file does not approve, verify, release, publish, tag, or deploy anything. It records what was measured on one Windows host at one commit, through the released 0.6.0 evaluator recorded in `.engineering-harness.toml` and installed outside this checkout. Commit-bound assurance for this work order remains a separate `VREC` decision, and this file is not that decision. No hosted lane has yet run on this branch, so every figure below is this host's.

artifact: WO-RSK-003
checkpoint: handoff
formal_snapshot_sha256: dcfb6df5abddd46f0e09f983000899d0b8541b3627e9de08a0b9d76b27e025e2

## 1. Governing packet, authorization, and the two lifecycle transactions

`WO-RSK-003` implements the already approved `REQ-RSK-007` under `SPEC-RSK-002` and `VER-RSK-002`. It adds no requirement and no packet artifact. The owner holds the engineering-owner, quality-owner, technical-owner, requirements-steward, assurance-owner and repository-owner roles in this repository.

Two lifecycle transactions, both through the released 0.6.0 evaluator installed in a virtual environment outside this checkout, because the in-tree CLI refuses these mutations under mutation guard `MG005` on runtime identity:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness transition . \
  --set WO-RSK-003=approved --decision WO-RSK-003=engineering-owner --reason "..." --apply
Workflow transition: COMPLETED
Applied 1 explicit lifecycle transition(s) atomically.
WO-RSK-003 is approved.
```

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness transition . \
  --set WO-RSK-003=in_progress --decision WO-RSK-003=engineering-owner --reason "..." --apply
Workflow transition: COMPLETED
Applied 1 explicit lifecycle transition(s) atomically.
WO-RSK-003 is in_progress.
```

The recorded decision timestamps are `2026-08-27T16:55:16Z` for `draft` to `approved` and `2026-08-27T16:57:13Z` for `approved` to `in_progress`. The owner's instructions were `i approve WO-RSK-003` and `Start`, given in that order and separated by the start preflight below. The two transitions are committed separately from this implementation, as `d1e4c2c` and `12a12d3`.

Start preflight from the same released evaluator, taken between the two decisions:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness preflight . --work-order WO-RSK-003 --phase start
Harness preflight: PASS
Phase: start
Work order: WO-RSK-003 (approved)
```

Its reading manifest resolves `INT-RSK-001`, `CAP-RSK-001`, `REQ-RSK-007`, `SPEC-RSK-002` and `VER-RSK-002`, so the traceability chain behind the amendment is complete. Before approval the same command reported exactly one diagnostic, `W005 status 'draft' is not eligible for start`, which is the correct reading of an unapproved proposal and not a defect.

## 2. Why the approved definitions could not describe the delivery

`REQ-RSK-007`, `SPEC-RSK-002` and `VER-RSK-002` were approved on 2026-08-25 against the schema-v2 skill surface, in which a portable skill wrote governed targets itself. `WO-AEX-006`, `WO-AEX-007` and `WO-AEX-008` replaced that surface with the schema-v3 closed contracts of the delegated execution model, in which the evaluator owns every governed-target write.

Measured in `se_harness/skill_contract.py`, `_parse_v3_contract` refuses every deviation by identifier. The evaluator-client boundary, `SKC036` at line 650, includes:

```python
        or client["bundle_owner"] != "evaluator"
        or client["target_writer"] != "evaluator"
        or _boolean(client["direct_target_writes"], "$.client.direct_target_writes")
        or client["canonical_restitution"] != "required"
    ):
        raise SkillContractError("SKC036", f"evaluator-client boundary differs from the closed {name} instance")
```

The effect surface, `SKC038` at lines 673 and 675:

```python
    if permitted != profile["permitted"] or path_source != profile["path_source"] or lifecycle:
        raise SkillContractError("SKC038", f"effects differ from the closed {name} instance")
    if not _V3_PROHIBITED_EFFECTS.issubset(prohibited):
        raise SkillContractError("SKC038", "closed v3 effect prohibitions are incomplete")
```

`_V3_PROHIBITED_EFFECTS` is `accountable-approval`, `assurance-decision`, `child-delegation`, `credential-use`, `delivery-selection`, `direct-target-write`, `external-action`, `git-mutation`, `lifecycle-authority`, `network-mutation`, `parallel-writer`, `release-decision`, `verification-decision`, `work-completion`. `direct-target-write` is therefore prohibited in every closed v3 contract, and `effects.permitted` must equal the closed profile exactly. The operation lists are pinned the same way by `SKC035` at line 625.

The helpers say the same thing in code, as closed sets:

```text
templates/.../harness-execute-work-order/scripts/check_scope.py:25
ALLOWED_EFFECTS = {"implementation-write", "test-execution", "evidence-write"}
templates/.../harness-draft-change/scripts/guard.py:24
ALLOWED_EFFECTS = {"draft-create", "draft-revise", "planning-note-write"}
```

A `raise-risk` evaluator operation invoked from a skill's own effect plan, and a `risk-raise` permitted effect written directly by the skill, are therefore unrepresentable under this model, not merely unfashionable. `RSK2-SKL-001` required both.

## 3. The delivered contract shapes

Read from the installed contracts through `load_skill_contract`:

```text
harness-draft-change            version 2.0.0
  required_operations  version, identity, doctor, delegated-workflow-catalog, delegated-workflow-execute
  permitted            draft-create, draft-revise, planning-note-write
  lifecycle_transitions []
  target_writer evaluator | direct_target_writes False

harness-execute-work-order      version 2.0.0
  required_operations  version, identity, doctor, delegated-workflow-catalog, delegated-workflow-execute
  permitted            implementation-write, test-execution, evidence-write
  lifecycle_transitions []
  target_writer evaluator | direct_target_writes False

harness-prepare-assurance       version 2.1.0
  required_operations  version, identity, doctor, delegated-workflow-catalog, delegated-workflow-prepare-vrec, risks
  permitted            verification-record-prepare
  lifecycle_transitions []
  target_writer evaluator | direct_target_writes False
```

No contract carries `raise-risk` as an operation or `risk-raise` as a permitted effect, none permits a lifecycle transition, and only `harness-prepare-assurance` moved, by a minor step, because only it gained a required operation.

## 4. What each amendment changed

The form follows the precedent set by `REQ-REB-024`, `SPEC-REB-011` and `VER-REB-010`, amended together under `WO-REB-022` in commit `def1484`: the normative text is edited in place and a `## Amendment record` section is appended as the file's last section, naming what changed, why, and what stands verbatim. As in that precedent, no frontmatter changed in any of the three artifacts; this was checked by parsing each file's `+++` block before and after and comparing byte for byte, which returned identical for all three.

### 4.1 `SPEC-RSK-002` rule `RSK2-SKL-001`

Before:

> `harness-draft-change` and `harness-execute-work-order` gain `raise-risk` in their `required_operations` and one procedure sentence each: a risk noticed during the procedure is raised with `raise-risk` and reported in the receipt; the skill never disposes. Their `guard.py` / `check_scope.py` admit `docs/engineering/*/risks/RISK-*.md` as an effect path for a new `identified` or `raised` risk only.

After: the two skills gain one procedure sentence each and nothing else; the risk is one more canonical destination in the same change plan, admitted while `identified` or `raised`, named in the receipt, and written by the evaluator through the change bundle; neither skill gains an operation, an effect class, or a risk-specific admission rule; the path is admitted by the standing scope exception of `REQ-RSK-006` under the existing `draft-create` and `implementation-write` effect classes; and both helpers keep their closed `ALLOWED_EFFECTS` sets, in which a `risk-raise` effect class is refused before the evaluator is called.

### 4.2 `SPEC-RSK-002` rule `RSK2-SKL-003`

Before:

> Contract `version` fields advance (patch); the portable-core manifests in `tests/fixtures/agentic_execution/canonical_vectors.json` are regenerated; the Claude adapters are unchanged.

Wrong on three counts. Only `harness-prepare-assurance` changes, because only it gains a required operation; the other two contracts must stay byte-identical, since a `version` move with no contract change would be a false digest. The move is minor, not patch, because a required operation is added. And `tests/fixtures/agentic_execution/canonical_vectors.json` does not exist: the live fixture is `tests/fixtures/agentic_execution/phase4/skills/portable-vectors.json`, `tests/fixtures/agentic_execution/host_activation/expected_surfaces.json` follows the version, and `tests/fixtures/agentic_execution/phase3/portable_vectors.json` is a frozen historical record that `tests/test_agentic_execution.py` pins against phase 4's own `previous` values, so regenerating it would falsify history rather than update a fixture.

### 4.3 `VER-RSK-002`, the `RSK2-SKL-001/002` matrix row and acceptance scenario 2

Before:

> | `RSK2-SKL-001/002` | skill contract, trigger, and sentinel tests | raise inside the execute skill; attempted dispose; prepare-assurance packet | raise admitted for new risk files only; dispose stopped; packet carries the register |

> 2. Execute skill raises a risk mid-procedure; receipt names it; handoff blocked by `QGP-G4I-RISK`.

There is no `raise-risk` operation and no `risk-raise` effect class to exercise, so the approved method named tests that cannot be written and a pass condition that cannot be observed. The amended row requires both directions at the helpers' real entry points: a risk path admitted under `implementation-write` and `draft-create` and reaching the evaluator, and a `risk-raise` effect class refused by identifier, `AEXEXE005` and `AEXDRF003`, before the evaluator is called. It adds two checks the approved row did not ask for: that no contract permits a `risk-raise` effect, and that no contract permits any lifecycle transition. The amended scenario adds that the plan is admitted with no scope decision, and keeps the `QGP-G4I-RISK` handoff block.

### 4.4 `REQ-RSK-007`, required-response bullet three and the failure-behaviour acceptance example

Before:

> `harness-draft-change` and `harness-execute-work-order` may invoke `raise-risk` from within their closed effect plans; `harness-prepare-assurance` includes the register for the selected work orders in its assurance packet; no skill disposes. Contract versions and the canonical vectors are updated.

> **Given** the execute skill's effect plan admits `raise-risk` / **When** the plan also admits a `transition` on a risk / **Then** the skill's guard rejects the plan before any effect.

The bullet now states the obligation and leaves the mechanism to `SPEC-RSK-002`, adds that no skill holds a risk-raising effect class at all, and narrows the fixture claim to the affected contract version and the portable-core digests. The example is restated because a plan that "admits `raise-risk`" is not constructable, so it could not be run as written; the amended example asserts the same refusal against a plan that is.

The `statement` field is unchanged and needs no amendment. It requires the system to "let the draft-change and execute-work-order skills raise risks", which is true of the delivery and does not depend on which component performs the write.

## 5. What is unchanged

`RSK2-SKL-002`, `RSK2-GRD-001`, `RSK2-DOC-001`, `RSK2-AMD-001`, `RSK2-AMD-002` and `RSK2-AMD-003` are delivered exactly as approved and are untouched, as are `SPEC-RSK-002`'s scope and failure-behaviour statements. In `VER-RSK-002`, the `RSK2-GRD-001`, `RSK2-DOC-001`, `RSK2-SKL-003` and `RSK2-AMD-001..003` matrix rows, acceptance scenarios 1 and 3, and the pass criteria are unchanged; the `RSK2-SKL-003` row still verifies that the regenerated digests equal `build_skill_manifest` and that the adapters are unchanged, which holds of whichever fixture file carries them. In `REQ-RSK-007`, the `WHEN` statement, `verification_method`, the rationale, the preconditions and trigger, the first, second and fourth required-response bullets, the failure and boundary behaviour, the constraints, the normal-behaviour acceptance example, and the empty open-decisions section are unchanged.

No rule is added, removed, renumbered or reordered. No pass condition is weakened, no evidence obligation is removed, no refusal is downgraded to a warning, and no waiver is introduced. `WO-RSK-002`, its execution scope and its retained evidence are untouched, as are `SPEC-RSK-001`, `REQ-RSK-001` through `REQ-RSK-006`, `VER-RSK-001`, `CAP-RSK-001`, `INT-RSK-001`, `ARCH-RSK-001` and `ADR-RSK-001`. No path outside `docs/engineering/risk-management/` changed, and no executable behaviour, managed policy, contract, fixture, test or note is in this work order's scope.

## 6. The record that cannot be superseded

`VREC-RSK-002` is `verified` and binds commit `2d64df052482b0626c6c2c691ae72926877e1eea`. Its recorded verification reason accepted "the explicit risk-raise effect class in the skill helpers, profiles, and contracts", which the re-expression under the delegated model removed. The record therefore no longer describes what the branch delivers.

It cannot be corrected, re-pointed, or superseded. `docs/engineering/WORKFLOW.json`'s `transitions.verification_record` has exactly one key, `ready`, whose targets are `verified`, `rejected` and `superseded`; `verified` is not a key, so no edge leaves it. Measured, dry run, no `--apply`:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness transition . \
  --set VREC-RSK-002=superseded --decision VREC-RSK-002=assurance-owner --reason "..."
Workflow transition: FAILED
Blockers
- [WEX201] transition VREC-RSK-002: verified -> superseded is not allowed
```

The `verification-supersession` packet governs only a stale `ready` record; its own README states that a superseded record must name exactly one distinct `verified` or `released` successor, and the implemented edge is `ready -> superseded`.

`VREC-RSK-002` therefore stands as the accountable verified fact about `2d64df0`, which is still an ancestor of this branch, so no provenance is orphaned. The route forward is an ordinary **additional** record covering `WO-RSK-002` and `WO-RSK-003` at a shared clean candidate commit off `main`, not a correction: measured across `docs/engineering`, 100 work orders in this repository are already covered by more than one verification record. That record is a separate governance act, taken outside every work order because a record cannot contain the hash of its own commit, and this work order's scope excludes every verification record deliberately. This file decides nothing about it.

## 7. Verification results on the amended tree

All figures from this Windows host, at the amendment state, against the merge commit `e7fd885` as the baseline.

```text
python scripts/run_tests.py
Ran 1009 tests in 88.101s (119 classes, 8 workers)
OK (skipped=24)
```

Identical to the baseline's 1009 OK with 24 skipped. The amendment is documentation only, so no test count moves and none should.

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness validate .
Engineering artifact validation: PASS
Artifacts: 986 | Errors: 0 | Warnings: 53
Planes: structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W53
```

The baseline at `e7fd885` read 985 artifacts, 0 errors, 53 warnings. The one added artifact is `WO-RSK-003`; no warning is added and none is lost. The root candidate validator agrees exactly.

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness doctor .
0 FAIL
```

The in-tree candidate `doctor` reads 50 FAIL, which is candidate-versus-released template skew already recorded on the merge, not a defect of this work order.

```text
python templates/repository/standard/scripts/validate_engineering_artifacts.py --root .
Artifacts: 986 | Errors: 0 | Warnings: 484
```

484, exactly the baseline's figure. This is the only validator carrying the `W-AUT-*` authoring advisories, and a prose-only amendment moves none of them. The three pre-existing `W-AUT-002`, `W-AUT-003` and `W-AUT-004` advisories on `REQ-RSK-007` all concern its `statement` field, which this work order does not touch, so they neither move nor clear.

```text
python scripts/validate_release_distributions.py --root .
SE Harness release distribution validation: PASS (3 distribution-bearing records)
```

`git diff --check` is clean and no file carries a mixed line ending: every amended file was edited byte-wise and asserted to have equal `\n`, `\r\n` and `\r` counts afterwards.

## 8. Handoff check

The `harnessctl check . --artifact WO-RSK-003 --checkpoint handoff` schema-2 block with the complete changed-path set is recorded in section 9, appended after this file was written, because the file is itself one of the changed paths. The formal snapshot digest ignores retained evidence, so the digest bound at the head of this file holds across that append.

## 9. Handoff check, schema-2 restitution verbatim

Run from the released 0.6.0 evaluator outside the checkout, over the complete six-path changed set, with `--changes-complete`:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness check . \
  --artifact WO-RSK-003 --checkpoint handoff --changes-complete \
  --changed-path docs/engineering/risk-management/README.md \
  --changed-path docs/engineering/risk-management/evidence/WO-RSK-003-delegated-skill-amendments.md \
  --changed-path docs/engineering/risk-management/requirements/REQ-RSK-007.md \
  --changed-path docs/engineering/risk-management/specifications/SPEC-RSK-002.md \
  --changed-path docs/engineering/risk-management/verification/VER-RSK-002.md \
  --changed-path docs/engineering/risk-management/work-orders/WO-RSK-003.md
```

```text
Outcome
Completed.

Done
- Evaluated handoff compliance for WO-RSK-003.

Not done
None.

Current lifecycle state
- WO-RSK-003 is in_progress.

Decision required
engineering-owner must decide whether the authorized implementation and evidence are complete for WO-RSK-003 under DR-WO-COMPLETE; permitted outcomes: implemented, continue, reject.

Next
whether the authorized implementation and evidence are complete (PROC-WO-IMPLEMENT/STEP-WO-IMPLEMENT-DECIDE).

Command or response
Mark WO-RSK-003 implemented.
```

result_sha256: 09791f0597e281a6ce950365139f28014eccdbdeb5d121e75a72c73cefb24d3d

The released 0.6.0 evaluator does not emit `result_sha256`; the field is candidate-only, and `restitution_digest` does not exist in the installed 0.6.0 package. The digest above is therefore computed over the *released* evaluator's own JSON block with the candidate's `se_harness.workflow_result.restitution_digest`, and it equals the value the candidate 0.7.0 CLI reports for the same invocation, character for character. Both evaluators render the same restitution block for this checkpoint.

The `--changes-complete` assertion is evidence, not trusted proof, as the command's own contract says. The six declared paths are exactly this work order's `execution_scope`, and `git status` reports no other modified or untracked file.

The gate result is `QG-G4-IMPLEMENTATION-EVIDENCE` pass, `WFL-WO-IMPLEMENT`, `PROC-WO-IMPLEMENT`, current step `STEP-WO-IMPLEMENT-DECIDE`. Governing scope resolved as `CAP-RSK-001`, `INT-RSK-001`, `REQ-RSK-007`, `SPEC-RSK-002` and `VER-RSK-002`, with no dependencies. `findings.scoped_blockers` and `findings.repository_blockers` are both empty; `unrelated_count` is 53, the repository's standing maintenance warnings. `mutation.writes` is empty, so the check wrote nothing. `state.before` and `state.after` both read `WO-RSK-003 is in_progress`.

The formal snapshot digest in the passing result is `dcfb6df5abddd46f0e09f983000899d0b8541b3627e9de08a0b9d76b27e025e2`, the same value bound at the head of this file and the same one the check reported before this file existed. That confirms in measurement what section 8 asserts: the formal snapshot ignores retained evidence, so the binding survives this append.

The remaining decision is the engineering owner's under `DR-WO-COMPLETE`. This file does not take it.
