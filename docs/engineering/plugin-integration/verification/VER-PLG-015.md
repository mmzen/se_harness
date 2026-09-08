+++
id = "VER-PLG-015"
type = "verification"
title = "Host qualification and measured workflow overhead"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-025", "REQ-PLG-026"]
+++

# Verification Contract: Host qualification and measured workflow overhead

## Independence

The assurance owner approves the profile before candidate observations. DEC-PLG-005 blocks this contract until that positive profile is selected; preview-only needs amended scope.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-025 | test, inspection | C01–C04, C07–C09 | Every selected live-host operation has reproducible observations; offline fixtures alone cannot confer host support. |
| REQ-PLG-026 | test, inspection | C03, C05–C08 | Raw timing/prompt samples are complete and meet the positively approved profile’s defined aggregate criteria. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-015/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

Independent run instrumentation records host launches, external effects and target hashes. Checkpoint-free evaluator projections confirm selected artifact states only, never plugin readiness.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Untrusted PR revision; no host credentials; captured protocol fixtures; independently hashed protected target outside disposable fixtures | Run the offline lane with independent process/effect recording, then inspect target and artifact states. | Authenticated-host launch and publication-effect counts are zero; protected target hashes and lifecycle readbacks are unchanged; declared fixture outputs are allowed; fixture-only report rows have no corresponding live-host events. | runner permissions; independent process/effect logs; before/after hashes; artifact readbacks; fixture report |
| C02 | Approved positive profile; trusted revision/run environment; authorized host authentication | Run every selected scenario from plugin-scenarios/README.md, including release preparation and controlled or refused publication. | Each operation retains host-visible events, actual target effects and outcome against its scenario contract; every matrix row has live evidence. | profile; host transcript; event/target snapshots |
| C03 | Same scenario repeated per profile, fixed recorded model/settings and workload | Run the selected repetitions in cold and warm conditions. | Each run records host/Python/plugin/evaluator versions, model/settings, cache state, repetition number and raw timestamps; absent controls are disclosed. | per-run identity/settings record; timestamps |
| C04 | One live operation missing, failed or interrupted | Build the coverage report. | The corresponding row remains missing/failed/interrupted; no complete-coverage or supported-combination result is emitted. | raw run; coverage matrix; report result |
| C05 | Transcript containing owner decisions, duplicate prompts, host permissions/trust and recovery questions | Independently classify and count every interaction. | Each interaction has one primary category and timestamp; totals reconcile with transcript entries and preserve the four separate counts. | annotated transcript; category counts |
| C06 | Timestamped startup, multiple checks and full operation | Calculate durations and compare with the approved profile. | Startup, each check and total-operation milliseconds are retained separately; selected aggregate calculations reproduce from raw samples. | raw/derived timing rows; aggregate calculation |
| C07 | Interrupted sample, missing timestamp, or preview-only DEC choice | Attempt qualification acceptance. | Missing data are not zero-filled; preview-only or incomplete criteria produce no accepted qualification result. | input samples; decision/profile; refusal report |
| C08 | Single warm CLI baseline; independently fixed approved profile; recorded live-run events; hashed governed target | Add the baseline to the report, then independently recompute coverage and limits. | Live-evidence count still matches actual host events and excludes the baseline; limits equal the fixed profile; profile/target hashes and artifact states stay unchanged; external-effect count is zero. | baseline provenance; raw host-event inventory; independent counts; profile/target hashes; artifact readbacks; effect log |
| C09 | Supported live host; guard before setup, after setup, and after interpreter removal | Start, resume and compact in each condition. | When the guard starts, missing runtime emits setup-required without invoking Python; present runtime runs fresh identity/context checks. Existence alone never establishes readiness. Absent startup is unconfirmed and tested under VER-PLG-005/006 C11. | host events; guard/argv trace; identity/context output |

## Property and invariant tests

C01/C08 compare independent effects, hashes and artifact readbacks. C04/C07 preserve missing observations; C05 counts transcript entries; C06 recomputes aggregates from raw timestamps.

## Static and architecture checks

Map cases to PLG-QLF-001–010. Review offline/live lane separation, selected revision, runner permissions and evidence paths before running authenticated hosts.

## Security and privacy checks

C01 has no host credentials. C02 uses an explicitly authorized trusted run environment; retained logs identify authentication method and scope without secret values.

## Performance and resilience checks

The profile fixes repetitions, workload, timing boundaries and aggregate budgets. It does not require identical stochastic prompt counts across runs.

## Manual assessments

Observe every accepted host/platform directly, recording host, model/settings, Python and exact released evaluator. Operator-run live evidence may supplement credential-free CI fixtures.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-015/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

No implemented plugin or passing run is claimed. Unselected platforms and fixture-only lanes remain unqualified; variable samples require the approved aggregate, not invented thresholds.
