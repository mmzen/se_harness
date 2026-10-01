# Release 0.21.0 preparation

Human mmzen approved this package and required commit-bound verification on
2026-10-01. WO-RLS-031 is in progress; WO-RLS-032/033 are approved and await their
public inputs. The v0.21.0 publication request is retained. No final aggregate
VREC, RLS, tag or public package has been created yet. This repository continues
to use released evaluator 0.20.1.

| Stage | Work order | Verification |
| --- | --- | --- |
| Final evaluator candidate, pinned build, aggregate verification and RLS | [WO-RLS-031](work-orders/WO-RLS-031.md) | [VER-RLS-030](verification/VER-RLS-030.md) |
| Plugin 0.2.4 assembly and native qualification after public evaluator release | [WO-RLS-032](work-orders/WO-RLS-032.md) | [VER-RLS-031](verification/VER-RLS-031.md) and existing VER-IAR-021 |
| Public fresh/update routes, current documentation and delivery closeout | [WO-RLS-033](work-orders/WO-RLS-033.md) | [VER-RLS-032](verification/VER-RLS-032.md) |

[REL-SEH-033](release/REL-SEH-033.md) selects the exact release work set, final
verification sequence and five delivery surfaces. Reuse accepted definitions and
existing tools; no new product requirement, framework or approval artifact is added.

## Review inputs

- Proposed evaluator: 0.21.0. Proposed plugin: 0.2.4, after public maintenance 0.2.3.
- Preparation base: f5f7c77c6eadfd7d6f1c68e136f1f7cc29cfc0a5.
- Confirmed assurance: required commit-bound verification for all three work orders.
- Review envelope: ordinary release-review branch push/draft PR and read-only
  existing build/replay workflow dispatches under WO-RLS-031.
- Human verification of the final candidate, exact RLS decision, merges, protected
  provider approval, marketplace publication and marker changes remain distinct.
- Existing evaluator publication and repository-adoption requests are retained.

## Unresolved qualification

VER-IAR-021 explicitly requires Codex Windows desktop native evidence. It remains
unverified. CLI and app-server evidence do not substitute. This package keeps the
criterion pending before release; it does not propose a waiver. Native checks may
use existing authorized test authentication in disposable profiles.

## Current observations

On 2026-10-01, main is the merged implementation above. GitHub has no v0.21.0 tag
or release; its latest release is v0.20.1. Existing VRECs accept their individual
candidates. None is a final aggregate covering REL-SEH-033's complete member set.
Current main host manifests still contain 0.2.2; the public 0.2.3 maintenance
package is separate. WO-RLS-031 will select the new identity without rewriting
either published package. Future build hashes and record IDs remain unallocated.
