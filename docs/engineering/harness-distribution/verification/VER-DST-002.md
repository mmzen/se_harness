+++
id = "VER-DST-002"
type = "verification"
title = "Verify cross-agent instructions and repository context"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-DST-007", "REQ-DST-008"]
+++

# Verification Contract

Automated tests shall prove that init creates `AGENTS.md`, `CLAUDE.md`, and repository context; Claude imports the shared contract; adoption preserves pre-existing content in both shared-root files and pre-existing context; malformed Claude markers fail closed; upgrade adds the new paths to an older installation; customized Claude instructions and repository context remain unchanged; deletion of an accounted seed is not reversed; doctor rejects a missing or invalid Claude import and a missing repository-context file; lock metadata distinguishes fragment and seed ownership; and package metadata contains every new template source.

The complete artifact graph, distribution unit suite, CLI help smoke test, and initialized/adopted target validation must pass.
