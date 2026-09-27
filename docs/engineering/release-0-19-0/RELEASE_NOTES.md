# SE Harness 0.19.0 — release preparation

This version introduces progressive discovery of harness instructions.
The release is being prepared; this document does not announce publication.

## Changes

- A compact ENGINEERING_HARNESS.md routes agents to the instructions needed
  for their current action. The detailed collection contains 25 supporting
  guides. Lifecycle decisions still come from the selected evaluator.
- Evaluator results distinguish agent instructions, governing artifacts and
  machine policy inputs. Agents receive exact procedure reading locations.
- Fresh installations leave AGENTS.md to the repository owner. Upgrade retires
  a recognized old harness fragment only after replacement-delivery checks.
  Unrelated owner bytes are preserved; ambiguous or customized inputs refuse
  the affected migration.
- Verity Plane 0.2.0 inputs include the shared root-delivery script and both
  host SessionStart configurations. These deliver current repository context
  at startup and after manual compaction on the demonstrated Windows hosts.
- CI upgrade rehearsals support plugin ownership and test guarded instruction
  retirement. The final integration also includes the intervening repository
  cleanup and onboarding work listed in coverage.md.

## Compatibility

The repository remains governed by released evaluator 0.18.0 while preparing
0.19.0. Publication does not itself upgrade a repository or install a plugin.
Repository-owner edits outside recognized managed fragments need an explicit
adoption plan; the installer does not infer permission to rewrite them.

Native delivery was demonstrated with Windows Codex CLI 0.155.0-alpha.16.4
and its native app server, and Claude Code 2.1.273. The accepted evidence covers
manual compaction. It does not establish desktop UI, automatic threshold
compaction, macOS or later host versions. Detailed limits remain in
VREC-IAR-011's evidence. Missing or incompatible delivery is reported as a gap.

Configurable definition/work-order exceptions and linked revisions of accepted
definitions remain future capabilities. Instructions state the supported
fallback; this version adds no command that implements those capabilities.

## Distribution sequence

First qualify, verify and release the exact checker candidate. After checker
publication, assemble the final plugin archives from that released record and
an independently obtained public wheel. Inspect and test those actual archives
before plugin publication. Live installation and repository adoption follow
their separately authorized procedures.
