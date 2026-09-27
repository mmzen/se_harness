# Release preparation review

The proposed release is **SE Harness 0.19.0**. The companion plugin inputs
would become **Verity Plane 0.2.0** for Codex and Claude Code.

Both formal artifacts below remain `draft`. Only this new proposal domain has
been added to the repository. No product file has changed and no build has run.

| Decision input | Purpose | SHA-256 |
| --- | --- | --- |
| [REL-SEH-030](release/REL-SEH-030.md) | Release scope and evidence expectations | `934eb56d4683ed37c1a264d5916cd07345cf6e22726eacb86784339e2d8eff3b` |
| [WO-RLS-025](work-orders/WO-RLS-025.md) | Bounded preparation and delivery authority | `625632d99db3733f1a4ac593cacf82168836acff58336f7215718fc7fd23df96` |

## Proposed work

- Include the 13 completed work orders listed in [coverage.md](coverage.md),
  plus WO-RLS-025 for final preparation.
- Add the existing injection script and both existing host hook files to the
  production assembly plan. Set the two plugin versions to 0.2.0.
- Test the final integration and build matching wheel/sdist bytes with the
  existing pinned Linux recipe. Prepare one final aggregate VREC.
- After human verification, prepare and bind the ready RLS, then replay it.
- Permit ordinary pushes of `work/release-0-19-0`, a draft PR to `main`, and
  the two existing read-only release rehearsal workflows in `mmzen/se_harness`.

## Review findings

The current production plan lacks the new delivery assets, so a checker-only
release would not itself update the published plugin. The draft covers these
release inputs and preserves the existing sequence: actual distributable plugin
archives consume the independently obtained public checker wheel after release.
It makes no claim that these archives have already been accepted or published.

The proposal reuses accepted distribution and instruction contracts and the
existing tools. It introduces no new release pipeline or verification contract.
Historical native demonstrations retain their Windows and manual-compaction
limits. Owner exceptions and accepted-definition revisions remain deferred.
The final candidate must have current integration evidence; earlier VRECs
cannot establish final-candidate acceptance by themselves.

## Checks performed

- Released 0.18.0 graph validation: pass, zero errors. The 50 existing
  maintenance-location warnings are unrelated to this proposal.
- Released 0.18.0 installation integrity (`doctor`): pass.
- Selected WO inspection: no scoped or repository blockers.
- Combined approval preview: pass; no transition applied.
- All relative Markdown file links in the proposal resolve.
- IDs checked across available Git refs before released-command creation.

Full local command results are retained outside the repository in
`work/evolution-evidence/r019-*.stdout` and their invocation files.
Exact review inputs are retained in `work/r019-review-inputs.json`.

## Requested decision

Approve **REL-SEH-030** and **WO-RLS-025** as drafted, including the proposed
plugin 0.2.0 version and bounded push/PR/read-only rehearsal envelope.
This would authorize preparation. Verification acceptance, release, merge,
publication, latest promotion and repository adoption remain separate decisions.

The installed repository rule in AGENTS.md requires an approved release work
order before a promotable build. DECISION_RIGHTS.md reserves WO approval to
the engineering owner and release-contract approval to its accountable owner.
The Verity Plane change skill's artifact-authoring reference requires an actual
accountable decision covering the reviewed inputs before applying approval.
