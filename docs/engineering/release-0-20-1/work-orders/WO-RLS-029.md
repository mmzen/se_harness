+++
id = "WO-RLS-029"
type = "work_order"
title = "Confirm public 0.2.3 delivery and reconcile current documentation"
status = "in_progress"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved the reviewed work-order and verification-contract pair with required commit-bound verification; later package and delivery decisions depend on the changed manifests, instructions and retained evidence."
decided_by = "mmzen"

[execution_scope]
paths = [
  "README.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/release-delivery-completion.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/instruction-architecture/README.md",
  "docs/engineering/release-0-20-1/",
  "tests/test_progressive_documentation.py",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py",
]

[relations]
implements = ["REQ-RLO-019", "REQ-RLO-020"]
specifications = ["SPEC-RLO-006"]
verification = ["VER-RLS-029"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T05:48:10Z"
decided_by = "engineering-owner"
reason = "Human mmzen approved the reviewed package and confirmed: Yes\u2014approve both 028 and 029 pairs. Approves WO-RLS-028, VER-RLS-028, WO-RLS-029 and VER-RLS-029, required commit-bound verification, the stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and the existing 0.19.0 engineering-owner encoding retaining mmzen as the human decision-maker. Reviewed SHA256 74f6ed84c045d9e557f7b79c76f5bdb7b2861eaf33250f22d8cbd7cd26e550a5; transition input SHA256 eabc0d95cbf1066200077a8ae3baae96c820270c825c8092e9a38d03c571bb1e. Only confirmed assurance metadata was added to work orders. Codex applies the matching decision. Human verification, merges, release, publication, release markers and adoption remain separate."
scope_paths = ["README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/instruction-architecture/README.md", "docs/engineering/release-0-20-1/", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T09:41:21Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Confirm public 0.2.3 delivery and reconcile current documentation

## Objective and prerequisites

Demonstrate that users can install and update to the accepted plugin 0.2.3
with public evaluator 0.20.1, and make current documentation match those facts.
Start after WO-RLS-028's package is verified and its exact marketplace
publication is separately authorized and observed. Use a separate current-main
checkout, its confirmed released evaluator and unchanged transported approvals.
No maintenance source merge or repository adoption is implied.

## In scope

1. Read the public marketplace commit and compare the complete tree with the
   accepted distribution. Exercise public fresh installation and update from
   0.2.2 on Windows Codex CLI and Claude Code in disposable profiles.
2. Retain loaded paths, installed-content digests, evaluator identity, native
   instruction-delivery observations, host versions and failures under VER-RLS-029.
3. Update only the listed current documentation and domain indexes. State observed
   0.20.1/0.2.3 availability, install/update routes, public receipts and support
   limits. Keep unreleased minimal-layout work clearly separate. Preserve useful
   historical information and unrelated content on main.
4. Adjust only obsolete version/status expectations in the two named documentation
   tests when the new observed facts require it. Preserve receipt, link and
   truthfulness checks. No unrelated test or implementation correction is covered.
5. Preserve earlier delivery plans and observations. Prepare the final plan and
   assess all five surfaces with the existing closeout checker: evaluator,
   marketplace, documentation, demonstration and release markers.
6. Complete the bounded documentation/evidence change and prepare its VREC for
   human verification. After authorized integration, retain append-only public
   documentation and final closeout receipts outside frozen VREC evidence.
   Integrating such unchanged receipts alone does not require another VREC.

## Proposed assurance and decision envelope

Commit-bound verification is proposed as required because consumers rely on the
current instructions, evidence and delivery claims. Human confirmation remains
pending; the agent has not supplied an assurance decision.

Approval would authorize the local work, read-only public observations,
disposable profiles, local commits, checks, evidence and VREC preparation.
The proposed review envelope includes ordinary pushes of
work/public-marketplace-0-2-3 and a draft PR to main in mmzen/se_harness,
including append-only closeout receipts after their prerequisites pass.
Human verification and each merge remain separate decisions. No force push,
publication, marker mutation or change to real user profiles is authorized.
Use the exact selected evaluator and preserve mmzen's actual decisions when a
legacy role label is required; an actor argument does not grant authority.

## Constraints, evidence and stops

Reuse SPEC-RLO-006 without a new tool, framework or architecture. The domain
path covers this work's records, generated VREC companions and delivery receipts;
it permits no rewrite of accepted definitions, prior histories or frozen evidence.
Use evidence/WO-RLS-029/, verification-records/ and evidence/ in this domain.
Keep credentials, environments and disposable repositories outside the repository.

Follow VER-RLS-029. Stop the affected route for mismatched public identity,
missing native access, changed qualified package, moved integration baseline,
failed required checks or an edit outside the declared scope. A package correction
requires new assembly and verification; do not alter public package bytes.
Do not manufacture success from an earlier version's result or a skipped host.
Repository adoption and successor qualification remain separate work.

## Completion report

Report exact public versions, source/public/documentation commits, both hosts'
fresh/update results, limitations and the five-surface closeout. Delivery is
complete only when every declared surface has matching retained evidence.
Name remaining work and its owner when any surface is incomplete.
