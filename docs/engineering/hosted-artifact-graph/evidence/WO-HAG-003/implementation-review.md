# WO-HAG-003 implementation review

The correction separates the actual decision-maker from the existing owner
label. `--decision` retains the human. Optional `--authority-owner` names one
existing holder. Omitting it retains direct-owner matching.

Tested and packaged source: `99a8c53f6a2e253c20737d5985223ea0c25c79d9`.
Correction implementation baseline: `fcfb02b3a8ff041023e0d85d7bc2af0524559f8a` (approved inputs before code).
This comparison is limited to WO-HAG-003. PR #535 keeps its original target.
The whole hosted change retains its existing integration scope finding.

## Requirement assessment

All eight VER-HAG-003 cases pass. See [verification-results.json](verification-results.json)
for the requirement mapping, platform identities and limits. The raw commands,
stdout, stderr and failed attempts are retained in [commands.zip](commands.zip).
The two pinned Linux builds produce equal archives; [build-replay.json](build-replay.json)
contains their source, image, toolchain and payload identities. The same wheel
passed installed tests on Windows and Linux through the real installed guard.
The probe source is [installed_probe.py](installed_probe.py).

## Design and diff review

One optional input and one optional disposition field solve the stated defect.
The CLI, paired-risk dispatcher and direct API reach the existing workflow
planner, decision validator and atomic writer. Owner selection is unchanged.
The scalar shape check is shared by request validation and graph validation.
No new identity registry, configuration file, dependency or policy engine is
needed. Invalid requests write nothing. Later holder changes do not rewrite
past dispositions. A later direct-owner request cannot inherit an old binding.

The caller must establish authority and hold the exact human decision. The
CLI does not authenticate either supplied string. Help and both instruction
resources explain that limit. No implementation step changes the live
decision, accepted ownership, historical evidence or governor pin.

## Findings and resolution

The first help test assumed an unwrapped phrase. Normalizing display whitespace
fixed that assertion without changing its meaning. The first full suite found
three diagnostic-index failures after an extra error-emission site was added.
Reusing the existing disposition-field loop preserves the index structure and
the old messages; the optional field still receives its precise diagnostic.
The focused regression and final full suite pass. The index was not edited.

The final source suite reports 1,305 tests and 22 skips, exit 0. Those skips
remain unexecuted checks; the raw output identifies them. Distribution checks
pass for 22 records. Released validation reports 1,939 artifacts, zero errors
and 61 existing warnings. Warning counts are not a risk acceptance.

## Boundaries

This verifies a correction candidate, not the hosted service. Zero hosted
scenarios have run. DEC-HAG-001 remains open, and release/adoption must precede
its disposition with the new option. VREC-HAG-001 and its bound evidence remain
unchanged. The private archives use development version 0.22.1; no publication,
release decision or adoption is implied. Human verification is still pending.
