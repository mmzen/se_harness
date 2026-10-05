+++
id = "WO-RLS-044"
type = "work_order"
title = "Prepare accurate release documentation before the frozen plan"
status = "draft"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"

[execution_scope]
paths = ["README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "release/plugin-marketplace/README.md", "docs/engineering/release-0-22-1/"]

[relations]
implements = ["REQ-RLO-019", "REQ-RLO-020"]
specifications = ["SPEC-RLO-006", "SPEC-RLO-007"]
verification = ["VER-RLS-005"]
+++

# Prepare accurate release documentation before the frozen plan

## Objective

Prepare six source documentation files that remain accurate before and after
0.22.1 / 0.2.6 publication. The frozen delivery plan must not lock in claims
that qualification is still running or that 0.22.0 is permanently current.

## In scope

Apply the concrete documentation proposal under evidence/WO-RLS-044/. Distinguish
dated 0.22.0 / 0.2.5 observations, verified 0.22.1 / 0.2.6 qualification, actual
release authority and public delivery. Direct readers to the release record,
public package identity and named delivery evidence. Correct stale work-order
and verification references for the 0.2.6 installation/publication procedures.
Keep the accepted desktop omission explicit; public tests remain outstanding
until observed. Create a stable delivery-evidence index before plan freeze.

This is source documentation preparation, independently verified before the
complete-release request. It does not change the binary candidate or REL-SEH-035
membership. WO-RLS-042 retains publication and its post-publication observations.
The fixed plan may select a later documentation commit while preserving candidate
4f640284ec496b88cd7aa4ba88ca537d9374a2f8 and VREC-SEH-033.

## Out of scope and constraints

No executable, test implementation, template, CI, provider, manifest, dependency,
version, assembled package, archive or inventory edit. No rebuild or rebinding of
verified evaluator/plugin payloads. No accepted definition amendment, changed
release membership, adoption, hosted service, new waiver or fabricated test pass.
The existing guide already distinguishes immutable packaged README snapshots from
current source guidance. Preserve those package bytes and disclose their older
preparation wording; do not represent the source corrections as delivered package
changes. No new architecture or publication mechanism is needed.

## Proposed authority and assurance

Propose required commit-bound verification because the release decision will rely
on the accuracy of these documents. The draft does not record a human classification.
After approval, Codex may apply the reviewed correction, run checks, retain evidence,
commit, record completion and prepare its independent verification record.

Include ordinary review pushes and updates to PR #536 from
mmzen/se_harness:codex/release-0-22-1 to main, and its later verification-decision
update. Existing release review authority is reused where it matches. No merge,
public release, public marketplace update or force push is granted here. Verification
acceptance and the frozen complete-release decision remain separate human decisions.

## Expected change surface

| Path | Purpose |
| --- | --- |
| README.md | Separate verified qualification, historical observations and live delivery status. |
| docs/notes/plugin-installation-guide.md | Select the release by evidence; explain immutable package snapshots and truthful support. |
| docs/notes/plugin-marketplace-publication.md | Correct provider state and 0.2.6 procedure references; preserve frozen-plan semantics. |
| release/plugin-marketplace/README.md | Correct current source guidance without replacing staged bytes. |
| plugins/verity-plane/codex/README.md | Correct qualification and desktop statements in source guidance. |
| plugins/verity-plane/claude-code/README.md | Correct qualification and desktop statements in source guidance. |
| docs/engineering/release-0-22-1/ | This bounded package, review and raw evidence under evidence/WO-RLS-044/, stable evidence/WO-RLS-042/README.md, status index, generated VREC and fixed evaluator companion, and prepared delivery inputs. |

The release-domain prefix covers fixed evaluator evidence destinations and the
separate source-documentation verification record whose ID is allocated on capture.
It does not permit changes to historical records, accepted definitions or unrelated
work. Inspect the actual generated paths before writing. Existing documentation
tests, builder consumers, frozen-plan validator and publisher hash comparisons were
inspected. Their implementations need no edit; a failure outside this scope stops
the affected correction. All scratch proposals/builds stay outside the repository;
the reviewed patch and evidence are retained at the prescribed paths.

## Required verification and evidence

Follow VER-RLS-005. Review claims against independently retained VREC-SEH-033,
DEC-RLS-009/RISK-RLS-007, public 0.2.5 receipts and provider readback. Run existing
documentation tests and repository checks. Check local and assembled links in their
actual contexts. Compare all six before/after files, and confirm the complete Git
diff has no executable or payload edits. Retain source, commands, outputs, failures,
digests and the manual criteria assessment under evidence/WO-RLS-044/.

## Stop and completion

Stop on uncovered paths, changed approved inputs, an unsupported source/package
claim or a required rule that would need a waiver. Do not change a frozen plan or
bound package to clear a result. Completion means the six documents and stable
status index are checked and ready for independent human verification. Report the
exact documentation candidate, observed checks, unverified limits and evaluator's
next step. Release delivery remains pending until its own grant and observations.
