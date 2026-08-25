+++
id = "INT-TCM-001"
type = "intent"
title = "Make agent communication clear without weakening precision or authority"
status = "approved"
owners = ["product-owner", "domain-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "product-owner"
+++

# Intent: Make agent communication clear without weakening precision or authority

## Problem

Supported coding agents explain harness state, ask for accountable decisions,
and draft human-readable engineering artifacts. Their prose can be longer,
less consistent, or more ambiguous than operators need. Different skills and
runtimes can also apply different writing conventions.

ASD-STE100 provides useful clarity principles for technical documentation, but
strict conformance is not the objective. It is not a universal conversation
protocol, and an agent must not download, reproduce, or claim to enforce the
standard. An uncontrolled simplification pass could also change a normative
obligation, technical term, command, identifier, or canonical harness result.

The product therefore needs one managed technical-communication policy that
improves eligible English prose while preserving formal authority and exact
technical content.

## Desired outcomes

- Operators receive concise explanations that identify the current fact, the
  required decision or action, the accountable role, and the relevant limit.
- New or materially revised technical prose uses consistent terms, direct
  sentence structure, explicit actors, and unambiguous conditions.
- Exact commands, evidence, identifiers, schemas, normative semantics, and
  canonical restitution blocks remain unchanged.
- Portable skills and ordinary supported agent routes consume one managed
  policy instead of copying writing rules into prompts or skill prose.
- Automation prepares clear communication and stops at the existing accountable
  decision point; it does not create a new review gate for routine prose.

## Actors and stakeholders

- Operators who must understand state and make bounded decisions.
- Accountable product, technical, engineering, assurance, repository, release,
  and service owners whose decision meanings must remain precise.
- Requirements stewards, technical authors, implementers, and reviewers.
- Runtime and skill maintainers who distribute provider-neutral behavior.
- Readers who use English as a second language.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Protected exact-content changes in the acceptance corpus | Not measured | 0 | Every conformance run |
| Critical meaning changes introduced by communication rendering | Not measured | 0 | Every reviewed corpus release |
| Tested operator briefs that identify the intended decision or action | Not measured | 100% | Every acceptance corpus run |
| Managed sources that own the communication rules | 0 | 1 | Every installation and upgrade test |
| Existing approved artifacts rewritten only for style | 0 | 0 | Every implementation review |
| Claims of ASD approval, certification, endorsement, or compliance | 0 | 0 | Every release review |

## Non-goals

- Certify or claim strict compliance with ASD-STE100.
- Download, bundle, reproduce, or parse the standard or controlled dictionary.
- Build a general grammar checker, controlled-English compiler, translation
  system, or proprietary terminology service.
- Change lifecycle legality, decision rights, gates, schemas, or normative force.
- Automatically rewrite the existing engineering artifact catalog.
- Correct operator-supplied language, quotations, logs, or evidence.
- Provide non-English controlled-language profiles in the first increment.
- Require a hosted service, network request, credential, or provider runtime.

## Principles and immutable constraints

- Harness authority and technical meaning take precedence over writing style.
- The product says ASD-STE100-based or follows selected ASD-STE100 principles;
  it does not say compliant.
- The runtime uses repository-managed policy and does not retrieve the standard.
- One managed policy owns the rules. Skills and adapters only consume them.
- Exact protected content is preserved byte for byte. Semantically protected
  content is not automatically paraphrased.
- Guidance applies only to agent-authored eligible English prose.
- Human attention is requested for meaning, terminology, accountable decisions,
  or declared exceptions—not every routine sentence.
- Existing integrity, evaluator, lifecycle, and external-action boundaries remain.

## Risks and assumptions

- **Risk:** shorter wording can omit a qualification. Verification must compare
  meaning, not readability scores alone.
- **Risk:** a broad trigger can overlap existing skills. The first skill is
  explicit-only and narrowly named.
- **Risk:** copied rules can drift. Checks must enforce one policy owner.
- **Risk:** protected-content classification can miss an exact token. Ambiguous
  source boundaries must fail closed.
- **Assumption:** supported agents can follow a concise managed policy without
  downloading the external standard.
- **Assumption:** project terminology can be absent; absence must not cause
  invented synonyms.
- **Open decision:** accountable owners must approve, revise, or reject the
  policy scope, profile strength, protected-content boundary, and skill outcome.
