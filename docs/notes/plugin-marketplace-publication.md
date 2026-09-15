# Prepare and publish the Verity Plane marketplace

WO-PLG-023 governs this implementation. Its verification and the selected
external-action procedure govern delivery. These commands grant no approval.

## Assemble committed inputs

Use the existing released SE Harness 0.18.0 wheel, independently obtained from
the published release. Its SHA-256 is
`a683dbdf485d42aa20ea8502122c171a4c61c7d60f85db5b5f264bd336371c54`.
RLS-SEH-027 is retained at governance commit
`e9db30d930e704ec3e40f3f0bf5e7d18799c0d4d`.

From the source checkout, replace `SOURCE_COMMIT`, `WHEEL`, `CHECKER_PYTHON` and
`NEW_OUTPUT` below. The source commit must contain the approved marketplace
implementation. Use full commit IDs and absolute, quoted filesystem paths.
`CHECKER_PYTHON` is the external released evaluator's Python; output stays outside
the source repository.

```text
python scripts/build_plugin_marketplace.py build --repository . --revision SOURCE_COMMIT --release-revision e9db30d930e704ec3e40f3f0bf5e7d18799c0d4d --release-record docs/engineering/release-0-18-0/releases/RLS-SEH-027.md --expected-wheel-sha256 a683dbdf485d42aa20ea8502122c171a4c61c7d60f85db5b5f264bd336371c54 --wheel "WHEEL" --evaluator-python "CHECKER_PYTHON" --output-directory "NEW_OUTPUT"
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

1. Run the declared package checks, host validators and local native installation
   acceptance in fresh profiles. Follow VER-PLG-023 and retain actual evidence.
2. Prepare the commit-bound verification record and obtain its owner decision.
   Resolve the applicable repository integration and external-action checkpoints.
3. Publish the accepted distribution tree at the root of
   `mmzen/se_harness:plugin-marketplace`. Check whether the ref already exists;
   preserve a conflicting ref and report the conflict. The source implementation
   is reviewed separately from this generated distribution branch.
4. Add the actual public Git marketplace in fresh Codex and Claude profiles,
   install verity-plane, and compare installed contents with the accepted package.
   Retain the public commit and outcomes before reporting Git installation as checked.

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
