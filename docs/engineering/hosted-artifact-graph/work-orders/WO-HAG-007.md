+++
id = "WO-HAG-007"
type = "work_order"
title = "Align remote command and unpublished plugin integration checks"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-06"

[execution_scope]
paths = [
  "docs/notes/harnessctl-reference.md",
  "tests/test_cli_shape.py",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py",
  "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-007.md",
  "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-007/"
]

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because later acceptance relies on these command and package checks; assess the combined WO-HAG-001/007 candidate under unchanged VER-HAG-001."
decided_by = "mmzen"

[relations]
implements = ["REQ-HAG-008"]
specifications = ["SPEC-HAG-003"]
architecture = ["ARCH-HAG-001", "ADR-HAG-001"]
verification = ["VER-HAG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-05T16:53:09Z"
decided_by = "mmzen"
reason = "mmzen answered \"I approve\" to the reviewed WO-HAG-007 correction and required commit-bound verification. Reviewed work-order SHA-256 395819937b4f769dda85d713f6b8f5d2675e7cacb0eb7624f3893b1bf97af9f5; exact three-file patch SHA-256 9bbfd310650fb1a71a7099a9099c548b9045098d1b6f7b4fd54a767a983f0cd2. Approved local implementation, checks, commits and combined verification preparation under unchanged VER-HAG-001. Also authorized bounded review publication of combined WO-HAG-001/007 and unchanged approved predecessors to draft PR #535 in mmzen/se_harness, source codex/hosted-artifact-phase1, target codex/hosted-artifact-graph-inputs, retaining original comparison base; includes ready record and later separately supplied verification-decision push. Keep unfinished qualification disclosed. No verification acceptance, merge, force push, retarget, release, public deployment or host-plugin installation is granted."
scope_paths = ["docs/notes/harnessctl-reference.md", "tests/test_cli_shape.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py", "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-007.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-007/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-05T16:54:41Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-06T04:11:23Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed the approved Phase 2 private sandbox and supporting correction. Final product candidate 21d268664ffeb111b8b9e9e94921073c7bc99ec1 has all twelve VER-HAG-001 scenarios observed, with actual native CLI, transaction and restart/restore evidence. Historical failures and raised RISK-HAG-001 remain retained. This records implementation completion only; human verification remains separate."
+++

# Align remote command and unpublished plugin integration checks

## Objective

Make existing command documentation and regression checks correctly cover the
approved hosted sandbox client and its distinct unpublished plugin candidate.

## In scope

- Document candidate `remote` separately from released evaluator commands,
  including explicit service selection, read/write effects and uncertain writes.
- Classify its operation positional argument and required endpoint and credential
  input without weakening existing repository-command checks.
- Select unpublished plugin 0.2.7 as the expected development identity. Keep
  public plugin 0.2.6, evaluator 0.22.1 and their retained public evidence exact.
  Add regressions for host-version disagreement and premature public claims.
- Execute the required regression checks and include the correction in the
  final WO-HAG-001 candidate assessment under unchanged VER-HAG-001.

## Expected change surface

| File | Reason |
| --- | --- |
| `docs/notes/harnessctl-reference.md` | The exhaustive command table omits `remote`, and the local command-shape introduction needs an explicit candidate-client boundary. |
| `tests/test_cli_shape.py` | Its exhaustive classification omits the remote operation family. Keep the existing local positional checks. |
| `tests/plugin_integration/package_assembly/test_refresh_guidance.py` | The shared identity helper treats the unpublished manifest as public 0.2.6. Separate candidate and public expectations and exercise meaningful failures. |
| This work order | Proposed bounded scope and its later actual lifecycle decisions. |
| `evidence/WO-HAG-007/` | Reviewed patch, original failures, commands, regression observations, review and completion evidence. |

The callers `tests/test_progressive_documentation.py` and
`tests/test_public_onboarding.py` need no edits: their existing assertions must
pass through the corrected documentation and shared helper. Product source,
CLI dispatch, plugin manifests and guidance remain under WO-HAG-001. No CI,
assembler, dependency, architecture or accepted-definition amendment is needed.
Future capture allocates the actual VREC and evaluator sidecar paths. Assess
them through automatic admission for records directly verifying this work;
do not preallocate an ID or grant their whole parent directories.

## Out of scope

No new product behavior, released-version change, public-documentation version
claim, source/evidence rewrite, gate waiver, plugin installation, release,
public deployment, force push, branch retargeting or merge.

## Authorized decision envelope

Proposed approval permits local implementation of these three supporting files,
local checks and commits, retained evidence and required commit-bound verification
preparation with WO-HAG-001. It does not reopen or expand the approved hosted
behavior, and it does not approve the eventual result.

Propose review publication for the combined WO-HAG-001/007 candidate and its
unchanged approved predecessors to draft PR #535 in `mmzen/se_harness`, source
`codex/hosted-artifact-phase1`, target `codex/hosted-artifact-graph-inputs`.
This includes the ready record and later separately supplied verification-decision
push. Keep the original comparison base and disclose unfinished qualification.
Human verification acceptance and merge remain separate.

## Constraints

Reuse REQ-HAG-008, SPEC-HAG-003 and VER-HAG-001 unchanged. The governor stays the
separate released 0.22.1 evaluator. A passing documentation or package-identity
check does not prove native plugin loading or hosted-service qualification.
Preserve all prior failures and historical VREC candidate/evidence bindings.

## Proposed assurance classification

Propose `commit_bound_verification = "required"` because later verification
relies on these command and package checks. The human must confirm this
classification with approval. Do not insert an assurance decision before then.

## Required verification

- Run the existing command-shape, progressive-documentation, public-onboarding
  and plugin refresh-guidance suites, including the added distinct failures.
- Run `python scripts/run_tests.py`, distribution validation and CLI smoke.
- Verify that only the three named supporting files change and that the public
  release, observation, root README and marketplace guide bytes are unchanged.
- Run released validation and required scope/handoff checks. Bind the final
  combined candidate and evidence through the existing VER-HAG-001 procedure.

## Evidence to record

Preserve the original three failures, the reviewed patch and its file hashes,
actual command arguments, environments, exits, skips and subsequent corrections.
Use this work order's evidence directory for correction evidence; keep hosted
scenario evidence at VER-HAG-001's existing WO-HAG-001 location.

## Stop and escalate conditions

Stop the affected action for an additional path, altered public identity,
new release/packaging behavior, a changed accepted definition, or a required
failed check. Keep unrelated findings separate and resume independent approved work.

## Completion report format

State the corrected behavior, tested commit, actual checks and limitations,
retained evidence and evaluator-selected next step. No passing subset or
completion transition substitutes for human verification of the final candidate.
