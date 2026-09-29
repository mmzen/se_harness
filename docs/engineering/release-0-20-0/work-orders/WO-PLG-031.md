+++
id = "WO-PLG-031"
type = "work_order"
title = "Confirm public 0.2.2 delivery and reconcile current documentation"
status = "in_progress"
owners = ["mmzen"]
created = "2026-09-29"
updated = "2026-09-29"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification by approving the reviewed 0.20.0/0.2.2 release package; later release, publication and availability decisions rely on this work."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/release-0-20-0/work-orders/WO-PLG-031.md",
  "docs/engineering/release-0-20-0/evidence/WO-PLG-031/",
  "docs/engineering/release-0-20-0/verification-records/",
  "README.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/release-delivery-completion.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/instruction-architecture/README.md",
  "tests/test_progressive_documentation.py",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py"
]

[relations]
implements = ["REQ-RLO-019", "REQ-RLO-020"]
specifications = ["SPEC-RLO-006"]
verification = ["VER-PLG-029"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T17:32:13Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the reviewed seven-artifact 0.20.0/0.2.2 release package, required commit-bound verification, stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and existing 0.19.0 role encoding. Reviewed SHA-256 f86b461c68312da6ac89a1cfb6b02154295ae08b86ecd710b79098605c6ae954; approval input SHA-256 b292643fa27cc608db189fe2a522e9b289601db09baaf249f7145fb8513e8ec9. Only the confirmed assurance classification was added to work orders. Legacy label engineering-owner transports the human decision; Codex applies it. Exact candidate verification, RLS release, merge, publication, markers and adoption remain separate."
scope_paths = ["docs/engineering/release-0-20-0/work-orders/WO-PLG-031.md", "docs/engineering/release-0-20-0/evidence/WO-PLG-031/", "docs/engineering/release-0-20-0/verification-records/", "README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/instruction-architecture/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-29T19:47:43Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the unchanged mmzen-approved public 0.2.2 delivery observations and documentation work after VREC-PLG-025 verification, merged PR 500 and authorized publication with exact public byte readback. User reconfirmed WO-PLG-031 approval."
+++

# Confirm public 0.2.2 delivery and current documentation

## Confirmed assurance

Commit-bound verification is `required`. Human mmzen confirmed the proposed
classification with "I approve" in response to the seven-artifact release
package review. The assurance metadata records that decision; Codex applies it.

## Objective and prerequisites

Establish that users can install and update to the reviewed plugin 0.2.2 with
public evaluator 0.20.0. Begin after the exact WO-PLG-030 distribution has passed
human verification and its separately authorized marketplace publication.
Current main must contain the reviewed release inputs. This work is downstream
of the evaluator release and is excluded from its pre-publication aggregate.

## In scope

1. Resolve the actual public plugin-marketplace ref and compare its commit,
   catalogs, manifests, inventories, archives and bundled wheel with the
   qualified distribution. A differing ref or content is a failure.
2. Exercise public fresh installation and 0.2.1-to-0.2.2 update on both Windows
   CLIs in disposable profiles. Retain exact host versions, starting source,
   loaded content and evaluator identity. Apply VER-PLG-029's native checks.
3. Correct the listed current source documentation to state actual availability,
   install/update commands, package/evaluator versions and observed limits.
   Check source and package-relative links in their proper contexts. The already
   qualified packaged READMEs stay unchanged; if they need a correction, return
   to a new reviewed assembly instead of editing public bytes in place.
4. Correct only version/status assertions in the two named documentation tests
   where necessary. Preserve their receipt, truthfulness and link checks.
5. Retain the reviewed current plan and observations in this work's evidence
   directory, including actual evaluator, marketplace, documentation, Pages and
   latest/last results. Keep changed plan versions and their prior observations;
   bind reuse explicitly after assessing applicability. A deferred or unobserved
   surface remains incomplete.
6. Complete implementation and capture the final public-delivery VREC at the
   clean documentation/evidence candidate. After human verification and separate
   integration authority, retain the merged-document readback and final report
   as append-only delivery receipts outside the bound candidate evidence.

## Decision envelope

Approval authorizes the local work, read-only public checks, disposable host
profiles, local commits, evidence, completion and verification preparation. The
proposed review envelope includes ordinary pushes of work/public-marketplace-022
and a draft PR to main in mmzen/se_harness. It includes no force push.
Human verification and merge remain separate exact decisions. Approval also
confirms required assurance and the 0.19.0 legacy encoding that preserves mmzen
and the actual human decision in transition reasons.

After an authorized integration is observed, the same bounded scope permits
append-only closeout receipts and their ordinary review-branch push/draft PR.
A receipt merge does not create another receipt obligation or VREC cycle.

## Constraints, verification and evidence

Use the external released 0.19.0 evaluator, VER-PLG-029, SPEC-RLO-006 and the
existing check_release_delivery.py command. Expected identities are reviewed
inputs, not values copied from an unexpected remote result. Preserve historical
records and failures. Follow the evidence policy under evidence/WO-PLG-031/.
No new architecture or decision is needed; this executes the accepted delivery
procedure without adding an executable component or authority boundary.

## Out of scope and stops

No implicit marketplace retry, version change, evaluator release, marker move,
real user-profile change, repository adoption, guide deletion or credential
transfer. Stop the affected route for identity mismatch, inaccessible native
host/authentication, changed qualified input or an edit outside these paths.
Report who owns the pending step. Do not label unsupported hosts as passed.

## Completion report

Report exact public versions and commits, both hosts' observed fresh/update
routes, documentation commit, final five-surface result and any limits. The
full delivery may be called complete only after all declared surfaces pass.
Repository adoption and stock-pointer cleanup remain separate next work.
