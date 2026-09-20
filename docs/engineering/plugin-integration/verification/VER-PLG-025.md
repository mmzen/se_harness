+++
id = "VER-PLG-025"
type = "verification"
title = "Verify completed cleanup and corrected onboarding coverage"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-16"
updated = "2026-09-16"

[relations]
verifies = ["REQ-PLG-032", "REQ-PLG-033", "REQ-PLG-034", "REQ-KIS-009", "REQ-DST-069"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T12:40:39Z"
decided_by = "assurance-owner"
reason = "The owner approved the reviewed replacement package with \"i approve\" on 2026-09-16, exercising the named assurance-owner decision for VER-PLG-025. Reviewed SHA-256 983ef679bb25e71af4f8bf1784c79760dbcd4b08c3a1e6fc40aa00d8254d3013. This records the definition or execution-scope approval; it makes no assurance or external-delivery decision."
+++

# Verify completed cleanup and corrected onboarding coverage

## Independence and applicability

Expected behavior derives from the approved requirements, SPEC-PLG-021,
SPEC-KIS-003 and SPEC-DST-024 as prospectively amended by SPEC-DST-029 for this
delivery. This contract governs WO-PLG-025; it does not change VER-PLG-024 or
turn its failed checks into passes. The baseline is
`f05c478a29c39f94968fdc842a34c861d30a42ac`.

Use the exact external released evaluator 0.18.0 for governance. Candidate
source 0.19.0 supplies source tests. Local acceptance is Windows/Python 3.13;
report actual patch versions. Existing CI checks remain applicable at later
integration, without a new platform matrix or claims about unobserved runs.

## Requirement-to-evidence matrix

| Requirement | Method | Case | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-032 | Inspection, demonstration and existing tests | C01, C04 | Exactly seven root skill files are removed after replacement checks; existing missing-replacement coverage passes. |
| REQ-PLG-033 | Inspection, demonstration and existing tests | C01, C02, C04 | Exactly eight total removals, authorized complete diff, retained restoration/rerun evidence and passing relevant failure tests. |
| REQ-PLG-034 | Inspection and demonstration | C01, C02, C03 | Portable provider choice, unchanged evaluator/unrelated entries, plugin-independent doctor/upgrade and documentation checks that do not require root skill copies. |
| REQ-KIS-009 | Inspection and released workflow checks | C01, C04 | Obsolete delegation TOML is absent; execution follows the replacement WO's recorded approval without an invented route or rewritten history. |
| REQ-DST-069 | Inspection and tests | C03, C04 | The preserved README satisfies the approved plugin-first addendum and unchanged presentation constraints; native commands, setup and direct manual routes have meaningful passing coverage. |

## C01 — Inventory, preservation and complete scope

Compare the final diff with the baseline and WO-PLG-025's exact paths.
Require the delegation TOML and seven named root skill files to be the only
tracked deletions. Compare the lock with the retained pre-migration lock:
schema 4, provider plugin, only those seven entries removed, and every unrelated
entry and evaluator identity unchanged. No local plugin path or identity is
required to check the cloned repository. AGENTS managed markers remain exact.

The repaired README must retain SHA-256
`240bf535c917234225d19e0efe1b48521322eb6f6504c5b7a5619a9e866546dc` as reviewed
locally, with only Git line-ending normalization permitted after checkout.
The already deleted value-proposition files stay deleted. Preserve original
WO-PLG-024 events, body and scope; allow only the explicitly authorized appended
replacement disposition. VER-PLG-024 and its retained evidence remain unchanged.
No unrelated source, tests, templates or package inputs change.

## C02 — Reuse of observed migration and native behavior

The original evidence under `evidence/WO-PLG-024/` contains the actual migration,
same-release upgrade, restoration, repeated switching and native discovery
observations. Compare the relevant baseline/final lock data, released evaluator,
migration implementation, template and plugin/runtime/discovery inputs before
reusing those results. Fresh documentation edits do not require replaying the
unchanged ownership operation. A differing relevant input requires the affected
check to run again in a disposable location.

Name the observed Codex/Claude versions and preserve the recorded differences
between the installed replacement package and the earlier accepted package.
Neither file presence nor reused discovery authenticates a new distribution.
Do not reinstall plugins, alter persistent profiles or claim a fresh host pass
from an old observation. Changed or missing relevant evidence is a blocker.

## C03 — Correct onboarding and skill documentation checks

Review the root as a new reader using SPEC-DST-029 PUB-ENTRY-001 through 004.
Native commands must name the published repository, marketplace ref and plugin.
The explicit setup instruction and offline bundled-wheel statement remain
accurate. The root links directly to manual getting-started and installation/
upgrade guidance; those guides retain actual external-environment, released
package and init/doctor content. Command checks must select expected examples
and fail when they are absent, rather than iterate over an empty list.

Review the corrected tests for the accepted behavior, not merely a green result.
Remove only the expectation that manual setup is duplicated inline. Keep
checks for usable command arguments, local links, release identity, Python
prerequisites, safe examples and the separation of setup from project mutation.
Use the existing parser for harness examples and retained published instructions
for native commands; no network or host installation is needed for these tests.

Skill-note checks resolve tracked plugin sources and default-installation
templates as applicable; they must not require discarded copies in this root.
Existing installation/ownership tests continue to cover repository and plugin
providers and missing replacements. A missing expected shipped source remains
a failing check. Update the current technical-communication explanation and
historical Phase 4 pointer; preserve the historical dated body and the two
earlier historical-note bodies. Check changed local links and source locations.

## C04 — Required regression checks and formal handoff

Run all repository-required checks after implementation: full source suite,
distribution validation, CLI help, candidate doctor with its documented identity
boundary, released doctor, graph validation, review preflight, complete scope
and Git-derived handoff. Every applicable acceptance check must pass. Preserve
the previous 12 failures and their resolutions. Record existing graph warnings
without turning warnings into approval. No new test framework or redundant
full-suite reruns are required after success unless a new change justifies them.

Apply ARTIFACT_AUTHORING.md's implemented-change review questions. Each change
must serve this bounded cleanup or the observed onboarding failures. Verify
that the replacement disposition is real, WO-PLG-025 has recorded scope approval,
and its handoff evidence belongs to its actual formal snapshot. Definition
approval and successful graph validation alone do not establish implementation.

## Evidence and preparation

Retain the comparison, failed and successful outcomes, commands, runtime/file
identities, material review findings and reuse assessment under
`evidence/WO-PLG-025/`. Reference earlier evidence without rewriting or copying
its full tree. Keep large scratch output outside the checkout.

After actual completion, commit the candidate and capture VREC-PLG-022 for
WO-PLG-025 and VER-PLG-025 only, selecting every relied-upon evidence file
explicitly. Retain that ready record and evaluator sidecar in a later governance
commit. No VREC for WO-PLG-024 and no assurance or delivery decision is implied.

## Limits

This establishes repository cleanup, unchanged migration compatibility and
corrected onboarding coverage on the observed platform. It does not qualify
future hosts, publish packages, purge historical evidence or repair the general
scope-amendment gap in evaluator 0.18.0.
