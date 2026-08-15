+++
id = "VER-DST-007"
type = "verification"
title = "Verify concise public README and layered reference notes"
status = "approved"
owners = ["quality-owner", "documentation-owner"]
created = "2026-08-12"
updated = "2026-08-15"

[relations]
verifies = ["REQ-DST-024", "REQ-DST-025", "REQ-DST-026", "REQ-DST-027", "REQ-DST-028"]
+++

# Verification Contract: Verify concise public README and layered reference notes

## Independence

Derive assertions from the five requirements and `SPEC-DST-007`, not from the implementation's chosen wording. Compare command facts to `se_harness.cli.build_parser()`, version facts to package metadata, authority claims to managed policy, self-hosting facts to current controls, and public structure to direct static inspection. Treat prior README content as migration input rather than expected output.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-DST-024` | deterministic line/heading count and 6/10 reader review | root has at most 200 lines and nine level-two sections while retaining all essential entry-point responsibilities |
| `REQ-DST-025` | fenced-command extraction and actor review | only the six allowed routine harness subcommands appear in root examples; `validate`, `inspect`, and `dashboard` remain distinct; agent mechanics remain understandable without syntax |
| `REQ-DST-026` | note inventory, content ownership, CLI comparison, and link traversal | all useful relocated detail has one expertise-labeled owner; local links resolve; managed policy is not duplicated as note authority |
| `REQ-DST-027` | installation and upgrade scenario walkthrough | fresh install remains usable and package versus repository upgrade is explicit, safe, and owner-controlled |
| `REQ-DST-028` | scenario, graph, responsibility, Explorer, limitations, and contributor-route review | shortening preserves the product value and all material authority/provenance boundaries |

## Automated checks

- Count `README.md` physical lines and `## ` headings; reject more than 200 lines or nine level-two sections.
- Assert root target expertise, project links, Python requirement, virtual environment, PyPI install, exact synchronized package version, `init`, `adopt`, `doctor`, `validate`, `inspect`, and `dashboard`.
- Extract fenced blocks and reject agent-only harness subcommands: `preflight`, `upgrade`, `scaffold-domain`, `create-artifact`, `identity`, `capture-verification`, and `prepare-release`.
- Assert `doctor`, `validate`, `inspect`, and `dashboard` have distinct plain-language outcomes, including that successful inspection-report production is not a passed validation gate.
- Assert exactly one Mermaid block, no more than nine conceptual node declarations, human verification and release decision shapes, Explorer observation, exact-commit meaning, prose fallback, and no unique color-only distinction.
- Assert the responsibility boundary names human owners, coding agent, and repository policy or hosting control.
- Assert both known 0.2.2 limitations remain and no prose claims they were corrected.
- Assert the three new note paths, exact 5/10, 7/10, and 8/10 labels, required topic ownership, and notes-index routes.
- Compare the command-reference inventory exactly to current CLI parser choices and exercise help for every subcommand.
- Assert all local Markdown links resolve and public notes contain no placeholders, mojibake, unsafe control characters, unbalanced fences, inline script, or obsolete consumer-repository claims.
- Assert root headings for full artifact model, command reference, installed layout, full commit-bound procedure, pull-request bootstrap, safe-upgrade procedure, and distribution development no longer exist as duplicated top-level manuals.
- Run focused public/documentation tests and the complete standard-library unit suite.
- Run formal validation with zero errors, `doctor`, phase-appropriate preflight after approval, deterministic dashboard generation, `git diff --check`, and protected-path comparison.

## Manual assessments

- **Public scan:** a 6/10 reader finds purpose, installation, start, inspection, authority, limitations, and next links without searching a 500-line page.
- **Human command surface:** a repository owner can distinguish the six ordinary operations and is not asked to execute agent-only lifecycle commands.
- **Agent transparency:** removing syntax does not hide that the agent checks authorization, works within scope, retains evidence, and only prepares proposals.
- **Upgrade safety:** a current user cannot reasonably infer that upgrading the Python package updates repository-managed content.
- **Relocation completeness:** each removed block is mapped to one note, existing owner, or explicit retirement rationale.
- **Authority:** explanatory notes consistently route normative questions to managed policy.
- **Contributor route:** source/self-hosting details remain reachable without dominating user onboarding.

## Acceptance scenarios

### Scenario: new repository owner

Given a reader starts at the root README, when they install the package and choose a new or existing repository, then they can reach `init` or `adopt`, inspect with `doctor`, `validate`, `inspect`, and `dashboard`, distinguish a gate from a derived report, and understand who retains approval.

### Scenario: coding agent mechanics stay behind the interface

Given the agent is expected to preflight and prepare evidence, when a human reads the root, then those responsibilities are visible but command syntax is delegated to the linked reference and workflow material.

### Scenario: existing installation

Given a repository was initialized by an older release, when its owner updates the package, then the documentation clearly requires a separate repository upgrade plan and explicit apply decision.

### Scenario: advanced contributor

Given a contributor needs source checks and self-hosting identities, when they follow the contributor route, then current three-plane detail is available without being copied into the root.

## Pass criteria

All automated and manual checks pass; formal validation has zero errors; only classified pre-existing warnings remain; root line and command budgets hold; no useful detail is orphaned; authority and provenance remain truthful; protected behavior and managed-policy surfaces are unchanged; and evidence records every relocation or retirement decision.

## Evidence retention

For the original concise-root candidate, retain commands, versions, root line/heading counts, fenced-command inventory, content-disposition ledger, note expertise inventory, CLI-reference comparison, link results, graph review, reader assessments, focused and complete test counts, validator and doctor results, preflight manifest, dashboard snapshot, warning classification, changed/protected paths, deviations, and residual risks in `docs/engineering/harness-distribution/evidence/WO-DOC-008-verification.md`. The current six-command revision is verified separately by `VER-DST-009` and retained under `WO-DOC-012`; do not rewrite the original evidence.

## Residual uncertainty

Scanability and persuasion are partly qualitative. Markdown renderers differ, external public state can change, and line-count constraints can encourage over-compression. Manual review must reject a technically short README that becomes cryptic or unsafe.
