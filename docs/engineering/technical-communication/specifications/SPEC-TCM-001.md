+++
id = "SPEC-TCM-001"
type = "specification"
title = "Managed technical-communication policy and operator-brief skill contract"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-TCM-001", "REQ-TCM-002", "REQ-TCM-003", "REQ-TCM-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "technical-owner"
+++

# Specification: Managed technical-communication policy and operator-brief skill contract

## Scope

This specification defines one managed technical-communication policy, two
bounded writing profiles, protected-content precedence, the explicit read-only
`harness-operator-brief` portable skill, installation and integrity behavior,
and independent verification expectations.

The policy follows selected ASD-STE100-based clarity principles. It is not a
copy or implementation of the standard and makes no compliance, certification,
approval, or endorsement claim. Runtime execution must not download or search
for the standard. This specification does not change lifecycle states, decision
rights, quality gates, traceability, artifact schemas, or external-action
permissions.

## Actors and external systems

- A supported coding agent authors eligible English prose under the managed route.
- An operator can explicitly invoke `harness-operator-brief` for one bounded
  explanation outcome.
- Accountable owners retain all existing product, technical, engineering,
  assurance, repository, release, and service decisions.
- The exact target released evaluator verifies installed identity and integrity.
- The standard installer and upgrader distribute the managed policy and portable
  skill.
- Repository-owned terminology can supply approved project terms.
- ASD-STE100 and its maintainer are external provenance references only. They are
  not runtime services or downloaded dependencies.

## Terms and precedence

- **Eligible prose:** agent-authored English explanatory text that is not exact
  or semantically protected content.
- **Exact protected content:** bytes whose identity, syntax, provenance, or
  canonical form must not change.
- **Semantically protected content:** language whose scope, force, qualification,
  or established terminology must not change through automatic simplification.
- **Communication profile:** one managed selection of principles and application
  strength; it is distinct from an agentic-execution logical profile.
- **Material deviation:** a conscious exception to a profile recommendation that
  is necessary to preserve meaning; routine protected spans are not deviations.

Precedence, from highest to lowest, is:

1. machine-readable harness contracts and exact evaluator results;
2. approved formal artifact semantics and accountable decisions;
3. managed workflow, decision-right, gate, traceability, and repository policy;
4. repository-approved technical terminology;
5. this managed technical-communication policy;
6. portable skill, runtime adapter, prompt, and model prose.

A lower item cannot rewrite or reinterpret a higher item.

## Inputs

Ordinary agent authoring receives the output purpose, applicable repository
instructions, selected draft scope, protected content, and any approved project
terms through the current task context.

The operator-brief skill receives one closed invocation containing:

- repository target;
- structured exact-evaluator launcher, expected version, and expected root;
- explicit skill name;
- requested bounded outcome and declared non-effects;
- source kind: `structured-harness-result` or `bounded-technical-text`;
- one UTF-8 source payload and its SHA-256;
- an ordered non-overlapping protected-content declaration with stable IDs,
  UTF-8 byte offsets, kinds, and SHA-256 values; and
- an optional bounded set of repository-approved project terms.

The complete encoded source input is limited to 262,144 bytes. The helper
rejects duplicate object keys, control characters outside valid structured
content, invalid UTF-8, negative or out-of-range offsets, overlapping spans,
wrong digests, and unknown fields.

## Outputs

Ordinary authoring produces the requested operator prose or draft artifact prose
and, when governed work requires it, evidence naming the applied profile and
material deviations.

`harness-operator-brief` returns inline:

- one `se-harness-skill-result-v1` containing outcome, profile name, source
  identity, operator message, protected-content bindings, material deviations,
  and residual uncertainty; and
- one `se-harness-execution-receipt-v1` binding skill identity, evaluator
  identity, validation outcome, and zero changed paths.

No skill output or receipt is retained in the target repository. Output must not
contain hidden reasoning, credentials, environment dumps, unbounded source
copies, or an authority claim.

## State model

The policy has no lifecycle state outside its managed-file identity. The skill
has no repository state and no mutation state. One invocation ends as:

- `completed`: source and output are valid, preservation passes, and no material
  uncertainty prevents the brief;
- `degraded`: the brief is safe but an optional project term or advisory check is
  unavailable;
- `stopped`: an accountable clarification, current orientation result, or exact
  output path is required;
- `blocked`: activation, policy, identity, source, or protected-span preconditions
  are missing or ambiguous; or
- `failed`: parsing, digest, preservation, or required validation fails.

No outcome changes lifecycle, repository, Git, network, or external state.

## Behavioral rules

### Managed policy

**TCM-POL-001:** The canonical source is
`templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md`.
Installation maps it to `docs/engineering/TECHNICAL_COMMUNICATION.md` with mode
`managed` and a schema-3 normalized digest in `.engineering-harness.lock`.

**TCM-POL-002:** The policy contains purpose, permitted claim, no-download rule,
precedence, eligible prose, two profiles, protected content, deviation handling,
human decision points, and examples. It contains no copied dictionary, complete
external rule catalog, logo, or compliance claim.

**TCM-POL-003:** `ENGINEERING_HARNESS.md` routes eligible operator and artifact
prose to the policy in one concise entry. `AGENTS.md`, skills, adapters, notes,
and artifact templates do not duplicate the policy body.

**TCM-POL-004:** The installed path is part of required and policy reading
manifests. Existing installer, lock, doctor, upgrade, repair, and transactional
conflict behavior applies without a special bypass.

**TCM-POL-005:** Candidate development changes the canonical template and
installer/package surfaces. It does not directly edit the self-hosting root copy
that remains bound to the currently installed released evaluator.

### Clarity principles

**TCM-CLR-001:** Eligible prose uses one stable term for one concept and defines
an uncommon project term before relying on it.

**TCM-CLR-002:** Eligible prose identifies the responsible actor when
responsibility matters, prefers active voice, and makes conditions, actions, and
results explicit.

**TCM-CLR-003:** Sentences remain focused and direct. Sentence length is a
review signal, not a conformance threshold and not permission to remove detail.

**TCM-CLR-004:** Prose avoids ambiguous pronouns, decorative synonyms, hidden
negation, vague references, and unnecessary introductory text.

**TCM-CLR-005:** Lists and tables are used when they make parallel conditions,
mappings, or steps clearer. They do not replace required semantic relationships.

### Protected content

**TCM-PRT-001:** Exact protected content includes code and inline code; commands;
paths; identifiers; hashes; version strings; URLs; schemas and field names;
JSON, TOML, YAML, XML, and other machine-readable data; logs, diagnostics, and
evidence; evaluator output and canonical restitution blocks; quotations; and
operator-supplied text.

**TCM-PRT-002:** Semantically protected content includes BCP 14 obligations,
requirement statements, lifecycle and decision meanings, safety or legal
qualifications, acceptance thresholds, formulas, and established terminology.

**TCM-PRT-003:** Exact protected content is byte-identical. Semantically
protected content is excluded from automatic paraphrase. A newly drafted
normative statement may use the principles only while its actor, condition,
force, scope, qualification, and result remain explicit and unchanged by any
later rendering pass.

**TCM-PRT-004:** An ambiguous boundary, unknown term, or failed comparison stops
a completed result. The source remains available unchanged.

**TCM-PRT-005:** A canonical block whose governing procedure forbids surrounding
text bypasses communication rendering and is returned alone.

### Profile selection

**TCM-PRF-001:** `operator-communication` leads with the outcome or one required
action, identifies the accountable actor, uses one principal action per
sentence, states limits directly, and avoids a second next step.

**TCM-PRF-002:** `technical-artifact-writing` applies clarity principles to
narrative purpose, rationale, scope, descriptions, procedures, assumptions,
risks, and examples. It applies minimally or not at all to normative statements,
semantic tables, metadata, code, exact results, and evidence.

**TCM-PRF-003:** Profiles apply during composition or deliberate revision of
selected draft prose. They are not automatic post-processors and do not justify
repository-wide or approved-artifact style migrations.

**TCM-PRF-004:** Non-English output, exact-output requests, direct quotation, and
unsupported purpose do not claim a managed profile result.

### Portable skill

**TCM-SKL-001:** The canonical portable core is
`templates/repository/standard/.agents/skills/harness-operator-brief/` and the
managed installed location is `.agents/skills/harness-operator-brief/`. It
contains `SKILL.md`, `skill-contract.json`, and `scripts/check_brief.py` only.

**TCM-SKL-002:** The contract is one new closed
`se-harness-skill-contract-v2` instance named `harness-operator-brief` version
`1.0.0`. Existing v1 and v2 instances, bytes, behavior, and manifest digests do
not change.

**TCM-SKL-003:** Activation is explicit true and implicit false. Mutation class
is `read-only`; delegation is disabled; fallback is `single-agent`; path source
is `none`; permitted effect is `inline-brief-render`; target retention is false;
and lifecycle transitions are empty.

**TCM-SKL-004:** Required evaluator operations are `version`, `identity`, and
`doctor`. The minimum operation baseline is 0.6.0, but execution always uses the
exact released evaluator bound by the target. No optional evaluator operation
can substitute for current structured harness state.

**TCM-SKL-005:** The closed inputs are the common v2 repository, evaluator,
explicit-skill, outcome, and non-effect inputs plus source kind, source payload,
protected-content declaration, and optional project terms. Contract parsing
adds no open-ended skill registration mechanism.

**TCM-SKL-006:** Before inline rendering, the skill verifies identity, integrity,
source digest, span ordering, span digests, and explicit activation. After
rendering, `check_brief.py` verifies every required protected binding and zero
changed paths. It does not score grammar, test substantive truth, or inspect
hidden reasoning.

**TCM-SKL-007:** Non-match examples include repository orientation, artifact
creation or revision, work-order execution, assurance preparation, lifecycle
transition, Git mutation, credential use, network use, release, and external
action.

**TCM-SKL-008:** If a request needs current repository or artifact state and no
current structured result is supplied, the result stops and routes to
`harness-orient`. It does not duplicate orientation or invent current state.

### Deviations and human decisions

**TCM-HUM-001:** The agent applies routine eligible prose automatically. A human
is asked only to decide meaning, approve a new project term, resolve an
ambiguous protected boundary, exercise an existing accountable right, or accept
a separately governed policy revision.

**TCM-HUM-002:** A material deviation records rule ID, reason, meaning protected,
and resulting limit. It does not record hidden reasoning or routine exclusions.

## Error and recovery behavior

Diagnostics use a stable `TCM` family and identify the exact failed class:
activation, policy integrity, source schema, source digest, protected span,
profile selection, unsupported language, output preservation, or prohibited
effect. Recovery supplies corrected local input or the required accountable
decision. Recovery never downloads the standard, broadens scope, edits protected
content, or performs a lifecycle or external action.

## Data and interface contracts

All retained JSON uses UTF-8, duplicate-key rejection, bounded arrays and text,
stable field sets, canonical ordering where identity is computed, and lowercase
SHA-256. UTF-8 byte offsets are measured against the exact source bytes. Paths
are repository-relative POSIX paths. Host absolute paths and credentials are not
portable skill inputs except the existing structured evaluator launcher and
expected root boundary.

## Security and privacy properties

- No network operation, credential, standard download, or remote terminology
  service is permitted.
- Source bodies are bounded, handled inline, and not retained in receipts.
- Diagnostics omit source bodies, secrets, host paths, environment dumps, and
  hidden reasoning.
- Repository content and structured results remain untrusted parser input.
- Runtime write permission cannot change the read-only mutation class.

## Performance and capacity

One invocation handles at most 262,144 input bytes and 256 protected spans.
Validation is linear in source bytes plus span count. No network latency or
subagent cost is permitted. Performance is secondary to exact preservation.

## Observability

The result and receipt identify skill name and version, portable-core digest,
policy path, selected profile, source digest, protected binding count, material
deviations, evaluator identity, outcome, and zero changed paths. They do not
claim that clarity metrics prove correctness or compliance.

## Compatibility and migration

- Current skill contract v1 and closed Phase 3 v2 instances remain accepted
  without byte or behavior changes.
- The new closed v2 instance fails on older evaluators that do not recognize its
  name; installation must keep skill and evaluator versions coherent.
- Standard install and upgrade add the policy and skill transactionally. A
  customized collision blocks before partial replacement.
- Existing approved artifacts and installed owner content are not migrated.
- Provider-specific host activation is outside this first work order; the
  portable core remains discoverable through the standard managed skill path.

## Examples and counterexamples

A valid brief can say that one work order is implemented and name the assurance
owner's next decision while preserving its artifact ID and canonical command.

It is invalid to replace `SHALL` with a weaker phrase, paraphrase a hash, alter a
JSON field, add prose around a canonical restitution block, or say that the
result is ASD-STE100 compliant.

It is also invalid to hide implementation inside the brief skill, activate it
implicitly, or copy the full policy into `SKILL.md`.

## Explicitly unspecified decisions

The implementation agent may choose helper function names, internal data
classes, test fixture organization, concise policy examples, and diagnostic
numbers within the reserved `TCM` family. It may not change policy precedence,
profile names, protected classes, skill activation, mutation class, public
claim, no-download boundary, source limits, output schemas, or stop behavior.
