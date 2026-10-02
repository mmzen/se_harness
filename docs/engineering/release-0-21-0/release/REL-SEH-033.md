+++
id = "REL-SEH-033"
type = "release_contract"
title = "Release 0.21.0 external resources and minimal installation"
status = "approved"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"
previous_release_tag = "v0.20.0"

[relations]
gates = ["WO-IAR-028", "WO-IAR-029", "WO-IAR-030", "WO-IAR-031", "WO-IAR-033", "WO-IAR-034", "WO-IAR-035", "WO-IAR-036", "WO-IAR-037", "WO-IAR-039", "WO-IAR-040", "WO-IAR-041", "WO-RLS-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T19:53:49Z"
decided_by = "release-owner"
reason = "Human mmzen: Approve package and required verification. Approves REL-SEH-033, WO-RLS-031/032/033 and VER-RLS-030/031/032, required commit-bound verification, plugin 0.2.4, ordinary release-review branch push/draft PR and read-only CI rehearsals. Existing v0.21.0 publication authorization is retained. Final-candidate verification, exact RLS decision and unresolved desktop evidence remain separate. Reviewed SHA256 455a614c22e47dde59a2359e8250e2cf549f7407740c9619c5cec9424430ebf9; transition-input SHA256 455a614c22e47dde59a2359e8250e2cf549f7407740c9619c5cec9424430ebf9. Only confirmed work-order assurance metadata was added. Codex applies the human decision using the selected evaluator role-label encoding; mmzen is the decision-maker."
+++

# Release 0.21.0 external resources and minimal installation

## Release unit

Select evaluator 0.21.0 from the integrated main lineage, starting at
f5f7c77c6eadfd7d6f1c68e136f1f7cc29cfc0a5. The gates array contains the twelve
external-resource implementation/correction work orders and WO-RLS-031 release
preparation. One final aggregate VREC must cover exactly that set at candidate C.
Its required contracts include VER-IAR-020, VER-IAR-021, VER-IAR-022 and VER-RLS-030.

The prior main-line product baseline is v0.20.0. Public v0.20.1 is a separately
released maintenance branch and supplies the independent verifier now adopted
in main. Do not invent ancestry or treat that maintenance release as unpublished.
The advisory release-unit census has missing merge trailers; no fabricated
trailers or exemptions are needed to define this explicitly reviewed unit.

Completed adoption, pointer/glossary cleanup, decision-transport and earlier
publication records remain history, not new release members. WO-IAR-032 and
WO-IAR-038 only transported existing authority. WO-RLS-032/033 are downstream
delivery work, excluded from the pre-publication VREC to avoid a dependency cycle.

## Versions and authority

Evaluator 0.21.0 already appears in source; it is not yet published. Propose a
new plugin identity 0.2.4 for the accepted new adapter behavior. Public 0.2.3 is
the 0.20.1 maintenance package. Recheck all version reservations before build
and publication. Never replace previously published bytes under the same identity.

Human mmzen requested "Publish v0.21.0". Retain that exact external request for
the matching immutable release once its prerequisites pass. It does not invent
approval of this new contract, an aggregate assurance verdict, a future RLS
decision, marketplace publication, latest/last targets or repository adoption.

## Required sequence

1. Approve the bounded preparation/delivery package and required commit-bound
   assurance. Run WO-RLS-031 under its recorded authority and selected 0.20.1 evaluator.
2. Pass final Windows/Linux source, installed-package, resource and migration
   checks, independent public-0.20.1 qualification and both publication rehearsals.
3. Resolve every required criterion before release, including the still-unverified
   Codex Windows desktop criterion in VER-IAR-021. No deferral or waiver is supplied
   here; a passing CLI trace or an earlier VREC decision cannot remove that criterion.
4. Produce wheel/sdist through two clean pinned recipe builds. Retain the schema-2
   bundle manifest and exact tested candidate, not a PR merge approximation.
5. Capture and obtain human verification of the final aggregate VREC at C.
6. Prepare RLS with explicit tag v0.21.0. Bind the manifest and pass bound-record
   replay. Obtain the human decision on that exact ready RLS.
7. Integrate the released RLS through the reviewed PR procedure. Run the publisher
   resolve command against main, then use the existing protected publish-pypi
   workflow. Its protected environment decision remains independently enforced.
8. Observe public bytes, complete WO-RLS-032 and WO-RLS-033, then assess all surfaces.

## Five-surface delivery plan

| Surface | Disposition and destination | Owner, work and required observation |
| --- | --- | --- |
| Evaluator | Update: PyPI se-harness 0.21.0 and GitHub v0.21.0 | mmzen decides; WO-RLS-031 prepares/publishes under matching authority. Publisher and independent wheel/sdist/install readback must match the RLS. |
| Marketplace | Update: mmzen/se_harness:plugin-marketplace, plugin 0.2.4 for Codex and Claude Code | WO-RLS-032 assembles from the public wheel and qualifies exact native inputs. Separate exact marketplace authority precedes descendant publication. WO-RLS-033 verifies public fresh/update routes. |
| Documentation | Update: current source and assembled release/install guides | WO-RLS-031 distinguishes proposal from current availability. WO-RLS-033 reconciles real observations and reads merged public guidance back. |
| Demonstration | Update: existing Pages deployment | Existing publisher performs deployment; WO-RLS-033 checks the deployed governance provenance. |
| Release markers | Update: GitHub latest and last | Separate exact human marker decision after the observation window; WO-RLS-033 retains target readback. |

Retain the existing versioned JSON delivery plan under evidence/WO-RLS-031/.
Bind known authority and destination inputs; keep future RLS/commit/hash values
pending until produced. Each subsequent observation binds its exact plan bytes.
Do not declare complete delivery after evaluator publication alone.

## Recovery and observation

Before publication, failed checks return to bounded correction planning; changed
candidate bytes require refreshed build and verification. Never relabel historical
VRECs. After publication, preserve immutable archives and tags. Correct defects
through a separately reviewed new version. Inspect uncertain external effects
before retrying; no force overwrite or new publisher path is authorized.

The observation window is one successful publication cycle: publisher success,
both independently downloaded distribution hashes match, and clean public install
passes. Latest/last promotion then needs its own exact authorization. Marketplace,
documentation, demonstration and markers each require retained observations for
overall closeout. The closeout checker grants no authority.

## Separate adoption

Keep this repository on selected 0.20.1 throughout release preparation. The human
has separately approved v0.21.0 adoption; WO-HUP-003 and VER-HUP-003 are its draft
package. Apply that migration only after published inputs and reviewed native
replacement delivery exist. This release work removes no root instruction file.
