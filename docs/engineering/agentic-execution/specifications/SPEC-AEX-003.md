+++
id = "SPEC-AEX-003"
type = "specification"
title = "Runtime-neutral core contract catalog and envelope authority binding"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-AEX-001", "REQ-AEX-002", "REQ-AEX-003", "REQ-AEX-004", "REQ-AEX-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:49:36Z"
decided_by = "technical-owner"
+++

# Specification: Runtime-neutral core contract catalog and envelope authority binding

## Scope

This specification refines `SPEC-AEX-001` and `SPEC-AEX-002` for Phase 2. It
defines the exact runtime-neutral contract catalog, strict validation boundary,
repository-state binding, evaluator-derived autonomy-envelope authority,
decision-packet projection, execution-receipt completeness, and reusable
portable-profile constraints required before a later work order can integrate a
mutating skill.

This specification introduces no lifecycle state, decision right, quality gate,
CLI command, skill, runtime adapter, or mutation authorization. An implementation
of this contract is a pure validation and evidence component until a later
approved work order connects it to an existing harness-controlled effect.

## Actors and external systems

- Only a later authorized integration in the exact released evaluator may
  label an envelope `derived` after validating current managed workflow and
  repository observations; the Phase 2 module constructs candidates from typed
  observations without authority.
- An accountable actor supplies the explicit decision assertion required by the
  selected managed procedure. The harness validates structure and consistency,
  not real-world identity.
- A skill, primary agent, worker, or runtime may request a narrower delegated
  scope and consume validated results, but cannot author authority.
- The harness-owned contract module parses, validates, canonicalizes, digests,
  narrows, projects, and assesses admission without performing an effect.
- The managed workflow, quality gates, mutation guard, lifecycle registry, and
  formal graph remain the sources of legality.
- Runtime providers supply technical capabilities only and are not authority
  sources.

## Inputs

### Contract catalog

The distributed catalog identifier is `se-harness-agent-contract-catalog-v1`.
Its exact meta-schema and normative type definitions appear in
**Normative contract catalog** below. It defines the complete field tree,
scalar type, nullability, enum values, collection semantics, uniqueness and
ordering rule, and local bounds for:

- `se-harness-autonomy-envelope-v1`;
- `se-harness-repository-state-binding-v1`;
- `se-harness-decision-packet-v1` compatibility and the lossless
  `se-harness-decision-packet-v2` projection;
- `se-harness-execution-receipt-v1`; and
- `se-harness-logical-execution-profile-v1`.

The existing `se-harness-skill-contract-v1` remains unchanged. A skill may
refer to a logical profile by name or consume a separately validated profile,
but adding the profile object to the Phase 1 skill contract would require a new
skill-contract schema.

The catalog is declarative contract data, not a workflow engine. It may refer to
managed identifiers but must not copy lifecycle transition tables, decision
rights, quality-gate predicates, or procedure selection rules.

The catalog and ordinary contract documents use these v1 resource bounds:

| Resource | Bound |
| --- | --- |
| UTF-8 input document | 1,048,576 bytes |
| JSON nesting below the root | 32 levels |
| Object members | 1,024 per object |
| Array entries | 1,024 per array |
| String value | 16,384 Unicode scalar values |
| Portable path or component prefix | 1,024 UTF-8 bytes |
| Operation, profile, skill, gate, finding, evidence, or worker entries | 1,024 per declared collection |
| `max_parallel_writers` | integer from 0 through 32 |
| Retry count per operation | integer from 0 through 10 |

Repository observation has separate streaming bounds: at most 100,000 manifest
entries, 16,384 formal artifacts, 1,073,741,824 bytes per regular file, and
8,589,934,592 regular-file bytes per observation. Its canonical manifest may
be at most 67,108,864 bytes. An over-bound repository is `not_assessable`; the
implementation may not silently omit entries.

The implementation may reject an input earlier for a separately approved
repository, operating-system, or process limit. It cannot accept an object that
exceeds these contract bounds.

### Canonical repository-state binding

The `selection.repository_state` string in
`se-harness-autonomy-envelope-v1` is the lowercase SHA-256 digest of canonical
bytes for this separate semantic object:

```json
{
  "schema": "se-harness-repository-state-binding-v1",
  "repository": {
    "git_object_format": "sha1-or-sha256",
    "head": "full-lowercase-object-id",
    "tree": "full-lowercase-object-id",
    "worktree_state_sha256": "lowercase-sha256"
  },
  "governance": {
    "formal_snapshot_sha256": "lowercase-sha256",
    "managed_lock_sha256": "lowercase-sha256",
    "work_order": "WO-...",
    "work_order_sha256": "lowercase-sha256"
  }
}
```

`worktree_state_sha256` is the lowercase SHA-256 of canonical
`se-harness-worktree-state-v1` bytes. The manifest covers every index entry,
every tracked worktree path even when an ignore rule matches it, and every
non-ignored untracked regular file or symlink. It excludes the repository's
`.git` administrative path and ignored untracked entries. It does not follow a
symlink, junction, reparse point, or submodule.

Each manifest entry contains exactly `path`, `index_mode`, `index_object_id`,
`worktree_kind`, `worktree_mode`, `worktree_sha256`, and
`worktree_object_id`. Entries are sorted by normalized path UTF-8 bytes:

- `index_mode` is `100644`, `100755`, `120000`, or `160000`, or `null` for an
  untracked path or staged deletion;
- `index_object_id` is the full lowercase Git object ID for `index_mode`, or
  `null` when `index_mode` is `null`;
- `worktree_kind` is `absent`, `regular`, `symlink`, or `gitlink`;
- `worktree_mode` is `100644` or `100755` for `regular`, `120000` for
  `symlink`, `160000` for `gitlink`, and `null` for `absent`;
- `worktree_sha256` hashes exact regular-file bytes or the UTF-8 symlink-target
  text without following the link, and is `null` for `absent` or `gitlink`;
  and
- `worktree_object_id` is the full lowercase checked-out submodule commit only
  for `gitlink`, and otherwise `null`.

A rename is represented by the old and new path states; rename heuristics are
not authority input. Empty directories are not entries. A dirty, unavailable,
or recursively linked submodule; special filesystem entry; junction or reparse
point not represented as a Git symlink; unsafe or non-UTF-8 path; case
collision; unsupported mode; or changing entry makes the observation
`not_assessable`.

The index must contain one stage-zero entry per tracked path. An unmerged stage,
intent-to-add or zero object ID, sparse-directory entry, `skip-worktree` bit,
or `assume-unchanged` bit makes the observation `not_assessable`; it may not be
flattened into a normal entry. Index extensions that do not change this semantic
entry set are not included in the digest. For an untracked
regular file, `worktree_mode` is `100755` only when the platform exposes its
executable bits unambiguously and at least one execute bit is set; otherwise it
is `100644`. For a tracked regular file, the evaluator uses Git's observed
worktree mode, including an unstaged executable-bit change. If that mode cannot
be determined, the observation is `not_assessable`.

The `formal_snapshot_sha256` value uses the existing formal snapshot algorithm:
sort every validated formal artifact by repository-relative `/` path encoded
as UTF-8; for each artifact hash an unsigned 8-byte big-endian path-byte length,
the path bytes, an unsigned 8-byte big-endian exact-content length, and the
exact file bytes. An invalid formal graph has no snapshot identity.
`managed_lock_sha256` hashes the exact `.engineering-harness.lock` bytes.
`work_order_sha256` hashes `utf8-text-lf-v1` bytes of the selected work order:
UTF-8 without a byte-order mark, with CRLF and CR normalized to LF and every
other byte preserved.

A future released-evaluator integration obtains two consecutive complete
repository observations. `HEAD`, tree, index entries, worktree entries, formal
snapshot, managed lock, and selected work-order digest must be identical in
both; otherwise derivation stops as stale. The binding uses the second
observation. Before a later effect, that integration obtains a fresh complete
observation and requires exact equality with the expected-current binding.

`WO-AEX-002` does not implement that live Git or filesystem observation. Its
pure functions accept the complete typed observation values above, validate
and canonicalize them, and construct a non-authoritative binding candidate. A
caller supplies expected repository and work-order identity but cannot turn a
candidate into authoritative state.

### Envelope construction request

The structured pure request contains:

- repository target and expected installed evaluator identity;
- selected work order and selected managed procedure;
- explicit actor assertion required by that procedure;
- requested operations, path or component-prefix scope, profiles, writer limit,
  retry limits, stop boundaries, and evidence obligations; and
- optional parent-envelope canonical bytes and digest; and
- complete already-observed state-binding inputs plus managed-scope and gate
  assessments supplied as untrusted typed data.

Requested delegated scope is untrusted input. The pure constructor validates
the supplied maximum managed scope and intersects it with the request. It never
broadens the request to fill an omitted capability and never claims that the
supplied observations are current or authoritative. A future exact released
evaluator obtains those inputs from current managed state and may label the
result authoritative only after performing the checks in `ADR-AEX-003`.

### Admission request and expected current state

A pure admission request contains the validated envelope bytes and digest, one
operation, target paths, execution profile, requested writer count, retry
ordinal, evidence plan, decision boundary, and the canonical expected-current
state observation.

In a later authorized effect integration, expected current state must equal the
state-binding object named by the envelope before the first admitted effect.
After that integration performs an admitted effect, its complete receipt
`state_after` becomes the expected-current observation for the next effect.
Every step therefore forms a validated before/after chain without changing the
envelope's original authority or widening its scope. Phase 2 compares supplied
typed values only and does not claim they are live.

### Decision-packet source

A decision packet accepts one canonical `se-harness-workflow-result-v2`, the
exact selected procedure step already present in that result, and one canonical
`se-harness-decision-packet-context-v1`. The source must already represent one
applicable decision or stop boundary. Raw prose, a model recommendation, a
partial workflow summary, or context that cannot be independently resolved
against the same managed state is not a valid source.

### Receipt expectations

Receipt validation accepts the canonical receipt plus the independently known
execution plan: selected scope, envelope digest when applicable, required
profiles, skill identities, operations, workers, evidence obligations, and
expected before/after observations. These expectations do not become fields in
the receipt and cannot be taken from the candidate receipt itself.

## Outputs

### Constructed envelope result

The Phase 2 pure constructor returns:

- outcome `constructed`, `blocked`, `not_assessable`, or `failed`;
- canonical state-binding bytes and digest when assessable;
- canonical envelope-candidate bytes and digest only for `constructed`;
- the exact selected work order, procedure, evaluator, and formal snapshot;
- normalized candidate scope and every narrowing applied to the request;
- stable diagnostics; and
- explicit non-effects stating that no mutation or accountable decision
  occurred.

`constructed` means structurally and semantically valid against the supplied
typed observations. It grants no authority. Only a future exact released
evaluator integration may relabel the same canonical bytes `derived`, after it
has itself obtained stable current observations and passed managed integrity,
workflow, gate, actor, work-order, and freshness checks. A parser, constructor,
skill, or caller cannot grant derivation authority.

### Validation and admission result

Pure validation returns a typed success value or stable diagnostics. Pure
admission assessment returns `admissible`, `denied`, `stale`,
`not_assessable`, or `failed`, the envelope digest, operation and normalized
scope, supplied expected-current identity, required evidence, and non-effects.
`admissible` means only that supplied semantic values satisfy the contract; a
future live evaluator/effect integration must independently establish authority
and may then label the operation `admitted`. Phase 2 invokes no callback and
performs no effect.

### Decision packet

Existing `se-harness-decision-packet-v1` objects remain valid compatibility
inputs. They cannot be the Phase 2 projection output because their approved
field tree has no location for selected scope or current lifecycle state.
Adding those fields under the same identifier would violate the approved schema
evolution rule.

The Phase 2 projection output is therefore
`se-harness-decision-packet-v2`. It adds one closed `context` object to the v1
tree and otherwise preserves v1 meanings. The projection provides exactly one
decision and preserves the source workflow result's selected artifact, current
state and scope, candidate and evaluator identity, required role, gate
assessments, blockers, recommendation, complete alternatives, findings,
assumptions, residual uncertainty, effects, non-effects, next step, command or
suggested response, and safe-deferral meaning.

### Execution receipt

The output remains `se-harness-execution-receipt-v1`. Validation reports exact
missing, duplicate, extra, inconsistent, secret-bearing, or authority-claiming
entries against independent expectations. A valid receipt is still evidence
only.

### Portable profile result

Reusable profile validation reports the stable profile name, purpose, operation
classes, default mutation class, prohibited decisions and actions, skill
capabilities, input and result schemas, requested runtime characteristics, and
single-agent fallback from one
`se-harness-logical-execution-profile-v1` object. It cannot name an accountable
role as profile authority or contain provider-specific configuration.

## Normative contract catalog

This section is the authority for `se-harness-agent-contract-catalog-v1`. The
distributed JSON catalog must encode these definitions exactly. It is not
permitted to add a field, variant, enum member, default, coercion, or extension
point that is absent here.

### Catalog meta-schema

The catalog root contains exactly:

| Field | Type | Rule |
| --- | --- | --- |
| `schema` | string | constant `se-harness-agent-contract-catalog-v1` |
| `canonical_encoding` | string | constant `se-harness-canonical-json-v1` |
| `schemas` | sequence of schema records | one record per top-level schema below, ordered by `id` UTF-8 bytes |
| `definitions` | sequence of definition records | one record per referenced type, ordered by `name` UTF-8 bytes |
| `diagnostics` | sequence of diagnostic records | ordered by numeric code |
| `bounds` | bounds record | exact ordinary and repository-observation bounds in this specification |

A schema record contains exactly `id`, `root`, and `compatibility`.
`compatibility` is always `fail-closed`. A definition record contains every one
of these fields: `name`, `kind`, `fields`, `variants`, `element`, `key_type`,
`value_type`, `enum`, `pattern`, `minimum`, `maximum`, `collection`,
`identity_field`, `ordering`, `max_items`, and `max_bytes`. Unused properties
are `null` or an empty array; omission is invalid.

- `kind` is `object`, `array`, `map`, `string`, `integer`, `boolean`, `null`, or
  `union`.
- Each object field record contains exactly `name`, `type`, and `required`;
  every field in this catalog has `required = true`. Nullability uses a named
  union containing `null`, never omission.
- `collection` is `scalar`, `sequence`, `set`, `identity-set`, or `map`.
- `ordering` is `none`, `source`, `utf8`, or `key-utf8`.
- An `identity-set` names its unique `identity_field`; a set has no identity
  field. Both are encoded in ascending UTF-8 byte order after validation.
- A map has string keys validated by `key_type`, values validated by
  `value_type`, and canonical key ordering. No other dynamic-key object exists.
- Every named type reference must resolve once, and no unused definition may be
  present.

The bounds record contains exactly `max_document_bytes`, `max_nesting`,
`max_object_members`, `max_array_entries`, `max_string_scalars`,
`max_path_bytes`, `max_collection_entries`, `max_parallel_writers`,
`max_retry`, `worktree_max_entries`, `formal_max_artifacts`,
`file_max_bytes`, `observation_max_file_bytes`, and `manifest_max_bytes`, with
the numeric values stated above. A diagnostic record contains exactly `code`
and `class` and matches the closed diagnostic table below.

The top-level schema records are:

| Schema ID | Root definition |
| --- | --- |
| `se-harness-autonomy-envelope-v1` | `autonomy-envelope` |
| `se-harness-decision-packet-context-v1` | `decision-packet-context` |
| `se-harness-decision-packet-v1` | `decision-packet` |
| `se-harness-decision-packet-v2` | `decision-packet-v2` |
| `se-harness-execution-receipt-v1` | `execution-receipt` |
| `se-harness-logical-execution-profile-v1` | `logical-execution-profile` |
| `se-harness-repository-state-binding-v1` | `repository-state-binding` |
| `se-harness-worktree-state-v1` | `worktree-state` |

The catalog itself is encoded canonically. Its lowercase SHA-256 is retained
outside the catalog and compared across source, wheel, and installed package.

### Shared scalar and collection rules

| Type | Exact rule |
| --- | --- |
| `bounded-text` | 1 through 16,384 Unicode scalar values; valid UTF-8; no byte-order mark, unpaired surrogate, U+0000 through U+001F, or U+007F |
| `short-text` | `bounded-text` limited to 512 Unicode scalar values |
| `portable-id` | ASCII full match `[a-z0-9](?:[a-z0-9._-]{0,126}[a-z0-9])?` |
| `profile-name` | ASCII full match `[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?` |
| `managed-id` | an identifier accepted by the installed managed registry for its declared kind; strings do not create a new registry entry |
| `artifact-id` | one exact artifact ID accepted by the formal artifact registry |
| `work-order-id` | an `artifact-id` whose type is `work_order` |
| `sha256` | 64 lowercase hexadecimal characters |
| `git-object-id` | 40 lowercase hexadecimal characters for `sha1`, 64 for `sha256` |
| `semantic-version` | ASCII semantic version accepted by `se-harness-skill-contract-v1` |
| `portable-path` | normalized repository-relative exact-file path defined by `AEX-CLOSE-005`, at most 1,024 UTF-8 bytes |
| `component-prefix` | `portable-path` ending in `/`; it matches only complete path components |
| `path-scope` | union of `portable-path` and `component-prefix` |
| `nullable-T` | exactly `null` or one valid `T`; empty string never means unavailable |

Unless a table says `sequence`, arrays are sets encoded in ascending UTF-8 byte
order. Identity sets are ordered by the UTF-8 bytes of their identity field.
Sequences preserve source semantic order and reject duplicate identity-bearing
entries. Objects reject duplicate and unknown keys. Integers are base-10 JSON
integers in the inclusive range `-(2^63 - 1)` through `2^63 - 1`; booleans are
not integers.

A portable path is NFC-normalized Unicode encoded as UTF-8 with `/` separators.
It has no leading `/`, trailing `/`, empty component, `.` or `..` component,
backslash, colon, wildcard, URI marker, control character, or NUL. No component
ends in a dot or space. The case-insensitive stem before the first dot may not
be `CON`, `PRN`, `AUX`, `NUL`, `COM1` through `COM9`, or `LPT1` through `LPT9`.
A component prefix follows the same rules before its one terminal `/`. Within
one object or observation, equal NFC paths and case-folded collisions are
invalid.

### Autonomy envelope

`se-harness-autonomy-envelope-v1` contains exactly this field tree:

| Path | Type and collection | Constraint |
| --- | --- | --- |
| `schema` | string | constant schema ID |
| `selection` | object | exact children below |
| `selection.work_order` | `work-order-id` | one selected approved or in-progress work order |
| `selection.work_order_sha256` | `sha256` | digest of selected canonical work-order bytes |
| `selection.repository_state` | `sha256` | digest of canonical repository-state-binding bytes |
| `selection.evaluator_payload_sha256` | `sha256` | exact released-evaluator payload identity expected by the repository |
| `delegation` | object | exact children below |
| `delegation.asserted_by` | `short-text` | explicit actor assertion; data, not proof of role ownership |
| `delegation.operations` | set of `managed-id` | 1 through 1,024 operation IDs |
| `delegation.path_scope` | set of `path-scope` | 1 through 1,024 non-overlapping entries; redundant descendants are invalid |
| `delegation.execution_profiles` | set of `profile-name` | 1 through 1,024 names |
| `delegation.max_parallel_writers` | integer | 0 through 32 |
| `delegation.retry_limits` | map `managed-id -> integer` | keys must be in `operations`; values 0 through 10 |
| `delegation.stop_before` | set of `managed-id` | must include `accountable-decision-required` and `action-time-authorization-required` |
| `evidence` | object | exact children below |
| `evidence.required_receipt` | boolean | must be `true` for any non-read-only operation |
| `evidence.required_paths` | set of `path-scope` | 0 through 1,024 entries, each within delegated path scope |

There are no optional fields or implicit permissions. A retry-limit map must
contain every operation exactly once; an operation that cannot retry has value
zero. `asserted_by` is preserved in a child envelope. Parent digest and
construction/derivation outcome remain outside the envelope to avoid
self-reference and authority confusion.

### Repository-state and worktree manifests

`se-harness-repository-state-binding-v1` contains exactly:

| Path | Type | Constraint |
| --- | --- | --- |
| `schema` | string | constant schema ID |
| `repository.git_object_format` | enum | `sha1` or `sha256` |
| `repository.head` | `git-object-id` | commit named by `HEAD`; unborn or detached-unreadable state is `not_assessable` |
| `repository.tree` | `git-object-id` | tree of `head` |
| `repository.worktree_state_sha256` | `sha256` | digest of the exact worktree-state object below |
| `governance.formal_snapshot_sha256` | `sha256` | complete valid formal snapshot |
| `governance.managed_lock_sha256` | `sha256` | exact managed-lock bytes |
| `governance.work_order` | `work-order-id` | same ID as the envelope |
| `governance.work_order_sha256` | `sha256` | same digest as the envelope |

`se-harness-worktree-state-v1` contains `schema`, `git_object_format`, `head`,
`tree`, and `entries`. The first four values equal their binding counterparts.
`entries` is an identity set ordered by `path`, bounded as specified above.
Every entry has all seven fields described in **Canonical repository-state
binding**; null and enum combinations outside that description are invalid.

The empty entry set is valid only when both Git index and non-ignored worktree
are empty. The worktree-state digest cannot be substituted by `git status`, a
tree ID alone, timestamps, file sizes, filesystem metadata, or a caller's dirty
flag.

### Decision-packet context

`se-harness-decision-packet-context-v1` is non-authoritative enrichment needed
because workflow-result v2 intentionally does not carry candidate identity,
evidence digests, or complete alternative procedure definitions. It contains:

| Field | Type and collection | Constraint |
| --- | --- | --- |
| `schema` | string | constant context schema ID |
| `repository` | `bounded-text` | portable repository identity |
| `candidate_commit` | nullable `git-object-id` | null only when no commit candidate is applicable |
| `evaluator_payload_sha256` | nullable `sha256` | null only when no evaluator observation is applicable |
| `evidence` | identity set of evidence bindings | ordered by `path`; each has exactly `kind`, `path`, and `sha256` |
| `assumptions` | set of `short-text` | explicit review assumptions |
| `residual_uncertainty` | set of `short-text` | uncertainty not represented as a gate or finding |
| `preview` | preview object | exact union below |
| `alternatives` | sequence of complete alternatives | one entry per source restitution alternative, same order |
| `safe_to_defer` | boolean | consequence statement is still required in packet rendering |

An evidence binding uses `kind: portable-id`, `path: portable-path`, and
`sha256: sha256`. A preview contains every field `kind`, `artifact`,
`from_status`, `to_status`, `action`, and `target`:

- `none`: the other five values are `null`;
- `lifecycle-transition`: `artifact`, `from_status`, and `to_status` are
  non-null managed values; `action` and `target` are null; or
- `external-action`: `action` and `target` are non-null short text; the three
  lifecycle values are null.

A complete alternative contains exactly `summary`, `procedure_id`,
`decision_right`, `subject`, `required_accountable_role`, `recommendation`,
`command_or_suggested_response`, `effects`, and `non_effects`. The first six
fields are bounded managed or short text, the command/response uses the union
below, and effects/non-effects are source-ordered short-text sequences. The
alternative must resolve through the current managed workflow registry for the
same repository-state binding; context bytes alone cannot authorize it.

### Decision packet and exact projection

`se-harness-decision-packet-v1` retains the exact root object and nested object
field sets approved in `SPEC-AEX-001`. Its formerly open entry types are closed
by the tables below. It is accepted for validation and canonical encoding but
is not generated from workflow-result v2.

`se-harness-decision-packet-v2` contains exactly `schema`, `context`,
`decision`, `identity`, `assessment`, `effect`, and `handoff`. All objects other
than `context` have the same exact fields and meanings as v1. `context`
contains:

| Path | Type and collection | Constraint |
| --- | --- | --- |
| `context.selected_artifact` | `artifact-id` | equals `selection.primary` and decision subject |
| `context.lifecycle_state` | `managed-id` | exact selected status before and after the stopped decision |
| `context.governing` | set of `artifact-id` | exact `scope.governing` |
| `context.dependencies` | set of `artifact-id` | exact `scope.dependencies` |
| `context.declared_paths` | set of `path-scope` | exact `scope.declared_paths` |
| `context.changed_paths` | set of `portable-path` | exact `scope.changed_paths` |
| `context.change_set_complete` | boolean | exact `scope.change_set_complete` |
| `context.procedure_id` | `managed-id` | exact selected procedure |
| `context.procedure_step_id` | `managed-id` | exact selected current step |

The common v1/v2 fields are:

| Path | Type and collection | Constraint |
| --- | --- | --- |
| `decision.kind` | `managed-id` | exact decision right from the source decision |
| `decision.subject` | `bounded-text` | exact source artifact or action subject |
| `decision.required_accountable_role` | `managed-id` | exact source role |
| `decision.recommendation` | `short-text` | one recommendation |
| `decision.alternatives` | sequence of complete alternatives | context-validated; may be empty |
| `identity.repository` | `bounded-text` | exact context value |
| `identity.candidate_commit` | nullable `git-object-id` | exact context value |
| `identity.evaluator_payload_sha256` | nullable `sha256` | exact context value |
| `assessment.gates` | sequence of gate entries | exact source order |
| `assessment.evidence` | identity set of evidence bindings | exact context values |
| `assessment.findings` | sequence of packet findings | selected blockers then repository blockers |
| `assessment.assumptions` | set of `short-text` | exact context values |
| `assessment.residual_uncertainty` | set of `short-text` | exact context values |
| `effect.preview` | preview object | v1 compatibility accepts only its approved empty object; v2 requires the exact context preview |
| `effect.effects` | sequence of `short-text` | exact selected procedure-step effects |
| `effect.non_effects` | sequence of `short-text` | exact selected procedure-step non-effects |
| `handoff.command_or_suggested_response` | command/response union | exact source restitution value |
| `handoff.safe_to_defer` | boolean | exact context value |

A command contains exactly `kind = "command"` and `argv`, a sequence of 1
through 1,024 bounded strings. A response contains exactly
`kind = "response"` and non-empty `value`. No shell string is reconstructed.

A gate contains exactly `id`, `status`, and `predicates`. A predicate contains
exactly `id`, `status`, `evidence`, and `message`. Gate and predicate status is
`pass`, `fail`, or `not_assessable`; evidence is a source-ordered sequence of
objects containing exactly `kind` and `reference`. A packet finding contains
exactly `scope`, `code`, `path`, `message`, and `plane`; `scope` is `selected`
or `repository`, while `path` and `plane` are nullable short text.

Projection uses this exact mapping:

| Packet target | Required source |
| --- | --- |
| `context.selected_artifact` | `selection.primary`, which must occur in `selection.artifacts` |
| `context.lifecycle_state` | the one `state.before` entry for the primary artifact; `state.after` must contain the same status because the packet stops before its effect |
| `context.governing`, `dependencies`, `declared_paths`, `changed_paths`, and `change_set_complete` | identically named `scope` fields; `scope.mode` must be `selected` |
| `context.procedure_id` | equal values from `compliance.procedure_id`, `procedure.id`, and `restitution.next.procedure_id` |
| `context.procedure_step_id` | equal values from `procedure.current_step` and `restitution.next.step_id` |
| `decision.kind` | `restitution.decision_required.decision_right` |
| `decision.subject` | `restitution.decision_required.artifact`, which must equal `selection.primary` |
| `decision.required_accountable_role` | `restitution.decision_required.role` |
| `decision.recommendation` | `restitution.next.action` |
| `decision.alternatives` | context entries whose `summary` values equal `restitution.alternatives` one for one |
| `identity.*` | exact context identity values |
| `assessment.gates` | `compliance.gates` without reordering or relabeling |
| `assessment.evidence` | exact context evidence bindings |
| `assessment.findings` | all `findings.scoped_blockers`, then all `findings.repository_blockers`, normalized only to the closed finding shape |
| `assessment.assumptions` and `residual_uncertainty` | exact context sets |
| `effect.preview` | exact context preview |
| `effect.effects` and `non_effects` | the step in `procedure.steps` whose ID equals `procedure.current_step` and `restitution.next.step_id` |
| `handoff.command_or_suggested_response` | `restitution.command_or_response`, which must equal the selected step's resolved command or response |
| `handoff.safe_to_defer` | exact context boolean |

The source must contain exactly one non-null `decision_required`; its selected
artifact, state, scope, procedure, and step IDs must agree across selection,
state, scope, compliance, procedure, restitution, and the context alternatives.
A blocked result without a complete decision is
`not_assessable` and produces no packet. A later evaluator integration must
therefore produce a complete workflow-result v2 decision at every boundary
where `REQ-AEX-003` requires a packet. Projection cannot repair an incomplete
workflow result.

Human rendering uses one deterministic heading in this order: Decision,
Subject, Accountable role, Current lifecycle state, Scope, Procedure,
Recommendation, Alternatives, Identity, Gates, Evidence, Findings,
Assumptions, Residual uncertainty, Preview, Effects, Non-effects, Safe to
defer, Command or response. It renders every collection entry once in canonical
order, labels null identity values `not applicable`, and adds no fact or
recommendation. Semantic equivalence means an independent renderer oracle
recovers the same scalar values, collection cardinalities, statuses, and
command argument sequence from both forms.

### Execution receipt

`se-harness-execution-receipt-v1` contains exactly `schema`, `selection`,
`execution`, `effects`, and `validation`, with this field tree:

| Path | Type and collection | Constraint |
| --- | --- | --- |
| `selection.repository` | nullable `bounded-text` | null only when repository identity could not be assessed |
| `selection.artifact` | nullable `artifact-id` | selected artifact when applicable |
| `selection.autonomy_envelope_sha256` | nullable `sha256` | null for non-envelope execution |
| `execution.profiles` | set of `profile-name` | at least one profile |
| `execution.skills` | identity set of skill entries by `name` | each has exactly `name`, `version`, and `portable_core_sha256` |
| `execution.operations` | sequence of operation entries | every planned operation represented once in plan order |
| `execution.worker_results` | identity set of worker entries by `id` | empty for single-agent execution |
| `effects.changed_paths` | set of `portable-path` | exact changed path set |
| `effects.evidence` | set of evidence entries ordered by canonical entry bytes | inline or retained variant below |
| `effects.state_before` | sequence of state entries | independently expected order |
| `effects.state_after` | sequence of state entries | same kinds and order as before when assessable |
| `validation.evaluator` | evaluator union | empty, Phase 1 basic, or payload-bound variant |
| `validation.gates` | sequence of gate entries | exact applied gate order |
| `validation.outcome` | enum | `completed`, `degraded`, `stopped`, or `failed` |
| `validation.deviations` | sequence of deviation entries | every deviation retained |
| `validation.residual_uncertainty` | set of `short-text` | may be empty |

A skill entry uses `name: profile-name`, `version: semantic-version`, and
`portable_core_sha256: sha256`. A state entry contains exactly `kind` and
`sha256`. State kinds are portable IDs; duplicate kinds are invalid.

The Phase 2 full operation entry contains every field `id`, `status`,
`exit_code`, `arguments_sha256`, `output_sha256`, and `evidence_path`.
`status` is `passed`, `failed`, `timed-out`, `cancelled`, `missing-output`, or
`not-assessable`. `exit_code` is nullable integer; the three digest/path fields
are nullable and may be null only when the corresponding observation does not
exist. The Phase 1 compatibility variant contains exactly `id`, `status`, and
`exit_code`, permits only `passed` or `failed`, and is valid only when profiles
is exactly `single-agent-orientation` and the envelope digest is null.

A worker entry contains exactly `id`, `profile`, `status`, `operation_ids`,
`changed_paths`, and `evidence`. Status is `completed`, `degraded`, `failed`,
`timed-out`, `cancelled`, or `missing-output`. Operation IDs are a source-order
sequence referencing receipt operations; paths are a set; evidence uses the
receipt evidence variants. Every independently planned worker ID must occur
once, including unsuccessful and missing-output workers.

An inline evidence entry contains exactly `kind` and `sha256`. It is retained
only for Phase 1 compatibility or evidence returned outside the target. A
retained evidence entry contains exactly `kind`, `path`, and `sha256`. For
envelope-governed work, every required evidence item uses the retained variant
and its path must be admitted by the envelope.

The evaluator union is exactly one of `{}`, `{identity, version}`, or
`{identity, version, payload_sha256}`. The empty variant is valid only when the
receipt outcome is `failed`; Phase 1 may use the basic variant; envelope-bound
work requires the payload-bound variant.

The Phase 2 deviation entry contains every field `code`, `operation`, `status`,
`message`, `evidence_path`, and `details_sha256`; all except `code` are nullable.
For byte compatibility, `single-agent-orientation` additionally admits only the
eight existing `AEXORI` field sets: `{code,diagnostics,operation}`,
`{code,expected,observed,operation}`, `{code,message,operation}`,
`{code,errors,operation}`, `{code,operation,status}`, `{code,operation,ready}`,
`{code,changed_paths}`, and `{code,message}`. Diagnostics are short-text
sequences; errors contain exactly `code`, `path`, `message`, and `plane`;
changed paths are portable paths. No other legacy field set is valid.

Receipt validation compares the receipt against an independent plan. It rejects
an unplanned operation, worker, profile, skill, path, evidence item, or state;
missing coverage; inconsistent outcome; an authority assertion; or any secret
or hidden-reasoning field. Receipt bytes remain evidence, not approval.

### Logical execution profile

`se-harness-logical-execution-profile-v1` contains:

| Field | Type and collection | Constraint |
| --- | --- | --- |
| `schema` | string | constant profile schema ID |
| `name` | `profile-name` | stable non-accountable identity |
| `purpose` | `bounded-text` | engineering purpose, not a role assertion |
| `operation_classes` | set of `managed-id` | at least one class |
| `default_mutation_class` | enum | `read-only`, `draft-writing`, `governed-mutation`, or `external-action` |
| `prohibited_decisions` | set of `managed-id` | decision rights or stop classes the profile cannot perform |
| `prohibited_actions` | set of `managed-id` | action classes the profile cannot perform |
| `required_skill_capabilities` | set of `portable-id` | may be empty |
| `input_schemas` | set of `portable-id` | accepted portable input schema IDs |
| `result_schemas` | set of `portable-id` | emitted portable result schema IDs |
| `runtime_characteristics` | set of `portable-id` | requests such as workspace-read or optional-subagents; no provider syntax |
| `single_agent_fallback` | boolean | must be `true` |

`prohibited_decisions` must include `accountable-decision-required` and
`action-time-authorization-required`. A profile name that equals an accountable
role remains non-authoritative and should be rejected as ambiguous by profile
policy. `external-action` describes a technical capability request only and
cannot remove the mandatory prohibited decisions or create action-time
authorization.

### Stable diagnostics

Every failure returns one primary code, semantic path, and bounded message.
These codes are closed for v1:

| Code | Class |
| --- | --- |
| `AEXCON001` | malformed bytes, invalid UTF-8, or invalid JSON |
| `AEXCON002` | resource bound exceeded |
| `AEXCON003` | duplicate key or duplicate collection identity |
| `AEXCON004` | unsupported catalog or schema identifier |
| `AEXCON005` | missing or unknown field |
| `AEXCON006` | invalid scalar, nullability, or collection type |
| `AEXCON007` | invalid enum, identifier, digest, or cross-reference |
| `AEXCON008` | invalid, ambiguous, or escaping portable path |
| `AEXCON009` | non-canonical object, bytes, or ordering |
| `AEXCON010` | widened child or request outside managed scope |
| `AEXCON011` | stale or mismatched repository, work-order, evaluator, or parent identity |
| `AEXCON012` | missing, conflicting, or non-authoritative actor assertion |
| `AEXCON013` | failed or not-assessable required gate |
| `AEXCON014` | incomplete or non-lossless decision-packet source or projection |
| `AEXCON015` | incomplete or inconsistent execution receipt |
| `AEXCON016` | authority claim, secret, hidden reasoning, or prohibited metadata |
| `AEXCON017` | invalid or provider-bound logical profile |
| `AEXCON018` | internal failure without partial result |

One input may produce additional diagnostics, but their codes must come from
this table and their order is semantic-path UTF-8 order then code. Messages do
not become compatibility keys.

## State model

The core contract layer is stateless. It introduces no formal lifecycle state.
For one call it moves only through these internal assessment stages:

```text
untrusted bytes
  -> bounded parse
  -> structural validation
  -> semantic validation
  -> identity and current-state comparison
  -> canonical object and digest
  -> constructed/admissible/projected/valid result or fail-closed diagnostic
```

Envelope authority is immutable after derivation. A narrower child is a new
canonical object with a new digest and a parent digest supplied to the
derivation/validation context. Repository changes update the expected-current
state chain, not the envelope's scope or identity.

## Behavioral rules

1. **AEX-CLOSE-001:** Parse every JSON object with duplicate-key detection and
   reject unknown fields, missing fields, invalid types, invalid Unicode,
   floats, non-finite values, and values outside the v1 bounds.
2. **AEX-CLOSE-002:** Fail closed on an unknown schema or catalog identifier.
3. **AEX-CLOSE-003:** Canonicalize accepted semantic objects using
   `se-harness-canonical-json-v1`; the digest is lowercase SHA-256 over the
   canonical bytes and remains outside the object.
4. **AEX-CLOSE-004:** Normalize declared sets to stable unique order and retain
   declared sequence order. Reject duplicates where the catalog declares a
   sequence or identity-keyed collection.
5. **AEX-CLOSE-005:** Validate paths as repository-relative portable paths or
   explicit component prefixes. Reject absolute, traversal, dot, empty,
   wildcard, URI, drive, device, alternate-separator, control-character,
   case-collision, and escape forms.
6. **AEX-CLOSE-006:** Derive authoritative envelope bytes only through the exact
   released evaluator after managed integrity, selected procedure, applicable
   gates, actor assertion, work-order scope, and repository state are
   assessable.
7. **AEX-CLOSE-007:** Treat runtime permissions, skill/profile names, prompts,
   model output, caller-supplied envelope bytes, and successful commands as
   non-authoritative inputs.
8. **AEX-CLOSE-008:** The constructed envelope-candidate scope is the
   intersection of the maximum managed scope and the requested scope. Omission
   never creates a default permission.
9. **AEX-CLOSE-009:** A child envelope is valid only when work order,
   repository-state anchor, evaluator identity, and reserved stop boundaries
   are preserved and every operation, path, profile, writer, retry, and evidence
   dimension is equal to or narrower than the parent.
10. **AEX-CLOSE-010:** `accountable-decision-required` and
    `action-time-authorization-required` are mandatory stop boundaries and
    cannot be removed by a request, child, retry, skill, profile, or adapter.
11. **AEX-CLOSE-011:** During pure assessment, compare every supplied selected
    work-order, evaluator-payload, formal-snapshot, parent, and expected-current
    repository identity. Any mismatch is stale or denied. A future effect
    integration repeats the comparison against a fresh live observation before
    an effect.
12. **AEX-CLOSE-012:** A retry repeats only the same admissible operation and
    scope within its declared bound; it cannot select another path, profile,
    decision class, evidence obligation, or external target.
13. **AEX-CLOSE-013:** Phase 2 parsing, observation validation, candidate
    construction, narrowing, admission assessment, projection, encoding, and
    digesting perform no filesystem, Git, lifecycle, process, credential,
    network, or external effect.
14. **AEX-CLOSE-014:** Project a decision packet only from one complete
    applicable workflow result, its selected procedure step, and one exact
    packet context. Do not infer a decision from successful execution or
    free-form prose.
15. **AEX-CLOSE-015:** Packet projection is lossless for decision-relevant
    semantics; human rendering and JSON cannot disagree.
16. **AEX-CLOSE-016:** Include an alternative only when it is complete and
    authorized for the same current state. Preserve failed and not-assessable
    gates without positive relabeling.
17. **AEX-CLOSE-017:** Validate receipt operation and worker coverage against
    independent expectations. Failed, stopped, timed-out, cancelled, and
    missing-output work remains visible.
18. **AEX-CLOSE-018:** Reject receipt authority claims, unplanned changed paths,
    missing state links, unsatisfied evidence obligations, secret-bearing
    values, hidden reasoning, and inconsistent evaluator or envelope identity.
19. **AEX-CLOSE-019:** Validate portable logical profiles independently from
    accountable roles and runtime-provider syntax; require deterministic
    single-agent fallback.
20. **AEX-CLOSE-020:** Persist envelope, packet, receipt, or state-binding bytes
    only at a repository-relative path predeclared by an approved work order or
    evidence obligation. Persistence grants no authority and is outside the
    Phase 2 pure contract implementation.

## Error and recovery behavior

Diagnostics use stable `AEXCON` codes and identify the schema, semantic path,
and failure class without echoing secret values or unnecessary repository
content. At minimum the implementation distinguishes malformed input, resource
bound, unsupported schema, unknown or duplicate field, invalid identity,
invalid path, widened child, stale state, missing authority assertion, failed or
not-assessable gate, incomplete packet projection, incomplete receipt,
authority claim, and internal failure.

No partial canonical object, digest, constructed candidate, derived envelope,
admission, packet, or valid receipt is returned on failure. Phase 2 recovery
requires corrected typed input. A later authority integration requires a fresh
released-evaluator derivation from current state. Retrying the same stale or
invalid bytes cannot change the result.

## Data and interface contracts

- All portable text is UTF-8 without a byte-order mark.
- Canonical objects end in exactly one LF and contain no insignificant
  whitespace.
- Digests are 64 lowercase hexadecimal characters.
- SHA-1 Git object IDs contain 40 lowercase hexadecimal characters; SHA-256 Git
  object IDs contain 64. The declared object format fixes the accepted length.
- Artifact and managed identifiers use the existing harness identifier
  grammars; this specification does not create a parallel identifier registry.
- Portable paths use `/`; component prefixes end in `/` and paths do not.
- Contract functions accept and return immutable semantic values or canonical
  bytes. Host paths, command launchers, timestamps, thread IDs, model names, and
  provider configuration remain outside portable objects unless an existing
  approved field explicitly admits a bounded observation.
- The contract catalog is distributed exactly once in source and package data.
  Candidate and installed bytes and digests must match.

## Security and privacy properties

- Treat every input, including formal files and evaluator output, as untrusted
  until its exact applicable validation passes.
- Parse and validate before allocating unbounded structures or invoking any
  effect-capable dependency.
- Prevent path traversal, symlink or junction escape, case ambiguity, reserved
  device names, alternate data streams, and ambiguous normalization.
- Do not evaluate contract strings as shell commands, templates, expressions,
  code, regular expressions supplied by the caller, or provider configuration.
- Never record credentials, tokens, environment dumps, private evidence bodies,
  conversation transcripts, or hidden reasoning in portable objects or normal
  diagnostics.
- Technical permissions and evaluator derivation do not authenticate the
  real-world actor; they only enforce the repository contract using the
  supplied actor assertion.
- A copied, replayed, modified, or stale envelope fails identity/current-state
  validation and cannot reach admission.

## Performance and capacity

- Validate and canonicalize bounded objects in time linear in their encoded
  size plus declared set-order normalization.
- Do not walk the repository when parsing an already supplied semantic object.
- A future released-evaluator observation may walk repository entries twice to
  establish a stable pair and must use deterministic streaming digests rather
  than retain file bodies. The Phase 2 pure module performs no walk.
- Report duration and peak memory for deterministic fixtures near 100, 500, and
  1,000 formal artifacts and near each declared collection bound.
- Reject over-bound data before expensive semantic comparison where possible.

## Observability

Return schema and catalog identifiers, canonical digest, evaluator payload and
formal snapshot when applicable, selected work order/procedure, normalized
scope counts, narrowing summary, state-binding digest, outcome, and stable
diagnostic codes. Do not expose host-absolute paths, raw secrets, full private
evidence, or hidden reasoning.

Receipts distinguish constructed, admissible, derived, and admitted contract
digests and record the before/after state chain. Decision packets bind evidence
paths and digests but normally summarize evidence content.

## Compatibility and migration

- Existing `harness-orient` behavior, portable-core digest, and
  `se-harness-skill-contract-v1` contract remain valid.
- Existing `se-harness-decision-packet-v1` bytes remain valid for validation
  and evidence. Phase 2 generates v2 because its required `context` fields
  cannot be added compatibly to v1.
- `SPEC-AEX-001` and `SPEC-AEX-002` remain the semantic baseline. This
  refinement resolves their explicitly deferred Phase 2 decisions without
  modifying their approved bytes.
- A new field, changed meaning, relaxed/widened rule, different canonical
  encoding, or incompatible bound requires a new schema/catalog identifier and
  accountable review.
- Repositories without an envelope continue through command-driven managed
  workflow. No automatic migration creates delegated mutation authority.
- A future mutation integration must use a released evaluator containing this
  approved contract and separately authorize its work order and effects.

## Examples and counterexamples

### Example: narrower construction and later derivation

An in-progress work order admits `se_harness/` and `tests/`. A caller requests
one test operation and `tests/test_agent_contract.py`. The pure constructor
produces a non-authoritative candidate for only that operation and path, with
mandatory stop boundaries and receipt evidence. A later released-evaluator
integration may label those exact bytes derived only after obtaining the
required stable current observations. The request does not inherit omitted
source-write authority.

### Example: chained expected state

A later authorized integration performs one admitted write. Its complete
receipt binds the prior expected state and new `state_after`. The next admission
uses that `state_after` as expected-current state while preserving the original
envelope identity and scope.

### Counterexample: skill-authored envelope

A skill emits structurally valid envelope JSON with wider paths. The parser may
report valid structure, but derivation authority is absent and admission is
denied. Renaming the skill or granting workspace-write permission changes
nothing.

### Counterexample: incomplete receipt

Three workers were required and one timed out. A receipt containing only two
successful workers is invalid even if the candidate tests pass.

### Counterexample: packet hides a gate failure

The source workflow result contains a not-assessable required gate. A packet
that recommends approval without that gate is not a lossless projection and is
rejected.

## Explicitly unspecified decisions

- Private Python type, helper, and cache names inside the approved work order.
- Verifier fixture directory subdivision inside the approved path prefix.
- Whether a later approved effect integration invokes the pure admission API
  through a Python call or an added harness command.
- Runtime-specific models, tools, sandboxes, permissions, hooks, agent formats,
  and adapter files.
- Real-world actor authentication and cryptographic decision signatures.

None of these decisions permits changing a public schema, contract bound,
authority source, repository-state binding, canonical encoding, workflow rule,
mutation behavior, or evidence obligation during `WO-AEX-002` implementation.
