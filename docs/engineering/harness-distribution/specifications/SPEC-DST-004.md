+++
id = "SPEC-DST-004"
type = "specification"
title = "Practical value example and semantic graph contract"
status = "implemented"
owners = ["technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-DST-014"]
+++

# Specification: Practical value example and semantic graph contract

## Scope

Define one compact root-README section that demonstrates SE Harness from a repository owner's perspective and connects that interaction to a representative governed engineering graph. The section explains outcomes and decision rights; it does not replace the detailed operating workflow, artifact model, Explorer questions, or command reference.

## Placement and structure

Add exactly one level-two section titled `What this looks like in practice` immediately after `Quick start` and before `What it provides`.

The section shall contain, in order:

1. a representative change request expressed by the user in natural language;
2. a short explanation of the agent preparing the governing chain and surfacing decisions before implementation;
3. explicit human approval followed by bounded agent implementation and evidence retention;
4. explicit human assurance review followed by preparation of the governance pull request;
5. a statement that routine harness commands are normally run by the coding agent while authority remains human;
6. a representative semantic graph;
7. a concise outcome statement selling the combined value.

## Representative interaction

Use the approved example of per-customer API rate limiting: preserve existing clients, return `429` with `Retry-After`, and prepare the material needed for review before implementation. The example is illustrative and must not create artifacts for an actual API product in this distribution repository.

The narrative shall accurately distinguish these stages:

- the agent translates the request into intent, requirements, design constraints, verification criteria, and a proposed bounded work order;
- the owner approves scope before implementation;
- the agent runs preflight, implements only approved work, runs repository checks, retains evidence, commits a clean candidate, and prepares a commit-bound verification record;
- the owner assesses evidence and authorizes the verification transition;
- pull-request CI checks the declared work order and governing chain;
- release remains a later, separate human decision.

Mention `doctor`, `preflight`, `validate`, `dashboard`, and verification capture as behind-the-scenes agent operations. Do not place those routine commands in the user's quoted requests or imply that the user must learn them to obtain value.

## Graph contract

Use an inline Mermaid `flowchart LR` with quoted labels and these semantic stages:

```text
approved outcome -> intent -> capability -> requirement
requirement -> specification + architecture + architecture decision + verification contract
design and verification -> approved work order -> agent implementation -> tests and evidence -> exact candidate commit
work order + verification + evidence + commit -> ready verification record -> human assurance decision -> verified record
verified record -> human release decision -> released revision
Harness Explorer -> traceability, scope, evidence, provenance, readiness, and anomalies
```

Architecture decisions, assurance decisions, and release decisions shall use diamond shapes. Other stages shall use labeled process nodes. Human decision nodes must remain visibly distinct from agent execution.

Define and apply Mermaid classes rather than external CSS. The semantic palette shall use high-contrast foregrounds and distinguish:

- human authority: blue;
- product intent and requirements: purple;
- specification and architecture: teal;
- authorized work: amber;
- agent execution and Explorer: slate;
- verification contracts and evidence: green;
- candidate and ready-record provenance: indigo;
- verified outcome: emerald;
- released revision: rose.

Labels, shapes, solid versus dotted relations, and surrounding prose shall convey the same distinctions without relying on color perception.

## README and package-index compatibility

The diagram shall be a standard fenced `mermaid` block with no inline script, remote stylesheet, generated image, or network-fetched prose. GitHub may render the diagram visually; other Markdown consumers may present the fenced source. The prose before and after the block must therefore communicate the complete value proposition independently, and the labeled source must remain readable as a compact flowchart.

Do not claim universal Mermaid rendering. Do not add a second README, PyPI-only variant, dynamic build step, or externally hosted mutable diagram as a required content dependency.

## Deterministic checks

Extend the existing standard-library public-onboarding tests to verify:

- the new section exists exactly once in the required position;
- the representative user prompts, human approval and assurance boundaries, agent responsibility, exact candidate provenance, Explorer value, and separate release decision are present;
- the five behind-the-scenes harness operations are named outside user command blocks;
- the Mermaid block declares the expected semantic stages, decision diamonds, class definitions, and node-to-class assignments;
- semantic labels remain present so color is not the only distinction;
- no external image, script, stylesheet, placeholder, or broken local link is introduced;
- the existing PyPI-first, version synchronization, metadata, upgrade, governance, and source-development tests continue to pass.

The tests inspect static text and do not execute README commands, fetch Mermaid, build a release distribution, or claim to prove package-index visual rendering.

## Explicitly unspecified decisions

Implementation may tighten prose and line wrapping and may adjust exact high-contrast color values, provided the approved scenario, semantic grouping, renderer fallback, authority boundaries, ordering, and deterministic checks remain satisfied.
