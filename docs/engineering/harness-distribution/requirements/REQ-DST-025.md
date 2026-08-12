+++
id = "REQ-DST-025"
type = "requirement"
title = "Human operational command surface"
status = "approved"
owners = ["product-owner", "documentation-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN the root README demonstrates routine repository operation, THE SYSTEM SHALL limit explicit harness subcommand examples to init, adopt, doctor, validate, and dashboard while describing agent-only mechanics without requiring humans to learn their syntax."
verification_method = "automated-static-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Human operational command surface

## Rationale

Humans need a small, memorable surface for installing or adopting the harness and inspecting its health, graph, and Explorer. Commands such as `preflight`, `scaffold-domain`, `create-artifact`, `capture-verification`, `prepare-release`, and `identity` are normally coding-agent or advanced-operator mechanics and currently distract from user value.

## Preconditions and trigger

The README includes fenced examples for normal target-repository operation.

## Required response

The examples explain:

- `init`: install into an absent or empty repository;
- `adopt`: preserve and introduce the harness into an existing repository;
- `doctor`: inspect installed-harness integrity;
- `validate`: inspect the formal engineering graph;
- `dashboard`: generate the read-only Harness Explorer.

Package installation, virtual-environment activation, and `harnessctl --version` are setup checks rather than repository subcommands and may remain.

The README states in plain language that the coding agent performs preflight, formal artifact drafting, scoped implementation, repository checks, evidence retention, and ready-record preparation. It does not include agent-only command syntax.

## Failure and boundary behavior

Removing syntax must not make agent operation magical or imply that the agent can approve its own work. The detailed command reference remains linked and explicitly classifies actor, side effects, and authority.

## Constraints

- Do not present `upgrade --apply` as automatic or agent-authorized mutation.
- Do not put tool commands inside quoted user requests.
- Keep `doctor` and `validate` visibly distinct.

## Acceptance examples

### Example: human quick start

**Given** a repository owner reads the start section,

**When** they inspect its harness command blocks,

**Then** they see only the five ordinary human-facing subcommands.

### Example: agent execution boundary

**Given** the reader wants to know what the coding agent does,

**When** they read the responsibility summary,

**Then** they understand the agent lifecycle without needing to copy a `preflight` or provenance-preparation command.

## Open decisions

The implementation may combine commands into one or more short blocks if actor and target-path meaning remain clear.
