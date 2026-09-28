+++
id = "SPEC-IAR-015"
type = "specification"
title = "Safe retirement of obsolete guide pointers"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-28"
updated = "2026-09-28"
contract = "Stop seeding six obsolete guides in new installations, preserve existing owner files on upgrade, and require consumer checks before separately authorized repository cleanup."

[relations]
specifies = ["REQ-IAR-028"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T07:51:40Z"
decided_by = "technical-owner"
reason = "Human repository owner mmzen: \"I approve, you can start the work orders\". Approval covers the reviewed instruction-cleanup package and required commit-bound assurance. Legacy evaluator role technical-owner records that human decision; Codex applies it. Reviewed SHA-256 e3336d7c24d89c8fce3c591194abba4c30f623fa81956b8dc4519011997f64cd."
+++

# Safe retirement of obsolete guide pointers

## Scope and relationship

This proposal supplements SPEC-IAR-014. It does not replace its accepted rules.
DEC-IAR-002 must select product-wide retirement before this contract is approved.
The repository remains governed by its selected released evaluator until a
separate adoption. No future release number is selected here.

## Rules

**IAR-RET-001.** Exact set. The retirement set is the following six paths under
docs/engineering/: OPERATING_CARD.md, DECISION_RIGHTS.md, QUALITY_GATES.md,
WORKFLOW.md, TRACEABILITY.md and TECHNICAL_COMMUNICATION.md. New installations
of the future release do not create or track these seed files. Remove their
current source templates and distribution entries together.

**IAR-RET-002.** Replacement routes. Current templates, skills, generated Explorer
content and instruction routes work without those six files. Their destinations
are CONTINUE.md; AUTHORITY.md; RESULTS.md; CONTINUE.md/RECORD_STATE.md/RESULTS.md;
ARTIFACTS.md/DEFINITION_LINKS.md/WORK_AND_EVIDENCE.md; and COMMUNICATION.md,
respectively, under docs/engineering/harness/. Select the exact applicable heading.
An old-release fallback may still name an old guide when that installed release
needs it. Classify each remaining reference as current, historical or conditional;
do not require zero textual matches across the repository.

**IAR-RET-003.** Existing owner files. An upgrade from the current instruction
collection preserves existing stock pointers and custom owner text byte-for-byte.
Retain an explicit migration disposition for customized guides. An absent
seed stays absent. Use the existing leaving-seed behavior to reconcile the lock;
do not hand-edit the lock, change a seed into managed content, or add automatic
owner-file deletion. Verify that doctor and readiness accept the resulting state.

**IAR-RET-004.** Supported predecessor migration. Keep recognized 0.18.0 migration
fingerprints and tests while that upgrade remains supported. A recognized old
full guide still follows the accepted migration to a compatibility pointer;
this version-conditioned conversion is not a new-installation seed. Show that
exact conversion in the preview. Customized old guides need an explicit owner
migration plan and remain untouched until it is authorized. If the migration
cannot safely classify an input, refuse before writes and report the exact
file and supported recovery. Record supported
source versions explicitly; removing a template is not permission to drop an
advertised upgrade path.

**IAR-RET-005.** Repository cleanup. Removing the six existing files from this
repository is a separate adoption action. Before it, inventory the active host
and plugin, verify current routes and native delivery, and bind the selected
release, exact files and their reviewed hashes to the cleanup authority. Remove
only unchanged stock pointers. A customized or ambiguous file needs a reviewed
owner migration; a still-required file remains. Preview and apply the selected
released installer's lock reconciliation, then run doctor and applicable checks.
Inspect actual state after interruption before retrying any deletion or apply.

**IAR-RET-006.** Preserved content. Keep ARTIFACT_AUTHORING.md, WORKFLOW.json,
QUALITY_GATES.json, the root and current harness collection, owner AGENTS.md,
historical evidence, accepted artifacts and required version-conditioned adapters.
An operating-card renderer or constant is not removed solely because the new
installation omits its output; first establish whether supported callers need it.

**IAR-RET-007.** Failure boundary. Unknown owner content, unsafe paths, missing
replacement instructions or an unresolved active consumer prevent the affected
retirement. The operation must not record a successful retirement or partially
delete files. Other independently authorized work can proceed.

## Simplicity and architecture

The existing installer already separates editable seeds from managed files.
Retaining existing seeds on upgrade and making cleanup explicit uses that
boundary. A new deletion engine or CLI is not required by this contract.
New code is justified only by a demonstrated gap in preview, preservation or
supported migration. This refinement adds no service, trust boundary, lifecycle
authority or retrieval system; no new architecture or ADR is proposed.

## Examples

A fresh installation has the current harness collection and no six pointers.
An upgrade with owner notes in TRACEABILITY.md keeps the complete file unchanged.
A separately approved cleanup with a stale installed skill stops before deleting
OPERATING_CARD.md. A 0.18.0 migration either gives a usable current route with an
explicit disposition for old guides or refuses without writing.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-IAR-028 | IAR-RET-001, IAR-RET-002, IAR-RET-003, IAR-RET-004, IAR-RET-005, IAR-RET-006, IAR-RET-007 |

## Not decided here

- The release version, release authority and exact self-adoption transaction.
- Replacement of customized owner files or removal of old-release support.
- A generic revision capability, exception engine or new lifecycle command.
