+++
id = "VER-PLG-028"
type = "verification"
title = "Qualify plugin 0.2.2 before marketplace publication"
status = "approved"
owners = ["mmzen"]
created = "2026-09-29"
updated = "2026-09-29"

[relations]
verifies = ["REQ-PLG-002", "REQ-RLO-018"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T17:31:39Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the reviewed seven-artifact 0.20.0/0.2.2 release package, required commit-bound verification, stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and existing 0.19.0 role encoding. Reviewed SHA-256 3d3a6dc9fb7afbeec88795a7a5078c28736d6f61fc44a281393694bcf8e365cf; approval input SHA-256 3d3a6dc9fb7afbeec88795a7a5078c28736d6f61fc44a281393694bcf8e365cf. Only the confirmed assurance classification was added to work orders. Legacy label engineering-owner transports the human decision; Codex applies it. Exact candidate verification, RLS release, merge, publication, markers and adoption remain separate."
+++

# Qualify plugin 0.2.2 before marketplace publication

## Independence

Expected versions come from the approved REL-SEH-031 and committed host manifests.
Expected wheel bytes come from its released RLS distribution binding, compared
with an independent public download. Source and release revisions are separate
named inputs. Expected content inventories come from the reviewed assembly,
never from whatever the public branch happens to contain.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-002 | test, inspection, demonstration | Both assemblies, builder check, source manifests, inventories and disposable Windows CLI installation | Both packages are 0.2.2 and carry the unchanged public 0.20.0 wheel; shared assets agree, required hooks exist and installed identities match. |
| REQ-RLO-018 | inspection | Reviewed delivery plan and publication handoff | Exact package and source identities are retained. WO-PLG-031 owns public-route observations and documentation; pending work remains visible. |

## Checks

After evaluator publication, assemble from one committed source revision and its
independently downloaded public wheel. Run the existing builder's build and
check modes plus relevant package tests. Compare wheel SHA-256, payload identity,
plugin version, inventories, archives and both host catalogs. Qualify both actual
package outputs in disposable Windows CLI profiles; record host versions and
startup, manual compaction and resumed-session observations. Use the existing
hook/probe methods. Do not invent desktop or automatic compaction coverage.
Authentication failures remain gaps; do not replace missing native proof with
synthetic protocol tests.

A negative wheel-digest case must refuse assembly. A package with the expected
version but mismatched inventory must fail the existing builder check. Reuse
applicable existing negative tests, retaining exact input identities.

Prepare a clean qualification candidate and a VREC covering WO-PLG-030. Present
its evidence for human acceptance before requesting publication of the exact
prepared distribution commit. Public fresh/update observations remain pending
under VER-PLG-029; they are not claimed by this pre-publication record.

## Evidence retention

Use evidence/WO-PLG-030/ in this domain. Retain command arrays, source/release
revisions, package identities, installed-content algorithm and inventories,
host versions, results, observation times and failures. Keep prior evidence
immutable and identify each reused observation and its applicability. Do not
commit profiles, credentials, environments or disposable repository trees.

## Limits

This establishes local qualification of the exact public-wheel-based package.
It does not establish public marketplace availability or adopt real user profiles.
Publication permission and remote success cannot be guaranteed in advance.
