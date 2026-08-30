# Agentic Execution Repository Host Activation Contract-Closure Proposal

> Historical record from 2026-08-24, at `284b842`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Prepared: 2026-08-24

Selected domain: `agentic-execution`

Local baseline: Phase 3 candidate
`b77dbdc86fc00c0bc053e2b19c203fc0dc1dee62`; the user reports that its pull
request is merged. The locally known `origin/main` does not yet contain that
commit. No fetch, pull, branch change, commit, or other Git mutation was
performed.

Formal artifacts prepared from this proposal: `REQ-AEX-009`, `SPEC-AEX-005`,
`ADR-AEX-005`, `VER-AEX-003`, and `WO-AEX-004` (all `draft`)

Lifecycle effect: none

Implementation effect: none

External effect: none

## Purpose

The Phase 3 MVP packages four canonical skills under `.agents/skills`. Codex
uses that repository discovery location, but the current source checkout has no
installed root skill copy and Claude Code expects `.claude/skills`. The three
writing skills also require explicit invocation while both hosts permit
implicit matching by default unless their native activation controls are used.

This proposal closes the small availability gap needed before cross-host MVP
testing. It does not begin the later review of `AGENTS.md`, `CLAUDE.md`, general
prompts, or skill-body quality. It also does not approve implementation or
change the Phase 3 artifacts retroactively.

## Identifier audit

The audit inspected all 55 refs currently available in the local repository,
including local branches, locally known remote-tracking refs, tags, and the
candidate ref. The following identifiers were absent from every inspected ref:

- `REQ-AEX-009`
- `SPEC-AEX-005`
- `ADR-AEX-005`
- `VER-AEX-003`
- `WO-AEX-004`

The audit did not contact the remote. The identifiers are assigned against the
complete locally available ref set, not against unfetched remote state.

## Current gap

| Concern | Current Phase 3 state | Required closure |
| --- | --- | --- |
| Codex discovery | Canonical template sources exist under `.agents/skills` | Retain direct discovery and install the cores at repository root through the standard installer |
| Codex writing activation | Portable contracts say explicit-only | Add native false implicit-invocation policy for the three writing skills |
| Claude discovery | No `.claude/skills` surface | Add one thin repository adapter per canonical skill |
| Claude writing activation | No provider surface | Set explicit user-only invocation on the three writing adapters |
| Canonical identity | One complete core per skill | Preserve one procedure and script set; adapters only map to it |
| Public availability | Published package remains 0.6.0 | Qualify and later release a new version before public installs receive the change |

## Recommended decisions

### D-AEX-HST-01 — define default availability as repository-scoped

Recommendation: a fresh or explicitly upgraded standard SE Harness repository
contains the supported skill surfaces. Do not install these harness-dependent
skills into user, system, organization, cloud-account, marketplace, or
unrelated-repository locations as part of this work.

### D-AEX-HST-02 — preserve one canonical `.agents` core

Recommendation: keep every complete procedure, contract, and helper under
`.agents/skills/<name>`. Codex discovers that core directly. A Claude adapter
contains only Claude metadata, the fixed same-name canonical path, and
fail-closed loading instructions.

Do not duplicate the skill body or scripts under `.claude`.

### D-AEX-HST-03 — use native activation controls

Recommendation: keep `harness-orient` eligible for implicit read-only use. Add
Codex false implicit-invocation metadata and Claude
`disable-model-invocation: true` only for the three writing skills. Retain the
portable explicit-activation precondition as a second fail-closed boundary.

### D-AEX-HST-04 — reject links as the portability mechanism

Recommendation: do not use symbolic links, junctions, hard links, or reparse
points even though individual hosts may follow them. Repository checkout,
Python wheel, and Windows behavior is not sufficiently portable, and the
existing canonical manifest contract rejects linked content.

### D-AEX-HST-05 — manage adapters through the existing installer

Recommendation: package canonical metadata and Claude adapter files in the
standard template. Let the existing recursive installer and managed lock own
them atomically. Customized or conflicting destinations block without partial
writes. Do not add installer code unless implementation proves the existing
generic behavior insufficient and the work order is revised first.

### D-AEX-HST-06 — verify actual hosts separately from static files

Recommendation: retain static package, lock, mapping, hostile-input, and upgrade
tests, then run fresh root and nested-directory sessions in exact recorded Codex
and Claude Code versions. Listing alone is insufficient: verify explicit
writing invocation, implicit writing non-activation, orientation matching, and
loading of the same canonical contract.

### D-AEX-HST-07 — preserve release boundaries

Recommendation: leave published 0.6.0 unchanged. Candidate acceptance may use
an explicitly non-promotable ephemeral package after implementation is
authorized. Public default availability requires separate qualification and a
later governed package release.

## Proposed implementation boundary

Draft `WO-AEX-004` permits only:

- three bounded Codex policy files and the corresponding writing-skill patch
  identity updates;
- four thin Claude adapter `SKILL.md` files;
- explicit source and wheel inventory;
- static, installation, hostile, upgrade, and actual-host tests;
- bounded documentation, domain indexing, and retained evidence.

It excludes installer code unless scope is revised, root materialization,
managed policy, instruction review, duplicated procedures, global or plugin
installation, provider tool permissions, subagents, autonomy-envelope effects,
Git mutation, publication, and every external action.

## Exit criteria

The change is complete only when commit-bound evidence shows:

- both supported hosts expose the same four repository skill names;
- the three writing skills are explicitly user-invoked in both hosts;
- orientation remains read-only and matchable;
- every Claude adapter loads exactly one same-named canonical `.agents` core;
- no second procedure, contract, or helper exists under `.claude`;
- `harness-orient` v1 identity remains exact;
- source, wheel, install, replay, and upgrade inventories are complete;
- customized or hostile destinations fail without partial writes;
- actual-host and command-path results preserve the same harness decisions and
  non-effects; and
- no global install, lifecycle transition, Git operation, release, credential,
  network, or external action occurred.

## Human decision point

The five formal artifacts are ready for accountable content review, not
approval. The recommended next response is:

```text
Begin accountable content review of draft REQ-AEX-009, SPEC-AEX-005,
ADR-AEX-005, VER-AEX-003, and WO-AEX-004. Keep every artifact draft; do not
apply transitions, start implementation, or perform Git, network, package,
host-runtime, or external actions.
```
