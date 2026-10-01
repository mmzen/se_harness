# Validator correction progress

Human mmzen approved WO-IAR-035 and required commit-bound verification in
VREC-IAR-020. The released 0.20.0 evaluator applied approval and start.
The work order remains in progress; no completion or verification is claimed.

## Change and review

Initialize authoring advisories before checking whether the artifact directory
exists. Accept an absent default directory only after the exact external-resource
selection resolves. Preserve the missing-root error for legacy installations and
alternate roots. Invalid selections return a diagnostic. Existing artifacts still
receive the normal validation passes. The validator creates no directory.

The caller used by the dashboard explicitly passes the default directory. It now
receives the same empty-install behavior as a direct validation call. Retain the
existing E001 diagnostic instance and replace its message for a selection error;
this preserves the generated diagnostic index without introducing a new code.

## Observed checks

The latest focused run executed 36 tests and passed with one Windows symlink
skip. It includes resource validation, diagnostic-index compatibility and the
minimal CLI/dashboard case. Earlier failed runs are retained in validation.json.
The earlier scope invocation accidentally supplied a directory as a changed file;
the concrete file-path invocation passed before source editing.

## Remaining work

The integrated suite still needs the five test-file adaptations in proposed
WO-IAR-036. Final package/native checks, complete Git-derived handoff and exact
commit-bound VREC-IAR-020 preparation remain outstanding. Approval of this work
order does not accept a verification record or authorize publication.
