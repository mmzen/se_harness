# Technical Communication Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain proposes one managed technical-communication policy and the first
portable skill that consumes it. The policy uses selected ASD-STE100-based
clarity principles. It does not claim ASD-STE100 compliance, bundle or download
the standard, or permit writing style to change engineering authority or
technical meaning.

## Draft definition packet

- `INT-TCM-001`: make agent communication clear without weakening precision or authority.
- `CAP-TCM-001`: let supported agents produce clear operator briefs and readable technical prose from one managed policy.
- `REQ-TCM-001`: distribute one managed ASD-STE100-based communication policy.
- `REQ-TCM-002`: preserve protected content and technical meaning.
- `REQ-TCM-003`: apply distinct operator and technical-artifact profiles.
- `REQ-TCM-004`: provide the explicit read-only `harness-operator-brief` skill.
- `SPEC-TCM-001`: define the policy, profile, skill, installation, and failure contracts.
- `ARCH-TCM-001`: separate managed communication authority from replaceable skill and runtime execution.
- `ADR-TCM-001`: select one managed policy consumed by non-authoritative skills.
- `VER-TCM-001`: verify integrity, protected-content preservation, skill boundaries, meaning, and usability.
- `WO-TCM-001`: implement the complete bounded first increment after approval and an explicit start decision.

Every artifact remains `draft`. This packet authorizes no implementation,
lifecycle transition, Git action, network access, standard download, or
external action.

`REQ-TCM-005`, `SPEC-TCM-002`, `VER-TCM-002` and `WO-TCM-003` are drafted and approved on 2026-08-31 for [issue #281](https://github.com/mmzen/se_harness/issues/281) item #281b, the last piece of the functional assessment's FA-2: a generated diagnostic-code index. `repository_tools/diagnostic_code_index.py` parses the candidate source's string literals (comments and identifiers never contribute), keeps a curated registry of the diagnostic prefixes, derives the run-time-composed record-preparation codes from the same source facts, and renders `docs/notes/diagnostic-codes.md` deterministically; `tests/test_diagnostic_code_index.py` fails the suite on any drift. Artifact and specification identifiers, which share the code shape, are excluded by construction. The page is linked from the notes index and beside the `check` note's small refusal table. The hash-locked root `scripts/` copies are the released evaluator's files and are not scanned.
