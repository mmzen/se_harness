# Plugin simplification implementation

Base: d01eb765d80234bc55803cc00039483969f5f84d, the merged approved packet.
WO-PLG-021 remains in_progress while final hosted acceptance runs.

Implemented: disposable skill replacement, provider-only schema 4, ordinary retries,
repairable setup, explicit checks, no automatic hooks or frozen host profiles,
development assembly, and a smaller installed migration acceptance on each OS.
The 50-scenario coverage map identifies all accepted removals and retained protections.

## Local observations

- Full source suite: 1,203 tests, one failure caused by CRLF counting 6,024 owner-region
  bytes against the existing 6,000-byte bound. Converting only working-copy line endings
  to Git's LF representation made all ten OwnerInstructionRegionTests pass.
  AGENTS.md has no committed content change. Final source CI remains required.
- Migration/installer/integration/integrity subset: 89 tests pass, three declared skips.
- Real setup: create, reuse, repair missing installed package content, then report an
  actual failed doctor on changed managed content: pass.
- Existing publication assembly tests: all 16 pass. The initial Python 3.12 run exposed
  a reparse-point test stub without st_mode; checking its reparse attribute before
  is_symlink preserves the same destination refusal and fixes that case.
- All five skill entrypoints pass the skill validator.
- Codex 0.154.0-alpha.6.2 exposes the plugin's skills in native prompt discovery.
- Claude 2.1.266 discovers all five skills through --plugin-dir and reports zero hooks.
  Its initial local-marketplace path trial was refused; that route is not claimed.
- Released 0.17.0 doctor, graph, scope and review pass; all 14 release distribution
  records pass. Candidate doctor reports expected candidate/root template differences;
  it is not the governing evaluator. See local-checks.json.

The current native discovery probes use disposable profiles without model calls,
normal host configuration changes, or copied credentials. Actual setup/checker
behavior is tested separately. No live project migration or release is claimed.

Hosted candidate/package/Windows/Linux acceptance and later commit-bound verification
remain required. Completion is not inferred from this evidence file.
