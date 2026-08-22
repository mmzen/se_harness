# WO-REB-012 build-toolchain evidence

## Hosted failure retained

Publication run `32596492345`, credential-free qualification job `97088259463`, passed exact predecessor authority resolution, C6 candidate verification, the complete Git-aware C6 test suite, and two mutually identical deterministic builds. It stopped while assembling the exact release bundle because the rebuilt manifest differed from released `RLS-SEH-012` in `checksums_content`, `checksums_sha256`, `sdist_sha256`, and `wheel_sha256`. GitHub Release, PyPI, Pages, maintenance-line, tag, root, governance-history, and external-policy mutation jobs did not run.

The workflow installed only `build==1.3.0` before invoking the no-isolation build. Under `--no-isolation`, the ambient setuptools and wheel versions are direct build inputs. The retained C6 evidence binds the original build to Windows Python 3.11.9, `build==1.3.0`, setuptools `84.0.0`, wheel `0.48.0`, and `SOURCE_DATE_EPOCH=1787392506`.

## Exact local reproduction

An exact Git archive of immutable C6 `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798` was extracted into a disposable directory. With Python 3.11.9 and the exact retained three-version toolchain, the existing commands were run unchanged:

```text
python -m build --wheel --sdist --no-isolation --outdir <raw> <exact-c6-export>
python <exact-c6-export>/scripts/normalize_sdist.py <raw-sdist> <final-sdist> --epoch 1787392506
```

The results exactly reproduce released `RLS-SEH-012`:

- `se_harness-0.6.0-py3-none-any.whl`: `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`;
- normalized `se_harness-0.6.0.tar.gz`: `9493aa40ffbaf021edd205d6c302d67d11975bc057f73ba09b91043a9a51bbe4`.

This proves the released bytes and record are internally consistent and isolates the hosted failure to omitted build-backend pins. The correction changes only the credential-free tool installation and its regression assertion; it does not change release inputs, artifacts, identities, or privilege boundaries.

## Corrective qualification

Pending exact implementation-candidate qualification and commit-bound verification.
