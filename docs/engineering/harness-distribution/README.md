# Standard Harness Distribution Packet

This packet governs the reusable `se-harness` repository and its single standard installation. It explicitly excludes `minimal`, `offline`, and other selectable profiles.

Artifact chain:

Base distribution chain:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-001..006` -> `SPEC-DST-001`, `ARCH-DST-001`, `ADR-DST-001`, `VER-DST-001` -> `WO-DST-001` -> `REL-DST-001`, `OPS-DST-001`.

Cross-agent and repository-context extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-007..008` -> `SPEC-DST-002`, `ARCH-DST-002`, `ADR-DST-002`, `VER-DST-002` -> `WO-DST-003`.

PyPI-first public onboarding and package-metadata extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-009..013` -> `SPEC-DST-003`, `ARCH-DST-003`, `ADR-DST-003`, `VER-DST-003` -> `WO-DOC-003`.

Practical value example and semantic-graph extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-014` -> `SPEC-DST-004`, `ARCH-DST-004`, `ADR-DST-004`, `VER-DST-004` -> `WO-DOC-005`.

Canonical artifact-layout and domain-authoring extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-015..018` -> `SPEC-DST-005`, `ARCH-DST-005`, `ADR-DST-005`, `VER-DST-005` -> `WO-DST-004`.

Progressive current-documentation extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-019..023` -> `SPEC-DST-006`, `ARCH-DST-006`, `ADR-DST-006`, `VER-DST-006` -> `WO-DOC-007`.

Concise public entry-point and layered-reference extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-024..028` -> `SPEC-DST-007`, `ARCH-DST-007`, `ADR-DST-007`, `VER-DST-007` -> `WO-DOC-008`.

Canonical Harness Explorer WebUI extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-029..033` -> `SPEC-DST-008`, `ARCH-DST-008`, `ADR-DST-008`, `VER-DST-008` -> `WO-DST-007`.

Validation and inspection documentation synchronization extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-034` -> `SPEC-DST-009`, `VER-DST-009` -> `WO-DOC-012`.

No architecture or ADR is selected for `REQ-DST-034`: the correction preserves the existing layered documentation responsibilities and introduces no architecturally significant requirement driver.

Concise Explorer Overview and bounded graph-context extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-035..039` -> `SPEC-DST-010`, `VER-DST-010` -> `WO-DST-011`.

No new architecture or ADR is selected for `REQ-DST-035..039`: the proposed presentation refinement remains within `ARCH-DST-008` and `ADR-DST-008` without changing the canonical model, provenance identity, dependency direction, trust boundary, runtime dependency, or deployment architecture.

The accountable human authorized creation and implementation of this new repository on 2026-08-11. Release remains a separate human decision governed by `REL-DST-001`.

Revision-provenance support added after this packet is governed independently under `../revision-provenance/` and does not reopen `WO-DST-001`.

The accountable human approved `WO-DST-003` on 2026-08-11 by accepting the recommended harness changes. Verification and release transitions remain separate accountable decisions.

The accountable human requested the `WO-DOC-003` artifact packet on 2026-08-11 after reviewing the proposed README and package-metadata changes, then approved the chain and bounded implementation with `ok go for implementation`. A distribution build, CI baseline-pin change, version change, release selection, and publication remain outside this work order. No standalone release contract is created; a future aggregate release contract must explicitly select this work when a version is planned.

The accountable human requested the `WO-DOC-005` artifact packet on 2026-08-11 after reviewing the proposed user-perspective example and semantically colored graph, then approved its governing chain and bounded implementation with `go for implementation`. The implementation and retained evidence are complete; commit, verification capture, push, pull request, build, release, tag, publication, and deployment remain separately controlled.

The accountable human requested the `WO-DST-004` artifact packet on 2026-08-11 after reporting that a consumer installation placed formal artifacts directly below its business-domain directory rather than in the distribution repository's type-specific structure, then approved the governing chain and bounded implementation with `go for implementation`. Implementation and retained evidence are complete. Migration of the consumer repository, commits, pull requests, verification transitions, and release actions remain separately controlled.

The accountable human requested the `WO-DOC-007` packet on 2026-08-12 to make the public README and human notes current, progressive, and explicit about reader expertise, then authorized the bounded work with `go for implementation`. The work-order artifact records the current implementation lifecycle. Runtime behavior, Explorer gate computation, managed policy, commit, push, pull request, verification transition, and release actions remain outside this documentation implementation authority.

The accountable human agreed with the concise-root proposal, requested `WO-DOC-008` and its governing packet, then explicitly authorized implementation on 2026-08-12 with `go for implementation`. The bounded documentation and focused-test work is complete with retained evidence. Behavior changes, commit-bound verification, commit, push, pull request, build, release, publication, deployment, and external configuration remain separately controlled.

The accountable human reviewed the canonical Explorer WebUI proposal and its `REQ-DST-029..033` packet, then explicitly authorized `WO-DST-007` on 2026-08-13 with `go implementation`. During review of the uncommitted candidate, the owner required preservation of the original prototype structure, visual identity, and CDN-backed `3d-force-graph`; `ADR-DST-008` records the accepted runtime risk. The model-faithful, deterministic, secure, and distributable integration is complete with retained evidence. Commit-bound verification, commit, push, pull request, release, publication, and deployment remain separately controlled.

The accountable human created and authorized `WO-DST-009` to integrate a refined Explorer presentation, then explicitly directed removal of the redundant `templates/webui/` design-source directory on 2026-08-15. The canonical standard template is now the sole reusable WebUI source, with a byte-equivalent active root copy and retained verification evidence. Historical artifacts continue to describe the prototype review that led to the canonical implementation; they do not require a duplicate runtime or design source to remain installed.

After reviewing the documentation impact of the layered validator and new inspection command, the accountable human instructed `yes go for the correction artifact packet` on 2026-08-15, then approved `REQ-DST-034`, `SPEC-DST-009`, `VER-DST-009`, and `WO-DOC-012` with `ok go for implementation`. The active six-command documentation contract, four progressive notes, focused assertions, and retained work-order evidence are complete. Runtime behavior and historical assurance facts remain unchanged. Candidate commit, deletion or replacement of the existing ready VREC, VREC preparation or transition, push, pull-request mutation, merge, release, publication, and deployment remain separately controlled.

On 2026-08-16, `WO-OCA-002` explicitly migrated `OPS-DST-001.assures` from the legacy release-contract target to `REQ-DST-001..006`, the requirement scope of its original accepted distribution packet. The approved contract's meaning and status are unchanged; later distribution requirements are not inferred into its scope.

On 2026-08-16, the repository owner authorized `WO-DST-010` to reassess `ARCH-DST-007` and `ARCH-DST-008` against their newer declared definitions, then explicitly authorized the resulting ADR reaffirmation. The reassessment confirmed that both architectures and accepted ADR outcomes remain applicable, corrected one source-copy phrase and one obsolete command list, and removed the resulting `W-HEX-003` observations without changing product behavior, governing definitions, inspection rules, or external lifecycle state. Retained evidence records the bounded review.

On 2026-08-16, after challenging the initial arbitrary-depth proposal, the repository owner requested the `WO-DST-011` packet for a shorter Explorer Overview and bounded `0 / 1 / 2` context around graph-filter matches. During definition, the owner accepted additional requirements for legible presentation-only observed-revision prefixes, generic sidebar containment, and a direct artifact-filter clear control while preserving full provenance identity and other graph choices, then explicitly authorized the complete bounded implementation. Before candidate commit, owner review identified duplicate state/type/assurance colors caused by the five-slot hash palette and required stable distinct colors within each analysis mode. `REQ-DST-035..039`, `SPEC-DST-010`, and `VER-DST-010` are approved; `WO-DST-011` is implemented with retained evidence. Commit, VREC, pull request, release, package publication, public-demonstrator update, and deployment remain separately controlled.
