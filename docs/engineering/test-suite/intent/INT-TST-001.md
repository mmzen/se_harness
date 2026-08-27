+++
id = "INT-TST-001"
type = "intent"
title = "A full suite in about a minute, with the same verdict"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T19:18:13Z"
decided_by = "product-owner"
reason = "Owner decision 2026-08-26: i approve the artifact packet."
+++

# Intent: A full suite in about a minute, with the same verdict

## Problem

The candidate suite is the gate every work order and every pull request
runs, and it takes six to eight minutes serially: 958 tests, 367 seconds
measured on 2026-08-26 on a twelve-CPU workstation, with `unittest`
running one test at a time. 365 of those seconds are inside the tests: two
"scale to one thousand artifacts" tests take 29 seconds; five modules take
half the time; about three hundred tests each pay a half-second
`harnessctl init` in `setUp`. The machine and the hosted runners have idle
cores the whole time.

## Outcome

One command runs the whole suite across worker processes and returns one
verdict identical to the serial run's, in about a minute locally and about
two on a hosted runner; the serial `unittest discover` remains the canonical
reference and is what the reusable qualification definition runs on a
release. Nothing about what a test asserts changes.

## Scope boundary

In: a repository-owned runner script, a marker for the scale tests, the
fixture install cache, the test command in `AGENTS.md`'s owner region, the
suite step of `candidate-evidence.yml`, and the developer notes. Out: any
change to a test's assertions, the release qualification definition (which
keeps the serial suite), the durable-write semantics of the installer, and
any new third-party dependency.

## Accountable product owner

The repository owner.

## Success measure

Full suite locally under 90 seconds at eight workers and under 150 seconds
at four; the same pass/fail set as the serial run on the same commit; the
hosted `candidate-source` job's suite step at least halved.
