+++
id = "WO-RLS-025"
type = "work_order"
title = "Prepare checker 0.19.0 and plugin 0.2.0 release inputs"
status = "in_progress"
owners = ["engineering-owner", "release-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "Proposed for human approval: release decisions will rely on the final integration, reproducible package bytes and corrected plugin assembly inputs."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/README.md",
  "docs/engineering/release-0-19-0/",
  "release/plugin-assembly.json",
  "plugins/verity-plane/codex/.codex-plugin/plugin.json",
  "plugins/verity-plane/claude-code/.claude-plugin/plugin.json",
  "plugins/verity-plane/codex/README.md",
  "plugins/verity-plane/claude-code/README.md"
]

[relations]
implements = ["REQ-DST-006", "REQ-PLG-002", "REQ-PLG-037", "REQ-IAR-026"]
specifications = ["SPEC-DST-001", "SPEC-PLG-001", "SPEC-PLG-021", "SPEC-IAR-014"]
architecture = ["ARCH-DST-001", "ADR-DST-001", "ARCH-PLG-001", "ADR-PLG-001", "ARCH-PLG-004", "ADR-PLG-004", "ARCH-IAR-011", "ADR-IAR-011"]
verification = ["VER-DST-001", "VER-PLG-001", "VER-PLG-021", "VER-IAR-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T17:46:14Z"
decided_by = "engineering-owner"
reason = "Human decision in this task: I approve. Apply the exact reviewed scope and required assurance classification, including ordinary release-branch pushes, a draft PR and read-only rehearsals. Codex may execute the approved preparation under DR-015; verification acceptance, release, merge, publication and adoption remain separate."
scope_paths = ["docs/engineering/README.md", "docs/engineering/release-0-19-0/", "release/plugin-assembly.json", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T17:46:58Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the approved release preparation under DR-015 after passing released start checks. The human approved the exact REL-SEH-030 and WO-RLS-025 package in this task."
+++

# Prepare checker 0.19.0 and plugin 0.2.0 release inputs

## Objective

Prepare the integrated checker 0.19.0 for an accountable release decision.
Prepare versioned plugin 0.2.0 inputs that include the accepted instruction
delivery files. The checker already declares version 0.19.0.

## In scope

1. Retain the release membership, compatibility limits, release notes and
   concise evidence in this release domain. Link the domain from the index.
2. Update the production assembly plan to include the existing shared
   `scripts/inject_instructions.py` and each host's `hooks/hooks.json`.
   Set both native plugin manifests to 0.2.0. Update the two packaged README
   files only to state the version, delivery behavior and evidenced host limits.
3. Establish a clean candidate descending from merged commit
   `fbc47dfdcff2b355ee973acb5be09bcdf7cefe78` with only this approved work added.
   Run the existing integration and package checks against that exact candidate.
4. Build the checker wheel and source archive twice with the pinned Linux
   recipe. Retain the exact candidate and matching bundle hashes.
5. Complete this WO after its checks and handoff pass. Prepare one aggregate
   VREC for the work selected by REL-SEH-030, using the final candidate and
   every selected WO's required verification contracts. Present it to the human.
6. After that exact VREC is verified by the human, prepare the ready RLS under
   REL-SEH-030, bind its distribution manifest, and run the bound-record replay.
   Present the ready record and results for the human release decision.

## Authorized decision envelope

This is a proposal. Approval authorizes Codex to start and execute these steps,
make local commits, retain evidence, record completion and prepare the required
VREC under DR-015. The user remains accountable for scope approval, verification
acceptance and release decisions. No acceptance is inferred from a passing test.

The proposed delivery envelope also permits ordinary pushes of
`work/release-0-19-0` to `mmzen/se_harness`, a draft PR to `main`, and dispatch
of the existing read-only `publication-rehearsal.yml` and
`release-candidate-replay.yml` workflows on that branch. These actions provide
the hosted build and review evidence. No force push is included.

## Constraints

Use the isolated released 0.18.0 evaluator for governance. Follow
`docs/notes/developing-se-harness.md#release-sequences` and the installed
authoring procedure. SPEC-IAR-014 governs the new instruction-only delivery;
SPEC-PLG-021 still preserves explicit lifecycle checks and the separate
development/publication paths. Do not revive retired blocking tool hooks.

Use the existing release recipe, workflows, assembly builder and accepted
verification contracts. This work adds no runtime behavior or new CI lane.
Keep historical decisions and evidence unchanged. A final package claim must
name its actual source and wheel; a development archive cannot become a release
archive by changing its label.

## Required verification

- The governing evaluator passes integrity, graph validation, selected
  preflight and handoff for the complete declared change set.
- The full candidate suite, distribution validation and CLI help pass.
  Exercise installation, package contents and 0.18.0-to-0.19.0 upgrade in the
  existing Windows and Ubuntu package environments. Record all skips.
- Check the production plan against tracked source files. Both host packages
  must include the injection script and their own event configuration; their
  shared bytes and declared plugin version must agree. Reuse the existing
  assembly and refusal tests. Retain the comparison with the accepted native
  demonstration inputs; any material delivery change needs fresh native proof.
- Run both manually selected publication rehearsal legs. Confirm the candidate
  replay names the chosen candidate, and retain the two matching wheel/sdist
  builds. A skipped leg does not satisfy this check.
- The final aggregate VREC covers every contract member and its required VERs
  at the same candidate. Reuse historical evidence only for its recorded claim;
  add final integration evidence. The bound ready RLS replay must pass before
  presenting the release decision.

## Evidence and completion

Retain a short report, command arrays, tested commits, evaluator identity,
exit codes, meaningful failure excerpts, CI artifact references and expiry,
coverage links and permanent build manifests under `evidence/WO-RLS-025/`.
Follow `docs/notes/evidence-retention.md`; do not copy fixture repositories or
virtual environments into Git. The completion report states changes, actual
checks, claim limits, final state and the exact next human decision.

The implementation portion completes before aggregate VREC capture. Approved
scope continues to cover the record preparation and later decision transport
described above. A human decision is applied only to the exact reviewed record.

## Out of scope

Merge, tagging, PyPI/GitHub/marketplace publication, latest-marker promotion,
live plugin installation and repository evaluator adoption remain separate
actions. Final distributable plugin archives require the released checker and
an independently obtained published wheel; this work prepares their inputs.
No root AGENTS.md, CLAUDE.md, managed policy, lock, runtime, builder, test or
workflow implementation changes are authorized by this WO.

## Stop conditions

Stop the affected action if integrity or a required check fails, evidence is
missing, the candidate changes, or remediation exceeds these paths or accepted
semantics. Retain the failure. Inspect uncertain effects before retrying.
Present a bounded correction when the existing tools cannot complete this scope.
