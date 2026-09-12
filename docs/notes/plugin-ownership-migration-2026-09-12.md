# Evaluator skill ownership migration: definitions and implementation

Prepared 2026-09-12 against main `3bf0ef2a7a2b4008efaa3cb79431d526d3f6f600`.
The operator selected delegated execution and approved DEC-PLG-007 with its amendments on 2026-09-12. The released evaluator records the nine packet approvals, and all eight exact applicability amendments are appended to their target contracts. PR #461 integrated them at `6559568e995fc6e28f64e6bc5a6d4a6dc5dcf7de`. The required live `validate` check passed there, and the delegated start was recorded at `e33d8c86`; WO-PLG-020 is now in progress. Development observations are retained in the [evidence index](../engineering/plugin-integration/evidence/WO-PLG-020/README.md); completion and verification preparation require the remaining acceptance and live candidate gates.

## Why this work is next

[DEC-PLG-004](https://github.com/mmzen/se_harness/blob/17382d8e7f7a5709f4f55facfe875fbf455e5794/docs/engineering/plugin-integration/decisions/DEC-PLG-004.md) already selected supported evaluator migration.
Its accepted goal is automatic replacement of overlapping repository skills by plugin implementations, with ownership/integrity updates and unrelated skills preserved.
WO-PLG-009 supplies the later connection procedure and explicitly excludes building this missing evaluator capability.

The current installation contains two retained canonical skills and one Claude orientation adapter: seven managed files total.
The three old writing skills were retired by the earlier ECP work; they are not a new migration catalog.
Current installer planning and doctor both derive their managed set from the standard template.
Deleting the retained skills alone breaks integrity and allows an upgrade to recreate them.

## Selected packet

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

## Selected design

1. Keep the single standard harness and ordinary repository ownership as the default.
2. Add an explicit plan/apply/restore operation for an independently selected plugin binding.
3. Represent plugin ownership with lock schema 4; keep schema 3 support for default ownership.
4. Share one effective-inventory resolver across installer, doctor, and applicable mutation checks.
5. Require complete input revalidation, exclusive application, durable interruption recovery, and exact-file retirement.
6. Keep portable provider identities in the lock; external machine paths remain local inputs.
7. Let credential-free CI validate repository ownership without falsely proving external plugin availability.

The operator selected the reviewed packet through delegated execution. DEC-PLG-007 resolves the additional schema-floor contradiction through the narrow exception below.
Native host discovery is deliberately a later observed result under WO-PLG-009; package inventory checks cannot establish it.

## Approved prior-contract amendments

These four applicability amendments are appended under `Amendment record` in their target contracts. Each identifies WO-PLG-020, the approval date, and accountable role; all preceding bytes, lifecycle history, and historical observations are preserved.

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

DEC-PLG-007 is decided as `narrow-schema4-exception`; the selected nine-artifact packet and all eight applicability amendments are approved.
The approved class-bearing definitions are integrated into main. The released evaluator applied the delegated start after check-run `103560311357` succeeded at the merged base; the retained start receipts identify the check and candidate.
Implement and verify the evaluator change; later select its release and adoption through appropriate governed work.
Only after that prerequisite is available can WO-PLG-009 connect live repositories, followed by WO-PLG-013 maintenance.
WO-PLG-015 qualification and WO-PLG-016 released guidance remain separate work.

These definition approvals do not select a release version, live migration, native host reconfiguration, public publication, verification decision, or PR merge.

## Implementation under acceptance

The candidate introduces `skill-ownership TARGET --provider plugin --binding-input FILE` for a read-only migration plan, and `--provider repository` for a restoration plan. An application requires `--apply --expected-plan-sha256 HASH`. The binding input explicitly names supported hosts, ordinary external assembly roots, and independently expected plugin, inventory, and retained-file identities. Planning and application do not execute a plugin or contact a host.

Plugin ownership is recorded in a closed schema-4 lock section. The seven catalog files leave the repository-managed set; unrelated content stays in place. Installer planning, direct application, doctor, ordinary mutation guards, and current-lock evaluator evidence share the ownership checks. Ordinary repository ownership remains schema 3. The portable binding records expected identities, not machine-local roots or a claim that a plugin is currently available. Its checksum detects inconsistent record edits; it is not proof of an owner's approval against a coherent rewrite of the whole record.

Application holds the repository mutex, revalidates the reviewed inputs, and retains bounded before/after stages and durable recovery metadata. A failure before durable commit restores prior state when safe. Recovery after durable commit finalizes the applied state and cleanup. Intervening owner edits, new destinations, conflicting file identities, and hostile recovery data cause explicit refusal or recovery-required status. Recovery does not treat an old snapshot as permission to overwrite owner changes.

The implementation is being tested on disposable repositories and isolated non-promotable package environments. The development full-suite run and preliminary wheel are recorded with their failures and source-snapshot limits. They do not establish final committed-candidate acceptance. The current root remains governed by released 0.17.0; this checkout has not been migrated and the new operation is not yet a released capability.

The operator approved [supplement revision 2](../engineering/plugin-integration/evidence/WO-PLG-020/governance/supplement-revision-2.md) on 2026-09-12. Its [decision receipt](../engineering/plugin-integration/evidence/WO-PLG-020/governance/supplement-revision-2-approval.json) records the five prior-contract applicability amendments and ten additional WO scope paths. They reconcile the Python 3.13 ownership matrix, the explicit command target and transaction outcomes, and their CI/CLI documentation and tests. The original verification matrix remains in force; this supplemental definition approval does not complete the work order or verify a record.

## Delegated route selected

The operator replied **"take the delegated route"** to the concrete packet approval and implementation question.
WO-PLG-020 now carries `[delegation] class = "execution"`, with reserved VREC-PLG-015 and evaluator-sidecar paths.
These identifiers were checked against all local refs and fetched GitHub branch history; no record is created by reserving its path.
The delegated executor may apply DR-WO-START, DR-WO-COMPLETE, and DR-VREC-PREPARE only after the approved class is present at the PR base and the live validate check passes for the exact candidate.
The class does not grant definition decisions, assurance, release, merge, credentials, or external-action authority.

## Additional schema-floor reconciliation

The preparation review found a gap in the original packet: the following current contracts explicitly limit reads and writes to schema 3.
The technical-owner decision in DEC-PLG-007 resolves this contradiction with `narrow-schema4-exception`.
The original four location amendments above remain part of the selected packet. The following four additional amendments were approved by the operator as the named accountable owners on 2026-09-12.

### REQ-HUP-024 — repository-owner, engineering-owner, security-owner

> For explicit plugin ownership conforming to SPEC-PLG-020, the schema-3-only read and write clauses admit one additional supported format: schema 4 with a fully validated plugin ownership binding. Ordinary repository ownership continues to use schema 3. Schemas 1 and 2 remain refused before any write; unknown schemas and invalid schema-4 bindings remain refused. Canonical digests, evaluator identity, fragment ownership, and preservation of historical evidence remain unchanged.

### SPEC-HUP-012 — technical-owner, security-owner

The exact approved text is preserved in [SPEC-HUP-012's amendment record](../engineering/repository-harness-upgrade/specifications/SPEC-HUP-012.md#approved-plugin-ownership-applicability--2026-09-12). It permits validated schema-4 plugin ownership for HUP-LSF-001, HUP-LSF-003, and HUP-LSF-008, retains the schema-3 lower floor and the unchanged rules, and keeps HUP-LSF-007's separate repository transition assessor schema-3-only. This operator note summarizes that record without repeating retired evaluator terminology.

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

### Recorded owner action

The operator approved DEC-PLG-007 option `narrow-schema4-exception`, the four additional applicability amendments, the candidate policy text, and the named scope/acceptance corrections with "i approve DEC-PLG-007’s `narrow-schema4-exception` with amendements".
The earlier "take the delegated route" selection authorizes the reviewed packet approvals and its execution class. The released evaluator records the selected approvals; deliver the class-bearing definitions to main before delegated implementation.
