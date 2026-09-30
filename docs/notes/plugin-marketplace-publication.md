# Prepare and publish the Verity Plane marketplace

The [0.20.0 release package](../engineering/release-0-20-0/README.md) selects
plugin 0.2.2. WO-PLG-030 covers assembly, qualification and preparation of the
marketplace commit. WO-PLG-031 covers public observations and current claims.
Their verification contracts and the selected external-action procedure govern
delivery. These commands grant no approval. Plugin 0.2.2 with evaluator 0.20.0
is now public at `5662817f42994bd0dc9aabaa56891f9c298ab965`.
The [public readback and installation evidence](../engineering/release-0-20-0/evidence/WO-PLG-031/README.md)
compares all 63 public files with the verified distribution. Current-document
integration and the final closeout receipt remain separate steps.

## Assemble committed inputs

For any new assembly, first require the selected RLS to be released and its wheel to be independently
available from the public release. Compare the downloaded wheel SHA-256 with
that record's distribution binding. A local candidate wheel does not satisfy
this prerequisite. The repository's own governing evaluator stays at its selected
0.20.0 until a separate adoption. A successor plugin may deliver external wheel
resources and session activation; publication must qualify those exact package
bytes and must not imply that existing repositories adopted the new layout.

From the source checkout, replace every uppercase placeholder below. Read
`RELEASE_COMMIT`, `RLS_PATH` and `WHEEL_SHA256` from the actual released record
and its committed governance source. `SOURCE_COMMIT` is the full approved
plugin source commit. `CHECKER_PYTHON` is the absolute external released
evaluator Python path. `PUBLIC_WHEEL` and `NEW_OUTPUT` are absolute paths;
output stays outside the source repository.

```text
python scripts/build_plugin_marketplace.py build --repository . --revision SOURCE_COMMIT --release-revision RELEASE_COMMIT --release-record RLS_PATH --expected-wheel-sha256 WHEEL_SHA256 --wheel "PUBLIC_WHEEL" --evaluator-python "CHECKER_PYTHON" --output-directory "NEW_OUTPUT"
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
For this release the selected inputs are plugin 0.2.2 and public evaluator
0.20.0. Track all five surfaces in the release delivery plan. Local package
qualification does not close delivery or establish the public branch state.

1. Run the declared package checks, host validators and local native installation
   acceptance in fresh profiles. Follow VER-PLG-028 and retain actual evidence for the exact 0.2.2 packages.
   Public fresh installation and update from 0.2.1 follow under VER-PLG-029.
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
   VER-PLG-029 governs these observations. Retain the public commit, active paths,
   installed hashes and native delivery before reporting public installation as checked.
5. Update current availability claims through WO-PLG-031, obtain commit-bound
   verification and separately authorized integration. Read the merged public
   documentation back before declaring overall delivery complete. Preserve the
   assembled source identity and earlier plan versions; bind observations to
   the final delivery plan bytes.

Read the assembled README for user commands. Record current publication status
in the work-order evidence; source preparation alone establishes no public ref.
The normal developer build remains available through
`scripts/build_plugin_archives.py develop` and is labeled development-only.

## Previous public delivery

The separately authorized 2026-09-29 publication advanced plugin-marketplace
from `ed68b30c88043773be929540b7b10ae537957c2d` to
`86d75e56e28c0c34819c0079b41dc67075f58490`. All 63 files matched the verified
0.2.1 distribution assembled from `ce6d5fa4080e2ef0904446aa0b066d907532b63c`.
Its evaluator is 0.19.0, bound by RLS-SEH-028. These identities describe that
delivery only; do not copy them into the new release's expected values.
The [publication receipt](../engineering/plugin-integration/evidence/WO-PLG-028/publication.json)
and [delivery closeout](../engineering/plugin-integration/evidence/WO-PLG-028/delivery-closeout.md)
retain its observations and limits.

## Provider submissions

The assembled `submissions/` directory contains the listing draft, logo and
reviewer cases. Publisher identity, support/legal URLs, regions and attestations
remain owner inputs. Prepare the materials independently of those missing fields;
submit only a complete owner-reviewed application through the requested provider
route. Public Git distribution and provider listing are separate observations.
