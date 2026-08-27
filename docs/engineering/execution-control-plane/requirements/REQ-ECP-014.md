+++
id = "REQ-ECP-014"
type = "requirement"
title = "A shipped skill invokes the evaluator it describes"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "IF a shipped skill script cannot invoke the released evaluator for the operation its `SKILL.md` describes, THEN THE SYSTEM SHALL exclude that skill from the distributed template."
verification_method = ["inspection", "test"]
priority = "must"
source = "review section 3; check_scope.py:190-199"

[relations]
derives_from = ["CAP-ECP-003"]
+++

# Requirement: A shipped skill invokes the evaluator it describes

## Rationale

The three writing skills inject a stub client and print `"evaluator_invoked":
false` while their `SKILL.md` says they invoke the evaluator
(.agents/skills/harness-execute-work-order/scripts/check_scope.py:190-199;
`check_prepare.py:174-180`; `guard.py:177-185`; docs/notes/agentic-execution-
review-2026-08.md:160-163). They are `disable-model-invocation: true`, require a
delegation table no work order has, and stub the evaluator, so 28 KB of hash-
locked skill scripts are dead weight (docs/notes/agentic-execution-
review-2026-08.md:247-251). A skill that describes an operation it cannot
perform misleads the agent into re-issuing the command by hand
(docs/notes/complexity-audit-2026-08.md:264).

## Behavior

- Trigger: a skill directory under
  `templates/repository/standard/.agents/skills/` is packaged into the
  distribution.
- Response: every script the skill's `SKILL.md` names as invoking the evaluator
  runs the released evaluator as a real subprocess and reports
  `evaluator_invoked: true` in its result, or the skill directory is absent from
  the distributed template and from every host adapter.
- On failure: the portable-surface check fails the build when a packaged skill
  script contains a stub client or emits `evaluator_invoked: false`.

## Assumptions and dependencies

- `harness-orient` is a real read-only wrapper today and stays.
- Retired skills are removed from `.claude/` adapters and `openai.yaml` in the
  same change, so no host lists a skill the template does not ship.
- A retired skill can return once it calls the evaluator for real.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-014.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** the distributed template is built.

**When** each packaged `SKILL.md` is inspected against its scripts.

**Then** every skill that says it invokes the evaluator has scripts that spawn
the released `harnessctl` and print `evaluator_invoked: true`; `harness-execute-
work-order` is absent.

### Example: failure behavior

**Given** a candidate reintroduces `check_scope.py` with `client=lambda ...`.

**When** the surface check scans the packaged skills.

**Then** the build fails and names `check_scope.py` and the stubbed line.

## Open decisions

None.
