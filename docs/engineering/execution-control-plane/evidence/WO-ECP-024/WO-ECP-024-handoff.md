```toml
artifact = "WO-ECP-024"
checkpoint = "handoff"
formal_snapshot_sha256 = "9d77f46747b95176407a95b317238f9a506089c1f022dc002fdab9d7f9d50978"
rebound_at = "2026-08-31T14:34:32Z"
```

# WO-ECP-024 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The dead tail is gone: the six-line `WO-ECP-010` retention comment with
its trailing blank line, and the `se_harness/agent_contract.json` rule
(eight lines total). The managed block between the `se-harness` markers is
byte-unchanged (`doctor` 0 FAIL), and every remaining rule matches tracked
content, measured with `git ls-files`: `docs/engineering/**/evidence/*.json`
149, `se_harness/hash_bound_classes.json` 1, `release/build-recipe.json` 1,
`release/build-toolchain.lock` 1,
`templates/repository/standard/.agents/skills/**` 6.

## The delegated route (ECP-GAT-004)

This work order is the first production use of the delegation class
(`WO-ECP-018`), the hosted demonstration issue #284 names. The gate is
`.engineering-harness.delegation.toml`: `github-checks`,
`check_name = "validate"` — the check the default branch's ruleset
requires since 2026-08-31. Each mechanical decision was taken on the
evaluator's own restitution naming `delegated-executor` with a bound
command, and each lifecycle event records the class, the check-run id and
the exact head:

- `DR-WO-START`: taken at head `3ce2302`, check-run `99523603905`,
  conclusion success.
- `DR-WO-COMPLETE` and `DR-VREC-PREPARE`: recorded below as they are
  taken, each on a fresh green reading of its own head.

The approval that granted the class, the verification of the prepared
record, and both merges are human decisions.

## Readings

- Suites reading `.gitattributes` (`test_hash_bound_integrity`,
  `test_upgrade_rehearsal`, `test_instruction_architecture`): 146 tests OK.
- `doctor` (exact 0.12.0 root): 0 FAIL. `validate`: recorded at the handoff
  check below.
