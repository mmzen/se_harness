# Prepare complete work scope before asking for approval

**Implementation review — draft package — 2 October 2026**

This is the Markdown copy of the HTML review, published at the repository
owner's request so the proposal can be read on GitHub. It is a review snapshot,
not an approval or an instruction to start implementation. The four formal
artifacts remain authoritative for their own content and remain in draft.

## Why

Reduce repeated approvals caused by predictable missing tests, documentation
and evidence paths.

## What changes

- The agent inspects affected code and supporting material before preparing
  the work order.
- A read-only planned-path view of check reports covered, uncovered and
  invalid paths using existing scope rules.
- Preparation explains generated records and unknown future destinations.
- The approval request explains the outcome, checks, limits and permission
  in plain language.

## What success looks like

A bug fix and an instruction change each reach verification preparation under
one unchanged work order in representative fixture demonstrations. An
intentionally omitted planned file is caught before approval.

## Important limit

Coverage checks only the supplied plan. It cannot prove that the agent found
every affected file. Real scope expansion still requires a decision.

## Your approval permits

Approve the four drafts below, confirm required verification tied to the exact
commit, and authorize bounded local implementation, tests, commits, completion
and verification-record preparation. Verification acceptance and external
publication remain separate.

The request to publish this review authorizes this review branch and PR. It
does not record the pending implementation or assurance-classification decision.

## Result at review preparation

Released evaluator 0.21.0: draft validation passed with zero errors. The
selected scope has no validation blockers. The implementation approval check
is blocked by `QGS-ASSURANCE`: the human must confirm the proposed assurance
classification. All four artifacts remain draft. No product implementation
has started.

**Pending decision:** Approve implementation, or request changes.

## Exact review details

Branch: `work/complete-scope-preparation`.

The original HTML review was transient and stored outside the repository.
This Markdown copy is retained here at the owner's explicit request. The
complete reviewed contents are reproduced below without changing the source
artifacts.

| Artifact | Reviewed source | Proposed state |
| --- | --- | --- |
| `REQ-KIS-010` | [REQ-KIS-010.md](../engineering/harness-simplification/requirements/REQ-KIS-010.md) | approved |
| `SPEC-KIS-004` | [SPEC-KIS-004.md](../engineering/harness-simplification/specifications/SPEC-KIS-004.md) | approved |
| `VER-KIS-004` | [VER-KIS-004.md](../engineering/harness-simplification/verification/VER-KIS-004.md) | approved |
| `WO-KIS-010` | [WO-KIS-010.md](../engineering/harness-simplification/work-orders/WO-KIS-010.md) | approved |

The installed authorization procedure states:

> Work-order approval must include confirmation of the assurance classification.

After a matching decision, the agent records the actual human and reruns the
required approval and start checks.

## Complete artifact contents

These are snapshots of the files reviewed before publication. Each SHA-256
below refers to the complete source file bytes, not to this Markdown document.

### REQ-KIS-010

Source: `docs/engineering/harness-simplification/requirements/REQ-KIS-010.md`

SHA-256: `d05553d5844ce31c7127adafc8c27c76eea87cba01dbf3c65f87881d47806e96`

````markdown
+++
id = "REQ-KIS-010"
type = "requirement"
title = "Prepare complete bounded scope before approval"
status = "draft"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
statement = "Before implementation approval, the harness shall help the agent present one complete bounded work proposal, check coverage of its planned paths, and make the human's decision understandable."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "CAP-KIS-001; the repository owner's priority 1 simplification proposal accepted on 2026-10-02"

[relations]
derives_from = ["CAP-KIS-001"]
+++

# Prepare complete bounded scope before approval

## In plain words

The human should review the intended result and the important choices once.
The agent should find foreseeable supporting changes before asking for
implementation approval. A planned-path assessment checks the proposed scope;
it does not prove that the impact analysis is complete.

## Why

Repeated work orders for predictable test, instruction, packaging or evidence
paths interrupt work without adding a new product decision. This change makes
preparation more complete while preserving approval for a real scope expansion.

## Acceptance

1. Preparation inspects the implementation, its callers and references, tests
   and fixtures, documentation, packaging, CI and verification outputs as
   applicable. The work order's existing Expected change surface names the
   planned paths and gives a short reason for each. Non-applicable areas are
   explained briefly.
2. One work order covers one bounded outcome with its necessary supporting
   changes. Exact file paths and narrow component directories use the existing
   admission rules. A directory entry does not authorize unrelated behavior.
3. A read-only assessment of explicitly supplied planned paths distinguishes
   explicit scope, existing automatic admission, uncovered paths and invalid
   inputs. It is usable before work approval. It leaves files and lifecycle
   states unchanged and grants no authority.
4. Preparation explains generated-record admission separately from evidence
   that needs explicit scope. A future record whose ID is unknown is not shown
   as an existing admitted path. Its actual destination is checked when known.
5. The approval request states the decision, reason, expected result, proposed
   changes, checks, material uncertainty and permission being requested in
   ordinary language. Exact artifact IDs, paths and reviewed revisions remain
   available as review details. Existing human decision rights remain intact.
6. A representative bug fix and instruction change reach verification
   preparation in temporary fixtures without another work order for a
   foreseeable omitted path. A deliberately uncovered planned file is caught
   before approval. A real expansion still requires a new human decision.

## Limits

No automatic dependency scanner or claim of exhaustive discovery is required.
No new artifact type, gate, checkpoint, approval right, broad directory
exemption, persistent planning file or universal benchmark is introduced.
Current gate, lifecycle, release and adoption rules remain unchanged.

````

### SPEC-KIS-004

Source: `docs/engineering/harness-simplification/specifications/SPEC-KIS-004.md`

SHA-256: `97b26ae6385c3af06bfd959314ee02203968a8b0b6f1583120d2c081a05a4121`

````markdown
+++
id = "SPEC-KIS-004"
type = "specification"
title = "Complete scope preparation and clear approval requests"
status = "draft"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
contract = "Prepare one bounded outcome with its supporting paths, assess the declared plan using existing admission rules, and request an exact human decision in plain language."

[relations]
specifies = ["REQ-KIS-010"]
+++

# Complete scope preparation and clear approval requests

## Scope and terms

A planned path is a proposed file destination, not an observed change.
Coverage means admission of the supplied paths under the selected work
order's current scope. It does not mean the plan contains every affected file.

These rules extend preparation through existing resources, the work-order
template and the check command. They add no lifecycle edge or checkpoint.
Existing calls without the new option retain their meaning.

## Rules

**KIS-SCP-001 - Inspect before asking.** Before requesting implementation
approval, the agent inspects the affected implementation and follows callers,
references and consumers. It checks supporting tests and fixtures, instructions
and documentation, packaging and CI, and verification destinations where they
apply. It records planned paths with short reasons in Expected change surface.
It briefly explains non-applicable areas and unresolved boundaries. Working
inventories remain transient outside the repository. The work order carries
the durable result; no new planning artifact or mandatory receipt is required.

**KIS-SCP-002 - Bound the complete outcome.** Use one work order for one
independently verifiable outcome, including its necessary supporting work.
Use exact files by default. A narrow existing component directory is suitable
when its files form the affected component and the outcome remains bounded.
Use existing path syntax and matching. No new automatic scope widening,
repository-wide directory grant or authority from a path match is introduced.
If an approved scope must grow, preserve its history and obtain the required
decision. Do not create separate work orders merely for already foreseeable
tests, documentation or evidence belonging to the same outcome.

**KIS-SCP-003 - Assess the supplied plan.** Add a repeatable --planned-path
option to check with an explicit --artifact selecting a work order and no
checkpoint. Each value names one repository-relative file; a missing future
file is allowed. The normal schema-2 lifecycle projection remains authoritative.
Add scope.preparation with the supplied paths, assessment coverage, explicit
matches, automatically admitted matches and their reasons, uncovered paths,
and invalid declarations when assessable. Each covered path identifies the
scope entry or existing admission rule that covers it.

Do not put planned paths in changed_paths, assert change-set completeness,
evaluate gates, select another next lifecycle action, or write files.
The existing projection's operation outcome, next action and exit meaning
remain unchanged. The separate preparation coverage is covered, uncovered,
or invalid. Neither exit zero nor covered is work approval or proof of a
complete impact analysis. Human rendering makes that distinction visible.

Reject mixed use with --checkpoint, --target, --procedure, --changed-path,
--changes-complete, --change-manifest, --from-git or --pull-request-body.
Reject a missing or non-WO selection. Reuse existing path validation and safe
target resolution, including malformed paths, duplicate case variants and
repository escape through links. Invalid inputs must not become covered
matches. Report exact offending paths or options through normal diagnostics.
Preserve unrelated-finding separation and existing result integrity; changes
to the machine planning fields must change the result digest.

**KIS-SCP-004 - Explain generated outputs.** Reuse current admission of the
selected WO's own file, directly linked verification/release records and
their declared evaluator-evidence paths. The assessment identifies these
existing concrete paths without admitting the surrounding directories.
A record linked only to another WO is not admitted by this rule.

When a future record has no allocated identity yet, the procedure explains
that its exact path is unresolved and states the existing relationship rule.
It does not invent a record or claim its future path is covered. Once the
record exists, reassess its actual path. Other evidence, retained reviews,
logs and publication files need explicit scope unless an existing rule
actually covers them. Conditional risk admission during execution remains
unchanged; preparation does not turn it into a blanket future-path grant.

**KIS-SCP-005 - Resolve the plan before approval.** Run the planned-path
assessment for the Expected change surface before the approval request.
Resolve uncovered or invalid paths in the draft or narrow the proposed
outcome. Explain unknown generated destinations and the check to perform
when they become known. Keep a genuine unresolved decision visible; do not
claim readiness from a successful command exit. Follow the existing
validation and authorization procedure for the actual decision.

**KIS-SCP-006 - Present a decision card.** The agent uses one concise request
for the coherent package. Lead with the exact decision and useful outcome.
State why it matters, what changes, what success looks like, material limits
or uncertainty, and what approval permits. Put exact artifact IDs, file
links and reviewed revisions in review details. The primary choices are
Approve implementation and Request changes when implementation is the
decision. Use different words for assurance acceptance or publication.

Describe any separate acceptance or external-action boundary only where it
matters to this decision. Do not mix implementation approval with an
unstated acceptance or publication decision. A yes applies to the exact
reviewed package and requested permission. Reuse actual prior authorization
while those inputs remain unchanged. Do not require the human to type IDs
or understand CLI flags to express that decision.

## Examples

A bug fix changes a parser, its caller, a fixture and its test. All four paths
appear in the proposed WO with reasons. The preparation assessment names all
four matches. An omitted test is reported as uncovered before approval.

An instruction change updates a released procedure, its template, a CLI note
and a documentation contract test. The same WO covers these supporting
changes and its evidence directory. A future linked VREC is explained as an
unresolved generated destination; its linked record and evaluator output are
assessed at their real paths when prepared.

A path under src/component/ matches that component scope. A path under
src/component-extra/ does not. A new request to change unrelated behavior
needs a decision even when its file happens to match an approved directory.

## Design choice and complexity

Reuse checkpoint-free check and its existing schema-2 result. Add one optional
planning view and reuse the established path/admission helpers. This avoids a
new command family, stored inventory, graph, gate or approval mechanism.
The plan is not passed off as a Git change set. The cost is one CLI option,
a small assessment function and rendering/documentation for that view.

No new architecture boundary, dependency, persistence model or trust model
is proposed. No active architecture addresses REQ-KIS-010; separate ARCH/ADR
artifacts are not needed for this bounded extension. If implementation
requires changing those boundaries, return with the concrete scope change.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-KIS-010 | KIS-SCP-001, KIS-SCP-002, KIS-SCP-003, KIS-SCP-004, KIS-SCP-005, KIS-SCP-006 |

````

### VER-KIS-004

Source: `docs/engineering/harness-simplification/verification/VER-KIS-004.md`

SHA-256: `8ec7905235cf9de1b005bd1c0961a933d78d755291c7d0c62af48300175b4fd3`

````markdown
+++
id = "VER-KIS-004"
type = "verification"
title = "Verify complete scope preparation before approval"
status = "draft"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[relations]
verifies = ["REQ-KIS-010"]
+++

# Verify complete scope preparation before approval

## Independence

Expected results come from REQ-KIS-010 and SPEC-KIS-004. Write fixtures with
independently listed planned paths and expected admission reasons. Do not
derive expected coverage by calling the candidate matcher. Reuse existing
scope, lifecycle and fixture helpers where they preserve independent
expectations. Candidate tests exercise future behavior; released evaluator
0.21.0 continues to govern the real repository.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-KIS-010 | test | A: planned paths | Exact files, component children and missing future files are classified correctly; sibling lookalikes and omitted files are uncovered. Each match names its reason. |
| REQ-KIS-010 | test | B: automatic outputs | The selected WO file, directly linked VREC/RLS and evaluator evidence are admitted by existing rules; unrelated records and neighboring evidence are not. |
| REQ-KIS-010 | test | C: refusal and invariants | Invalid paths, case duplicates, escapes, conflicting flags and invalid selection are rejected or reported invalid without writes. No plan becomes an actual diff, gate result or approval. |
| REQ-KIS-010 | test | D: compatibility and integrity | Existing commands retain their meaning and result shape when the option is absent; planning data participates in the digest; one repository validation is reused. |
| REQ-KIS-010 | inspection | E: instructions and request | Discovery, reasons, unknown generated destinations and the plain-language decision card appear at the existing preparation/approval entry points without duplicate policy or extra artifact types. |
| REQ-KIS-010 | demonstration | F: complete outcomes | A bug fix and an instruction change each reach verification preparation in temporary fixture repositories under one unchanged WO; a deliberately omitted planned path is caught before approval and a later real expansion requires a decision. |

## Execution conditions

Run A-D through the public CLI in temporary fixture repositories, including
a draft WO and an approved WO. Check human and JSON output. Snapshot fixture
files before and after read-only assessments. Assert no lifecycle events,
evidence files or Git changes are written. Supply an explicit WO and test
the failure of missing, unknown and non-WO selections.

For B, include an unrelated record and a linked record with its concrete
evaluator-evidence path. A future unallocated record is an explained
uncertainty, not a synthetic admitted path. Test explicit evidence files
separately. Keep existing start, scope and handoff regression tests so that
planning cannot weaken real execution checks.

For C, cover absolute paths, parent traversal, case-duplicate inputs, a
component-prefix lookalike and a repository escape through a link. Exercise
mixed planned and actual change-set flags. Where Windows cannot create a
link without privileges, retain the explicit skip and exercise that case
on Linux CI. Never convert a skipped check to a pass.

For D, compare projection without the option with the same selection using
the option. Lifecycle state, next action, gate status and actual change-set
fields remain unchanged. Change only one planned path or its classification
and confirm the result digest changes. Use the existing one-validation test
to prevent another full graph pass for the additional view.

For E, review the released-resource sources, WO template, CLI reference and
their discovery tests. The request must let a reader identify the outcome,
scope, checks, uncertainty and permission without reading IDs or commands.
Exact definitions, WO, VER and reviewed revisions remain linked. This is
an inspection judgement, not a claimed usability score.

For F, use two small temporary repositories with independently recorded
expected file lists. One models a bug fix with a caller, test and fixture.
The other models an instruction, template, documentation and contract test.
Use fixture-only decisions and candidate CLI transitions; never apply
simulated human approval to real records. Retain the starting plan, coverage
output, actual change set, handoff and prepared record for each example.
Both examples must retain the same WO identity and approved scope through
preparation of the VREC. Also show that a proposed extra file is caught before
approval and a genuinely new later change cannot rely on the old scope.

## Commands and platforms

Run the focused modules selected by the implementation in
tests/test_scope_preparation.py, tests/test_cli_shape.py,
tests/test_workflow_execution.py, tests/test_workflow_compliance.py,
tests/test_workflow_restitution.py and tests/test_one_validation.py.
Run the affected authoring and instruction-discovery tests.

Then run python scripts/run_tests.py and the repository distribution checks
after reading their required release-sequence prerequisites. Check CLI help.
Use local Windows and the existing Linux/Windows CI at integration. Local
results do not establish CI success. External model calls, host login and
desktop interaction are not needed for these deterministic checks.

Use the exact selected released evaluator for real validate, doctor,
start/review/handoff checks and commit-bound verification capture. Candidate
source is limited to development tests and isolated demonstrations.

## Evidence retention

Retain commands, input lists, expected and observed results, exit codes,
platforms, skips and the exact candidate commit in the selected WO's evidence
directory. Keep one ordinary review covering requirements, scope, generated
outputs and remaining uncertainty. Do not create a separate benchmark or
planning receipt framework. Capture the VREC through the released evaluator
against the exact clean candidate; its actual ID is allocated later.

## Residual uncertainty

Passing two representative cases does not prove exhaustive impact analysis
or a measured reduction in interruptions across all work. The human still
reviews semantic scope and real expansion. The installed evaluator and
plugin will acquire this behavior only through a later release and adoption.

````

### WO-KIS-010

Source: `docs/engineering/harness-simplification/work-orders/WO-KIS-010.md`

SHA-256: `62d8a3bf0bfdf2246afbd37c7a5884b48f2ca860b5fd5617a102444753eb84d0`

````markdown
+++
id = "WO-KIS-010"
type = "work_order"
title = "Deliver complete scope preparation and clear approval requests"
status = "draft"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/workflow_change_set.py",
  "se_harness/workflow_result.py",
  "se_harness/scope_preparation.py",
  "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md",
  "templates/repository/standard/docs/engineering/harness/DRAFT_WORK_ORDERS.md",
  "templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md",
  "templates/repository/standard/docs/engineering/harness/WORK_AND_EVIDENCE.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "docs/notes/harnessctl-reference.md",
  "tests/test_scope_preparation.py",
  "tests/test_cli_shape.py",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_compliance.py",
  "tests/test_workflow_restitution.py",
  "tests/test_one_validation.py",
  "tests/test_artifact_authoring.py",
  "tests/test_artifact_authoring_policy.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_artifact_catalog.py",
  "tests/test_instruction_architecture.py",
  "tests/test_progressive_instruction_discovery.py",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-010.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-004.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-004.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-010.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-010/",
]

[relations]
implements = ["REQ-KIS-010"]
specifications = ["SPEC-KIS-004"]
verification = ["VER-KIS-004"]
+++

# Deliver complete scope preparation and clear approval requests

## Objective

For the human requesting a bounded change, provide one understandable
implementation decision after the agent has inspected the affected work,
included foreseeable supporting paths, and assessed the proposed scope.

## In scope

Implement KIS-SCP-001 through KIS-SCP-006: dependency inspection guidance,
one complete bounded WO, the optional planned-path view of check, explicit
explanation of generated outputs, and a clear approval request. Reuse
INT-KIS-001 and CAP-KIS-001 unchanged. Existing KIS design simplicity and
routine-execution authority remain applicable.

## Out of scope

No change to authority, lifecycle edges, gates, actual change-set admission,
record capture, release or adoption. No automatic dependency scanner,
persistent planning inventory, new artifact type or scoring framework.
No host authentication or live desktop test. Push, PR, merge, marketplace
publication and installed evaluator/plugin updates are separate actions.

## Proposed assurance decision

Proposed classification: required commit-bound verification under VER-KIS-004.
Reason: later human approval and engineering decisions rely on the correctness
of the CLI report and released instructions. Confirm this classification with
the package approval. The assurance metadata will then record the actual
human decision; no deciding identity is fabricated in this draft.

## Authorized decision envelope

Once this package is approved and start checks pass, the agent may implement
within the listed paths, run checks, make local commits, retain evidence,
record eligible completion and prepare the required VREC. It may choose
local helper structure and test organization within the accepted behavior.
It must not treat preparation as approval or independently accept verification.

The change surface is an allowed boundary, not a quota: do not edit a listed
file when the implementation does not need it. Approval covers the exact
reviewed definitions and verification contract. Any changed accepted meaning
or actual scope expansion requires the applicable human decision.

## Constraints

Use the selected released evaluator 0.21.0 for real governance. Candidate
source may run only as development tests and isolated demonstrations.
Preserve existing calls without the new option. Reuse validation and path
admission instead of a second graph pass or competing matcher.
Keep transient working notes outside the repository. Preserve owner content.

## Expected change surface

| Paths | Planned change and reason |
| --- | --- |
| se_harness/cli.py | Parse planned-path input, enforce mutually exclusive options and use the existing check result route. |
| se_harness/workflow.py | Add the planning view while reusing the already validated catalog and selected lifecycle projection. |
| se_harness/workflow_change_set.py | Reuse or expose the smallest existing normalization/admission seam; do not widen its behavior. |
| se_harness/workflow_result.py | Render preparation coverage and its limits; preserve canonical lifecycle content and bind machine planning data to the digest. |
| se_harness/scope_preparation.py | Small read-only assessment helper if separation is clearer than extending the existing module. No persistent state. |
| templates/repository/standard/docs/engineering/harness/DRAFT_WORK_ORDERS.md | Put dependency inspection and planned-path assessment in the existing preparation procedure. |
| templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md | Present the concise decision card at the existing human approval step. |
| templates/repository/standard/docs/engineering/harness/WORK_AND_EVIDENCE.md | Explain complete bounded scope and existing automatic generated-output admission at the shared reference. |
| templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md | Point the WO checklist to the common preparation guidance without duplicating its procedure. |
| templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md | Replace guessed-file guidance with inspected paths, short reasons and explicit unknown outputs in Expected change surface. |
| docs/notes/harnessctl-reference.md | Document the opt-in check mode, report meaning, compatibility and limitations. |
| tests/test_scope_preparation.py | Public CLI coverage, path boundaries, no-write assertions, generated outputs and the two representative demonstrations. |
| tests/test_cli_shape.py | Preserve command shape and exercise the new option's input contract. |
| tests/test_workflow_execution.py | Protect checkpoint-free projection, selection and lifecycle compatibility. |
| tests/test_workflow_compliance.py | Protect actual scope and generated-record admission when shared helpers are reused. |
| tests/test_workflow_restitution.py | Check human/JSON clarity and machine-field digest binding. |
| tests/test_one_validation.py | Assert that the planning view reuses one repository validation. |
| tests/test_artifact_authoring.py; tests/test_artifact_authoring_policy.py | Verify the supported authoring route and updated WO guidance. |
| tests/test_workflow_documentation_contract.py; tests/test_artifact_catalog.py | Keep instruction links, headings and CLI documentation consistent. |
| tests/test_instruction_architecture.py; tests/test_progressive_instruction_discovery.py | Ensure agents discover the guidance at preparation/approval without loading it at every startup. |
| The four exact formal-artifact paths in execution_scope | Carry this reviewed package and its evaluator-applied lifecycle history with the work. No manual rewrite of accepted decisions. |
| docs/engineering/harness-simplification/evidence/WO-KIS-010/ | Retain local checks, demonstration results, ordinary review and generated start/review/handoff evidence for this WO. |

The code entry point, projection, result renderer, admission helpers, current
CLI reference, WO template and relevant test consumers were inspected before
this draft. The common change skill already routes agents to released
authoring and continuation procedures, so no duplicate skill policy is
needed. Existing package data includes these modules and resources;
packaging and CI configuration changes are not planned. Distribution and
CI checks will verify that assumption.

No existing fixture file needs revision; the focused test creates small
temporary fixtures through current helpers. No new schema for formal
artifacts or machine gate contract is needed. Do not change unrelated stale
documentation while carrying this proposal.

## Generated outputs and unresolved destinations

The selected WO's own path is explicitly listed. Start, review, handoff,
test and ordinary review evidence use the explicit evidence directory above.

The future VREC ID is allocated by the evaluator during preparation. Its
exact record and evaluator-evidence paths are not known yet. Existing
relationship-based admission covers a record that directly verifies this
WO and its declared evaluator evidence. Recheck the actual returned paths
when the record exists. This does not admit its whole directory or a record
for another WO. No release record or publication output is planned.

## Required verification

Perform VER-KIS-004 cases A-F. Run focused CLI, workflow, authoring and
discovery tests, then the repository suite and distribution checks. Retain
unavailable checks and skips explicitly. Windows local checks and existing
Linux/Windows CI serve their distinct scopes; local passing results do not
stand in for CI. Human acceptance uses the exact candidate-bound VREC.

## Evidence to record

Under the declared evidence directory, retain one ordinary review plus
commands, exit codes, outputs, the requirement-to-result assessment and the
two fixture demonstrations. Record actual changed files and compare them
with this plan. Use the released evaluator's required evidence format for
start, review, handoff and verification capture. Preserve failed attempts.

## Stop and escalate conditions

Stop the affected action if the implementation requires an unlisted path,
changes accepted semantics, changes path admission or lifecycle authority,
needs another persistent schema or cannot preserve existing check behavior.
Also stop for a failed required gate or unresolved material verification
failure. Report the exact new need and prepare one bounded correction.

## Completion report format

State the user-visible change, actual scope, test results, limitations and
the evaluator's next decision. Show whether either demonstration needed
an additional WO for a foreseeable omission. Do not turn these two examples
into a general measured improvement claim.

````
