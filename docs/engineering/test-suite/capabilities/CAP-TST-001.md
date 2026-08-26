+++
id = "CAP-TST-001"
type = "capability"
title = "Run the candidate suite in parallel with one aggregated verdict"
status = "draft"
owners = ["product-owner", "technical-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
derives_from = ["INT-TST-001"]
+++

# Capability: Run the candidate suite in parallel with one aggregated verdict

## Description

The repository runs its `unittest` suite across worker processes with a
runner it owns, scheduling test classes so the slowest do not end the run,
aggregating every worker's result into one report and one exit code, and
keeping each test's isolation as it is today. Expensive fixtures are shared
through a per-session cache, and the largest scale tests run at full size
only when asked.

## Users

Engineers running the suite before a commit; candidate CI; reviewers reading
a suite figure in evidence.

## Boundaries

Same tests, same assertions, same skips; the serial run stays canonical and
is what a release qualification executes. No pytest, no plugin, no network.

## Derived requirements

`REQ-TST-001` through `REQ-TST-003`.
