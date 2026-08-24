+++
id = "VER-EVP-001"
type = "verification"
title = "Verify executive positioning against shipped behavior"
status = "approved"
owners = ["assurance-owner", "documentation-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-DST-060"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:55:25Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Verify executive positioning against shipped behavior

## Independence

Expected facts come from current source, released and candidate CLI help,
formal lifecycle records, packaged skill contracts, and existing focused tests.
Verification must not infer product capability from the rewritten marketing
prose, the attached proposal, a model's general capabilities, or roadmap status.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-DST-060` | source/record comparison, focused regression, CLI inspection, link and manual narrative review | README facts, executive current/roadmap/vision split, scope and security boundary, real demo lifecycle, exact-commit wording, scale and multi-agent claims | every present-tense capability matches shipped behavior; planned and visionary claims are labeled; no executable or formal state changes |

## Acceptance scenarios

- The README and executive brief state that the harness is not an agent sandbox,
  permission system, or standalone enforcement boundary.
- Selected-scope language states the complete-change-evidence dependency and
  the role of external runtime/hosting controls.
- The current skill is described as read-only, single-agent, and delegation
  disabled; multi-agent orchestration is labeled roadmap or vision.
- The executive demo uses actual lifecycle ordering and canonical restitution
  headings, and a `ready` VREC is not described as verified.
- Exact Git commit language does not become an unqualified executable/binary
  identity claim.
- Enterprise-scale operation is not claimed as demonstrated.
- Current installation, version, integration-package, command, Explorer, and
  link facts remain accurate.

## Property and invariant tests

- `README.md` remains at most 200 lines with the current nine level-two
  headings and balanced Markdown fences.
- Every local link resolves and all repository-owned images remain valid PNGs.
- `VALUE_PROPOSAL.md` contains no placeholder, unsafe HTML, credential, or
  unqualified current multi-agent capability claim.
- Formal artifacts outside this new packet, managed files, package metadata,
  CLI code, workflows, and historical evidence remain byte-for-byte unchanged.

## Static and architecture checks

- Run the focused public-onboarding and value-proposition tests.
- Inspect candidate and released `harnessctl --help` and `check --help` output.
- Run formal graph validation, release-distribution validation, CLI help,
  released-evaluator `doctor`, and start/review preflight at the required stage.
- Run the complete unit suite and compare failures/skips with a clean-main
  baseline when the local platform has known line-ending failures.
- Review the final diff against `SPEC-EVP-001` and the exact execution scope.

## Security and privacy checks

Confirm the documents do not imply that hashes, lifecycle state, or an agent
skill physically constrain a privileged process. Confirm no private external
state, unsafe markup, executable snippet, or copied secret is introduced.

## Performance and resilience checks

No runtime performance changes. Rehearse the talk track against a prepared
disposable repository or reviewed fixture and confirm the primary flow fits the
target duration without depending on a live agent completing on schedule.

## Manual assessments

- Review each material claim as **current**, **roadmap**, or **vision**.
- Confirm the story remains persuasive after qualifiers are applied.
- Confirm “human-at-the-decision-point” does not imply that every organization
  must use separate people or that automation exercised a decision right.
- Confirm the Q&A answers challenge complexity, enforcement, scale,
  multi-agent maturity, compliance, and malicious-author boundaries directly.

## Evidence retention

Retain the claim audit, attachment-to-output disposition, exact commands and
results, test counts, CLI/version observations, link and Markdown checks,
README information budget, demo rehearsal observation, residual uncertainty,
and every unperformed lifecycle, Git, release, publication, deployment, or
external action at
`docs/engineering/harness-distribution/evidence/WO-EVP-001-verification.md`.

## Residual uncertainty

Static checks cannot prove executive comprehension, adoption, organizational
scale, or that external agent runtimes and hosting controls are configured
correctly. Future agentic-execution work may make currently prospective claims
true; the documents must be reviewed again when that state changes.
