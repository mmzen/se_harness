```toml
artifact = "WO-TCM-003"
checkpoint = "handoff"
formal_snapshot_sha256 = "a2a658a0318562eed042124736476c92f567f4dbb2e1d1f008c7549800a3750f"
rebound_at = "2026-08-31T10:13:27Z"
```

# WO-TCM-003 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`docs/notes/diagnostic-codes.md` exists, generated from the candidate
source: 256 diagnostic codes across 28 registered prefixes, each with the
message text it appears in, a Summary, and a how-to-read-a-code prefix
table. `repository_tools/diagnostic_code_index.py` scans string literals
through the parser (comments and identifiers never contribute), keeps the
curated diagnostic-prefix registry, and derives the run-time-composed
`WEX301`-`WEX304` and `WEX401`-`WEX404` record-preparation codes
from the same source facts. `tests/test_diagnostic_code_index.py` fails
the suite when the committed page drifts (`REQ-TCM-005`; `TCM-DCI-001`
to `TCM-DCI-006`).

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included. The evaluator environment was recreated during execution after
  it disappeared from the workstation; its identity is unchanged (0.11.0).
- Candidate: this checkout, branch `wo/tcm-003-code-index` off `main` at
  `1ba300979ca0bc44c82b7f77c7fe50c3187168cb`.

## Change

- `repository_tools/diagnostic_code_index.py` (new, standard-library
  only): the scanner, the registry, the composed-code derivation, the
  deterministic renderer, and `--write`/`--check` modes.
- `docs/notes/diagnostic-codes.md` (new, generated and committed).
- `tests/test_diagnostic_code_index.py` (new, 8 tests): no-drift,
  check-mode, prefix coverage, the 17-code known sample, identifier
  exclusion, page shape, links, and determinism.
- `docs/notes/README.md`: one operator-table row.
- `docs/notes/harnessctl-check.md`: one sentence pointing from its small
  refusal table to the full index.
- This domain's index paragraph and this packet.

## Verification readings (VER-TCM-002)

- New suite plus the progressive-documentation suite: 26 tests OK (the
  link test resolves the new row).
- Full Windows suite: 1171 tests, 1 error — the known
  `test_artifact_authoring` temp-directory baseline — 26 Windows-only
  skips; at baseline.
- Two regenerations byte-identical; `--check` reports a match on the
  committed page.
- Known codes indexed (`A001`, `I001`, `E012`, `W013`, `W-AUT-002`,
  `WEX210`, `WEX-ECP-030`, `WEX301`, `WEX404`, `MG001`, `RID018`,
  `EPS001`, `JNL001`, `PRE001`, `REN010`, `RR001`, `PV001`);
  `WO-ECP-010`, `SPEC-ECP-006`, `ECP-DLG-001` and `SHA256` absent.
- Released 0.11.0 evaluator: `doctor` 0 FAIL; `validate` 1207 artifacts,
  0 errors, 486 warnings (the pre-existing flood);
  `validate_release_distributions` PASS (8 records).
- The `repository_tools` import barrier holds: the module imports nothing
  from `se_harness`.
- The pull request's own lanes are the lane reading; recorded on the pull
  request when green.

## Material non-effects

No diagnostic code, message, or emitting module changed. No hash-locked
root file changed; the root `scripts/` copies are not scanned. No other
note changed.

## Hosted lanes

All thirteen lanes of pull request #302 pass at its head `1e8c1a2`. The
owner merged the pull request on 2026-08-31 as `4028e72`, the tip of
`main`; the push-event check runs on `main` for that commit all thirteen
completed with success, including the candidate suite running the pinning
tests over the committed index, the managed Engineering Harness
`validate` and both release-qualification rehearsal legs.
