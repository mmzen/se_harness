+++
id = "VER-DST-029"
type = "verification"
title = "Verify the public README with native plugin onboarding"
status = "approved"
owners = ["assurance-owner", "documentation-owner"]
created = "2026-09-15"
updated = "2026-09-16"

[relations]
verifies = ["REQ-DST-069"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T05:51:30Z"
decided_by = "assurance-owner"
reason = "The assurance owner approved the named verification contract in the same explicit approval response; reviewed bytes still match."
+++

# Verification: Public README with native plugin onboarding

## Scope and independence

Verify the new README under the existing REQ-DST-069 and SPEC-DST-024. This
contract selects fresh evidence for WO-DOC-016; VER-DST-024 and its historical
publication inputs and evidence remain unchanged.

Expected presentation and authority boundaries come from SPEC-DST-024 and the
installed 0.18.0 policy. Expected native installation commands and setup effects
come from the released plugin and the retained public Git acceptance in
`docs/engineering/plugin-integration/evidence/WO-PLG-023/publication-2026-09-15/README.md`,
covered by VREC-PLG-020 for its candidate and separately observed publication.
Do not use the rewritten README as its own source of expected behavior.

The owner reviews the proposed content and render. Agent-run checks are technical
evidence; the assurance owner separately decides the resulting ready VREC.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-DST-069 | Inspection, existing tests, demonstration | Reviewed README and render, input/output hashes, existing public-onboarding and progressive-documentation checks, native-command comparison, released CLI help | Within the existing word/line/heading budgets; branding and images preserved; installation is usable; authority and current-versus-vision claims are accurate; every local link resolves. |

## Acceptance checks

- Compare README.md with the owner-reviewed proposal and preserve the existing
  logo and both Explorer PNGs byte-for-byte.
- Run the existing public-onboarding and progressive-documentation tests. Check
  links, anchors, fences, image readability, layout and the current workflow.
  Do not add tests that merely pin the new prose or duplicate plugin acceptance.
- Compare the four native commands with the retained public Git acceptance and
  the published distribution at ed68b30c88043773be929540b7b10ae537957c2d.
  Plugin 0.1.0 supplies released evaluator 0.18.0; setup installs its wheel offline
  into a private environment. Reject claims of automatic PyPI download, automatic
  project initialization/upgrade, or an approved provider-catalog listing.
- Confirm the init and doctor examples against both the candidate parser and the
  isolated released 0.18.0 CLI. Keep the PyPI path and pinned-project upgrade link.
- Run the source suite, release-distribution validator, candidate CLI help,
  released doctor and graph validation, phase preflight and scoped handoff checks
  required by AGENTS.md. Retain any failure with its resolution or explicit
  unresolved status; a required failing check blocks completion.
- Review the final diff and run git diff --check. Confirm the complete changed
  path set fits WO-DOC-016.

## Evidence and pass criteria

Retain the approved input, hashes, command arguments, outcomes and content/render
review under `docs/engineering/harness-distribution/evidence/WO-DOC-016/`.
Identify Windows and the exact Python, candidate and isolated released evaluator
versions. Existing plugin evidence may be cited for unchanged commands and package
inputs; rerun only when the compared inputs or an unresolved concern require it.

Pass requires the reviewed README to satisfy the existing presentation contract
and all required checks. Prepare VREC-DOC-008 against the clean implementation
commit, selecting only WO-DOC-016 and this verification contract.

## Limits

This work verifies documentation, not new plugin behavior, another host platform,
a model-driven session, a provider submission, or a package release. Public README
readback follows a separately authorized PR merge; record it as publication
evidence after that action without rewriting candidate verification facts.
