[harness]
schema_version = 2
tool_version = "{{HARNESS_VERSION}}"
installed_at = "{{INSTALL_DATE}}"
project_name = "{{PROJECT_NAME}}"
artifact_root = "docs/engineering"
dashboard_output = "target/harness-dashboard"

[revision_provenance]
require_full_commit = true
require_clean_worktree = true
required_for_verified_work = true
required_for_release = true
verification_record_status = "ready"
release_record_status = "ready"

[risk]
acceptance_level = 1
scale = "5x5"
release_requires_disposition = true
