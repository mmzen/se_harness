+++
id = "REQ-DST-056"
type = "requirement"
title = "Install consumer GitHub CI additively"
status = "implemented"
owners = ["product-owner", "engineering-owner", "security-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN init or adopt targets a GitHub repository with zero or more existing workflows, THE SYSTEM SHALL install one dedicated managed SE Harness workflow without modifying unrelated workflow files or implying that external merge enforcement has been configured."
verification_method = "automated-installation-and-workflow-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Install consumer GitHub CI additively

## Rationale

GitHub discovers every workflow below `.github/workflows/`; SE Harness does not need to parse or splice itself into arbitrary repository-owned YAML. A dedicated file gives the installer one deterministic ownership boundary and leaves application build, test, deployment, and release workflows under repository control.

## Preconditions and trigger

The user runs `harnessctl init` for an empty repository or `harnessctl adopt` for an existing repository. The target may contain no `.github` directory, an empty workflow directory, or any number of unrelated workflow files.

## Required response

- Plan and install `.github/workflows/engineering-harness.yml` as the one standard managed consumer workflow.
- Create missing parent directories safely.
- Preserve every unrelated workflow byte-for-byte.
- Declare GitHub `pull_request` and `push` triggers so GitHub discovers and executes the workflow independently of other CI.
- Explain that making the resulting check mandatory requires repository-owner configuration of GitHub rulesets or branch protection.

## Failure and boundary behavior

If the exact destination already contains unknown, customized, symlinked, or conflicting content, installation fails before any write. The system does not rename, merge, absorb, or overwrite that workflow and does not infer an alternative CI topology.

## Constraints

- The dedicated workflow is part of the single standard installation, not a selectable profile.
- No GitHub credential, ruleset mutation, required-check mutation, or external API call is implied by repository installation.
- Existing workflows may run in parallel; ordering or deployment dependency remains repository policy.

## Acceptance examples

### Example: repository already has CI

**Given** a repository containing `build.yml` and `deploy.yml`,

**When** the repository is adopted,

**Then** the dedicated SE Harness workflow is added and both existing files remain unchanged.

### Example: repository has no CI

**Given** a repository without `.github/workflows`,

**When** the repository is adopted,

**Then** the required directories and dedicated workflow are created safely.

### Example: destination conflict

**Given** an untracked repository-owned `engineering-harness.yml`,

**When** adoption is planned,

**Then** the conflict is reported and no installation file is written.

## Open decisions

None when approved.
