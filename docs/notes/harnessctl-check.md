# `harnessctl check`: what it evaluates, and why it refuses

<!-- Target expertise: 6/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

This note explains one command. It is human-readable guidance derived from
the installed contracts, `docs/engineering/WORKFLOW.json` and
`docs/engineering/QUALITY_GATES.json`; those files and `harnessctl` itself
are authoritative, and nothing here grants approval, verification, or release
authority. The command surface is listed in the
[`harnessctl` reference](harnessctl-reference.md).

## What the command does

`harnessctl check` answers one question about one selected artifact at one
moment: *at this checkpoint, do the gates the workflow requires pass?* It
reads the repository, evaluates predicates, and prints the result as the
canonical schema-2 block (`--json` for the machine form). It is read-only in
every respect but one: a completed handoff check derived from Git retains its
own result as `handoff.json` in the work order's evidence directory.

```text
harnessctl check [TARGET] --artifact WO-...|VREC-...|RLS-... [--include-background] [--json]
harnessctl check [TARGET] --artifact WO-...|VREC-...|RLS-... \
  --checkpoint start|pre-action|transition|handoff|scope [--target STATE] \
  [--procedure PROC-...] [--from-git BASE | --changed-path PATH ... \
  [--changes-complete] | --change-manifest PATH] [--pull-request-body PATH] [--json]
```

What it does **not** do:

- it changes no lifecycle state; `harnessctl transition --apply` does that,
  after the accountable person decides;
- it approves, verifies, releases, commits, pushes, or publishes nothing;
- it does not pick the artifact for you; `harnessctl next` does that, and
  `check` needs `--artifact`;
- without `--checkpoint` it evaluates nothing: it *projects* the selected
  rule, procedure and next step (what `harnessctl focus` returned before
  se-harness 0.11.0; `focus` remains one release as a byte-identical alias
  that prints a deprecation notice);
- it does not decide; it names the decision that is due and who owns it.

## The five checkpoints

A checkpoint is the moment in a procedure at which the command is run. Each
one needs different inputs and evaluates different gates.

| Checkpoint | When it is used | Extra input | What is evaluated |
| --- | --- | --- | --- |
| `start` | before an approved work order begins | none | the selected rule's gates (for a work order: `QG-G3-WORK-AUTHORIZATION`, which includes the start preflight) |
| `pre-action` | before any decision step of any procedure | `--procedure PROC-...` (the selected procedure or one declared alternative) | the rule's gates plus the gates of the procedure's first step |
| `transition` | to preview exactly what `transition --set ID=STATE` will evaluate | `--target STATE` | the predicates bound to that artifact family and target state in `QUALITY_GATES.json`, plus the structural `QGS-*` checks |
| `handoff` | when an `in_progress` work order's implementation is offered for completion | a change set (see below) | `QG-G4-IMPLEMENTATION-EVIDENCE`: status, graph, integrity, scope, change-set completeness, path scope, review preflight, evidence packet |
| `scope` | on every pull request, whatever the work order's state; also by hand, to ask "is this diff inside scope?" | a change set (see below) | the three scope predicates of `QG-G4-IMPLEMENTATION-EVIDENCE` only: `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE`, `QGP-G4I-PATHS`; nothing is written |
| *(none)* | to ask "which rule applies and what is next?" without evaluating anything — the procedure steps `STEP-WO-START-FOCUS`, `STEP-FOCUS-SELECTED`, `STEP-FOCUS-RELATED`, `STEP-REMEDIATE-FOCUS` | `--include-background` optionally | no gate; the rule, procedure, current step, decision required and background count |

Each gate declares the checkpoints at which it applies. A rule whose gate is
not declared for the requested checkpoint is refused with `WEX210: gate
QG-... does not apply at checkpoint ...`. This is why a handoff check is only
defined while the work order is `in_progress`: once it is `implemented`, the
rule selects a different gate, and the handoff checkpoint no longer applies to
it. The `scope` checkpoint is the one exception to "the state selects the
gate": it always evaluates `QG-G4-IMPLEMENTATION-EVIDENCE`, whose scope
predicates declare `scope` and whose other predicates do not, so a work order
in any state — `draft` included — is checked against its declared scope and
against nothing else. It exists for the managed pull-request gate, which
before se-harness 0.10.0 ran the handoff check unconditionally and was
therefore red from a work order's completion to its merge (issue #255).

## How the artifact's state selects the rule

`check` does not take a rule as input. It selects the first rule of
`WORKFLOW.json` whose selector matches the artifact's type, its state, and,
where the selector says so, the state of a directly related record. Rules are
ordered, so the first match wins: an `implemented` work order with a `ready`
verification record selects `WFL-WO-READY-VREC`, never `WFL-WO-PREPARE-VREC`.

| Rule | Artifact | State | Related record | Procedure (alternatives) | Gates | Decision right |
| --- | --- | --- | --- | --- | --- | --- |
| `WFL-WO-READY-VREC` | work order | `implemented` | VREC `ready` | `PROC-FOCUS-RELATED` | `QG-G4-ASSURANCE-DECISION` | `DR-VREC-DECIDE` |
| `WFL-WO-VERIFIED-VREC` | work order | `implemented` | VREC `verified` or `released` | `PROC-DELIVERY-SELECT` (`PROC-REPOSITORY-INTEGRATION`, `PROC-PREPARE-RELEASE`) | `QG-G4-VERIFIED-COVERAGE` | `DR-DELIVERY-SELECT` |
| `WFL-WO-PREPARE-VREC` | work order | `implemented` | none | `PROC-WO-PREPARE-VREC` | `QG-G4-CANDIDATE-READY` | `DR-VREC-PREPARE` |
| `WFL-WO-START` | work order | `approved` | | `PROC-WO-START` | `QG-G3-WORK-AUTHORIZATION` | `DR-WO-START` |
| `WFL-WO-IMPLEMENT` | work order | `in_progress` | | `PROC-WO-IMPLEMENT` | `QG-G4-IMPLEMENTATION-EVIDENCE` | `DR-WO-COMPLETE` |
| `WFL-WO-COMPLETED` | work order | `verified`, `released` | | `PROC-FOCUS-SELECTED` | none | `DR-RELATED-RECORD-SELECT` |
| `WFL-VREC-DECIDE` | verification record | `ready` | | `PROC-VREC-DECIDE` (`PROC-VREC-REJECT`, `PROC-VREC-SUPERSEDE`) | `QG-G4-ASSURANCE-DECISION` | `DR-VREC-DECIDE` |
| `WFL-VREC-DELIVER` | verification record | `verified`, `released` | | `PROC-DELIVERY-SELECT` (`PROC-REPOSITORY-INTEGRATION`) | `QG-G4-VERIFIED-COVERAGE` | `DR-DELIVERY-SELECT` |
| `WFL-RLS-DECIDE` | release record | `ready` | | `PROC-RLS-DECIDE` (`PROC-RLS-REJECT`) | `QG-G5-RELEASE-DECISION` | `DR-RLS-DECIDE` |
| `WFL-RLS-EXTERNAL` | release record | `released` | | `PROC-EXTERNAL-ACTION` | `QG-G5-EXTERNAL-ACTION` | `DR-EXTERNAL-ACTION` |
| `WFL-REJECTED` | any | `rejected` | | `PROC-REMEDIATE` | none | `DR-REMEDIATION-SCOPE` |
| `WFL-VREC-SUPERSEDED` | verification record | `superseded` | | `PROC-FOCUS-SELECTED` | none | `DR-RELATED-RECORD-SELECT` |
| `WFL-DEFINITION-COMPLETE` | definition | `approved` | | `PROC-DEFINITION-COMPLETE` | `QG-G1-DEFINITION`, `QG-G2-ARCHITECTURE` | `DR-DEFINITION-DECIDE` |
| `WFL-DEFINITION-WORK` | definition | `implemented` | | `PROC-DEFINITION-WORK` | `QG-G3-WORK-AUTHORIZATION` | `DR-WO-SELECT` |
| `WFL-DEFAULT-REVIEW` | any | any | | `PROC-FOCUS-SELECTED` | none | `DR-RELATED-RECORD-SELECT` |

"Definition" means an intent, capability, requirement, specification,
architecture, ADR, verification, release contract, or operating contract.
`check` itself accepts only a work order, a verification record, or a release
record (`WEX210` otherwise); `next` projects the other types.

The procedure is a typed list of steps, each either a `command` (an argument
array the harness can run) or a `decision` (a decision right and its permitted
outcomes). `check` reports the step the procedure is at: after a passing
`start` or `handoff` check that is the decision step; after a blocked one it
is the command to retry (the preflight or the check itself).

## Gates and predicates by checkpoint

A gate is a named group of predicates. A predicate has a stable identifier, an
evaluator, and a status of `pass`, `fail`, or `not_assessable`. The gate's
status is the worst of its predicates, and a check completes only when every
gate passes and no repository-level error is present.

| Gate | Applies at | Predicates |
| --- | --- | --- |
| `QG-G0-INTENT` | `pre-action`, `transition` | `QGP-G0-GRAPH`, `QGP-G0-INTEGRITY` |
| `QG-G1-DEFINITION` | `pre-action`, `transition` | `QGP-G1-GRAPH`, `QGP-G1-INTEGRITY`, `QGP-G1-AUTHORING` |
| `QG-G2-ARCHITECTURE` | `pre-action`, `transition` | `QGP-G2-GRAPH`, `QGP-G2-INTEGRITY`, `QGP-G2-AUTHORING` |
| `QG-G3-WORK-AUTHORIZATION` | `start`, `pre-action`, `transition` | `QGP-G3-STATUS`, `QGP-G3-GRAPH`, `QGP-G3-INTEGRITY`, `QGP-G3-SCOPE`, `QGP-G3-PREFLIGHT` |
| `QG-G4-IMPLEMENTATION-EVIDENCE` | `pre-action`, `transition`, `handoff`; `scope` for `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE`, `QGP-G4I-PATHS` only | `QGP-G4I-STATUS`, `QGP-G4I-GRAPH`, `QGP-G4I-INTEGRITY`, `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE`, `QGP-G4I-PATHS`, `QGP-G4I-PREFLIGHT`, `QGP-G4I-EVIDENCE` |
| `QG-G4-CANDIDATE-READY` | `pre-action`, `transition` | `QGP-G4C-STATUS`, `QGP-G4C-GRAPH`, `QGP-G4C-INTEGRITY` |
| `QG-G4-ASSURANCE-DECISION` | `pre-action`, `transition` | `QGP-G4A-GRAPH`, `QGP-G4A-INTEGRITY` |
| `QG-G4-VERIFIED-COVERAGE` | `pre-action`, `transition` | `QGP-G4V-GRAPH`, `QGP-G4V-INTEGRITY` |
| `QG-G5-RELEASE-PREPARATION` | `pre-action`, `transition` | `QGP-G5P-GRAPH`, `QGP-G5P-INTEGRITY`, `QGP-G5P-RELEASE-UNIT` |
| `QG-G5-RELEASE-DECISION` | `pre-action`, `transition` | `QGP-G5D-STATUS`, `QGP-G5D-GRAPH`, `QGP-G5D-INTEGRITY` |
| `QG-G5-EXTERNAL-ACTION` | `pre-action` | `QGP-G5E-STATUS`, `QGP-G5E-GRAPH`, `QGP-G5E-INTEGRITY` |

The predicate names say what they read:

- `*-STATUS`: the artifact is in the state the rule expects;
- `*-GRAPH`: the formal artifact graph validates with no error;
- `*-INTEGRITY`: the installed managed files match the lock (`doctor`);
- `*-SCOPE`: the work order declares a non-empty `[execution_scope].paths`;
- `*-PREFLIGHT`: the start or review preflight of the work order is clean;
- `*-AUTHORING`: the definition meets the authoring policy;
- `G4I-COMPLETE`, `G4I-PATHS`: the change set is complete and inside scope;
- `G4I-EVIDENCE`: an evidence packet for this work order and checkpoint is
  bound to the current formal snapshot, a digest over every formal
  artifact's line-ending-canonical bytes, so a packet bound on a CRLF
  checkout matches the LF runner;
- `G5P-RELEASE-UNIT`: the release unit's census resolves.

For `--checkpoint transition --target STATE`, the predicates come from the
transition binding for the artifact family and target state instead of from
the rule, with the structural checks (`QGS-EDGE` for the edge's legality,
`QGS-ASSURANCE`, `QGS-VREC-COVERAGE`, `QGS-RLS-COVERAGE`, `QGS-SUCCESSOR`,
`QGS-VERIFIED-INCLUSION` where the target needs them) under the synthetic
`QG-STRUCTURAL` gate. `transition --apply` evaluates exactly the same set and
refuses if any is not `pass`.

## Supplying the change set

The handoff and scope checkpoints judge an implementation by the paths it
changed. Three forms are accepted, and they are mutually exclusive:

| Form | Meaning | Completeness |
| --- | --- | --- |
| `--from-git BASE` | the union of `git diff --name-only BASE` against the working tree (renames contribute both names) and the untracked files Git does not ignore | complete by construction; the result records `change_set_source = "git"` |
| `--changed-path PATH` (repeatable) with `--changes-complete` | typed, normalized repository-relative paths | complete only when asserted; the assertion is evidence, not proof |
| `--change-manifest PATH` | an in-repository `se-harness-change-set-v1` JSON file with `schema`, `complete`, and `paths` | as declared in the file |

Without a completeness assertion the scope predicates are `not_assessable`,
which blocks the check. `QGP-G4I-PATHS` passes when every changed path is
inside the work order's declared scope; the work order's own artifact file,
its evidence directory, and the verification and release records that name it
(`verifies_work_order`, `releases_work`) with their `evaluator_evidence_path`
files are admitted by construction, each record as an exact path, so a scope
need not list a records directory. Paths are checked as
untrusted text: they must be relative, normalized, without `.` or `..`
components, without reserved components, and without backslashes.

`--pull-request-body PATH` lets the check read a stored pull-request body and
report its `Harness-Work-Order` and `Harness-Restitution` lines, including a
carriage-return trailer that the selector would refuse.

## Outcomes and what `Blocked by` names

The result has exactly two outcomes.

- **Completed.** Every gate passed and no repository-level error was
  present. The block names the decision now due (`Decision required`), the
  decision right, the permitted outcomes, and one `Command or response` — for
  a handoff, `Mark WO-... implemented`. With `--from-git`, the result is
  retained as `handoff.json` beside the evidence packet, and its
  `result_sha256` is the value a pull-request body declares as
  `Harness-Restitution`.
- **Blocked.** At least one predicate did not pass, or a scoped error
  exists. `Blocked by` lists each refusing predicate by its own identifier
  with its message (for example `QGP-G4I-EVIDENCE: No readable evidence for
  WO-..., checkpoint handoff, and formal snapshot ... is available.`), or a
  `WEX` code when the check could not be evaluated at all. `Current lifecycle
  state` says that nothing changed, and `Next` names the retry.

`result_sha256` covers the change set and every predicate's status, so the
same tree evaluated twice yields the same digest, and any changed path or
predicate changes it.

## Refusal codes

These are refusals of the command itself, before or instead of predicate
evaluation. Each names its cause.

| Code | Cause |
| --- | --- |
| `WEX210` | the checkpoint is not one of the five; a checkpoint-specific option (`--target`, `--procedure`, `--changed-path`, `--changes-complete`, `--change-manifest`, `--from-git`, `--pull-request-body`) given without `--checkpoint`; `--target` given without `transition`, or `transition` without `--target`; the artifact is not a WO, VREC, or RLS, or is unknown; `scope` on a VREC or RLS; the rule's gate does not apply at this checkpoint; repository integrity fails; the installed machine policy is invalid |
| `WEX220` | `pre-action` without `--procedure`; a `--procedure` that the selected rule neither selects nor declares as an alternative; a procedure with no steps |
| `WEX200` | a changed path, manifest, or pull-request body that is not safe text: absolute, empty, non-normalized, escaping the repository, reserved or dot components, duplicates, an oversized or malformed manifest or body; a work order whose execution scope is empty or invalid |
| `WEX-ECP-002` | `--from-git` combined with `--changed-path`, `--changes-complete`, or `--change-manifest` |
| `WEX-ECP-003` | `--from-git` outside a Git checkout, with a base Git cannot resolve, or after any Git failure; no predicate is evaluated as `pass` |
| `WEX-ECP-010` | the evidence packet path cannot be derived or the packet is malformed: the work order is not under a domain directory, the header at byte offset 0 is missing, unclosed, not TOML, or carries the wrong keys, or names another artifact or checkpoint |
| `WEX-ECP-014` | `--artifact` names an unknown identifier |

Before se-harness 0.10.0, `WEX-ECP-010: ... is not under a domain directory`
was also raised on Windows for every work order, because the evaluator's own
path reached the resolver in native form (issue #254); a Linux runtime over the
same checkout did not raise it.

## One work order, from approved to implemented

1. The work order is `approved`. `harnessctl next . --artifact WO-X` selects
   it and names `PROC-WO-START`.
2. `harnessctl check . --artifact WO-X --checkpoint start` evaluates
   `QG-G3-WORK-AUTHORIZATION`. Completed: the decision `DR-WO-START` is due.
3. The accountable person decides; `harnessctl transition . --set
   WO-X=in_progress --decision WO-X=engineering-owner --apply` applies it
   after evaluating the same predicates as `check --checkpoint transition
   --target in_progress`.
4. Implementation happens inside the declared scope.
5. `harnessctl evidence . --artifact WO-X --checkpoint handoff` writes the
   packet header bound to the current formal snapshot; the body is written by
   the implementer.
6. `harnessctl check . --artifact WO-X --checkpoint handoff --from-git
   main` evaluates `QG-G4-IMPLEMENTATION-EVIDENCE` over the Git-derived change
   set. Completed: `DR-WO-COMPLETE` is due; `handoff.json` is retained;
   `harnessctl pr-body` emits the body carrying its `result_sha256`.
7. The accountable person decides; `transition --set WO-X=implemented
   --apply`. From here the rule for the work order changes
   (`WFL-WO-PREPARE-VREC`), and the handoff checkpoint no longer applies to
   it: the next checks are `pre-action` checks of the verification
   procedures, on the verification record. The pull request's managed gate
   keeps running `check --checkpoint scope --from-git` on every push, so
   the completion commit, the verification record and its verification are
   still held to the declared scope; only the digest comparison stops.

If any step is Blocked, the block names the predicate or code, states that
no lifecycle state changed, and gives the one retry; the fix is made in the
tree, never in the result.
