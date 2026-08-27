+++
id = "WO-HUP-007"
type = "work_order"
title = "Adopt exact public 0.7.1 as the standard root, the simple way"
status = "in_progress"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity and the test assumptions are trusted engineering state."
decided_by = "repository-owner"

[execution_scope]
paths = [".agents/skills/", ".claude/skills/", ".engineering-harness.lock", ".engineering-harness.toml", ".gitattributes", ".github/workflows/engineering-harness.yml", "AGENTS.md", "CLAUDE.md", "ENGINEERING_HARNESS.md", "README.md", "docs/engineering/ARTIFACT_AUTHORING.md", "docs/engineering/DECISION_RIGHTS.md", "docs/engineering/OPERATING_CARD.md", "docs/engineering/QUALITY_GATES.json", "docs/engineering/QUALITY_GATES.md", "docs/engineering/TECHNICAL_COMMUNICATION.md", "docs/engineering/WORKFLOW.json", "docs/engineering/WORKFLOW.md", "docs/engineering/templates/", "docs/engineering/repository-harness-upgrade/", "docs/notes/developing-se-harness.md", "pyproject.toml", "repository_tools/predecessor_facts.py", "scripts/select_harness_work_order.py", "scripts/validate_engineering_artifacts.py", "se_harness/__init__.py", "tests/"]

[relations]
implements = ["REQ-HUP-014", "REQ-HUP-015"]
specifications = ["SPEC-HUP-007"]
architecture = ["ARCH-HUP-005"]
verification = ["VER-HUP-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T17:43:27Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-27 with the words 'Approve and start', as a decision distinct from the approval of its definitions seconds earlier. Authorizes start preflight and then only the declared simple upgrade from an isolated 0.7.1 index install outside the checkout, the owner statements, the candidate move to 0.8.0 with its scenario and legacy-contract entry, the root-assumption test changes and the retained evidence, inside the declared execution scope. It authorizes no verification record, no release, no publication and no change to the guard. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-27T17:43:33Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-27, 'Approve and start'. Start preflight PASS at phase start over the approval commit carrying unmoved main 23d5781, run with the governing exact public 0.6.0 evaluator outside the checkout. Bounded to the declared execution scope; the applying runtime is exact public 0.7.1 in C:\\Users\\mathi\\se-harness-eval-071, installed from the index. This start authorizes no verification record, no release and no publication."
+++

# Work Order: Adopt exact public 0.7.1 as the standard root, the simple way

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It succeeds the rejected `WO-HUP-006`, whose
packet-bound transaction could not be completed from an index install; that
rejection and `REL-SEH-018` are why it exists.

Commit-bound verification is `required`: the root this work order writes is
what every later gate runs under.

## Objective

Use exact public 0.7.1, installed outside the checkout from the index, to
replace the 0.6.0 standard root with one evidence-bound 0.7.1 root by the
simple upgrade — one command, no packet — and prove the complete graph and
the repository suites under the new root, without changing product,
release, publication, deployment, maintenance or external state.

## In scope

- Prove the installed 0.7.1 identity (version, payload digest, `null`
  archive pair) from the isolated environment; `SPEC-HUP-007` rules 1 and 2.
- Review the plan against the installer's managed set: `add` or `update`
  only, no `customized`, no `conflict` (rule 3). Measured on 2026-08-27
  against `main` at `23d5781`: 61 files, 43 add or update, 18 unchanged.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-007-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5).
- Update owner content only where it must state the new governor: the
  `se-harness==0.6.0` instruction and the managed-path list in `AGENTS.md`'s
  owner region, and the root-evaluator statements in
  `docs/notes/developing-se-harness.md` (rule 8).
- Move the candidate to `0.8.0` with its scenario written by the canonical
  writer from the 0.7.1 pair, keep the 0.7.1 pair as the previous candidate,
  add the `0.7.1` legacy acceptance-contract entry measured from the
  installed evaluator, and move the README install example (rule 7).
- Replace pinned 0.6.0 root assumptions in `tests/` with released-root
  identity-aware assertions, each named in the evidence (rule 9); the seven
  modules `WO-HUP-006` measured are the expected set.
- Run the complete `VER-HUP-007` qualification, both suites, and retain the
  evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages workflows; the
`release/0.7` line; credentials; the RC-070 and RC-071 issues; the published
0.7.1 itself, which does not move; any change to the guard when it refuses.

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements; which assertion form replaces each pinned test assumption,
provided the released-root identity and the candidate templates are both
still asserted; the order of readings.

## Constraints

- The applying runtime is exact public 0.7.1 outside the checkout, in
  isolated mode; a refusal by the guard is a stop, not a thing to bypass.
- No `customized` or `conflict` action may be waived.
- The complete graph must pass exact 0.7.1 directly after apply.
- Candidate template bytes must remain unchanged; the repository-owned
  `.gitattributes` rules outside the managed block stay effective.
- The candidate version and the scenario move in one change.

## Expected change surface

The 43 reviewed add or update paths and the installer-owned lock;
`AGENTS.md`'s owner region and `docs/notes/developing-se-harness.md`;
`pyproject.toml`, `se_harness/__init__.py`, `README.md`, the new scenario
and the writer's legacy map; the test files named in the evidence; this
packet, the domain index, the transaction JSON and the evidence.

## Required verification

Execute `VER-HUP-007` in full; repository-required checks; the pull
request's lanes green; the handoff check over the complete changed-path set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-007-verification.md`
and `WO-HUP-007-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the managed set, customization,
conflict, a partial transaction, a failed replay, a failed graph or suite, an
unexplained warning, a product or release byte moved beyond the version
identity, a test that cannot assert the released root without weakening the
candidate-template assertion, or a need for authority beyond the approved
stage.

## Completion report format

The evidence file, the changed-path ledger, the handoff `check` restitution;
the completion decision is the engineering owner's.
