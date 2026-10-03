+++
id = "WO-HUP-028"
type = "work_order"
title = "Adopt released evaluator 0.22.0"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification: future engineering and release decisions depend on the selected evaluator, CI pin and source boundary."
decided_by = "mmzen"

[execution_scope]
paths = [
  ".engineering-harness.toml",
  ".engineering-harness.lock",
  ".github/workflows/engineering-harness.yml",
  "pyproject.toml",
  "se_harness/__init__.py",
  "README.md",
  "docs/engineering/README.md",
  "docs/engineering/self-hosting-boundary/SELF_HOSTING.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/release-delivery-completion.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-028.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-005.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-028/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-028-evaluator-upgrade.json",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-027.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-027-evaluator.json",
]

[relations]
implements = ["REQ-REB-027", "REQ-IAR-031"]
specifications = ["SPEC-REB-012", "SPEC-IAR-016"]
architecture = ["ARCH-REB-011", "ADR-REB-011", "ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-HUP-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T07:09:21Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" to the reviewed WO-HUP-028 and VER-HUP-005 package, including required commit-bound verification, repository adoption of 0.22.0, unpublished source 0.22.1 and review branch push/PR. Reviewed file SHA-256 fd5793a291f80b96d06374fa57c1283bf431a2a832ae88f966d8d6ea01368fa6. Human verification acceptance, merge, host updates, provider configuration and new release/publication remain separate."
scope_paths = [".engineering-harness.toml", ".engineering-harness.lock", ".github/workflows/engineering-harness.yml", "pyproject.toml", "se_harness/__init__.py", "README.md", "docs/engineering/README.md", "docs/engineering/self-hosting-boundary/SELF_HOSTING.md", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/release-delivery-completion.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-028.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-005.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-028/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-028-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-027.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-027-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-03T07:10:26Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start the unchanged adoption scope under human mmzen approval recorded on 2026-10-03."
+++

# Adopt released evaluator 0.22.0

## Objective

Use exact public evaluator 0.22.0 for this repository, its external instructions
and its CI. Preserve repository-owned content and formal history. Keep source
development distinct by advancing both source version fields to unpublished 0.22.1.

Human mmzen requested: "Merged, you can start adoption" after PR #531 completed
the 0.22.0 public-delivery receipts. Reuse that adoption direction. This draft
makes its path scope, development-version change and assurance proposal explicit;
it does not claim the human approved these newly prepared artifacts.

## Exact inputs

- Base: `b9821e3a3ef3f821f36cc92da7fa4ce900f7e750`, including merged PR #531.
- Current evaluator: public 0.21.0, schema 5, `released-resources-v1`.
- Target: released RLS-SEH-032, candidate `abbec12ac5524c8adfb28693f846dd59de88f759`.
- Wheel: `se_harness-0.22.0-py3-none-any.whl`.
- Wheel SHA-256: `44543f242ed19bb30cfd65da415372a87508a6e439204d7f3e37f9f45aefe4e4`.
- Target payload SHA-256: `b4464e0c55814ee62a6e844d712503188493dacf841aeac90d5f270e8c6836c9`.

## In scope

1. Prepare the exact target privately, preserving the existing 0.21.0 environment.
2. Repeat and inspect the target upgrade preview. Apply only the two selection-file
   updates and retain the canonical transaction at the declared evidence path.
   No integration replacement or resource retirement is selected.
3. Change only the owner CI version pin to 0.22.0. Preserve its download,
   digest-check and wheel-file installation procedure.
4. Change `pyproject.toml` and `se_harness/__init__.py` to 0.22.1. This avoids
   PRE008 when source and released evaluator both identify as 0.22.0. It does
   not build or publish 0.22.1.
5. Update the seven named current guides/indexes to the actual selected evaluator,
   unpublished source version and completed release receipts. Keep historical
   descriptions and accepted host-test omissions explicit. The single-approval
   release route still needs separately reviewed provider configuration.
6. Run VER-HUP-005, reactivate this exact checkout through the existing session
   helper after apply, record completion and capture the exact adoption candidate.

## Expected change surface

Twelve selection, CI, source-version and current-documentation files; this work
order, VER-HUP-005 and their bounded evidence; planned VREC-HUP-027 and its fixed
evaluator JSON. The work-order scope includes all these generated outputs.
The installer preview leaves `.gitattributes`, `.gitignore`, the PR template and
the existing CI seed unchanged. The separately listed CI pin is an owner edit.

## Verification and evidence

VER-HUP-005 defines the checks. Propose **required commit-bound verification**:
future engineering and release decisions rely on the selected evaluator and CI.
The human must confirm this classification with approval. No `decided_by` value
is fabricated in this draft. Reserve VREC-HUP-027 only after checking availability
again at capture. Use the actual preparing actor; human acceptance remains separate.

Retain commands, versions, digests, results and failures under evidence/WO-HUP-028/.
Use `evidence/WO-HUP-028-evaluator-upgrade.json` for the installer transaction and
`evidence/VREC-HUP-027-evaluator.json` for generated assurance evidence. Preserve
old release records, verification records, decisions and their bound bytes.

## Authorized decision envelope

Proposed package approval authorizes bounded local execution, the listed source
version and CI changes, checks, evidence, local commits and verification preparation.
It also authorizes review-branch pushes and a PR from `work/adopt-0-22-0` to
`mmzen/se_harness:main`, so the branch is accessible when verification is requested,
plus the later commit recording the matching human decision. Do not infer merge,
verification acceptance, another release or provider changes from this approval.

## Out of scope

Runtime or installer behavior changes; source instruction/template changes;
host plugin installation/update, authentication or trust changes; native Claude
or desktop qualification; release publication, tags or marketplace changes;
provider configuration and complete-release route activation. Do not recreate
ENGINEERING_HARNESS.md, copied templates or retired guide files. AGENTS.md stays intact.

## Stop conditions

Stop for a changed target identity, customized/conflicting file, additional installer
write, failed required check, new source/test correction or scope outside the listed
paths. Prepare a bounded correction when necessary; do not weaken tests or rewrite
accepted history. A same-selection repeat must produce no changes.

## Simplicity

Use one work order and one verification contract. Reuse the accepted upgrade and
external-resource definitions, installer, activation helper and existing tests.
No new product mechanism, template copy, policy service or architecture is needed.

## Completion report

Report selected release and resource identity, installer writes, preserved owner
content, source/CI versions, actual checks, limitations, exact candidate and the
remaining human verification decision. Distinguish helper/resource readback from
native startup or desktop qualification; unrun tests remain unverified.
