# Artifact Authoring

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
**OPTIONAL** in this document are to be interpreted as described in BCP 14
(RFC 2119 and RFC 8174) when, and only when, they appear in all capitals.

## Purpose and precedence

This policy states how a good formal artifact is written, per type. It is
consumed by templates, by `harnessctl create-artifact`, which prints the
type's checklist, and by the drafting skill. No consumer restates it.

It ranks below the machine contracts, approved formal semantics, and the
workflow, decision-right, quality-gate, and traceability policies, and above
templates, skills, prompts, and model prose. It grants no authority: a
checklist item is a review standard, not an approval. Rules marked
*mechanical* are enforced by the validator or a gate; the rest are judgement
rules for the accountable reviewer.

## requirement

### Checklist

- One obligation: the statement contains exactly one `SHALL`; split on "and SHALL". *(mechanical: W-AUT-002)*
- One of the five shapes opens the statement: `THE SYSTEM SHALL …` (always), `WHEN <event>, …` (event), `WHILE <state>, …` (state), `IF <unwanted condition>, THEN …` (unwanted), `WHERE <feature>, …` (optional feature). The concrete component may replace `THE SYSTEM` (`THE VALIDATOR SHALL …`); name it when one exists, and keep `THE SYSTEM` for an obligation that spans components. *(mechanical: W-AUT-001)*
- The statement is one sentence of at most 30 words. *(mechanical: W-AUT-003)*
- A statement that opens `WHEN` names a real event, not the act of evaluating; an invariant reads `THE SYSTEM SHALL`. *(mechanical: W-AUT-010)*
- `verification_method` lists the methods that will verify it: `test`, `analysis`, `inspection`, `demonstration`. *(mechanical)*
- `priority` says whether it is a `must`, a `should`, or a `could`.
- `source` names where the obligation came from: a stakeholder, a standard clause, an incident, or an artifact.
- A quality requirement carries a `measure`: a value and a unit, not an adjective.
- The body has four sections, in this order: `In plain words`, `Why`, `Behavior`, `Examples`.
- `In plain words` is one or two sentences a newcomer understands. A project term used there is defined in this repository's own glossary, `GLOSSARY.md` at the repository root, which this repository writes; the harness ships none. *(mechanical: W-AUT-009)*
- `Why` says why the obligation exists, not what it does, in at most five sentences and 120 words. *(mechanical: W-AUT-006)*
- `Behavior` is one table row per trigger: the trigger the reader can observe, the response the reader can check, what happens instead on failure. That row is the requirement's acceptance condition; the cases that prove it live in the verification contract that `verifies` this requirement, and the way it is met lives in the specification that `specifies` it.
- `Examples` holds one `Normal` and one `Failure` scenario, each Given, When, Then. They fix meaning; they are not the test plan.
- The body stays under 250 words, every sentence under 25 words, and cites at most three code identifiers; the rest belongs in the specification. *(mechanical: W-AUT-005, W-AUT-007, W-AUT-008)*
- No template placeholder (`<…>`) survives. *(mechanical at approval)*
- Draft-time advisories (`W-AUT`) never fail validation and never fire on an approved requirement. An approved requirement is not rewritten for shape; it adopts the shape when it is amended for another reason.

### Guidance

Write the trigger the reader can observe, the response the reader can check,
and nothing else. Avoid escape clauses ("where appropriate", "as needed"),
vague quantities ("fast", "adequate"), and "and/or". If a requirement needs a
diagram or a table beyond its Behavior row to be understood, the detail
belongs in a specification that `specifies` it. A requirement that reads like
a plan of work is a work order in disguise.

The glossary `GLOSSARY.md` at the repository root is this repository's own: the
harness seeds it empty at installation and never rewrites it, and no term
ships with the distribution. A glossary entry may cite the artifact that
fixes the term's meaning; an amendment that changes a term's meaning names
the entry. `harnessctl inspect` reports the frequent project terms that
have no entry and the entries whose term has left the artifacts.

A pending question is not written into the requirement. Below the threshold
in the `decision` section it is asked and answered in a transition's
`reason`; above it, it is a `DEC-` artifact that names this requirement in
`blocks`, and the approval gate reads it from there. A legacy `Open
decisions` section, where one still exists, reads `None` or lists `DEC-`
identifiers; prose there is `E-DCM-004`.

## intent

### Checklist

- `outcome` is one sentence of at most 30 words that names who can do or observe what after delivery, and names no solution or code identifier. *(mechanical: W-AUT-011)*
- The body has four sections, in this order: `In plain words`, `Problem`, `Success measures`, `Not this`.
- `In plain words` is one or two sentences a newcomer understands. A project term used there is defined in this repository's own glossary, `GLOSSARY.md` at the repository root, which this repository writes; the harness ships none. *(mechanical: W-AUT-009)*
- `Problem` says what happens today, to whom, and why it is worth changing, in at most five sentences and 120 words. Evidence is cited by link to a note, an RCA or an ADR, not quoted. *(mechanical: W-AUT-012)*
- `Success measures` is one table row per measure: `Measure`, `Today`, `When reached`, `Observed`. A measure is observed in operation, after delivery, by someone who has not read the code; `Observed` names a place and a cadence an operator recognises. A row observed by a CI run, a test, a validator run, a verification or an implementation review is an acceptance check and belongs in the verification contract. `Today` may read `not measured`. *(mechanical: W-AUT-013, W-AUT-014)*
- `Not this` lists what the initiative deliberately leaves alone, in at most five bullets.
- The body stays under 200 words, every sentence under 25 words, and cites at most two code identifiers and no repository path or source line range; the evidence belongs in the note it links to. *(mechanical: W-AUT-005, W-AUT-007, W-AUT-008, W-AUT-015)*
- Who the actors are belongs in the capability's `Actor and need`; the principles later decisions must keep belong in a specification rule or an ADR; a risk is a risk artifact; an open question is a `DEC-` artifact. None of them is a section of the intent.
- No template placeholder (`<…>`) survives. *(mechanical at approval)*
- Draft-time advisories (`W-AUT`) never fail validation and never fire on an approved intent. An approved intent is not rewritten for shape; it adopts the shape and the `outcome` field when it is amended for another reason.

### Guidance

An intent survives many requirements. Write it so that a reader can tell,
years later, whether the outcome was reached. A new intent is warranted when
an owner would be asked about a new outcome in a year. A new thing an actor
can do toward an outcome already stated is a capability under the existing
intent, not a new intent.

## capability

### Checklist

- Names what an actor can do, not how the system does it.
- Derives from at least one active intent and lists its derived requirements.
- Boundaries state what the capability does not decide.

## specification

### Checklist

- Every rule carries a stable identifier (`<PREFIX>-<AREA>-NNN`) and one testable sentence.
- Every `specifies` target requirement is covered by at least one rule.
- Inputs, outputs, and failure behaviour are explicit; no rule depends on prose elsewhere.

### Guidance

A specification is where detail lives. Rules are numbered so that verification
contracts and evidence can cite them exactly.

## architecture

### Checklist

- `addresses` names only architecturally significant requirements; `conforms_to` names the specifications it must respect.
- Components, responsibilities, dependency direction, and trust boundaries are each stated.
- The decision assessment is complete: `adr_required` with triggers, or `no_significant_decision` with a rationale.

## adr

### Checklist

- Context, drivers, at least two considered options with consequences, the decision, and its consequences.
- The chosen option is stated as a decision, not a preference.
- Every `decides` target architecture is an active artifact.

## verification

### Checklist

- Independence: expected values derive from the requirements and specifications, never from candidate output.
- A requirement-to-evidence matrix with a pass condition per requirement.
- Acceptance scenarios cover the failure path, not only the normal path.
- Pass criteria name the platforms and the evaluator.

## work_order

### Checklist

- `[execution_scope].paths` is exact: files or component-prefix directories, nothing wider.
- `[assurance]` is classified and its rationale names what later decisions depend on.
- In scope and out of scope are both stated; the decision envelope says what the implementer may and may not decide.
- Stop conditions and the completion report format are stated.

## release_contract

### Checklist

- `gates` names every work order the release may include.
- Version, rollback conditions, and evidence expectations are explicit.

## operating_contract

### Checklist

- `assures` names every requirement it claims continuing assurance for.
- Observability, support, and operating obligations are measurable.

## decision

A pending question becomes a `decision` (`DEC-`) when it blocks a transition
of another artifact, concerns more than one artifact, or must survive the
approval of the artifact that raised it. Below that threshold the actor asks
and the answer stays in the transition's `reason`.

### Checklist

- `kind` is `question` (an ambiguity met while authoring or planning) or `deviation` (an implementation cannot meet one rule of one specification). *(mechanical)*
- One `question`, `raised_by`, at least two `[[options]]` with `id` and `label`, and a `recommendation` naming one option. *(mechanical)*
- A deviation also names `against = "SPEC-xxx#rule-N"` and the `observed` fact; its options are drawn from `amend`, `supersede`, `accept`, `stop` and include `stop`. *(mechanical)*
- `concerns` names every artifact the question is about; `blocks` names the artifacts that cannot change state while it is `open`, each also in `concerns`. *(mechanical)*
- The `[disposition]` table is written by `harnessctl decide`; a hand-written one is `E-DCM-003`. A deferral needs a scope and a revisit trigger; accepting a deviation needs a revisit trigger. *(mechanical)*
- `decided` and `withdrawn` decisions are never deleted or rewritten.
- The definition templates carry no `Open decisions` section: a definition's pending decisions are the `DEC-` artifacts that name it in `blocks`, and the approval gate reads them from the graph. A legacy section, where one remains, reads `None` or lists `DEC-` identifiers; prose there is `E-DCM-004`.

## risk

### Checklist

- One cause, one effect, one threatened stage; likelihood and impact on the 5x5 scale.
- Prefer `harnessctl raise-risk`, which computes the score and the raise.
- Disposition rationale and residual are written by the disposing role, not the raiser.

## verification_record and release_record

Prepared by `capture-verification` and `prepare-release`; they are not
authored by hand. This policy does not apply to them.
