+++
id = "REL-SEH-031"
type = "release_contract"
title = "Release evaluator 0.20.0 with complete plugin 0.2.2 delivery"
status = "approved"
owners = ["mmzen"]
created = "2026-09-29"
updated = "2026-09-29"
previous_release_tag = "v0.19.0"

[relations]
gates = ["WO-HUP-021", "WO-HUP-023", "WO-KIS-016", "WO-IAR-020", "WO-IAR-021", "WO-IAR-022", "WO-IAR-023", "WO-IAR-024", "WO-IAR-025", "WO-RLO-010", "WO-RLO-011", "WO-PLG-026", "WO-PLG-027", "WO-PLG-028", "WO-PLG-029", "WO-RLS-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T17:31:39Z"
decided_by = "release-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the reviewed seven-artifact 0.20.0/0.2.2 release package, required commit-bound verification, stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and existing 0.19.0 role encoding. Reviewed SHA-256 ea50a1e5291d48a466adcd608ef0d39e1c091ef8e341621628281a6f9ca19326; approval input SHA-256 ea50a1e5291d48a466adcd608ef0d39e1c091ef8e341621628281a6f9ca19326. Only the confirmed assurance classification was added to work orders. Legacy label release-owner transports the human decision; Codex applies it. Exact candidate verification, RLS release, merge, publication, markers and adoption remain separate."
+++

# Release evaluator 0.20.0 with complete plugin 0.2.2 delivery

## Release unit

Release SE Harness 0.20.0 with the merged instruction refinements, safe guide
retirement, human decision identity correction and release-delivery controls.
Deliver plugin 0.2.2 with the published 0.20.0 wheel through the existing public
plugin-marketplace branch. Plugin and evaluator versions are independent.

The preparation baseline is merged commit
`ff2b5694f5f74743cfc305ed563f01d165f2fe91`. Its post-merge candidate evidence
passed in run 36602157912. WO-RLS-026 adds only the reviewed preparation scope.
The final clean candidate C is selected by the aggregate VREC and matching
reproducible build; no final C or RLS ID is invented before they exist. The human
reviews C, its member set and evidence before verification. The RLS binds C.

The explicit gates select these completed contributions plus preparation:

| Members | Contribution |
| --- | --- |
| WO-HUP-021, WO-HUP-023 | Released 0.19.0 adoption and its CI/documentation compatibility correction. |
| WO-KIS-016 | Recognize the actual human decision identity. |
| WO-IAR-020 through WO-IAR-025 | Native qualification, corrected instruction routes/context, safe retirement and bounded test/consumer corrections. |
| WO-RLO-010, WO-RLO-011 | Publication-reader compatibility and complete five-surface delivery reporting. |
| WO-PLG-026 through WO-PLG-029 | Current plugin packaging/guidance, public observation and truthful availability checks. |
| WO-RLS-026 | This release's integrated candidate, versions, documentation, build and handoff. |

The history census is advisory. Its four missing first-parent trailers do not
require historical rewrites or exemptions. Rejected WO-HUP-022 is excluded.
WO-RLS-025 was already covered by RLS-SEH-028 and is not released again solely
because its decision transport appears after the old candidate. Open PR #488
and any later unrelated main changes are excluded unless separately reviewed.

WO-PLG-030 and WO-PLG-031 are downstream delivery work, not members of the
pre-publication evaluator candidate. Their existence and approved handoff are
required before evaluator publication, but their public-wheel results necessarily
follow it. This separation avoids a circular release prerequisite.

## Required evidence before the release decision

1. All 16 selected work orders are implemented. The external released 0.19.0
   evaluator passes integrity, graph, scope and required lifecycle checks.
2. The final integration passes the existing Windows/Ubuntu source, installed
   wheel/sdist, distribution and predecessor-upgrade lanes. Report skips.
   VER-RLS-026 defines the preparation checks; each member retains its required
   verification contracts. No old VREC is silently rebound to C.
3. Two fresh runs of the pinned Linux build recipe produce identical wheel and
   sdist bytes for C. Retain the schema-2 manifest and both manual publication
   rehearsal legs. A skipped job does not establish the required result.
4. One human-verified aggregate VREC covers exactly these members at C and every
   required VER. Retain final integration evidence alongside justified historical
   reuse. A changed candidate needs matching build and verification.
5. Prepare the ready RLS for 0.20.0, bind the distribution manifest, and pass the
   bound-record replay before the human release decision. Publish only after
   the exact released record is merged and publication is separately authorized.

## Required delivery plan

Before publication, retain and review a `se-harness-delivery-plan/v1` plan under
`evidence/WO-RLS-026/`. All five surfaces are `update`; no deferral is proposed.
Unknown future hashes/commits remain null until derived from reviewed inputs.
The operator is Codex; accountable release and external decisions belong to mmzen.

| Surface | Destination | Owner and governing work | Required observed result |
| --- | --- | --- | --- |
| evaluator | PyPI se-harness 0.20.0 and GitHub release v0.20.0 in mmzen/se_harness | mmzen; WO-RLS-026 and the subsequently released RLS | Exact public wheel/sdist hashes match the RLS; clean public installation passes. |
| marketplace | https://github.com/mmzen/se_harness#plugin-marketplace | mmzen; WO-PLG-030, then WO-PLG-031 | Public immutable revision and both host packages identify plugin 0.2.2 with the exact 0.20.0 wheel; fresh and update routes pass. |
| documentation | Current main README/install/publication guidance plus packaged READMEs | mmzen; WO-RLS-026 and WO-PLG-031 | Versions, availability, commands and support limits match actual observed packages; source and packaged links resolve. |
| demonstration | https://mmzen.github.io/se_harness/ | mmzen; released-RLS publisher, observed by WO-PLG-031 | Deployed provenance identifies the selected release governance snapshot. |
| release_markers | GitHub latest release and refs/tags/last in mmzen/se_harness | mmzen; separate exact marker authorization, observed by WO-PLG-031 | Latest is v0.20.0; last resolves to C after the required public observation cycle. |

## Marketplace handoff and documentation

The evaluator publisher does not update plugin-marketplace. After public wheel
observation, WO-PLG-030 uses the existing build_plugin_marketplace.py build/check
commands with explicit source revision, release revision, RLS path, expected
wheel SHA-256 and that independently obtained public wheel. Qualify the exact
outputs and obtain human acceptance before exact branch-publication authority.

The branch update must preserve history and contain only the reviewed generated
distribution. Recheck its parent against the live remote before pushing. Conflicts
stop the push; do not force over concurrent work. No future push can be declared
successful from a rehearsal or document alone.

WO-PLG-031 then resolves the actual public ref and tests fresh and public
0.2.1-to-0.2.2 updates on Codex and Claude Code Windows CLIs. Compare installed
content hashes and evaluator identity, not just version labels. Reconcile current
source documentation only with observed availability. Keep packaged README
wording valid both before and after publication so availability corrections do
not silently alter the qualified package. Any package correction needs a newly
reviewed assembly and appropriate version decision.

These obligations follow `docs/notes/release-delivery-completion.md` and
`docs/notes/plugin-marketplace-publication.md`. Their source and package link
checks and the actual branch/readback commands belong to retained evidence.
Run `scripts/check_release_delivery.py` on the final reviewed plan and observations.
Evaluator publication alone is incomplete; all five surfaces must pass with no
deferral before reporting overall delivery complete.

## Compatibility and adoption

Fresh 0.20.0 installations omit the six retired guide seeds under SPEC-IAR-015.
Supported upgrades preserve existing owner files. This repository keeps its
installed 0.19.0 root, lock and six stock pointers until separate reviewed
adoption and cleanup. Do not remove owner content as part of this release.
Host support claims remain limited to actual tested Windows CLI versions and
manual compaction. Desktop UI, automatic threshold compaction and other operating
systems are not inferred. Real user-profile adoption is separate.

Owner-configured exceptions and linked accepted-definition revisions remain
unimplemented where the selected release says so; this contract creates no new
runtime capability, lifecycle transition or exception rule.

## Human decisions and recovery

Contract/work approval selects scope and the proposed verification obligations.
It does not supply the later exact aggregate verification, RLS release, merge,
publication or latest/last decisions. The downstream WOs keep pending delivery
visible through those pauses. Use the existing procedures and provider controls.

Stop on failed required checks, incomplete coverage, mismatched identities or
out-of-scope corrections. Preserve failed evidence and inspect uncertain effects
before retrying. After publication, preserve immutable archives and tags. Repair
product defects with a separately reviewed new version. A marketplace correction
uses a reviewed history-preserving commit, never an unreviewed force push.

## Post-release observation window

Before latest/last promotion, require one successful public observation cycle:
the evaluator publisher completes, both distribution digests match the RLS and
a clean public wheel installation passes. This is an event-based window, not an
invented time delay. Marketplace and documentation remain outstanding until
VER-PLG-029 and all five-surface closeout checks establish their actual results.
