+++
id = "SPEC-RLS-001"
type = "specification"
title = "Assess legacy and minimal candidate layouts from the 0.20 maintenance line"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"
contract = "The maintenance acceptance runner assesses both declared layouts while preserving independent qualification, existing refusal checks and the 0.20 installer."

[relations]
specifies = ["REQ-SHB-008", "REQ-REB-020", "REQ-REB-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T19:43:46Z"
decided_by = "engineering-owner"
reason = "Human mmzen: Approve package and required verification. Approves reviewed SPEC-RLS-001, VER-RLS-027, WO-RLS-027 and REL-SEH-032 and required commit-bound verification. Includes bounded local implementation/preparation and the maintenance 0.19.0 role-label encoding, with mmzen retained as human decision-maker. Reviewed SHA256 a18b72f9e9aadba2590bbab9f990148449e525c4ec0589d6dd672417b0a4877d; transition input SHA256 a18b72f9e9aadba2590bbab9f990148449e525c4ec0589d6dd672417b0a4877d. Only confirmed assurance metadata was added to the work order. Codex applies the matching decision. Push/PR, dispatch, verification acceptance, release, publication, markers and adoption remain separate."
+++

# Assess legacy and minimal candidate layouts

## Purpose and scope

Released 0.20.0 assumes that every candidate creates ENGINEERING_HARNESS.md.
The minimal-layout candidate deliberately omits it. DEC-IAR-004 selects a
maintenance release so an independently released verifier can assess that
candidate. This specification extends the acceptance scenario setup; it does
not replace the existing qualification or authority contracts.

## Rules

**RLS-COMPAT-001 — Recognize the layout.** After successful candidate init,
read its lock. The supported cases are the existing repository-copy layout
(no resource_layout field) and released-resources-v1. Reject an
unsupported declared layout or unusable lock. Do not infer legacy layout from
a missing ENGINEERING_HARNESS.md or silently skip a scenario.

**RLS-COMPAT-002 — Assess the intended footprint.** For the external layout,
default init must create exactly .engineering-harness.toml and
.engineering-harness.lock. Check that footprint before selecting an integration.
Then request the existing Git integration explicitly for the managed-content
refusal test. Bind the setup command and outcome into retained evidence. Do not
require a minimal candidate to recreate repository copies of instructions.

**RLS-COMPAT-003 — Preserve refusal coverage.** On a legacy candidate, keep
the root-instruction customization and managed-file digest corruption cases.
On an external candidate, customize the managed .gitattributes block and corrupt
the evaluator payload digest in separate disposable copies. Require refusal;
the customized-content refusal must leave the repository unchanged. A failed
setup, a missing managed block, a skipped case or an unexpected success fails
assessment. Other existing scenarios, identity checks and isolation stay required.

**RLS-COMPAT-004 — Preserve independent authority.** Keep the typed
qualify candidate-package operation, its result schema, scenario IDs, exact
wheel/commit bindings and role checks. The verifier must not import candidate
code into its process. Tests of the unreleased maintenance runner establish
its behavior only. It becomes an independent released verifier after publication
and the separately authorized selection of its exact public identity.

**RLS-COMPAT-005 — Keep the maintenance product bounded.** Build from the
published 0.20 source baseline. Change the acceptance runner and its tests,
version metadata and the declared release preparation material only. Preserve
the 0.20 installer and packaged instruction/template behavior. Do not backport
the new resource resolver, minimal installer, plugin activation or lifecycle
changes. Reuse the existing runner and release tools; no new command, framework
or bootstrap exception is needed.

## Examples

- A maintenance candidate still initializes the legacy footprint. Its independent
  released predecessor can run the existing acceptance contract against it.
- The maintenance runner assesses the exact minimal wheel retained with
  DEC-IAR-004, including its two-file default and both refusal cases.
- A candidate declares an unknown layout, adds an unexpected default file,
  accepts managed customization, or reports a mismatched digest: assessment fails.
- Passing tests of the maintenance runner does not authorize the successor
  candidate's integration or supply its independent qualification result.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-SHB-008 | RLS-COMPAT-001, RLS-COMPAT-002, RLS-COMPAT-003, RLS-COMPAT-004 |
| REQ-REB-020 | RLS-COMPAT-004, RLS-COMPAT-005 |
| REQ-REB-031 | RLS-COMPAT-004 |

## Design assessment

Reuse ARCH-SHB-002 / ADR-SHB-002 and ARCH-REB-009 / ADR-REB-009. The same isolated verifier controls the same
acceptance operation. A small layout selection within the current scenarios is
enough. A second qualification path or importing the successor resource system
would add scope without meeting an additional need. No new architecture decision
is required. Version identity, release membership and delivery belong to the
release contract; implementation details within these rules remain delegated.
