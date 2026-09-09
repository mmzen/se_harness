+++
id = "WO-DST-026"
type = "work_order"
title = "Wave 5, templates: the managed workflow's failure surface, header and pins, the gitignore markers, the environment inventory"
status = "implemented"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the hash-locked workflow and the ignore block that the installer writes into every governed repository, so every consumer upgrade rewrites them, and it amends an approved specification; the next release and this repository's own root adoption rely on its correctness."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/.github/workflows/engineering-harness.yml",
  "se_harness/installer.py",
  "tests/",
  "docs/notes/delegation-class.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/engineering/harness-distribution/README.md",
  "docs/engineering/harness-distribution/evidence/",
  "docs/engineering/harness-distribution/verification-records/",
  "docs/engineering/harness-distribution/requirements/REQ-DST-072.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-073.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-074.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-075.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-027.md",
  "docs/engineering/harness-distribution/verification/VER-DST-027.md",
  "docs/engineering/harness-distribution/work-orders/WO-DST-026.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-006.md",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-DST-072", "REQ-DST-073", "REQ-DST-074", "REQ-DST-075"]
specifications = ["SPEC-DST-027"]
verification = ["VER-DST-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:56:54Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-08 by selecting the presented option 'Approve all three (Recommended)', as a decision distinct from the approval of its definitions in the same transaction. This approval is the delegating act under DR-007 and DR-015: the work order carries [delegation] class = 'execution', so DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE may be applied by the delegated-executor role while the required validate check is success for the exact candidate head, read from the base of the pull request. It authorizes only the declared scope: the standard template of the managed workflow, the installer's fragment writer, the tests, the two notes, the amendment record on SPEC-ECP-006, the domain index and the evidence file. It authorizes no change to any root managed byte, no verification decision, no release, no publication and no adoption; the merges remain the owner's decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-08T21:39:59Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at fd4584ccd47110d137fb87eeea40a2fa0f726724 (check-run 102246942278, source github-checks). Start decided by the delegated-executor role on 2026-09-08 under the execution delegation class WO-DST-026 carries, delegated by the engineering owner in the approval of 2026-09-08 and read at the base of this branch: main at fd4584ccd47110d137fb87eeea40a2fa0f726724, the merge of WO-CIP-007, where the required validate check is success. Branch wo/dst-026-managed-template off main at fd4584cc. This decision authorizes only the declared execution scope: the standard template engineering-harness.yml, se_harness/installer.py, tests/, the two notes, the amendment record on SPEC-ECP-006, the four requirements, SPEC-DST-027, VER-DST-027, this work order, the domain index and the evidence file. It authorizes no change to any hash-locked root managed byte, the lock, the root .gitignore block, the installer's transaction rules, the skills or the gate source's behaviour, and no build, release, publication or adoption. Completion and record preparation are separate decisions of this role under the same gate; verification and every merge remain the accountable human owners."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-08T22:14:12Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at 18af8c09b7d66d331866370078b043cb148a8e6c (check-run 102255329206, source github-checks). Completion decided by the delegated-executor role on 2026-09-09 under the execution delegation class WO-DST-026 carries, delegated by the engineering owner in the approval of 2026-09-08 and read at the base of pull request #420, main at fd4584cc. Rules DST-MWF-001 to -013 of SPEC-DST-027 are met and mapped to evidence in docs/engineering/harness-distribution/evidence/WO-DST-026/WO-DST-026-handoff.md and WO-DST-026-verification.md; DST-MWF-014 is carried to the root-adoption work order of the carrying release. The retained handoff check from fd4584cc completed, nine predicates passing, 11 changed paths in scope, result ae487118 at its fixed point. Released 0.16.0: validate 1,432 artifacts, 0 errors, 44 W013; doctor 97 PASS, every managed path matching; review preflight PASS. Suite 1,098 tests, 11 added, at the Windows baseline; the hosted suite passed. VER-DST-027 scenarios A, B and C ran outside the checkout from a non-promotable candidate wheel: install writes hash markers, doctor passes; a repository initialized by released 0.16.0 upgrades with .gitignore as a fragment update, owner bytes identical, doctor passing, and a block edited inside is refused unchanged; the embedded readers print a refusal and exit with its status on an empty result and judge parsed results as before, no traceback. Lanes: five of five success at the packet head 18af8c09; at 3dda64d1 the managed lane was blocked on QGP-G4I-EVIDENCE only. Every root managed byte is identical to main. Disclosed: the environment inventory reads three names where the rule counted two; an empty result with status 0 fails with 1; no existing test moved; the work order's completion sentence gives the decision to the engineering owner while its approval delegates DR-WO-COMPLETE, and the owner refuses this completion by rejecting the pull request. Completion approves nothing: record preparation is this role's separate decision; verification and the merge remain the human owners."
+++

# Work Order: Wave 5, templates: the managed workflow's failure surface, header and pins, the gitignore markers, the environment inventory

## Lifecycle

This work order carries `[delegation] class = "execution"`: approving it is
the act of delegating `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
to the `delegated-executor` role, each unlocked only while the required
`validate` check is `success` for the exact candidate head (`REQ-ECP-011`,
`SPEC-ECP-006`). The class is read at the base of the pull request, so the
approved packet merges to `main` first and the execution follows on a second
branch. The approval below, the verification of the record it prepares, and
every merge stay human decisions. Commit-bound verification is `required`.

The template half of issue #380 ships with the release after next and is
felt in this repository only at the root adoption of that release; nothing
here changes a root managed byte.

## Objective

Execute rules `DST-MWF-001` to `DST-MWF-013` of `SPEC-DST-027`: the managed
workflow's two check steps surface a refusal as the evaluator's own text, its
header names the steps it runs and its three actions are pinned to commits;
the installer writes the ignore block between hash markers and an upgrade
migrates existing blocks; `SPEC-ECP-006` names `SE_HARNESS_REHEARSAL` and a
test pins the environment inventory.

## In scope

- `templates/repository/standard/.github/workflows/engineering-harness.yml`:
  the status and stderr capture in both `check` steps and the reader's
  empty-file branch (`DST-MWF-001` to `-003`); the header (`DST-MWF-004`);
  the three pins (`DST-MWF-005`).
- `se_harness/installer.py`: `_block` chooses the hash pair for `.gitignore`
  (`DST-MWF-006`); `_extract_block` unchanged in what it accepts
  (`DST-MWF-007`).
- `tests/`: the pins of `DST-MWF-012` and the inventory test of
  `DST-MWF-011`; the existing tests that quote the template's header or the
  HTML markers of `.gitignore`, measured on `main` at `a68caf70` in
  `test_ci_pipeline.py`, `test_harnessctl.py`,
  `test_standard_repository_lifecycle.py` and `test_instruction_architecture.py`.
- The amendment record on `SPEC-ECP-006` (`DST-MWF-009`); the sentence in
  `docs/notes/delegation-class.md` (`DST-MWF-010`); a sentence in
  `docs/notes/harness-installation-and-upgrades.md` on the marker rewrite.
- The domain index and the evidence file.

## Out of scope

- Any byte of this repository's root `engineering-harness.yml`, root
  `.gitignore`, `.engineering-harness.lock` or other root managed file; they
  move at the root adoption of the carrying release (`DST-MWF-013`,
  `DST-MWF-014`).
- The repository-owned workflows (`WO-CIP-007`).
- The markers of `AGENTS.md` and `CLAUDE.md`, which stay HTML comments.
- Any change to the installer's transaction rules, the lock schema, the
  skills under `.agents/`, or the gate source's behaviour.
- Building, releasing, publishing or adopting anything.

## Authorized decision envelope

The shell shape of the capture; the digests of the three pins; whether the
header lists steps in a sentence or a list; where the inventory test lives;
the wording of the amendment record and the two note sentences. The
implementer may not change what the reader decides on a parsed result, add a
new installer mode, touch a root managed byte or widen the scope.

## Constraints

- Read `ENGINEERING_HARNESS.md` and run the review preflight with the
  released 0.16.0 evaluator from its venv outside the checkout before
  completion.
- The candidate suite must pass on the hosted Linux lane; the local Windows
  suite is a control whose skips are labelled.
- The amendment to `SPEC-ECP-006` changes prose only; no rule identifier,
  statement or relation moves.
- Keep the diff free of unrelated changes, and list every test file touched
  in the completion report.

## Expected change surface

About thirty lines in the template; two lines in the installer; one new test
module or class plus the upgrade fixture and about eight assertions changed;
one amendment record; two note sentences; this domain's index and evidence.

## Required verification

`VER-DST-027` in full: the template tests, the reader cases, the install and
upgrade scenarios from a wheel installed outside the checkout, the inventory
test, the two inspections, with outputs retained.

## Evidence to record

`docs/engineering/harness-distribution/evidence/WO-DST-026-verification.md`:
the template before and after, the scenario outputs, the upgrade plan, the
environment inventory, the hosted lane's test report, the local control
reading, the list of test files changed, and the review preflight result.

## Stop and escalate conditions

- The upgrade classifies the unmodified ignore file or workflow as anything
  but a safe rewrite, or moves an owner line.
- A parsed result is judged differently than before the change.
- The amendment to `SPEC-ECP-006` would need more than prose.
- The scope check reports a path outside `[execution_scope]`, or a root
  managed byte is in the change set.

## Completion report format

The evidence file, the changed-path ledger and the handoff `check`
restitution: the template before and after, the scenario A to C outcomes,
the upgrade plan's classification, the inventory, the hosted lane result and
the local control reading each labelled; state that every root managed byte
is identical to `main`; name the adoption obligation `DST-MWF-014` carried
forward to the next root-adoption work order. The completion decision is the
engineering owner's.
