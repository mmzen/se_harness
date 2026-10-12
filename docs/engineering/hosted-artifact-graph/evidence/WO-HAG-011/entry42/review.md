# Bounded qualification correction 42

The full lifecycle trials completed independently, but Claude called the supplied
implementation commit unknown and Codex used a direct task-file reader. The
focused positive case was separately refused before launch at 67,945 bytes.
See the retained final40-result and final41-result assessments.

The correction changes five files in the existing test and instruction surface:

- Share release/root metadata in complete-input entries. Preserve each complete
  canonical section, source file, reference and identity; retain full JSON metadata.
- Remove repeated task framing while preserving its requested outcome, no-prior-
  trial rule, file/command/permission boundary and report branches.
- Give Codex its existing bounded task reader before it must read task.md. Use
  the same helper for recovery. Reject unsafe literal paths; add no shell authority.
- Return the supplied qualification_candidate in the existing identity result;
  preserve null when absent. Point the report guide to this exact field.

This uses existing helpers and policies, with no new abstraction, dependency,
service endpoint, source fixture, protocol or lifecycle rule. The 64 KiB cap is
unchanged. A mixed release or unsafe path is refused. Historical evidence remains
unaltered. The observer's false missing-read interpretation was separately corrected.

Focused driver, resource and plugin checks, the full source suite, distribution,
CLI smoke, released validation and scope/preflight checks passed. See checks.zip.
Review then restored the explicit no-prior-trials sentence in the shorter task;
the final committed candidate will receive another source check and exact package
build before native qualification. No native pass is claimed for this correction.

Required next checks: exact candidate build/component comparison; unassisted
affected NQ runs; focused EFF-04A2 and EFF-04B cases on the same final candidate.
No human verification, release, merge or permission change is inferred.
