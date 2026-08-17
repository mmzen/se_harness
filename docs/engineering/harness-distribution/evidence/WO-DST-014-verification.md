# Verification evidence for WO-DST-014

## Authority and scope

The repository owner approved the DST-014/015 packet and authorized implementation on 2026-08-17. This evidence records implementation checks only. It does not create or approve a candidate commit, VREC, release, publication, deployment, push, pull request, or change to open PR 63 or the isolated `VREC-DST-011` stash.

## Implemented result

- One validator-owned in-memory projection is partitioned into bundle schema `harness-dashboard-bundle-v2`: bounded `index.html`, manifest, summary, compact topology, readiness, 432 content-addressed artifact details, and shared digest-named evidence text.
- The bootstrap binds the fixed manifest path, UTF-8 byte count, SHA-256, bundle schema, and observed revision without embedding repository artifacts or Markdown.
- Every loadable resource has a controlled role/schema/path, byte count, SHA-256, and digest filename. Artifact IDs are data, never path selectors.
- The writer creates a sibling tree, independently reparses the manifest/bootstrap/resources with duplicate-key rejection, recomputes the recursive set, schemas, identities, bytes, and hashes, and promotes only the complete tree.
- The Pages packager recursively reads regular files, rejects symlinks and undeclared/missing resources, independently validates supported roles/schemas, exact entry points, resource identities, hashes, governance revision, Git object format, bootstrap, generation summary, and publication provenance, then copies only declared bytes.
- `capture-verification` now records the SHA-256 of `dashboard-manifest.json`; that deterministic manifest recursively binds the candidate's artifact, relation, readiness, provenance, and retained-content resources after removal of v1 `dashboard-data.json`.
- Canonical and active generator/template copies are byte-identical and schema-2 lock reconciliation passes through `harnessctl upgrade . --apply` followed by an unchanged plan.

## Automated and security checks

| Check | Result |
| --- | --- |
| Focused dashboard/publication/CLI/provenance suites | PASS — 91 tests, 2 expected skips |
| Complete checkout-local suite | PASS — 228 tests, 3 expected Windows skips |
| Formal graph validation | PASS — 432 artifacts, 0 errors, 42 pre-existing maintenance warnings |
| `harnessctl doctor .` | PASS — active/canonical/lock integrity |
| Real repository generation | PASS — 432 artifacts, 1,559 relations, no validator errors |
| Current repository hard budgets | PASS — shell below 153,600 bytes, summary below 262,144 bytes, topology below 524,288 bytes |
| Pages tamper and exact-set fixtures | PASS — added and changed resources fail closed |
| Nested transaction and unsafe path fixtures | PASS — prior output preserved |
| Non-Git consumer dashboard | PASS — explicit `unavailable` revision, valid v2 bundle |

The first unrestricted complete-suite run used globally installed 0.4.0 metadata outside the checkout and produced only `RID018` in the candidate-source identity test. Refreshing the existing repository `.venv` with the documented editable install made distribution metadata checkout-local; the unchanged suite then passed 228/228 with three expected skips. No source correction was made for that environmental boundary.

## Documentation and disclosure

README, installation, command-reference, and repository-specific Pages notes now state that Explorer is a progressive static directory served over HTTP, direct `file://` use is unsupported, publication exposes every manifest-declared body, and no application server or new runtime dependency is introduced.

## Residual risk and actions not taken

The fixed manifest URL is mutable at a static host; the shell therefore requests it with revalidation and fails visibly on a stale hash rather than combining revisions. Content-addressed resources use ordinary browser caching. SHA-256 proves consistency relative to the trusted shell, not authenticity if an attacker replaces the whole site. Large future topology remains observational beyond the current acceptance target and requires separate authority to shard.

No commit, VREC, PR, push, merge, release, package publication, public demonstrator publication, deployment, service worker, API, database, secret scanner, telemetry, or new origin was created.
