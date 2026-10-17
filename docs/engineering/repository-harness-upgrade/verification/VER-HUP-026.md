+++
id = "VER-HUP-026"
type = "verification"
title = "Verify repository adoption of public 0.23.0"
status = "approved"
owners = ["mmzen"]
created = "2026-10-17"
updated = "2026-10-17"

[relations]
verifies = ["REQ-REB-027", "REQ-IAR-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-17T09:49:41Z"
decided_by = "mmzen"
reason = "mmzen approved implementation and review publication for repository/CI adoption of public 0.23.0, development source 0.23.1, the named documentation/test changes, required commit-bound verification, review pushes/draft PR codex/adopt-0-23-0 to mmzen/se_harness:main and the later verification-decision push. Human verification, merge and host-plugin updates remain separate."
+++

# Verify repository adoption of public 0.23.0

## Independence

Expected identities come from released RLS-SEH-034 and public observations verified
in VREC-RLS-005 at base `ed29d435f37b5c2c8b81b1e1375d504edc98787a`.
The wheel SHA-256 is `ffa486d386383992349e75e2890b36ded105c797acaa483783d1380cfd520d5c`;
the payload SHA-256 is `8b5671743d56fceb81bf6117fca97c807f407bafaf9137d629ac60b91ffa14b6`.
Use released 0.22.1 for preparation/approval and the isolated public 0.23.0 target
for its upgrade and post-adoption checks. Source tests remain candidate evidence.
The human accepts the exact final candidate independently of its implementation.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence and pass condition |
| --- | --- | --- |
| REQ-REB-027 | inspection, test | Public identity, preview/apply and canonical transaction match the exact release; target doctor, validate and released-root qualification pass. |
| REQ-IAR-031 | inspection, test | Installer changes only the two selection files. Schema 5, external resources, retained integrations and owner bytes remain valid. Repeat preview changes nothing. |
| REQ-IAR-031 | analysis, test | CI selects 0.23.0, both development versions are 0.23.1, evaluator-facts has no PRE008, current claims match retained public evidence and historical records are preserved. |

## Acceptance scenarios

1. Compare the wheel, installed archive and payload with the expected identities.
   Run target `upgrade --help`, `doctor` and the read-only preview from outside
   the checkout. Before adoption only the old-selection mismatch is expected.
   Other findings require diagnosis, not an assumed waiver.
2. Apply the reviewed installer plan with the canonical evidence path. Run target
   `identity`, `doctor`, `validate`, `qualify released-root` and a repeat preview.
   Require matching identity, no integrity error, no unexpected writes and no
   repeat changes. Retain all outcomes, including failed attempts.
3. Compare the complete Git diff with the approved scope and base. Compare owner
   files and all pre-existing formal artifacts/evidence byte-for-byte. Permit only
   the named current documentation changes. Keep HAG artifacts, service pin,
   release decisions, accepted risks and published package snapshots unchanged.
4. Derive evaluator/source facts through `repository_tools.evaluator_facts`.
   Require evaluator 0.23.0 and candidate 0.23.1. Run the existing governor-transition
   assessment on the committed adoption and its trusted base. Run the existing
   CI upgrade rehearsal twice and compare its declared semantic result.
5. Run the existing CI-pipeline, governor-transition, predecessor-bootstrap,
   progressive-documentation, public-onboarding and refresh-guidance suites.
   Run the full source suite with `scripts/run_tests.py --scale full`, distribution
   checks and CLI help. Retain actual test counts, skips and failures. Use a clean
   source-test environment without unrelated installed se-harness metadata.
6. Review edited documentation and links against the exact public delivery record.
   Keep source, repository evaluator, plugin bundle and private service versions
   distinct. Preserve failed native cases and the desktop omission; no host pass
   may be inferred from repository adoption or a direct resource query.
7. Resolve the selected entry and current procedures, then activate this checkout
   for the supplied host/session. Require 0.23.0 and available instruction discovery.
   This checks selection, not native startup/compaction or desktop behavior.
8. Pass scope, handoff and commit-bound capture checks. Publish the ready VREC
   and evidence in the review PR before requesting human verification. Required
   CI, including Windows/Linux upgrade and integration checks, must pass before merge.

## Evidence retention and limits

Retain actual commands, inputs, component identities, exits and failures under
`evidence/WO-HUP-031/`. The canonical transaction is
`evidence/WO-HUP-031-evaluator-upgrade.json`. Planned capture outputs are
`verification-records/VREC-HUP-029.md` and `evidence/VREC-HUP-029-evaluator.json`;
recheck the unused ID and returned destinations before capture.

The local preparation rehearsal covers Windows. Hosted CI supplies the required
Windows/Linux candidate and integration results. A planning pass is not final
implementation verification. Host update, native sessions, desktop, service
qualification, release publication and provider settings are outside this contract.
Preserve DEC-RLS-010/011 and their risks; this contract grants no broader deferral.
