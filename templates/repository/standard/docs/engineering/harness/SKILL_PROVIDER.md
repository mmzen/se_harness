# Select or restore the skill provider

## Read this when

Provider selection or discovery repair is requested.

## Before this action

Read the actual ownership/provider selection and available host capabilities. If the evaluator is unavailable, use [SETUP.md#procedure](SETUP.md#procedure) first.

## Procedure

### Select or restore the skill provider

**Inputs:** The requested provider (`plugin` or `repository`), absolute
repository path, selected evaluator, and the installed plugin path when using
plugin ownership.

**Output:**

- **Repository files:** The provider record and exact generated skill paths
  changed by the reviewed installer operation.
- **Formal artifacts:** No lifecycle decision.
- **Transient working material:** The path review and actual apply/doctor results.

**Actions:**

1. Inspect `skill-ownership --help` in the selected release. If unavailable,
   report the required compatible release; do not substitute candidate source.
2. Preview the requested provider selection.
3. Inspect the named paths. A plugin switch replaces the generated
   `harness-orient` and `harness-operator-brief` directories under
   `.agents/skills/` and `.claude/skills/`, including edits inside them.
4. Confirm that the required plugin skills exist and the destinations are safe.
   Preserve unrelated files. Apply only the already authorized provider change.
5. Run doctor. After interruption, inspect and rerun the same operation.
6. If the task requires native plugin discovery, verify it in the host separately.
   Do not infer it from the repository check.

**Harness commands:**

```text
harnessctl skill-ownership --help
harnessctl skill-ownership REPO --provider plugin --plugin-root ABSOLUTE-PLUGIN --json
harnessctl skill-ownership REPO --provider plugin --plugin-root ABSOLUTE-PLUGIN --apply --json
harnessctl doctor REPO --json
```

For a requested return to repository ownership, use `--provider repository`
and omit `--plugin-root` in both preview and apply. The provider record stores
the portable choice, not the host's absolute plugin path.

**Completion:** The requested provider is recorded and its repository checks
pass, or the specific refusal is reported. Host discovery remains a separate
observed result.

**Later use:** Use the selected provider's skills for future tasks. They invoke
or render evaluator results and grant no additional lifecycle authority.

## Read next when

Discovery works with the selected repository → [CONTINUE.md#procedure](CONTINUE.md#procedure). Unsupported host delivery → [RESULTS.md#if-a-procedure-is-blocked](RESULTS.md#if-a-procedure-is-blocked).
