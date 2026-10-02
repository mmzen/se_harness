# CI correction assessment — WO-HUP-027

This record covers the four-file correction to PR #520. It does not reassess or rewrite the original adoption decision in VREC-HUP-025.

## Implementation and review

The four implementation files match the approved proposal, with normalized contents checked before tests. The source commit is 1757cffcddd71d2cdc0114838dc8563241297c4e. `wo027-implementation-identity.json` retains byte hashes. Later governance and evidence commits do not change these files.

The workflow downloads the pinned public wheel, requires a single matching filename and SHA-256, and installs that local file with no index lookup or dependencies. This retains archive provenance without changing the resolver or repository lock. The filename from the lock is compared as data and is never executed or used to choose a filesystem path.

The existing rehearsal classifier recognizes schema 5 only with released-resources-v1 and no skill_ownership field. It rejects external-resource fields on older schemas, unknown layouts and layout switches. Version, payload, doctor, graph, replay and unchanged-checkout checks remain intact.

The changes reuse the existing installer, helper and test modules. No new framework, dependency, release version or product template is introduced. Review found no additional implementation change needed beyond the approved patch. This is an agent assessment; human verification is separate.

## Contract coverage

| Criterion | Correction evidence and status |
|---|---|
| A0210-01: selected release identity | Released 0.21.0 identity, doctor and root qualification pass. A fresh index installation reproduces the CI failure; digest-checked local-wheel installation passes the PR and root checks. |
| A0210-02: replacement delivery | Unchanged, inherited from verified VREC-HUP-025 and the original acceptance assessment. No new native host observation. |
| A0210-03: migration and preservation | This correction performs no migration, lock edit or retirement. Prior adoption evidence remains unchanged. Real rehearsal exports independently check source preservation. |
| A0210-04: usable repository | Full-scale source suite: 1,222 tests, 21 skips, exit 0. Includes CI-pipeline and upgrade-rehearsal tests. Distribution, CLI smoke, identity, doctor and validation pass. Additional committed rehearsal and predecessor results are recorded below. |
| A0210-05: exact candidate and integration | Combined four-work-order scope and handoff and exact-candidate capture are required. VREC-HUP-026 will bind the final candidate. Hosted Linux/Windows CI must pass before merge; no hosted success is claimed from local tests. |

## Retained failures and limits

The original validate job and both hosted rehearsal failures are retained in the diagnostic log index with raw paths and hashes. Diagnostic prototype tests and public-wheel probes are retained separately from implementation checks.

The first root-qualification probe failed RQ001 when Git observation could not run in that invocation; the local retry using the same file-installed evaluator passed. The first prototype rehearsal suite had three missing-reference errors due to its transient runner root; correcting only that runner produced 39 passing tests. An implementation identity invocation omitted required arguments and returned usage; the corrected invocation passes. These failures have not been discarded.

The 21 test skips and 58 pre-existing graph warnings do not waive required checks. Claude and Codex Windows desktop remain unverified. Neither this assessment nor a ready verification record authorizes merge, release or publication.

## Committed rehearsal and predecessor results

Both real rehearsals against source commit 1757cffcddd71d2cdc0114838dc8563241297c4e pass, with semantic SHA-256 `354078b8c689d92e80ef7e2f1428835c1bbffb9d70e07a175b1c77a38c25be01`. The released 0.21.0 predecessor and retained CI-built non-promotable 0.21.1 successor run in separate environments. The original checkout and HEAD are unchanged after both runs. The clean-commit predecessor assessment passes with no diagnostics.
