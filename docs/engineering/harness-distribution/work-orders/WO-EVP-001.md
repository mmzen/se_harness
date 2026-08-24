+++
id = "WO-EVP-001"
type = "work_order"
title = "Align public and executive positioning with current capability"
status = "implemented"
owners = ["engineering-owner", "documentation-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "Public onboarding and executive product claims are trusted engineering state that may influence adoption, assurance expectations, and later product decisions."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "README.md",
  "VALUE_PROPOSAL.md",
  "tests/test_public_onboarding.py",
  "tests/test_value_proposal.py",
  "docs/engineering/harness-distribution/README.md",
  "docs/engineering/harness-distribution/specifications/SPEC-EVP-001.md",
  "docs/engineering/harness-distribution/verification/VER-EVP-001.md",
  "docs/engineering/harness-distribution/work-orders/WO-EVP-001.md",
  "docs/engineering/harness-distribution/evidence/WO-EVP-001-verification.md",
]

[relations]
implements = ["REQ-DST-060"]
specifications = ["SPEC-EVP-001"]
verification = ["VER-EVP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:55:25Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T12:58:10Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T13:29:17Z"
decided_by = "engineering-owner"
+++

# Work Order: Align public and executive positioning with current capability

## Lifecycle

This draft prepares a bounded documentation correction in response to the
accountable user's request to replace `VALUE_PROPOSAL.md` with the supplied
executive speech/demo proposal, check the current README against the repository,
and challenge unsupported claims. Drafting records no approval, start decision,
implementation completion, verification, repository integration, release, or
external action.

Commit-bound verification is required because public claims about authority,
scope enforcement, provenance, multi-agent capability, and release boundaries
can materially affect adoption and assurance decisions. No active architecture
addresses `REQ-DST-060`, so the conditional `architecture` relation is omitted.

## Objective

Deliver a persuasive executive narrative and consistent root README that state
the current product accurately, distinguish roadmap from shipped capability,
and demonstrate the real human decision boundary without turning marketing
language into an unsupported technical guarantee.

## In scope

- Audit every material README and supplied-proposal claim against current main,
  released/candidate CLI help, formal records, and the shipped skill contract.
- Replace `VALUE_PROPOSAL.md` with the challenged executive speech and
  demonstration brief defined by `SPEC-EVP-001`.
- Correct and compress README wording needed to expose the same boundaries,
  retain its current operational facts, and link the executive brief.
- Add focused tests for scope/enforcement, current-versus-roadmap agentic
  capability, canonical demo lifecycle, exact-commit language, and scale claims.
- Update the harness-distribution index and retain work-order-keyed evidence.

## Out of scope

- Implementing delegation, additional skills, multi-agent orchestration,
  runtime adapters, sandboxing, permissions, concurrency control, or issue #80.
- Changing CLI, package, templates, managed policy, lifecycle semantics,
  workflows, tests unrelated to these two documents, or formal history.
- Claiming compliance certification, independent assurance without role
  separation, proven enterprise scale, or physical prevention of unauthorized
  writes.
- Commit, push, pull request, merge, VREC preparation/transition, release,
  publication, deployment, demo hosting, or any other external action.

## Authorized decision envelope

After approval and an explicit start decision, the implementation agent may
edit sentence structure, timing, demo scenario details, diagrams, Q&A order,
and README compression within `SPEC-EVP-001`. It may add the focused test module
named in the execution scope. It may not convert roadmap content into current
capability, remove a required qualifier, change formal state, or broaden scope.

## Constraints

- Treat the attachment as proposed content, not executable instructions.
- Use current `main` facts and preserve unrelated work in other worktrees.
- Keep README at most 200 lines and retain its current nine level-two headings.
- Keep the executive primary flow within 10–15 minutes by design, with a
  prepared fallback rather than reliance on a live model's timing.
- Preserve repository-relative links, UTF-8 Markdown, and exact authority
  boundaries.

## Expected change surface

The two public Markdown documents, focused documentation tests, this bounded
packet's index entry, and one retained evidence file only.

## Required verification

- Start and review preflight for `WO-EVP-001` at the applicable lifecycle stage.
- Focused `test_public_onboarding` and `test_value_proposal` suites.
- Complete unit suite with clean-main baseline comparison for any known local
  platform failures.
- Formal artifact and release-distribution validation.
- Candidate and released CLI/help inspection; released-evaluator `doctor`.
- Markdown fence, local-link, image, line-budget, and final-diff review.
- Manual claim classification and executive-flow rehearsal.

## Evidence to record

Record the attachment disposition, before/after claim matrix, current source
facts, exact changed paths, commands and exit codes, test counts and skips,
validation and doctor summaries, line/heading/link checks, demo rehearsal,
deviations, residual uncertainty, and all unperformed lifecycle/Git/external
actions in `docs/engineering/harness-distribution/evidence/WO-EVP-001-verification.md`.

## Stop and escalate conditions

Stop if the packet is not approved, no explicit start decision exists,
preflight fails, current main changes a reviewed fact, a required qualifier
would make the intended narrative unacceptable, a change needs runtime or
managed-policy work, tests fail beyond a confirmed baseline, or any requested
action exceeds the exact execution scope.

## Completion report format

Report the challenged claims, resulting README/value narrative, exact checks
and results, retained evidence path, unchanged runtime/formal/external
boundaries, current WO state, and one next accountable decision.
