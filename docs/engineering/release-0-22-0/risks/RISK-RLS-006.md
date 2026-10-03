+++
id = "RISK-RLS-006"
type = "risk"
title = "Missing draft evidence can crash an unrelated transition"
status = "raised"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"
description = "Public evaluator 0.22.0 raises FileNotFoundError during a start preview when another draft names a future evidence_paths file that does not yet exist. Validation accepted the draft. Keeping future evidence destinations in draft prose avoids this crash, but the raw failure remains a product limitation."
action = "Plan a bounded follow-up to report missing evidence safely and keep unrelated draft evidence from crashing lifecycle operations. Retain the observed workaround and failure until corrected and verified."
raised_by = "operator"

[relations]
threatens = ["WO-RLS-035"]

[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-03T05:09:30Z"
decided_by = "operator"
reason = "Recorded by harnessctl raise-risk."
+++

# Risk: Missing draft evidence can crash an unrelated transition

## Description

Public evaluator 0.22.0 raises FileNotFoundError during a start preview when another draft names a future evidence_paths file that does not yet exist. Validation accepted the draft. Keeping future evidence destinations in draft prose avoids this crash, but the raw failure remains a product limitation.

## Next action

Plan a bounded follow-up to report missing evidence safely and keep unrelated draft evidence from crashing lifecycle operations. Retain the observed workaround and failure until corrected and verified.
