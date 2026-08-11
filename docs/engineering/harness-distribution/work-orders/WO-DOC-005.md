+++
id = "WO-DOC-005"
type = "work_order"
title = "Demonstrate harness value through a user story and semantic graph"
status = "implemented"
owners = ["engineering-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-014"]
specifications = ["SPEC-DST-004"]
architecture = ["ARCH-DST-004", "ADR-DST-004"]
verification = ["VER-DST-004"]
+++

# Work Order: Demonstrate harness value through a user story and semantic graph

## Lifecycle and authorization

The repository owner reviewed the proposed user-perspective README example and colored graph, then explicitly instructed `go for the artifact packet` on 2026-08-11. After reviewing the resulting `REQ-DST-014`, `SPEC-DST-004`, `ARCH-DST-004`, `ADR-DST-004`, `VER-DST-004`, and bounded work order, the owner explicitly instructed `go for implementation` on 2026-08-11. That accountable decision approves the governing chain and places `WO-DOC-005` in progress.

The approval authorizes only the implementation, tests, local verification, artifact lifecycle updates, and retained evidence described below. Commit, verification capture, push, pull request, build, release, tag, publication, deployment, merge, force push, and history rewriting remain separately controlled.

## Objective

Make the public README demonstrate, in one short user-centered example and one semantic graph, how SE Harness lets a coding agent operate the engineering mechanics while humans retain scope, assurance, and release decisions, with traceability to evidence and an exact candidate commit.

## In scope after approval

- Add exactly one `What this looks like in practice` section after `Quick start` and before `What it provides`.
- Use the approved per-customer API rate-limiting scenario and concise owner-agent interaction defined by `SPEC-DST-004`.
- Explain that the coding agent normally runs the routine harness operations while decision authority remains human.
- Add one inline semantically colored Mermaid graph with decision shapes, accessible labels, dotted Explorer observations, and renderer-independent prose.
- End the section with a concise value statement covering purpose, bounded scope, evidence, exact provenance, visible anomalies, and separately authorized release.
- Extend focused deterministic README tests and retain `WO-DOC-005` evidence after implementation.
- Make only minimal supporting acceptance-scenario and distribution index updates required by this packet and implementation lifecycle.

## Out of scope

- Changing CLI, validator, dashboard, installer, upgrade, provenance, workflow, publication, or release behavior.
- Changing `pyproject.toml`, package metadata, package version, runtime dependencies, entry points, Python support, canonical installed templates, lock data, managed ownership, GitHub workflow, action pins, or independent baseline pin.
- Creating a second README, external stylesheet, executable diagram script, generated image pipeline, or required mutable remote image.
- Creating actual API rate-limiting product artifacts or implying this repository implements the illustrative scenario.
- Modifying historical work orders, evidence, VRECs, RLS records, releases, tags, GitHub releases, PyPI files, attestations, or external configuration.
- Building a wheel or source distribution, publishing, deploying, merging, force pushing, or rewriting history.

## Authorized decision envelope after approval

Implementation may tighten the proposed prose, line wrapping, and exact high-contrast color values. It may not change the representative scenario, section ordering, semantic stages, human authority boundaries, decision shapes, textual fallback, protected surfaces, or required verification without renewed accountable approval.

## Expected change surface

- `README.md`;
- `tests/test_public_onboarding.py`;
- `docs/engineering/harness-distribution/acceptance/pypi-onboarding.feature` if the approved scenario requires lifecycle clarification;
- `docs/engineering/harness-distribution/README.md` for packet indexing and lifecycle facts;
- this packet's artifacts as their lifecycle advances;
- `docs/engineering/harness-distribution/evidence/WO-DOC-005-verification.md` after implementation.

## Implementation sequence after approval

1. Transition the approved governing artifacts and this work order to phase-eligible statuses.
2. Run start preflight for `WO-DOC-005` and read the complete manifest.
3. Add deterministic failing tests for the approved README example and graph contract.
4. Add the concise narrative, Mermaid graph, and textual value statement without disturbing existing onboarding or deep-reference sections.
5. Run `VER-DST-004`, the existing public-onboarding checks, the complete regression suite, and harness diagnostics.
6. Inspect the diff and retain exact work-order-keyed evidence.
7. Stop for separate commit and verification-capture authority.

## Required verification

Perform every locally authorized check in `VER-DST-004`; retain the existing `VER-DST-003` focused checks; run the complete Python 3.11 and local-runtime suites, validator, doctor, CLI help, start/review preflight, and deterministic dashboard; manually inspect narrative accuracy, authority boundaries, Mermaid source, non-color cues, and renderer fallback; confirm no protected surface changed. Do not build a distribution under this work order.

## Evidence to record

Retain the authorization and scope, red-to-green focused-test result, exact commands and outputs, runtime versions, test counts and skips, README ordering and semantic assertions, graph source and accessibility review, graph and doctor results, dashboard snapshot hashes, changed and protected paths, deviations, renderer residual risk, and deferred package-index rendering in `docs/engineering/harness-distribution/evidence/WO-DOC-005-verification.md`.

## Stop and escalate conditions

Stop if implementation requires a new renderer dependency, external mutable content, a generated asset pipeline, package metadata or version change, template or lock mutation, workflow or baseline-pin change, build, release action, external publication, weakening of human authority, failed required check, or scope beyond this packet.

## Completion report format

Report the user-facing story and graph outcome, agent/human authority separation, focused and full verification results, renderer fallback assessment, changed and protected surfaces, deviations, residual risks, and exact evidence path. Do not describe the change as verified, released, published, or visually proven on PyPI without later accountable evidence.

## Implementation result

The root README now introduces one concise user-and-coding-agent scenario immediately after the quick start, explains that routine harness operations stay with the agent while accountable decisions remain human, and renders the representative engineering chain as a semantically colored Mermaid graph with labeled decision diamonds and dotted Explorer observations. Surrounding prose preserves the complete authority and provenance story when Mermaid is displayed as source. Two new focused tests capture the section, workflow, graph, styling, and fallback contract; both supported-runtime suites and all harness diagnostics pass. Exact results and residual rendering uncertainty are retained in `docs/engineering/harness-distribution/evidence/WO-DOC-005-verification.md`.
