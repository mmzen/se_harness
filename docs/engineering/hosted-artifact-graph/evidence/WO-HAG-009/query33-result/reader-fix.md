# Reader correction after the Claude run

The completed candidate-33 run exported snapshots into directories named
`export-earlier.json` and `export-later.json`. These are valid export directory
names. The observation and independent replay scanners selected them with
`rglob('*.json')` and attempted to read them as files. The observation command
failed; it did not prove that the exports were corrupt.

Both readers now skip ordinary directories while still traversing their contents.
Existing file checks and the replay reader's symlink refusal remain unchanged.
The regression test exercises the real observation entry with a JSON-named export
directory containing both a manifest and a failed command record. It requires
the failure record to remain visible. No service, client, instructions, schema,
permissions, dependencies, criterion or lifecycle policy changes.

Validation: 41 focused tests; full source suite 1,337 tests, 24 reported skips;
distribution and CLI smoke; released validation 1,991 artifacts, zero errors,
63 warnings; scope and review preflight passed. The actual completed transcript
produces the same summary as the explicit offline recovery. The corrected replay
reader independently checks all ten accepted operations and all four export
copies (two distinct baselines), including exact bytes and candidate objects.

Failures are preserved: the initial focused command could not use the sandbox
temporary directory, then passed with normal host access. A repeated replay with
an unnecessarily long observer directory hit Windows Git's filename limit, then
passed in a shorter new directory without host-setting changes. The original
summary failure and all native errors remain retained.

This correction was made after the native session and does not rewrite its
inputs or verdict. Candidate-33 native evidence is still bound to
`4ce5bfb56d5fc594380deec56c20f1696961a621`. There was no further native model run
for this mechanical reader correction. Full qualification remains incomplete
because of the independently assessed procedure and reporting findings.
