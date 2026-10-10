+++
id = "SPEC-HAG-008"
type = "specification"
title = "Concise hosted authoring through the existing client"
status = "approved"
owners = ["mmzen"]
created = "2026-10-08"
updated = "2026-10-10"
contract = "Reduce instruction reads, repeated payloads and sequential calls with focused instruction views, typed existing operations, exact file input and concise evidence-backed results."

[relations]
specifies = ["REQ-HAG-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-08T16:03:26Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the reviewed REQ-HAG-014, SPEC-HAG-008, VER-HAG-008 and WO-HAG-011 package on 2026-10-08. Approves the bounded client and instruction implementation with required commit-bound verification. Includes ordinary review pushes and updates to draft PR #543 in mmzen/se_harness, source codex/hosted-agent-qualification, target main, its ready verification record and the later separately supplied verification-decision commit. Keep the PR draft while WO-HAG-009/010 qualification remains incomplete. Git remains authoritative. No human verification acceptance, merge, force-push, release, adoption, host-plugin update, permission bypass or changed qualification criterion is granted."
+++

# Concise hosted authoring through the existing client

## In plain words

Keep the agent responsible for the change and the client responsible for its
mechanical representation. Return enough to take the next intended action
without another call merely to extract or decode the previous answer.

## Scope

The private hosted authoring route in the installed CLI, its plugin guidance,
and the native qualification adapter. Existing service and evaluator contracts
are constraints, not implementation targets. Existing raw request/result modes
remain compatible. No server endpoint, wire schema, persistence format, decision
right, new dependency, background service or selection store is introduced.

Reuse INT-HAG-002 and CAP-HAG-002. ARCH-HAG-003 and ADR-HAG-003 remain background
constraints: the existing client-to-service boundary and released evaluator are
unchanged. No new architecture decision is required for presentation and input
adaptation inside the existing client. If that boundary proves insufficient,
return the affected scope for review instead of extending it silently.

## Terms

- **Instruction view:** complete selected sections copied from identified
  canonical resources, with path, heading and release/digest provenance.
- **Compact result:** selected exact fields and a readable document when small,
  with explicit references to the retained complete result. It is not a verdict.

## Rules

**HAG-EFF-001.** Read the applicable instructions.

Keep common skill entry points short. Route hosted, repository and private
lifecycle tasks to the matching references without loading every route. Each
normative rule has one canonical owner; skills select it rather than restate it.
Move existing route detail into references, preserving its meaning. Do not add
test-specific restrictions to ordinary repository instructions.

Use existing resource resolution and returned instruction-discovery references.
A client-side section reader may assemble the shared prerequisites and selected
artifact checklist in one view. It MUST use the selected release, preserve the
complete sections and expose source identity. It MUST NOT invent a next step or
silently summarize away obligations. Unknown headings, missing files and identity
mismatches fail explicitly. No service response supplies a trusted local path.

Exact source/template paths come from selected inputs or actual operation results.
The test adapter may resolve its staged inventory mechanically; it MUST NOT
choose a semantic subset of source content, supply a completed artifact or script
the workflow. The bounded complete-input delivery below is permitted only for
the operator-selected fixture; it supplies original inputs, not an authored answer.
No full inventory is required for the normal known-input path. Reuse retained unchanged
instruction content; recover applicable rules after compaction or a context change.

**HAG-EFF-002.** Use typed operations and ordinary files.

Extend the existing remote CLI for import, draft-open, create-artifact,
revise-artifact and revision read with typed inputs for their current contracts.
Keep their raw request-file mode. Reject mixed or conflicting input modes.
Do not create a new operation that silently performs an entire authoring workflow.

The agent selects the operation, target, content, expected versions and retry key.
The client constructs the existing envelope, reads exact manifest/document bytes,
encodes them, computes mechanical digests and uses the installed client identity.
Do not silently obtain newer versions, allocate a different retry key or retry a
mutation after a conflict or unknown response. Preserve current limits and guards.
Credentials stay in their existing environment-variable route, never in artifacts
or evidence. Inputs that cannot form the existing request fail before sending.

**HAG-EFF-003.** Return a useful answer once.

Offer a compact result mode backed by an explicitly selected new local evidence
destination. Retain the request without credentials, actual response, command
exit and uncertainty. Preserve exact response/document bytes and existing raw mode.
Present operation outcome, selected IDs, versions, receipt identity, actionable
validation findings and the required instruction references together. Render
small document text directly or return its decoded exact local file path; do not
send the agent both a full base64 value and its duplicate text.

List omitted content and its location. Do not hide a failure to fit a display
budget. Large findings are explicitly incomplete and remain required reading
before a conclusion. Evidence-write failure after a remote commit must identify
the possible committed effect and recovery key; it is not a not-sent result.
New destinations must preserve unrelated files and reject unsafe/linked paths.

**HAG-EFF-004.** Preserve evidence and native choice.

The qualification adapter uses the installed public client for the new behavior;
it adds only its existing permission boundary, fixture lookup and capture. No
second implementation of client encoding, policy or result interpretation.
Generate mechanical evidence summaries from command records. Include recovered
failures and native permission denials in the independent assessment. An agent
adds the content judgement and limitations; a successful exit proves neither.

Keep the required independent readback and uncertain-reply checks. Batch only
independent reads; preserve the order and authorization of dependent mutations.
An explicit read/receipt lookup remains available even if the preceding result
already contains the useful fields.

**HAG-EFF-005.** Measure duration as well as context.

Keep Opus10 as historical evidence: 673.18 seconds, 56 native tool calls and
112,326 peak input-context tokens, including 16,397 initial host-context tokens.
Its task requests an intent for an already-defined greeting. Retain that exact
request and all original EFF-04A evidence as historical observations. Use the
separately identified EFF-04A2 request in VER-HAG-008 for subsequent missing-input
qualification. It asks for a new change without a same-outcome example in the
fixture. Existing failures remain failures; the new case cannot repair them.
Do not compare the two tasks as equivalent performance samples.

Use EFF-04B's one-verification-contract task as the positive authoring case. The
goals remain less than 180 seconds, at most 15 native calls and less than 40,000
peak input-context tokens. Report each as met, missed or unavailable, separately
from correctness. These measurements introduce no lifecycle gate or waiver.

The new task is not comparable to Opus10 as a same-task performance measurement.
Establish its own observations. Compare repeated runs only when their model,
task, fixture, permissions, candidate and fresh-project work match. Include import,
draft creation and final reporting inside the clock. Report preparation/build time
separately. An existing-project trial is a separate case.

Measure session start through final saved output/report. Retain calls, model turns,
provider-reported peak context, initial context, failures and retries. Record tool
durations only where observable; leave provider time unclassified. A visible-call
lower bound is not an exact total. A stopped or incomplete draft is not positive
authoring success. Report the negative diagnostic's costs separately.

**HAG-EFF-006.** Apply KIS to the whole task.

Apply the existing Design simplicity policy. Review every instruction and call
against an actual decision, required effect or concrete failure boundary. Prefer
ordinary files and existing client code. Remove superseded guidance and transport
work from the agent route; do not merely put another wrapper around every call.

Do not invent product outcomes to fill a template. Report a task/template mismatch
honestly. The two explicit qualification cases in VER-HAG-008 separate this
negative behavior from successful drafting of an applicable verification contract.
Any later semantic amendment must be proposed separately. This change does not alter
accepted artifact content requirements, verification criteria or the KIS policy.
Use existing artifact/review evidence for these choices; add no KIS artifact,
automatic score, separate approval, benchmark framework or CI job.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Missing selected instruction or invalid section | Report the missing source/heading; no guessed fallback | Existing error route plus exact input |
| Invalid file, mixed input modes or version input missing | Refuse before network mutation | Client input error |
| Stale version or reused key with different bytes | Preserve the service conflict; no automatic rewrite/retry | Existing service result |
| Reply lost or local evidence write fails after send | Preserve uncertainty and recovery identity | Unknown outcome; do not claim rollback |
| Compact output omits large findings | Mark the view incomplete and point to the exact retained content | No success inferred from truncation |

## Examples

Given an authored UTF-8 file, typed revision input produces the same semantic
wire request and exact document bytes as the existing raw request (HAG-EFF-002).
Given a successful create, its compact view supplies the template text or decoded
file location without an extra base64 extraction call (HAG-EFF-003).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-HAG-014` | HAG-EFF-001, HAG-EFF-002, HAG-EFF-003, HAG-EFF-004, HAG-EFF-005, HAG-EFF-006 |

## Not decided here

- Exact CLI option names and internal function layout, documented before the native run.
- Concise presentation layout and byte budgets, provided omitted findings stay explicit.
- Any later evaluator, service, schema, template-policy or production deployment change.

## Linked qualification revision

This revision replaces the complete accepted SPEC-HAG-008 file at commit `71bd0751dba3cd5305e8c9a07ec7e49bbc08239a`
with SHA-256 `a07260341d4ce5fb84c8e07a19c57cb3380b8a7f0a312960c9d910c30b9b26d5` and recorded state `approved`.
The [accepted bytes](../evidence/WO-HAG-011/amendment-20261009/SPEC-HAG-008.accepted.txt)
remain unchanged. Earlier work and evidence keep that definition reference.
The [activation record](../evidence/WO-HAG-011/amendment-20261009/activation.json)
identifies the actual human decision, before/after digests and effect on selected
WO-HAG-011. This link proposes no new machine relation or lifecycle event.

## Bounded complete-input delivery

For the focused EFF-04 trials, the operator MAY select one initial entry containing
the complete existing staged source fixture. Include every file inventoried under
the selected source root, not a helper-selected subset of relevant paragraphs.
Retain each source path, byte count and digest. Include exact applicable instruction
sections and selected setup/tool references once, with their source identities.
Use only the existing instruction and fixture readers; no new service or framework.

This entry is a read-only presentation. It MUST NOT modify source files, summarize
their content, supply a completed new artifact, identify the expected content gap,
choose operation order or run a workflow. Each UTF-8 source is copied completely
with its line endings preserved. Keep the original files available. Mark source
records as task data, not instructions or new authority. A pointer is not a read;
reading this complete entry is a content read of the included files.

Check path containment, the staged inventory and manifest identities before
assembly. Refuse missing, changed, linked, duplicate, non-UTF-8 or oversized inputs.
The complete entry MUST fit 64 KiB; do not truncate, select a semantic subset or
silently fall back. The operator may select the existing pointer route in a new
run. No credentials, previous trial, answer, private reasoning or unrelated file
may enter the fixture. Keep the selected accepted requested outcome unchanged and the assessor
case classification out of the data transformation.

Native agents still select each operation, artifact ID, document and conclusion.
Keep the current model, permission boundaries, tool capabilities, released governor
and content criteria. This delivery option does not establish automatic startup
or compaction qualification. Report its instruction/source bytes and preparation
time separately; include the first entry read in native wall time and context.

## Linked complete-input revision

This revision preserves the complete accepted SPEC-HAG-008 at commit
`a6d85f8d7431728e13bf39b5c48c90f064cd0656`, SHA-256 `02b199be5ae7fb867a6fda43f29ac1f3e6ef2bfd2cab2610150fdd8e4e22627c`, in
`../evidence/WO-HAG-011/input-delivery-20261010/SPEC-HAG-008.accepted.txt`.
The matching activation record must identify the actual human decision and exact
before/after digests before this revision is applied. Earlier evidence retains
its original definition and input-delivery references. Keep prior lifecycle events
unchanged; this link grants no authority by itself.

## Linked diagnostic revision

This revision preserves the complete accepted SPEC-HAG-008 at commit
`8ed1ae5391ec1b405b132b9d120ab91a47803cca`, SHA-256 `805c9da66ca26c1d56b767bbd3e8545229a0c1f9a46a2846b95fcc04c98da343`, and recorded
state `approved` in
`../evidence/WO-HAG-011/diagnostic-review-20261010/SPEC-HAG-008.accepted.txt`.
The activation record must identify the actual human decision and exact
before/after digests before this revision governs work. Earlier evidence keeps
its original definition and task references. No machine relation or lifecycle
event is invented by this link.
