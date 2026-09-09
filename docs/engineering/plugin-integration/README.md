# Plugin integration

These deliveries introduce the plugin packets from [PR #416](https://github.com/mmzen/se_harness/pull/416), reviewed at `be8b4126`. Lifecycle authority is recorded in each artifact's metadata. Each implementation uses its own work order and branch.

## Shared assembly and runtime definitions (D03)

WO-PLG-001 is implemented. WO-PLG-002 remains draft; introducing its approved
definitions does not start its implementation.

[VREC-PLG-003](verification-records/VREC-PLG-003.md) is verified following the
operator's assurance decision for WO-PLG-001 at candidate `b8d6f04a`.
Repository integration or release requires a separate delivery decision.

- [Published evaluator payload](requirements/REQ-PLG-001.md) and [shared source](requirements/REQ-PLG-002.md)
- [Assembly specification](specifications/SPEC-PLG-001.md), [verification](verification/VER-PLG-001.md), [work order](work-orders/WO-PLG-001.md), and [evidence](evidence/WO-PLG-001/README.md)
- [Python prerequisite](requirements/REQ-PLG-003.md), [runtime identity](requirements/REQ-PLG-004.md), and [atomic environment creation](requirements/REQ-PLG-005.md)
- [Runtime specification](specifications/SPEC-PLG-002.md), [verification](verification/VER-PLG-002.md), and [work order](work-orders/WO-PLG-002.md)
- [Shared architecture](architecture/ARCH-PLG-001.md) and [packaging decision](architecture/adr/ADR-PLG-001.md)

## Compatibility probes (D01 and D02)

- [Requirement: establish the Codex activation sequence](requirements/REQ-PLG-006.md)
- [Specification: reproducible Codex compatibility assessment](specifications/SPEC-PLG-003.md)
- [Verification contract: compatibility evidence](verification/VER-PLG-003.md)
- [Work order: probe Codex activation in isolated fixtures](work-orders/WO-PLG-003.md)

- [Requirement: establish the Claude Code activation sequence](requirements/REQ-PLG-007.md)
- [Specification: reproducible Claude Code compatibility assessment](specifications/SPEC-PLG-004.md)
- [Verification contract: Claude Code compatibility evidence](verification/VER-PLG-004.md)
- [Work order: probe Claude Code activation in isolated fixtures](work-orders/WO-PLG-004.md)

See the [definition-delivery plan](../../notes/plugin-definition-delivery-2026-09-08.md) for the remaining introductions. Production adapters and support decisions are separate work.
