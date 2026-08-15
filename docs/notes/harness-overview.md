# SE Harness: a Tier-0 overview

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is a non-authoritative explanation. Formal authority comes from `ENGINEERING_HARNESS.md`, its managed policies, and approved artifacts under `docs/engineering/`.

## What it is

SE Harness is a repository-native governance system for software changes. It gives humans and coding agents a shared, inspectable answer to five questions:

1. Why does this work exist?
2. What must the software do?
3. What work was actually authorized?
4. What evidence supports the result, and for which exact commit?
5. Who decided that the result was verified or released?

It is installed into a new or existing repository. Its Markdown artifacts, policies, checks, and dashboard then travel with the code instead of depending on a separate service.

## The problem it solves

Code, tickets, chat messages, test results, and review comments often tell only part of a change's story. They may not show whether the final implementation still matches the original purpose, whether scope expanded without approval, or whether a later release contains the exact revision that was reviewed.

SE Harness keeps that lineage explicit:

```text
approved purpose -> defined behavior -> bounded authorized work
                 -> implementation + retained evidence
                 -> exact candidate commit -> human verification
                 -> separate human release decision
```

This does not guarantee that a decision is wise. It makes the claim attributable, structured, and reviewable.

## Main concepts

| Concept | Plain-language meaning |
| --- | --- |
| Intent and capability | Why the change matters and what an actor should be able to do. |
| Requirement | One observable obligation the system **SHALL** satisfy. |
| Specification | The detailed behavior or interface that satisfies requirements. |
| Architecture and ADR | Structural constraints and, only when significant choices exist, the recorded decision and rationale. |
| Verification contract | How the requirements must be checked independently. |
| Work order | A bounded permission to implement selected requirements and engineering material. |
| Evidence | Retained results from tests, analysis, review, or other checks. Evidence supports a claim but does not approve it. |
| Candidate commit | The exact clean Git revision containing the completed implementation, honest work-order state, and evidence. |
| Verification record | A record that binds the selected work, verification contract, evidence, and candidate commit. A human assurance owner decides whether it becomes `verified`. |
| Release record | A separate release-owner decision tied to the same candidate commit. |

The [simplified UML model](harness-uml-model.md) shows the relationships at a glance.
The authoritative [artifact applicability catalog](../engineering/TRACEABILITY.md#artifact-applicability-catalog) defines every standard formal type, its objective, when it applies, when it may be omitted or reused, its accountable owner, and its primary relations.

## How it fits into a change

Before implementation, people approve the problem, expected behavior, significant architecture decisions, verification approach, and bounded work order. A coding agent normally runs preflight, reads the returned manifest, implements within scope, performs repository checks, retains evidence, and helps prepare review material.

After the completed work is committed as candidate **C**, automation may prepare a `ready` verification record pointing back to C. An accountable human reviews the evidence and may transition it to `verified`. Release preparation happens later and also points to C; a separate human decides whether it becomes `released`.

The [operational phasing guide](harness-operational-phasing.md) explains why those records live in later governance commits.

## What SE Harness governs

- the types and relationships of formal artifacts;
- lifecycle rules for authorized work, verification, and release records;
- traceability to retained evidence and exact commits;
- managed instruction routing for coding agents;
- deterministic validation, preflight, integrity checks, and Explorer generation;
- boundaries that prevent automation from claiming human authority.

## What remains under human or repository control

- product purpose, priorities, acceptance, and risk decisions;
- whether an architectural choice is significant and, after assessment, whether an ADR is required;
- semantic review of code and evidence;
- verification and release decisions;
- programming language, build commands, test strategy, branch model, merge policy, and deployment process;
- GitHub protection, required checks, permissions, and other host settings;
- repository-owned additions to `AGENTS.md` and `REPOSITORY_CONTEXT.md`.

The harness can enforce supported repository policy when configured, but it does not silently invent that policy or claim control over external services.

## What the tools can and cannot do

`harnessctl preflight`, `validate`, `doctor`, and `dashboard` produce observations or enforce configured checks. `capture-verification` and `prepare-release` may prepare records in `ready` state. None of these commands approves work, changes a record to `verified` or `released`, commits, pushes, tags, publishes, or deploys.

Green tests are evidence. A generated dashboard is a derived view. Human decisions remain separate.

## Continue learning

- Read the [simplified UML model](harness-uml-model.md) for entity relationships.
- Read [operational phasing](harness-operational-phasing.md) for timing and decision points.
- Read the [illustrative branching model](harness-branching-model.md) for one possible Git mapping.
- Read the [practical example](harness-lineage-example.md) for an end-to-end interaction and commands.
- Before doing real work, follow the authoritative route from [`ENGINEERING_HARNESS.md`](../../ENGINEERING_HARNESS.md).
