# Linux rehearsal failure at 26f32349

Run 34640805937, job 103400106532, selected head
`26f323493b0339717824a7985c5c1aaff403431b`. The first replay reached its cleanup
after predecessor/successor version checks, doctor calls, upgrade plan/apply and
successor validation. Its timing log marks those subprocess stages finished;
this does not establish a passing replay verdict.

`repository_tools/upgrade_rehearsal.py:138` called TemporaryDirectory cleanup.
Python 3.11.16's shutil.rmtree raised `OSError: [Errno 39] Directory not empty:
'repository'`. The replay and job failed; the second replay did not run. The
available log does not identify what remained or prove a particular race cause.
No Claude adapter was invoked in this job.

The failing helper and workflow lie outside WO-PLG-006's execution scope. No
shared cleanup, workflow or managed-control change is made here. Investigation
of the leftover tree/processes or a separately authorized rehearsal correction
is required; this failure cannot be waived by adapter test results.

Captures used `gh api repos/mmzen/se_harness/actions/jobs/103400106532` and
the same URL plus `/logs --allow-escape-sequences`. The first log request was
rejected by gh's terminal-escape output check; the second captured it locally.
`job-log-capture.json` preserves the original captured text and SHA-256; `job.log`
is a readable projection stripping terminal escapes/trailing whitespace. No raw
HTTP byte identity is claimed. These were read-only GitHub API requests.
