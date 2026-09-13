# Plugin simplification implementation

Base: d01eb765d80234bc55803cc00039483969f5f84d, the merged approved packet.
Final hosted source, package, Windows/Linux, integration, required validation and publication checks pass for 9fbec8b6741c757d57f45dad02a079c2b307b186.

Implemented: disposable skill replacement, provider-only schema 4, ordinary retries,
repairable setup, explicit checks, no automatic hooks or frozen host profiles,
development assembly, and a smaller installed migration acceptance on each OS.
The 50-scenario coverage map identifies all accepted removals and retained protections.

## Local observations

- Full source suite: 1,203 tests, one failure caused by CRLF counting 6,024 owner-region
  bytes against the existing 6,000-byte bound. Converting only working-copy line endings
  to Git's LF representation made all ten OwnerInstructionRegionTests pass.
  AGENTS.md has no committed content change. Final hosted source CI passes.
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

Hosted acceptance passes. The released evaluator records delegated completion separately; later commit-bound verification remains an assurance-owner decision.

## CI comparison

The earlier passing packet run 34745652601 used 902 seconds for the Windows
upgrade job and 283 seconds for Linux. Implementation run 34749784336 used
124 and 79 seconds respectively. Its installed migration took 3 seconds on
Windows and less than the one-second timestamp resolution on Linux.
Setup/development checks took 25 and 13 seconds. These are observed hosted runs,
not a controlled benchmark. The final instruction-only correction is covered by
run 34750034482 and the retained final-head checks. That final run used 149 seconds
for Windows and 64 seconds for Linux.

The tested PR merge f2e2b7c has the same Git tree as candidate head 9fbec8b6.
package-qualification.json retains the actual merge commit and wheel SHA-256.
