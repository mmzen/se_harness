# Native delivery qualification and adoption handoff

WO-IAR-020 remains **in progress**. This is an intermediate handoff, not completed
qualification. VER-IAR-016 requires both hosts and post-adoption native evidence.

## Observed state

Read-only native plugin listings identify enabled Verity Plane **0.1.0** in the
real Codex and Claude profiles. Their inspected caches have no startup hook or
instruction-delivery helper. Codex CLI is 0.158.0-alpha.2.1; Claude Code is 2.1.273.
The repository remains on the selected released evaluator **0.19.0**.

The separately verified **0.2.0** packages contain the public 0.19.0 wheel, whose
SHA-256 is `43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8`.
Every package file was checked against its retained assembly inventory.
[replacement.json](replacement.json) gives the exact archive, assembly, hook,
skill and marketplace hashes and target paths.

## Fresh native observations

- Codex: full root delivered at startup and manual compaction in the isolated
  demo profile. Exact path, release, root hash and final heading match.
- Codex: repository switch, missing root and release mismatch produce the
  expected current context or explicit refusal. A hypothetical interrupted-write
  prompt requires inspection before retry; no write or tool execution occurred.
  This last probe is not proof of transaction recovery after a real partial write.
- Claude: the native startup hook delivered the full current root. The model
  call then failed because the isolated OAuth session expired and could not be
  refreshed. Model interpretation, manual compaction and authenticated recovery
  remain unverified. No synthetic event is counted as native compaction.

The [evidence inventory](../../evidence/WO-IAR-020/inventory-of-evidence.json)
lists retained native events and their digests. It excludes credentials and raw
host debug logs. Real profile and marketplace settings remain unchanged.

## Exact next adoption proposal

Review the package and target manifest above, then authorize only replacing the
real profiles' `se-harness` marketplace source with the prepared local marketplace
and installing/updating `verity-plane@se-harness` to 0.2.0. Review and trust the
exact read-only SessionStart hook through the host's supported trust UI where
required. Restart the affected sessions, inspect actual selected package paths
and hashes, then repeat native startup and compaction on the intended repository.

The existing marketplace source is `https://github.com/mmzen/se_harness.git`;
retain that selection for recovery. Keep unrelated plugins and configuration.
This proposal changes neither the selected evaluator nor repository instructions.
No marketplace publication, cache editing, hook weakening or legacy-file deletion
is authorized by this handoff. Separately renew the isolated Claude login through
its normal login flow before continuing the incomplete compaction demonstration.

Installing a Codex plugin does not itself trust its hooks; the applicable current
host behavior is documented in [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).
Observed native event payloads, rather than package presence alone, establish
successful delivery for the tested configuration.
