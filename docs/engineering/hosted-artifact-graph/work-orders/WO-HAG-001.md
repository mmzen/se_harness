+++
id = "WO-HAG-001"
type = "work_order"
title = "Remote artifact context and draft authoring through the existing harness"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"

[assurance]
commit_bound_verification = "required"
rationale = "Later pilot, engineering, assurance and release decisions depend on the correctness of changed executable behavior, import fidelity, transaction correctness and evidence bindings. Confirmed through mmzen's approval of the reviewed WO-HAG-001 proposal, whose proposed classification was required."
decided_by = "mmzen"

[relations]
implements = ["REQ-HAG-001", "REQ-HAG-002", "REQ-HAG-003", "REQ-HAG-004", "REQ-HAG-005", "REQ-HAG-006", "REQ-HAG-007", "REQ-HAG-008"]
specifications = ["SPEC-HAG-001", "SPEC-HAG-002", "SPEC-HAG-003"]
verification = ["VER-HAG-001"]
architecture = ["ARCH-HAG-001", "ADR-HAG-001"]

[execution_scope]
paths = ["server/", "se_harness/remote.py", "se_harness/cli.py", "pyproject.toml", "tests/test_remote_client.py", "tests/hosted_artifact_graph/", "tests/test_hosted_artifact_graph.py", "plugins/verity-plane/common/skills/harness-orient/SKILL.md", "plugins/verity-plane/common/skills/change/SKILL.md", "plugins/verity-plane/common/skills/setup/SKILL.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "tests/plugin_integration/test_simple_plugin.py", "docs/notes/hosted-artifact-graph.md", "docs/notes/README.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-001/"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:16:18Z"
decided_by = "mmzen"
reason = "Repository owner mmzen approved the reviewed work order and authorized starting Phase 0 in this conversation. Required commit-bound verification is confirmed as proposed in the reviewed work order. Only confirmed assurance fields were added before this transition; reviewed hashes are retained in the review package and approval binding. This decision targets WO-HAG-001 only, changes no related artifact state, grants no verification acceptance or external publication/deployment, and does not mark the complete work implemented. The user directed retaining Cypher while leaving Memgraph-side read-only enforcement unresolved in RISK-HAG-001."
scope_paths = ["server/", "se_harness/remote.py", "se_harness/cli.py", "pyproject.toml", "tests/test_remote_client.py", "tests/hosted_artifact_graph/", "tests/test_hosted_artifact_graph.py", "plugins/verity-plane/common/skills/harness-orient/SKILL.md", "plugins/verity-plane/common/skills/change/SKILL.md", "plugins/verity-plane/common/skills/setup/SKILL.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "tests/plugin_integration/test_simple_plugin.py", "docs/notes/hosted-artifact-graph.md", "docs/notes/README.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-001/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-04T12:34:26Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Codex starts WO-HAG-001 under mmzen recorded work-order approval and explicit instruction to start, following approval of the reviewed 16-definition package and passing start preflight. Scope and required commit-bound verification are unchanged. Phase 0 contract preparation is complete; this start records no implementation completion, risk acceptance, verification acceptance or external delivery."
+++

# Remote artifact context and draft authoring through the existing harness

## Objective

An agent retrieves the expected context for WO-X at baseline B, submits a valid draft revision through harnessctl, receives correct refusal and accepted-retry results, and reads B unchanged. Implement the complete Phase 2 sandbox path defined by the accompanying Phase 0/1 contracts. This work order is draft; it grants no current implementation or deployment authority.

## In scope

One Python service and one Memgraph store; explicit schema/init and canonical Git importer; immutable revisions and baselines; draft contexts; server admission through the selected released evaluator; atomic guarded writes and receipts; domain reads, MCP and constrained Cypher; packaged remote CLI and plugin guidance; reproducible Docker sandbox; reference fixtures, meaningful failure tests and retained qualification report. Finish the full twelve-step walkthrough, including documentation and actual packaged identities.

## Out of scope

Production deployment, repository authority cutover, hosted human approval/verification/release operations, a new evaluator policy, persistent enrichment, cross-project tenancy, a general graph console, background jobs and synchronization. No accepted historical definition or evidence is amended. No public release, registry upload, host-plugin installation, PR publication or merge is authorized by this work order. Local candidate installation into disposable test environments is part of verification.

## Proposed assurance classification

Propose `commit_bound_verification = "required"`: later pilot, engineering, assurance and release decisions depend on changed executable behavior, import fidelity, transaction correctness and evidence bindings. The accountable human must confirm this classification with implementation approval. The draft deliberately has no `assurance.decided_by`; no identity or approval is inferred from authorship or from the user clarifying Cypher.

## Authorized decision envelope, effective only after approval

The implementer may select maintained Python HTTP/MCP and Memgraph driver dependencies, their pinned compatible versions, module layout within the service, deterministic test fixtures, candidate-only version increments, image pins and private sandbox test ports. Record these actual choices in the component manifest. The implementer may start, implement, make local commits, run checks, retain evidence, record completion and prepare the required VREC under the existing released procedure once authority and gates match. Acceptance and external delivery remain separate decisions.

Do not switch database, remove Cypher, rewrite evaluator policy, change canonical hash schemes, expand authority beyond sandbox drafts or waive a verification case without an accountable scoped decision. The user instruction retaining Cypher and deferring Memgraph-side read-only enforcement is incorporated into REQ-HAG-006 and SPEC-HAG-002. The associated open item remains unresolved; this is not formal risk acceptance or production authorization.

## Constraints

Use one repository, one synchronous service and one authoritative sandbox graph. Invoke the separately installed released evaluator and preserve the current checkout governor. Keep historic path/code/evidence digests intact. Use explicit view and component identities; refuse unsupported inputs and missing evidence. Use a disposable non-sensitive dataset, private database network and loopback service binding. A compatible Docker engine is a test prerequisite; none was found in PATH on the preparation host.

## Expected change surface

| Planned path | Reason and boundary |
| --- | --- |
| `server/` | New dedicated service component: its package/dependency lock, source, schema/init/importer, Dockerfile/Compose, container qualification entry point and component manifest. The directory is new because the current repository has no server. It admits this component only. |
| `se_harness/remote.py` | New standard-library client/command adapter; core local dependencies stay unchanged. |
| `se_harness/cli.py` | Inspected argparse dispatch: add explicit remote namespace without changing existing local behavior. |
| `pyproject.toml` | Existing package and entry-point declarations: minimal candidate version/packaging adjustment only if needed for distinct built identities. |
| `tests/test_remote_client.py` | New CLI/transport failures, retry semantics and compatibility tests. |
| `tests/hosted_artifact_graph/` | New bounded reference fixtures, independent expected values, server scenarios and container qualification helpers. |
| `tests/test_hosted_artifact_graph.py` | New discoverable unittest entry into the hosted test cases; Docker integration has an explicit runnable command and must not be reported passed when skipped. |
| `plugins/verity-plane/common/skills/harness-orient/SKILL.md` | Inspected local orientation guidance: add explicit sandbox remote read selection while retaining existing local route. |
| `plugins/verity-plane/common/skills/change/SKILL.md` | Inspected authoring route: add the bounded remote draft path and unsupported lifecycle boundary. |
| `plugins/verity-plane/common/skills/setup/SKILL.md` | Inspected setup route: document separate candidate client environment and explicit endpoint; do not replace the governor or infer hosted authority. |
| `plugins/verity-plane/codex/README.md`, `plugins/verity-plane/claude-code/README.md` | Existing host package descriptions: document the development combination and only observed host coverage. |
| `plugins/verity-plane/codex/.codex-plugin/plugin.json`, `plugins/verity-plane/claude-code/.claude-plugin/plugin.json` | Distinct candidate plugin versions before packaging changed bytes; no reuse of published 0.2.5 identity. |
| `tests/plugin_integration/test_simple_plugin.py` | Existing plugin packaging and portable behavior tests: cover changed guidance and preserved evaluator/client separation. |
| `docs/notes/hosted-artifact-graph.md`, `docs/notes/README.md` | New runnable sandbox guide and a link from the inspected notes index. |
| `docs/engineering/hosted-artifact-graph/README.md` | Domain index status and links after actual implementation/evidence, without inserting working notes. |
| `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-001/` | Bounded durable qualification records required by VER-HAG-001. |

The existing plugin assembly manifest already includes the selected guidance and host metadata, and its builder can produce inert candidate archives from committed inputs. No builder, assembly manifest, release workflow, CI workflow or repository governor change is planned. The service has its own dependency surface and documented qualification command; existing repository checks remain required. If inspection during implementation identifies a necessary path outside this complete plan, use the existing scope-amendment process before editing it.

The work order's own file and its directly verifying future VREC/evaluator evidence are admitted by existing relationship rules. The VREC ID and paths are unresolved until released capture allocates them; recheck those actual returned destinations then. Do not invent a VREC, authorize an evidence parent directory by implication, or create a release record to fill the plan.

## Required verification and evidence

Execute all VER-HAG-001 scenarios, the actual twelve-step packaged walkthrough and applicable repository regression/distribution checks. Retain exact commands, exits, requests, failure observations, baseline comparisons and component/image/evaluator digests at its prescribed evidence location. Complete drafts and passing structural validation during preparation do not satisfy these implementation checks.

## Stop and escalate conditions

Stop the affected action if the selected evaluator cannot express legitimate draft validation or historical bindings; an accepted definition needs amendment; a planned path is uncovered; required identity or pinned source/evidence is missing; concurrency or canonical serialization cannot meet the stated contract; or application Cypher restrictions cannot reject a discovered bypass. Stop authoritative deployment or exposure to untrusted callers until the database-side read-only item and human-decision authorization are resolved. Retain failure evidence without weakening the contract to obtain a pass.

## Completion report format

Report implemented behavior, exact tested component tuple, actual checks and failures, the twelve-step outcome, baseline preservation and retry/conflict results, evidence locations, unresolved limits and the evaluator's current next step. Identify database-side Cypher enforcement as still open. Preparation, implementation completion, VREC preparation, human verification acceptance, publication and deployment are separate results.
