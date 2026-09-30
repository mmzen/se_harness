+++
id = "REL-SEH-032"
type = "release_contract"
title = "Release the 0.20.1 candidate-assessment compatibility patch"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"
previous_release_tag = "v0.20.0"

[relations]
gates = ["WO-RLS-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T19:43:46Z"
decided_by = "release-owner"
reason = "Human mmzen: Approve package and required verification. Approves reviewed SPEC-RLS-001, VER-RLS-027, WO-RLS-027 and REL-SEH-032 and required commit-bound verification. Includes bounded local implementation/preparation and the maintenance 0.19.0 role-label encoding, with mmzen retained as human decision-maker. Reviewed SHA256 df54402ca6f85abe87dd95782f0ddb51fb5acce1af4b4a88d95558ab34aef999; transition input SHA256 df54402ca6f85abe87dd95782f0ddb51fb5acce1af4b4a88d95558ab34aef999. Only confirmed assurance metadata was added to the work order. Codex applies the matching decision. Push/PR, dispatch, verification acceptance, release, publication, markers and adoption remain separate."
+++

# Release the 0.20.1 candidate-assessment compatibility patch

## Release unit

Propose SE Harness 0.20.1 from maintenance baseline
7253d13b212ad6f7df670021290fea32e81d66de (public release/0.20 and v0.20.0).
Include only WO-RLS-027. The already released 0.20.0 contributions are baseline
history, not new release members. No minimal-resource implementation, new plugin
activation behavior or unrelated main-branch work enters this maintenance release.

The final candidate C, wheel hashes, VREC and RLS do not exist yet. Supported
capture/preparation commands will bind them after the required evidence and
human decisions. Do not use the successor's 6dd70f2 commit as maintenance C.
Version 0.20.1 was unused in observed public refs, GitHub releases and PyPI on
2026-09-30. Recheck before execution and publication; an occupied version requires
review of a successor contract, not replacement of public bytes.

## Required evidence and decision sequence

1. WO-RLS-027 is approved and implemented under its own selected released
   evaluator. Required formal, integrity, scope and handoff checks pass.
2. VER-RLS-027 passes for exact C, including Windows/Linux legacy and minimal
   candidate scenarios, independent public 0.20.0 qualification of the maintenance
   wheel, source/installed package checks, and preserved refusal/identity checks.
3. The existing pinned recipe produces identical wheel and sdist bytes in two
   clean runs. Retain its schema-2 manifest and required CI/rehearsal evidence.
4. The authorized human verifies the exact final-candidate VREC covering
   WO-RLS-027 and VER-RLS-027. Earlier records do not supply that decision.
5. After release preparation is selected, prepare the RLS, bind the manifest,
   run the existing bound-record replay, and request the exact human release
   decision. No RLS is authored by hand.
6. Publication follows separate authorization for that immutable released record
   and the established provider controls. A verified VREC or approved contract
   does not itself authorize publication, Git actions or marker movement.

## Five-surface delivery plan

The preparation plan selects update for all five surfaces. Human mmzen owns the
release/external decisions; Codex prepares and executes only authorized work.
Retain the existing se-harness-delivery-plan/v1 preparation format under
`evidence/WO-RLS-027/`. Unknown future identities stay pending until observed.
No deferral or unchanged-surface completion claim is selected here.

| Surface | Intended result | Governing work and next handoff |
| --- | --- | --- |
| Evaluator | Exact 0.20.1 wheel/sdist on PyPI and GitHub v0.20.1, matching the RLS. | WO-RLS-027 prepares the candidate. Later release and publication decisions select actual immutable inputs. |
| Marketplace | A new immutable plugin package based on the public 0.2.2 source, containing the exact public 0.20.1 wheel. | Prepare a separate bounded delivery WO/VER and unused plugin version before release authorization. After public wheel observation, use the existing marketplace builder/checker, qualify the package and obtain exact publication authority. Never replace plugin 0.2.2 under its existing identity. |
| Documentation | Maintenance notes, current-main availability guidance and packaged READMEs describe observed versions and support accurately. | WO-RLS-027 prepares its listed maintenance documents. The downstream delivery scope must cover current main and packaged guidance, source/package links and public receipts. Do not label unobserved availability as complete. |
| Demonstration | Deployed provenance matches the selected release governance snapshot. | Observe the existing released-RLS publisher/deployment under the downstream delivery work. Keep failure or missing observation visible. |
| Release markers | GitHub latest identifies v0.20.1 and last resolves to C. | Separate human marker authority after the public observation window; retain actual readback. |

The downstream package must remain on the released plugin behavior. It must not
bring the unreleased activation/resources work from main into this maintenance
delivery. Review its exact source commit, new plugin version, paths, native/public
verification and evidence destinations before approving its work. Those actual
WO/VER IDs must be present in the bound delivery plan before evaluator publication.
They are downstream work, not pre-publication members in this contract's gates.

Follow docs/notes/release-delivery-completion.md and
docs/notes/plugin-marketplace-publication.md. Publishing the evaluator cannot
prove marketplace delivery. Run the existing closeout checker only with the real
RLS, wheel identity, bound plan and observations. Overall delivery remains
incomplete until all five declared surfaces have matching evidence.

## Compatibility and adoption

The maintenance installer retains 0.20 behavior. It does not offer the new
minimal layout. Its verifier can assess that layout in another candidate.
Keep the maintenance baseline's selected 0.19.0 root unchanged. The current
successor checkout remains on 0.20.0 until separately approved adoption.

After public 0.20.1 identity and required observations are available, prepare a
separate adoption WO/VER for the current repository and CI. Then reconcile the
successor branch, rebuild it and obtain independent qualification with that
released verifier. Finish VER-IAR-022 before preparing VREC-IAR-020. Desktop
instruction delivery remains unverified until actual evidence exists.

## Recovery and observation

Stop release on failed checks, incomplete verified coverage, mismatched identity,
changed candidate, missing downstream authority or unreviewed scope. Preserve
failed evidence and inspect uncertain effects before retrying. Before publication,
repair under the existing bounded work only if scope still matches, then rebuild
and obtain matching verification. After publication, preserve immutable archives
and tags; repair product defects through a separately reviewed new version.

Before latest/last promotion, observe one successful public publication cycle:
the publisher succeeds, both public distribution digests match the RLS and a clean
public install passes. This is an event-based window. Marketplace publication
must preserve branch history and stop on an advanced remote parent. Public fresh
and update routes for each claimed host, documentation, demonstration and markers
need their own retained observations before delivery closeout.
