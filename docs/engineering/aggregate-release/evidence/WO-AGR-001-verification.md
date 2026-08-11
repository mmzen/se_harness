# Verification Evidence for WO-AGR-001

## Scope and authority

The accountable repository owner approved `WO-AGR-001` on 2026-08-11 with the instruction `ok, perform the change`. This evidence records implementation verification only. No commit, push, pull request, verification transition, release record, tag, publication, or deployment was authorized or performed.

## Implemented behavior

- `capture-verification` accepts repeatable work-order, verification-contract, and evidence options and emits deterministic aggregate arrays at one clean final candidate commit.
- Multi-work aggregate verification requires the complete union of declared verification contracts and evidence keyed to every selected work order; legacy single-work records may retain a non-empty declared subset.
- `prepare-release` accepts repeatable work-order and verification-record options, requires releasable work, exact verified-versus-released scope equality, release-contract gating, and one shared candidate identity.
- Formal validation rejects duplicates, missing or extra verification coverage, unkeyed aggregate evidence, inactive relations, missing or extra released work, ungated work, and commit or object-format disagreement.
- Harness Explorer artifact detail exposes verified or released work, included verification records, and governing contracts.
- Distribution source and canonical standard-template copies are identical, documented, packaged, and represented by updated self-install hashes.

## Requirement evidence

| Requirement | Evidence | Result |
|---|---|---|
| REQ-AGR-001 | Aggregate CLI integration with two work orders, distinct contracts, deterministic evidence arrays | PASS |
| REQ-AGR-002 | Aggregate release preparation from one aggregate VREC and from two VRECs | PASS |
| REQ-AGR-003 | Same-commit success and mixed-commit rejection; existing SHA-1/SHA-256 coverage retained | PASS |
| REQ-AGR-004 | Reordered inputs, duplicate rejection, missing-contract rejection, single-item regressions | PASS |
| REQ-AGR-005 | Validator cases for incomplete, extra, duplicate, inactive, ungated, and lifecycle scope | PASS |
| REQ-AGR-006 | Dashboard JSON lists complete aggregate work and verification sets; Explorer renders them | PASS |
| REQ-AGR-007 | End-to-end assertions preserve HEAD and tags and emit only ready records | PASS |
| REQ-AGR-008 | Full init/adopt/upgrade suite, source-template parity, wheel contents, fresh install and doctor | PASS |

## Commands and outcomes

### Artifact graph

```powershell
python scripts/validate_engineering_artifacts.py --root .
```

Result: PASS. 67 formal artifacts, 0 errors, 0 warnings.

### Automated test suite

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Result: PASS. 37 tests passed; 2 symlink tests were skipped because this Windows host does not provide the required symlink privilege. Aggregate success, failure, compatibility, multi-VREC, installer, upgrade, dashboard, and Git non-mutation cases passed.

### CLI and installed-harness checks

```powershell
python -m se_harness --help
python -m se_harness doctor .
```

Result: PASS. Aggregate options appear in both provenance command help pages. Doctor reports Python 3.14.6, required files, Claude import, managed hashes, and self-install integrity as passing.

### Dashboard

```powershell
python scripts/generate_harness_dashboard.py --root .
```

Result: PASS. 67 artifacts, 227 relations, 0 errors, 5 warnings. The warnings are retained historical missing-VREC observations for `WO-DOC-001`, `WO-DOC-002`, `WO-DST-001`, `WO-REV-002`, and `WO-REV-003`; none is introduced by `WO-AGR-001`. Checkout differences on existing verification records remain informational, as designed.

### Source and canonical-template parity

SHA-256 equality was confirmed for:

- artifact validators;
- Harness Explorer templates;
- `WORKFLOW.md`;
- `TRACEABILITY.md`;
- verification-record templates;
- release-record templates.

Result: PASS for all six pairs.

### Wheel build

Build dependencies used in the repository virtual environment were `build 1.5.0` and `setuptools 84.0.0`.

```powershell
.venv\Scripts\python.exe -m build C:\Users\mathi\RustroverProjects\se_harness `
  --wheel --no-isolation `
  --outdir C:\Users\mathi\Documents\Codex\2026-08-10\st\wheel-verification-agr
```

Result: PASS. Built `se_harness-0.2.0-py3-none-any.whl` containing the aggregate CLI implementation, canonical workflow and traceability, record templates, validator, dashboard generator, and Explorer template.

Wheel SHA-256:

```text
4577b1bf9630e02c9e9bf80ceb683c8a93543f3e00b81c06a154c22748c4ff66
```

### Fresh wheel installation

```powershell
python -m venv C:\Users\mathi\Documents\Codex\2026-08-10\st\wheel-smoke-agr
wheel-smoke-agr\Scripts\python.exe -m pip install --no-deps wheel-verification-agr\se_harness-0.2.0-py3-none-any.whl
wheel-smoke-agr\Scripts\harnessctl.exe init wheel-smoke-repo-agr --project-name "Aggregate Smoke"
wheel-smoke-agr\Scripts\harnessctl.exe doctor wheel-smoke-repo-agr
wheel-smoke-agr\Scripts\harnessctl.exe validate wheel-smoke-repo-agr
```

Result: PASS. Version `0.2.0` installed; initialization added the complete 30-file standard harness; doctor and validation passed; installed workflow and validator contained the aggregate-release rules.

### Diff hygiene

```powershell
git diff --check
```

Result: PASS with no whitespace errors. Git emitted only the repository's existing LF-to-CRLF checkout notices.

## Deviations and residual risks

- Direct execution under Python 3.11 was not assessable because that runtime is not installed on this host. Python 3.14.6 satisfies the declared Python 3.11-or-later constraint.
- Two existing symlink boundary tests were skipped by host privilege; no symlink behavior was changed.
- Selecting release-bearing work remains an accountable human decision. The harness validates explicit scope but does not infer it.
- `REL-AGR-001` and `OPS-AGR-001` remain draft. No actual product release has been qualified or authorized.
- A commit-bound `VREC-*` for this implementation can only be prepared after a separately authorized clean candidate commit containing this evidence.
