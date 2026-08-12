+++
id = "VER-DST-006"
type = "verification"
title = "Verify progressive and current SE Harness documentation"
status = "approved"
owners = ["quality-owner", "documentation-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
verifies = ["REQ-DST-019", "REQ-DST-020", "REQ-DST-021", "REQ-DST-022", "REQ-DST-023"]
+++

# Verification Contract: Verify progressive and current SE Harness documentation

## Independence

Verification derives assertions from the approved requirements and `SPEC-DST-006`, then checks prose against independently inspected managed policy, CLI parsing, templates, tests, release metadata, and Git state. Existing wording and diagrams are inputs to challenge, not expected results. Manual review is performed from the declared reader perspectives and does not treat author confidence as evidence.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-019` | static document inventory and link traversal | expertise labels, notes index, ordered links | every in-scope document has the exact expected score and a reader can navigate 4/10 through 7/10 |
| `REQ-DST-020` | focused README tests plus manual comparison with current implementation and release metadata | section order, commands, paths, version, relations, authority wording | README preserves its useful structure and contains no known obsolete or false implementation claim |
| `REQ-DST-021` | model and phasing inspections plus terminology tests | overview, UML, timeline, current typed edges, decision assessment | notes are SE-Harness-specific, current, concise, and distinguish authority, observation, assurance, and release |
| `REQ-DST-022` | policy-boundary review and one-model assertion | branching guide, repository-context disposition | exactly one branching example is documented and it is never stated as a universal harness requirement |
| `REQ-DST-023` | end-to-end walkthrough and command verification | practical example, candidate/governance timeline, canonical paths | the example is internally ordered, uses current commands, labels fiction, and preserves human decision boundaries |

## Automated checks

- Assert `README.md` contains `Target expertise: 6/10` and retains exactly one required public section marker for installation, quick start, practical value, command reference, upgrades, release integrity, CI/self-hosting, and distribution development.
- Assert the required `docs/notes/` file set exists, each document has its specified expertise label, the notes index links to every guide, and all local Markdown links resolve.
- Reject Mokiterions-as-current-repository wording, `SE Harness 0.2.1` as the current model, current-authoring use of `ARCH.constrains`, "validator wins" authority inversion, and fictional identifiers presented as repository facts.
- Assert the current relation terms `addresses`, `conforms_to`, `decides`, `implements`, `specifications`, `architecture`, `verification`, `verifies_work_order`, `includes_verification`, and `releases_work` appear in the appropriate model or example documents.
- Compare documented CLI forms with `se_harness/cli.py` parser behavior and run CLI help for every referenced `harnessctl` command.
- Keep the exact-version README example synchronized with `pyproject.toml` and `se_harness.__version__`.
- Verify Markdown fences, Mermaid source, tables, ASCII fallback, and headings are structurally balanced and contain no mojibake or disallowed control characters.
- Run `tests/test_public_onboarding.py`, any new focused documentation test module, and the complete standard-library unit suite on Python 3.11 and the available local runtime when feasible.
- Run formal artifact validation with zero errors, `doctor`, start and review preflight for `WO-DOC-007`, deterministic dashboard generation, and `git diff --check`.
- Verify canonical managed templates and self-hosted operational copies are unchanged unless the approved work order is explicitly amended.

## Manual assessments

- **4/10 reader review**: confirm the overview explains the problem, core concepts, workflow fit, guarantees, and human boundaries without assuming artifact-schema knowledge.
- **6/10 reader review**: confirm the README, UML, and phasing guide agree on current concepts, relation direction, timing, commands, and exact commit binding.
- **6.5/10 reader review**: confirm the branching guide is practical but unmistakably illustrative and repository-configurable.
- **7/10 reader review**: execute a paper walkthrough of the practical example and confirm every artifact, path, command, state, commit, and accountable action occurs in a valid order.
- Inspect the README in source and a Mermaid-capable renderer; ensure required meaning remains available without rendered diagrams or color.
- Review repeated paragraphs and tables across all documents; replace substantial duplicate policy with cross-references.
- Confirm the authoritative G0-G5 versus current Explorer-readiness discrepancy is reported accurately and not silently resolved in prose.

## Acceptance scenarios

### Scenario: progressive reader path

Given a reader with no SE Harness implementation knowledge, when they start at the notes index and follow the ordered path, then each document declares its expected expertise and adds a distinct layer of understanding without requiring source inspection.

### Scenario: current typed model

Given the 0.2.2 managed traceability policy, when the reader inspects the UML and practical example, then architecture addresses significant requirements, conforms to specifications, records decision applicability, and is decided by ADRs only when required.

### Scenario: honest branching example

Given a repository chooses the documented work-branch model, when a reader maps an approved work order through PR, candidate, governance commits, and tag, then the example is coherent and the guide still states that another repository may choose a different model.

### Scenario: unresolved behavior discrepancy

Given managed `QUALITY_GATES.md` and the current Explorer generator reuse G0-G5 differently, when documentation is reviewed, then it identifies the difference and authority boundary without changing behavior or claiming alignment.

## Pass criteria

All automated checks pass; formal validation has zero errors; only classified pre-existing compatibility warnings remain; doctor and phase-appropriate preflight pass; the dashboard is generated successfully; every manual reader-level assessment passes; no obsolete consumer-repository fact remains; commands and relations match current implementation and managed policy; and the final diff contains only approved documentation, focused tests, formal packet lifecycle updates, and retained evidence.

## Evidence retention

Retain exact commands, Python and harness versions, inspected source and policy paths, test names and counts, link results, section and expertise inventory, terminology checks, model and timeline review, branching-policy review, example walkthrough, validator warnings, dashboard snapshot, changed/protected paths, discrepancies, deviations, and residual risks in `docs/engineering/harness-distribution/evidence/WO-DOC-007-verification.md`.

## Residual uncertainty

Reader expertise is partly qualitative and cannot be proven by static tests. GitHub and PyPI rendering differ, external release state can change, and current Explorer readiness semantics require a separate product decision. These limits must be reported rather than converted into implied conformance.
