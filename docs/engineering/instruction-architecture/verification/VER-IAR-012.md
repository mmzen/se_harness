+++
id = "VER-IAR-012"
type = "verification"
title = "Owner instruction region evidence contract"
status = "approved"
owners = ["quality-owner", "repository-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
verifies = ["REQ-IAR-020"]
+++

# Verification Contract: Owner instruction region evidence contract

## Independence

Verification reads `AGENTS.md` and `.engineering-harness.lock` as data and derives every expected value from the lock rather than from a literal copied out of the implementation. The managed-path expectation is computed by filtering lock entries on `mode == "managed"`, so a future lock change makes the test fail rather than silently pass. The digest expectation is computed with `se_harness.integrity.canonical_sha256` over `se_harness.installer.tracked_content`, the same functions the evaluator uses, so the test cannot pass by reimplementing the rule more loosely.

Content-presence checks assert on stable identifiers — path strings, the `Harness-Work-Order` field name, `RID018`, the unittest invocation — not on prose, so wording remains free per the specification's unspecified decisions.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-IAR-020 rule 1 | Automated test | Recompute the fragment digest from `AGENTS.md` | Equals `files["AGENTS.md"].sha256` in `.engineering-harness.lock` |
| REQ-IAR-020 rule 2 | Automated test | `installer._extract_block` over `AGENTS.md` | Returns a block; raises no `HarnessError` |
| REQ-IAR-020 rules 3-4 | Automated test | Owner region substring assertions | Contains `docs/engineering/REPOSITORY_CONTEXT.md` and the unittest discover command |
| REQ-IAR-020 rule 3 negative | Automated test | Owner region negative assertions | Does not describe any pointed-to file as preflight-required, harness-seeded, or harness-required; the pointer is stated by content only, so it stays true across `REQ-DST-065` |
| REQ-IAR-020 rule 5 | Automated test + review | Owner region negative assertions | Does not contain the withdrawn product-invariant restatements; contains the domain-index pointer |
| REQ-IAR-020 rule 6 | Automated test | Lock-derived managed set vs owner region | Every `mode == "managed"` path is represented; `.engineering-harness.lock` is named |
| REQ-IAR-020 rule 7 | Automated test | Lock-derived owner-editable set under `scripts/` | Each of the five is named as owner-editable; no blanket `scripts/` claim |
| REQ-IAR-020 rule 8 | Automated test | Owner region substring assertion | Names `templates/repository/standard/scripts/` and the lag rule |
| REQ-IAR-020 rules 9-10 | Automated test | Owner region substring assertions | Contains `Harness-Work-Order` and `RID018` |
| REQ-IAR-020 rule 11 | Automated test | Owner region substring assertions | Retains the four agent-facing constraints |
| REQ-IAR-020 rule 12 | Automated test | Owner region byte length | Under 6,000 bytes |
| REQ-IAR-020 rule 13 | Manual assessment | Accountable review of the region | No approval, product intent, or precedence claim over `docs/engineering/` |
| REQ-IAR-020 boundary | Automated test | Mutated managed block fixture | Digest differs from the lock value; the mutation is detected |
| REQ-IAR-020 scope | Automated test | Diff surface of the candidate | Only `AGENTS.md`, this domain's artifacts, evidence, and the domain README changed |

## Acceptance scenarios

An instruction-architecture acceptance scenario shall record that an agent loading only the always-available surface can name the test command and correctly choose the candidate-source copy of a managed script.

## Property and invariant tests

- **Lock agreement.** For every lock entry with `mode == "managed"`, the owner region represents that path, individually or through an unambiguous directory form such as `docs/engineering/templates/*`. No path with a mode other than `managed` is described as managed.
- **Idempotent integrity.** Running the revision twice produces identical bytes, and the fragment digest is unchanged in both runs.
- **Packaged fragment untouched.** `templates/repository/standard/AGENTS.md.fragment` and `templates/repository/standard/CLAUDE.md.fragment` are byte-identical to their pre-change state.

## Static and architecture checks

- `python scripts/validate_engineering_artifacts.py --root .` reports zero errors.
- `python -m unittest discover -s tests -p "test_*.py"` shows no new failure relative to the recorded baseline. The known `RID018` failure caused by a machine-wide editable `se-harness` is an environment condition and shall be recorded as such rather than treated as a regression; a clean environment without an installed `se-harness` shows it passing.
- The existing `tests/test_instruction_architecture.py::test_instruction_route_and_ownership_modes_are_explicit` continues to pass, confirming the managed fragment still names `ENGINEERING_HARNESS.md`, still omits `REPOSITORY_CONTEXT.md`, and that ownership modes are unchanged.

## Security and privacy checks

Confirm the untrusted-input instruction is retained and that no credential, token, path outside the repository, or environment value is introduced into the instruction surface.

## Performance and resilience checks

Not applicable beyond the rule 12 size bound. The change adds no runtime behavior.

## Manual assessments

The assurance owner assesses that the region adds constraints without waiving formal artifact authority, approved work-order scope, required evidence, or accountable verification and release decisions, and that the withdrawn product-invariant bullets are genuinely owned by governed requirements rather than silently dropped.

The technical owner assesses whether reusing `INT-IAR-001` and `CAP-IAR-001` correctly covers a repository-local instruction obligation. A negative assessment invalidates the packet's upstream trace and requires a distinct intent and capability before approval.

## Evidence retention

Retain evidence keyed to `WO-IAR-012` at `docs/engineering/instruction-architecture/evidence/WO-IAR-012-verification.md`, recording the computed and expected fragment digests, the lock-derived managed and owner-editable path sets, the test and validator output, the diff surface, and the environment condition affecting the `RID018` case.

## Residual uncertainty

Automated checks confirm that required facts are present and that the lock agrees with them. They cannot confirm that an agent reads the region, that the prose is unambiguous to a reader, or that the resulting instruction surface actually shortens the path to a correct first action. Those remain matters of accountable judgement. The region is also not integrity-tracked, so nothing prevents future drift from `.engineering-harness.lock`; the rule 6 and rule 7 tests are the only standing detector, and they run only when the suite runs.
