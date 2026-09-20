# SE Harness workflow and enforcement assessment

Critical review of the engineering workflow, executable controls and agent instructions

16 September 2026 | Repository `mmzen/se_harness` | Commit `f05c478a29c39f94968fdc842a34c861d30a42ac`

## 1 Assessment

**SE Harness provides substantial checks on the consistency of engineering records. Its control of agent behavior and decision authority is much weaker.** It can establish that records are well formed, related, in admissible states, and bound to particular inputs. Several stronger claims still depend on the agent and repository owner following instructions: that approval came from the right person, that implementation stayed inside the approved behavior, that tests actually passed, and that assurance was independent.

This is a useful foundation for cooperative engineering. It is not sufficient, by itself, to constrain an agent that skips steps, confuses a declaration with an observation, or can edit both implementation and its authorization records. The key weakness is that an actor can often supply the facts used to authorize that actor's next action.

The most consequential findings are:

- **Approval is largely asserted.** The released evaluator applied a definition approval using an unrelated actor label. A locally authored work-order approval event was accepted without any Git history or authenticated approval.
- **Evidence presence can be mistaken for successful verification.** A handoff passed with a referenced file explicitly stating that tests had not run. A second case rebound a stale packet to changed code, preserved its failure text, and also passed.
- **Completion can skip the stronger handoff checks.** An out-of-scope edit failed the Git-based handoff, but the same work order could then be marked `implemented` through the released evaluator.
- **The real integration barrier is narrower than the process description.** The live default-branch rules require the `validate` check and a PR, but zero approving reviews. Candidate test jobs are not required by the inspected effective rules.
- **Some instructions disagree with the executable route.** Start and completion ownership are described differently in different parts of the workflow guide. A selected transition check can pass while the transition planner refuses an unrelated graph error.

These findings are not an allegation that existing decisions were fabricated or releases were defective. They show what the current controls do and do not prove. A green result should be described by its actual predicates, rather than by the broader name of its gate.

**Scope.** This review covers the pinned 0.18.0 evaluator, the checkout's 0.19.0 candidate source, supplied policy and plugin instructions, CI definitions, and read-only observations of live GitHub controls. All behavioral experiments used disposable fixtures outside the clone. No product records, repository settings, branches, or releases were changed. This report is an external assessment, not a formal harness lifecycle result.

## 2 The workflow the harness intends to establish

The central idea is to put engineering intent and authority into versioned records, then treat code and tests as implementation and evidence. Markdown files contain TOML metadata defining identity, state, owners, and typed relations. The graph is more important than file proximity: a filename, conversation, commit message, or dashboard connection does not substitute for a declared relation. [S01, S02]

### The records and their jobs

| Record | Purpose | Accountable decision |
| --- | --- | --- |
| INT and CAP | Desired outcome and capability | Product or domain owner |
| REQ | Observable requirement | Product or domain owner |
| SPEC, ARCH and ADR | Contract, applicable architecture and significant design decisions | Technical owner |
| VER | Verification contract and acceptance approach | Assurance owner |
| WO | Bounded implementation scope, paths and assurance classification | Engineering owner approves scope; executor carries out authorized work |
| VREC | Evidence associated with selected work and an exact candidate commit | Assurance owner verifies or rejects |
| REL and RLS | Release contract and candidate-specific release record | Release owner |
| OPS | Continuing operational assurance | Service owner |
| DEC and RISK | Explicit unresolved decisions and threats | Owner accountable for the affected artifact or decision |

Architecture is conditional; the policy explicitly rejects inventing ARCH or ADR records for routine work. Commit-bound verification is classified as `required` or `not_required`. This is not an instruction to generate every artifact for every change. [S02, S03]

### The intended sequence

1. **Orient and establish the evaluator.** Read the repository instructions, managed contract and operating card. Use the selected released evaluator in an isolated environment. Run integrity checks and obtain the selected reading manifest.
2. **Define the change.** Draft or amend the governing records, verification approach and work order. Resolve blocking decisions and obtain the relevant definition and scope approvals.
3. **Start approved execution.** Confirm the recorded execution grant, unchanged scope and start preflight. Explicitly move the selected WO from `approved` to `in_progress` under that grant.
4. **Implement and retain observations.** Change admitted paths and behavior, run repository checks, preserve evidence, and evaluate the implementation handoff against the change set.
5. **Complete implementation.** Move the selected WO to `implemented` when its required predicates pass. Ordinary covered execution should not need repeated owner permission.
6. **Prepare and decide assurance.** Where required, commit a clean candidate and prepare a `ready` VREC binding the selected WOs, VERs, candidate and retained evidence. An assurance decision changes that VREC only.
7. **Choose delivery.** Repository integration and release preparation are distinct choices. Prepare a `ready` RLS from eligible verified coverage and one candidate identity; the release owner separately decides it.
8. **Authorize each external effect.** Merge, tag, publish, deploy and operate only under the authority and controls for that exact action and destination. A released record does not itself perform these actions. [S01, S03, S04, S17]

The core state paths are `WO: draft -> approved -> in_progress -> implemented`, `VREC: ready -> verified`, and `RLS: ready -> released`. Rejection and applicable supersession paths also exist. WO verification or release states require their own explicit transitions; VREC and RLS decisions must not silently synchronize related records. [S04]

A VREC or RLS must live in a later governance commit than the candidate it names: a record cannot contain its own commit hash. This is logically sound but introduces a practical distinction between the tested candidate and the later commit carrying its decision records. [S03, S14]

## 3 Where enforcement actually lives

There are three different kinds of control: instructions that the agent is expected to follow, predicates enforced when a harness command runs, and external controls enforced by the host or server. They should not be presented as interchangeable.

| Obligation | Actual mechanism | Practical limit |
| --- | --- | --- |
| Load and obey the workflow | AGENTS router and explicit plugin skills | No automatic session or before-tool hooks in the reviewed plugin |
| Keep managed policy intact | Locked managed files and fragments; evaluator identity checks | Detection and refusal at checks, not prevention of ordinary edits |
| Maintain a valid formal chain | Metadata, relation, coverage and lifecycle validation | Does not establish that prose is correct or that code implements it |
| Act only with approval | Actor text, lifecycle events and scope comparisons | No authenticated identity boundary for ordinary definition approvals |
| Stay inside scope | Path comparison; Git-derived or caller-declared change set | Path scope is not behavioral scope; declarations can omit changes |
| Supply implementation evidence | Nonempty referenced file or matching packet header | Passing tests and evidential relevance are not inferred from the body |
| Complete work correctly | Transition-specific predicates | Completion does not consume the full path/completeness handoff result |
| Bind a candidate | Clean-tree and commit identity, relations, snapshots, evaluator evidence | Provenance identifies inputs; it does not certify their adequacy |
| Integrate through CI | PR check and GitHub ruleset | Observed required checks and review policy are limited |
| Keep delivery independent | Skill instructions, publishing workflow and environment settings | Depends on the actual credential route and configured server controls |

**Interpretation:** the implementation is strongest where a fact has a deterministic representation: IDs, states, paths, hashes, relation sets and evaluator identity. It is weakest where a human fact is represented as a writable string: approval, accountability, successful testing and independent judgment. [S05-S13, S16-S19]

## 4 Findings that materially weaken enforcement

Severity reflects the risk of an incorrect engineering claim being accepted, not a security CVSS rating. "Demonstrated" means observed through unpatched evaluator calls in disposable fixtures. "Observed" means directly read from source or live settings. Proposed agent reactions are inferences, not measured failure rates.

### F1 Decision actors are not authenticated

**High | Demonstrated on released 0.18.0; matching candidate behavior at planning.** A draft intent whose `owners` contained `owner` was approved using `--decision INT-002=unrelated-person --apply`. The command exited successfully and wrote `decided_by = "unrelated-person"`.

For an ordinary definition transition, `validate_edge` validates the actor as nonempty, bounded, single-line text. It does not establish the caller's identity or entitlement to the stated role. VREC and RLS validation have some additional owner-membership checks, and DEC handling has its own checks; these do not create authentication because the corresponding metadata is still repository content. [S05, S06, S15]

**Why it matters for an LLM:** a suggested command containing an owner label can look like a usable authorization token. The skill correctly warns that it is not. Enforcement therefore depends on the model remembering that distinction while executing a command that is technically accepted. [S17]

**Repair:** separate authenticated principal, accountable role and recorded display name. Where real authority is required, validate an approval obtained through a protected channel and bound to the reviewed artifact bytes, target state and candidate. Preserve a lightweight local assertion mode, but label it explicitly as an assertion.

### F2 Approval binds writable path metadata more strongly than approved behavior

**High | Demonstrated.** An engineering-owner approval event inserted locally into a synthetic WO was accepted as an execution grant before the fixture had a Git repository. Appending a new behavioral instruction to the same WO, without changing its paths, still permitted handoff evaluation to pass.

`_approved_scope` accepts the latest matching event's `scope_paths` directly for current-format approvals. The grant comparison checks that table against `execution_scope`. Older approvals without that field may be recovered from Git history; that history lookup is not a general authenticity check for current events. The approval snapshot does not bind the full WO body or its governing specification bytes. [S07]

The lifecycle validator checks internal event continuity and timestamps when events exist, while allowing historical artifacts without events. It does not, in that function, compare the current event history with a protected earlier version. An internally consistent record can therefore be changed without proving preservation of the original decision. [S06]

**Repair:** bind approval to the approved behavioral contract and governing revisions as well as path scope. Check approval and history changes against a protected base or append-only decision service at integration. Define precisely which changes preserve the grant and which require amendment. Do not make all in-scope implementation edits invalidate scope approval.

### F3 Evidence gates can pass failed or stale observations

**High | Demonstrated through two independent evidence paths.** A referenced evidence file containing `FAIL: the required tests did not run; there is no passing test result.` passed the implementation handoff. The predicate checks file existence, safe location and nonempty bytes. It does not interpret a result or require a command execution record. [S08]

The header-based path has a different problem. After changing an admitted source file, a Git-derived handoff updated an existing packet's `formal_snapshot_sha256`, preserved its stale failure body byte-for-byte, and passed. The check runs `rebind_handoff_packet` before evaluating evidence freshness. No tests were rerun by that operation. The digest now describes a current binding, not necessarily an observation made against the current inputs. [S09, S10]

This is not a claim that hashing is broken. It is a mismatch between what the hash proves and what "Fresh retained evidence" can suggest. Even a newly generated packet body contains only an owner-authored evidence placeholder until useful observations are added.

**Repair:** separate evidence attachment from observed test execution. Retain immutable run records containing candidate, input digests, exact argv, tool identity, exit status and output digest. Rebinding an attachment must not advance the observed test candidate. Define which checks are required by the VER and assess their outcomes. The candidate also has an explicit committed-candidate capture path that runs a supplied test command; that is a useful building block, but adequacy of the selected command still needs a contract. [S14]

### F4 Completion can proceed after a failed scope handoff

**High | Demonstrated with a real released mutation.** The fixture changed both `src/exact.py` and `src/outside.py`, with only the former admitted. `check --checkpoint handoff --from-git HEAD` failed on the outside path. Immediately afterward, `transition --set WO-AUD-001=implemented --decision WO-AUD-001=executor --apply` succeeded.

The contract deliberately excludes changed-path completeness and path matching from the transition to `implemented`, because that command does not receive the change set. It checks a subset of the handoff predicates and does not require a retained successful handoff bound to the current diff. This is a procedural gap between two individually functioning commands. [S10, S11]

Git-derived CI scope checking can still catch the outside path at integration. That is useful later detection; it does not make the local `implemented` claim reliable or stop dependent local work from proceeding.

**Repair:** make completion derive and evaluate the current change set, or require and verify a successful handoff result bound to the exact candidate, baseline, selected WO and input digest. Reject absent, failed, stale or differently scoped handoffs.

### F5 Live integration does not require independent review or candidate tests

**High | Observed in the effective GitHub rules on 16 September 2026.** The active default-branch ruleset requires a PR, prevents deletion and non-fast-forward updates, and requires `validate` from integration ID 15368. It requires **zero** approving reviews, no code-owner review, no last-push approval, and no stale-review dismissal. Strict up-to-date status checking is false. A repository-role bypass is allowed in PR mode. [S18]

The candidate-source suite and package checks exist in `candidate-evidence.yml`, but their job names do not appear in the observed required-status list. The sole required `validate` job runs the released governance evaluator and scope check; it is not the complete candidate test suite. Thus, the server policy does not establish that candidate regression passed or an independent person reviewed every merge. This describes configured enforcement, not an observed bad merge. [S12, S13]

PyPI is better protected in one respect: its environment has a required reviewer and permits deployment from `main`. However, `prevent_self_review` is false, so that setting alone does not establish separation between initiator and approver. The release and plugin-marketplace rulesets were disabled when inspected. [S18, S19]

**Repair:** require the candidate evidence jobs that define acceptance, then configure review and bypass policy to match the intended independence. If a sole owner may exercise several roles, document that trust model honestly. Independently protect credentials and every supported publication route.

### F6 A writable CI definition can still look like a healthy installation

**High for adversarial enforcement; medium for cooperative operation | Demonstrated locally.** Replacing the supplied harness workflow with a job that only executes `echo pass` left `doctor` successful. The workflow is intentionally an editable seed; seed checks verify its presence/state, not agreement with the released template. Managed-router tampering, in contrast, correctly failed `doctor`. [S03, S12, S16]

Editable CI is a reasonable extension point. The missing guarantee is independent protection of that extension point. Requiring a check name does not itself prove that the expected checker ran. The live lack of required code-owner review and approving reviews makes this boundary especially important. No workflow-bypass merge was attempted.

**Repair:** enforce the trusted evaluation entry point outside the proposed change, or protect workflow and policy updates with dedicated review and server-owned execution. Expose CI conformance as a separate readiness result; do not imply that an installation-health pass attests to integration enforcement.

## 5 Where the workflow confuses the agent

### F7 The same guide assigns start and completion differently

**High for instruction reliability | Observed contradiction.** `DECISION_RIGHTS.md` DR-015 authorizes an executor to start, implement, check, commit, record completion and prepare verification under WO approval without renewed permission. The workflow's approved-execution section agrees. Yet its end-to-end step 5 says to receive an explicit start decision, and step 7 assigns marking the WO implemented to the engineering owner. [S04]

An explicit executor transition can reasonably be called a start decision, but the text does not make that distinction clear. The completion-owner discrepancy is more direct. One agent may repeatedly seek approval; another may treat the general execution grant as permission to decide matters reserved to an owner.

**Repair:** generate one role/action/authorization table from the executable contract. State, for each action, whether it reuses WO approval or requires a new accountable decision. Generate the corresponding procedure prose and verify meaning through behavior tests, not only string-level documentation checks.

### F8 Selected checks and transition planning disagree about unrelated failures

**Medium | Demonstrated in both evaluator versions.** Introducing an unrelated draft intent with an empty owners list left `check --artifact WO-AUD-001 --checkpoint transition --target implemented` successful. Planning the same transition failed because the planner rejects any current graph error before scoped gate evaluation. [S05, S10]

This conflicts with the promise that unrelated work should not block the selected scope absent a dependency or repository-wide integrity problem. It also undermines the claim that the transition checkpoint previews what transition will evaluate. The agent receives a legal-looking next step and then a refusal for a different scope.

**Repair:** centralize the blocking-error classification used by projection, checkpoint evaluation, plan and apply. Preserve genuinely global blockers, such as duplicate identities, while making other scope differences explicit in the result.

### F9 The word check covers substantially different operations

**Medium | Observed and partly demonstrated.** Checkpoint-free `check` projects state, procedure and next action; it does not evaluate the gates. The `scope` checkpoint assesses path scope without execution authority. The Git-derived `handoff` checkpoint may write evidence headers and retain `handoff.json`. These are different assurances and side effects behind one verb. The notes explain this accurately, but an agent can easily retain the simpler belief that "check passed" means readiness or that a check is always read-only. [S09, S10, S20]

The same risk appears in gate names. `QG-G4-ASSURANCE-DECISION` principally checks graph, integrity and open-decision conditions. Its name is broader than those machine predicates. It does not mean that an independent reviewer understood the tests and judged the requirements satisfied. [S11]

**Repair:** put `evaluation_mode`, `gates_evaluated`, `evidence_origin`, `authority_verified` and `writes_performed` prominently in the result. Render explicit statements such as "Projection only; readiness not evaluated" and "Evidence available; test success not assessed." Never ask the model to infer the scope of a green result from a gate title.

### F10 Reading and version boundaries impose a substantial memory burden

**Medium | Measured burden; agent failure risk inferred.** At the inspected commit, the nine central instruction/policy Markdown files total **95,114 bytes**. Actual review manifests contained 10 files / 48,718 bytes for WO-CIP-006, 21 files / 151,076 bytes for WO-DST-023, and 12 files / 49,985 bytes for WO-KIS-009. These are byte counts of the local checkout, not tokenizer measurements. The formal graph contains 1,652 artifacts.

The instructions require entry reads, phase reads, relevant authoring policy and rereading after compaction. Rules also exist in editable prose, locked JSON, packaged executable contracts, plugin references, owner instructions and historical notes. The root selects 0.18.0 while candidate source declares 0.19.0. That separation protects the evaluator from candidate self-modification, but it also makes a plausible in-tree command the wrong authority for a mutation. [S01, S03, S17]

Other ambiguity traps include VER versus VREC, REL versus RLS, a ready record versus an approved decision, approved scope versus a proposed next action, and actor identity versus an accountable role. The three-digit sequential IDs must be unique across concurrent work; the instruction to inspect every ref reduces collisions but cannot reserve an ID against another agent doing the same thing. [S03]

**Repair:** produce a small, versioned phase brief that separates immutable constraints, selected inputs, existing authority, unresolved decisions, effects and the next command. Keep full source links and digests for expansion. Add a cross-session ID allocation strategy. Test fresh and compacted sessions on task-level outcomes, including refusal accuracy and unnecessary approval requests, rather than merely successful command replay.

## 6 What deserves to be preserved

The assessment should not flatten the harness into "just prompts." There is significant executable engineering here.

- **A coherent data model.** Typed relations, state vocabularies, coverage and decision/risk records make implicit engineering assumptions inspectable.
- **A separate released evaluator.** Private runtime selection, payload identity, managed policy hashes and mutation guards materially reduce accidental candidate self-validation. The inspected root passed the exact released evaluator's `doctor` and graph validation.
- **Meaningful failure behavior.** Out-of-scope Git changes and managed-file tampering were rejected in the probes. Unknown or unsafe paths and missing assessable inputs have explicit refusal paths.
- **Explicit effects and non-effects.** Preparing a record is distinct from deciding it. VREC and RLS transitions do not automatically synchronize their WOs. Typed argv helps prevent shell-boundary ambiguity.
- **Useful provenance.** Exact candidate identities, clean-tree capture, verification-contract equality, release coverage checks and retained evaluator evidence are real controls. Their evidential meaning needs tighter language, not removal.
- **Honest plugin limitations.** The plugin says it has no automatic session or before-tool hooks and that ordinary edits use host permissions. Its authority guidance explicitly rejects actor labels and skill instructions as independent enforcement.
- **A substantial test culture.** The selected run completed 158 tests with one skip and no failures. The repository also distinguishes agent behavioral acceptance from deterministic command replay. [S01, S11, S14, S16, S17, S21]

The target should be fewer unverifiable claims and better composed gates, not a larger vocabulary of process rules.

## 7 Recommended repair sequence

### First make existing verdicts trustworthy

| Priority | Change | Acceptance criterion |
| --- | --- | --- |
| P0 | Bind completion to the full current handoff | The F4 sequence cannot produce `implemented`; changed baseline or inputs invalidate a retained pass |
| P0 | Separate observed test runs from evidence attachments | Failure, missing runs and stale candidates remain failed or unassessed after any rebind |
| P0 | Align live required checks with acceptance | A PR lacking successful candidate regression or required assurance cannot merge through the normal route |
| P1 | Bind approvals to authenticated decisions and reviewed scope | Editing an event, its paths or approved behavior cannot manufacture or silently extend authority |
| P1 | Protect the checker invocation and workflow changes | An altered candidate workflow cannot satisfy the trusted gate merely by producing the same check name |
| P1 | Unify scoped evaluation and simplify instructions | Checkpoint, plan and apply agree on blockers; executor versus owner obligations are unambiguous |
| P2 | Reduce phase context and reserve IDs | Fresh concurrent sessions obtain the same bounded brief and cannot allocate the same artifact ID |

P0 means repair before describing these verdicts as reliable automation barriers. It is not a request to suspend all repository work.

### Define the intended trust model

**Cooperative mode:** the owner trusts the agent to report observations and act within supplied approval. The harness provides structure, auditability and error detection. Actor names and evidence attachments are assertions, and the interface should say so.

**Enforced mode:** an implementation actor must not be able to grant itself approval or replace the relevant evidence and checker. That requires a trusted component outside the actor's writable authority: protected review records, trusted CI, separated credentials, or another authenticated approval mechanism. Adding more MUST statements to Markdown cannot establish this boundary.

No configuration can make an all-powerful repository administrator independently constrained by the same mutable repository. The design should explicitly state whether the repository owner is the trust root and which other actors it intends to constrain.

### Add behavioral acceptance cases that challenge the promises

Retain the cases reproduced here as regression requirements: unrelated actor approval; locally forged approval history; changed behavior with unchanged path scope; failure text as evidence; stale packet rebind; omitted paths under declared completeness; completion after failed handoff; unrelated-error disagreement; and edited CI that still passes installation health.

Add fresh-agent and post-compaction scenarios: user intent conflicts with a suggested command, a plan is mistaken for an applied transition, an earlier approval's candidate changes, an external mutation has uncertain outcome, two agents reserve the same ID, and a green projection is presented as verification. Judge observed calls and effects. Do not treat a scripted replay of expected commands as proof of model compliance. [S21]

## 8 Evidence and verification performed

| Experiment | Released 0.18.0 result | Meaning |
| --- | --- | --- |
| Baseline root doctor and validate | Both exit 0; 1,652 artifacts, zero errors, 48 maintenance warnings | The reviewed root is structurally healthy under its selected evaluator |
| Definition approval with unrelated actor | Applied, exit 0 | Actor label does not authenticate decision authority |
| Unsigned current-format approval in a fixture without Git | Execution grant accepted | Current approval lookup trusts local event content |
| Explicit failed-test text in evidence_paths | Handoff exit 0 | Evidence predicate checks availability, not test outcome |
| Omit outside edit and assert changes complete | Scope check exit 0 | Caller-declared completeness is trusted |
| Derive the same changes from Git | Scope and handoff exit 1 | Git-derived path control works |
| Complete immediately after that failed handoff | Applied, exit 0 | Completion omits the stronger diff predicates |
| Change WO behavior while retaining approved paths | Handoff exit 0 | Path grant does not bind the whole behavioral approval |
| Add unrelated malformed draft | Selected transition check exits 0; transition plan exits 1 | Scope semantics disagree |
| Replace supplied CI with echo pass | Doctor exit 0 | Editable seed integrity does not attest to CI behavior |
| Alter managed router | Doctor exit 1 | Managed-file detection works |
| Change source and rebind stale failure packet | Handoff exit 0; packet body unchanged | Current attachment digest does not prove a current test run |

The corresponding candidate-source probes reproduced the read-only planning and check outcomes. Mutation probes were executed only with the actual released evaluator, with its identity guard enabled. No approval, preflight, evidence or mutation guard was mocked in those experiments. Repository fixture helpers created synthetic input records; they were not used to claim that real owner decisions occurred.

The focused candidate suite comprised `test_workflow_execution`, `test_workflow_compliance`, `test_authoring_gate`, `test_instruction_architecture` and `test_workflow_documentation_contract`: **158 tests run, one skipped, no failures** in about 74 seconds. Some repository unit fixtures intentionally mock boundary checks, so these tests support their asserted units, not an end-to-end authentication claim. The full regression suite, package builds, real publication and adversarial merges were not run.

Initial exploratory probes used the repository helper's legacy WO-001 spelling; preflight refused it. The retained corrected experiment uses WO-AUD-001 and a baseline graph with zero errors. Failed exploratory runs are retained separately to avoid misrepresenting the fixture repair as product behavior.

GitHub settings are a dated observation, not a guarantee about future settings or every possible credential path. The effective rules endpoint was checked, not just the legacy branch-protection endpoint: the latter returned 404, but an active ruleset did protect the default branch. This distinction prevents an incorrect "main is unprotected" conclusion.

The evidence archive contains the probe scripts, raw JSON results, focused test log, root checks, measurements and live-control responses. Experiments can be rerun against the pinned checkout in a fresh scratch directory. No repository patch or server-setting change was applied.

## 9 Source map

Code and document references below are pinned to the inspected commit. Execution findings come from the separately installed released 0.18.0 evaluator and the retained experiment results. A source reference identifies the mechanism; an experiment establishes the observed behavior.

- **S01** [Managed engineering contract](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/ENGINEERING_HARNESS.md#L17): invariants, authority, scoped analysis exemption, handoff and stop conditions.
- **S02** [Traceability policy](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/docs/engineering/TRACEABILITY.md#L12): typed relations and conditional artifact applicability.
- **S03** [Repository instructions](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/AGENTS.md): editable seeds, released/candidate boundary, ID allocation and governance commits.
- **S04** [Decision rights](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/docs/engineering/DECISION_RIGHTS.md) and [workflow procedure](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/docs/engineering/WORKFLOW.md#L127): compare DR-015 with end-to-end steps 5 and 7.
- **S05** [Transition actor validation](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/workflow_edges.py#L82) and [transition planner](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/workflow.py#L433): actor assertions, global error check and explicit writes.
- **S06** [Lifecycle event validation](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/engine/validation_lifecycle.py#L162): optional historical events and internal continuity.
- **S07** [Execution grant lookup](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/gate_source.py#L43): current scope_paths and older Git-history path.
- **S08** [Evidence availability predicate](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/workflow_predicates.py#L38): direct files and matching packet headers.
- **S09** [Packet rebind](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/workflow_evidence_packet.py#L90): header replacement with unchanged body.
- **S10** [Checkpoint evaluation](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/workflow_compliance.py#L207): declarations, change-set preparation, scoped gates and retained results.
- **S11** [Executable quality gates](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/quality_gates_contract.json) and [gate explanations](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/docs/engineering/QUALITY_GATES.md#L27): predicate checkpoints and transition bindings.
- **S12** [Required governance workflow](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/.github/workflows/engineering-harness.yml) and [PR evaluator](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/github_ci.py#L136): live body, scope union and conditional handoff.
- **S13** [Candidate evidence workflow](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/.github/workflows/candidate-evidence.yml#L35): source regression and candidate package lanes.
- **S14** [Verification capture](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/provenance.py#L394): explicit candidate tests, ordinary capture and record provenance.
- **S15** [Evidence and owner validation](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/engine/validation_evidence.py): additional VREC/RLS ownership and metadata conditions.
- **S16** [Installation inspection](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/preflight.py#L195) and [mutation guard](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/se_harness/mutation_guard.py#L135): seed versus managed integrity and released evaluator identity.
- **S17** [Plugin boundary](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/plugins/verity-plane/codex/README.md#L3), [continuing authority](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/plugins/verity-plane/common/skills/change/references/authority.md) and [external actions](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/plugins/verity-plane/common/skills/evidence/references/external-actions.md).
- **S18** [Live main ruleset](https://github.com/mmzen/se_harness/rules/20693381) and [effective branch rules endpoint](https://api.github.com/repos/mmzen/se_harness/rules/branches/main), plus the [ruleset listing](https://api.github.com/repos/mmzen/se_harness/rulesets): observed 16 September 2026; raw responses retained.
- **S19** [PyPI environment endpoint](https://api.github.com/repos/mmzen/se_harness/environments/pypi), [deployment branches endpoint](https://api.github.com/repos/mmzen/se_harness/environments/pypi/deployment-branch-policies) and [publication workflow](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/.github/workflows/publish-pypi.yml#L309): live settings may require repository access.
- **S20** [Check command explanation](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/docs/notes/harnessctl-check.md#L17): projection, checkpoints and handoff side effects.
- **S21** [Agent acceptance versus replay](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/tests/plugin_integration/change_skill/README.md) and [workflow compliance fixtures](https://github.com/mmzen/se_harness/blob/f05c478a29c39f94968fdc842a34c861d30a42ac/tests/test_workflow_compliance.py#L68): scope of behavioral and unit evidence.

## 10 Questions the design needs to answer

1. Is the product intended to help a trusted agent follow a process, or to prevent an untrusted implementation actor from granting itself authority? Which guarantees differ between those modes?
2. What independent observation must exist before the product is willing to say `implemented`, `verified` or `released`?
3. Why should a current snapshot header make old evidence current if no observation has been repeated?
4. Which exact bytes did an owner approve, and which changes preserve that decision?
5. What must the server refuse even if the agent skips every local instruction?
6. Can a fresh agent determine the right action from one bounded, versioned result, without resolving contradictory prose or learning the process through repeated refusals?

Answering these questions and closing F1-F6 would strengthen the meaning of the existing workflow more than adding further artifact types or mandatory prose.
