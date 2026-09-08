# Plugin integration

These deliveries introduce the Codex and Claude Code compatibility probes from [PR #416](https://github.com/mmzen/se_harness/pull/416), reviewed at `be8b4126`. Lifecycle authority is recorded in each artifact's metadata. Each probe uses its own work order and implementation branch.

- [Requirement: establish the Codex activation sequence](requirements/REQ-PLG-006.md)
- [Specification: reproducible Codex compatibility assessment](specifications/SPEC-PLG-003.md)
- [Verification contract: compatibility evidence](verification/VER-PLG-003.md)
- [Work order: probe Codex activation in isolated fixtures](work-orders/WO-PLG-003.md)

- [Requirement: establish the Claude Code activation sequence](requirements/REQ-PLG-007.md)
- [Specification: reproducible Claude Code compatibility assessment](specifications/SPEC-PLG-004.md)
- [Verification contract: Claude Code compatibility evidence](verification/VER-PLG-004.md)
- [Work order: probe Claude Code activation in isolated fixtures](work-orders/WO-PLG-004.md)

See the [definition-delivery plan](../../notes/plugin-definition-delivery-2026-09-08.md) for the remaining introductions. Production adapters and support decisions are separate work.
