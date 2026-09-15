+++
id = "SPEC-PLG-022"
type = "specification"
title = "Package complete native marketplaces from committed plugin inputs"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-15"
updated = "2026-09-15"
contract = "Compose the existing native package assembly with committed marketplace catalogs and listing materials, then check the exact contents offered for installation."

[relations]
specifies = ["REQ-PLG-038"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T13:40:15Z"
decided_by = "technical-owner"
reason = "The owner reviewed the four marketplace drafts and replied \"OK i approve the artifacts you can start\" on 2026-09-15. Record approval of this exact reviewed artifact in the named accountable role. This authorizes WO-PLG-023 execution under DR-015, not verification of a future candidate or a provider submission."
+++

# Package complete native marketplaces from committed plugin inputs

## Rules

- **PLG-MKT-001:** The distribution root contains Codex's
  `.agents/plugins/marketplace.json` and Claude's `.claude-plugin/marketplace.json`.
  Both catalogs are named `se-harness` and offer `verity-plane`. Sources resolve
  inside the distribution root to complete native plugin directories. They never
  reference the development repository's incomplete host overlays or an external
  shared directory. Preserve the existing native manifest formats.
- **PLG-MKT-002:** Use the existing released-input assembly for plugin 0.1.0 and
  the unchanged published SE Harness 0.18.0 wheel selected by RLS-SEH-027 and its
  independently obtained archive digest. Assemble shared skills and setup from
  one committed revision. Include the existing LICENSE through the committed
  assembly plan. Add the operator-brief display name and short description in
  its source metadata while preserving explicit-only invocation.
- **PLG-MKT-003:** Keep catalog assets and publication instructions under
  `release/plugin-marketplace/`. A small composition command reuses the existing
  assembly builder and acceptance functions. Place their unchanged output under
  `packages/`; catalogs point to `./packages/codex/verity-plane` and
  `./packages/claude/verity-plane`. Export catalog assets from the same source
  commit. Record source commit, wheel identity and final file digests. Acceptance
  compares files with those committed inputs and the released wheel, including
  the native archives. No manual post-assembly metadata overlay is accepted.
  Reject conflicting, redirected, escaped, missing or unexpected output paths.
  Preserve unrelated destinations and retain partial output for inspection.
- **PLG-MKT-004:** The installation guide documents the standard host marketplace
  add/install commands and the separate setup skill. State Python 3.11+, venv and
  ensurepip prerequisites. Setup installs the supplied wheel offline into its
  private environment. Plugin installation alone neither downloads the checker
  from PyPI nor initializes or upgrades a project. Existing project release
  selection remains authoritative. Shared setup instructions remain the source
  for detailed setup and repair steps.
- **PLG-MKT-005:** Check the actual local marketplace with both native hosts in
  disposable Windows profiles before proposing publication. Retain observed host
  versions and limitations. Publish the accepted distribution tree to
  `mmzen/se_harness`, ref `plugin-marketplace`, only through the applicable
  verified-coverage and external-action procedure. Never force a conflicting
  public ref. After publication, repeat standard Git-based installation against
  that ref in fresh profiles, compare installed contents with the accepted
  package, and only then report the remote route as checked.
- **PLG-MKT-006:** Prepare OpenAI skills-only submission materials and the supported
  Anthropic community submission materials using the same package identity.
  Include listing text, existing logo, starter prompts, reviewer cases and data
  behavior. Separate expected reviewer scenarios from tests actually run.
  Unconfirmed identity, support contact, public privacy/terms URLs, regions and
  owner attestations remain explicit publisher inputs. A prepared draft, Git
  publication and provider acceptance are separate recorded facts. No provider
  submission, legal attestation or provider approval is inferred from packaging.

## Simpler choice and compatibility

Two static catalogs plus composition of the existing builder satisfy the need.
Keeping the builder output intact preserves its acceptance checks and inventories.
The proposed `packages/` layout avoids copying or rewriting native package trees.
This work adds no installer, package registry, automatic hooks, runtime download,
new evaluator release, service, or second policy engine. Current public-catalog
formats are read from provider documentation; their ordinary validators are used.

SPEC-PLG-001, ARCH-PLG-001 and ADR-PLG-001 continue to govern the selected wheel
and shared package boundary, with their existing SPEC-PLG-021 amendments.
SPEC-PLG-016 governs installation guidance. No new architectural decision is
introduced by the catalog files. This specification adds marketplace behavior;
it does not amend historical approval or acceptance records.

## Examples

A fresh profile adds the local distribution and installs verity-plane; all
referenced skills and the wheel are present inside the host's cached plugin.
If a catalog points at a missing or escaping directory, acceptance fails and
the destination outside the distribution remains unchanged.

## Provider references checked on 2026-09-15

- [OpenAI packaging and repository marketplaces](https://developers.openai.com/plugins/build/plugins)
- [OpenAI submission](https://developers.openai.com/plugins/deploy/submission)
- [Claude marketplace distribution](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude community submissions](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace)

All PLG-MKT rules cover REQ-PLG-038. Provider directory acceptance is not an
implementation completion criterion; unresolved publisher inputs remain visible.
