+++
id = "WO-ECP-007"
type = "work_order"
title = "Close remaining product-boundary gaps"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-10-17"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification for the reviewed definition amendments, viewer behavior, package checks and installation guidance. Later verification and release decisions rely on the exact implemented result."
decided_by = "mmzen"

[execution_scope]
paths = [
  "repository_tools/explorer_design/build_explorer_template.py",
  "se_harness/engine/harness_explorer/index.template.html",
  "scripts/check_portable_release_surface.py",
  "tests/test_dashboard_webui.py",
  "tests/test_release_orchestration.py",
  "tests/test_harnessctl.py",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/intent/INT-ECP-001.md",
  "docs/engineering/execution-control-plane/capabilities/CAP-ECP-003.md",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-012.md",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-013.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-007.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-007.md",
  "docs/engineering/execution-control-plane/architecture/adr/ADR-ECP-005.md",
  "docs/engineering/execution-control-plane/decisions/DEC-ECP-003.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-007.md",
  "docs/engineering/execution-control-plane/evidence/WO-ECP-007/",
]

[relations]
implements = ["REQ-ECP-012", "REQ-ECP-013"]
specifications = ["SPEC-ECP-007"]
verification = ["VER-ECP-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-17T11:51:14Z"
decided_by = "mmzen"
reason = "mmzen approved the reviewed package: seven exact linked manual definition amendments, WO-ECP-007 implementation, required commit-bound verification, and review pushes/draft PR to mmzen/se_harness from codex/narrow-ecp-007 to main, including the later separately given verification-decision push. Plan SHA-256 5b9d646ceb8931b0049a10564bc6198ad5309ce412d0d6536923c8e77efcbde9; definition activation is retained and DEC-ECP-003 is resolved. The confirmed doctor criterion requires effective Git evidence attributes before passing. Verification acceptance and merge remain separate."
scope_paths = ["repository_tools/explorer_design/build_explorer_template.py", "se_harness/engine/harness_explorer/index.template.html", "scripts/check_portable_release_surface.py", "tests/test_dashboard_webui.py", "tests/test_release_orchestration.py", "tests/test_harnessctl.py", "docs/notes/harness-installation-and-upgrades.md", "docs/engineering/execution-control-plane/README.md", "docs/engineering/execution-control-plane/intent/INT-ECP-001.md", "docs/engineering/execution-control-plane/capabilities/CAP-ECP-003.md", "docs/engineering/execution-control-plane/requirements/REQ-ECP-012.md", "docs/engineering/execution-control-plane/requirements/REQ-ECP-013.md", "docs/engineering/execution-control-plane/specifications/SPEC-ECP-007.md", "docs/engineering/execution-control-plane/verification/VER-ECP-007.md", "docs/engineering/execution-control-plane/architecture/adr/ADR-ECP-005.md", "docs/engineering/execution-control-plane/decisions/DEC-ECP-003.md", "docs/engineering/execution-control-plane/work-orders/WO-ECP-007.md", "docs/engineering/execution-control-plane/evidence/WO-ECP-007/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-17T11:55:21Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-17T12:56:12Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Close remaining product-boundary gaps

## Objective

Remove the remaining repository-specific exception from the shipped graph viewer,
detect its return during package checks, and reconcile fresh-install acceptance
with the selected minimal-installation policy.

The human confirmed narrowing this draft on 2026-10-17. That confirms preparation,
not implementation, definition acceptance, assurance classification or publication.

## Approval dependencies

`DEC-ECP-003` blocks approval pending reviewed definition revisions and their
activation. The existing links above are retained; proposed revisions do not
yet govern work. The affected accepted records are `REQ-ECP-012`, `REQ-ECP-013`,
`SPEC-ECP-007`, `VER-ECP-007` and the relevant passages of `INT-ECP-001`,
`CAP-ECP-003` and `ADR-ECP-005`. Preserve their exact accepted versions.

Evaluator 0.23.0 has no supported linked-definition revision/activation command.
Exact amendment proposals remain transient outside the repository for review.

On 2026-10-17, mmzen confirmed the installation choice: "doctor: yes, go".
Keep current behavior. In a Git repository, effective evidence attributes are
required before `doctor` passes, including before the first evidence file.
The owner selects `--integration git` or supplies an equivalent rule. Minimal
`init` still writes only the configuration and lock. This clarification does
not activate the proposed definition amendments or approve implementation.

## In scope

1. Remove the shipped viewer's special treatment of `VREC-SEH-021`. Records
   that differ only in ID receive the same selection treatment. Preserve the
   existing status and relationship rules.
2. Apply the correction through the existing count-checked Explorer build
   patches and regenerate its packaged HTML. Keep retained design exports intact.
3. Extend the existing portable-surface check to cover product implementation
   and generated executable UI. Test clean packages and forbidden literals.
   Define the exact scan boundary in the revised specification, distinguishing
   executable policy from historical documentation and package-description links.
4. Document and test the accepted installation sequence using a separately
   installed candidate wheel. The confirmed choice preserves two-file default
   `init` and explicitly selects `--integration git` before expecting a Git
   repository to pass `doctor`. Equivalent owner rules remain valid.
5. Retain the exact candidate, actual checks and unchanged historical bytes.
6. Only after separate explicit authority for the reviewed manual amendment,
   preserve the seven accepted definitions byte-for-byte, activate the exact
   reviewed replacement text and retain its links and actual human decision.
   This proposal supplies no generic amendment mechanism or new relation type.

## Out of scope

No removal or relocation of `candidate-package`, `public-install`,
`candidate_acceptance.py`, `release_qualification.py` or
`scripts/validate_governor_transition.py`. No release/adoption CI change,
retired exemption restoration, schema-1/2 support, general dashboard redesign,
performance project, lifecycle change, release, deployment or host update.
No accepted-artifact edit through this draft-authoring step. The proposed manual
activation is limited to the seven exact definitions and selected WO named here.

## Expected change surface

| Path | Purpose |
| --- | --- |
| `repository_tools/explorer_design/build_explorer_template.py` | Correct the runtime through the existing patch mechanism; preserve design exports. |
| `se_harness/engine/harness_explorer/index.template.html` | Regenerate the shipped UI. |
| `scripts/check_portable_release_surface.py` | Extend the existing package check; reuse its current CI caller. |
| `tests/test_dashboard_webui.py` | Check ID-independent selection and deterministic generation. |
| `tests/test_release_orchestration.py` | Check clean and contaminated packages, including embedded UI. |
| `tests/test_harnessctl.py` | Check the accepted minimal-install/Git-readiness sequence. |
| `docs/notes/harness-installation-and-upgrades.md` | Explain the sequence and observed readiness result. |
| `intent/INT-ECP-001.md`, `capabilities/CAP-ECP-003.md`, `requirements/REQ-ECP-012.md`, `requirements/REQ-ECP-013.md`, `specifications/SPEC-ECP-007.md`, `verification/VER-ECP-007.md`, `architecture/adr/ADR-ECP-005.md` under this domain | Activate only the exact reviewed definition replacements after explicit manual-amendment authority. |
| This WO, `DEC-ECP-003.md`, and the domain `README.md` | Record the bounded proposal and its dependency. |
| `evidence/WO-ECP-007/` | Retain implementation and review evidence after authorization. |

The proposed manual route preserves original bytes as
`evidence/WO-ECP-007/definition-revisions/2026-10-17/accepted/ID.txt`, uses the
seven existing definition paths for reviewed replacements, and records the actual
activation in that directory's `activation.json`. Each replacement links its
preserved predecessor by path, SHA-256 and original Git commit. No new artifact
ID or machine relation is invented. Earlier work keeps its original definition
meaning and evidence; this revision selects only remaining WO-ECP-007 work.
`DEC-ECP-003` remains open until that exact route is authorized and recorded.

The future VREC has no allocated ID. Check its actual record and declared evaluator-evidence paths after
preparation under the direct-verification scope rule; parent directories are not
authorized by that rule.

## Authorized decision envelope

After definition activation and explicit work approval, the executor may choose
the smallest implementation within the accepted rules and named paths. No new
tool or general JavaScript parser is needed. Changing the installation choice,
weakening checks or expanding scope requires review. Required commit-bound
assurance is proposed and still needs human confirmation for this scope.

Proposed review-publication grant for that later approval: push this selected
package from `codex/narrow-ecp-007` to a draft PR targeting `main` in
`mmzen/se_harness`, including the later push of a separately recorded verification
decision. This draft grants no publication authority or merge decision.

## Required verification

Use the accepted revision of `VER-ECP-007` before execution. Derive expected
results from requirements, not candidate output. Cover ID-equivalent graphs,
forbidden literals in Python and embedded UI, permitted documentation links,
deterministic Explorer generation, the built wheel, the accepted installation
sequence and damaged-attribute refusal. Preserve existing package protections.

Run the installation checks on Windows and Linux with the wheel installed outside
the disposable consumer. Reuse existing tests and CI; report missing or skipped
cases. Run repository-required regression, distribution and CLI checks, then the
released validation, scope and handoff checks. Candidate source is a test subject;
govern with the repository-selected released evaluator 0.23.0, through its absolute
Python path with `-I -m se_harness`, from outside the checkout.

## Evidence and completion

Retain commands, results, failures, candidate/wheel identities, platform results,
package inventories, historical-byte comparisons, the complete change set and
review assessment under `evidence/WO-ECP-007/`. Keep transient amendment proposals
outside the repository until an explicitly authorized revision route exists.

Report the evaluator's actual handoff result, effects, limitations and next typed
step. Prepare the required VREC only after the approved work and checks complete.
A prepared record is not human verification, merge or release approval.

## Stop conditions

Stop dependent approval or execution while `DEC-ECP-003` is open or accepted
revisions are not activated. Stop for uncovered
paths, changed semantics, failed checks, missing evidence or historical-byte
changes. Return to draft preparation for a concrete reviewed correction.

## Scope reconciliation

Reassessed against main `0b93e92ceabdb4cae85e1f4fdab943f955aa1c38` on 2026-10-17.
The original draft remains in Git history. WO-HBI-005 removed the self-hosting
hash class; WO-REB-028 retired predecessor bootstrap; WO-ECP-010/011 retired
migration machinery; WO-ECP-030 removed the recovery command; WO-HUP-012 enforced
the lock-schema floor; WO-LRE-002 replaced legacy exemptions with the evidence
floor. Those completed changes are not repeated. Active qualification and
adoption checks remain intact.
