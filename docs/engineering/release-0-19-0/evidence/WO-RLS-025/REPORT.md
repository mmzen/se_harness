# Release preparation implementation

Selected work: WO-RLS-025. Contract: REL-SEH-030. Governance: isolated released
evaluator 0.18.0. The human approved the exact proposal in this task.

## Delivered changes

Both plugin manifests select 0.2.0. The production assembly plan includes the
existing injection helper and each host's event configuration. The packaged
READMEs state the demonstrated Windows/manual-compaction limits. Release notes,
explicit membership and the domain index are present. The existing builder,
runtime, tests, workflows and installed root files are unchanged.

## Implementation checks

The tested implementation head is f77e95be5060528e22289ee33370a75733bddc08.
Its CI merge ffbb15de71e2c0a1d597e2ccbd5517b71b75e29d has the same Git tree,
1e9f055e71a17211621f18becdcfb7067f4e88b3. ci-tree-equivalence.json records it.

- Windows source: 1,122 tests pass, 16 skips, Python 3.14.6, normal scale.
- Linux source: 1,122 tests pass, 2 skips, Python 3.11.16, full scale.
- Focused assembly, setup and delivery suite: 35 tests pass, 2 skips.
- Distribution validation, candidate help, governing integrity, graph and
  review preflight pass. Required scope and handoff precede completion.
- Candidate CI 36338508348 passes every source, package, Windows/Linux upgrade
  and integration-package job. Its exact inputs and artifact expiry are in
  candidate-initial-ci.json; downloaded raw files remain outside the checkout.
- Manual rehearsal 36338516496 passes both legs. Its candidate leg builds this
  implementation head twice with matching wheel and sdist hashes. The other
  leg replays prior released RLS-SEH-027; it is not a 0.19.0 release decision.
  build-initial.json retains the recipe and both matching build observations.

The completion/evidence commit will become the final candidate. Rebuild that
exact candidate and require its current CI before aggregate verification.
The initial manifest is not relabelled as a build of a later commit.

## Evidence reuse and boundaries

historical-evidence-review.json checks eight verified records and 622 bound
evidence files against their original Git blobs. All are unchanged. The union
for this release has 14 WOs and 11 VERs. The aggregate record must name that
complete selection. Historical claims retain their original candidate bounds;
they do not replace final integration evidence.

Production plan inspection confirms both host configurations and identical
shared assets. The source evaluator, templates, common plugin code and hook
files are unchanged from the native candidate accepted by VREC-IAR-011.
The two development archives match all shared mapped assets they carry.
The development builder omits LICENSE; the production plan includes its checked
source. Final production archives remain pending the public released wheel.
The initial archive inspection exposed this difference; no release-assembly
pass or new native session is inferred from a development archive.

## Review and recorded refusals

Three plan entries, two version fields and bounded host-documentation updates
serve the approved outcome directly. Existing tests cover normal assembly and
its failure boundaries. No new abstraction, workflow or redundant test was
added. Root AGENTS.md, CLAUDE.md, ENGINEERING_HARNESS.md, lock/configuration,
accepted definitions and historical evidence are unchanged.

The first PR check refused the missing handoff header. The released evidence
command created it, and the retry passed. No gate was waived. Full raw local
output remains in this task's work/r019-local and work/r019-full-suite folders;
the retained summaries state commands, results and interpreter identities.

## Remaining decisions

Prepare the aggregate VREC for the final exact candidate after its build and
CI pass. The human decides verification acceptance. A later ready RLS and its
bound replay precede the human release decision. Merge, publication, latest
promotion and adoption remain separate.
