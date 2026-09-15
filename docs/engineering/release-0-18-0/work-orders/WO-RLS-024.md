+++
id = "WO-RLS-024"
type = "work_order"
title = "Prepare checker 0.18.0 and the first plugin release"
status = "implemented"
owners = ["engineering-owner", "release-owner"]
created = "2026-09-15"
updated = "2026-09-15"

[assurance]
commit_bound_verification = "required"
rationale = "Release consumers will rely on the selected checker build and plugin package contents."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/README.md",
  "docs/engineering/release-0-18-0/",
  "release/plugin-assembly.json",
  "plugins/verity-plane/codex/.codex-plugin/plugin.json",
  "plugins/verity-plane/claude-code/.claude-plugin/plugin.json"
]

[relations]
implements = ["REQ-DST-006", "REQ-PLG-002", "REQ-PLG-037"]
specifications = ["SPEC-DST-001", "SPEC-PLG-001", "SPEC-PLG-021"]
architecture = ["ARCH-DST-001", "ADR-DST-001", "ARCH-PLG-001", "ADR-PLG-001", "ARCH-PLG-004", "ADR-PLG-004"]
verification = ["VER-DST-001", "VER-PLG-001", "VER-PLG-021"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T05:56:44Z"
decided_by = "engineering-owner"
reason = "The owner explicitly selected release preparation through the delegated route on 2026-09-15: \"prepare the release (delegated route): go\". WO-RLS-024 records that bounded mandate: checker 0.18.0 qualification/build evidence and plugin 0.1.0 assembly inputs using existing tools. This selects and starts preparation; it records no result-specific verification, release, publication or live adoption decision."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-15T05:58:10Z"
decided_by = "engineering-owner"
reason = "The owner explicitly instructed release preparation through the delegated route. Record the requested start of this bounded preparation after passing start preflight with the complete governing chain."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-15T06:29:02Z"
decided_by = "engineering-owner"
reason = "The owner reviewed release preparation in PR #480 and the report, then replied \"I approve you can prepare the verification record\" to the pending WO-RLS-024 completion question. Record that explicit engineering-owner completion approval and permission to prepare the aggregate VREC. The full local suite, exact-source candidate CI, final evidence-commit CI and two pinned recipe builds passed. This decision does not verify the future record, release, publish, merge or adopt a checker."
+++

# Prepare checker 0.18.0 and the first plugin release

## Result

Prepare a checked checker 0.18.0 candidate, its reproducible build evidence,
release notes and coverage, and the versioned inputs for verity-plane 0.1.0.
The source already declares checker 0.18.0. Set both native plugin manifests to
0.1.0 and add one production assembly plan using the existing builder.

## Execution

The owner selected release preparation with "prepare the release (delegated
route): go" on 2026-09-15. Codex performs the bounded preparation and uses
independent agents for release-path, coverage and package review. Use the
installed 0.17.0 evaluator for repository authority. The accepted single-route
design in SPEC-KIS-003 guides the work; candidate 0.18.0 does not govern its own
release. Record actual lifecycle decisions through the installed evaluator.

Run the normal full suite and package checks. Obtain the build of record from
the existing hosted pinned Linux producer because this workstation has no
Docker. Retain the run, exact candidate, replay manifest and concise results.
Use an explicit release-member list, existing work-order evidence and one
integration summary. Review the Git delta as well as trailers; do not repair
history with empty commits or add a new CI lane.

## Acceptance and evidence

VER-DST-001 covers checker distribution. For plugin preparation, inspect the
production plan against tracked common and host files, check manifest agreement,
and exercise existing assembly tests under VER-PLG-001 as amended by
SPEC-PLG-021 and VER-PLG-021. These checks prove preparation of the inputs.
Final plugin archives need the released checker and its independently obtained
published wheel; their actual assembly and installation are recorded later.
Do not describe a development archive as a published plugin acceptance result.

Keep commands, results, candidate/build identities and material limits in
evidence/WO-RLS-024/. Reuse completed host-discovery and connection evidence;
no new model-session, macOS or desktop-interface support claim is made.
Complete the existing graph, integrity, preflight and handoff checks. A real
failure is resolved within this scope or reported with its exact effect.

## Delivery boundary

Prepare a reviewable candidate and required records to the extent permitted by
their actual gates. Accountable verification and release decisions remain
separate. Tagging, publication, merging, live plugin installation and upgrading
the repository's selected evaluator are not included. No runtime, workflow,
managed root or historical verification/release evidence changes are included.
