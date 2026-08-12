# Verification Evidence for WO-RLS-004

Date: 2026-08-12

## Result

The integrated `se-harness` 0.2.2 candidate qualification passed. Version metadata and the self-hosted managed installation agree on 0.2.2; independent CI is pinned to the immutable released 0.2.1 wheel; both supported test runtimes pass; eligible package artifacts reproduce; normalized archive safety and metadata checks pass; and a clean Python 3.11 installation passes installed-harness checks.

This evidence supports `WO-RLS-004` at `implemented`. It does not verify the candidate or authorize a release. The candidate must first be committed; `VREC-SEH-003` can then be captured as `ready` in a later governance change against that exact commit.

## Scope and provenance model

`REL-SEH-003` gates exactly:

- `WO-IAR-002` under `VER-IAR-002`;
- `WO-IAR-003` under `VER-IAR-003`;
- `WO-IAR-004` under `VER-IAR-004`;
- `WO-IAR-005` under `VER-IAR-005`;
- `WO-RLS-004` under `VER-DST-001`.

`VREC-IAR-002` remains `verified`, continues to identify implementation commit `ca2006059eac8d13de9190d3c7b07066f82c5f74`, and has no diff from the pre-qualification `HEAD`. The planned `VREC-SEH-003` is a new integrated record for the later 0.2.2 candidate, not a mutation or lifecycle supersession of that verified history.

## Version and immutable assurance baseline

- `pyproject.toml` and `se_harness.__version__`: `0.2.2`.
- Root `.engineering-harness.toml`, `ENGINEERING_HARNESS.md`, and schema-2 lock: `0.2.2` after the supported transactional upgrade.
- Public exact-version installation example: `se-harness==0.2.2`.
- Candidate CI fallback: `se-harness==0.2.2`.
- Independent assurance baseline: GitHub release `v0.2.1`, wheel `se_harness-0.2.1-py3-none-any.whl`, SHA-256 `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454`.

The baseline is independently available and immutable. Candidate-source checks remain separate and do not claim that unreleased 0.2.2 is an external baseline.

## Commands and results

### Start and review readiness

```powershell
python scripts/validate_engineering_artifacts.py --root .
python -m se_harness preflight . --work-order WO-RLS-004 --phase start --json
python -m se_harness preflight . --work-order WO-RLS-004 --phase review --json
```

Result: PASS. Both preflight phases returned `ready: true` with zero diagnostics and the complete governing manifest. Formal validation found 227 artifacts, zero errors, and 36 compatibility/layout warnings before the final evidence and lifecycle update.

The warning set is fully classified:

- 7 `W013` historical canonical-location advisories;
- 14 `W014` completed legacy architecture decision-assessment advisories;
- 15 `W015` completed legacy `constrains` relation advisories.

These findings are the explicit compatibility behavior authorized by `WO-IAR-004` and `WO-IAR-005`, plus older location guidance. They do not identify an invalid relation, missing active assessment, changed candidate, failed gate, or unverified release member.

### Supported transactional upgrade and integrity

```powershell
python -m se_harness upgrade . --apply
python -m se_harness upgrade . --apply
python -m se_harness doctor .
python -m se_harness --version
```

Result: PASS. The first apply updated only `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, `ENGINEERING_HARNESS.md`, and their lock state. The second apply reported all 33 distributed files unchanged. Doctor passed required-file, distribution-parity, seed, schema-2 lock, managed-integrity, and runtime checks. The CLI reported 0.2.2.

### Supported-runtime regression

```powershell
python -m unittest discover -s tests -p "test_*.py"
C:\Users\mathi\Documents\Codex\2026-08-10\st\v0.2.0-final-smoke-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Result: PASS on Python 3.14.6 and Python 3.11.9. Each runtime executed 111 tests with 3 documented Windows/platform-conditional skips.

The first run exposed one stale test constant that still asserted the prior 0.2.0 baseline hash. The fixture was updated to assert the approved 0.2.1 baseline identity, and both complete suites then passed. No runtime product failure occurred.

### Harness Explorer

```powershell
python scripts/generate_harness_dashboard.py --root .
python scripts/generate_harness_dashboard.py --root .
```

Result: PASS and deterministic. Both runs produced snapshot SHA-256 `f8f18b305ccb49eb574876ee703b7feca5701ddf525c06ac7063a3b86e27f6c5` with 227 artifacts, 750 relations, zero errors, and 37 warnings. The 36 validator advisories are described above; the additional derived, non-authoritative finding is the known `VREC-AGR-001` stale-ready observation. No Explorer output grants approval or changes lifecycle state.

### Independent package builds

Build runtime: Python 3.14.6, `build` 1.5.0, and setuptools 84.0.0. Preliminary qualification epoch: `1786536975`, the pre-candidate `HEAD` commit time.

```powershell
$env:SOURCE_DATE_EPOCH='1786536975'
python -m build --wheel --sdist --no-isolation --outdir target/qualification-0.2.2/raw-a .
python -m build --wheel --sdist --no-isolation --outdir target/qualification-0.2.2/raw-b .
python scripts/normalize_sdist.py <raw-a-sdist> <normalized-a-sdist> --epoch 1786536975
python scripts/normalize_sdist.py <raw-b-sdist> <normalized-b-sdist> --epoch 1786536975
```

| Artifact | Build A SHA-256 | Build B SHA-256 | Result |
| --- | --- | --- | --- |
| wheel | `c7bd054504186642473d2a61b3befccade4de15d33aa94345625e4849080014f` | `c7bd054504186642473d2a61b3befccade4de15d33aa94345625e4849080014f` | byte-identical |
| raw sdist | `f7f19257b576f76f8c19f79b0f09aacae091416adc37e223073c51c499dc80ce` | `146a2f3be0b72bb4ceaa4dd27aa91805477360a53ad6efbb5f529f4f1d1a6f93` | expected producer-metadata variance |
| normalized sdist | `5c2d40d0ae5771c739bda0c4e0c73e8e1a1589eb1a09269e8b387ac93a5eb1dd` | `5c2d40d0ae5771c739bda0c4e0c73e8e1a1589eb1a09269e8b387ac93a5eb1dd` | byte-identical |

The initial attempt to run both setuptools builds concurrently collided in their shared Windows `build/` workspace. Only generated qualification output was removed after resolving each target below the repository, and the two builds were rerun sequentially with the intermediate workspace cleared between them. This preserves independence and avoids masking a product defect.

Raw setuptools sdists remain nondeterministic intermediates and are ineligible for publication. The normalized source distribution is the eligible sdist.

### Archive, metadata, and offline reconstruction

The wheel contains 47 unique entries and 47 RECORD rows. All RECORD entries validate through the release regression suite, metadata reports version 0.2.2 and the correct console entry point, and no path is absolute or traversing.

The normalized sdist contains 77 unique sorted members. Every member is a regular file or directory, every path is safe, and every timestamp equals epoch `1786536975`. With `SOURCE_DATE_EPOCH=1786536975`, an offline `--no-index --no-deps --no-build-isolation --no-cache-dir` wheel reconstruction from the normalized sdist exactly reproduced wheel SHA-256 `c7bd0545...0014f`.

The first offline reconstruction intentionally exposed the control's importance: without propagating `SOURCE_DATE_EPOCH`, the wheel hash differed. Repeating it with the declared epoch reproduced exactly. Final candidate-derived builds must use the later candidate commit timestamp.

Setuptools emitted its existing deprecation notice for table-form `project.license`, with enforcement dated 2027-02-18. It does not affect current metadata validity or reproducibility; migration is a separately governable maintenance item.

### Fresh Python 3.11 installation

The qualified wheel was installed offline with `--no-index --no-deps` into a new Python 3.11.9 virtual environment. `python -m se_harness --version` returned 0.2.2. `init` installed all 33 standard files into a new repository; doctor passed all required, distribution, lock, managed-integrity, seed, and runtime checks; formal validation reported zero diagnostics; and Explorer generation passed with snapshot `c7709b3fe75c859b7e40f5e857ee34028b2f3d6994fa31c01c00f3a1e249696c` for the intentionally empty graph.

## Changed surface

- New `REL-SEH-003`, `WO-RLS-004`, release-0.2.2 index entry, and this evidence.
- Package/runtime version metadata and public exact-version guidance.
- Immutable independent-baseline constants and rendered workflow.
- Self-hosted configuration, managed router identity, and schema-2 lock updated through supported upgrade.
- Version/baseline-focused test expectations.

No IAR implementation artifact, historical VREC/RLS, release tag, publication workflow contract, package-index credential, or external repository state changed.

## Residual risks and next gate

- Qualification hashes above describe the pre-commit candidate content at a preliminary epoch. After the clean candidate commit exists, final release assets must be rebuilt from that exact tree with its commit timestamp and retained before any tag or publication.
- Completed legacy architecture and historical location advisories remain visible by design. They require accountable migration only when those artifacts are changed; automatic rewriting would violate the approved compatibility model.
- Three platform-conditional skips remain documented. No symlink behavior changed, and malicious/special archive handling remains covered by the regression suite.
- GitHub branch protection, release immutability, PyPI Trusted Publisher identity, protected-environment approval, and package-index immutability remain external controls.

The next authorized step is a clean candidate commit followed by `capture-verification` for `VREC-SEH-003` as `ready`. Quality-owner review is still required for `ready -> verified`. No tag, release, publication, or deployment is authorized by this evidence.
