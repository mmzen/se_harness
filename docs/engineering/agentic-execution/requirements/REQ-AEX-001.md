+++
id = "REQ-AEX-001"
type = "requirement"
title = "Distinguish accountable authority from agent execution"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN the system represents a human decision actor, delegated worker, skill, or runtime permission, THE SYSTEM SHALL distinguish the accountable role, agent execution profile, executable procedure, delegated scope, and technical permission; and SHALL NOT infer an engineering decision right from an agent name, model, prompt, tool, sandbox, runtime configuration, or successful command."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "requirements-steward"
+++

# Requirement: Distinguish accountable authority from agent execution

## Rationale

Terms such as architect, verifier, or release assessor can describe either a
human accountable role or a specialized agent. Without explicit separation, a
runtime configuration may appear to grant product, architecture, assurance, or
release authority that the harness never authorized.

## Preconditions and trigger

The system is rendering, validating, materializing, or executing a workflow
that identifies a decision actor, worker profile, skill, delegated scope, model,
tool, sandbox, or runtime permission.

## Required response

- Represent accountable decision roles separately from non-accountable agent
  execution profiles.
- Identify the selected formal artifact or work scope independently from both.
- Treat skill and agent names as execution metadata rather than proof of
  authority.
- Treat runtime permissions only as technical access controls.
- Require the existing applicable decision-right and lifecycle evidence for any
  accountable transition.
- Render a clear conflict when an execution profile is presented as the source
  of an accountable decision.

## Failure and boundary behavior

- Reject or stop before mutation when required authority fields are absent,
  ambiguous, or represented only by runtime configuration.
- Do not silently reinterpret a profile such as `verification-evidence-analyst`
  as `assurance-owner`.
- Do not claim organizational independence because a subagent uses a fresh
  context, different model, or read-only sandbox.

## Constraints

- Existing accountable role names and decision-right semantics remain governed
  by managed policy.
- The harness may record an actor assertion but cannot prove real-world identity
  or role ownership without a separately governed identity mechanism.
- Human and machine outputs must express the same authority separation.

## Acceptance examples

### Example: agent prepares assurance material

**Given** a worker with execution profile `verification-evidence-analyst`

**When** it reviews tests and prepares a ready VREC proposal

**Then** the receipt identifies the execution profile, the decision packet names
the required `assurance-owner`, and no output claims that the VREC is verified.

### Example: runtime permission is not authority

**Given** an implementation worker running with workspace-write permission

**When** no approved work order or permitted autonomy envelope authorizes a
requested write

**Then** the harness refuses the governed mutation even though the runtime could
technically write the file.

## Open decisions

Before approval, the specification must decide the stable field names and
compatibility behavior for existing outputs that currently contain only an
actor or owner string.
