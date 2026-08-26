# Definition lifecycle: declared exemptions, not lifecycle status

A definition's lifecycle status says who decided what about it. It does not say
what was built, and it is not evidence that a contract was satisfied. Where a
mechanism reads a status as a stand-in for an unrelated fact, the status becomes
load-bearing for something nobody decided, and the mechanism silently changes
meaning whenever an artifact is transitioned.

The `definition-lifecycle` domain removes those readings one at a time. This
note describes the first one, which has landed, and names the two that have not.

## What the architecture-generation proxy was

Every architecture must declare `decision_assessment.outcome`, either
`adr_required` or `no_significant_decision` with an accepted rationale. The rule
is `TRC-007`, and a missing table is a governance error.

Fourteen architectures in this repository predate that contract. Rather than
declare them, the validator carried a set of lifecycle statuses and skipped the
check for any architecture whose status was one of them. An architecture was
exempt because it had reached `implemented`, `verified`, or `released`.

That has three consequences worth stating plainly. Reaching a completed status
granted an exemption nobody asked for, so a *new* architecture could satisfy
`TRC-007` by being transitioned rather than by being assessed. The exemption was
invisible: no artifact recorded which architectures relied on it, or why. And
transitioning an architecture backwards would have withdrawn the exemption and
converted a warning into an error, with no change to the architecture itself.

## What replaced it

An exemption is now declared. Resolution reads governed artifact content only,
and the architecture's own status is not an input to it.

Two sources exist. The first is a frozen closed set of the fourteen
self-hosting identifiers, held in `se_harness/definition_generation.py` and in
the managed validator script. It is closed: no identifier is ever added to it.
The second is an optional `[definition_generation]` table in an **approved** work
order:

```toml
[definition_generation]
schema = "se-harness-definition-generation-v1"
scope = "architecture-decision-assessment"
legacy_architectures_without_decision_assessment = ["ARCH-XXX-001"]
```

The shape, the 512-entry bound, and the approved-declarer precondition follow
`SPEC-LRE-001` and `se_harness/legacy_release_evidence.py` deliberately, so that
a reader who knows the legacy-release-evidence surface already knows this one.
It is the same mechanism applied to a second question, not a second mechanism.

A declaration is fail-closed. A malformed table, a wrong schema or scope string,
a non-array value, an over-bound array, an invalid identifier, an unknown or
ambiguous target, a target of the wrong type, a target that already carries an
assessment, or a declaration in a work order that is not approved: each of these
resolves *nothing* and is reported as `E012` against the declaring work order. A
defect never grants an exemption by accident, and it never widens one.

## The exemption is maintenance, not a resolution

An exempt architecture still raises `W014` on every run, and the message names
the source of the exemption and states that the assessment remains outstanding.
There is no flag, field, environment value, or declaration key that turns it off.
Exemption suppresses the error; it never suppresses the warning.

The remedy for a `W014` is to record the assessment and delete the declaration
entry. Extending the declaration is not the remedy, and a new architecture is
never declared: it carries a real assessment from the start.

## Upgrading a consumer repository

This is a breaking change for a repository that relies on the old proxy, and the
governance-migration contract cannot express it — its capability vocabulary is a
closed set that the predecessor already holds in full, so the version pair
classifies compatible. The migration path is forward-compatible instead, which
is what actually protects a target repository:

1. **Before upgrading**, add a `[definition_generation]` declaration to an
   approved work order naming each architecture that has no
   `decision_assessment`. The table is additive: an older evaluator ignores it
   and the repository keeps validating exactly as before.
2. **Then upgrade.** The declaration is already in place, so the architectures
   resolve as exempt and the verdict is unchanged.
3. **Then work the warnings down.** Each `W014` names an architecture whose
   assessment is still owed.

Upgrading first and declaring second also works, but the repository does not
validate in between: each undeclared unassessed architecture reports `E014`
until its declaration lands.

## What has not landed

Two further readings remain, each under its own work order and its own merge
base:

- `implemented` is still a reachable state for a definition, and 165 records
  carry it. Retiring the edge and deriving a realization signal from work orders
  and verification records instead is `WO-DLC-002`. Until it lands, a reader
  encountering one of those 165 will still read it as "built".
- A definition may still hold a status past `draft` with no `lifecycle_events`
  chain recording how it got there. Closing that permission, with a declared
  pre-contract set for the existing 449, is `WO-DLC-003`.

Neither is anticipated by the mechanism above. Each is a separate decision.
