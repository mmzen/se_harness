+++
id = "WO-DST-002"
type = "work_order"
title = "Install the standard harness into its distribution repository"
status = "implemented"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-001", "REQ-DST-002", "REQ-DST-003", "REQ-DST-004", "REQ-DST-005", "REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]
+++

# Work Order

Retain the standard SE Harness 0.2.0 installation in its own distribution repository: schema-2 configuration, managed-content lock, GitHub Actions workflow, bounded `AGENTS.md` and `.gitignore` integrations, engineering workflow documents, and the complete artifact-template set.

The accountable repository owner explicitly authorized this local commit on 2026-08-11 by stating that the staged files were part of the new harness installation and instructing the agent to commit them.

The work order excludes executable source changes, canonical distribution-template changes, commit rewriting, tags, pushes, release transitions, and publication. Commit identity is discovered from Git history after creation rather than self-recorded here.
