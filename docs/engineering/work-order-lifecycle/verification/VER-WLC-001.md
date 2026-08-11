+++
id = "VER-WLC-001"
type = "verification"
title = "Verify work-order lifecycle consistency"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-WLC-001", "REQ-WLC-002", "REQ-WLC-003", "REQ-WLC-004", "REQ-WLC-005", "REQ-WLC-006"]
+++

# Verification Contract: Verify work-order lifecycle consistency

## Automated checks

- Validate a legacy repository without policy or with `required_for_verified_work = false` and confirm uncovered verified work remains compatible.
- Enable the policy and confirm missing, `ready`, and `superseded` VREC coverage fail with `E010`.
- Confirm verified and released VREC coverage passes.
- Generate Explorer for a configured violation and confirm the validator error is present while `W-REV-001` is absent.
- Run the full unit suite on Python 3.11 and the local runtime.
- Run fresh initialization, safe upgrade, source doctor, CLI help, formal validation, and dashboard generation.
- Confirm canonical/root parity for the validator, Explorer, workflow, traceability guide, and work-order template.

## Inspection checks

- Review the eleven explicit legacy status changes.
- Confirm every normalized work order has retained completion evidence.
- Confirm covered verified work orders are unchanged.
- Confirm no VREC or RLS file changed.
- Confirm lifecycle documentation distinguishes authority, completion, assurance, and release.

## Pass criteria

All automated and inspection checks pass, formal validation has zero diagnostics, Explorer no longer reports `W-REV-001`, managed integrity passes, and only the known Windows symlink checks may be conditionally skipped.
