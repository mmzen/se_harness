+++
id = "SPEC-HAG-004"
type = "specification"
title = "Standalone draft validation and shared relationship rules"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"
contract = "The evaluator reports bounded draft admissibility through a read-only command, preserves explicit incompleteness, rejects structural invalidity, and shares declared relationship types with validation and preflight."

[relations]
specifies = ["REQ-HAG-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T13:24:31Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved REQ-HAG-009, SPEC-HAG-004, VER-HAG-002 and WO-HAG-002 for local implementation with required commit-bound verification in this conversation. Reviewed manifest SHA-256: e36a47fb59f1bf1f856aa8a47c20189bc84d9d53d787fce505e6bc0f895eabe8. All complete reviewed bytes matched; only the confirmed assurance table was completed before preview. This approval grants bounded local implementation and required verification preparation, not verification acceptance, publication, release or governor adoption. DEC-HAG-001 remains unchanged."
+++

# Standalone draft validation and shared relationship rules

## Scope and terms

Draft admissibility means that one selected artifact has a supported draft
shape. It does not mean that the artifact is approval-ready or that a caller
may commit a remote mutation. The server retains its authentication, protected
field comparison, version guard and transaction responsibilities.

The supported types match the prepared hosted command contract: intent,
capability, requirement, specification, architecture, adr, verification,
work_order, release_contract and operating_contract, each in draft. Decision,
risk, verification_record and release_record are unsupported here. Existing
commands for those records keep their meaning.

### HAG-EVL-001 — Explicit read-only entry point

Add `harnessctl validate-draft TARGET --artifact ARTIFACT-ID --json` and a callable
implementation using the same parser and catalog as the evaluator. The target
is a complete disposable projection prepared by the caller. The command does
not create a projection, a work order, an ID, or an artifact. Selection must
resolve exactly one supported draft. No writes or lifecycle next step occur.

JSON uses `se-harness-draft-validation-v1` and contains selection (ID, type,
status and original relative path), `admissible`, `errors`, `incomplete`, and
`background` findings. Findings carry stable codes, paths and machine-readable
field/relation/target detail where classification depends on it. Missing or
ambiguous selection is a refusal, never an empty success. Exit 0 means the
selected draft is admissible; exit 1 means a produced refusal; exit 2 retains
the CLI usage/pre-result error convention. Human output carries the same facts.
The caller binds the actual package identity separately; this is not a new
authority or evaluator-selection mechanism.

### HAG-EVL-002 — One relationship contract

One shared table defines declared source/relation/target types, from the released
DEFINITION_LINKS, WORK_AND_EVIDENCE and RISKS_AND_DECISIONS contracts. Repository
validation, draft validation and preflight consume it. Centralize existing
required relation names where needed without changing ordinary completeness
rules. Do not maintain a second table in the server.

In particular, requirement.derives_from targets capability and
capability.derives_from targets intent. A target's existence alone is insufficient.
Reject a supplied undeclared relation/source pair and an endpoint of the wrong
type. Preserve existing self-link, target-shape and missing-target refusals.
An all-artifact target set is explicit only for declared general relations,
such as decision.concerns and risk.threatens; it is not a default fallback.

Ordinary `validate` gains the missing typed-link refusals. It does not gain a
draft exception or stop requiring its existing fields. Preflight keeps its
selected governing-chain scope, state checks and decision gates. Expected
differences caused by the newly enforced relation contract are retained and
explained; existing valid graphs and approval protections must still pass.

### HAG-EVL-003 — Narrow, structured incompleteness

Only the selected supported draft can use this classification. It requires a
valid unique ID, matching type, draft status, well-formed TOML and metadata
shapes, and no lifecycle history or disposition. Missing identity fields and
invalid dates/types are errors.

Permitted incompleteness consists of:

1. Unfilled authoring text or metadata placeholder values in the exact field
   positions of that type's canonical template shipped by the same evaluator.
   Placeholder matching is exact and type/field-specific. Identity, type,
   status, dates and lifecycle/decision/evidence history are never exempt.
2. A required authoring relation omitted or supplied as an empty array, and
   exact canonical template relation placeholders in their proper fields.
   Each unresolved slot is reported as incomplete. Other supplied targets
   still undergo existence and endpoint checks, including in mixed arrays.

For example, a requirement's canonical `CAP-xxx`, an omitted derives_from, or
`derives_from = []` is incomplete. `CAP-MISSING-999` is an error, not a placeholder.
`["CAP-xxx", "RLS-SEH-001"]` is refused because one supplied endpoint is wrong.
Copying a template-looking string into a different field does not create an
exception. Non-array relations, non-string targets and blank target strings
are malformed, not empty authoring slots.

Implement predicate-level classification with structured details. Do not match
English diagnostic messages, suppress every E005/E006, remove errors by plane,
or supply an `ignore_errors` switch. Normal validation and approval still report
their original completeness failures for these same incomplete drafts.

### HAG-EVL-004 — Honest selection and failure scope

Parsing failures and duplicate IDs that prevent a trustworthy projection catalog
block the result. Within a trustworthy catalog, check the selected draft's
metadata and every supplied outgoing relationship using the shared rules.
An existing unique correctly typed target establishes that edge's endpoint;
this command does not assert that the target's entire governing chain is ready.
Unselected artifact findings are preserved as background and cannot disappear
into a claim that the whole repository is valid. All refusal paths leave files
and selected lifecycle state unchanged. No synthetic work order is used to
force an unlinked draft into preflight.

### HAG-EVL-005 — Keep decisions and mutation checks separate

Reject a selected artifact outside draft or containing lifecycle_events or a
disposition. The command checks the supplied snapshot and cannot prove that an
existing imported artifact's identity, original bytes or provenance were not
changed; the hosted caller must compare those against its immutable base before
using this result. It must also enforce rights and expected versions. A draft
result cannot substitute for transition, verification, release or decision gates.

### HAG-EVL-006 — Qualification before adoption

Exercise the command from an installed candidate wheel outside the source tree
against disposable fixtures. Keep repository governance on the selected 0.22.0
release. Retain archive and installed-payload identities with results. No source
fallback, package substitution in the private governor, or automatic pin update.
The eventual released version and hosted identity amendment require their normal
release and definition procedures; they are not selected by this specification.

## Design assessment

Extending the current parser/validators with a separate read-only query is the
smallest complete correction. A two-entry table patch alone fixes the observed
false positive but cannot distinguish a saveable incomplete draft. Putting that
classification in the service would duplicate policy. No new storage, service,
workflow state, external dependency or generalized policy engine is needed.
No active architecture directly addresses REQ-HAG-009; this local evaluator
extension needs no invented architecture or ADR link.

## Examples and coverage

An unlinked draft requirement with derives_from pointing to RLS-SEH-001 is refused
by validate-draft and normal validate without selecting any work order. A generated
requirement remains admissible but incomplete; its ordinary approval still fails.

| Requirement | Rules |
| --- | --- |
| REQ-HAG-009 | HAG-EVL-001, HAG-EVL-002, HAG-EVL-003, HAG-EVL-004, HAG-EVL-005, HAG-EVL-006 |
