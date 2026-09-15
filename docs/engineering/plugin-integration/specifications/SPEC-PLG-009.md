+++
id = "SPEC-PLG-009"
type = "specification"
title = "Connect and maintain projects through the existing setup route"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-14"
updated = "2026-09-14"
contract = "Connect and maintain a project through the existing setup and installer, with disposable skill replacement and explicit version choice."

[relations]
specifies = ["REQ-PLG-015", "REQ-PLG-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T22:05:14Z"
decided_by = "technical-owner"
reason = "The owner reviewed and approved completion of the KISS backlog amendment and explicitly said \"you can start WO-PLG-009 and WO-PLG-016\" on 2026-09-15. This accepts the selected rewritten definition chain and authorizes its bounded routine execution, checks and evidence under the installed evaluator. No result-specific assurance, merge, release or live host/project installation is inferred."
+++

# Connect and maintain projects through the existing setup route

## Design

Extend the common setup instructions and their reference pages. Reuse setup.py and
the installer delivered by WO-PLG-020/021 and the later KISS changes. Add code only
for an observed gap inside the stated scope; do not introduce a connection service.

- **PLG-CON-001:** Ask only for missing target or operation choices. Use the selected
  compatible checker and its actual CLI for init, provider selection and explicit
  upgrade. Never silently adopt candidate source as the target's governing release.
- **PLG-CON-002:** For an existing project, explain once that the named generated
  skills will be replaced, then use the existing replacement operation. Edits
  inside those copies do not become ownership conflicts. Unrelated content and
  out-of-target writes remain protected by SPEC-PLG-021.
- **PLG-CON-003:** Repair with the same setup command and one private environment.
  Choose the wheel compatible with the project; do not automatically move its
  version on plugin update. Report actual setup/doctor failures and the retry.
- **PLG-CON-004:** Run the normal explicit check after the requested operation.
  Record actual checker origin/version once in ordinary evidence. Do not add
  session hooks, tool interception, activation receipts or host-version allowlists.
- **PLG-CON-005:** Keep the provider setting portable across clones. Check native
  skill discovery through the installation walkthrough in WO-PLG-016; do not
  duplicate that host exercise in every installer test.

## Applicability and simpler choice

This replaces the unmerged SPEC-PLG-009 and absorbs useful SPEC-PLG-013 maintenance
outcomes. A new setup engine, alternate repair environment and ownership review
protocol would duplicate working mechanisms. REQ-PLG-015 covers connection and
version-preserving maintenance; REQ-PLG-016 covers disposable replacement and
portability. Existing safety tests remain useful; the retired synthetic scenarios
are not acceptance conditions. Public release/adoption remains a later real action.
