+++
id = "REQ-DST-076"
type = "requirement"
title = "Describe the retired architecture relation as refused in the managed traceability policy"
status = "approved"
owners = ["product-owner", "technical-owner"]
created = "2026-09-10"
updated = "2026-09-10"
statement = "THE MANAGED TRACEABILITY POLICY SHALL describe the retired architecture relation as refused by the validator and name the typed pair as its only replacement."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #433 finding 1; SPEC-AUT-004 AUT-WIN-018 (WO-AUT-006, PR #431) owes the TRC-008 sentence to the next managed-template work order; measured on main at f0a3a223: templates/repository/standard/docs/engineering/TRACEABILITY.md lines 121 to 124 still call ARCH.constrains compatibility-only while validation_architecture.py refuses every constrains relation with E016"
measure = "the template's TRC-008 names the relation retired and refused with E016, names addresses and conforms_to as the only form, and promises no classification or migration report; the root copy follows at the root adoption of the carrying release"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T10:18:43Z"
decided_by = "product-owner"
reason = "Approved on 2026-09-10 by the accountable owner by selecting the presented option 'Approve both packets (Recommended)', given after the two issue #433 packets (the wave 5 leftovers: TRC-008 still describing the retired constrains relation, the completion boilerplate contradicting the delegation class, and the two ci-pipeline definitions naming the old job) were presented with the released 0.17.0 evaluator reading 0 errors and 0 advisories. Approval of a definition authorizes no work. The managed-template packet: TRC-008 for the retired relation, the completion decider in the work-order template."
+++

# Requirement: Describe the retired architecture relation as refused in the managed traceability policy

## In plain words

The policy every governed repository receives still says the validator
tolerates an old architecture relation and helps migrate it. The validator
now refuses it.

## Why

Since the compatibility windows closed, the validator reports every
`constrains` relation as an error, whatever the architecture's status, and
classifies nothing. Rule `TRC-008` of the managed traceability policy
promises the opposite, so a reader expects a grace the tool does not give.
The owner kept the template out of that work order and owed the sentence to
the next managed-template work order. This repository's root copy is
hash-locked and follows a release.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a reader consults the shipped policy's rule on the retired relation | the rule names the relation retired and refused, and the typed pair as the only form | a test names the stale phrase |
| the carrying release is adopted as a root | the root copy carries the same rule text | the parity test of the root adoption fails |

## Examples

### Normal

**Given** the candidate template,

**When** its rule on the retired relation is read,

**Then** it says the relation is retired, that a validator refuses it with
`E016`, and that the typed pair is the only form.

### Failure

**Given** a template that still says compatibility-only,

**When** the suite runs,

**Then** the template test fails naming the phrase.
