+++
id = "REQ-DST-036"
type = "requirement"
title = "Navigate bounded context around filtered Explorer nodes"
status = "superseded"
owners = ["product-owner", "technical-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-09-01"
statement = "WHEN a reader filters the Explorer topology, THE SYSTEM SHALL offer bounded zero-, one-, and two-hop connected context around the matching artifacts while preserving filter meaning, relation direction and authority, deterministic limits, and an explicit distinction between matches and contextual nodes."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Navigate bounded context around filtered Explorer nodes

## Supersession

Superseded on 2026-09-01 by `REQ-DST-067` under `WO-DST-023`, authorized by the
repository owner's approval of the designed-Explorer packet. The zero-, one-, and two-hop filter context is replaced by the designed interactions: lenses that dim rather than remove on the Virtual Twin, and the lit spine of a selection on the Lineage board. The
sections below record what the shipped product did while this artifact was
active and are retained unchanged as history; they no longer bind the
candidate.

## Rationale

The current Overview filter removes every node that does not directly match the search, type, and lifecycle criteria. An exact search such as `SPEC-DST-007` therefore locates the artifact but hides the requirements, architecture, work, and verification connected to it. The reader loses the context that makes the graph useful.

An unrestricted traversal depth would be misleading and operationally unsafe: in a dense graph, a small number of hops can expose most of the repository. Context expansion must therefore be explicit, bounded, and observable.

## Required response

- Add a keyboard-operable `Context depth` control with exactly `0 — matches only`, `1 — direct neighbors`, and `2 — two hops`.
- Treat artifacts matching the current text, artifact-type, and lifecycle filters as root matches. Search continues to match canonical artifact ID and title without renaming types or states.
- At depth zero, preserve the current match-only behavior.
- At depth one or two, traverse resolved canonical relations in either direction for neighborhood membership while preserving the stored arrow direction, relation type, authority, and derived status in presentation.
- Expand from every root match. Context nodes may appear even when they do not satisfy the root type or lifecycle filter; the control must explain that filters select roots and depth adds context.
- Always retain every root match. Add at most 100 distinct context nodes in deterministic breadth-first order; when eligible context exceeds the budget, report that the view is truncated.
- Distinguish root matches from context nodes through more than color alone. Preserve selected-node emphasis as a separate state.
- Report match, context-node, visible-relation, depth, and truncation counts in readable text.
- Keep the analysis lens honest about whether it describes the complete visible graph, and clear stale selection when the selected artifact is no longer visible.
- Reset context depth to zero with the existing graph reset action.

## Graph semantics

A hop is one currently displayed resolved canonical relation, declared or derived. Traversal is undirected only for deciding which nodes belong to the neighborhood; rendered arrows and textual relation details remain authoritative about direction and authority. Unresolved targets cannot contribute a node but remain represented by existing metrics and relation details.

Multiple matches are all roots. Cycles, self-relations, duplicate paths, dense hubs, empty results, unknown future artifact types, and repositories larger than the context budget must terminate deterministically without dropping matches or mutating canonical data.

## Acceptance examples

### Exact specification search

**Given** `SPEC-DST-007` has resolved inbound and outbound relations

**When** the reader searches for that exact ID and selects context depth one

**Then** `SPEC-DST-007` remains visibly identified as the match and every direct neighbor within the context budget is shown as context with authoritative arrows.

### Two-hop context

**Given** artifact A is connected to B and B is connected to C

**When** A is the only match and context depth two is selected

**Then** A is a match, B and C are context nodes, and an unrelated D is absent.

### Type-filter context

**Given** the artifact-type filter selects specifications

**When** context depth one is selected

**Then** connected requirements or verification contracts may appear as contextual nodes even though they do not match the specification filter.

### Dense graph

**Given** the matching roots have more than 100 distinct reachable context nodes

**When** depth expansion runs

**Then** all roots remain visible, no more than 100 context nodes are added, and the UI explicitly reports truncation.

## Out of scope

This requirement does not add arbitrary traversal depth, graph mutation, a new relation, a second snapshot schema, server-side search, persisted UI state, a new runtime dependency, or a replacement for focused Lineage.
