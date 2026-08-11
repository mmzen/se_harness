+++
id = "VER-DST-004"
type = "verification"
title = "Verify the practical value example and semantic graph"
status = "approved"
owners = ["quality-owner", "documentation-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-DST-014"]
+++

# Verification Contract: Verify the practical value example and semantic graph

## Independence

Verification derives assertions from `REQ-DST-014` and inspects the README as static UTF-8 Markdown. It does not execute example commands, load a Mermaid runtime, access an external renderer, create API artifacts, or treat the illustrative graph as formal authority.

## Requirement-to-evidence matrix

| Requirement behavior | Method | Pass condition |
| --- | --- | --- |
| User-perspective example is prominent and concise | ordered heading and text inspection plus manual review | exactly one section follows `Quick start` and precedes `What it provides` |
| Agent operates routine harness mechanics | deterministic phrase and context inspection | the five named operations are attributed to the coding agent, not quoted as required user commands |
| Human authority remains explicit | text and graph inspection | scope approval, assurance, and release decisions remain human and distinct from implementation |
| End-to-end value is visible | graph-node, edge, and summary inspection | purpose, design, work, evidence, exact commit, verification, Explorer findings, and release separation are present |
| Styling remains semantic and accessible | Mermaid class, shape, label, and contrast review | classes are applied consistently, decisions use diamonds, and labels preserve meaning without color |
| Renderer fallback remains useful | source and prose review | required meaning remains complete outside the Mermaid rendering and has no external runtime dependency |

## Automated checks

- Extend `tests/test_public_onboarding.py` using only the standard library.
- Verify the new heading occurs once and its ordering is stable.
- Verify the representative request includes compatibility, `429`, `Retry-After`, and pre-implementation review.
- Verify owner approval, evidence assessment, exact candidate commit, verification transition, pull-request enforcement, and separate release authority are described truthfully.
- Verify `doctor`, `preflight`, `validate`, `dashboard`, and verification capture are attributed to the coding agent.
- Verify one fenced Mermaid flowchart contains the approved semantic nodes, required edges, dotted Explorer observations, three decision diamonds, named class definitions, and node-to-class assignments.
- Reject external scripts, stylesheets, required remote images, unresolved placeholders, mojibake, and broken repository-relative links.
- Run the existing focused public-onboarding tests and complete unit suite on Python 3.11 and the available local runtime.
- Run formal graph validation, CLI help, `harnessctl doctor`, start and review preflight as phase-appropriate, and deterministic dashboard generation.
- Confirm no package metadata, version, runtime source, installed template, lock, workflow, CI pin, historical record, release artifact, or external state changes.

## Manual assessments

- Read the section as a prospective user and confirm the practical value is understandable before the artifact reference material.
- Confirm the story does not make the owner operate routine `harnessctl` mechanics.
- Inspect the graph in a Mermaid-capable GitHub Markdown rendering when a pull request is later authorized.
- Read the prose and fenced source without rendering and confirm the same authority and provenance story remains understandable.
- Confirm fixed colors have high-contrast text and that labels, shapes, and line styles provide non-color cues.

## Pass criteria

All locally authorized checks pass; the formal graph has zero diagnostics; the new section is short, ordered, truthful, accessible through redundant cues, and renderer-tolerant; existing public-onboarding contracts remain satisfied; and no prohibited surface changes.

## Evidence retention

Retain exact commands, runtime versions, focused and full test counts, README ordering and semantic assertions, Mermaid source review, graph and doctor results, deterministic dashboard snapshots, changed and protected paths, deviations, renderer residual risk, and deferred release inspection under `WO-DOC-005`.

## Residual uncertainty

Static checks do not prove every Markdown consumer's visual output. GitHub rendering can be observed during later pull-request review, while package-index rendering remains a release-time observation and must not be claimed by this documentation implementation.
