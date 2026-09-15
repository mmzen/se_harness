+++
id = "SPEC-HUP-019"
type = "specification"
title = "Adopt evaluator 0.18.0 with consistent supplied guidance"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-09-15"
updated = "2026-09-15"
contract = "A conforming adoption uses the verified public package, records one atomic upgrade, preserves owner content and retains consistent development identities."

[relations]
specifies = ["REQ-HUP-037", "REQ-HUP-038"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T11:01:51Z"
decided_by = "technical-owner"
reason = "The owner replied \"i approve evaluator upgrade\" to the reviewed WO-HUP-019 scope and its five governing drafts on 2026-09-15. This records approval of the selected artifact, including the proposed architecture assessment and required assurance classification where applicable. The accepted scope authorizes start, completion only after passing checks, and ready verification-record preparation; independent verification and external integration remain separate."
+++

# Adopt evaluator 0.18.0 with consistent supplied guidance

## In plain words

The published checker upgrades the repository through its normal installer. Explicit replacements bring the unchanged supplied guides and workflow to the same release.

## Scope

The root installation, supplied guidance, candidate version and directly affected owner instructions.

## Terms

- **Public package:** the 0.18.0 wheel whose checksum is bound by `RLS-SEH-027`.
- **Control:** the unchanged checkout at `386b5b96` under released 0.17.0.

## Rules

**HUP-NEW-001.** The applying runtime MUST use public 0.18.0 outside the checkout in isolated Python mode.

**HUP-NEW-002.** The downloaded wheel SHA-256 MUST equal `a683dbdf485d42aa20ea8502122c171a4c61c7d60f85db5b5f264bd336371c54` before installation.

**HUP-NEW-003.** The approved plan MUST update 25 supplied paths, adopt 11 unchanged paths as editable, and leave five paths unchanged.

**HUP-NEW-004.** The installer MUST receive an explicit replacement argument for each path listed in the replacement set below.

**HUP-NEW-005.** The upgrade MUST retain one transaction document identifying the prior committed lock and the installed 0.18.0 package.

**HUP-NEW-006.** The upgrade MUST preserve owner content surrounding managed fragments and all historical verification and release records.

**HUP-NEW-007.** A repeated upgrade MUST report every supplied path unchanged.

**HUP-NEW-008.** The resulting repository MUST pass released 0.18.0 doctor and graph validation without new errors or unexplained warnings.

**HUP-NEW-009.** The candidate version MUST become 0.19.0 in `pyproject.toml` and `se_harness/__init__.py`.

**HUP-NEW-010.** The supplied workflow and current owner instructions MUST identify evaluator 0.18.0.

**HUP-NEW-011.** Candidate templates and product source MUST remain unchanged except for the candidate version declaration.

**HUP-NEW-012.** Test corrections MUST be limited to demonstrated assumptions about the adopted root identity or supplied-file ownership.

**HUP-NEW-013.** Implementation MUST stop on an unexpected plan action, changed package checksum, failed gate or required change outside the work-order scope.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Download checksum differs | Refuse installation | Package digest mismatch |
| Plan contains unexpected actions | Stop before applying | Installer action and path |
| Candidate remains 0.18.0 | Derivation refuses equal versions | PRE008 |
| Tests fail beyond control failures | Report exact failing tests; stop for correction | Test output |

## Examples

**Given** the reviewed public package, **when** adoption finishes, **then** the lock names 0.18.0 and the repeated plan is unchanged (HUP-NEW-005, HUP-NEW-007).

**Given** the moved root, **when** identity derivation runs, **then** it reports the 0.18.0 to 0.19.0 pair (HUP-NEW-009).

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-HUP-037 | HUP-NEW-001, HUP-NEW-002, HUP-NEW-003, HUP-NEW-004, HUP-NEW-005, HUP-NEW-006, HUP-NEW-007, HUP-NEW-013 |
| REQ-HUP-038 | HUP-NEW-008, HUP-NEW-009, HUP-NEW-010, HUP-NEW-011, HUP-NEW-012 |

## Not decided here

- External environment and temporary output locations.
- Wording of current owner instructions.
- Exact identity-aware corrections for demonstrated test failures.

## Replacement set

These files match their released 0.17.0 distribution before replacement. The 0.18.0 defaults would preserve their older contents.

- `.github/workflows/engineering-harness.yml`
- `docs/engineering/ARTIFACT_AUTHORING.md`
- `docs/engineering/DECISION_RIGHTS.md`
- `docs/engineering/OPERATING_CARD.md`
- `docs/engineering/QUALITY_GATES.md`
- `docs/engineering/TRACEABILITY.md`
- `docs/engineering/WORKFLOW.md`
- `docs/engineering/templates/ADR.template.md`
- `docs/engineering/templates/ARCHITECTURE.template.md`
- `docs/engineering/templates/CAPABILITY.template.md`
- `docs/engineering/templates/INTENT.template.md`
- `docs/engineering/templates/RELEASE_CONTRACT.template.md`
- `docs/engineering/templates/RELEASE_RECORD.template.md`
- `docs/engineering/templates/REQUIREMENT.template.md`
- `docs/engineering/templates/RISK.template.md`
- `docs/engineering/templates/SPECIFICATION.template.md`
- `docs/engineering/templates/VERIFICATION.template.md`
- `docs/engineering/templates/VERIFICATION_RECORD.template.md`
- `docs/engineering/templates/WORK_ORDER.template.md`
