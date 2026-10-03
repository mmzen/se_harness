+++
id = "VER-HUP-024"
type = "verification"
title = "Verify release decision identity compatibility in adoption checks"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[relations]
verifies = ["REQ-REB-027", "REQ-IAR-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T07:27:59Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" to the reviewed WO-HUP-029 / VER-HUP-024 two-file CI correction, required commit-bound verification in VREC-HUP-027 and inclusion in the existing review PR grant. Reviewed file SHA256 420ee07f509d2f465cd9f70f6a7f181bcae61fac3cb6b009e48fb9657bbdb772; patch SHA256 10fd74e48ab683ff1e85e5735a40aa027047164f72db4260e616ccf4ff3bc3a5. Human verification acceptance and merge remain separate. Codex applies the recorded decision."
+++

# Verify release decision identity compatibility in adoption checks

## Independent expectations

The accepted simple-upgrade and external-resource contracts preserve lifecycle
authority. The selected released AUTHORITY.md requires the actual decision-maker.
Trusted RLS-SEH-032 records mmzen in both release-decision fields. Neither a
candidate result nor a matching string alone authenticates a human decision.
The checker retains its trusted-base boundary and all other release checks.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-REB-027 | Existing predecessor tests and the exact real adoption assessment | Named-human and legacy-label releases with matching decision fields pass; absent, blank, non-string or mismatched authorizers fail; version, tag, archive, release uniqueness and transaction refusals remain effective. |
| REQ-IAR-031 | Diff and historical-record inspection; selected evaluator checks | Only the reviewed checker/test behavior changes; RLS-SEH-032, its evidence and prior records retain their bytes; adopted schema-5 resources and identity remain valid. |

## Checks and retained evidence

1. Run all `tests.test_governor_transition` tests, including the new cases.
   Demonstrate that the named-human case fails against the original script.
2. Run the corrected predecessor `plan` and `assess` against trusted base
   b9821e3a3ef3f821f36cc92da7fa4ce900f7e750 and the exact clean adoption
   candidate, using the released 0.22.0 Python, entry point and exact wheel.
   Require RLS-SEH-032 and the retained WO-HUP-028 transaction to be selected.
3. Run `python scripts/run_tests.py --scale full` and the remaining VER-HUP-005
   checks on the combined result. Respect each fixture's Git configuration;
   retain actual skips and failed attempts. Required hosted checks remain
   necessary before merge.
4. Pass selected-evaluator validation, both work-order handoffs and combined
   capture gates. Bind evidence from both contracts in VREC-HUP-027 at one
   exact candidate. Publish the review package before requesting verification.

Retain results under evidence/WO-HUP-029/. Windows local tests and hosted
Linux/Windows integration checks have distinct evidence. This work supplies
no native Claude or Codex desktop claim and does not waive their existing limits.
