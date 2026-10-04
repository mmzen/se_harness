+++
id = "SPEC-HAG-003"
type = "specification"
title = "Packaged sandbox qualification and coordinated release boundaries"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
contract = "Qualify the actual client, plugin, service, evaluator and database combination through a reproducible Docker sandbox and the complete twelve-step walkthrough, keeping later authority and release decisions separate."

[relations]
specifies = ["REQ-HAG-007", "REQ-HAG-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:32:03Z"
decided_by = "mmzen"
reason = "mmzen approved the current artifact package in this conversation: \"i approve the artifact package\". This applies to the 16 reviewed governing definitions in the Phase 0 package, whose review manifest SHA-256 is fc1009f1b5fbfc3259f9df4057695500ac7ad3b80777f3107155c629eaea99cc. Complete reviewed file hashes were compared immediately before application. This records definition approval only; WO-HAG-001 approval remains unchanged. The user clarification remains: keep using Cypher, defer Memgraph-side read-only enforcement and retain the open item. RISK-HAG-001 remains raised; this decision does not accept that risk, verify implementation or authorize external delivery."
+++

# Packaged sandbox qualification and coordinated release boundaries

## Selected phase and operating scope

The first work package implements Phases 0-2 as one complete sandbox outcome, ending at the twelve-step walkthrough. One disposable project named `hosted-artifact-poc` imports the public reference snapshot. One operator and two author test principals use a local Docker Compose deployment on Linux x86-64, Python 3.11 or later, and Memgraph in transactional storage mode. Windows with Docker Desktop/WSL may host the same Linux containers but is an additional observed host combination, not an assumed pass. Docker Desktop was installed by the user after the initial review. Phase 0 confirmed its Linux engine and Compose are available through the per-user executable; the exact observation is recorded in HAG-OPS-008. Application/container qualification remains Phase 2 work.

### HAG-OPS-001 — Reproducible deployment

`server/` contains its own service package/dependency lock, image recipe, Compose definition, schema initialization/migration command, configuration example, health/readiness and recovery guide. Pin the Memgraph image and server runtime base by immutable digest when building the first runnable candidate; retain the resolved version/platform/digest. Use one Memgraph persistent named volume mounted at its configured data directory with snapshots and WAL enabled. Use a private database network and loopback API binding. Inject test secrets through Compose secret/configuration inputs excluded from source and logs. Do not bundle real credentials or user data.

Initialize a new schema only through an explicit operator command. Normal startup verifies schema revision, evaluator payload, resources, configured project and required database capabilities, then becomes ready. A migration mismatch makes readiness fail; a client request cannot migrate the database. Health means the process is alive; readiness additionally means the declared operations can use the configured store and evaluator. Log request/operation IDs, outcome and component identities without document bodies or credentials by default.

### HAG-OPS-002 — Actual component identities

The candidate-combination report is supporting evidence, not a replacement release record. It identifies source repository/candidate commit, harness package version and digest, plugin package version and digest, each embedded evaluator identity, server version and image digest, Memgraph version/image/configuration digest, API/read-contract versions, evaluator/policy identity and database schema revision. Test the actual installed wheel, assembled plugin guidance and built server image. A source-tree invocation alone is insufficient.

Keep client and governing evaluator separate. The initial remote client is candidate development code; the server's validation evaluator is released 0.22.0 with wheel SHA-256 `44543f242ed19bb30cfd65da415372a87508a6e439204d7f3e37f9f45aefe4e4` and payload SHA-256 `b4464e0c55814ee62a6e844d712503188493dacf841aeac90d5f270e8c6836c9`. Root governance remains this exact released evaluator. If a candidate plugin needs both remote client and governing evaluator, keep both identities explicit and prepare the remote client in a separate candidate environment. Do not replace the governor to make the remote CLI available.

Allocate unpublished development component versions before building and retain their actual values. Never label changed plugin/evaluator bytes as the existing immutable public 0.2.5/0.22.0 package. The implementation may choose unused development versions under the current build conventions; public release versions are a later release-owner decision. An unchanged public component can be reused only with its original identity and a compatibility assessment for the actual combination.

### HAG-OPS-003 — Minimal packaging changes

Keep all components in this repository. Add a dedicated service distribution in `server/`; preserve the core checker package's zero runtime dependencies. Add the remote client under the existing harness package and necessary CLI dispatch only. Use existing plugin assembly and development-package support; its existing manifest includes the selected guidance. Install the candidate client in a separate test environment. A newly discovered need to change the manifest or packager requires a scoped amendment before editing those paths. Reuse the repository build recipe and distribution checks. Do not redesign all release jobs, add independent release pipelines or publish a container registry image in this work order.

The initial supported tuple is the exact built client/plugin/server/evaluator/database set retained by the Phase 2 run, API `se-harness-remote-command/v1`, result `se-harness-remote-result/v1`, read contract `se-harness-graph-read/v1`, baseline `se-harness-artifact-baseline/v1`, and schema revision 1. Reject unsupported tuples before mutation, even when protocol decoding succeeds. Public release qualification later extends the existing release contract and bundle manifest to include the server image and deployment conditions. Existing REL-SEH-034 and historical bundles remain unchanged; no release record is proposed by this sandbox package.

### HAG-OPS-004 — Required walkthrough

1. Build/start the pinned Compose deployment and record actual readiness identities.
2. Import the complete reference source snapshot and retain the deterministic import report.
3. Select WO-RLS-038 at the resulting baseline B.
4. Compare its full governing context, scope and meaningful findings to the pinned released-evaluator oracle, with explicit completeness.
5. Create a new incomplete draft through the packaged `harnessctl remote` client in a context based on B.
6. Revise its body and one valid relationship through that client and observe a new revision.
7. Submit a prohibited relation/type command; observe a specific invalid result and unchanged state.
8. Submit an old expected revision/context/project version; observe conflict. Also change a governing dependency in a disposable variant and prove a pending acceptance is stale.
9. Commit a command, suppress its response, then retry; observe the same accepted receipt with no extra revision or version increment. Reuse the key with different content and observe refusal.
10. Retrieve B and compare its complete selection/content/relations/digest to the original.
11. Retrieve the explicit draft context, compare it to B and distinguish proposed and baseline state. Exercise the MCP reads and bounded Cypher route against this same packaged service.
12. Run the applicable released harness checks on the exact remote selection via its disposable projection. Report findings and limitations without claiming a new lifecycle decision.

No step may be substituted by mocked HTTP, a standalone database query or an unrelated unit test. Supplemental focused tests cover deliberate failure before commit, concurrent keys, server-side denial despite local success, and unsupported identities. A failed mandatory step keeps this work incomplete.

### HAG-OPS-005 — Persistence and recovery observations

After acknowledged commands, restart both containers without discarding the volume and verify the exact B and accepted operation receipts. Take a documented consistent backup, restore into a fresh disposable volume, and compare selected baseline, revision and receipt identities. A deliberately interrupted uncommitted transaction produces no accepted receipt. Measure restore duration and record the point-in-time cutoff; this POC promises reproducibility of the selected acknowledged set at that cutoff, not a production RPO/RTO or high-availability claim. Keep original volumes/evidence until comparison completes; no destructive recovery of the development repository.

Production power-loss durability, filesystem behavior, supported schema upgrades/rollback and recovery objectives need Phase 4 qualification against the chosen environment. The old image alone does not prove it can read a migrated schema. Do not mark these unperformed cases passed.

### HAG-OPS-006 — Authority, release and next phases

Git remains the SE Harness repository's artifact authority throughout Phases 0-2. Imported claims and sandbox drafts are test data. No bidirectional authoritative synchronization or automatic cutover exists. A later Phase 3 work package must choose the exact non-production pilot scope, support every required mutation, authenticate humans/agents and enforce their rights, resolve database-side Cypher enforcement, handle unfinished branches, explicitly select remote authority, and preserve export/historical resolution with no silent file-write fallback. New verification binds candidate C and baseline B without a circular identity; VREC/RLS integration requires its own approved contract changes.

Phase 4 qualifies the exact released harness/plugin/server set, publication and deployment observations, schema migration, persistence/recovery and supported rollout combinations. Release qualification, publication, plugin installation and server deployment are separate observable outcomes under the existing release/delivery procedure. A single later delivery grant may cover named external actions; this draft grants none. Assign no fabricated release number, registry destination, cloud account, RLS/VREC ID or deployment approval.

### HAG-OPS-007 — Component boundaries and first server contents

The first hosted candidate consists of three coordinated product components from one source commit: the existing `se-harness` distribution containing the remote client, the Verity Plane plugin archives containing matching remote guidance, and a separately packaged Python service under `server/`. They form one qualified combination; matching version numbers alone do not establish compatibility.

| Component | Owns | Does not own |
| --- | --- | --- |
| Harness/client | Explicit endpoint/project/view selection, transport, request keys, structured results and existing local commands | Server authority, database credentials or a second lifecycle policy |
| Verity Plane plugin | Operator/agent guidance, selection of the correct client and released evaluator, existing local workflows | An embedded server, automatic repository cutover or inferred human approval |
| Hosted service | Authenticated sandbox commands, graph reads/MCP/Cypher, version guards, atomic receipts and the materialization adapter | A replacement evaluator, general shell/build execution or hosted human decisions in this POC |

The server candidate must contain its installable package, exact dependency lock, image recipe, Compose configuration, explicit schema initialization command, schema revision declaration, health/readiness routes, import support and the documented qualification/recovery commands. The server image includes the selected 0.22.0 evaluator in a separate isolated environment. The service itself may have dependencies; these do not become dependencies of the core checker distribution.

The development plugin uses the existing assembly mechanism and carries the unchanged released evaluator wheel. The remote client wheel is installed separately into a candidate test environment and identified explicitly in the plugin guidance. This avoids changing the assembler to carry two governing evaluators. The source package containing remote commands never governs this checkout or substitutes for server validation.

The first candidate's claim is a reproducible single-project sandbox read/author/check path and observed restart/restore behavior under VER-HAG-001. It makes no production, authenticated-human-decision, multi-tenant, database-read-only-enforcement, high-availability or public-delivery claim. All included drafts retain their lifecycle meaning.

### HAG-OPS-008 — Initial combination and operating scope

The first qualification target is the following closed combination. It is a target, not evidence that unbuilt components already work together. A change to a pinned input requires recording the replacement identity and rerunning the affected qualification; no floating-tag or semver-range substitution is permitted in an accepted result.

| Input | Initial target | Identity/qualification rule |
| --- | --- | --- |
| Source | One future clean candidate commit in `mmzen/se_harness` containing WO-HAG-001 implementation | All changed product components derive from that commit. The original reference import remains commit `82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1`. |
| Harness remote client | Candidate source currently declares `0.22.1` | Use a distinct unpublished candidate identity; record actual wheel version and SHA-256 before tests. No public version is allocated by this contract. |
| Plugin | A candidate version distinct from public `0.2.5` | Record the actual host package version, ZIP SHA-256 and assembly-inventory digest. Existing host qualification requirements are not waived. |
| Server | New candidate service distribution and image | Record actual package version, dependency-lock digest and image manifest digest. No server release exists yet. |
| Service runtime | CPython `3.13.16`, Debian Bookworm slim, `linux/amd64` | `python@sha256:88310c082760d93ac7c74d579e95e53a4ab6ea52dd8901abc61a103daf488ac4`; registry index observed as `sha256:5024f48ba9441d4b13a95d3945abc6365538e3a31109833367a1923523c6efed`. Verify the running interpreter during qualification. |
| Database | Memgraph `3.13.1`, transactional storage, `linux/amd64` | `memgraph/memgraph@sha256:4710bee1ab5b47599876e30f17ae1679d0bbb2262d84dc06641521fecb7c89ce`; registry index observed as `sha256:bd3fe13228f40881365486729c78110dde6e04f3c1f102c84720d31f38b693f8`. This target requires no Enterprise read-only-role claim. |
| Evaluator | Released `0.22.0` | Archive and payload SHA-256 are fixed in HAG-OPS-002. Record the same identities for root governance, service evaluation and the plugin's reused evaluator. |
| Protocols | Remote command/result v1; graph-read v1; revision/baseline v1 | Preserve the exact named schemes from SPEC-HAG-001/002. Reject unsupported combinations before mutation. |
| Database schema | Revision `1` | Explicit initialization on an empty sandbox store. Fail readiness on mismatch; do not auto-migrate. |

The development host observation on 2026-10-04 is Windows Docker Desktop `4.93.0 (240920)`, Docker Engine/client `29.8.1`, Compose `v5.5.1`, context `desktop-linux`, engine platform `linux/amd64`, WSL2 kernel `6.18.40.1-microsoft-standard-WSL2`. Docker is installed per-user at `C:/Users/hok/AppData/Local/Programs/DockerDesktop/`; use the discovered executable rather than assuming the current shell PATH has refreshed. The client, server and registry manifests were queried successfully. These observations establish engine availability, not hosted application qualification or support for other host combinations.

Use one operator and two test authors, one project, non-sensitive public reference data, one service process, one persistent database volume, a private database network and a loopback API listener. Initial HTTP port `8080` and internal Bolt port `7687` are configurable; no database port is published to the host by default. The bounds in HAG-API-007 apply. Database-side read-only enforcement remains RISK-HAG-001. The Phase 3 pilot must resolve it and supply authenticated human decision enforcement before authority cutover or untrusted-network exposure.

### HAG-OPS-009 — Coordinated identity and compatibility reporting

Produce a supporting `se-harness-hosted-combination/v1` JSON manifest after the candidate artifacts exist. It is technical evidence, not a new approval or release record. Its identity-bearing contents are: source repository/full candidate commit; actual client wheel identity; plugin package and assembly-inventory identities per qualified host; service package/version/image/dependency-lock identities; reused evaluator archive/payload identities; pinned runtime and Memgraph platform manifest digests; schema and protocol schemes; and a digest of non-secret deployment configuration. Represent secrets by required configuration key names, never values or reusable credentials.

Calculate `combination_id` as SHA-256 over the UTF-8 scheme `se-harness-hosted-combination/v1`, one LF, and the canonical manifest payload using SPEC-HAG-001's JSON rules. Keep `combination_id` itself, observation timestamps, mutable delivery results and later VREC/RLS identifiers outside that payload. The candidate commit does not contain a manifest that includes its own commit identity: create the manifest as subsequent retained evidence. A later review/evidence commit may carry it without changing the code candidate it identifies.

The initial compatibility policy admits only the actually qualified component tuple. Equal API versions do not imply support for arbitrary clients, plugins, evaluator payloads, database versions or schema revisions. Server readiness reports the selected tuple and schema; the packaged client reports its actual build identity. The qualification report distinguishes selected targets, built identities and tested identities. Missing digests or unperformed required tests leave qualification incomplete; placeholders must never be treated as a completed release manifest.

The existing core release recipe remains unchanged: digest-pinned Linux/amd64 producer, CPython `3.11.9`, locked build tooling and two-build replay for promotable wheel/sdist outputs. The service runtime pin above is separate from that release-build producer. Read and follow the existing release sequence before a later build. This Phase 0 contract creates no build, tag, package or release record.

### HAG-OPS-010 — Publication, installation and deployment evidence

Qualification, release acceptance, publication, installation and deployment are separately observed outcomes. Keep existing REL/VREC/RLS authority and the repository's delivery procedure. Extend the later release contract to name the server combination and its required evidence; do not claim that a Python-only distribution binding already authenticates a server image.

| Outcome | Required later evidence |
| --- | --- |
| Qualified candidate | Actual component tuple, complete VER-HAG-001 observations, clean candidate identity and existing verification record procedure |
| Release accepted | The actual human release decision and existing release record, with the hosted combination/evidence selected by the applicable release contract |
| Client published | Public package version/location and independently downloaded matching archive digest |
| Plugin published | Host package/inventory identities, marketplace commit and observed public route under the existing marketplace procedure |
| Server image published | Authorized registry destination and immutable platform manifest digest; independent registry readback matching the qualified image |
| Plugin installed | Host identity/version, installed package/inventory digest, actual fresh/update outcome and evaluator/client selection readback |
| Server deployed | Environment identifier, combination ID, exact running image/database identities, non-secret configuration digest, schema, readiness and functional checks |
| Recovery/rollback observed | Backup cutoff, restore result and compatible image/schema pair. Selecting an old image alone is not proof that it can read a migrated database. |

For each applicable surface retain the actual outcome, attempt identity/time and evidence reference using the existing delivery report conventions. A missing observation keeps that surface pending or unobserved. A release decision, registry push or running process alone must not mark the other surfaces complete. Preserve the existing documentation, demonstration and marker obligations when a later public release selects them. No registry, cloud account, public version or deployment destination is authorized here.

### HAG-OPS-011 — Minimum tooling changes and phase handoff

The inspected `repository_tools/release_distribution.py` fixes `kind = python-wheel-sdist` and uses closed schema-2 fields. The current build recipe likewise produces only wheel/sdist/checksums. The existing plugin assembler already maps the selected guidance and host metadata. Therefore the sandbox work needs only a service-local build/qualification entry point and supporting combination manifest, a separately installed remote client, candidate plugin packaging through the existing assembler, and the scoped evidence/guide updates. Do not insert arbitrary server fields into the existing schema-2 bundle or change the current publisher in this work order.

For a future public coordinated release, the minimum additional work is a versioned, validated binding from the existing release contract/evidence to the server combination, an image build/qualification step in the existing coordinated path, and image publication/deployment observations in the existing delivery flow. The exact schema extension and affected paths must be reviewed through later bounded release work. Reuse the existing release record and publisher controls; do not create independent component release pipelines or a second release authority system.

Phase 0 is complete as contract preparation when the boundaries, closed initial target, combination identity, operating scope, release claims, delivery evidence and minimum later tooling changes above are recorded and structurally validated. This does not assert that Phase 2 qualification has occurred or approve a changed definition. WO-HAG-001 remains open for its full outcome. Definition lifecycle decisions remain explicit; work-order approval does not change their states automatically.

Phase 1 next fixes the exact project-ID allocation, source-manifest and staging contract, command-specific required fields/view selectors, context initialization/freeze behavior, physical properties/constraints and serialization byte vectors discussed in the examples. Those examples are not an implemented API. Phase 2 then implements the six engineering milestones described in the work discussion and completes every VER-HAG-001 scenario. Phase 0 performs no product implementation, public publication or service deployment.


## Coverage and references

REQ-HAG-007: HAG-OPS-002/006. REQ-HAG-008: HAG-OPS-001 through HAG-OPS-011. Memgraph durability uses snapshots and WAL: https://memgraph.com/docs/fundamentals/data-durability. Qualify the chosen configuration instead of assuming defaults meet a recovery objective.

Phase 0 primary sources: Memgraph release notes at https://memgraph.com/docs/release-notes and the official Python image at https://hub.docker.com/_/python. Registry manifests and the local Docker commands are retained under `evidence/WO-HAG-001/phase0-environment.json`.
