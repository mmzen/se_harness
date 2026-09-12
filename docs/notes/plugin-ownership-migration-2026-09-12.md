# Evaluator skill ownership migration: proposed packet

Prepared 2026-09-12 against main `3bf0ef2a7a2b4008efaa3cb79431d526d3f6f600`.
All nine new formal artifacts remain draft. No implementation or prior-contract amendment has been applied.

## Why this work is next

[DEC-PLG-004](https://github.com/mmzen/se_harness/blob/17382d8e7f7a5709f4f55facfe875fbf455e5794/docs/engineering/plugin-integration/decisions/DEC-PLG-004.md) already selected supported evaluator migration.
Its accepted goal is automatic replacement of overlapping repository skills by plugin implementations, with ownership/integrity updates and unrelated skills preserved.
WO-PLG-009 supplies the later connection procedure and explicitly excludes building this missing evaluator capability.

The current installation contains two retained canonical skills and one Claude orientation adapter: seven managed files total.
The three old writing skills were retired by the earlier ECP work; they are not a new migration catalog.
Current installer planning and doctor both derive their managed set from the standard template.
Deleting the retained skills alone breaks integrity and allows an upgrade to recreate them.

## Proposed packet

| Artifact | Owner decision | Purpose |
| --- | --- | --- |
| REQ-PLG-028 | requirements-steward | Explicit ownership transfer |
| REQ-PLG-029 | requirements-steward | Durable ownership through integrity and upgrades |
| REQ-PLG-030 | requirements-steward | Safe recovery and restoration |
| REQ-PLG-031 | requirements-steward | Data-only external identity verification |
| SPEC-PLG-020 | technical-owner | Exact operation, boundaries, compatibility, and data contracts |
| ARCH-PLG-003 / ADR-PLG-003 | technical-owner | Explicit lock binding and shared transaction architecture |
| VER-PLG-020 | assurance-owner | Windows/Linux identity, failure, race, recovery, and regression criteria |
| WO-PLG-020 | engineering-owner | Bounded evaluator implementation scope |

## Design for review

1. Keep the single standard harness and ordinary repository ownership as the default.
2. Add an explicit plan/apply/restore operation for an independently selected plugin binding.
3. Represent plugin ownership with lock schema 4; keep schema 3 support for default ownership.
4. Share one effective-inventory resolver across installer, doctor, and applicable mutation checks.
5. Require complete input revalidation, exclusive application, durable interruption recovery, and exact-file retirement.
6. Keep portable provider identities in the lock; external machine paths remain local inputs.
7. Let credential-free CI validate repository ownership without falsely proving external plugin availability.

The schema and recovery design are proposed technical choices requiring approval. The already accepted supported-migration direction is not reopened.
Native host discovery is deliberately a later observed result under WO-PLG-009; package inventory checks cannot establish it.

## Exact proposed prior-contract amendments

These four append-only applicability amendments are part of the approval package. Their target files remain unchanged in this draft.
On approval, retain their existing statements, rules, lifecycle history, and historical observations, and append the corresponding text under `Amendment record`.
The new amendment must identify WO-PLG-020 and the actual approval date and accountable actor.

### REQ-AEX-009 — repository host discovery

> For an explicit plugin ownership selection conforming to SPEC-PLG-020, repository-local installation and canonical-location clauses apply to the unselected default repository route only. The selected retained skills are represented by the evaluator's plugin ownership binding instead. Invocation policy, evaluator authority, customization protection, and atomicity remain required. Native discovery must be observed separately under WO-PLG-009. This amendment does not restore retired writing skills or alter historical host observations.

### SPEC-AEX-005 — canonical locations and managed host surfaces

> For the retained catalog explicitly migrated under SPEC-PLG-020, its versioned provider binding governs storage location and managed inventory instead of repository-local location and host-surface clauses AEX-HST-001, AEX-HST-003, AEX-HST-007, AEX-HST-009, and AEX-HST-012. All unaffected contracts and default repository behavior remain in force. No provider binding grants lifecycle or external authority. Historical catalog, version, and verification facts are preserved; this amendment creates no new native host qualification claim.

### REQ-TCM-004 — retained operator briefing

> When SPEC-PLG-020 explicitly selects plugin ownership, the operator-brief skill may be loaded from the bound plugin package instead of its repository-managed location. Its exact retained core identity, explicit invocation requirement, bounded source, read-only effects, and evaluator checks remain unchanged. The default repository-owned location remains unchanged.

### SPEC-TCM-001 — TCM-SKL-001 location

> For explicit plugin ownership conforming to SPEC-PLG-020, TCM-SKL-001's managed installed location is supplied by the validated provider binding. Its canonical distribution source and retained core identity remain unchanged. TCM-SKL-002 through TCM-SKL-006 and every other unaffected rule remain in force. This exception does not authorize edits to the retained core or any new skill effect.

REQ-HUP-022's seven-file inventory is a historical 0.11.0 adoption observation and is not rewritten.
INT-DST-001 remains one standard installation: this proposal changes ownership location, not governance policy or a support-profile matrix.
DEC-PLG-004's terminal disposition and DEC-PLG-006's accepted C10/C11 limitation remain unchanged.

## Delivery sequence and current boundary

Approve the nine draft artifacts and four exact applicability amendments, then separately start WO-PLG-020.
Implement and verify the evaluator change; later select its release and adoption through appropriate governed work.
Only after that prerequisite is available can WO-PLG-009 connect live repositories, followed by WO-PLG-013 maintenance.
WO-PLG-015 qualification and WO-PLG-016 released guidance remain separate work.

No new release version, live migration, native host reconfiguration, public publication, or lifecycle decision is authorized by this draft.
