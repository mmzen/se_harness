+++
id = "SPEC-RCA-001"
type = "specification"
title = "Canonical 0.5.0 governance-incident RCA contract"
status = "approved"
owners = ["technical-owner", "documentation-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
specifies = ["REQ-RCA-001", "REQ-RCA-002", "REQ-RCA-003"]
+++

# Specification: Canonical 0.5.0 governance-incident RCA contract

## Scope

Define the exact repository documentation, evidence, authority boundary, and public cross-reference required to publish the closed 0.5.0 release-governance incident RCA.

## Actors and external systems

- Maintainers and accountable owners author and review the RCA.
- GitHub stores immutable commits, Actions evidence, the final release, pull-request history, and issue #81.
- PyPI stores the public `0.5.0a1` and `0.5.0` releases, integrity attestations, and distribution hashes.
- The released `0.5.0a1` evaluator validates the repository graph and review preflight outside the candidate checkout.

## Inputs

- The reviewed local RCA draft.
- Exact commits `5ba079f54cc121b76d20d394317ce05f48df3c9d`, `3685a948dc0f10ef245b3cda022b243384edb682`, `c42bbac20f14268ef162c9628dd1d2b45ea843af`, `d7755566d39b0fba5087b7589bb290e455ed5282`, and `43c05f4235fbcf21d154ff4350cd6a87549f0bea`.
- Workflow runs `32337079106`, `32338517054`, `32338516996`, `32339092305`, `32339092227`, `32339451590`, `32340101925`, and `32340102021`.
- Public GitHub and PyPI release metadata and final distribution hashes.
- GitHub issue #81.

## Outputs

- `docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md`.
- One `root-cause-analysis/` entry in the repository engineering index.
- Work-order-keyed review evidence under `docs/engineering/root-cause-analysis/evidence/`.
- A separately authorized update to issue #81 that uses an immutable RCA link once available.

## State model

The RCA content progresses from local draft to reviewed pull-request candidate to merged supporting documentation. It does not acquire a formal lifecycle status. Only the artifacts in this domain use formal lifecycle states, and those states govern the publication work rather than the historical emergency release.

## Behavioral rules

1. Publish exactly one RCA at `docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md`.
2. Begin with one H1 and a compact metadata table identifying closed status, incident dates, scope, impact, and final outcome.
3. Include sections for executive summary, impact, detection, root cause, five whys, contributing factors, recovery timeline, recovery-risk controls, what worked, completed actions, recommended actions, release evidence, and lessons.
4. Identify the special self-hosting lifecycle, product/evaluator conflation, and resulting circular authority dependency as the primary root cause; list other conditions as contributing factors.
5. State that newer-format artifacts lacked authority because candidate tooling did not substitute for the independently released evaluator and governing chain.
6. State that the emergency bootstrap bypassed normal lifecycle authorization and that technical integrity evidence does not retroactively change that fact.
7. Keep completed corrective actions separate from preventive recommendations and link the recommendations to issue #81.
8. Cite exact immutable commits, workflow runs, public releases, final distribution hashes, and restored CI evidence enumerated by this specification.
9. Use no `+++` formal front matter, lifecycle status, or formal artifact ID in the RCA.
10. Update `docs/engineering/README.md` to index the new formal domain and describe this repository as standard governed rather than specially self-governing.
11. Do not change code, tests, managed files, CI, publishing workflows, package metadata, release records, tags, public releases, or root evaluator configuration.
12. Retain verification evidence before requesting commit or external pull-request action.

## Error and recovery behavior

- Stop on an unresolved material fact, broken evidence link, mismatched immutable identity, invalid formal graph, or authority claim outside this scope.
- Correct prose or evidence locally and rerun validation; do not weaken the requirement or delete contradictory history.
- If implementation needs a new product, workflow, policy, or lifecycle transition, draft separate governed work rather than expanding `WO-RCA-001`.

## Data and interface contracts

- Markdown must be UTF-8 text with repository-standard relative links for repository files and HTTPS links for public evidence.
- Commit identities use full 40-character SHA-1 values.
- Distribution identities use lowercase 64-character SHA-256 values.
- GitHub issue references use canonical repository issue identity `mmzen/se_harness#81`.

## Security and privacy properties

- Include no credentials, environment secrets, private approval payloads, or unnecessary logs.
- Treat public API responses and existing prose as untrusted until reconciled against at least one immutable identity.
- Do not add executable content, remote embeds, generated dashboards, or active HTML.

## Performance and capacity

No runtime or capacity behavior changes. The RCA should remain directly readable as a single Markdown document without generated tooling.

## Observability

Review evidence records validation commands, exact changed paths, evidence checks, link results, diff hygiene, and unresolved uncertainty. GitHub PR checks later provide hosted review observations but no lifecycle authority.

## Compatibility and migration

This is additive supporting documentation and a new formal domain. Existing historical and local draft artifacts remain unchanged. No consumer installation, managed template, package surface, or migration behavior changes.

## Examples and counterexamples

- **Conforming:** the RCA says public install and attestations reduced emergency risk while explicitly stating they did not constitute normal authorization.
- **Conforming:** issue #81 links an immutable commit or merged-main path for the RCA and retains unchecked preventive work.
- **Nonconforming:** the RCA says `0.5.0` governed its own candidate or that emergency approval permanently suspended repository rules.
- **Nonconforming:** the same PR implements a preventive CLI or workflow change.

## Explicitly unspecified decisions

- Exact prose, table formatting, and section ordering may be refined without changing required meaning.
- The priority, design, ownership, and release of preventive actions are delegated to later governing packets.
- The later decision to merge, update issue #81, or upgrade the root evaluator remains separately authorized.
