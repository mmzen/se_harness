# WO-REB-013 retained build-platform evidence

## Hosted failure retained

Publication run `32597819730`, credential-free qualification job `97091491671`, passed exact authority resolution, C6 candidate verification, the Git-aware C6 tests, and two mutually identical builds after installing `build==1.3.0`, setuptools `84.0.0`, and wheel `0.48.0`. It stopped at exact bundle assembly with the same four distribution identity fields differing from released `RLS-SEH-012`. The log records Ubuntu with Python `3.11.16` at `/opt/hostedtoolcache/Python/3.11.16/x64`. No bundle transfer, GitHub Release, maintenance-line, PyPI, Pages, tag, root, history, distribution, or policy mutation ran.

The immutable C6 retained evidence identifies the original producer as Windows Python 3.11.9. A local exact Git export built with that runtime, the exact three-version package toolchain, and `SOURCE_DATE_EPOCH=1787392506` reproduced both released hashes byte-for-byte:

- wheel: `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`;
- normalized sdist: `9493aa40ffbaf021edd205d6c302d67d11975bc057f73ba09b91043a9a51bbe4`.

The correction therefore selects `windows-2022` and exact Python `3.11.9` only for the unprivileged qualification/build job. Resolver and all downstream privileged or reporting jobs retain their existing runners and dependencies.

## Corrective qualification

Corrective candidate `d4aa21471c4740ca8a1737176c42b7eb89d940f0` contains exactly four paths: the trusted workflow, its regression test, `WO-REB-013`, and this evidence. The stopped untracked `RLS-SEH-008` is absent. The workflow diff changes only the unprivileged qualification runner from Ubuntu to `windows-2022`, its setup label, and its Python selector from the shared 3.11 value to exact `3.11.9`; resolver and every privileged or reporting job remain unchanged.

A clean exact-commit clone produced these results:

- retained Windows Python 3.11.9 C6 reconstruction: exact released wheel and normalized-sdist hashes;
- focused release-workflow policy: 5 tests passed;
- complete release-orchestration module: 22 tests passed;
- complete isolated suite: 452 tests passed with seven declared platform skips in 209.357 seconds;
- complete current-semantics graph: 663 artifacts, zero errors, 50 maintenance warnings;
- exact released-distribution validation: passed with one distribution-bearing record;
- portable release surface, diff whitespace, and clean-checkout checks: passed.

At closeout C6 `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`, `v0.6.0`, released `RLS-SEH-012`, distribution bytes, rejected history, the schema-2 root evaluator, and external policy remain unchanged. No publication credential, GitHub Release, PyPI file, Pages deployment, maintenance-line mutation, tag movement, root mutation, or distribution replacement occurred. A later commit-bound VREC must be accepted before this correction is pushed and publication resumes.
