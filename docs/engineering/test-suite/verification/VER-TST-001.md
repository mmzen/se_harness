+++
id = "VER-TST-001"
type = "verification"
title = "Independent evidence for the parallel suite"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
verifies = ["REQ-TST-001", "REQ-TST-002", "REQ-TST-003"]
+++

# Verification Contract: Independent evidence for the parallel suite

## Independence

The serial run on the same commit is the oracle; wall times are measured
on the workstation and read from the hosted `candidate-source` job.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-TST-001` | verdict comparison; timed runs | serial vs `--workers 4` and `8` on one commit; an injected failing test; a class that fails to import | identical pass/fail/error/skip sets; the injected failure and the import error reported; wall under half of serial at four workers |
| `REQ-TST-002` | test | marker absent and present | 1,000 size skipped via `subTest` without the marker, run with it |
| `REQ-TST-003` | test; timed comparison | helper called twice; tree compared with a direct `init` | `init` ran once; byte-identical trees including the lock |
| all | documentation inspection | `AGENTS.md` Test line, the two notes | updated in the same change |

## Acceptance scenarios

1. Serial and parallel on one commit: same verdict; wall times recorded.
2. Inject a failing test in a scratch copy: the runner exits 1 and prints
   the traceback.
3. Hosted: the `candidate-source` suite step's duration before and after.

## Pass criteria

Every scenario recorded; released-evaluator validation 0 errors.
