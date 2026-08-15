+++
id = "SPEC-IAR-006"
type = "specification"
title = "Authoritative artifact applicability and consistency contract"
status = "implemented"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
specifies = ["REQ-IAR-014"]
+++

# Specification: Authoritative artifact applicability and consistency contract

## Scope

Add one authoritative artifact-applicability catalog to the focused traceability policy, route coding agents to it, cross-reference it from progressive human documentation, and align validator and preflight behavior with its conditional architecture rule. This contract changes guidance and one inconsistent work-order relation cardinality; it does not add an artifact type or change accountable lifecycle authority.

## Authority placement

`docs/engineering/TRACEABILITY.md` owns the normative catalog because artifact purposes, applicability, reuse, and relations are traceability policy. `ENGINEERING_HARNESS.md` routes artifact-definition and applicability questions directly to that policy. The canonical installed template and self-hosted managed copy remain equivalent.

Human notes may summarize concepts in simpler language and link to the catalog. `docs/engineering/templates/README.md` continues to own canonical authoring locations and mechanics. Individual templates continue to describe type-specific fields and content. Neither notes nor templates may establish a conflicting applicability rule.

## Catalog schema

The catalog covers exactly the canonical standard artifact types exposed by `ARTIFACT_DIRECTORIES`:

```text
intent, capability, requirement, specification, architecture, adr,
verification, work_order, verification_record, release_contract,
release_record, operating_contract
```

For each type, the catalog states:

1. stable type name and ID prefix;
2. plain objective;
3. the condition under which active coverage or an instance is required;
4. when omission is valid and when an active existing artifact may be reused;
5. the principal accountable owner from `DECISION_RIGHTS.md`;
6. primary typed relations and their direction;
7. lifecycle-phase context by reference to `WORKFLOW.md`, without copying lifecycle procedure.

A nearby non-formal-material section distinguishes evidence, acceptance scenarios, source, candidate commits, dashboards, tickets, and conversations from formal artifacts.

## Required applicability semantics

| Type | Required semantic boundary |
| --- | --- |
| `intent` | Establishes approved purpose and accountable outcome; new work may reuse an active intent only when that purpose still covers it. |
| `capability` | Expresses an actor-visible ability derived from intent; reuse is valid when the same ability is being extended rather than invented. |
| `requirement` | States one observable normative obligation; create or change it when the obligation changes. |
| `specification` | Provides exact behavior or interface coverage for active requirements selected by implementation work. |
| `architecture` | Applies only when an active architecture directly `addresses` a selected architecturally significant requirement; routine requirements do not require fabricated architecture. |
| `adr` | Applies only when selected architecture declares `adr_required`; accepted `no_significant_decision` permits omission. |
| `verification` | Defines independent checks for active requirements and is selected by implementation work. |
| `work_order` | Is required before bounded implementation or governance execution; completed scope cannot silently authorize later work. |
| `verification_record` | Is created after a clean candidate when commit-bound assurance is proposed; verified or released claims require an eligible record. |
| `release_contract` | Defines gates for a proposed release and is required by a release record, not by ordinary unreleased delivery. |
| `release_record` | Exists only for a proposed release decision and binds eligible verification coverage to one exact candidate commit. |
| `operating_contract` | Applies when repository or service policy declares continuing operational obligations; absence must not imply an operational assurance claim. |

The final catalog may improve wording and layout but cannot weaken these boundaries.

## Work-order architecture correction

The formal validator must stop treating `work_order.architecture` as universally non-empty. A work order may omit that relation when no active architecture has an `addresses` intersection with its implemented requirements. If an applicable architecture exists, the work order must select all such architecture and every required deciding ADR. A present empty relation remains invalid; truthful omission uses no key.

Preflight text and JSON must preserve the distinction between:

- no applicable architecture, which passes;
- omitted applicable architecture, which fails;
- selected irrelevant architecture, which fails;
- selected `adr_required` architecture without deciding ADR coverage, which fails.

The canonical work-order template and its guidance must allow relation omission only under this rule. Existing completed work orders and historical commit-bound records are not rewritten.

## Registry and documentation consistency

A deterministic test derives the canonical type set from `scripts/artifact_layout_registry.py` and proves that the authoritative catalog contains every type exactly once and no unsupported type. The test also proves that:

- the router names the catalog owner for artifact purpose and applicability;
- human overview/model documentation links to the authoritative catalog;
- templates do not claim universal architecture coverage;
- root managed policy, standard template, packaged data, and schema-2 lock remain consistent.

The catalog is maintained manually under accountable review; the test checks structural coverage, not the semantic quality of prose.

## Upgrade behavior

Fresh `init` and `adopt` receive the revised managed policy and templates. `upgrade` plans the changes and applies only through the existing ownership and transactional rules. Customized managed content remains protected; no repository-owned formal artifact is migrated or synthesized.

## Security and authority boundaries

Catalog parsing in tests treats Markdown and type names as untrusted text and performs no execution. The catalog does not grant product approval, decide architectural significance, authorize work, assess evidence, transition a VREC or RLS, commit, push, release, or publish.

## Explicitly unchanged

Artifact IDs and prefixes; lifecycle values; relation direction outside the work-order architecture cardinality correction; VREC/RLS commit binding; supersession; release aggregation; self-hosting roles; branch policy; and repository decision rights remain unchanged.

## Delegated implementation choices

Heading names, Markdown table layout, parsing helper placement, stable diagnostic selection, and exact human-note cross-reference wording are delegated if the catalog remains complete, authoritative, readable, and machine-covered.
