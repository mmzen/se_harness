# WO-REB-014 Windows Git-Bash path evidence

## Hosted failure retained

Publication run `32598292643`, qualification job `97092604303`, resolved released authority and selected Windows Python 3.11.9 successfully. Candidate export then failed before validation or build because Git Bash passed native `D:\a\_temp/source-a` to tar, which reported `Cannot open: No such file or directory` and exited 2. No build, bundle transfer, GitHub Release, maintenance-line, PyPI, Pages, tag, root, history, distribution, or external-policy mutation ran.

The correction derives `temp_root="$(cygpath -u "$RUNNER_TEMP")"` independently in export, candidate verification, build, and bundle verification. All shell file operations use that POSIX root. The action-owned upload path remains `${{ runner.temp }}/release-bundle/`, preserving its native runner contract.

## Corrective qualification

Pending exact implementation-candidate qualification and commit-bound verification.
