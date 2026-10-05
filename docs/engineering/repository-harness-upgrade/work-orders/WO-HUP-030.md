+++
id = "WO-HUP-030"
type = "work_order"
title = "Adopt released evaluator 0.22.1"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because later engineering and release decisions rely on the evaluator selection, CI pin, source boundary and adoption guidance."
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
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/release-0-22-1/README.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/release-delivery-completion.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/harnessctl-reference.md",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-030.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-025.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030-evaluator-upgrade.json"
]

[relations]
implements = ["REQ-REB-027", "REQ-IAR-031"]
specifications = ["SPEC-REB-012", "SPEC-IAR-016"]
architecture = ["ARCH-REB-011", "ADR-REB-011", "ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-HUP-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-05T10:40:00Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Approve package, verification and review PR\" to the exact WO-HUP-030 / VER-HUP-025 review: public evaluator 0.22.1 adoption, unpublished source 0.22.2, named CI/documentation/test updates, required commit-bound verification and ordinary review pushes/draft PR from codex/adopt-0-22-1 to mmzen/se_harness:main, including the later recorded verification decision. Human verification acceptance, merge, host-plugin updates and HAG contract amendment remain separate. Reviewed bytes matched; only confirmed assurance fields were added before preview. Reviewed SHA-256 03bd64a07c100532a29d5c11743b604feb28678e12b17df502b06d233c8d00ff."
scope_paths = [".engineering-harness.toml", ".engineering-harness.lock", ".github/workflows/engineering-harness.yml", "pyproject.toml", "se_harness/__init__.py", "README.md", "docs/engineering/README.md", "docs/engineering/self-hosting-boundary/SELF_HOSTING.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/release-0-22-1/README.md", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/release-delivery-completion.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/harnessctl-reference.md", "tests/plugin_integration/package_assembly/test_refresh_guidance.py", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-030.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-025.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030-evaluator-upgrade.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-05T10:45:08Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Adopt released evaluator 0.22.1

## Objective

Use exact public evaluator 0.22.1 for this repository, its external instructions
and CI. Preserve owner content, accepted artifacts and historical evidence.
Advance development source to unpublished 0.22.2 so CI can distinguish it from
the governing release.

Human mmzen requested "Go adopt" after PR #539 merged the verified delivery
closeout. This draft makes the path scope, source-version change, assurance and
review-publication proposal explicit. It does not infer approval of these new
records or confirmation of their assurance classification.

## Exact inputs

- Trusted base: `00708eb1000020cf4b1672ffe9bfc684b0c6d51c`, merged PR #539.
- Current selection: released 0.22.0, schema 5, `released-resources-v1`.
- Target: RLS-SEH-033, candidate `4f640284ec496b88cd7aa4ba88ca537d9374a2f8`.
- Wheel: `se_harness-0.22.1-py3-none-any.whl`.
- Wheel SHA-256: `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053`.
- Payload SHA-256: `0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff`.
- Public-delivery verification: VREC-RLS-004, verified by mmzen and merged.

## In scope

1. Prepare and validate the exact target in its separate private environment.
   Preserve the installed 0.22.0 environment.
2. Recheck the target upgrade preview. Apply only its two selection-file changes
   with the declared canonical transaction path. Select no integration replacement,
   resource retirement or managed-file overwrite.
3. Update only the owner CI version pin to 0.22.1. Preserve the digest-checked
   wheel-file installation procedure and provider controls.
4. Change both source versions to 0.22.2. The existing evaluator-facts check
   reports PRE008 when source and governor both identify as 0.22.1. This does
   not build or publish another release.
5. Update the named current guides to actual public 0.22.1 / 0.2.6 delivery and
   repository adoption. Preserve dated older observations, published snapshots
   and the accepted Codex Windows desktop omission.
6. Update the existing refresh-guidance test's public expectations to independent
   RLS-SEH-033 and WO-RLS-042 receipts. Keep wrong identities, contradictory
   observations, premature claims and broken links rejected.
7. Run VER-HUP-025, reactivate this checkout after apply, record completion and
   capture the exact adoption candidate for human verification.

## Expected change surface

| Paths | Reason and limit |
| --- | --- |
| `.engineering-harness.toml`, `.engineering-harness.lock` | Installer selection and resource identity, from the two-file preview. |
| `.github/workflows/engineering-harness.yml` | One evaluator pin; preserve download and integrity checks. |
| `pyproject.toml`, `se_harness/__init__.py` | Matching unpublished 0.22.2 source versions; no executable behavior change. |
| `README.md`, `docs/engineering/README.md`, `docs/engineering/self-hosting-boundary/SELF_HOSTING.md` | Current public release, repository selection and development boundary. |
| `docs/engineering/repository-harness-upgrade/README.md`, `docs/engineering/release-0-22-1/README.md` | Current adoption and completed delivery links; preserve prior decisions. |
| `docs/notes/developing-se-harness.md`, `docs/notes/harness-installation-and-upgrades.md`, `docs/notes/release-delivery-completion.md` | Current selection, development version and delivery status. |
| `docs/notes/plugin-installation-guide.md`, `docs/notes/plugin-marketplace-publication.md`, `docs/notes/harnessctl-reference.md` | Current public/selected versions and actual CLI availability; retain historical snapshots. |
| `tests/plugin_integration/package_assembly/test_refresh_guidance.py` | Existing public assertions name 0.22.0 receipts; use independently retained current receipts without weakening negative cases. |
| WO-HUP-030, VER-HUP-025, the packet directory and canonical transaction | Approval, actual checks, installer evidence and completion. |

The preview preserves `.gitattributes`, `.gitignore`, the PR template and CI.
The CI pin is the separately declared owner edit. No other test, product source,
template, manifest, workflow or packaging change is covered.

The future VREC ID is unresolved until allocation. Existing scope rules admit
the record directly verifying WO-HUP-030 and its declared evaluator JSON, not
their parent directories. Check the actual returned paths before capture.

## Required verification and evidence

VER-HUP-025 supplies the checks. Propose required commit-bound verification
because later decisions depend on the resulting selection, CI and instructions.
Only the human can confirm this classification; `assurance.decided_by` is absent
until that decision. Do not invent an actor to satisfy approval checks.

Retain commands, identities, changes, checks, skips and failures under
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/`.
Use `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030-evaluator-upgrade.json`
for the canonical installer transaction. Preserve pre-existing bound bytes.

## Authorized decision envelope

Proposed approval covers bounded local implementation, the listed CI/source
version changes, current documentation/test expectations, checks, local commits,
completion and verification preparation. It also proposes ordinary review pushes
and a draft PR from `codex/adopt-0-22-1` to `mmzen/se_harness:main`, including the
later decision-only push and marking it ready after matching human verification
is remote. Human verification acceptance and merge remain separate.

Session activation of the adopted checkout is included. No force-push, release,
tag, marketplace, provider-setting, authentication or installed host-plugin
change is covered. No external action is performed during draft preparation.

## HAG dependency boundary

Adoption makes the published fixes available but does not amend the hosted
contract. SPEC-HAG-003 and VER-HAG-001 still pin 0.22.0. Preserve them,
WO-HAG-001, DEC-HAG-001 and historical HAG evidence unchanged. Do not resume
dependent HAG execution or claim its scenarios passed through adoption.

The selected release lacks a supported linked-definition amendment command and
relation. Keep the exact replacement/preserved-version proposal transient until
a reviewed supported route or explicitly authorized bounded exception exists.
The existing `extend-evaluator` choice is known and must not be asked again.
Recording it and integrating adoption into PR #535, with its current target
preserved, remain separate from this repository-adoption package.

## Stop conditions

Stop for changed public identities, a conflicting owner file, additional
installer writes, a failed required check or uncovered scope. Do not weaken
checks, alter accepted definitions or change comparison bases to pass. Inspect
uncertain writes before retrying. Repeating the same selection must be unchanged.

## Simplicity and completion

Use one work order and one verification contract with the accepted upgrade and
external-resource definitions. Add no mechanism, dependency or instruction copy.
Report selected identities, installer writes, source/CI versions, preservation
checks, exact candidate, evidence, limitations and the next decision.
