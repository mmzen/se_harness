+++
id = "VER-RLS-035"
type = "verification"
title = "Verify complete public 0.22.0 delivery"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-02"

[relations]
verifies = ["REQ-RLO-019", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T22:07:58Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package and required verification\" to the reviewed evaluator 0.22.0 / plugin 0.2.5 package: REL-SEH-034, WO-RLS-034/035/036 and VER-RLS-033/034/035. This confirms required commit-bound verification and authorizes bounded preparation, qualification, review pushes/PRs and listed delivery work under the retained request \"Merged. Next: prepare and execute the release\". Human verification of exact results, the exact release-record decision and merge remain separate. Repository adoption and provider-setting changes are excluded. Selected released 0.21.0 governs; Codex applies the recorded human decision. Reviewed SHA-256 642b5127238f8dcd5b792893438b3223b8274fe2447b2cda6e3070b96c200260; transition-input SHA-256 642b5127238f8dcd5b792893438b3223b8274fe2447b2cda6e3070b96c200260. Only confirmed assurance fields were added."
+++

# Verify complete public 0.22.0 delivery

## Independence

Expected identities derive from RLS-SEH-032, the verified plugin package and the
reviewed delivery plan. Read GitHub, PyPI, marketplace and Pages independently.
Matching local documents alone do not prove public availability.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-RLO-019 | test, inspection | Public archives and clean install | Both archive digests match the RLS; installed version, evaluator and resource identities are exact. |
| REQ-RLO-019 | demonstration, inspection | Both public fresh and 0.2.4-to-0.2.5 update routes | Record the public commit, host/version, route, installed content hashes and selected resources; compare them with the qualified package. Required native checks pass or remain explicitly unresolved. |
| REQ-RLO-019 | inspection, test | Current source/assembled documentation and Pages | Claims match actual availability and platform limits; links resolve in their proper context; demo provenance identifies the selected governance input. |
| REQ-RLO-020 | test, inspection | Final plan, delivery checker and marker readbacks | All five surfaces are satisfied, RLS is released, and latest/last equal the authorized tag/candidate. No pending or deferred item is reported complete. |

## Procedure and evidence

Use existing public installation/update procedures in disposable profiles.
Preserve real profiles and credentials. Run existing documentation/link tests
after current-claim edits. Capture VREC-PLG-033 for that exact commit and publish
its review before requesting human verification. Preserve later merged-source
and public observations separately from the frozen verification inputs.

Retain concise observed identities, exact commands, failures and evidence hashes
in evidence/WO-RLS-036/. Version the existing plan and observations rather than
rewriting bound bytes. Run scripts/check_release_delivery.py against their exact
digest and evidence root. Retain unavailable checks as gaps. Older accepted
Claude/desktop omissions do not satisfy this release's criteria.
