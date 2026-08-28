+++
id = "WO-HUP-008"
type = "work_order"
title = "Adopt exact public 0.8.0 as the standard root, the simple way"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity and the test assumptions are trusted engineering state."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".gitattributes", ".github/workflows/engineering-harness.yml", "AGENTS.md", "ENGINEERING_HARNESS.md", "README.md", "docs/engineering/QUALITY_GATES.json", "docs/engineering/QUALITY_GATES.md", "docs/engineering/WORKFLOW.json", "docs/engineering/WORKFLOW.md", "docs/engineering/repository-harness-upgrade/", "docs/notes/developing-se-harness.md", "pyproject.toml", "scripts/validate_engineering_artifacts.py", "se_harness/__init__.py", "tests/"]

[relations]
implements = ["REQ-HUP-016", "REQ-HUP-017"]
specifications = ["SPEC-HUP-008"]
architecture = ["ARCH-HUP-006"]
verification = ["VER-HUP-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T17:04:49Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-28 with the words 'Approve and start', as a decision distinct from the approval of its definitions seconds earlier. Authorizes start preflight and then only the declared simple upgrade from an isolated 0.8.0 wheel-file install outside the checkout, the owner statements, the candidate move to 0.9.0, the identity-aware test changes and the retained evidence, inside the declared execution scope. It authorizes no verification record, no release, no publication, no deletion of the retained stage machine and no change to the guard. Start preflight has not been run."
+++

# Work Order: Adopt exact public 0.8.0 as the standard root, the simple way

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It follows `WO-HUP-007` (0.7.1) and is the
acceptance in the wild that `REL-SEH-019`'s observation window names.

Commit-bound verification is `required`: the root this work order writes is
what every later gate runs under.

## Objective

Use exact public 0.8.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-017` binds, to replace the 0.7.1 standard root with one
evidence-bound 0.8.0 root by the simple upgrade — one command, no packet —
and prove the complete graph and the repository suite under the new root,
without changing product, release, publication, deployment, maintenance or
external state.

## In scope

- Prove the installed 0.8.0 identity (version, payload digest, archive pair
  equal to the published wheel) from the isolated environment;
  `SPEC-HUP-008` rules 1 and 2. Rehearsed on 2026-08-28 on a throwaway
  export of `main` at `2628627`: payload
  `ea75cc53a518cfe0f027336f1a9aabfa301175a00410091f6c2f4b50ccd92eb5`,
  archive `se_harness-0.8.0-py3-none-any.whl`
  `e08aab8a96c156f9e5edf99b9a28aad96c7cffe5b18c262a2598a6b6873fadeb`.
- Review the plan against the installer's managed set: `add` or `update`
  only, no `customized`, no `conflict` (rule 3). Measured: 61 files, 9
  `update`, 52 unchanged.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-008-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5).
- Update owner content only where it must state the new governor: the
  `se-harness==0.7.1` instruction in `AGENTS.md`'s owner region, and the
  root-evaluator statements in `docs/notes/developing-se-harness.md`
  (rule 8).
- Move the candidate to `0.9.0` (`pyproject.toml`, `se_harness/__init__.py`,
  the README install example); no scenario, no legacy-contract entry
  (rule 7).
- Replace pinned root and candidate assumptions in `tests/` with
  identity-aware assertions, each named in the evidence (rule 9). The
  rehearsal's suite on the moved root read 1011 tests, 24 failures and 1
  error in nine modules: `test_ci_pipeline` (legacy table lookup for a root
  that has none), `test_predecessor_bootstrap_retirement` (root copy versus
  candidate copy of the validator, now byte-identical),
  `test_validation_taxonomy` (quality-gates root copy, now byte-identical),
  `test_standard_repository_lifecycle` (managed `.gitattributes` block, now
  the 0.8.0 fragment without the migration rules),
  `test_instruction_architecture` (owner region names the root),
  `test_progressive_documentation` and `test_public_onboarding` (candidate
  version in README and the note); `test_release_build`'s
  `test_declared_mode_set_is_what_a_posix_export_already_carries` fails on
  this workstation before and after the move for file-mode reasons and passes
  hosted, and is not a root assumption.
- Run the complete `VER-HUP-008` qualification and the suite, and retain the
  evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages workflows; the
`release/0.8` line; credentials; the published 0.8.0 itself, which does not
move; the deletion of the retained stage-machine files, their owner-region
`.gitattributes` rules and their test exemptions (issue #210's follow-up,
a separate work order this adoption unblocks); any change to the guard when
it refuses.

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements; which assertion form replaces each pinned test assumption,
provided the released-root identity and the candidate templates are both
still asserted in both root states; the order of readings.

## Constraints

- The applying runtime is exact public 0.8.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal by
  the guard is a stop, not a thing to bypass.
- No `customized` or `conflict` action may be waived; a `null` archive pair
  is a stop.
- The complete graph must pass exact 0.8.0 directly after apply.
- Candidate template bytes must remain unchanged; the repository-owned
  `.gitattributes` rules outside the managed block stay effective.

## Expected change surface

The 9 reviewed `update` paths, the installer-owned lock and
`.engineering-harness.toml`; `AGENTS.md`'s owner region and
`docs/notes/developing-se-harness.md`; `pyproject.toml`,
`se_harness/__init__.py`, `README.md`; the test files named in the evidence;
this packet, the domain index, the transaction JSON and the evidence.

## Required verification

Execute `VER-HUP-008` in full; repository-required checks; the pull
request's lanes green; the handoff check over the complete changed-path set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-008-verification.md`
and `WO-HUP-008-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the managed set, customization,
conflict, a `null` archive pair, a partial transaction, a failed replay, a
failed graph or suite, an unexplained warning, a product or release byte
moved beyond the version identity, a test that cannot assert the released
root without weakening the candidate-template assertion, or a need for
authority beyond the approved stage.

## Completion report format

The evidence file, the changed-path ledger, the handoff `check` restitution;
the completion decision is the engineering owner's.
