# Published marketplace and public installation evidence

## Published identity and authority

On 2026-09-15, the owner verified VREC-PLG-020 for candidate
`7f32dcbd18b50254a0d4e43e2dfdd9789dc9b78e`. The released evaluator applied that
decision to VREC-PLG-020 only. WO-PLG-023 remains implemented.

The owner then selected **"Authorize this one publication with existing Git
permissions"** in response to the question naming distribution commit
`ed68b30c88043773be929540b7b10ae537957c2d` and
`mmzen/se_harness:plugin-marketplace`. The question explicitly requested a
one-time exception to the Evidence skill's separate-enforcement prerequisite:
GitHub had no publication rules covering that ref. This exception applies to
that publication only; no GitHub policy was changed.

The exact commit was published at 2026-09-15T16:06:21Z. A create-only Git lease
required the destination ref to be absent. Remote inspection confirmed the
result, and inspection after native acceptance confirmed it remained unchanged.
All 59 committed distribution blobs matched the verified package before push.
The source PR's required validation and complete CI suite passed at source head
`c44a290d0a29747d7caa4116c726eefbea78df81` before publication.

- [Public marketplace](https://github.com/mmzen/se_harness/tree/plugin-marketplace)
- [Immutable distribution](https://github.com/mmzen/se_harness/tree/ed68b30c88043773be929540b7b10ae537957c2d)
- Git tree: `614447e9b97b12318ccb6b415178538db60379f2`
- Package input source: `e813e0c78341dd108013a0e59d3cbcbce275cae5`
- Package identity SHA-256:
  `fc9d0c585b104e6ef2ba4598e38ffeade0191e3aeae1658f9df4830244b37e58`

See [actual action and authorization inputs](public-020-action-inputs.json),
[push and readback result](public-020-action-result.json), and
[released evaluator pre-action result](public-020-pre-action.json).
This record adds the post-publication observation required by VER-PLG-023 M05;
it changes no earlier VREC or RLS facts and does not claim a new assurance decision.

## VER-PLG-023 M05: public native installation passed

Ten actual native commands passed against `mmzen/se_harness` with ref
`plugin-marketplace` in fresh Windows profiles. Codex CLI 0.154.0-alpha.6.2 and
Claude Code 2.1.269 each installed all 24 native files byte for byte. The five
intended skills were present; Codex preserved explicit-only operator briefing.
The bundled released SE Harness 0.18.0 wheel's SHA-256 remained
`a683dbdf485d42aa20ea8502122c171a4c61c7d60f85db5b5f264bd336371c54`.

```text
codex plugin marketplace add mmzen/se_harness --ref plugin-marketplace
codex plugin add verity-plane@se-harness

claude plugin marketplace add mmzen/se_harness@plugin-marketplace
claude plugin install verity-plane@se-harness
```

See [native results](native-summary.json), [actual commands](native-commands.json),
and [all 48 installed file comparisons](installed-files.json). Setup was not
rerun for M05: its unchanged wheel, scripts and skills retain the earlier
walkthrough evidence selected by VREC-PLG-020. Plugin installation alone does
not install the checker from PyPI. Invoked setup installs the bundled wheel
offline. No model calls, provider scanner, portal submission or additional
platform support is claimed.

## Windows path-length finding and fixture correction

Codex's observed Git route clones and checks out the repository's default branch
before selecting `plugin-marketplace`. The first disposable profile was deeply
nested under the workspace, so historical source evidence paths exceeded
Windows Git's path-length limit before marketplace installation. A drive alias
did not help because Codex resolved it to its physical path. Moving the nested
fixture to `C:/seh020` still left two historical paths over the limit.

The passing fixture used `C:/p020` and removed the redundant `profile` directory
level. Its Codex home `C:/p020/codex/codex` has the same path length as the
operator's normal `C:/Users/hok/.codex`. The only fixture source change is retained
with both source digests in [the invocation record](public-020-home-depth.json).
Native commands, checks and expected results were unchanged. No Git setting,
user profile or published package was modified to make this test pass.

The [three failed trials](failed-profile-trials.json) remain evidence. Users with
deep custom Codex home paths can encounter this Windows Git limitation; this
run establishes acceptance at the recorded normal home-path depth. Raw native
logs were copied into `work/public-020-retained-raw/` before temporary profile
cleanup. [Retention paths](retention.json) identify those local copies; no remote
raw-log archival or retention period is asserted.

## Source integration and provider submissions

[Source PR #482](https://github.com/mmzen/se_harness/pull/482) contains the
implementation, assurance decisions and this later publication evidence.
Source merge is separate from the completed distribution-branch publication.
The public branch must remain a standalone distribution root.

The immutable [submission materials](https://github.com/mmzen/se_harness/tree/ed68b30c88043773be929540b7b10ae537957c2d/submissions)
include listing text, reviewer scenarios and the logo. The complete native
archives are [Codex](https://github.com/mmzen/se_harness/blob/ed68b30c88043773be929540b7b10ae537957c2d/packages/verity-plane-codex.zip)
and [Claude](https://github.com/mmzen/se_harness/blob/ed68b30c88043773be929540b7b10ae537957c2d/packages/verity-plane-claude.zip).
Official provider applications remain unsubmitted: confirmed publisher identity,
contact, public privacy/terms URLs, regions and owner attestations remain required
inputs. Public Git installation is established; provider directory approval is
not claimed.
