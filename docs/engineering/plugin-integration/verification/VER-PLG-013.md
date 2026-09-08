+++
id = "VER-PLG-013"
type = "verification"
title = "Fresh repair and explicit repository upgrade"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-022", "REQ-PLG-023"]
+++

# Verification Contract: Fresh repair and explicit repository upgrade

## Independence

The assurance owner selects expected outcomes from SPEC-PLG-013 and canonical readiness checks in SPEC-PLG-002. Expected version, payload and archive identities come from the independently verified bundled wheel. Preserve a fixed snapshot of the previous selection and repository before each case.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-022 | test, inspection | MNT01–MNT07, MNT11 | Only a fresh, verified replacement becomes active; failure preserves a usable previous selection. |
| REQ-PLG-023 | test, inspection | MNT08–MNT10 | Plugin maintenance preserves project authority; only an authorized existing upgrade changes repository version. |

## Acceptance scenarios

Use disposable persistent plugin data and repositories. MNT01 supplies the valid baseline; failed-repair cases retain its usable previous environment. Evidence paths below are relative to the retention directory.

| Case | Fixture | Action | Observable pass condition | Evidence |
| --- | --- | --- | --- | --- |
| MNT01 | Working old environment, provided Python, trusted bundled wheel; network disabled | Prepare replacement and request selection | Empty external environment installs offline; selection changes only after canonical version/payload/observed-archive checks pass | `mnt01.json` |
| MNT02 | Provided Python missing or unsupported | Start repair through host shell | Guidance before Python-dependent checks; no Python download, installation or silent substitute; previous selection unchanged | `mnt02.json` |
| MNT03 | Replacement install fails or is interrupted | Resume repair | Incomplete replacement unavailable; actual partial effects inspected; previous selection remains usable | `mnt03.json` |
| MNT04 | Replacement has wrong version or modified payload | Request selection | Expected identity remains fixed; replacement refused; previous selection unchanged | `mnt04.json` |
| MNT05 | Matching replacement payload; observed archive digest differs | Request selection | Archive mismatch refuses replacement; previous selection unchanged | `mnt05.json` |
| MNT06 | Matching version/payload; installed archive metadata absent | Request selection with expected wheel flag supplied | Plugin readiness refuses missing observation; previous selection unchanged | `mnt06.json` |
| MNT07 | Bundled wheel changed after trusted digest selection | Repair | Digest check prevents installation; previous selection unchanged | `mnt07.json` |
| MNT08 | Project lock, owner content and historical evidence fixed | Separately update, repair or remove plugin | Repository snapshots unchanged; no implicit project upgrade | `mnt08.json`, `mnt08-diff.txt` |
| MNT09 | Actual existing upgrade authority; clean and conflicting-owner-content variants | Run authorized upgrade preview and apply | Clean variant preserves owner content; conflict variant refuses without partial repository writes | `mnt09.json`, `mnt09-diff.txt` |
| MNT10 | New plugin evaluator differs from project lock; no upgrade authority | Request ordinary governed use | Incompatible use stops; lock unchanged; no inferred upgrade approval | `mnt10.json` |
| MNT11 | Repository shadow module, inherited PYTHONPATH and global harnessctl | Repair using provided Python | Absolute isolated interpreter, cleared PYTHONPATH and controlled PATH; no repository import or global substitute | `mnt11.json` |

## Property and invariant tests

MNT02–MNT07 compare selection identity before and after each failure. MNT08–MNT10 compare repository bytes, including lock and retained governance evidence.

## Static and architecture checks

MNT01 inspects `--no-index --no-deps` installation from the verified wheel. MNT05/MNT06 inspect observed archive metadata, not the expected wheel flag echoed by identity.

## Security and privacy checks

MNT11 retains selected invocation fields only. Credentials are absent from fixtures and evidence.

## Performance and resilience checks

Record replacement duration in MNT01 and interruption/retry behavior in MNT03. Failed preparation never activates an incomplete environment.

## Manual assessments

Run with released evaluator 0.16.0 and provided Python 3.11+ on Windows and Linux. Record unavailable combinations; fixture results alone establish no live host coverage.

## Evidence retention

Retain the named files, trusted identity inputs, commands, identity reports and snapshots under `evidence/WO-PLG-013/`.

## Residual uncertainty

These are future acceptance cases, not passing results. Existing generic evaluator identity and upgrade semantics remain unchanged; stricter archive observation applies to plugin-managed readiness.
