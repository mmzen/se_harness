+++
id = "SPEC-ECP-025"
type = "specification"
title = "Supported ownership in the real upgrade rehearsal"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-16"
updated = "2026-09-16"
contract = "The real upgrade rehearsal accepts supported repository or plugin ownership, requires its preservation, and retains the existing evaluator handover checks."

[relations]
specifies = ["REQ-ECP-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T16:55:52Z"
decided_by = "technical-owner"
reason = "The owner approved the presented SPEC-ECP-025, VER-ECP-027 and WO-ECP-039 package with \"i apprive\" on 2026-09-16, exercising the technical-owner decision for SPEC-ECP-025. Reviewed SHA-256 5fb747ca2bb885570c46de8124be5eae787e6ebb2c0a617355db25fabe95f0c0. This records definition and bounded execution approval, not assurance or external delivery."
+++

# Supported ownership in the real upgrade rehearsal

## Problem and applicability

PR #487's Linux and Windows upgrade rehearsals successfully perform the
0.18.0-to-0.19.0 handover, then fail the repository helper's schema-3-only
assertion. Both produce the same schema-4 lock digest. Plugin ownership is
already supported by the evaluators and preserved by the upgrade.

This addendum refines SPEC-ECP-007 ECP-PRD-008 for WO-ECP-039. Its rules replace
the fixed resulting-schema-3 assertion carried into the helper by historical
WO-ECP-010; that completed record remains unchanged. Supported ownership means
the existing schema-3 repository mode or schema-4 plugin mode described by
REQ-HUP-024's approved exception and SPEC-PLG-021 PLG-KIS-009/012. No new lock
format or product behavior is introduced.

## Rules

**ECP-UPG-001.** The rehearsal accepts schema 3 without skill_ownership as
repository ownership, and schema 4 with a skill_ownership object selecting
provider="plugin" as plugin ownership. Earlier permitted extra plugin binding
fields remain readable. Schema identifiers must be integers; unsupported
schemas or inconsistent provider records fail. The resulting supported
ownership mode must equal the initial mode: an evaluator upgrade without a
provider-change option must not switch ownership. Extra binding metadata need
not be byte-identical; the provider selection must be preserved.

**ECP-UPG-002.** Retain the existing real predecessor doctor, successor plan
and apply, successor doctor and validation, and expected predecessor rejection
after the handover. Retain the existing successor version and installed-payload
checks against transaction evidence. Ownership support cannot excuse a failed
step, wrong evaluator version or wrong payload digest.

**ECP-UPG-003.** Retain the existing result schema, canonical resulting-lock
digest, two-run determinism and cross-platform comparison. The operational
checkout is unchanged; real operations run only in the existing disposable
export. Preserve interpreter isolation, credential filtering, network-free
rehearsal and cleanup behavior.

## Examples and coverage

A schema-4 plugin-owned 0.18.0 root upgraded to a valid schema-4 plugin-owned
0.19.0 root passes after the existing handover checks. The equivalent schema-3
repository-owned upgrade also passes. A schema-4 result with no plugin provider,
a provider switch, an unsupported schema or a mismatched payload fails.

| Requirement | Rules |
| --- | --- |
| REQ-ECP-012 | ECP-UPG-001, ECP-UPG-002, ECP-UPG-003 |

## Design rationale

Change the existing final ownership assertion and extend its existing fixture.
Do not duplicate the installer, add a generic migration framework, change the
workflow or add a dependency. Checking preservation is needed because merely
accepting either schema would also permit an unintended provider switch.
The real evaluators continue to validate complete lock integrity. This bounded
repository-only correction introduces no architecture or trust-boundary change.
