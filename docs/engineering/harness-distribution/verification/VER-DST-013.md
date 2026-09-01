+++
id = "VER-DST-013"
type = "verification"
title = "Verify deterministic progressive bundle integrity"
status = "approved"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-17"
updated = "2026-09-01"

[relations]
verifies = ["REQ-DST-048", "REQ-DST-049", "REQ-DST-054", "REQ-DST-055"]
+++

# Verification Contract: Verify deterministic progressive bundle integrity

## Independence

Verification treats the generated directory, manifest, bootstrap, and Pages input as hostile external products. Tests parse bytes independently from generator helper objects, recompute recursive sets, sizes, and SHA-256, and exercise the public CLI and publication script. Browser observations confirm acquisition boundaries without using implementation-internal success flags.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-DST-048 | Generated-byte and browser-startup test | shell, bootstrap, summary, missing summary | shell and verified summary render without embedded artifact/evidence bodies; failure is explicit |
| REQ-DST-049 | Independent manifest/tree verifier and fault injection | repeat generation, hashes, exact set, unsafe paths, partial promotion | supported deterministic manifest binds every allowed resource and all corrupt/incomplete cases fail closed |
| REQ-DST-054 | Static-server and Pages packager tests | ordinary HTTP, Pages governance revision, undeclared/missing/tampered resources, `file://` | static bundle is portable; local generation does not publish; explicit publication validates exact bytes |
| REQ-DST-055 | Deterministic size-budget tests | current repository plus bounded fixtures | shell/summary hard caps, no deferred Markdown, existing content bounds, and repository topology target pass |

## Acceptance scenarios

- Generate the current repository twice into distinct empty destinations and compare every relative path and byte.
- Serve the output with the Python standard-library HTTP server and load summary before topology/detail/evidence.
- Replace, remove, add, rename, truncate, enlarge, or duplicate one resource and assert generator/publisher/browser rejection at the appropriate boundary.
- Force recursive directory creation, collision, write failure, verification failure, and promotion failure; prove the previous valid output remains byte-identical.
- Select an authorized governance snapshot for Pages and prove only its exact manifest tree is packaged; generation alone performs no network action.

## Property and invariant tests

- Manifest descriptors are unique, deterministically ordered, controlled relative paths, role/schema valid, and exact in size/digest.
- Content-addressed filenames equal their computed lowercase SHA-256 and identical evidence shares one file.
- The manifest excludes itself; bootstrap manifest binding has no hash cycle and matches actual bytes.
- Summary excludes topology, bodies, and evidence; topology/readiness exclude body Markdown; artifact details exclude evidence body duplication.
- Recursive actual set equals root allowlist plus manifest set; no prefix, Unicode, separator, case, symlink, junction, or traversal ambiguity escapes output.
- Same projection produces identical resource partition regardless of filesystem enumeration order or hash-map insertion order.

## Static and architecture checks

- Assert `ARCH-DST-010` addresses only significant progressive-bundle drivers, conforms to both specifications, records `adr_required`, and is decided by `ADR-DST-010` before approval.
- Assert validator-owned projection -> partitioner -> manifest -> publisher/browser dependency direction and no browser/repository feedback.
- Scan HTML and data files for the old complete embedded snapshot marker and deferred Markdown collections.
- Preserve canonical/active managed generator/template parity and schema-2 lock integrity through supported upgrade.

## Security and privacy checks

- Reject absolute/parent/backslash/encoded paths, repository-ID filenames, unexpected extensions, duplicate JSON keys, invalid UTF-8, oversized values, unsupported schemas/roles, and mismatched revision/object format.
- Race evidence reads and output promotion; reject changed files and incomplete raw copies.
- Prove the Pages packager does not glob or copy an undeclared file and cannot publish a partial tree.
- Confirm generation makes no network request and publication disclosure still covers every artifact/evidence body.
- Preserve the exact graph CDN URL as the sole existing exception and ensure no bundle content is sent to it.

## Performance and resilience checks

- Measure UTF-8 bytes before compression: `index.html <= 524288`, summary `<= 262144`, and current repository topology `<= 2097152`.
- Retain 262,144-byte per-document and 16,777,216-byte total-content behavior with deterministic whole-document omission.
- Record per-role counts/totals, largest resource, and full output size in generation summary without a score.
- Generate larger consumer topology to prove target excess is observational while hard shell/content violations fail before promotion.

## Manual assessments

Review generated tree readability, bootstrap failure wording, local HTTP instructions, snapshot-information disclosure, Pages provenance, and current-repository metrics. Confirm the output is still recognizably one portable static site and not an undocumented application service.

## Evidence retention

Retain exact commands/versions/exit codes; before/after byte breakdown; recursive path/hash manifests; deterministic digests; tamper/failure fixtures; transaction/rollback observations; publisher selected revision and output set; network trace; size budgets; managed/template/lock/package parity; static-server and `file://` behavior; changed paths; deviations; residual risks; and all publication actions not performed under `docs/engineering/harness-distribution/evidence/WO-DST-014-verification.md`.

## Residual uncertainty

SHA-256 detects accidental or partial substitution only relative to the trusted generated HTML/publication context; it does not authenticate an attacker who replaces the whole site. Static hosts and browsers differ in caching and compression. Explicit governance, exact-set packaging, preparse verification, deterministic outputs, and uncompressed structural budgets bound those uncertainties.

## Amendment record

**The `index.html` measurement follows the 524,288-byte budget, proposed 2026-09-01
under `WO-DST-023` (`SPEC-DST-013` amendment).** Every other measurement and check
in this contract is unchanged.
