+++
id = "REQ-PLG-016"
type = "requirement"
title = "Use plugin skills without duplicate repository copies"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-14"
updated = "2026-09-14"

statement = "WHEN a project switches to plugin skills, THE INSTALLER SHALL replace the named disposable skill copies through the existing provider choice while preserving unrelated owner files."
verification_method = ["test", "inspection"]
priority = "must"
source = "Owner-directed KISS amendment, 2026-09-14; existing PR #416 identifier"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Use plugin skills without duplicate repository copies

## In plain words

The plugin supplies the skills. Old generated copies are disposable, including
edits inside those copies. Unrelated user files are kept.

## Acceptance

Follow SPEC-PLG-021: check that replacement skills exist before deleting named old
directories, reject a path that would escape the target, and allow an interrupted
operation to be rerun. Store the portable provider choice, not a local plugin path,
signature or ownership receipt. An ordinary clone can run doctor and upgrade
without a plugin installed; invoking plugin skills requires the host to have it.
No second conflict-resolution design or DEC-PLG-004 decision is needed.
