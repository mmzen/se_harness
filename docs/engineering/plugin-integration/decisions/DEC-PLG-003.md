+++
id = "DEC-PLG-003"
type = "decision"
title = "Plugin-first public onboarding"
status = "open"
owners = ["product-owner"]
created = "2026-09-08"
updated = "2026-09-08"

kind = "question"
question = "How should the approved PyPI-first contracts change before plugins become the primary onboarding route?"
raised_by = "implementation-planner"
recommendation = "amend-public-contracts"

[[options]]
id = "amend-public-contracts"
label = "Approve scoped amendments making qualified plugins the primary route while retaining the CLI."

[[options]]
id = "retain-cli-primary"
label = "Keep the CLI primary and document plugins as an additional route."

[relations]
concerns = ["REQ-PLG-027", "SPEC-PLG-016", "WO-PLG-016", "REQ-DST-009", "SPEC-DST-003", "SPEC-DST-024"]
blocks = ["REQ-PLG-027"]
+++

# Decision: Plugin-first public onboarding

## Question

How should the approved PyPI-first contracts change before plugins become the primary onboarding route?

The operator prefers plugin installation. Existing public-onboarding contracts still require PyPI-first guidance, so publishing contradictory guidance would leave two competing contracts.

## Options

**amend-public-contracts.** Approve scoped amendments making qualified plugins the primary route while retaining the CLI.

**retain-cli-primary.** Keep the CLI primary and document plugins as an additional route.

## Recommendation

The recommended option preserves Python as an operator prerequisite and the released CLI for CI. Exact amendments require the accountable owners; existing approved records are unchanged in this packet.

## Disposition

Pending. Only the evaluator records a disposition after the accountable owner's explicit decision.

The selected option does not amend existing contracts or approve the new requirement. Those decisions remain separate and name the exact changed artifacts.
