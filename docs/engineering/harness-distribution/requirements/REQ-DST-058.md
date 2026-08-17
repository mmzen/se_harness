+++
id = "REQ-DST-058"
type = "requirement"
title = "Run consumer governance semantics from the released package"
status = "implemented"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN the managed consumer workflow selects authorized work or assesses repository state, THE SYSTEM SHALL execute work-order selection, preflight, installation diagnosis, graph validation, and Explorer generation from the isolated released package while treating checkout content only as untrusted input and retained evidence."
verification_method = "automated-adversarial-integration-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Run consumer governance semantics from the released package

## Rationale

Installing a trusted package is insufficient if CI then executes the repository's copies of validator, selector, or dashboard scripts as the assessment authority. Package-owned entry points make the runtime boundary meaningful and keep consumer behavior consistent with the requested release.

## Preconditions and trigger

The exact released evaluator has passed identity checks and the checkout is available as the repository under assessment.

## Required response

- Parse the GitHub pull-request event and select exactly one standalone `Harness-Work-Order: WO-...` declaration through package-owned logic.
- Run review preflight for that work order through the isolated evaluator.
- Run `doctor`, formal graph validation, and deterministic Explorer generation through package-owned command paths.
- Preserve exit codes, bounded diagnostics, validation planes, lifecycle authority, and dashboard non-authority.
- Leave application-specific commands such as `cargo test`, build, deployment, and release in repository-owned CI.

## Failure and boundary behavior

A missing or ambiguous work-order declaration, damaged managed installation, invalid graph, package/check-out semantic mismatch, or failed generation remains a failed or explicitly observational harness result according to the existing command contract. CI may not repair artifacts, approve work, transition records, configure hosting policy, or reinterpret project test results.

## Constraints

- The consumer workflow does not directly execute `scripts/select_harness_work_order.py`, `scripts/validate_engineering_artifacts.py`, or `scripts/generate_harness_dashboard.py` from the checkout.
- Installed managed scripts may remain portable repository tools for local operation and integrity comparison, but they are not the executable CI oracle.
- Repository paths, events, artifacts, Markdown, and configuration remain untrusted inputs.

## Acceptance examples

### Example: repository script is modified

**Given** a pull request changes a managed validator script,

**When** the released evaluator runs CI,

**Then** managed drift or semantic disagreement is reported without executing that changed script as the authority.

### Example: application tests

**Given** the repository has a Rust test workflow,

**When** SE Harness CI runs,

**Then** governance validation and Rust tests remain separate checks whose required status is external repository policy.

## Open decisions

None when approved.
