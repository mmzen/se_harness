+++
id = "VER-RLS-027"
type = "verification"
title = "Verify the 0.20.1 compatibility maintenance release"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[relations]
verifies = ["REQ-SHB-008", "REQ-REB-020", "REQ-REB-031", "REQ-RLO-018", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T19:43:46Z"
decided_by = "engineering-owner"
reason = "Human mmzen: Approve package and required verification. Approves reviewed SPEC-RLS-001, VER-RLS-027, WO-RLS-027 and REL-SEH-032 and required commit-bound verification. Includes bounded local implementation/preparation and the maintenance 0.19.0 role-label encoding, with mmzen retained as human decision-maker. Reviewed SHA256 21d7acea8dc1a24aa4ad861c4cc2e1cd79751134ecc3ec426655aca293f0102b; transition input SHA256 21d7acea8dc1a24aa4ad861c4cc2e1cd79751134ecc3ec426655aca293f0102b. Only confirmed assurance metadata was added to the work order. Codex applies the matching decision. Push/PR, dispatch, verification acceptance, release, publication, markers and adoption remain separate."
+++

# Verify the 0.20.1 compatibility maintenance release

## Independence and scope

Expected behavior comes from SPEC-RLS-001 and the linked accepted requirements.
Use exact installed wheels outside the checkout. Candidate-runner results prove
behavior; they do not become independent released-verifier evidence. Human mmzen
accepts the eventual commit-bound verification record. No existing VREC is reused
as acceptance of changed bytes.

The maintenance checkout retains its baseline-selected 0.19.0 governor and CI
selection. Use that exact released evaluator for its lifecycle and root checks.
Also assess the maintenance wheel with the independently acquired released
0.20.0 qualify candidate-package operation. The current successor checkout
remains selected to 0.20.0. Neither test changes either repository's selection.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence and pass condition |
| --- | --- | --- |
| REQ-SHB-008 | Test and inspection | On Windows and Linux, the installed maintenance runner completes the existing scenarios against a legacy wheel and the exact minimal wheel below. Minimal init contains exactly the two selection files before the explicit Git integration. Both refusal cases and unchanged customized bytes pass. |
| REQ-SHB-008 | Test | Unknown layout, unusable lock, extra default file, missing managed block, failed integration setup and unexpected refusal success produce failures. Use focused tests for these distinct boundaries and actual wheels for end-to-end behavior. No new framework is needed. |
| REQ-REB-020 | Test and inspection | Exact public 0.20.0 independently qualifies the maintenance wheel through the typed operation on Windows and Linux. Retain verifier archive/payload identity, candidate commit, wheel digest, role, all scenarios and no-change proof. Candidate-runner tests remain labelled as candidate evidence. |
| REQ-REB-031 | Inspection and existing tests | Qualification still uses the one typed operation. No workflow fallback, bootstrap exemption, candidate-as-verifier substitution or new role is added. Existing qualification and CI conformance tests pass. |
| REQ-RLO-018 | Inspection | The release contract and retained preparation delivery plan cover all five surfaces, owners and next actions. Downstream publication work is separately identified; unknown release hashes remain pending. |
| REQ-RLO-020 | Inspection | Documentation distinguishes preparation, publication and observed delivery. No current public claim or completion claim precedes matching observation. Pending marketplace work remains visible. |

## Fixed compatibility input

The minimal-layout test input is the retained wheel for source commit
6dd70f29cd43ffc230779d61ee1a7ced43a7a611:

- Filename: se_harness-0.21.0-py3-none-any.whl.
- Archive SHA256: e518c10d0fe34ae8d2864d7af5ecef0f84e0b94fe4c90afccc4f2d407b791f3b.
- Payload SHA256: 5782f29c8242fe0c60bc78110863cc2bdcd1a4050823d343da006f180824fe45.
- Existing observations: instruction-architecture/evidence/WO-IAR-030/compatibility-check.json.

Retain or reference that immutable input with the maintenance evidence so it can
be replayed. Check its digest before use; do not rebuild it and retain the old
identity. If unavailable, report the missing criterion and return a replacement
input for review. This input is a non-promotable test artifact, not a release.

## Integrated release checks

1. Compare the complete candidate change set against the published 0.20 baseline.
   Installer, resource payload, lifecycle contracts and plugin code stay unchanged;
   only the work order's bounded correction and release material may differ.
2. Run the focused acceptance/qualification tests and existing identity refusals.
   Run the full source suite, distribution validation and installed wheel/sdist
   checks on the maintenance candidate under the existing Windows/Linux lanes.
   Retain reported skips; skips cannot satisfy a required criterion.
3. Confirm fresh legacy init and supported predecessor upgrade behavior on Windows
   and Linux. Existing source tests alone do not establish the installed footprint.
4. Use the pinned repository recipe to produce two identical wheel/sdist builds
   from the exact clean candidate. Retain the manifest, commands and outputs.
5. Obtain the existing CI and publication rehearsal results when separately
   authorized. A local pass cannot be reported as a hosted workflow pass.
6. Capture the VREC with the selected released governor after handoff passes.
   Retain exact commit, all required evidence and limitations. After human
   verification, release-record preparation and bound-record replay follow the
   separately selected release action.

## Evidence and limits

Retain results under evidence/WO-RLS-027/ in this domain, including actual argv,
runtimes, exit codes, digests, failed attempts and the requirement assessment.
Use the existing evidence formats. Required candidate fixtures may be retained
as digest-bound CI artifacts or durable external inputs; do not commit a wheel
into source. Capture commands allocate the VREC and RLS later.

Native host behavior is not changed by this maintenance patch. Marketplace
package and public-route qualification remain downstream obligations. Do not
extend prior CLI observations into desktop support or claim that this record
finishes VER-IAR-022. After separate adoption, the successor needs its own exact
released-verifier qualification and remaining integrated/native assessment.
