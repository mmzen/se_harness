+++
id = "VER-RLS-026"
type = "verification"
title = "Verify the 0.20.0 release candidate and delivery handoff"
status = "approved"
owners = ["mmzen"]
created = "2026-09-29"
updated = "2026-09-29"

[relations]
verifies = ["REQ-DST-006", "REQ-PLG-002", "REQ-IAR-027", "REQ-IAR-028", "REQ-RLO-018", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T17:31:39Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the reviewed seven-artifact 0.20.0/0.2.2 release package, required commit-bound verification, stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and existing 0.19.0 role encoding. Reviewed SHA-256 f38d07f7382aa06e6fcca7ed90c8eac45b5b5a169472aee56efffb8a478d7296; approval input SHA-256 f38d07f7382aa06e6fcca7ed90c8eac45b5b5a169472aee56efffb8a478d7296. Only the confirmed assurance classification was added to work orders. Legacy label engineering-owner transports the human decision; Codex applies it. Exact candidate verification, RLS release, merge, publication, markers and adoption remain separate."
+++

# Verify the 0.20.0 release candidate and delivery handoff

## Independence

Expected behavior comes from SPEC-DST-001, SPEC-PLG-001, SPEC-IAR-014,
SPEC-IAR-015 and SPEC-RLO-006. The released 0.19.0 evaluator governs this work.
Candidate 0.20.0 runs only as the system under test. A passing source test is
not independent acceptance, a native-host observation or publication evidence.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-DST-006 | test, inspection | Final source and installed-package CI on Windows and Ubuntu; two pinned recipe builds; bundle manifest | Exact candidate C passes existing suites and distribution checks. Wheel and sdist repeat byte-for-byte. Installed package reports 0.20.0. |
| REQ-PLG-002 | inspection, test | Both source manifests, assembly plan, shared-asset inventory and existing assembly tests | Both proposed host inputs name plugin 0.2.2; required shared assets and hooks are included. No candidate wheel is represented as a public plugin wheel. |
| REQ-IAR-027, REQ-IAR-028 | inspection, test | Current documentation review, complete reading traces, retirement and predecessor-upgrade checks | Current summaries distinguish implementation, release and adoption. Fresh candidate installs omit the six retired seeds; supported upgrades preserve owner bytes and pass their existing checks. Historical evidence stays unchanged. |
| REQ-RLO-018 | inspection | Reviewed five-surface delivery plan and WO-PLG-030 and WO-PLG-031 handoffs | Every surface has a destination, owner, exact known inputs, pending unknown inputs, and next action. Marketplace publication is an explicit downstream step. |
| REQ-RLO-020 | test, inspection | Existing delivery-check suite plus a pending-marketplace scenario using this plan | Evaluator-only publication cannot yield complete delivery. Pending identities or absent marketplace evidence return incomplete. |

## Candidate and release checks

Use one clean final commit C for the full release member set in REL-SEH-031.
Run the full source suite, distribution checks, CLI smoke, installed wheel/sdist
checks and actual predecessor upgrade rehearsals in the existing Windows and
Ubuntu lanes. Report skips. Run both manual publication rehearsal legs; a
skipped leg is not a pass. Retain the dispatch head, actual tested candidate,
workflow identity and permanent build manifest.

The aggregate VREC selects every release member and all their required VERs.
Earlier VRECs support only their original claims. Add integration evidence at C;
do not copy an old result onto C. Compare native-delivery inputs before reusing
historical host observations; changed inputs require matching observations or
an explicitly limited claim. Post-evaluator-publication native package qualification is
owned by VER-PLG-028 and is not a prerequisite for building its evaluator.

After human verification, prepare the RLS and bind the schema-2 distribution
manifest. The separate bound-record replay must pass before the release decision.
This replay is a release-decision check, not evidence retroactively inserted
into the already bound aggregate VREC.

## Evidence retention

Retain command arrays, runtime identities, exact commits, exit codes, failures,
successful retries, CI references and permanent build identities under
`docs/engineering/release-0-20-0/evidence/WO-RLS-026/`. Follow the existing
evidence-retention policy. Do not commit virtual environments or fixture trees.

## Residual uncertainty

This contract does not establish a successful future marketplace push or public
installation. VER-PLG-029 assesses those actual effects. Real profile adoption
and removal of this repository's six existing pointers remain separate work.
