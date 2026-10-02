+++
id = "VER-RLS-032"
type = "verification"
title = "Verify public 0.21.0 and plugin 0.2.4 delivery"
status = "approved"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[relations]
verifies = ["REQ-RLO-019", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T19:53:49Z"
decided_by = "engineering-owner"
reason = "Human mmzen: Approve package and required verification. Approves REL-SEH-033, WO-RLS-031/032/033 and VER-RLS-030/031/032, required commit-bound verification, plugin 0.2.4, ordinary release-review branch push/draft PR and read-only CI rehearsals. Existing v0.21.0 publication authorization is retained. Final-candidate verification, exact RLS decision and unresolved desktop evidence remain separate. Reviewed SHA256 4afb0c1292f45d5b1ec58638ae411a2ae6c1258e8e5154e7c6402e473721e7a3; transition-input SHA256 4afb0c1292f45d5b1ec58638ae411a2ae6c1258e8e5154e7c6402e473721e7a3. Only confirmed work-order assurance metadata was added. Codex applies the human decision using the selected evaluator role-label encoding; mmzen is the decision-maker."
+++

# Verify public 0.21.0 and plugin 0.2.4 delivery

## Independence

Expected public identities derive from the released RLS, qualified 0.2.4 package
and reviewed delivery plan. Use independent reads of GitHub, PyPI, marketplace
and Pages. SPEC-RLO-006 controls closeout; agreement between two local documents
does not prove availability.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-RLO-019 | demonstration, inspection | Public wheel/sdist and install observations | Public digests equal the RLS binding; a clean public evaluator install proves its exact identity. |
| REQ-RLO-019 | demonstration, test | Fresh and 0.2.3-to-0.2.4 public routes for Codex and Claude Code | Actual public marketplace commit, installed tree and bundled wheel match the qualified package. Native startup, activation, compaction and resume observations identify actual host/session/resource inputs. Missing desktop criteria are not relabelled as passes. |
| REQ-RLO-019 | inspection | Current README, install/package guidance, catalog links and Pages readback | Current versions, routes, provenance and platform limits match observed identities in source and assembled contexts. Historical evidence remains unchanged. |
| REQ-RLO-020 | test, inspection | Existing delivery checker, bound final plan, marker readback | Every surface has matching evidence and the RLS is released before overall complete is reported. Pending/failed/deferred items remain visible. Latest/last targets match separately authorized actions. |

## Execution and evidence

Use existing public marketplace fresh-install/update procedures in disposable
profiles. Record the starting 0.2.3 identity, public 0.2.4 commit, commands,
installed hashes, host versions and native traces. A local package check is not
public-route evidence. Keep credentials and real user profiles unchanged.

Review current documentation against those observations; preserve earlier receipts
and history. Run existing documentation/link tests and the delivery checker with
the exact plan digest. Read merged public documentation back before closeout.
Observe deployed Pages provenance and release markers independently.

Retain evidence under evidence/WO-RLS-033/. Capture a commit-bound VREC for the
bounded owner-documentation changes. Obtain human verification before integration.
Keep later public readbacks as subsequent observations; do not rewrite the bound
VREC. Use staged plan versions and preserve their observation bindings.

## Residual uncertainty

No public 0.21.0 or 0.2.4 result is claimed by this draft. Inability to run a
required host check blocks that claim and complete delivery; it supplies no waiver.
Repository adoption and live-profile installation remain separate work.
