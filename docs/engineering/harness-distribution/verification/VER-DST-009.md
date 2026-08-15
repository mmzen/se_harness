+++
id = "VER-DST-009"
type = "verification"
title = "Verify synchronized validation and inspection documentation"
status = "approved"
owners = ["quality-owner", "documentation-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
verifies = ["REQ-DST-034"]
+++

# Verification Contract: Verify synchronized validation and inspection documentation

## Independence

Derive expected command inventory from the approved requirement and compare command facts independently to `se_harness.cli.build_parser()`, validator results, inspection human and JSON fixtures, managed policy, and direct Markdown inspection. Do not accept documentation merely because its focused test was changed to match it. Compare current definitions to Git history rather than modifying historical evidence.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-034` | static contract comparison | `REQ-DST-025`, `SPEC-DST-007`, `VER-DST-007`, README, parser, and focused onboarding test | all current surfaces use the six-command inventory and distinguish `validate`, `inspect`, and `dashboard` |
| `REQ-DST-034` | validator behavior tests and policy comparison | valid graph, invalid graph, warning-only graph, JSON findings, `QUALITY_GATES.md` root/canonical pair | planes, severity, pass/fail, and no-score semantics agree |
| `REQ-DST-034` | inspection behavior tests and documentation comparison | valid and invalid repositories, supported and unsupported findings, human/JSON output, no-write check | inspection remains derived and non-gating; suggestions are bounded, non-executable, `automatic = false`, and authority-neutral |
| `REQ-DST-034` | progressive-document walkthrough | overview, phasing, installation/upgrade, and lineage-example notes | each document carries only the depth appropriate to its audience and all four include the necessary inspection distinction |
| `REQ-DST-034` | protected-history inspection | changed-path inventory and Git diff | no retained evidence, VREC, RLS, release contract, or released-candidate fact is modified |

## Acceptance scenarios

### Six-command public surface

Given the current CLI exposes `inspect`, when the root README, active contract, and focused onboarding checks are compared, then all identify the same six ordinary human-facing repository commands and still exclude agent-only lifecycle syntax.

### Gate versus report

Given an invalid formal graph, when `validate` and `inspect` are run against the same fixture, then validation preserves its blocking exit behavior while successful inspection reports `valid = false`, retains findings, exits zero, and claims no approval.

### Bounded suggestion

Given a supported lifecycle queue or derived warning, when inspection emits a suggestion, then its action class and accountable role come from the closed catalog, `automatic` is false, and no executable command or target lifecycle state appears.

### Unsupported observation

Given a validator diagnostic, informational observation, or unknown finding, when inspection reports it, then the finding remains visible and no guessed suggestion is created.

### Historical evidence

Given `WO-DOC-008` evidence describes the earlier five-command candidate, when the correction is implemented, then that evidence and its commit-bound records remain byte-for-byte untouched.

## Property and invariant tests

- Extract fenced root `harnessctl` subcommands and compare them to the exact approved six-command allowlist.
- Assert agent-only commands remain absent from root fenced examples.
- Assert required note files mention `inspect` in the defined phase or boundary and keep working relative links.
- Re-run validator and inspection determinism, no-write, invalid-graph, suggestion-catalog, escaping, package-data, and root/canonical parity tests affected by documentation assertions.
- Assert no health score, implicit eligibility, automatic remediation, approval, verification, or release claim is introduced.

## Static and architecture checks

Confirm the work order legitimately omits architecture: no active architecture directly addresses `REQ-DST-034`, and the correction changes no component boundary, responsibility direction, public data protocol, dependency, or significant alternative. Confirm the root README remains within its existing line and heading budgets and detailed policy is not copied into it.

## Security and privacy checks

Scan changed examples for secrets, absolute repository URLs, executable suggestion text, unsafe Markdown links, and authority claims derived from untrusted repository content.

## Performance and resilience checks

Not applicable to runtime performance. Run the affected documentation, CLI, validator, inspection, installer, managed-integrity, and package tests plus the complete supported-runtime suite to detect accidental behavior changes.

## Manual assessments

- A 4/10 reader can explain that inspection helps locate attention but cannot decide.
- A 6/10 reader can distinguish validation planes, gate exit behavior, inspection reporting, and dashboard visualization.
- A 7/10 reader can follow the practical command sequence and identify the accountable next decision.
- Review duplication so the command reference owns detail and other notes cross-reference rather than reproduce catalogs.

## Evidence retention

Retain command inventory, changed-path list, definition comparison, focused and complete test results, formal validation, doctor, start and review preflight, inspect output, dashboard generation, root/canonical parity, managed-upgrade idempotence where applicable, link checks, reader assessment, historical-path protection, and diff hygiene in `docs/engineering/harness-distribution/evidence/WO-DOC-012-verification.md`.

## Residual uncertainty

Automated checks can prove command spelling and required distinctions but cannot fully prove reader comprehension. Retain the manual audience assessment and flag any ambiguous behavior instead of documenting an assumption.
