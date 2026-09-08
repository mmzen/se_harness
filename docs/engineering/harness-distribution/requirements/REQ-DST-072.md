+++
id = "REQ-DST-072"
type = "requirement"
title = "Surface a scope or handoff check refusal as its own text"
status = "draft"
owners = ["product-owner", "technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "IF the managed workflow's scope or handoff check produces no result, THEN THE MANAGED WORKFLOW SHALL fail with the check's own refusal text."
verification_method = ["test", "inspection"]
priority = "must"
source = "issue #380 (code health assessment 2026-09-07, section 4): the managed template engineering-harness.yml lines 98 and 132 at main a68caf70, where `|| true` hands an empty result to a JSON reader"
measure = "an empty or non-JSON result file fails the step with the check's stderr and exit status in the log, and no JSONDecodeError traceback"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Surface a scope or handoff check refusal as its own text

## In plain words

When the released evaluator refuses to run the scope check, the pipeline
shows a Python traceback about missing JSON. It should show what the
evaluator said.

## Why

The managed lane swallows the check's exit status and hands its stdout to a
JSON reader. A mutation-guard or identity refusal writes nothing to stdout,
so the reader crashes and the refusal text scrolls away in stderr. A consumer
debugging a red check then reads a decoder traceback instead of the rule
that stopped them. This is the file every governed repository installs, so
the fix ships by release.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| the check exits without writing a result | the step prints the check's stderr and fails with its exit status | a decoder traceback is the only message |
| the check writes a result | the step reads it exactly as today | unchanged |

## Examples

### Normal

**Given** a consumer repository whose evaluator refuses the scope check with
a guard code,

**When** the managed lane runs,

**Then** the step log ends with the guard's message and the step fails.

### Failure

**Given** a scratch copy of the template where the exit status is swallowed
again,

**When** the template test runs the embedded reader on an empty file,

**Then** the test fails because a traceback, not the refusal, reached the log.
