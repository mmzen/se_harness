+++
id = "RISK-RLO-001"
type = "risk"
title = "Publication control drift during complete-release activation"
status = "raised"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
description = "Removing the separate PyPI reviewer before the exact approved release plan, trusted main resolution, OIDC binding and branch restrictions are verified could permit publication outside the intended human approval. Live configuration can also drift after review."
action = "Under WO-RLO-016, retain the exact control snapshot and proposed diff, verify preservation of main-only publication, OIDC and credential isolation, and require the concrete one-time configuration review before activation. Stop on drift or unavailable required evidence."
raised_by = "Codex agent"

[relations]
threatens = ["REQ-RLO-023"]

[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-02T20:11:38Z"
decided_by = "Codex agent"
reason = "Recorded by harnessctl raise-risk."
+++

# Risk: Publication control drift during complete-release activation

## Description

Removing the separate PyPI reviewer before the exact approved release plan, trusted main resolution, OIDC binding and branch restrictions are verified could permit publication outside the intended human approval. Live configuration can also drift after review.

## Next action

Under WO-RLO-016, retain the exact control snapshot and proposed diff, verify preservation of main-only publication, OIDC and credential isolation, and require the concrete one-time configuration review before activation. Stop on drift or unavailable required evidence.
