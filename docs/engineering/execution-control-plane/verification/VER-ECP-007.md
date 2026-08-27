+++
id = "VER-ECP-007"
type = "verification"
title = "Independent evidence for the consumer product boundary"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
verifies = ["REQ-ECP-012", "REQ-ECP-013", "REQ-ECP-014"]
+++

# Verification Contract: Independent evidence for the consumer product boundary

## Independence

Expected behaviour derives from `REQ-ECP-012`, `REQ-ECP-013`, `REQ-ECP-014`,
and the `ECP-PRD-` and `ECP-SKL-` rules of `SPEC-ECP-007`. The consumer
repository is created by the test from an empty directory with the built
wheel, never from this repository's tree. The identifier inventory is a
grep over the wheel's unpacked contents with a pattern written from the
requirement (`RLS-SEH-`, `VREC-SEH-`, `REL-SEH-`, `WO-SEH-`), and the skill
inventory compares each `SKILL.md` claim against a subprocess trace captured
by the test.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-012` fresh consumer passes doctor | test and demonstration: `init`, `git init`, commit, `doctor` in an empty directory on each platform | the wheel built from the candidate; a consumer with no verification record | `doctor` exits 0 with no `FAIL` line (today it prints `FAIL hash-bound-class-declared` and `FAIL hash-bound-attribute-effective` and exits 1; complexity audit P0-1, `docs/notes/complexity-audit-2026-08.md:108-116`) |
| `REQ-ECP-013` no product code names this repository's records | analysis: identifier grep over the unpacked wheel and the rendered template; test: the same grep as a packaged test | wheel contents; `templates/repository/standard/` as installed by `init` | zero matches in `se_harness/`, in installed scripts, and in the rendered template (today `se_harness/legacy_release_evidence.py:30-36`, `templates/repository/standard/scripts/validate_engineering_artifacts.py`, and `.github/scripts/publish_dashboard.py:76` match); the six historical records stay exempt through data declared in this repository only |
| `REQ-ECP-014` a shipped skill invokes the evaluator it describes | inspection: each shipped `SKILL.md` against its script; test: subprocess trace of each script | every skill under `templates/repository/standard/.agents/skills/` | every script whose `SKILL.md` says it invokes the evaluator spawns the released evaluator in the trace and prints no `"evaluator_invoked": false`; any skill that cannot is absent from the wheel and from the rendered template (today `check_scope.py:190-199`, `check_prepare.py:174-180`, and `guard.py:177-185` stub the client) |

## Acceptance scenarios

### Scenario 1: init, commit, doctor

In an empty directory on each platform, install the wheel outside the
directory, run `harnessctl init .`, `git init`, commit, `harnessctl doctor .`.
Assert exit 0 and no `FAIL`.

### Scenario 2: failure path, doctor still detects damage

In the same consumer, edit one managed file. Assert `doctor` exits 1 naming
the file, so the pass in Scenario 1 is not a silenced check.

### Scenario 3: identifier sweep

Unpack the wheel and run the identifier grep. Assert zero matches. Render
`init` into a consumer and grep again. Assert zero matches.

### Scenario 4: failure path, the exemption still holds here

In this repository, run the validator with the six historical records
present. Assert the same exemption outcome as before the change, now sourced
from data under `docs/engineering/`, not from a constant.

### Scenario 5: a stubbed skill is absent from the wheel

Add a fixture skill whose script injects a stub client. Build the wheel.
Assert the packaging check refuses the build or the skill is excluded, with
a diagnostic naming the skill.

### Scenario 6: the surviving skill really calls the evaluator

Run each retained skill script under a subprocess trace. Assert the traced
argv resolves to the released evaluator launcher and the result carries the
evaluator's schema-2 block.

## Property and invariant tests

- For every managed-file class in `hash_bound_classes.json`, the class
  either matches at least one path in the rendered consumer or is declared
  optional; no class fails on absence alone.
- The identifier grep is stable across both platforms and across two
  builds of the same commit.

## Static and architecture checks

- `grep -rn "RLS-SEH-" se_harness templates` returns nothing.
- `se_harness/governance_migration.py`, `se_harness/recovery_rehearsal.py`,
  and `scripts/validate_governor_transition.py` are absent, or absent from
  the wheel's `RECORD` where retained under `repository_tools/`.
- The wheel imports no name from `repository_tools` (today
  `qualify predecessor-view` does; the 2026-08 agentic execution review,
  section 5, weakness 5).

## Security and privacy checks

- The rendered consumer contains no path, hostname, or identifier from this
  repository's release history.

## Performance and resilience checks

- `init` plus `doctor` in the consumer completes within 60 seconds on both
  platforms; figures recorded.

## Manual assessments

The quality owner reads every retained `SKILL.md` and confirms each claim
about invocation is matched by a traced subprocess in the evidence.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/<WO-ID>/`: the
consumer transcript per platform, the `doctor` output, the grep inventories
before and after, the wheel `RECORD`, the subprocess traces, and
per-platform test figures.

## Pass criteria

Every deterministic test passes on Linux and on Windows, figures labelled per
platform. Scenario 1 is demonstrated on both platforms with the wheel built
from the candidate and installed outside the consumer directory. Graph and
integrity readings in this repository come from the exact released
evaluator, se-harness 0.7.1, installed outside the checkout.

## Residual uncertainty

The identifier pattern is specific to this repository's prefixes; a future
prefix needs the pattern extended. Skill invocation is traced on the two CI
platforms and not on every host an agent may use.
