+++
id = "ARCH-TST-001"
type = "architecture"
title = "A standard-library scheduler over unittest, with the serial run as the reference"
status = "approved"
owners = ["technical-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[decision_assessment]
outcome = "adr_required"
triggers = ["material-alternatives"]
rationale = "A pytest-based runner with xdist is the obvious alternative to a repository-owned scheduler; the choice binds every future test and the hosted lanes."
assessed_by = "technical-owner"

[relations]
addresses = ["REQ-TST-001", "REQ-TST-002", "REQ-TST-003"]
conforms_to = ["SPEC-TST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T19:18:13Z"
decided_by = "technical-owner"
+++

# Architecture: A standard-library scheduler over unittest, with the serial run as the reference

## Context and scope

The suite is `unittest`; the repository declares no third-party test
dependency and its release qualification runs the serial suite inside the
producer's pinned environment. Parallelism is added around `unittest`, not
by replacing it.

## Components and responsibilities

### Runner
`scripts/run_tests.py`: discovery, class-level scheduling, worker pool,
aggregation, timings. Owns nothing a test can observe.

### Marker
An environment variable read by the two scale tests only.

### Fixture cache
A helper in `tests/` used by fixtures; owns one session-scoped install.

### Reference
`python -m unittest discover`: canonical; the runner at one worker equals
it.

## Dependency direction

Runner depends on `unittest` and the standard library; tests depend on the
fixture helper; nothing in `se_harness` depends on either.

## Trust and failure boundaries

Each class runs in its own process with its own temporary directories, as
today. A verdict difference between parallel and serial is a runner
defect.

## Quality attributes

Under 90 seconds locally at eight workers; same verdict; no dependency.
