+++
id = "WO-HAG-010"
type = "work_order"
title = "Keep hosted setup separate from checkout activation"
status = "draft"
owners = ["mmzen"]
created = "2026-10-07"
updated = "2026-10-07"

[execution_scope]
paths = ["plugins/verity-plane/common/assets/bootstrap.md", "plugins/verity-plane/common/skills/setup/SKILL.md", "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-010.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-001.md", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-002.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-010/"]

[relations]
implements = ["REQ-HAG-011"]
specifications = ["SPEC-HAG-007"]
architecture = ["ARCH-HAG-003", "ADR-HAG-003"]
verification = ["VER-HAG-007"]
+++

# Keep hosted setup separate from checkout activation

## Objective

An agent given an explicit hosted test project follows that route without trying
to activate the temporary test directory as a repository. Local checkout work
continues to use the existing activation procedure.

## In scope

1. Route explicit hosted requests before local activation in the bootstrap text.
2. Clarify the matching setup route and reuse an already selected installed client.
3. Rebuild candidate packages and rerun affected native qualification with the
   normal hooks, Skill tool and approved permission checks intact.
4. Retain the failed trial, proposed correction, actual checks and exact component
   identities. Assess the correction with WO-HAG-009 under VER-HAG-007.

## Out of scope

No hook, activation, evaluator, service or client implementation change. No new
configuration, selection store, protocol, authority, permission bypass, public
release, actual host-plugin update, merge or changed acceptance criterion.
Automatic startup/resume/compaction and desktop qualification remain excluded.
The native run must still receive its normal startup instructions.

## Authorized decision envelope

After human approval, the agent may implement the two instruction edits, build
and check disposable packages, retain evidence and prepare commit-bound
verification. The required verification classification is proposed because later
host qualification depends on these instructions. Record the confirming human
in `[assurance]` only after the actual decision.

The requested publication grant adds this correction and its evidence to draft
PR #543 in mmzen/se_harness, from codex/hosted-agent-qualification to main. It
includes a later ready record and separately supplied human verification decision.
It grants no human verification decision, merge, release or deployment. Existing
WO-HAG-009 execution and publication authority remain unchanged.

## Constraints

Reuse REQ-HAG-011, SPEC-HAG-007, ARCH-HAG-003/ADR-HAG-003 and VER-HAG-007 unchanged.
Git remains authoritative. Keep the exact released 0.22.1 governor separate from
the candidate remote client. Preserve WO-HAG-009 approval and all earlier failed
runs and qualification evidence. RISK-HAG-001 and RISK-HAG-002 remain raised.

## Expected change surface

| Path | Purpose |
| --- | --- |
| `plugins/verity-plane/common/assets/bootstrap.md` | Add explicit hosted routing before the existing local checkout procedure |
| `plugins/verity-plane/common/skills/setup/SKILL.md` | Make the hosted route terminal with respect to checkout activation; reuse the selected client |
| `docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-010.md` | This bounded draft and later matching decisions |
| `docs/engineering/hosted-artifact-graph/README.md` | Link the correction and its actual state |
| `docs/engineering/hosted-artifact-graph/risks/RISK-HAG-001.md`, `risks/RISK-HAG-002.md` in this domain | Add affected work links, preserving status and history |
| `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-010/` | Proposed text review, check evidence, handoff and verification preparation |

The existing package test checks exact bootstrap and setup bytes in both host
archives. Existing activation/delivery tests exercise the preserved local route.
No test code change is planned; WO-HAG-009 already covers native test drivers.
The existing package assembler consumes these files without a code change.
No CI, version, lock, schema or deployment change is needed.

The actual VREC is not allocated yet. A record directly verifying this work and
its declared evaluator sidecar are expected to use the released generated-output
rule. Check their exact returned paths at capture; no parent directory is granted.

## Required verification

Run existing package and activation/delivery checks, source suite, distribution
checks, CLI smoke, released validation, scope and handoff checks. Review that the
local activation wording is preserved under its route. Rebuild the changed
guidance and rerun affected native cases from fresh recorded test projects.
VER-HAG-007 still requires NQ-01 through NQ-05 for both hosts. No failed, assisted,
skipped or unavailable case becomes a pass. Evidence reuse needs exact component
comparison and a stated limit; it must not hide an affected instruction change.

## Evidence to record

Retain the correction review and checks under this work order's evidence path.
The full native transcripts remain under WO-HAG-009 with digest references here.
Retain candidate/package identities, actual commands, failures, real checkout
and host state comparisons, and the exact instruction reads. The interrupted
Claude activation has no returned result; retain that uncertainty and readback.
Synthetic VREC/RLS records never verify this actual work.

## Stop and escalate conditions

Stop affected work for a denied operation, write outside the test boundary,
new implementation path, required hook/runtime change, changed accepted meaning,
missing evidence or failed required check. Do not disable the hook to hide the
conflicting instruction. Preserve existing authority for independent work.

## Completion report format

State the delivered route, tested candidate, native outcomes, actual checks,
retained failures and limits. Report the released evaluator's next step.
Implementation completion supplies no human verification or merge decision.
