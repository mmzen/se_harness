+++
id = "INT-LRE-001"
type = "intent"
title = "Let a repository adopt evaluator-evidence enforcement without falsifying or freezing its history"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:44:00Z"
decided_by = "repository-owner"
+++

# Intent: Let a repository adopt evaluator-evidence enforcement without falsifying or freezing its history

## Problem

Released harness 0.6.0 requires every `released` release record to carry
`evaluator_evidence_path` and `evaluator_evidence_sha256`. A record written
before that rule existed cannot carry them, and `SPEC-REB-001` states as a
non-goal that historical release and verification records are never rewritten to
add evaluator evidence. The two statements are individually correct and jointly
unsatisfiable for any repository that already holds such a record.

This repository does not feel the contradiction, because
`LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE` in the managed validator names six
identifiers, `RLS-SEH-001`, `RLS-SEH-002`, and `RLS-SEH-004` through
`RLS-SEH-007`, all of them its own. The set is hard-coded in managed,
hash-locked source. It is described in exactly one place in the artifact tree,
`docs/engineering/released-evaluator-boundary/evidence/WO-REB-002-implementation.md`,
which is non-authoritative evidence. A consumer repository has no equivalent and
no mechanism to obtain one.

The consequence was measured, not predicted. In a consumer repository governed by
0.4.0, holding one released record `RLS-MOK-001` with
`released_at = "2026-08-19T17:53:05Z"` and no evaluator-evidence fields, a
complete and otherwise clean 0.6.0 upgrade transaction produces exactly one
diagnostic:

    [E012] [governance] docs/engineering/simulation/releases/RLS-MOK-001.md:
    field 'evaluator_evidence_path' must be a non-empty string

That single error makes `validate` FAIL, the dashboard INVALID, and `preflight`
FAIL in both the `start` and the `review` phase. Every governed action in that
repository stops and its required CI check is red on every push. Nothing else in
the transaction is wrong: 19 of 36 managed files change, `doctor` reports 87
PASS, 0 WARN and 0 FAIL, and the identical error is reported by the installed
released evaluator and by the upgraded in-repository script.

No in-repository remedy exists. The allowlist is managed and hash-locked, so
editing it breaks integrity and the required gate. Binding evidence onto a
released record would be a falsification of an immutable fact and is forbidden by
the specification. The predecessor-bootstrap path is not an alternative:
`REQ-REB-008` scopes it to exactly one contract-bound bootstrap release record,
states as a non-goal that it is not a missing-evidence allowlist and cannot fall
back to a generic one, requires a `ready` record, and never waives the binding.
The repository is therefore expected to obey a prohibition for which the harness
ships no mechanism.

The wider defect is that the six-identifier set is a repository-specific fact
living in code that is distributed to every consumer. Consumers inherit this
repository's history as their only permitted exception.

## Desired outcomes

- A repository holding pre-enforcement released records can adopt schema-3
  evaluator-evidence enforcement, and its governed work continues.
- The exemption for such a record is declared once, by an accountable owner, in a
  reviewable governed artifact, and remains valid without being restated at every
  later upgrade.
- No historical record is rewritten, recomputed or repointed to obtain the
  exemption.
- A record prepared under schema-3 rules is never exempt, and a partially bound
  record is never exempt.
- The exemption is visible as debt for as long as it is in force, rather than
  silently absorbed.
- An upgrade that would freeze the repository is refused before it writes
  anything, naming the records that must be declared, instead of succeeding and
  leaving a dead repository.

## Actors and stakeholders

- Consumer repository owners, who currently cannot adopt 0.6.0 at all if they
  have ever cut a release.
- Release owners, who must not be offered falsification of an immutable record as
  the way out.
- Quality and security owners, who require that the exemption stay narrow,
  accountable, dated, and impossible to widen into a general waiver.
- This repository's own owners, whose six-identifier compatibility set is the
  present mechanism and must keep working unchanged.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Repositories able to adopt enforcement with pre-existing released records | this repository only | any repository with an accountable declaration | packet verification |
| Repository-specific identifiers hard-coded in distributed managed source | 6 | 6, frozen and closed to additions | every candidate review |
| Authoritative artifacts describing the exemption mechanism | 0 | 1 specification | packet verification |
| Exemptions in force that produce no diagnostic | all | 0 | every `validate` run |
| Upgrades that freeze a repository after a successful apply | possible | refused before any write | every `upgrade --apply` |
| Historical records rewritten to obtain an exemption | 0 | 0 | every `validate` run |

## Non-goals

- Rewriting, recomputing or repointing any existing `RLS`, `VREC`, `WO` or `REL`
  field. The prohibition in `SPEC-REB-001` stands and this intent depends on it.
- A generic, undated or self-service missing-evidence allowlist. The exemption is
  per-record, owner-declared, and guarded by the record's own release instant.
- Relaxing the binding for a `ready` release record, for a verification record,
  or for any record prepared after enforcement existed. `prepare-release` keeps
  writing the binding under `SPEC-REB-001` rule 13.
- Reopening the predecessor-bootstrap contract. `REQ-REB-008` and `SPEC-REB-003`
  are unchanged and are not a fallback for this problem.
- Retiring the six-identifier self-hosting compatibility set, or migrating this
  repository's own history onto the new mechanism. That belongs to a separate
  chain and would touch another domain's implemented work order.
- Releasing a harness version, publishing it, or upgrading any consumer. The
  mechanism reaches consumers only through a separately authorized release.
- Changing how evaluator evidence is captured, canonicalized or hashed.

## Principles and immutable constraints

An immutable record is read, never rewritten. An exemption is a declared,
attributable act with a date, never a default. Absence of an exemption fails
closed. The scope of an exemption is bounded by facts the repository already
holds, not by an operator's assertion at run time. A mechanism distributed to
consumers never encodes one repository's history as the universal exception.

## Risks and assumptions

- Fact: at `2b78f42` the managed and candidate validators both hold a
  six-identifier `frozenset`, and the candidate copy is the one consumers run;
  `se_harness/cli.py` resolves `validate` to
  `templates/repository/standard/scripts/validate_engineering_artifacts.py` from
  the installed distribution.
- Fact: the `[evaluator_upgrade]` packet is a table in the authorizing work
  order's own front matter, as `WO-HUP-002` demonstrates, so the artifact graph
  already contains the only place a declaration would belong.
- Fact: `se_harness/upgrade_authorization.py` requires the
  `[evaluator_upgrade]` field set to equal `AUTHORIZATION_FIELDS` exactly, so an
  optional key is an explicit contract change and cannot be smuggled in.
- Fact: the validator never reads `[evaluator_upgrade]` today, so this becomes
  the first validator-side reading of that table.
- Fact: the managed work-order lifecycle in `WORKFLOW.json` marks exactly
  `approved`, `in_progress`, `implemented`, `verified` and `released` as
  authority-granting, so "an authoritative declaration" needs no new state list.
- Fact: `se_harness/installer.py` records no timestamp for the upgrade
  transaction and preserves the original `installed_at`, so no recorded schema-3
  transition instant exists. Dating must come from artifact lifecycle events.
- Assumption: the validator script must stay self-contained for consumers, so the
  declaration logic exists twice, once in the script and once in `se_harness`
  for the installer's pre-apply refusal. Their agreement is a tested property,
  not an assumption.
- Assumption: an owner willing to declare a record is a better gate than an
  environment variable or a command-line flag, because the declaration is
  reviewable in the diff that introduces it.
- Risk: a declaration is a permanent widening of what validates. The date guard
  bounds it: a record released after the declaring work order was approved can
  never be covered by that declaration.
