# Evidence Keying Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This draft packet governs how normalized retained-evidence paths are attributed to work orders without requiring established repositories to rename commit-bound evidence.

Chain: `INT-EVK-001` -> `CAP-EVK-001` -> `REQ-EVK-001..004` -> `SPEC-EVK-001`, `ARCH-EVK-001`, `ADR-EVK-001`, `VER-EVK-001` -> `WO-EVK-001`.

The packet proposes a backward-compatible expansion from filename-only attribution to exact work-order keys in filenames or path components at or below a literal `evidence` directory. It keeps package and repository-local execution planes independent, preserves existing path-safety checks, and requires equivalent results from capture, validation, inspection, and Harness Explorer.

The accountable repository owner approved the intent-through-verification chain and `WO-EVK-001` on 2026-08-19 with the instruction `go implement`. The bounded implementation is recorded as `implemented` with retained work-order evidence. Commit-bound verification remains pending a later candidate commit and accountable VREC; no historical-record rewrite, release build, publication, or governor change was performed.
