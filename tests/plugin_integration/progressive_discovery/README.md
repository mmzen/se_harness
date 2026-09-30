# Qualify session activation and instruction delivery

The unit tests assess selection, integrity, atomic replacement and refusal
boundaries. The installed-wheel walkthrough tests the assembled adapter against
two real evaluator packages. Neither establishes native host support.

## Portable package checks

Run from the product checkout with Python 3.11 or later:

```text
python -m unittest tests.plugin_integration.progressive_discovery.test_delivery tests.plugin_integration.progressive_discovery.test_activation tests.plugin_integration.test_simple_plugin tests.plugin_integration.package_assembly.test_package_assembly
python tests/plugin_integration/progressive_discovery/run_resource_acceptance.py --wheel CANDIDATE_WHEEL --expected-identity INDEPENDENT_IDENTITY_JSON --legacy-wheel RELEASED_020_WHEEL --output NEW_TEMPORARY_DIRECTORY
```

The independent identity JSON has an `evaluator` object with version, payload
manifest/digest and archive name/digest. Obtain it from the wheel's reviewed build
evidence. Do not infer expected values from the adapter response.
The walkthrough writes its exact commands, outputs and failures to `report.json`.
Use the same runner on Windows and Linux. Keep failed runs before correcting inputs.

## Native observations required by VER-IAR-021

Use disposable checkouts, fixture remotes and private host profiles. Install the
reviewed development package using each host's supported development route.
Review and trust its hooks through the native host; do not bypass hook trust.
Keep the real user's settings and credentials unchanged. A fresh profile may
need the human to authenticate through the host's normal login flow.

1. Start Codex Windows desktop and Claude Code sessions in a parent directory
   before their fixture checkouts exist. Retain the host version, plugin file
   digests, native startup callback and bootstrap visible to the agent.
2. Ask the agent to clone the prepared local fixture remote and activate that
   destination using setup. Retain the native session identity, plugin-data path,
   helper invocation and immediately returned full entry. There must be no
   repository instruction copy in the successor fixture.
3. Keep the host working directory in the parent. Trigger manual compaction
   through the host UI, then observe a native automatic compaction during normal
   test-session work. Retain both callbacks and the full delivered entry digest.
   A helper invocation with `source=compact` does not satisfy this step.
4. Close and resume the same native session. Confirm it restores its own checkout
   and release. A new session or fork with a different host ID must select its own
   target. Do not infer successful resume from an unchanged working directory.
5. Run two native sessions concurrently from the same parent. Activate separate
   checkouts pinned to 0.20.0 and the candidate. Interleave compaction and confirm
   each selection. Switch one session and clear it; confirm the other is unchanged.
6. In the disposable fixtures, follow the selected procedures for a proposed work
   order and a previously authorized fixture work order. At delivery, identify
   the exact candidate, destination and required push/PR authority without making
   a real external publication. Activation must supply no decision authority.

Record a result per row of VER-IAR-021, including unavailable hosts and unobserved
events. Capture host identity from native events, not transcript inference.
Do not reuse an earlier plugin's native evidence without exact input comparison.
The work order stays in progress while required observations are missing; no
ready verification record or assurance acceptance is implied by these scripts.

Protocol references: [Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Claude hooks](https://code.claude.com/docs/en/hooks), and
[persistent Claude plugin data](https://code.claude.com/docs/en/plugins-reference#environment-variables).
