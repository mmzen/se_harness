# Verity Plane catalog submission materials

These materials accompany plugin 0.1.0 and its published SE Harness 0.18.0 wheel.
They are drafts for provider review. A Git marketplace installation does not
establish approval or availability in a provider directory.

## Upload and source inputs

- OpenAI archive: `packages/verity-plane-codex.zip`, from the distribution root.
- Claude archive: `packages/verity-plane-claude.zip`.
- Complete Claude source directory: `packages/claude/verity-plane` at the
  eventual immutable commit of `mmzen/se_harness:plugin-marketplace`.
- Package identity and file hashes: `PACKAGE-IDENTITY.json` at the root.
- [Existing project logo](verity-plane-logo.png) and [reviewer cases](reviewer-test-cases.md).

Use the same tested file tree in a portal. Inspect and retest any converted
manifest. The development source path `plugins/verity-plane/claude-code` alone
is incomplete and must not be submitted as the plugin.

## Listing copy

**Name:** Verity Plane

**Short description:** Govern AI coding work with explicit scope and verification.

**Description:** Verity Plane connects your coding agent to SE Harness. Prepare
the checker, connect a repository, inspect engineering artifacts, work within
approved scope and retain verification evidence. Repository instructions and the
selected released evaluator determine the workflow. Human owners decide scope,
assurance and delivery. Five skills and the published checker wheel are bundled;
an existing Python 3.11+ installation is required.

**Category:** Developer Tools / Development, using the closest portal category.

**Publisher label in source:** SE Harness; publisher identity requires confirmation.

**Website suggestion:** https://github.com/mmzen/se_harness

**Support suggestion:** https://github.com/mmzen/se_harness/issues

**Starter prompts:**

1. Set up SE Harness in this project with the bundled released checker.
2. Explain this repository's engineering state and next decision.
3. Draft a bounded work order for my requested change.

**Initial release notes:** Standard marketplace packaging of shared setup,
orientation, change, evidence and operator-brief skills. The supplied checker
wheel installs offline when setup is invoked. Plugin installation alone does
not initialize or upgrade a project. There are no automatic tool/session hooks,
remote MCP service or plugin-specific login.

## OpenAI

Use the [plugin portal](https://platform.openai.com/plugins), select **Skills only**,
and upload the checked native archive and listing materials. The existing
`.codex-plugin/plugin.json` compatibility manifest remains supported. The portal
review and any required scanner/model checks are separate from local acceptance.
After provider approval, the owner chooses publication in the Plugins Directory.
See the [submission procedure](https://developers.openai.com/plugins/deploy/submission).

## Anthropic

Submit through the [Console form](https://platform.claude.com/plugins/submit) or
[organization form](https://claude.ai/admin-settings/directory/submissions/plugins/new)
using the complete published plugin directory and immutable Git commit.
Third-party submissions go to the reviewed **Claude community marketplace**.
The official catalog is curated separately and has no direct application route.
See [Claude distribution guidance](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace).

## Publisher inputs still needed

- Confirmed publisher identity and the appropriate provider account role.
- Confirmed website and support contact, plus public privacy-policy and terms URLs.
- Intended countries/regions and confirmation of logo suitability in each portal.
- Owner review of policy attestations and the completed application.

No missing identity, legal URL, attestation or provider approval is supplied by
this draft. Record submission and publication outcomes only when observed.

## Data behavior for reviewers

The skills read repository files and call the selected local checker. Requested
initialization and workflow operations can write project artifacts. Setup writes
a private environment outside the project. Requested plugin ownership replaces
the named disposable generated skill copies. The plugin defines no remote MCP
endpoint or plugin-specific account. The coding host's own account, permissions
and model data policies continue to apply; do not promise that repository text
never reaches the host's model service.

Use a disposable project. [Reviewer scenarios](reviewer-test-cases.md) describe
expected agent behavior; measured direct CLI results belong to the work-order
evidence and do not establish that those model-driven scenarios have run.
