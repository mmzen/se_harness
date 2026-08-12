# Publication evidence for WO-PUB-005

Date: 2026-08-12

## Authorized operation

The accountable repository owner instructed: `this becomes the commit candidate, you can commit, create the PR, and create the validation record`.

The operation was limited to retaining the approved documentation candidate, preparing and retaining one aggregate ready verification record, pushing the named branch normally, and opening one pull request. No assurance transition, merge, release, tag, build, PyPI publication, deployment, governor promotion, history rewrite, or force push was performed.

## Candidate identity

- Candidate commit: `755785bb5be296b6920bf68b7398260454cd200b`
- Candidate tree: `9dddf91ed5624ceeeae5b61e99b5f21286167238`
- Candidate subject: `docs: streamline harness onboarding`
- Worktree at capture: `clean`
- Implementation work orders: `WO-DOC-007`, `WO-DOC-008`
- Verification contracts: `VER-DST-006`, `VER-DST-007`
- Retained evidence:
  - `docs/engineering/harness-distribution/evidence/WO-DOC-007-verification.md`
  - `docs/engineering/harness-distribution/evidence/WO-DOC-008-verification.md`

## Verification record retention

- Record: `VREC-DST-005`
- Record path: `docs/engineering/harness-distribution/verification-records/VREC-DST-005.md`
- Record state: `ready`
- Bound commit: `755785bb5be296b6920bf68b7398260454cd200b`
- Artifact snapshot SHA-256: `da1d193a5d23b9af7315a47d4ec3dce4afa490445a6abce821d3dfa3d3a7fede`
- Record file SHA-256: `07fbb1a63b7b077dab4d6ef9193d58bfdcc46d418c987e7c54a7079cd5c5f598`
- Governance retention commit: `5a9e4b1d28fff5bf496d8a12ddba8df80857f919`

The record intentionally covers only the two release-bearing documentation work orders. `WO-PUB-005` is publication governance and is not part of the verification claim. The record was not transitioned to `verified`.

## Candidate checks

- Formal validation before capture: PASS, 264 artifacts, 0 errors, 38 classified historical warnings.
- Formal validation with the ready VREC present: PASS, 265 artifacts, 0 errors, the same 38 classified historical warnings.
- `doctor`: PASS, including managed-file integrity and the pinned self-hosting governor.
- Review preflight: PASS for `WO-DOC-007`, `WO-DOC-008`, and `WO-PUB-005`.
- Focused documentation suite: PASS, 27 tests.
- Complete suite: PASS, 140 tests with 3 skips.
- Root README constraint: 140 lines and 9 level-two sections.
- Staged diff check: PASS.
- Protected managed/runtime surfaces: unchanged.

## Publication identity

- Remote: `origin` (`https://github.com/mmzen/se_harness.git`)
- Branch: `docs/update-readme`
- Upstream: `origin/docs/update-readme`
- Push mode: normal, with upstream tracking; no force option used.
- Pull request: `https://github.com/mmzen/se_harness/pull/32`
- Pull request number: `32`
- Pull request state at evidence capture: `OPEN`
- Base/head: `main` <- `docs/update-readme`
- Pull request title: `docs: streamline harness onboarding`
- Standalone declaration: `Harness-Work-Order: WO-PUB-005`
- Declaration transport: normalized from PowerShell CRLF to LF after the strict repository selector rejected the otherwise identical visible field; the work-order ID and PR scope did not change.

The pull request was created after the candidate and ready-record governance commits were pushed. This evidence and the work order's `implemented` state are retained afterward in governance-only commits on the same open branch; they do not alter the candidate named by `VREC-DST-005`.

The first PR event carried CRLF line endings and failed `Select the pull-request work order` because the selector intentionally accepts a strict LF-delimited standalone field. The body was normalized through GitHub without changing its content. Because a body edit is not one of the workflow's default triggering pull-request events, this evidence correction was committed and pushed normally to create a fresh `synchronize` event against the corrected body. An unrelated released-governor attempt also received an external HTTP 503 while downloading the pinned wheel; a parallel PR run subsequently acquired the same checksum-pinned governor successfully.
