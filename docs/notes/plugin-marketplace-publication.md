# Prepare and publish the Verity Plane marketplace

## Release status and immutable packages

For evaluator 0.22.1 / plugin 0.2.6, [VREC-SEH-033](../engineering/release-0-22-1/verification-records/VREC-SEH-033.md)
records mmzen's verification of the exact candidate. The [release record](../engineering/release-0-22-1/releases/RLS-SEH-033.md)
records its release decision; the [delivery evidence](../engineering/release-0-22-1/evidence/WO-RLS-042/README.md)
records completed publication and public-route results separately.
[VREC-RLS-004](../engineering/release-0-22-1/verification-records/VREC-RLS-004.md)
records mmzen's verification of those observations. Read those records
and the actual public identity before claiming a current version or complete delivery.
Codex Windows desktop remains unverified under accepted DEC-RLS-009 / RISK-RLS-007.

Staged package READMEs are immutable snapshots of preparation. In 0.2.6 they
include earlier 0.2.5 status and qualification wording. Preserve those bytes
and inventories. Current source guidance and the delivery receipts describe
later verification and publication; do not rewrite a qualified package in place.

## Historical public delivery: 0.22.0 / 0.2.5

[REL-SEH-034](../engineering/release-0-22-0/release/REL-SEH-034.md) records the
evaluator 0.22.0 / plugin 0.2.5 delivery. Human mmzen verified VREC-PLG-032.
WO-RLS-035 published the qualified tree at `7d30907f15bd7e06fb632e1ebf4e88e01b68726c`;
independent public readback matches all 69 files and the exact released wheel.

[WO-RLS-036 observations](../engineering/release-0-22-0/evidence/WO-RLS-036/README.md)
record Codex CLI public fresh installation, update from 0.2.4 and offline setup.
The retained [delivery closeout](../engineering/release-0-22-0/evidence/WO-RLS-036/closeout.md)
confirms guidance integration and release-marker completion.

[Claude follow-up (2026-10-03)](../engineering/release-0-22-0/evidence/WO-RLS-038/README.md): on Windows, Claude Code 2.1.273
passed public fresh installation and update from 0.2.4, plus startup, activation,
resume, manual/automatic compaction and session-isolation checks for plugin 0.2.5
and evaluator 0.22.0. The native test package matches all 29 public package files.
Codex Windows desktop, the full Claude work-order walkthrough and the earlier
long-path case remain unverified. DEC-RLS-007/008 record the bounded follow-up;
the original release omissions and accepted risks under DEC-RLS-005/006 remain
historical records.

This rollout used the existing delivery route under selected evaluator 0.21.0.
The repository now selects 0.22.1 under WO-HUP-030. The separately authorized reviewer-only
provider change for 0.22.1 is recorded in the
[configuration readback](../engineering/release-0-22-1/evidence/WO-RLS-040/provider-configuration-applied.json).
Recheck actual provider controls before each authorized publication.
Earlier release records retain their original results and decisions.

## Assemble committed inputs

For the legacy `build` path, first require the selected RLS to be released and its wheel to be independently
available from the public release. Compare the downloaded wheel SHA-256 with
that record's distribution binding. A local candidate wheel does not satisfy
this prerequisite. Use the checkout's selected released evaluator; resolve its
actual version and absolute path from the selected repository context.
Publication does not change a repository's selection. A successor plugin may
deliver external wheel resources and session activation; publication must
qualify those exact package bytes and must not imply that existing repositories
adopted the new layout.

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

## Stage before release approval

The [0.22.1 / plugin 0.2.6 preparation](../engineering/release-0-22-1/README.md)
uses the complete-release route. Candidate qualification, exact final approval
and public delivery are separate observed stages. Consult its current records
for the observed public state. Repository adoption and the hosted evaluator
pin require their own approved changes.


The [complete-release route](release-delivery-completion.md#one-approval-for-the-complete-release)
uses `stage` and `check-stage` before publication. They take the retained candidate's
schema-2 build manifest, its independently retained digest and the exact wheel.
The builder checks the commit, Git source tree, build recipe and wheel identity.
It writes the same native formats and marketplace layout as the released-input
path. Staging grants no assurance, host-support or publication decision.

```text
python scripts/build_plugin_marketplace.py stage --repository . --revision CANDIDATE_COMMIT --candidate-manifest BUNDLE_JSON --expected-manifest-sha256 MANIFEST_SHA256 --expected-wheel-sha256 WHEEL_SHA256 --wheel CANDIDATE_WHEEL --evaluator-python EVALUATOR_PYTHON --output-directory NEW_OUTPUT
python scripts/build_plugin_marketplace.py check-stage --repository . --revision CANDIDATE_COMMIT --candidate-manifest BUNDLE_JSON --expected-manifest-sha256 MANIFEST_SHA256 --expected-wheel-sha256 WHEEL_SHA256 --wheel CANDIDATE_WHEEL --evaluator-python EVALUATOR_PYTHON --output-directory NEW_OUTPUT
```

Use absolute paths for the manifest, wheel, evaluator Python and fresh output.
The released evaluator runs outside the checkout to compute canonical payload
identity. The candidate wheel is inspected as inert bytes. `--dry-run` is not
an option here; `check-stage` compares the existing output without replacing it.

Complete the required package/host qualification and human verification before
the final complete-release request. Prepare its exact marketplace child commit
and retain it on the authorized staging ref. Candidate provenance stays in the
inventories. The later RLS decision and public receipts reference those identities;
they do not rewrite or requalify the package merely because governance changed.

After evaluator publication, the existing publisher compares the independently
downloaded public wheel, rechecks every staged file and its parent/tree, and
promotes that commit to `plugin-marketplace`. Matching retries make no new commit.
Unexpected branch movement stops promotion. Public fresh/update checks remain
required after promotion and before delivery can be complete.

## Check and deliver

For a legacy delivery, use the
[release delivery handoff](release-delivery-completion.md#perform-and-retain-each-handoff).
Evaluator publication leaves plugin assembly, qualification and separately
authorized marketplace publication pending with an owner and next action.
Historical deliveries retain their own plans and observations. For the selected
complete-release route, execute the frozen plan under its matching human grant;
do not request again authority that the grant already supplies.
Track all five surfaces in the release delivery plan. Local package
qualification does not close delivery or establish the public branch state.

1. Run the declared package checks, host validators and local native installation
   acceptance in fresh profiles. For 0.2.6, follow VER-RLS-037 and VER-IAR-021.
   Public fresh installation and update from 0.2.5 follow under VER-RLS-038.
   Earlier accepted omissions remain limited to their recorded scope.
   Confirm the loaded package bytes, startup, manual compaction and resume. Do not alter real user profiles.
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
   For 0.2.6, VER-RLS-038 governs these observations. Retain the public commit, active paths,
   installed hashes and native delivery before reporting public installation as checked.
5. For 0.2.6, retain public observations through WO-RLS-042. Read the merged
   public documentation back before declaring overall delivery complete.
   The complete-release plan freezes documentation before approval; later
   observations belong in its named receipt files. Preserve the assembled
   source identity and the frozen plan. Any new documentation correction
   needs bounded review before its changed bytes enter a new plan.

Read the assembled README for user commands. Record current publication status
in the work-order evidence; source preparation alone establishes no public ref.
The normal developer build remains available through
`scripts/build_plugin_archives.py develop` and is labeled development-only.

## Previous public delivery

Plugin 0.2.2 with evaluator 0.20.0 was published at
`5662817f42994bd0dc9aabaa56891f9c298ab965`. Its
[public receipt](../engineering/release-0-20-0/evidence/WO-PLG-031/README.md)
is retained unchanged. The 0.2.3 update checks start from that preserved package.


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
