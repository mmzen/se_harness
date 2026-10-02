+++
id = "WO-RLO-017"
type = "work_order"
title = "Cover the generated complete-release verification evidence"
status = "draft"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[execution_scope]
paths = [
  "docs/engineering/release-orchestration/evidence/VREC-RLO-014-evaluator.json",
  "docs/engineering/release-orchestration/verification-records/VREC-RLO-014.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-017.md",
  "docs/engineering/release-orchestration/evidence/WO-RLO-017/",
]

[relations]
implements = ["REQ-RLO-021", "REQ-RLO-022", "REQ-RLO-023"]
specifications = ["SPEC-RLO-007"]
verification = ["VER-RLO-011"]
architecture = ["ARCH-RLO-006", "ADR-RLO-006"]
+++

# Cover the generated complete-release verification evidence

## Objective

Complete the already approved verification preparation at the actual output
locations used by the selected released evaluator, without changing approved
work-order history or product behavior.

## In scope

The selected 0.21.0 evaluator always writes the generated evaluator identity
evidence to `docs/engineering/release-orchestration/evidence/VREC-RLO-014-evaluator.json`.
Its `--output` option changes only the Markdown record location. WO-RLO-014/015/016
incorrectly reserved both files under `verification-records/`. The scope check
refused the real JSON destination with `QGP-G4I-PATHS` / `WEX201`.

This supplementary work order admits that exact JSON file, the matching
verification record, its own lifecycle record, and the retained correction review.
Capture VREC-RLO-014 for WO-RLO-014/015/016/017 under VER-RLO-011. Leave all accepted
definitions and the previous work orders' scope and lifecycle history intact.

## Proposed assurance classification

Required commit-bound verification, included in VREC-RLO-014. The human must
confirm this classification before approval. The result will bind the actual
evaluator identity and assessed candidate used in the later verification decision.
No human classification or decision is asserted in this draft.

## Authorized decision envelope

On approval, allow local checks, execution, completion and capture at the named
destinations. Extend the existing review-delivery grant only to these correction
files on `work/complete-release-approval`, draft PR #527 to `mmzen/se_harness:main`,
and its later verification-decision update. Human verification, merge, actual
release/publication and live provider settings remain separate.

## Out of scope

No product code, tests, release behavior, accepted definitions, prior work-order
semantics, provider settings, credentials, releases, tags or package publication.
Do not patch the installed evaluator or hand-edit its generated binding fields.

## Required verification and evidence

Use the selected released 0.21.0 evaluator. Check the generated destinations and
record bindings, assess the union of all four work-order scopes against the
original trusted base, and capture the complete candidate under VER-RLO-011.
Reuse the retained product tests where source is unchanged. Run the final
commit-bound full suite during capture. Retain the refusal, source inspection,
destination review and actual result under this work order's evidence directory.

## Stop conditions

Stop on a changed VREC identity, another generated destination, failed required
checks or mismatched evaluator identity. Do not silently extend this scope.

## Completion report

Report the generated destinations, exact candidate, checks and remaining human
verification decision. This correction does not accept the implementation.
