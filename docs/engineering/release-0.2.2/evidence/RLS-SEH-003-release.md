# Release Evidence for RLS-SEH-003

Date: 2026-08-12

## Decision and scope

After reviewing and validating `VREC-SEH-003`, the accountable release owner explicitly instructed `i approve the release`. This authorizes the `RLS-SEH-003` transition from `ready` to `released` for version 0.2.2 and exactly `WO-IAR-002`, `WO-IAR-003`, `WO-IAR-004`, `WO-IAR-005`, and `WO-RLS-004` under `REL-SEH-003`.

The release record and all eligible artifacts identify or derive from candidate commit `9ba0cec3710167ad4568931747ed5f4e48a63532`, the commit bound by verified aggregate record `VREC-SEH-003`. The later verification and release governance commits are not release payloads.

## Exact-candidate qualification

The candidate was exported with `git archive` and built twice from independent clean intermediate workspaces using Python 3.14.6, `build` 1.5.0, setuptools 84.0.0, and `SOURCE_DATE_EPOCH=1786537968`, the candidate commit timestamp.

| Artifact | Build A SHA-256 | Build B SHA-256 | Result |
| --- | --- | --- | --- |
| wheel | `d06ad21d91b6aeabefefbcac93fc87ab42e95b4ead27f87bade83cd9f901bb2d` | `d06ad21d91b6aeabefefbcac93fc87ab42e95b4ead27f87bade83cd9f901bb2d` | byte-identical |
| raw sdist | `b8b360c09c50192a08c8e21d87fffdf51be0b8fcd021dcc71598ae3ddedaf76f` | `a1dc525f70e2444c4350b1250ba0816233c28e95a34fc10ae8eaed0335a1d579` | expected producer-metadata variance; ineligible |
| normalized sdist | `e21458d6f8e9e9f1df35087390e040e05218ba3d1165ce2ffc9800a6a53521a8` | `e21458d6f8e9e9f1df35087390e040e05218ba3d1165ce2ffc9800a6a53521a8` | byte-identical |

The wheel contains 47 unique entries and 47 RECORD rows. Metadata reports version 0.2.2. The normalized sdist contains 77 unique sorted members, all regular files or directories, with safe paths and epoch `1786537968`. An offline rebuild from the normalized sdist reproduced wheel SHA-256 `d06ad21d...bb2d` exactly.

A new Python 3.11.9 environment installed the exact wheel offline with no dependencies. The installed CLI reported 0.2.2; initialization produced all 33 standard files; doctor and formal validation passed; and Explorer generation passed with zero diagnostics and snapshot `7883949d67c07d632308fcfa7b93b59cfed3c1c05063dcaf20033fcc4aaa9d00` for the empty smoke graph.

## Gate result

- `REL-SEH-003` is approved and gates the exact five-work-order set.
- Every gated work order is implemented with retained evidence.
- `VREC-SEH-003` is verified and binds the same candidate and exact work set.
- Candidate version is 0.2.2 and the planned immutable tag is `v0.2.2`.
- Exact-candidate eligible artifacts reproduce and pass archive, metadata, offline-reconstruction, and installation checks.

Result: PASS for the `RLS-SEH-003 -> released` governance transition.

## Authority boundary

This evidence records release approval. It does not create or push tag `v0.2.2`, publish a GitHub release, dispatch or approve the PyPI workflow, upload artifacts, deploy, push this branch, open a pull request, merge, force push, or rewrite history. Each external action requires separate explicit authorization and must use the exact hashes above without rebuilding or replacing assets.
