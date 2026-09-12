# Evaluator skill ownership migration: proposed packet

Prepared 2026-09-12 against main `3bf0ef2a7a2b4008efaa3cb79431d526d3f6f600`.
The operator selected delegated execution on 2026-09-12. The nine implementation artifacts remain draft while the newly discovered schema-floor conflict awaits DEC-PLG-007. No implementation or prior-contract amendment has been applied.

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

The operator selected the reviewed packet through delegated execution. The additional existing schema-floor contradiction below needs an accountable decision before that selection can be activated.
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

Resolve DEC-PLG-007 and accept the four additional amendments below, then record approval of the selected nine-artifact packet and all eight applicability amendments.
Integrate the approved class-bearing definitions into main. Start WO-PLG-020 through delegated execution only after the required live check succeeds for the exact implementation candidate.
Implement and verify the evaluator change; later select its release and adoption through appropriate governed work.
Only after that prerequisite is available can WO-PLG-009 connect live repositories, followed by WO-PLG-013 maintenance.
WO-PLG-015 qualification and WO-PLG-016 released guidance remain separate work.

No new release version, live migration, native host reconfiguration, public publication, or lifecycle decision is authorized by this draft.

## Delegated route selected

The operator replied **"take the delegated route"** to the concrete packet approval and implementation question.
WO-PLG-020 now carries `[delegation] class = "execution"`, with reserved VREC-PLG-015 and evaluator-sidecar paths.
These identifiers were checked against all local refs and fetched GitHub branch history; no record is created by reserving its path.
The delegated executor may apply DR-WO-START, DR-WO-COMPLETE, and DR-VREC-PREPARE only after the approved class is present at the PR base and the live validate check passes for the exact candidate.
The class does not grant definition decisions, assurance, release, merge, credentials, or external-action authority.

## Additional schema-floor reconciliation

The preparation review found a gap in the original packet: the following current contracts explicitly limit reads and writes to schema 3.
DEC-PLG-007 blocks SPEC-PLG-020 until its technical owner resolves this contradiction.
The original four location amendments above remain part of the selected packet. The following four additional amendments require accountable acceptance.

### REQ-HUP-024 — repository-owner, engineering-owner, security-owner

> For explicit plugin ownership conforming to SPEC-PLG-020, the schema-3-only read and write clauses admit one additional supported format: schema 4 with a fully validated plugin ownership binding. Ordinary repository ownership continues to use schema 3. Schemas 1 and 2 remain refused before any write; unknown schemas and invalid schema-4 bindings remain refused. Canonical digests, evaluator identity, fragment ownership, and preservation of historical evidence remain unchanged.

### SPEC-HUP-012 — technical-owner, security-owner

> Under SPEC-PLG-020, HUP-LSF-001, HUP-LSF-003, and HUP-LSF-008 admit validated schema-4 plugin ownership as an explicit exception to their schema-3-only clauses. The lower floor remains 3, including the existing pre-3 refusal and recovery guidance. HUP-LSF-002, HUP-LSF-004, HUP-LSF-005, and HUP-LSF-006 remain unchanged. HUP-LSF-007 continues to govern the separate repository-owned governor-transition assessor as schema-3-only; no schema-4 support is claimed for that tool.

### VER-HUP-012 — assurance-owner, security-owner

> The existing schema-3 writer observations remain the required default-repository cases and retain their historical results. Explicit schema-4 plugin ownership is verified by VER-PLG-020, including valid and invalid bindings, unchanged evaluator-evidence matching, legacy-reader refusal, upgrade preservation, and safe restoration. Every pre-3 refusal, deleted-symbol prohibition, digest-semantic check, and reserved MG002 criterion remains in force.

### SPEC-PMI-001 — engineering-owner, quality-owner, security-owner

> The schema-3-only applicability stated by the WO-HUP-012 amendment now includes the narrowly validated schema-4 plugin ownership exception of SPEC-PLG-020 and the corresponding SPEC-HUP-012 amendment. The historical reason for retiring schema-1 and schema-2 handling is preserved. No digest canonicalization, fragment semantics, historical evidence, or default schema-3 behavior changes.

### Candidate WORKFLOW source — technical-owner

During implementation, replace its integrity paragraph with the following text at `templates/repository/standard/docs/engineering/WORKFLOW.md`; do not edit the installed root copy:

> Managed-file integrity uses SHA-256 over the versioned `utf8-text-lf-v1` representation and binds the installed released-evaluator payload plus its archive when available. LF, CRLF, and CR are equivalent line terminators; all other content distinctions remain significant. Schema 3 is the default repository format. Schema 4 is supported only with a validated explicit plugin ownership binding under SPEC-PLG-020. Schemas 1 and 2 are refused before writes. Ordinary mutation requires the exact evaluator identity bound by the selected supported lock. `doctor` and mutation plans are read-only, and customized, ambiguous, or identity-mismatched content is never overwritten.

### Scope and acceptance corrections

Add `se_harness/engine/validation_evidence.py` to the implementation scope because its current-lock evidence matcher independently requires schema 3.
Add the candidate WORKFLOW source and its documentation regression test; use existing `tests/test_harnessctl.py` instead of a nonexistent `tests/test_cli.py`.
Require positive/mismatch evaluator-evidence cases on a plugin-owned lock.
Require interrupted recovery to preserve intervening owner edits/new files and refuse tampered, truncated, or path-escaping recovery records.
These additions implement the packet's existing preservation and unchanged-governance obligations; no new product behavior or relaxed acceptance criterion is introduced.

### Accountable action

Select DEC-PLG-007 option `narrow-schema4-exception`, approve the four additional applicability amendments and candidate policy text above, and include the named scope/acceptance corrections in WO-PLG-020.
After that decision, record the selected packet approvals with the released evaluator and deliver the class-bearing definitions to main before delegated implementation.
