+++
id = "SPEC-HUP-006"
type = "specification"
title = "Standard-root adoption contract for released 0.7.0"
status = "draft"
owners = ["technical-owner", "engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
specifies = ["REQ-HUP-012", "REQ-HUP-013"]
+++

# Specification: Standard-root adoption contract for released 0.7.0

## Scope

One ordinary `harnessctl upgrade` transaction moving this repository's
standard root from exact public 0.6.0 (schema-3 lock
`978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e`) to exact
public 0.7.0, plus the qualification that proves the result. Nothing else.

## Inputs

- Exact public 0.7.0: wheel
  `e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3`,
  installed payload
  `26c11ec5e2363c3c0a9a416e69a3faa8bdf2d7a046710075bdeb661dd1003ee9`,
  installed from the wheel file into a virtual environment outside the
  checkout and proven with `identity --role released-evaluator`.
- `WO-HUP-006` with its `[evaluator_upgrade]` table naming those digests and
  the prior lock.
- The reviewed plan below.

## State model

`0.6.0 root` → (plan reviewed, identity proven) → `apply` → `0.7.0 root
candidate` → (doctor, validate, suites, hosted lanes) → `WO-HUP-006
implemented` → separate VREC, pull request, merge.

## Behavioral rules

1. Execute the evaluator only from the isolated 0.7.0 environment, with
   `-I`, no `PYTHONPATH`, user site disabled.
2. Validate archive and installed-payload identities before the plan and
   again immediately before `--apply`.
3. Review the plan: it must list exactly the paths in *Reviewed managed
   plan* with no `customized` and no `conflict` result. Owner content
   outside the fragment markers of `AGENTS.md`, `CLAUDE.md` and
   `.gitignore`, and the repository-owned `.gitattributes` rules outside the
   managed block, stay as they are.
4. Apply only through
   `harnessctl upgrade . --work-order WO-HUP-006 --evidence-output docs/engineering/repository-harness-upgrade/evidence/WO-HUP-006-evaluator-upgrade.json --apply`.
5. Require an atomic write, a schema-3 lock naming 0.7.0 with the exact
   archive and payload digests, canonical LF evidence, and a no-op replay.
6. Run exact 0.7.0 `doctor`, `validate`, `inspect`, `dashboard` and review
   preflight on the complete checkout, never a predecessor view.
7. Run the repository suites on the default runtime and Python 3.11, the
   repository-required checks, and the diff ledger against the base commit.
8. Adjust owner content only where it must state the new governor truthfully:
   the pinned evaluator instruction in `AGENTS.md`'s owner region and the
   root-evaluator statements in `docs/notes/developing-se-harness.md`.
   Test files may change only to replace a pinned 0.6.0 root assumption with
   the released-root identity, one file at a time and named in the evidence.
9. Move the candidate to the next development version, `0.8.0`, together
   with its migration scenario written by the canonical writer, so that the
   predecessor derivation has a pair to rehearse (`PRE008` otherwise). Do not
   edit any other candidate product or template byte, the published
   version's install example, release records, verification records,
   contracts, tags, publication or Pages workflows, maintenance refs, or
   external policy.
10. Stop before commit, push, pull request, merge, verification, release or
    deployment unless separately authorized.

## Reviewed managed plan

Measured on 2026-08-27 with exact public 0.7.0 over `main` at `7284743`:
**61 files, 18 unchanged, 43 add or update**, no customization.

- add: the five agent skills under `.agents/skills/` (18 files) and their
  four `.claude/skills/` adapters; `docs/engineering/ARTIFACT_AUTHORING.md`,
  `docs/engineering/OPERATING_CARD.md`,
  `docs/engineering/TECHNICAL_COMMUNICATION.md`.
- update: `.engineering-harness.toml`, `.gitattributes`,
  `.github/workflows/engineering-harness.yml`, `AGENTS.md`, `CLAUDE.md`,
  `ENGINEERING_HARNESS.md`, `docs/engineering/DECISION_RIGHTS.md`,
  `QUALITY_GATES.json`, `QUALITY_GATES.md`, `WORKFLOW.json`, `WORKFLOW.md`,
  the templates `README.md`, `RELEASE_CONTRACT`, `REQUIREMENT`,
  `VERIFICATION_RECORD` and `WORK_ORDER`,
  `scripts/select_harness_work_order.py`,
  `scripts/validate_engineering_artifacts.py`.
- installer-owned: `.engineering-harness.lock`.

## Error and recovery behavior

Any rule failure stops before the write, or the installer's transaction
restores the pre-write state. A failed qualification after apply is reported
on `WO-HUP-006` as a stop condition; the branch is abandoned rather than
repaired in place.

## Compatibility and exit

After adoption, `AGENTS.md` names `se-harness==0.7.0` as the evaluator to
install outside the checkout. The 0.6.0 evaluator environment stays available
for reading historical records. The candidate CLI may again lead the released
one from the next work order on.
