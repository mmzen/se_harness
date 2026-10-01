+++
id = "VER-RLS-029"
type = "verification"
title = "Verify public plugin 0.2.3 and the 0.20.1 delivery claims"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-10-01"

[relations]
verifies = ["REQ-RLO-019", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T05:48:10Z"
decided_by = "engineering-owner"
reason = "Human mmzen approved the reviewed package and confirmed: Yes\u2014approve both 028 and 029 pairs. Approves WO-RLS-028, VER-RLS-028, WO-RLS-029 and VER-RLS-029, required commit-bound verification, the stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and the existing 0.19.0 engineering-owner encoding retaining mmzen as the human decision-maker. Reviewed SHA256 6f3c1cf5242699c0588bc5c80b3fb7e09defaeec6c7724829b1a994888838712; transition input SHA256 6f3c1cf5242699c0588bc5c80b3fb7e09defaeec6c7724829b1a994888838712. Only confirmed assurance metadata was added to work orders. Codex applies the matching decision. Human verification, merges, release, publication, release markers and adoption remain separate."
+++

# Verify public plugin 0.2.3 and the 0.20.1 delivery claims

## Independence and inputs

Expected identities come from released RLS-SEH-030, the package accepted under
VER-RLS-028, its exact authorized marketplace commit and the reviewed delivery
plan. Never replace an expected value with an unexpected public result.
Use current main's confirmed released evaluator; repository adoption is separate.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence and pass condition |
| --- | --- | --- |
| REQ-RLO-019 | demonstration, inspection | Public fresh installation and public 0.2.2-to-0.2.3 update on both Windows CLIs resolve to the reviewed marketplace commit. Installed manifests, common content and evaluator archive/payload identities match the accepted package. Current documentation and links agree with those observations. |
| REQ-RLO-020 | test, inspection | The existing closeout checker reports complete only with released RLS-SEH-030 and matching observations for all five surfaces. Missing marketplace evidence and a wrong revision each remain incomplete. |

## Public route checks

After separately authorized marketplace publication, read back its exact Git
commit and compare the complete tree with the qualified distribution. Test
fresh installation and update from the preserved public 0.2.2 package through
https://github.com/mmzen/se_harness#plugin-marketplace in disposable Windows
Codex CLI and Claude Code profiles. A local directory cannot substitute for
the public route. Record host versions, starting revision, installation/update
commands, loaded path, installed file inventory, evaluator identity and time.

Check native startup, manual compaction and resume with the actual public
content. Earlier native evidence may be reused only with a retained exact-input
comparison explaining what still applies. Authentication failures and missing
host access remain gaps. Do not claim desktop or automatic compaction support.

## Documentation and final closeout

Review current main's README, install/publication/release guidance and domain
indexes against the actual public versions. Keep 0.20.1 maintenance behavior
separate from unreleased minimal-layout work. Check links in their source
context. Read the packaged guidance from the public tree; a needed package
change returns to new qualification, not an edit to published bytes.

Run the existing relevant documentation tests. Capture the clean documentation
and public-observation candidate under WO-RLS-029. Its VREC requires a separate
human decision. After separately authorized documentation integration, retain
an append-only public readback. Do not alter the earlier bound candidate evidence.

Use scripts/check_release_delivery.py with the exact reviewed plan, observations
and evidence root. Require matching evaluator publication/public-install results,
marketplace results for both hosts, current documentation, deployed Pages
provenance and the separately authorized latest/last targets. Retain the
checker's result and the two negative cases in the matrix. All five surfaces
must pass before reporting complete delivery; pending is not success.

## Evidence retention and limits

Use evidence/WO-RLS-029/ in this domain. Retain command arrays, exact commits,
archive/content digests, native transcripts, times, failed attempts, plan versions
and applicability of reused evidence. Generated VRECs use verification-records/
and their evaluator companions use evidence/. Final integration receipts stay
outside the evidence already bound to a VREC. Transport of those unchanged
receipts alone does not create another assurance loop. No credentials, real
profiles, environments or disposable repository trees enter the repository.

This establishes observed delivery at the recorded times. It does not perform
publication, authorize marker changes, adopt 0.20.1 or finish the successor's
independent qualification.
