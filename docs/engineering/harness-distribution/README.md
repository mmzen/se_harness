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

The accountable human authorized creation and implementation of this new repository on 2026-08-11. Release remains a separate human decision governed by `REL-DST-001`.

Revision-provenance support added after this packet is governed independently under `../revision-provenance/` and does not reopen `WO-DST-001`.

The accountable human approved `WO-DST-003` on 2026-08-11 by accepting the recommended harness changes. Verification and release transitions remain separate accountable decisions.

The accountable human requested the `WO-DOC-003` artifact packet on 2026-08-11 after reviewing the proposed README and package-metadata changes, then approved the chain and bounded implementation with `ok go for implementation`. A distribution build, CI baseline-pin change, version change, release selection, and publication remain outside this work order. No standalone release contract is created; a future aggregate release contract must explicitly select this work when a version is planned.

The accountable human requested the `WO-DOC-005` artifact packet on 2026-08-11 after reviewing the proposed user-perspective example and semantically colored graph, then approved its governing chain and bounded implementation with `go for implementation`. The implementation and retained evidence are complete; commit, verification capture, push, pull request, build, release, tag, publication, and deployment remain separately controlled.

The accountable human requested the `WO-DST-004` artifact packet on 2026-08-11 after reporting that a consumer installation placed formal artifacts directly below its business-domain directory rather than in the distribution repository's type-specific structure, then approved the governing chain and bounded implementation with `go for implementation`. Implementation and retained evidence are complete. Migration of the consumer repository, commits, pull requests, verification transitions, and release actions remain separately controlled.
