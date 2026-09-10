# Plugin integration

These deliveries introduce the plugin packets from [PR #416](https://github.com/mmzen/se_harness/pull/416), reviewed at `be8b4126`. Lifecycle authority is recorded in each artifact's metadata. Each implementation uses its own work order and branch.

## Shared assembly and runtime definitions (D03)

WO-PLG-001 and WO-PLG-002 are implemented. Their verified records are
[VREC-PLG-003](verification-records/VREC-PLG-003.md) and
[VREC-PLG-004](verification-records/VREC-PLG-004.md).

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

## Shared session and tool handlers (D04)

The operator accepted [DEC-PLG-001](decisions/DEC-PLG-001.md) and
[DEC-PLG-002](decisions/DEC-PLG-002.md) for the tested Windows activation routes.
The shared definitions are approved. WO-PLG-007 is implemented. WO-PLG-008's
implementation and lifecycle decisions are delivered separately in
[PR #436](https://github.com/mmzen/se_harness/pull/436); its local definition and
the production adapter/helper work orders remain draft in this delivery.

- [Session contract](specifications/SPEC-PLG-007.md), [verification](verification/VER-PLG-007.md), [WO-PLG-007](work-orders/WO-PLG-007.md), and [evidence](evidence/WO-PLG-007/README.md)
- [Tool-action contract](specifications/SPEC-PLG-008.md), [verification](verification/VER-PLG-008.md), and [WO-PLG-008](work-orders/WO-PLG-008.md)
- [Host architecture](architecture/ARCH-PLG-002.md) and [decision](architecture/adr/ADR-PLG-002.md)
- [Codex adapter](work-orders/WO-PLG-005.md), [Claude adapter](work-orders/WO-PLG-006.md), and [optional helpers](work-orders/WO-PLG-014.md): definitions only

The remaining introductions and notes are in [PR #416](https://github.com/mmzen/se_harness/pull/416).
Shared handler fixtures do not qualify native host delivery or universal interception.

## D05: WO-PLG-010 delegated skill packet

- [REQ-PLG-017](requirements/REQ-PLG-017.md)
- [REQ-PLG-018](requirements/REQ-PLG-018.md)
- [SPEC-PLG-010](specifications/SPEC-PLG-010.md)
- [VER-PLG-010](verification/VER-PLG-010.md)
- [WO-PLG-010](work-orders/WO-PLG-010.md)

This definition delivery records the operator-selected execution delegation. Implementation starts separately after the delegation is present on `origin/main` and the current required GitHub check passes. The packet does not provide implementation evidence or an assurance decision.

## D06: WO-PLG-011 delegated skill packet

- [REQ-PLG-019](requirements/REQ-PLG-019.md)
- [SPEC-PLG-011](specifications/SPEC-PLG-011.md)
- [VER-PLG-011](verification/VER-PLG-011.md)
- [WO-PLG-011](work-orders/WO-PLG-011.md)

This definition delivery records the operator-selected execution delegation. Implementation starts separately after the delegation is present on `origin/main` and the current required GitHub check passes. The packet does not provide implementation evidence or an assurance decision.
