+++
id = "SPEC-PLG-023"
type = "specification"
title = "Refresh marketplace delivery and current guidance for plugin 0.2.1"
status = "approved"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
contract = "Prepare and qualify plugin 0.2.1 with released evaluator 0.19.0, correct current guidance, and confirm separately authorized public delivery before closing its availability claims."

[relations]
specifies = ["REQ-PLG-039", "REQ-PLG-040", "REQ-PLG-041"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T20:39:06Z"
decided_by = "technical-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the nine-artifact marketplace refresh package and required commit-bound verification for WO-PLG-026, WO-PLG-027 and WO-PLG-028. The selected pairing is plugin 0.2.1 with the unchanged released evaluator 0.19.0. Reviewed SHA-256 2e58fc3614d6032d9af587f753a50420b8418f227519a9e394befd82afb09bb8; transition input SHA-256 2e58fc3614d6032d9af587f753a50420b8418f227519a9e394befd82afb09bb8. Legacy 0.19.0 role technical-owner encodes the right; mmzen is the human decision-maker and Codex applies it. Only confirmed assurance fields and confirmation prose were added to the three draft WOs. WO-PLG-026 and WO-PLG-027 may start after required checks. WO-PLG-028 waits for human-verified preparation coverage and separately authorized, observed publication. No external mutation is authorized."
+++

# Refresh marketplace delivery and current guidance for plugin 0.2.1

## Applicability and preserved authority

This specification defines the new plugin 0.2.1 delivery. SPEC-PLG-022 and
VER-PLG-023 remain records of the initial 0.1.0/0.18.0 delivery; this specification
does not replace their rules or govern their work orders. Their file bytes,
states and historical evidence remain unchanged.

Reuse INT-DST-001 and CAP-DST-001 without changes. Preserve the existing package
architecture, setup behavior, plugin-first presentation and approved hook logic.
The current installed evaluator remains released 0.19.0. If implementation needs
to change an accepted definition, stop that part and use the supported amendment
boundary; this new-delivery record is not an amendment workaround.

## Package identity

**MREF-001.** Select plugin 0.2.1 in both native manifests. Bundle the unchanged
`se_harness-0.19.0-py3-none-any.whl`, SHA-256 `43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8`. RLS-SEH-028 and its
distribution metadata provide the release identity. Resolve and retain a full
governance commit containing that released record. Do not bundle candidate 0.20.0.
The assembly source is one committed descendant of `c4d9036fdaab378f08fe2db68978126f66ab961e` with approved
package inputs. Record the source commit and exact assembly-plan digest.

**MREF-002.** Reuse `scripts/build_plugin_marketplace.py build` and `check` with
the selected source, release revision/record, wheel digest, external evaluator
Python, and a fresh absolute output directory outside the checkout. Keep both
catalogs named `se-harness`, offering `verity-plane` from complete package paths.
Validate inventories, expanded files and both archives against independent source
and wheel inputs. Do not edit generated output, replace only a version string in
the public tree, change the builder, or widen its acceptance rules.

## Current instructions and availability

**MREF-003.** Before publication, current source instructions distinguish the
observed public 0.1.0/0.18.0 route from prepared 0.2.1/0.19.0. The assembled guide
describes the selected package and how to install it, with publication checks as
conditions rather than invented past results. Preserve Python 3.11+, venv and
ensurepip prerequisites, offline setup and explicit repository adoption.

**MREF-004.** Correct the audited instruction routes, whole-file AGENTS ownership,
absolute released-evaluator convention, glossary link and provider boundaries.
Preserve dated descriptions and fixtures. Bound descriptions of hook support to
actually tested hosts and versions. Keep published 0.19.0 behavior separate from
unreleased installer seed retirement. State that instruction hooks do not enforce
all tool invocations. Keep submission drafts distinct from a provider listing;
unconfirmed publisher/legal inputs remain explicit. Check current provider rules
when changing those drafts; unsupported listing claims must be removed or dated.

**MREF-005.** Extend existing tests to check expected candidate identity against
manifests and the selected release metadata, and public-availability claims
against retained public observations. Two matching README strings are insufficient.
Keep normal tests offline. Check source links in their source context and composed
links in the generated distribution. Include wrong-version, wrong-wheel,
missing-heading and premature-public-claim cases. Preserve existing useful checks.

## Qualification and delivery sequence

**MREF-006.** Before publication, retain real Windows native qualification on
both Codex and Claude Code: fresh local install; public 0.1.0 to candidate update;
and switching from the known local 0.2.0 selection. Record marketplace precedence,
cache refresh, active source and installed bytes. Test startup, compaction,
repository switch, and missing/mismatched root disclosure on selected 0.19.0
consumer repositories. Retain complete delivered roots and their digests, host
versions, commands, output and limits. A test-only model override may be used
only when recorded; it must not change the saved user setting. Missing login,
trust or supported commands is a visible prerequisite, never a passing result.

**MREF-007.** Prepare commit-bound verification for package and guidance work.
An authorized human decides verification. Then select the exact public action,
distribution digest, source commit, destination and expected old public revision
under the external-action procedure. A WO or verification alone grants no push,
merge or publication authority. Add an ordinary descendant commit on the existing
public branch only under that separate authorization. Unexpected ref movement
requires comparison and renewed checks; never force over it.

**MREF-008.** After authorized publication, perform fresh and update installs
from the actual public ref in disposable profiles on both hosts. Confirm active
package bytes and native delivery. Keep failures and partial publication visible.
Update only current availability/status text and its evidence after passing
observations. Preserve the immutable assembled tree and the source commit from
which it was built. A later text correction never relabels an archive's source.

**MREF-009.** Use the existing plan/observations format from
`docs/notes/release-delivery-completion.md`. Marketplace, documentation and
demonstration are updates; evaluator 0.19.0 and release markers are unchanged
with compatibility review and readback. Record owners, governing work references,
expected identities and pending actions before publication. Unselected commit
identities remain pending; do not invent hashes. Bind observations to the final
plan bytes, preserve earlier versions, and require an explicit evidence mapping
when reusing unchanged evidence. Run `scripts/check_release_delivery.py` with
the plan, observations and evidence root. A pass is a supplied-evidence result,
not a new human decision or automatic proof of live state.

## Coverage and examples

| Requirement | Rules |
| --- | --- |
| REQ-PLG-039 | MREF-001, MREF-002, MREF-003, MREF-005, MREF-006, MREF-007 |
| REQ-PLG-040 | MREF-003, MREF-004, MREF-005 |
| REQ-PLG-041 | MREF-007, MREF-008, MREF-009 |

A correct local 0.2.1 package can pass preparation while delivery remains
incomplete. A public host still loading cached 0.1.0 fails public acceptance even
if the branch contains 0.2.1. Two documents that both say 0.18.0 cannot establish
the identity of a selected 0.19.0 wheel.

## Design choice

Reuse the existing composer, identity inventories, delivery checker, native host
commands and documentation tests. No new registry, installer, generic framework,
runtime mechanism, lifecycle rule, architecture or ADR is needed. Separate
preparation from public confirmation so pre-publication verification does not
depend on an external action that it has not yet authorized.
