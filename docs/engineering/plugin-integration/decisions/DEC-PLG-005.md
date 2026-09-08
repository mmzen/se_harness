+++
id = "DEC-PLG-005"
type = "decision"
title = "First plugin qualification profile"
status = "open"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

kind = "question"
question = "Which host configurations and performance acceptance limits will define the first qualified plugin version?"
raised_by = "implementation-planner"
recommendation = "bounded-qualification"

[[options]]
id = "bounded-qualification"
label = "Approve an explicit configuration matrix and numeric or relative budgets before qualification."

[[options]]
id = "preview-only"
label = "Publish measurements as an unqualified technical preview without supported-version or performance claims."

[relations]
concerns = ["REQ-PLG-025", "REQ-PLG-026", "SPEC-PLG-015", "VER-PLG-015", "WO-PLG-015"]
blocks = ["VER-PLG-015"]
+++

# Decision: First plugin qualification profile

## Question

Which host configurations and performance acceptance limits will define the first qualified plugin version?

The proposal names both hosts and Windows, Linux, and macOS, but has no observed host compatibility matrix or accepted execution-time budget.

## Options

**bounded-qualification.** Approve an explicit configuration matrix and numeric or relative budgets before qualification.

**preview-only.** Publish measurements as an unqualified technical preview without supported-version or performance claims.

## Recommendation

The profile must name host versions, operating systems, Python versions, repository sizes, measurement repetitions, and acceptable prompt and latency changes. Current authority checks cannot be removed to meet a budget.

## Disposition

Pending. Only the evaluator records a disposition after the accountable owner's explicit decision.

The preview option does not supply qualification criteria or approve the verification contract. Preview delivery would require separate amended scope.
