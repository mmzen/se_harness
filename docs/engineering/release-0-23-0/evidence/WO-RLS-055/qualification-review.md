# Historical rehearsal correction — qualification

Tested source: `c740d49e30da74bab27ad29bb59fef2e785a6eae`. WO-RLS-055's correction resolves R23-REHEARSAL-001.
The original historical README refusal and intermediate local failures remain
in the previous evidence. The correction does not change live publication rules.

The [actual manual rehearsal](https://github.com/mmzen/se_harness/actions/runs/38901644102) passed candidate qualification,
historical RLS-SEH-033 qualification, and complete-delivery/recovery rehearsal.
The retained raw artifacts contain exact source/package identities, commands,
hashes and results. The historical output remains qualification-only and no
release bundle was offered for publication. No public surface was changed.

The full Windows suite passed at the tested source after a retry outside the
filesystem sandbox. The initial run failed on sandbox temporary-directory access
denials; that failed result is retained and is not counted as a product pass.
Focused checks, ordinary
validation, distribution validation and CLI smoke passed. Actual counts, skips,
durations and complete output are retained in `qualification-checks.zip`.
Linux/installed-package and two-producer build results are in the real workflow
artifacts. The PR merge subject remains distinct from the manual head subject.

The implementation reuses one resolver and qualification sequence. Historical
resolution checks immutable record bytes, recorded plan/evidence and approved
documentation. Live publication retains current-main documentation checks.
Publication consumers reject the historical output. Regression tests cover
changed bindings and history, not only successful reuse of older documentation.

R23-NATIVE-010/011 remain open. Codex Windows desktop remains not run/unverified.
DEC-RLS-010/011 retain their release-only limits. No claim of repaired native
findings, desktop coverage, human verification, merge or release is made.

Next: complete the normal handoff, then qualify the final clean release candidate
and refresh its exact package/staging identities before aggregate verification.
Earlier native observations require explicit unchanged-input comparisons.
