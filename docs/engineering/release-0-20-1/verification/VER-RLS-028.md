+++
id = "VER-RLS-028"
type = "verification"
title = "Qualify the 0.2.3 maintenance marketplace package"
status = "draft"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[relations]
verifies = ["REQ-PLG-002", "REQ-RLO-018"]
+++

# Qualify the 0.2.3 maintenance marketplace package

## Independence and selected inputs

Expected behavior comes from SPEC-PLG-001 and SPEC-RLO-006. REL-SEH-032
selects evaluator 0.20.1; RLS-SEH-030 binds its exact candidate and archives.
Plugin 0.2.3 is proposed as a new immutable version. Check that it remains
unused before editing. The source baseline is the public 0.2.2 source,
7253d13b212ad6f7df670021290fea32e81d66de, recorded in the public marketplace's
PACKAGE-IDENTITY.json. Select the final source commit after the permitted
metadata and packaged documentation changes are committed.

Use each checkout's selected released evaluator: 0.19.0 on the maintenance
line and the confirmed selection on current main. Recheck its identity when
switching checkouts. Neither package qualification nor transport adopts 0.20.1.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence and pass condition |
| --- | --- | --- |
| REQ-PLG-002 | test, inspection, demonstration | Both host packages are 0.2.3, contain the exact independently downloaded public 0.20.1 wheel, and share identical common assets. The builder's check mode passes. Actual Windows Codex CLI and Claude Code qualification identifies matching loaded bytes. |
| REQ-RLO-018 | inspection | The reviewed delivery plan names all five surfaces, RLS-SEH-030 and the exact source/package identities. WO-RLS-029 owns public installation, documentation and closeout. Pending observations remain visible. |

## Before evaluator publication

Compare the source diff with the fixed 0.2.2 baseline. Only the two host
version fields and the work order's packaged documentation may change among
assembly inputs. Shared skills, setup, hooks, assembly plan and builder stay
byte-identical. Review source and package-relative links in their proper contexts.
Run applicable existing package and documentation tests. Retain the exact
source commit and the passing formal/scope checks. A source review does not
qualify a package that has not yet been assembled.

When transporting release governance to main, compare all selected records and
evidence byte-for-byte with their reviewed source. Preserve candidate commits,
history and evidence digests. Validate with main's own selected evaluator and
run the existing release-record qualification procedure. Report a version or
graph incompatibility; do not patch accepted records to make transport pass.

## After evaluator publication

Download the wheel independently from the public release and compare its
archive digest with released RLS-SEH-030. Build and check the marketplace with
scripts/build_plugin_marketplace.py, using explicit source and release revisions
and fresh output outside the repository. Compare both catalogs, manifests,
inventories, archives, common files and wheel bytes. Reuse the existing wrong
wheel and changed inventory refusal cases, with their actual results retained.

Install each output in a disposable Windows host profile. Record host versions,
installed paths and content hashes, evaluator identity, actual startup,
manual compaction and resumed-session delivery. Use the existing acceptance
tools. Authentication or unavailable native behavior remains an unmet check;
a synthetic hook call cannot replace host evidence. Desktop and automatic
compaction remain unclaimed unless separately demonstrated.

Prepare a distribution commit descending from the observed public marketplace
head. Its complete tree must match the qualified output. Capture the work's
VREC and obtain human verification before exact marketplace publication is
requested. Public fresh/update results belong to VER-RLS-029.

## Evidence retention and limits

Retain actual arguments, runtime identities, source/release/public commits,
digests, native transcripts, failures and assessment under evidence/WO-RLS-028/.
Use this domain's verification-records/ and evaluator evidence destinations.
Do not commit credentials, profiles, environments or generated package trees.
Local qualification proves neither public availability nor adoption.
