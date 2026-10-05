# Draft definitions

## Read this when

The selected change lacks a definition, verification, release or operating contract.

## Before this action

Before choosing a type, read [ARTIFACTS.md#artifact-types](ARTIFACTS.md#artifact-types) and [ARTIFACTS.md#artifact-locations](ARTIFACTS.md#artifact-locations). Before links, read [DEFINITION_LINKS.md#links-between-definitions](DEFINITION_LINKS.md#links-between-definitions). Before authoring, read [../ARTIFACT_AUTHORING.md#design-simplicity](../ARTIFACT_AUTHORING.md#design-simplicity) and the exact type checklist linked in this file.

## Procedure

### Check an unfinished draft

Use `harnessctl validate-draft REPO --artifact ARTIFACT-ID --json` to inspect
one draft in a complete caller-supplied projection. The read-only result separates
`errors`, permitted `incomplete` slots, and unselected `background` findings.
Exact canonical template placeholders and omitted or empty required authoring
relations can be incomplete. Every actual endpoint still needs a declared
relationship and the correct type. A requirement cannot derive from a release
record, including in an array that also contains `CAP-xxx`.

An admissible result does not make the draft approval-ready. Normal validation,
preflight and transition gates still apply. Selection must identify one supported
draft without lifecycle history or disposition. The query does not create files,
change state or supply a lifecycle next step. Its caller remains responsible for
authentication, immutable-base comparison and expected versions before a write.

### Draft any missing definitions

**Inputs:** The confirmed outcome, scope limits, and missing-definition list
from [Identify the existing artifacts that apply to the change](DEFINE_CHANGE.md#identify-the-existing-artifacts-that-apply-to-the-change).

**Output:**

- **Formal artifacts:** New drafts of the missing intents (INT), capabilities
  (CAP), requirements (REQ), specifications (SPEC), applicable architectures
  (ARCH), and required architecture decisions (ADR). None if no definitions
  are missing.
- **Domain files and directories:** The structure reported by
  `scaffold-domain`, created only if the selected domain is missing.
- **Transient working material:** The inventory updated with generated IDs
  and file paths. Retain it under the same conditions as [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome).

**Actions:**

1. Read `Design simplicity` in `docs/engineering/ARTIFACT_AUTHORING.md`.
2. Select the domain for each missing definition from the inventory. For a
   missing domain, preview its creation with the domain commands below.
3. Inspect the proposed domain paths. Resolve any reported conflict before
   running the domain creation command.
4. Select the first missing artifact type from the table below. Skip types
   already covered by unchanged existing artifacts.
5. Run the artifact preview command. Inspect its type, destination path, and
   `allocated_id`.
6. Run the artifact creation command with that exact ID. If a conflict occurs,
   repeat the preview; do not overwrite an existing record.
7. Open the returned file. Complete its title, owners, dates, content, and
   declared links. Replace all template placeholders.
8. Apply `### Checklist` under the matching `## TYPE` heading in
   `docs/engineering/ARTIFACT_AUTHORING.md`.
9. Read the completed draft. Record its ID and path in the inventory.
10. Repeat actions 4–9 for each remaining missing definition.

| Order | Artifact | TYPE | Content | Declared links |
| --- | --- | --- | --- | --- |
| 1 | Intent (INT) | `intent` | Problem, intended outcome, affected users, and scope limits. | None required here. |
| 2 | Capability (CAP) | `capability` | The ability needed to achieve the outcome. | `derives_from` → intent (INT). |
| 3 | Requirement (REQ) | `requirement` | Observable behavior, conditions, and acceptance criteria. | `derives_from` → capability (CAP). |
| 4 | Specification (SPEC) | `specification` | Detailed behavior, constraints, failure behavior, and checkable examples. | `specifies` → requirement (REQ). |
| 5 | Architecture (ARCH), when applicable | `architecture` | Components, boundaries, and the architecture decision assessment. | `addresses` → requirement (REQ); `conforms_to` → specification (SPEC). |
| 6 | Architecture decision (ADR), when required | `adr` | Context, alternatives, chosen design, and consequences. | `decides` → architecture (ARCH). |

Record an unresolved design choice for [Record unresolved decisions (DEC)](RISKS_AND_DECISIONS.md#record-unresolved-decisions-dec). Do not present a recommendation
as an agreed architecture decision (ADR). Prepare verification contracts (VER)
in [Define how the result will be verified](DRAFT_DEFINITIONS.md#define-how-the-result-will-be-verified).

**Harness commands:**

For a missing domain, use the first command in action 2 and the second only
after reviewing the preview in action 3:

```text
harnessctl scaffold-domain REPO --domain DOMAIN --dry-run --json
harnessctl scaffold-domain REPO --domain DOMAIN --json
```

For each missing artifact, use this **creation sequence** in actions 5–6.
Replace `TYPE` with the table value. Replace `ARTIFACT-ID` in the second
command with the first command's `allocated_id`:

```text
harnessctl create-artifact REPO --domain DOMAIN --type TYPE --dry-run --json
harnessctl create-artifact REPO --domain DOMAIN --type TYPE --id ARTIFACT-ID --json
```

The preview writes nothing and does not reserve an ID. Creation writes one
incomplete template and returns its path. Content completion is a separate
editing action. The JSON output does not contain the authoring checklist.

**Completion:** Each missing definition has a completed draft with an ID and
path. Unresolved choices are identified. If no definitions are missing,
record `None needed` in the transient inventory.

**Later use:** These definitions supply the verification contracts (VER) in
[Define how the result will be verified](DRAFT_DEFINITIONS.md#define-how-the-result-will-be-verified) and the governing links in work orders (WO) in [Prepare work orders (WO) linking the definitions, scope, planned work, and verification requirements](DRAFT_WORK_ORDERS.md#prepare-work-orders-wo-linking-the-definitions-scope-planned-work-and-verification-requirements). Their acceptance
is handled in the authorization process.

### Define how the result will be verified

**Inputs:** The selected requirements (REQ), specifications (SPEC), proposed
amendments, and existing verification contracts (VER).

**Output:**

- **Formal artifacts:** New or updated verification contracts (VER) in
  `draft` where coverage is missing. None created or modified where existing
  contracts provide unchanged coverage. Accepted contracts remain unchanged.
- **Transient working material:** The selection of reused verification
  contracts (VER), any amendment proposals prepared through [Propose any needed amendments to existing definitions](AMEND_DEFINITIONS.md#propose-any-needed-amendments-to-existing-definitions), coverage
  gaps, and unresolved questions. Retain these under the same conditions
  as [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome).

**Actions:**

1. Read each selected requirement's (REQ) acceptance criteria and linked
   specifications (SPEC).
2. Compare those criteria with the existing verification contracts (VER).
3. Select unchanged contracts that cover the proposed behavior.
4. For each coverage gap, create a verification contract (VER) with the
   commands below, or use [Propose any needed amendments to existing definitions](AMEND_DEFINITIONS.md#propose-any-needed-amendments-to-existing-definitions) to propose an amendment to an existing one.
5. Complete `Requirement-to-evidence matrix`. For each requirement (REQ),
   record its ID, method, case or evidence, and pass condition. Use `test`,
   `analysis`, `inspection`, or `demonstration` as the method.
6. Specify the inputs, platform, evaluator, and command or manual actions for
   each check. Derive expected results from the requirement (REQ) and
   specification (SPEC), not from candidate output.
7. Set `[relations].verifies` to the covered requirement (REQ) IDs.
8. Complete `Independence`, `Evidence retention`, and applicable assessment
   sections in each new or edited draft.
9. Apply `## verification` → `### Checklist` in
   `docs/engineering/ARTIFACT_AUTHORING.md`.
10. Retain questions about missing criteria or methods for [Record unresolved decisions (DEC)](RISKS_AND_DECISIONS.md#record-unresolved-decisions-dec).

**Harness commands:**

For each new verification contract (VER), run the creation sequence from
[Draft any missing definitions](DRAFT_DEFINITIONS.md#draft-any-missing-definitions) with these arguments. Inspect the preview before creation; replace
`VER-ID` with its `allocated_id`:

```text
harnessctl create-artifact REPO --domain DOMAIN --type verification --dry-run --json
harnessctl create-artifact REPO --domain DOMAIN --type verification --id VER-ID --json
```

No harness command writes the verification method or pass criteria. The human
or agent completes that content. No verification record (VREC) is created here.

**Completion:** Every selected requirement (REQ) has a defined verification
method and pass condition, or an explicit unresolved question. Each proposed
check identifies how to perform it and where its evidence will be retained.

**Later use:** [Prepare work orders (WO) linking the definitions, scope, planned work, and verification requirements](DRAFT_WORK_ORDERS.md#prepare-work-orders-wo-linking-the-definitions-scope-planned-work-and-verification-requirements) links these contracts to work orders (WO). The execution
and verification processes later perform the checks and assess the evidence.

### Prepare a release or operating contract

**Inputs:** A proposed release or ongoing operating obligation, its scope,
existing work-order or requirement IDs, and any accepted contract that may
already cover it.

**Output:**

- **Formal artifacts:** A completed release-contract (REL) or operating-contract
  (OPS) draft when needed. An accepted contract is reused only if its meaning
  and scope already cover the proposed obligation.
- **Transient working material:** Selection notes, new IDs and paths, and
  unresolved questions. No release or operating authorization is inferred.

**Actions:**

1. Decide which obligation applies: release scope uses `release_contract`;
   continuing assurance uses `operating_contract`. Do not create both by default.
2. Read existing contracts selected for reuse. If an accepted contract needs
   changed meaning, use the accepted-definition amendment boundary; do not edit
   it through this draft-creation procedure.
3. For a missing contract, use the supported domain and artifact creation
   sequence from “Define the change.” Inspect the dry-run result and use its
   returned `allocated_id` in the creation command.
4. Complete the generated body and accountable metadata. For a REL, record
   release scope, version conditions, rollback, and evidence expectations.
   For an OPS, record measurable observability, support, and operating obligations.
5. Set `REL.gates` to every existing work-order ID covered by the release
   contract, or `OPS.assures` to every existing requirement ID for which it
   claims continuing assurance. Do not leave invented or unresolved IDs.
6. Apply `## release_contract` or `## operating_contract` and its `### Checklist`
   in `docs/engineering/ARTIFACT_AUTHORING.md`.
7. Validate the completed draft and resolve findings within the proposed scope.
8. Include the contract in [Authorize the work](AUTHORIZE_WORK.md#procedure) for the exact human decision.

**Harness commands:**

Here `TYPE` is `release_contract` or `operating_contract`, selected in action 1:

```text
harnessctl create-artifact REPO --domain DOMAIN --type TYPE --dry-run --json
harnessctl create-artifact REPO --domain DOMAIN --type TYPE --id CONTRACT-ID --json
harnessctl validate REPO --json
```

**Completion:** The applicable contract is covered by an unchanged accepted
record or a completed draft ready for its decision. Unresolved amendments
remain visible and block dependent work.

**Later use:** An accepted REL governs release preparation. An accepted OPS
governs its stated continuing obligations after delivery. Perform the checks
and follow-up actions named in the OPS at its specified triggers; one successful
delivery does not establish continuing conformance. External operating actions
still require their exact authority.

## Read next when

A risk or question needs a record → [RISKS_AND_DECISIONS.md#procedure](RISKS_AND_DECISIONS.md#procedure). Definitions are ready for work planning → [DRAFT_WORK_ORDERS.md#procedure](DRAFT_WORK_ORDERS.md#procedure).

## Type checklists

Before editing the selected type, read its section in ARTIFACT_AUTHORING.md:
[intent](../ARTIFACT_AUTHORING.md#intent),
[capability](../ARTIFACT_AUTHORING.md#capability),
[requirement](../ARTIFACT_AUTHORING.md#requirement),
[specification](../ARTIFACT_AUTHORING.md#specification),
[architecture](../ARTIFACT_AUTHORING.md#architecture),
[adr](../ARTIFACT_AUTHORING.md#adr),
[verification](../ARTIFACT_AUTHORING.md#verification),
[release_contract](../ARTIFACT_AUTHORING.md#release_contract), or
[operating_contract](../ARTIFACT_AUTHORING.md#operating_contract).
