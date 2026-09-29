# Prepare and publish the Verity Plane marketplace

WO-PLG-026 and WO-PLG-027 prepared the 0.2.1/0.19.0 package and guidance,
verified by VREC-PLG-023 and integrated in PR #496. WO-PLG-028 covers public confirmation. Its verification and the selected
external-action procedure govern delivery. These commands grant no approval.

## Assemble committed inputs

Use the existing released SE Harness 0.19.0 wheel, independently obtained from
the published release. Its SHA-256 is
`43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8`.
RLS-SEH-028 is retained at governance commit
`c4d9036fdaab378f08fe2db68978126f66ab961e`.

From the source checkout, replace `SOURCE_COMMIT`, `WHEEL`, `CHECKER_PYTHON` and
`NEW_OUTPUT` below. The source commit must contain the approved marketplace
implementation. Use full commit IDs and absolute, quoted filesystem paths.
`CHECKER_PYTHON` is the external released evaluator's Python; output stays outside
the source repository.

```text
python scripts/build_plugin_marketplace.py build --repository . --revision SOURCE_COMMIT --release-revision c4d9036fdaab378f08fe2db68978126f66ab961e --release-record docs/engineering/release-0-19-0/releases/RLS-SEH-028.md --expected-wheel-sha256 43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8 --wheel "WHEEL" --evaluator-python "CHECKER_PYTHON" --output-directory "NEW_OUTPUT"
```

Run the same command with `check` in place of `build` to independently recheck
the tree against the committed inputs. The command keeps interrupted output and
refuses to replace an existing directory; inspect it and choose a fresh destination.

The composition contains:

```text
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
README.md
LICENSE
PACKAGE-IDENTITY.json
submissions/
packages/codex/verity-plane/
packages/claude/verity-plane/
packages/verity-plane-codex.zip
packages/verity-plane-claude.zip
```

The native builder's inventories and archives remain intact under `packages/`.
Both host packages include LICENSE through the shared committed plan. Catalogs
and instructions come from the same source commit; no output overlay is needed.

## Check and deliver

For a newly planned delivery, use the
[release delivery handoff](release-delivery-completion.md#perform-and-retain-each-handoff).
Evaluator publication leaves plugin assembly, qualification and separately
authorized marketplace publication pending with an owner and next action.
The selected plugin is 0.2.1, while the wheel remains the published 0.19.0
release. Do not use source version 0.20.0 as the evaluator or bundled wheel.
The separately authorized publication on 2026-09-29 advanced the public branch
from `ed68b30c88043773be929540b7b10ae537957c2d` to
`86d75e56e28c0c34819c0079b41dc67075f58490`. All 63 public files match the verified
distribution. Its assembly source remains
`ce6d5fa4080e2ef0904446aa0b066d907532b63c`.
See the [publication receipt](../engineering/plugin-integration/evidence/WO-PLG-028/publication.json)
and [confirmation status](../engineering/plugin-integration/evidence/WO-PLG-028/README.md).
After publication, retain both fresh-install and update observations from the
actual public ref on each claimed host. Reconcile current availability claims
and run the [overall completion check](release-delivery-completion.md#run-the-completion-check).
Local qualification alone does not close that delivery.

1. Run the declared package checks, host validators and local native installation
   acceptance in fresh profiles. Follow VER-PLG-026 and retain actual evidence, including fresh installation,
   update from public 0.1.0 and replacement of local 0.2.0 on both hosts.
   Confirm the loaded package bytes, startup, manual compaction, repository
   switch and missing/mismatched root handling. Do not alter real user profiles.
2. Prepare the commit-bound verification record and obtain its owner decision.
   Resolve the applicable repository integration and external-action checkpoints.
3. Publish the accepted distribution tree at the root of
   `mmzen/se_harness:plugin-marketplace`. Record the expected old public commit before authorization. Add an ordinary
   descendant commit on the existing branch; never force over an unexpected
   revision. Recheck and compare any movement before proceeding. The source implementation
   is reviewed separately from this generated distribution branch.
4. Add the actual public Git marketplace in fresh Codex and Claude profiles,
   install verity-plane, and compare installed contents with the accepted package.
   Also test an existing public installation's update path on both hosts.
   VER-PLG-027 governs these observations. Retain the public commit, active paths,
   installed hashes and native delivery before reporting public installation as checked.
5. Update current availability claims through WO-PLG-028, obtain commit-bound
   verification and separately authorized integration. Read the merged public
   documentation back before declaring overall delivery complete. Preserve the
   assembled source identity and earlier plan versions; bind observations to
   the final delivery plan bytes.

Read the assembled README for user commands. Record current publication status
in the work-order evidence; source preparation alone establishes no public ref.
The normal developer build remains available through
`scripts/build_plugin_archives.py develop` and is labeled development-only.

## Provider submissions

The assembled `submissions/` directory contains the listing draft, logo and
reviewer cases. Publisher identity, support/legal URLs, regions and attestations
remain owner inputs. Prepare the materials independently of those missing fields;
submit only a complete owner-reviewed application through the requested provider
route. Public Git distribution and provider listing are separate observations.
