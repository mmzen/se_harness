# Upgrade the harness

## Read this when

An exact harness upgrade is requested and authorized.

## Before this action

Read [SETUP.md#prepare-or-repair-the-released-evaluator](SETUP.md#prepare-or-repair-the-released-evaluator) for the selected target evaluator. Read [migration/IMPLEMENTATION_PLAN.md#installation-and-adoption](migration/IMPLEMENTATION_PLAN.md#installation-and-adoption) for the instruction-ownership migration.

## Procedure

### Upgrade the installed harness

**Inputs:** An explicitly selected target release, its released wheel, the
repository's upgrade authority and scope, and any specifically authorized
editable-file replacements.

**Output:**

- **Repository files:** Only changes accepted by the reviewed installer plan,
  including the selected configuration and lock identity when the upgrade succeeds.
- **Retained evidence:** Upgrade transaction evidence when required, at the
  selected authorized path.
- **Formal artifacts:** No approval, verification, release, or product
  lifecycle transition is inferred from the upgrade.
- **Transient working material:** The preview and actual post-upgrade checks.

**Actions:**

1. Prepare the private environment with the explicitly selected target release.
   During this upgrade, the target evaluator may differ from the repository's
   old lock. Do not edit that lock manually to erase the difference.
2. Read the target evaluator's `upgrade --help` and run its doctor against the
   repository. Separate expected old-version/template differences from unrelated
   integrity failures.
3. Preview the upgrade. Inspect every changed path and the target identity.
   If the plan retires an AGENTS.md or CLAUDE.md harness block, follow
   [Legacy entry delivery evidence](#legacy-entry-delivery-evidence) before apply.
4. Leave editable seed files unchanged unless their replacement was explicitly
   selected. Repeat `--replace-file PATH` for each selected editable file in both
   preview and apply. Preserve unrelated owner files and formal records.
5. If transaction evidence is required, choose its authorized repository path
   below `docs/engineering/DOMAIN/evidence/` and pass `--evidence-output PATH`.
6. Apply the same selected plan only when its changes match the existing upgrade
   authority. Customized managed content or an unsafe destination must be resolved
   before apply; neither a version mismatch nor a failed check grants overwrite
   authority.
7. Run doctor and the repository's required post-upgrade checks with the resulting
   selected evaluator. Report actual failures and effects.
8. After interruption, inspect the configuration, lock, and files. Reuse the same
   selected wheel and installer operation. Do not introduce a second environment
   or a fabricated recovery receipt.

**Harness commands:**

For this procedure only, `harnessctl` invokes the explicitly selected target
release, not whichever executable happens to be on `PATH`:

```text
harnessctl upgrade --help
harnessctl doctor REPO --json
harnessctl upgrade REPO --json
harnessctl upgrade REPO --apply --json
harnessctl doctor REPO --json
```

Include the same selected `--replace-file` and `--evidence-output` arguments
in the applicable preview/apply commands. An initialized repository uses
`upgrade`; do not reinitialize it to replace its settings. A plugin update
changes the plugin, not the repository's selected evaluator release.

**Completion:** The configuration, lock, installed managed content, and released
evaluator agree, and the required checks pass, or the remaining failures and
actual writes are explicit.

**Later use:** Resume only the work allowed by the resulting evaluator and
existing authority. An upgrade performs no merge, tag, publication, deployment,
or product release.

## Legacy entry delivery evidence

Before approving removal of an old harness block, review native startup and
post-compaction traces from the configured replacement host. A direct call to
the hook script is not a native trace. Confirm the host is installed, enabled
and trusted for this repository. Rehearse the exact planned root in an isolated
copy before changing the real installation.

Retain a JSON evidence file and its trace files in the authorized evidence
location. Its schema is `se-harness-native-instruction-delivery-v1`:

| Field | Value to retain |
| --- | --- |
| `repository` | Absolute path of the repository being upgraded. |
| `target_version` | Selected target evaluator version. |
| `prior_lock_sha256` | SHA-256 of the original lock using `utf8-text-lf-v1`. |
| `entry_sha256` | SHA-256 of the complete planned root using `utf8-text-lf-v1`. |
| `host`, `host_version` | Observed `codex` or `claude` and its exact version. |
| `events.startup`, `events.compact` | One object for each native event. |

Each event object records `origin: "native-host"`, the observed
`delivered_root_sha256`, a `trace` path relative to the JSON evidence file, and
the trace's exact-byte `trace_sha256`. Keep both complete traces. Do not copy a
startup result into the compaction entry or label a simulated event as native.

Pass `--instruction-delivery-evidence PATH` on the target evaluator's upgrade
apply command. The installer checks the repository, prior lock, planned entry,
event pair and retained trace digests. This checks evidence consistency; it
does not independently prove how the host produced a trace. The accountable
upgrade reviewer assesses that evidence. Missing or stale evidence leaves the
old entry unchanged. An already migrated installation needs no new retirement
receipt. A fresh installation still needs host setup before automatic delivery
can be claimed.

## Read next when

After the resulting identity and checks pass → [CONTINUE.md#procedure](CONTINUE.md#procedure). A conflict remains → [RESULTS.md#if-a-procedure-is-blocked](RESULTS.md#if-a-procedure-is-blocked).

## Retired guide files

New installations omit OPERATING_CARD.md, DECISION_RIGHTS.md, QUALITY_GATES.md,
WORKFLOW.md, TRACEABILITY.md and TECHNICAL_COMMUNICATION.md under
docs/engineering/. The current instructions are under docs/engineering/harness/.
ARTIFACT_AUTHORING.md, WORKFLOW.json and QUALITY_GATES.json remain in place.

An upgrade from 0.19.0 preserves each existing pointer or customized owner file
byte-for-byte. An absent file stays absent. The preview lists previously tracked
guides as unchanged; successful apply removes their seed entries from the lock.
The files are then ordinary owner files. Do not use --replace-file for these
retired 0.19.0 seeds, and do not edit the lock by hand.

The supported 0.18.0 migration is different: recognized old full guides convert
to compatibility pointers. Inspect each proposed update in the preview. A
customized old guide blocks apply. Review an owner migration plan first; only
when exact replacement is authorized, pass its --replace-file path in both
preview and apply. Missing old guides remain absent. The resulting pointers
remain owner files and are not tracked by the new lock. The legacy entry
delivery-evidence requirement above still applies.

### Separately authorized pointer cleanup

**Inputs:** An adopted release that omits these seeds, an exact cleanup decision,
the reviewed file paths and byte hashes, and a current consumer inventory.

**Output:** Only the reviewed stock pointers are removed. Owner customizations,
required instructions and historical records remain intact.

**Actions:**

1. Confirm the actual selected host and plugin versions. Review their native
   startup and compaction qualification for the adopted instruction collection.
2. Inspect active instructions, scripts and tools for dependencies on each
   selected pointer. Confirm that their replacement file and heading exist.
   Keep any pointer still required by an active consumer.
3. Compare each selected file with its reviewed stock bytes and exact hash.
   A changed, customized or ambiguous file needs a separate owner decision.
   Check every selected file before deleting any of them.
4. Remove only the unchanged stock pointers covered by that cleanup decision.
5. Run the selected released evaluator's upgrade preview. Apply only the
   authorized reconciliation, then run doctor and the applicable repository
   checks. Use the commands under Upgrade the installed harness.
6. After interruption, inspect the actual files and lock before continuing.
   Retry only effects known not to have occurred. Do not recreate an old pointer
   or repeat a deletion merely because an acknowledgement was lost.

There is no harness deletion command or cleanup flag. Ordinary file removal
requires the reviewed owner authority above; an upgrade alone never supplies it.
