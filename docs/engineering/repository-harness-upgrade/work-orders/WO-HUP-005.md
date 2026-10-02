+++
id = "WO-HUP-005"
type = "work_order"
title = "Complete documentation and test compatibility for 0.21.0 adoption"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved WO-HUP-005 and required commit-bound verification in VREC-HUP-025; later adoption and instruction-discovery decisions rely on these corrections."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/notes/README.md",
  "docs/notes/harness-overview.md",
  "docs/notes/harness-uml-model.md",
  "docs/notes/harness-operational-phasing.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/technical-communication.md",
  "docs/notes/agentic-execution-host-adapters.md",
  "tests/test_progressive_documentation.py",
  "tests/test_artifact_catalog.py",
  "tests/test_instruction_architecture.py",
  "pyproject.toml",
  "se_harness/__init__.py",
  "docs/notes/developing-se-harness.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-005.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-005/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-005-evaluator.json",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-025.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-025-evaluator.json",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-HUP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T08:35:03Z"
decided_by = "mmzen"
reason = "Human mmzen: i approve. Approves reviewed WO-HUP-005 and required commit-bound verification in VREC-HUP-025, including seven guide routes, three source test corrections, development version 0.21.1 and its contributor statement. Prior clarification: advance development source to 0.21.1 without publishing; governing evaluator remains 0.21.0. Reviewed SHA256 f65151e3e6b0820a836e12e15adbdc60c584111183f305eff5490c7ce570b7f3; assurance metadata records this decision. No verification acceptance or external action is granted."
scope_paths = ["docs/notes/README.md", "docs/notes/harness-overview.md", "docs/notes/harness-uml-model.md", "docs/notes/harness-operational-phasing.md", "docs/notes/harnessctl-reference.md", "docs/notes/technical-communication.md", "docs/notes/agentic-execution-host-adapters.md", "tests/test_progressive_documentation.py", "tests/test_artifact_catalog.py", "tests/test_instruction_architecture.py", "pyproject.toml", "se_harness/__init__.py", "docs/notes/developing-se-harness.md", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-005.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-005/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-005-evaluator.json", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-025.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-025-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T08:35:48Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-02T08:57:30Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Complete documentation and test compatibility for 0.21.0 adoption

## Objective

Readers of seven current owner guides can find the selected released instructions
after adoption removes repository copies. Source tests remain usable without
those copies, and development version 0.21.1 remains distinct from the adopted
released evaluator 0.21.0. Reuse the accepted resource route in
SPEC-IAR-016 (IAR-EXT-009) and verification case A0210-04 in VER-HUP-003.

## Finding and relationship to adoption

WO-HUP-003 applied the authorized 0.21.0 migration. Its documentation checks
found 17 obsolete link occurrences across eight guides. One guide is already
within WO-HUP-003; the other seven need this bounded scope correction. The
focused run reported 16 failing assertions across two tests. Preserve that
failure and later corrected results. The full run also found two source test
modules reading deleted instructions and PRE008 because candidate source and
the adopted evaluator both name 0.21.0. Human mmzen selected advancing development
source to 0.21.1 without publication. No installer behavior or CI policy change
is needed. Two other full-run failures observed the briefly incomplete new draft
while it was being created; retain that diagnostic and rerun on a stable tree.

WO-HUP-003 remains in progress. Do not rewrite its approved scope or history.
This work supplements its current-guide coverage and joins the same exact
adoption candidate in planned VREC-HUP-025. No new requirement, specification,
architecture, verification contract or policy exception is proposed.

## In scope

- Replace links to retired repository copies in the seven named guides with
  the existing owner installation guide's resource lookup procedure. Each
  reference keeps its explicit released resource ID and applicable heading.
- Clarify that repository skill copies belong to legacy layouts and that
  current policy comes from the selected release. Preserve existing behavior
  descriptions, historical records and source-template links.
- Update the existing UML catalog assertion in the named documentation test
  to check the released resource ID and heading. Keep link and anchor checks.
- Change the two named source test modules to inspect canonical product assets
  under templates/repository/standard instead of deleted adopted copies. Keep
  catalog coverage, instruction content and legacy-fixture assertions. Remove
  only the redundant comparison of the same template with itself. Released
  resource identity and usability remain separately required by VER-HUP-003.
- Set pyproject.toml and se_harness/__init__.py to development version 0.21.1,
  and update its sentence in the contributor guide. Preserve evaluator 0.21.0,
  its wheel/payload selection and all public release claims. Publish nothing.
- Retain review and check results, record local completion and prepare the
  combined commit-bound adoption verification record.

## Out of scope

Runtime behavior, product templates, new resolver behavior, other documentation,
formal definition amendments, deleting further files, credentials, host plugin
settings, release actions, push/PR and merge. Historical artifacts and evidence
remain unchanged. This work grants no verification acceptance.

## Proposed assurance and authorized decision envelope

Propose required commit-bound verification: readers and later adoption decisions
depend on correct instruction discovery. Human confirmation is pending, so this
draft has no invented assurance.decided_by field. Approval may confirm the
classification together with this scope.

Once approved and started, the agent may implement these exact changes, run the
existing checks, retain evidence, make local commits, record completion and
prepare VREC-HUP-025 with WO-HUP-003. Human verification and external actions
remain separate. Use the actual human decision-maker with the selected evaluator;
if legacy role encoding is required, retain mmzen and the exact decision in its
reason and obtain approval for that compatibility encoding.

## Constraints and expected change surface

Use public 0.21.0 outside the checkout. Retain the adoption comparison base
695d6773dc86f25691a9799e969bcca014207837. Do not copy instructions back into the
repository or route users to candidate templates as governing policy.

The execution scope names seven route guides, one contributor-guide sentence,
three existing test files, two version fields, this record,
its bounded evidence locations and the planned shared VREC destinations. The
central lookup section in harness-installation-and-upgrades.md is covered by
WO-HUP-003. Overlapping VREC paths permit one combined record, not two writers.

## Required verification

Reuse VER-HUP-003 without changing its accepted meaning. In particular:

1. Run tests.test_progressive_documentation and the existing package refresh
   guidance tests. All current local links and anchors must resolve. Confirm
   referenced resource IDs and headings against the exact released package.
   Run tests.test_artifact_catalog, the owner-instruction tests and predecessor
   derivation tests. Both package version fields must agree at 0.21.1; derive
   must identify released evaluator 0.21.0 and candidate 0.21.1. All prior
   missing/ambiguous-identity refusals remain required.
2. Review the diff: no current link points to retired copies, no historical
   evidence or source-template link changes, and test checks remain effective.
3. Run the full source suite with --scale full, distribution validation, CLI
   smoke, current evaluator validation and complete combined scope/handoff.
4. Meet the remaining adoption checks and prepare VREC-HUP-025 at one clean
   commit covering both work orders. Required hosted checks remain required
   before integration. Codex desktop and Claude remain unverified by this work.

## Evidence to record

Retain the actual failed and successful documentation results, reviewed diff,
resource/heading checks and test summaries under this work's evidence directory.
Raw logs may stay outside the repository with retrieval information. Generated
handoff evidence uses WO-HUP-005-evaluator.json. VREC-HUP-025 and its evaluator
companion are shared with the adoption scope; check availability before capture.

## Stop and escalate conditions

Stop affected work if a required check fails, a resource/heading is absent,
the correction needs another file, or current accepted meaning must change.
Do not weaken checks, infer a waiver or expand the approved scope.

## Completion report format

Report corrected guide routes, actual tests and unresolved findings, both work
orders' current states and the exact verification candidate. Name the remaining
human verification decision. No completion or approval is claimed by this draft.
