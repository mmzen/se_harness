+++
id = "SPEC-DST-018"
type = "specification"
title = "Bounded documentation-state consistency correction"
status = "approved"
owners = ["technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
specifies = ["REQ-DST-060"]
+++

# Specification: Bounded documentation-state consistency correction

## Scope

Correct the four priority documentation groups identified by the 2026-08-19 audit: the obsolete README architecture limitation, incomplete engineering-domain index, stale self-hosting boundary summary, and stale evidence-keying, work-order-assurance, and release-orchestration status summaries. Update only the focused public-onboarding regression needed by the corrected README claim.

On 2026-08-19, the accountable owner approved this specification with the original identifier `SPEC-DST-017` together with `REQ-DST-060`, the verification contract then identified as `VER-DST-017`, and `WO-DOC-013`. After current `main` independently assigned both `017` identifiers to another packet, the owner approved renumbering this unchanged contract to `SPEC-DST-018` and its verification contract to `VER-DST-018`. Those decisions authorize only the bounded behavior described here and grant no verification transition, release, publication, deployment, or governor-promotion authority.

## Actors and external systems

- Public readers use the root README for current product behavior and limitations.
- Maintainers use repository-owned indexes for navigation and current explanatory context.
- Formal artifacts, configuration, validator behavior, and the governor descriptor supply factual inputs but remain independently authoritative.
- No external service is changed or required for this correction.

## Inputs

- Current validator relation requirements and canonical work-order authoring guidance.
- Existing engineering domain and release directories.
- `.self-hosting/governor.toml`.
- Verified VREC and released RLS metadata for the named work orders.
- The existing public-onboarding test contract.

## Outputs

- Corrected public and repository-owned explanatory Markdown.
- Focused regression assertions that reject the obsolete README claim while preserving the unresolved Explorer gate-label limitation.
- Work-order-keyed retained verification evidence after implementation.

## State model

Formal lifecycle and governor-selection state do not change. Documentation moves from a stale observation to an accurate description of already-authoritative state.

## Behavioral rules

1. Remove the README claim that every work order requires a non-empty `architecture` relation; retain the unresolved managed-policy versus Explorer G0-G5 grouping mismatch.
2. Change the focused public-onboarding test so it rejects the obsolete architecture-limitation text and continues to require honest unresolved limitations.
3. Add `dashboard-publication/`, `release-0.3.0/`, `release-0.4.0/`, and `release-0.4.1/` to the repository engineering index with factual bounded descriptions.
4. Describe `reconcile-governor` as implemented but authority-bounded, and state that the selected released governor is 0.3.0 under `RLS-SEH-005` while candidate 0.4.1 remains separate.
5. Update the evidence-keying summary to name verified `VREC-EVK-002` without implying release.
6. Update the work-order-assurance summary to record verified and released aggregate coverage through `VREC-SEH-006` and `RLS-SEH-006`.
7. Update the release-orchestration summary to record verified `VREC-RLO-002` and `VREC-RLO-003` without implying release or publication authority.
8. Preserve historical dates, decisions, record bytes, and the distinction between implementation, verification, release, publication, and governor promotion.

## Error and recovery behavior

Stop if a proposed statement cannot be tied to current repository evidence, if the selected governor changes during implementation, if formal lifecycle state differs from the reviewed inputs, or if a correction would require modifying a formal historical record. A failed check leaves the documentation work unimplemented and requires correction within the approved scope or escalation.

## Data and interface contracts

Use exact artifact IDs and versions already present in repository metadata. Keep Markdown links repository-relative. Do not add generated status data, a documentation build system, or a new public interface.

## Security and privacy properties

Do not copy secrets, environments, unbounded command output, or private external state into documentation or evidence. Treat repository prose and metadata as untrusted until checked against the formal graph and bounded sources.

## Performance and capacity

Focused checks remain bounded by the existing Markdown documents and test suite. No runtime or generated-dashboard performance behavior changes.

## Observability

Verification records exact changed paths, source facts, commands, outcomes, and the unchanged formal validation warning counts.

## Compatibility and migration

The correction changes no installed consumer template or managed file. Historical artifacts remain where they are. Existing local and PyPI/GitHub rendering remains compatible Markdown.

## Examples and counterexamples

**Intended:** “The selected released governor is 0.3.0; publication of candidate 0.4.1 does not promote it automatically.”

**Prohibited:** changing `.self-hosting/governor.toml` merely to make an explanatory page true.

**Intended:** reporting that `WO-RLO-003` has verified VREC coverage while explicitly withholding any release claim.

**Prohibited:** changing `WO-RLO-003` status or its VREC while editing its domain index.

## Explicitly unspecified decisions

The implementation agent may choose concise sentence structure and the ordering of the four new engineering-index entries within `SPEC-DST-018`. It may not broaden the correction into formal-artifact migration, warning remediation, link-checker expansion, compatibility-window policy, behavior changes, or release work.
