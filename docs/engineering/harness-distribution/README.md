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

Structured and reversible Explorer Lineage extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-040..041` -> `SPEC-DST-011`, `VER-DST-011` -> `WO-DST-012`.

No architecture or ADR relation is selected for `REQ-DST-040..041`: the Lineage board and in-memory navigation history are routine browser-presentation refinements inside the responsibilities and boundaries of `ARCH-DST-008` and `ADR-DST-008`; those architecture artifacts do not declare that they address the new requirements.

Safe content-rich Explorer detail extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-042..047` -> `SPEC-DST-012`, `ARCH-DST-009`, `ADR-DST-009`, `VER-DST-012` -> `WO-DST-013`.

`ARCH-DST-009` addresses the architecturally significant untrusted-content and evidence-publication drivers in `REQ-DST-043` and `REQ-DST-046`, conforms to `SPEC-DST-012`, and records `adr_required`. `ADR-DST-009` accepts the additive, bounded, locally rendered and sanitized content pipeline; the remaining requirements are presentation behavior governed by the same specification without fabricated architecture coverage.

Integrity-addressed progressive Explorer extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-048..055` -> `SPEC-DST-013..014`, `ARCH-DST-010`, `ADR-DST-010`, `VER-DST-013..014` -> `WO-DST-014..015`.

`WO-DST-014` owns deterministic static partitioning, manifest integrity, transactional output, payload budgets, static hosting, and Pages exact-set validation. `WO-DST-015` owns verified progressive browser acquisition, revision-scoped caching, asynchronous failure/race containment, and preserved navigation/rendering semantics. `ARCH-DST-010` addresses the significant protocol, data-partition, trust, deployment, reliability, and performance drivers in `REQ-DST-049`, `REQ-DST-050`, `REQ-DST-052`, `REQ-DST-054`, and `REQ-DST-055`, conforms to both specifications, and records `adr_required`; `ADR-DST-010` selects content-addressed static sharding rather than compression-only, page-only bulk data, a backend, persistent browser storage, or binary range access.

Owner-authorized Explorer dashboard revision:

`REQ-DST-030`, `REQ-DST-032..033`, `REQ-DST-035`, `REQ-DST-040..042`, `REQ-DST-045`, `REQ-DST-047`, `REQ-DST-050`, and `REQ-DST-055` -> `SPEC-DST-017`, `VER-DST-017` -> `WO-DST-018`, within the boundaries selected by `ARCH-DST-008`, `ADR-DST-008`, `ARCH-DST-010`, and `ADR-DST-010`. The repository owner authorized the supplied template revision, two later browser-identified route-safety corrections, a 262,144-byte generated `index.html` ceiling, and controlled same-document URL fragments plus History API state for Explorer navigation. Persistent browser storage, additional runtime URLs, transferred authority, publication, and deployment remain excluded.

Additive single-runtime consumer GitHub CI extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-056..059` -> `SPEC-DST-015`, `ARCH-DST-011`, `ADR-DST-011`, `VER-DST-015` -> `WO-DST-016`.

The approved packet specifies one dedicated managed workflow that GitHub discovers beside any existing workflows, one exact isolated released evaluator for all consumer harness semantics, package-owned CI execution, and the ordinary init/adopt/upgrade transaction as the only consumer installation and upgrade path. `ARCH-DST-011` records the significant runtime-role, trust, dependency, deployment, and ownership boundary; `ADR-DST-011` accepts removing the consumer-only bootstrap while preserving the implementation repository's independent released-governor and candidate planes.

Explicit artifact-collision recovery extension:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-061` -> `SPEC-DST-019`, `ARCH-DST-012`, `ADR-DST-012`, `VER-DST-019` -> `WO-DST-019`.

The approved packet governs the implemented plan-by-default `harnessctl renumber-artifacts` command for explicit pre-assurance identifier mappings. It transactionally changes parsed identities, typed relations, and mapped paths; reports free-form hard references for manual review and change; preserves retained evidence contents byte-for-byte; blocks any selected artifact referenced by a VREC or RLS; and leaves reviewable uncommitted changes. Identifier allocation, ref scanning, PR collision detection, VREC/RLS renumbering, semantic text rewriting, commits, and external actions remain outside the implementation.

Repository-context retirement:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-065` -> `SPEC-DST-021`, `VER-DST-021` -> `WO-DST-021`.

No architecture or ADR relation is selected for `REQ-DST-065`: the change withdraws a scaffolded document, a required-path check, a diagnostic family, and one report field, and no active architecture declares that it addresses the new requirement. `ARCH-DST-002`, `ARCH-DST-007`, and `ARCH-IAR-001` describe the withdrawn document, all three through the deprecated `constrains` relation. The technical owner recorded that applicability decision at approval on 2026-08-21: none of the three requires revision beyond its descriptive references, and no deciding ADR is required, because the change withdraws a scaffolded component and an unreachable extension point without altering a selected boundary, dependency direction, or trust boundary. `WO-DST-021` also implements `REQ-IAR-021` under `../instruction-architecture/`, because the scaffold cannot be withdrawn without revising the managed router in the same change.

`REQ-DST-065`, `SPEC-DST-021`, and `WO-DST-021` are `implemented`; `VER-DST-021` remains `approved` because a verification transition is a separate accountable decision. Evidence is retained at `evidence/WO-DST-021-verification.md` for `VER-DST-021` and at `../instruction-architecture/evidence/WO-DST-021-verification.md` for `VER-IAR-013`.

Topology acceptance headroom amendment:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-062..064` -> `SPEC-DST-020`, `ARCH-DST-013`, `VER-DST-020` -> `WO-DST-020`.

The implemented packet raises only the candidate distribution's SE Harness topology acceptance target from 524,288 to 2,097,152 UTF-8 bytes. It preserves bundle-v2 data and integrity, every other content budget, the existing no-sharding architecture, and the independently installed public-0.5.0 managed root. Commit, VREC, release, root upgrade, and external actions remain separate decisions.

Leaving-set managed-path retirement extension (issue #271):

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-066` -> `SPEC-DST-022`, `VER-DST-022` -> `WO-DST-022`.

No architecture or ADR relation is selected for `REQ-DST-066`: the retirement rule is upgrade-transaction behaviour inside the installer boundary `ARCH-DST-001` already draws, and no active architecture declares that it addresses the new requirement. `SPEC-DST-001`'s upgrade action vocabulary and `SPEC-ECP-007`'s `ECP-SKL-004` are amended by record under `WO-DST-022`.

Designed self-contained Explorer:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-067`, `REQ-DST-068` -> `SPEC-DST-023`, `ARCH-DST-008` (amended), `ADR-DST-013`, `VER-DST-023` -> `WO-DST-023`.

On 2026-09-01, after reviewing the designed Explorer against the complete repository bundle in a local design loop, the repository owner instructed its integration as the canonical template. The packet replaces the previous page's presentation contracts: `REQ-DST-032` and `REQ-DST-036` are superseded by `REQ-DST-067`; `SPEC-DST-008`, `SPEC-DST-010`, `SPEC-DST-011`, `SPEC-DST-012`, `SPEC-DST-016`, `SPEC-DST-017` are superseded by `SPEC-DST-023`, which carries every other approved Explorer requirement forward, while their verification contracts stay active because verified records bind them and `VER-DST-023` verifies the same requirements beside them; `SPEC-DST-013`, `VER-DST-013`, `SPEC-DST-014`, `VER-DST-014`, `ARCH-DST-008`, and `ARCH-DST-009` are amended by record; `ADR-DST-008` records the reassessment that closes its CDN exception. The designed views are retained verbatim under `repository_tools/explorer_design/sources/` and rebuilt deterministically into one self-contained template of at most 524,288 bytes that names no remote origin; the generator gains a `metrics` object and the record proof fields the page presents. The root template and generator remain the released 0.12.0 copies until the next adoption.

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

After that candidate was verified and merged on 2026-08-16, the repository owner requested a separate `WO-DST-012` packet for the accepted focused-Lineage evolution, then explicitly authorized its bounded implementation with `go for implementation`. `REQ-DST-040..041`, `SPEC-DST-011`, `VER-DST-011`, and `WO-DST-012` define a deterministic conceptual-stage/exact-type board, complete direct context, bounded optional second-level context, preserved relation authority, and non-hierarchical reversible navigation. The implementation and retained evidence are complete; candidate commit, VREC, pull request, release, publication, and deployment remain separately controlled.

During review of that uncommitted candidate, the repository owner requested a richer selected-artifact detail panel and accepted the challenged separation between presentation, canonical content projection, trust, and publication. On 2026-08-16 the owner authorized creation of the `WO-DST-013` packet, then explicitly accepted its definitions and authorized bounded implementation with `go implementation`. `REQ-DST-042..047`, `SPEC-DST-012`, `ADR-DST-009`, and `VER-DST-012` remain approved; `ARCH-DST-009` and `WO-DST-013` are implemented with retained evidence. Candidate commit, VREC, pull request, release, package publication, public-demonstrator publication, and deployment remain separately controlled.

On 2026-08-17, after measuring the generated HTML at approximately 2.68 MB and identifying duplicated embedded artifact/evidence bodies, the repository owner accepted the progressive static-bundle proposal and instructed `ok, go for the artifact packet`. Packet creation was interrupted after the requirement layer; the owner then instructed `go for implementation`, accepting the completed `REQ-DST-048..055`, `SPEC-DST-013..014`, `ARCH-DST-010`, `ADR-DST-010`, `VER-DST-013..014`, and bounded `WO-DST-014..015` once structural validation passes. Work is isolated on a stacked branch based on the unchanged PR 63 candidate; the prior ready `VREC-DST-011` is preserved separately and no commit, PR mutation, release, package publication, Pages deployment, or public-demonstrator update is implied.

On 2026-08-17, after inspecting a recently upgraded consumer repository and confirming that its 0.2.1 bootstrap validates only itself while 0.4.0 performs consumer assessment, the repository owner accepted the KISS proposal for one additive dedicated GitHub workflow and one exact released consumer evaluator. The owner then clarified GitHub's independent workflow discovery, requested this artifact packet, reviewed its conflict behavior, and explicitly authorized the bounded implementation with `ok, then go implement`. `REQ-DST-056..059`, `SPEC-DST-015`, `ARCH-DST-011`, and `WO-DST-016` are implemented with retained local evidence; `ADR-DST-011` and `VER-DST-015` remain approved. Commit-bound verification, commit, push, pull request, release, publication, deployment, hosted CI, and external GitHub policy changes remain separately controlled.

On 2026-08-21, after assessing the instruction surface, the repository owner stated the boundary directly: `AGENTS.md` is repository-owned and may carry or point to build and test material; the harness needs a reference to the governance material it owns; and `docs/engineering/REPOSITORY_CONTEXT.md` in its current form sits outside the harness boundary because it concerns only the local repository. The owner proposed keeping `AGENTS.md` as it is today with its marked harness integration, relying on existing repository-owned content for build and test, and removing the repository-context burden entirely to make harness initialization easier. The owner approved `REQ-DST-065`, `SPEC-DST-021`, `VER-DST-021`, and `WO-DST-021` the same day, resolving all three open decisions: the preflight report schema advances to `se-harness-preflight-v2`; the loss of the structured `repository_commands` payload object is accepted with no replacement scaffold and no relocated typed declaration, both alternatives having been put and declined; and no architecture artifact requires revision or a deciding ADR. `WO-DST-021` authorizes the bounded implementation and nothing further. Commit-bound verification, commit, push, pull request, release, publication, and deployment remain separately controlled. The bounded implementation was carried out the same day: the seed template, the readiness gate, the `C` diagnostic family, the `repository_commands` payload field, and the unreachable reference-step action form are withdrawn from the candidate; the report schema is `se-harness-preflight-v2`; `REQ-IAR-005` and `REQ-DST-008` are superseded; and every active governed artifact enumerated in the work order's in-scope list is revised. The repository-root managed copies still describe the released product and are reconciled at publication.

The work order's in-scope list was derived from a scan for the literal path, so it did not reach active artifacts that describe the same obligation in lowercase prose. Implementation measured eleven such artifacts and left every one unmodified, because revising them is outside the authorized envelope. `VER-DST-002` still requires tests proving that `init` creates repository context and that `doctor` rejects a missing repository-context file; `REQ-IAR-006` still states that preflight success output lists the repository-context path and the repository commands; `ADR-DST-002` and `ADR-IAR-001` still record seeding that document as an accepted decision; `INT-IAR-001` still states that readiness blocks on invalid repository context; `SPEC-WEX-002` and `VER-WEX-002` still list unreadable required repository context as a failure category; and `SPEC-DST-002`, `SPEC-DST-003`, `ARCH-DST-006`, and `ADR-DST-006` carry descriptive references. The first six are now factually wrong about the candidate product and need a follow-on governance packet with its own accountable approval; the rest read correctly once "repository context" is understood as the owner-controlled region. `CAP-IAR-001`, `REQ-IAR-001`, `REQ-WEX-007`, `REQ-HUP-002`, and `OPS-VSP-001` were assessed and remain accurate as written.

On 2026-08-20, after issue 80 exposed repeated cross-branch identifier collisions and the broader prevention proposal proved disproportionate, the repository owner selected a narrower recovery command and instructed creation of its artifact packet. `REQ-DST-061`, `SPEC-DST-019`, `ARCH-DST-012`, `ADR-DST-012`, `VER-DST-019`, and `WO-DST-019` remain `draft` pending accountable review. The instruction authorizes packet drafting only; implementation, lifecycle transitions, evidence capture, commit, push, pull request, build, release, publication, and deployment remain unauthorized.

Owner-reviewed Verity Plane public presentation:

`INT-DST-001` -> `CAP-DST-001` -> `REQ-DST-069` -> `SPEC-DST-024`, `VER-DST-024` -> `WO-DOC-014`.

The current README presentation contract replaces earlier root-only format inventories while preserving the linked guides and authority boundaries.
