+++
id = "SPEC-DST-006"
type = "specification"
title = "Progressive and current SE Harness documentation contract"
status = "approved"
owners = ["technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
specifies = ["REQ-DST-019", "REQ-DST-020", "REQ-DST-021", "REQ-DST-022", "REQ-DST-023"]
+++

# Specification: Progressive and current SE Harness documentation contract

## Scope

Correct and organize the public README and explanatory notes so readers can progress from a 4/10 conceptual understanding to a 7/10 practical understanding of the current SE Harness without first reading source code. The work preserves authoritative policy ownership and does not change runtime, validation, Explorer, workflow, release, or publication behavior.

## Reader-expertise contract

Every in-scope document shall display this exact semantic label near its title or introductory notice:

```text
Target expertise: N/10
```

The surrounding introduction shall explain, directly or through the notes index, that the value describes expected reader knowledge rather than quality or complexity. Decimal values are allowed where explicitly required.

The required progression is:

| Document | Responsibility | Target expertise |
| --- | --- | --- |
| `README.md` | public value, installation, quick start, current reference, and links into deeper material | 6/10 |
| `docs/notes/README.md` | non-authoritative learning-path index and expertise-scale explanation | 4/10 |
| `docs/notes/harness-overview.md` | concise Tier-0 purpose, concepts, workflow fit, guarantees, and boundaries | 4/10 |
| `docs/notes/harness-uml-model.md` | simplified current conceptual entities, relations, cardinalities where useful, and authority distinctions | 6/10 |
| `docs/notes/harness-operational-phasing.md` | timing of drafting, approval, implementation, checks, commits, records, and release actions | 6/10 |
| `docs/notes/harness-branching-model.md` | one illustrative Git and release workflow, explicitly repository policy rather than harness law | 6.5/10 |
| `docs/notes/harness-lineage-example.md` | realistic current end-to-end examples and commands | 7/10 |

## Documentation responsibility boundaries

Each document owns one reader question:

- README: "Why should I use this, how do I install it, and where is the operational reference?"
- Overview: "What is SE Harness and what does it control?"
- UML model: "What are the concepts and how are they related?"
- Operational phasing: "When does each concept or action occur?"
- Branching model: "How could one repository map those phases onto Git?"
- Practical examples: "What does a complete real interaction look like?"

Documents shall cross-reference these responsibilities and avoid copying complete workflow, decision-rights, quality-gate, traceability, or command-reference sections into multiple notes.

## Sources of truth and inspection

Documentation facts shall be checked against:

- `pyproject.toml`, `se_harness/__init__.py`, and the public release records for version and packaging facts;
- `se_harness/cli.py`, installer, integrity, preflight, provenance, runtime-identity, and self-hosting modules for CLI behavior;
- current canonical templates and root operational copies for installed layout and managed ownership;
- `ENGINEERING_HARNESS.md` and its routed managed policies for authority, workflow, relations, and gates;
- `.self-hosting/governor.toml`, `docs/engineering/self-hosting-boundary/SELF_HOSTING.md`, and repository workflow source for implementation-repository assurance planes;
- tests for executable conformance, without treating tests as product or governance authority;
- retained release evidence and public services only for externally verified release facts.

When implementation, tests, formal policy, and existing prose disagree, the work shall state the discrepancy and its authority implications. It shall not invent intended behavior or modify product behavior solely to make prose uniform.

## Current conceptual model

New documentation shall use the current typed traceability model:

```text
INT -> CAP -> REQ <- SPEC.specifies
                  <- ARCH.addresses
            SPEC <- ARCH.conforms_to
            ARCH <- ADR.decides

REQ + SPEC + applicable ARCH/ADR + VER -> WO
WO + evidence + clean candidate commit C -> VREC
REL gates release-bearing WO
RLS includes eligible VREC and releases the same work at C
OPS assures requirements and/or release policy
```

Architecture coverage applies only to architecturally significant requirement drivers. Every new or ongoing architecture uses `addresses`, `conforms_to`, and a completed decision assessment. An `adr_required` assessment needs active deciding ADR coverage; `no_significant_decision` needs an accountable rationale and no active trigger. Legacy `constrains` relations are compatibility history, not the new authoring model.

Automated graph validation, preflight, doctor, Explorer, CI, and tests produce observations or enforce configured checks. They do not grant product approval, accountable verification, release authorization, publication authority, or repository-host configuration.

## README contract

Preserve the current top-level order unless a local move removes duplication or creates the required learning-path link. Keep PyPI-first installation, virtual-environment launcher guidance, quick start, practical value, feature inventory, agent-instruction architecture, operating workflow, artifact model, Explorer, provenance, command reference, safety, installed layout, upgrades, release integrity, CI/self-hosting, and distribution development discoverable.

Correct at minimum:

- architecture and ADR edge directions in prose and diagrams;
- the full governing chain selected by a work order;
- candidate, ready-record, verified-record, release-record, tag, GitHub Release, and PyPI boundaries;
- the current two-role consumer workflow versus the implementation repository's three assurance planes;
- current package version and public installation behavior;
- malformed Markdown introduced by the draft lineage edit;
- links to the progressive notes.

The README shall name authoritative G0-G5 definitions from `QUALITY_GATES.md`. It may describe Explorer's current per-work-order readiness view only as derived behavior. Because the current generator reuses G0-G5 identifiers with different titles and condition groupings, this work shall report that discrepancy explicitly and shall not claim it was resolved by documentation.

## Tier-0 overview contract

Rewrite the overview for SE Harness itself. Remove Mokiterions claims and consumer-specific repository facts. Use simple explanations of formal artifacts, bounded work, evidence, exact commit binding, derived checks, human decisions, repository-owned policy, and limits. Link deeper documents for cardinalities, phases, Git mapping, and commands.

## Simplified UML model contract

Replace the 0.2.1 `constrains` model with the current typed architecture relations and decision assessment. Show conceptual entities rather than Python implementation classes. Include commit binding as a value-object relationship, distinguish evidence from a formal artifact, and distinguish validation observations from VREC assurance. Include only cardinalities that materially prevent misunderstanding.

The note shall not state that the validator overrides managed policy. A policy/checker disagreement is a stop-and-report condition.

## Operational-phasing contract

Show at least these phases:

1. problem framing and product approval;
2. definition, architecture applicability, ADR decision, and verification-contract approval;
3. bounded work-order approval and start preflight;
4. agent implementation, repository checks, evidence retention, review preflight, and Explorer inspection;
5. clean candidate commit containing implementation, honest work-order state, and evidence;
6. later ready VREC preparation and accountable `verified` transition;
7. later ready RLS preparation and accountable release decision;
8. authorized tag/GitHub Release, separately governed PyPI or deployment action, and operating assurance.

Explain that a record cannot contain the hash of its own commit and that later governance commits point back to candidate C. Do not place an `implemented` lifecycle edit after the candidate it is claimed to be part of.

## Branching-model contract

Document one main-plus-short-lived-work-branch example:

- start a work branch from the repository's integration branch after work-order approval;
- declare exactly one standalone `Harness-Work-Order: WO-...` field in the pull request;
- retain the honest work-order lifecycle and evidence before selecting final candidate C;
- allow later governance commits or pull requests to retain VREC/RLS decisions while continuing to bind C;
- place an authorized immutable release tag on C, not automatically on a later governance commit.

Branch prefixes, release branches, merge strategy, default branch name, and protection configuration are illustrative repository policy. The guide shall explicitly state that SE Harness does not require this model and cannot claim to configure hosting controls it does not own.

## Practical-example contract

Rewrite the current lineage example so fictional and actual facts cannot be confused. Use current commands, repeatable options, and canonical paths. At least one example shall show:

```text
intent -> capability -> requirement -> specification
       -> applicable architecture/ADR + verification contract
       -> approved work order -> implementation + evidence
       -> clean candidate C -> ready VREC -> human verification
       -> ready RLS -> human release decision -> immutable tag at C
```

Show `harnessctl preflight`, repository checks, `harnessctl validate`, `harnessctl dashboard`, `harnessctl capture-verification`, and `harnessctl prepare-release` in their correct phases. Make clear which commands are normally agent-operated and which state transitions require humans.

## Repository-specific branching context

The owner-controlled branching section currently added to `docs/engineering/REPOSITORY_CONTEXT.md` is implementation draft, not approved policy. During implementation it shall either be aligned with the single illustrative model and labeled as current repository guidance, or removed in favor of the explicitly non-authoritative branching note. It must not contradict the branch used for the documentation work or claim an unenforced prefix set as a harness rule.

## Compatibility and migration

Do not rewrite completed formal artifacts, historical evidence, VRECs, RLS records, or compatibility-era architecture relations. Current documentation may explain that those historical files preserve the model valid at the time while new authoring follows 0.2.2 rules.

The 0.2.2 release and PyPI publication may be described only from verified public facts. Retaining new repository-native external-publication evidence requires separately authorized scope and must not be fabricated as part of explanatory cleanup.

## Verification and quality

Add or update focused standard-library tests for expertise labels, required note set, note index links, obsolete-repository markers, current typed relation terminology, public README structure, exact-version synchronization, current command forms, local links, and prohibited authority claims. Run formal validation, doctor, start and review preflight, the focused documentation tests, the complete unit suite, CLI help, deterministic dashboard generation, Markdown link inspection, and diff hygiene.

Manual review shall be performed at the declared reader levels and shall confirm progressive disclosure, diagram readability, terminology consistency, example ordering, repository-policy labeling, and absence of large duplicated policy sections.

## Explicitly unspecified decisions

Exact prose, diagram layout, Mermaid versus plain-text choice per note, number of examples beyond the minimum, and cross-reference wording are delegated to the implementation agent within this contract. Changing CLI behavior, validator rules, Explorer gate computation, CI behavior, templates, package version, release records, publication state, or repository-host protection is outside scope.
