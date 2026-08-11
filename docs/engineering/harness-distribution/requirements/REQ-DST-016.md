+++
id = "REQ-DST-016"
type = "requirement"
title = "Create domains and draft artifacts safely"
status = "implemented"
owners = ["product-owner", "technical-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a user or coding agent scaffolds an engineering domain or creates an artifact, THE SYSTEM SHALL route the requested content to the canonical location using conflict-safe, traversal-safe, non-authorizing writes."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Create domains and draft artifacts safely

## Rationale

Documentation alone does not reliably produce a consistent repository. Coding agents should be able to ask the harness for the correct location and template without manually reconstructing the layout, while the command must not invent product facts, approvals, or governance authority.

## Required response

- Provide a command that safely scaffolds a named domain and its canonical artifact organization.
- Provide a command that creates one artifact from the canonical template at the canonical domain-local path.
- Validate the requested domain slug, artifact type, stable identifier, type prefix, destination, parent chain, and existing-file conflicts before writing.
- Support a dry-run plan that performs the same resolution and safety checks without changing the repository.
- Create artifacts exclusively as incomplete drafts that require accountable completion and normal validation.
- Fail without partial writes when any requested destination is unsafe or conflicts with repository content.

## Failure and boundary behavior

Reject absolute paths, traversal, path separators in slugs or identifiers, invalid identifiers, type-prefix mismatches, reserved domains, symlink escapes, non-directory parents, and existing destinations. Never overwrite, merge, approve, validate, or transition an artifact as a side effect of creation.

The domain index is repository-owned content. Scaffolding may seed it only when absent and must never replace an existing domain index.

## Constraints

- Reuse the canonical installed artifact templates rather than maintaining a second template family.
- Preserve the installer ownership model: dynamically created domain content is not a managed distribution file.
- Recreate a missing canonical parent directory on demand because Git does not retain empty directories.
- Keep command behavior deterministic and locally testable without network access.

## Acceptance examples

`harnessctl scaffold-domain . --domain simulation --title "Simulation"` plans and creates the canonical domain structure without product artifacts or approval claims.

`harnessctl create-artifact . --domain simulation --type requirement --id REQ-MOK-012` exclusively creates `docs/engineering/simulation/requirements/REQ-MOK-012.md` from the requirement template in `draft` state and reports that accountable fields still require completion.

## Open decisions

The packet proposes initial flags, supported types, validation rules, and dry-run behavior. User-interface refinements that change these semantics require accountable review.
