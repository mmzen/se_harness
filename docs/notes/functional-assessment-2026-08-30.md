# Functional assessment, 2026-08-30

<!-- Target expertise: 3/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Point-in-time assessment of `main` at `574e132` (candidate 0.12.0, root evaluator 0.11.0). It is a reading of what the tool does and how it is to operate, not a formal artifact; it grants no approval and changes no state. The findings were filed as issues #280 to #286 (tracking: #287) under the `functional-assessment` label.

Each statement is marked **Fact** (checked in the CLI, docs, tests or CI on this commit), **Inference** (a reasonable reading of the facts) or **Unconfirmed** (could not be verified from the repository).

## Contents

1. [What it is](#1-what-it-is)
2. [The main workflows](#2-the-main-workflows)
3. [Capability by capability](#3-capability-by-capability)
4. [Cross-cutting findings](#4-cross-cutting-findings)
5. [Scores](#5-scores)
6. [Summary and judgment](#6-summary-and-judgment)
7. [Recommendations](#7-recommendations-by-user-impact)
8. [Implementation plan](#8-implementation-plan)

## 1. What it is

SE Harness makes a Git repository run its own engineering process. You write the plan for a change as small formal files (a requirement, a specification, a verification contract, a work order). The tool then checks that the code change stays inside the plan, that every decision was taken by the right person, and that each step left evidence behind. It ships as one Python package with one command, `harnessctl`, plus a set of managed files it installs into the repository.

Terms used below, in plain words:

- **Work order (WO)**: a file describing one bounded change and which paths it may touch.
- **Verification record (VREC)** and **release record (RLS)**: files that pin a result to one exact commit.
- **Decision right**: the rule saying who may take a given decision.
- **Evaluator**: the installed copy of the tool that judges the repository. It runs from *outside* the checkout, at a pinned version.
- **Gate / checkpoint**: a named set of checks run at a fixed moment (start, handoff, scope).
- **Projection**: `check` without a checkpoint. It reads the state and names the next step; it judges nothing and writes nothing.
- **Restitution**: the fixed-format result block every workflow command prints, with a digest of its own content.
- **Managed file**: a file the tool installs and hash-locks. Editing it by hand breaks `doctor` and CI.

Measured on `main` (**Fact**): 22 subcommands plus 4 `qualify` roles; 13.5k lines of product code; 922 tests in 48 modules; 46 notes (8.8k lines); 1,436 formal artifacts in 54 domains; 72 distinct diagnostic codes in product code. The package declares no dependencies and needs Python 3.11 or later.

## 2. The main workflows

### 2.1 One change, from plan to merge

**Fact.** The managed procedure has 18 operator steps. Eleven decision rights are involved; three (start a WO, mark it implemented, prepare its VREC) can be delegated to an automated actor behind a green CI check; the other eight stay human. Measured on the most recent completed work order (WO-ECP-020): **11 governance commits plus 4 merge commits, about 11 pushes**, for a change that touched one product module and one test module.

```text
create-artifact -> transition (approve definitions, 3-4 human decisions)
-> transition (approve WO) -> check --checkpoint start -> transition (start)
-> implement -> evidence -> check --checkpoint handoff --from-git main
-> pr-body -> transition (implemented) -> capture-verification
-> transition (verified) -> merge
```

**Inference.** The cost is dominated by ceremony, not by the change. Each lifecycle act is a commit and a push because CI must re-read the tree. A three-line fix costs the same number of acts as a large one.

### 2.2 One release

**Fact.** Ten steps and roughly twelve commands, mixing `harnessctl` with three repository-owned Python scripts and two manually dispatched GitHub workflows. Two steps are pure hand-work at the end: marking the GitHub Release as latest and force-moving a `last` tag. The developer note records that this last step was missed for two consecutive releases.

### 2.3 An agent inside a governed repository

**Fact.** The agent's loop is short: run `check`, do what the result says, run `check` again. The result names the next command verbatim, or the human decision that is due and who owns it. `check` with no arguments picks the single in-progress work order and returns the reading list, so the first call needs no prior knowledge.

## 3. Capability by capability

### 3.1 Install, adopt, upgrade, doctor

- Purpose: put the managed files into a repository, keep them hash-locked, move them forward safely when the tool version changes. Used by the repository owner.
- Works well (**Fact**): `doctor` is the clearest command in the product, a flat list of PASS/FAIL lines; `upgrade` refuses partial writes when a managed file was customized, and now retires files that left the managed set (WO-DST-022).
- Difficult (**Fact**): the evaluator must be installed in a virtual environment outside the checkout and run as `python -I -m se_harness`. Running from the checkout is refused with codes such as `RID018` and `MG005`, readable only in source. No getting-started page says this up front.
- Maturity: complete. Two older lock schemas are still readable, and a whole module exists for releases that predate evidence rules.

### 3.2 validate, inspect, dashboard

- Works well (**Fact**): `validate` is fast and deterministic; `inspect` answers "what is waiting on whom" in one screen.
- Difficult (**Fact**): on this repository `validate` reports 0 errors and **485 warnings**; `inspect` reports 700 findings. Almost all are advisory style warnings nobody acts on. `doctor` and `dashboard` have no `--json`.
- Maturity: complete. `doctor` re-runs the validator internally to show one warning code.

### 3.3 check, preflight, evidence, pr-body

- Purpose: the core. `check` says what state one artifact is in and what to do next; with a checkpoint it runs a gate and prints pass/fail per rule. `evidence` writes a work order's packet header; `pr-body` prints the pull-request body CI needs.
- Works well (**Fact**): the result block is consistent and honest ("done", "not done", "blocked by", "decision required", "next"), and the next step is copy-pastable. A blocked result never tells you to re-run the same command. The handoff checkpoint derives the change set from Git rather than trusting a typed list.
- Difficult (**Fact**): three hidden prerequisites. The handoff digest is only stable after *two* runs, because the first writes `handoff.json`, which joins the change set. After any merge from `main` the packet must be re-bound with `evidence`, or the gate reads `not_assessable`. On Windows, switching branches converts the packet to CRLF and the evaluator refuses it (`WEX-ECP-010`) while `git status` stays clean. Error text can carry a doubled code (`WEX210: WEX210: check accepts only WO, VREC, or RLS artifacts`). `preflight` still exists as a separate command although `check --checkpoint start` composes it.
- Maturity: complete and the most refined part. `evidence` accepts four checkpoints, `check` five.

### 3.4 transition

- Works well (**Fact**): plan-then-apply; illegal moves are refused with the rule's name; several artifacts move in one atomic transaction; the delegated route reuses the same command with a role name.
- Difficult (**Fact**): the reason text is typed by hand and the same decision is restated in the commit message. The `--decision` value is an unverified role assertion. There is no way back from `implemented`: a change after completion needs a second work order.
- Maturity: complete.

### 3.5 capture-verification, prepare-release, release-unit

- Works well (**Fact**): records bind an exact commit, the evaluator's identity and the evidence digests; a later edit cannot rewrite them. `release-unit --toml` produces the contract table so it is measured, not typed.
- Difficult (**Fact**): a record cannot contain its own commit hash, so every record is a separate later commit. `capture-verification` fails with one code, `WEX301`, for four causes: work order not implemented, dirty tree, packet not tracked, and an unrelated 30-second subprocess timeout (seen once). Exit codes differ from the rest of the CLI (2 rather than 1). Naming varies: `--work-order` here, `--artifact` in `check`, `--id` for the new record, `--authorized-by` in `prepare-release` whose help says it "does not authorize".
- Maturity: complete. A verified record is terminal by design.

### 3.6 qualify (four roles), identity, rehearse-recovery

- Purpose: release-pipeline evidence. Used by CI almost exclusively.
- Works well (**Fact**): every lane in the eight workflows calls one of these, and release records cite their outputs. The independence label ("candidate-controlled" versus an independent verifier) is printed on every result.
- Difficult (**Fact**): 25 `RID` codes and eleven required options across the four roles; `identity` has no `--json`. The 0.6.0 bootstrap branch (`accept-candidate`) still lives in the candidate-evidence workflow although the command was removed. **Inference**: no human runs these by hand; the option surface is oversized for the two people who ever read it.
- Maturity: complete for CI; provisional as a human tool. **Unconfirmed**: whether any consumer other than this repository runs `qualify`.

### 3.7 scaffold-domain, create-artifact, renumber-artifacts

- Works well (**Fact**): `create-artifact` allocates the next free id across every local ref, closing a real trap (id collisions across branches), and prints an authoring checklist.
- Difficult (**Fact**): `renumber-artifacts` is 1,316 lines, the second-largest module, for an operation never used operationally. None of the three has a CLI-level test; `create-artifact` and `scaffold-domain` always exit 0.
- Maturity: `create-artifact` complete and useful; `scaffold-domain` could be a flag of it; `renumber-artifacts` dormant.

### 3.8 Delegation class, skills, select-work-order

- Works well (**Fact**): the delegation design is small and legible: one table on a work order, one owner file for the gate source, the same commands with a role name. `check` tells the actor whether the decision is its own.
- Difficult (**Fact**): not yet active anywhere; it becomes real only after 0.12.0 is released and adopted, and only with a branch-protection rule the owner has not set. The README and the installation note still describe three skills that were retired; only two ship. Four "Phase 4" notes describe a removed command and are indexed as live guidance. A PR body with two `Harness-Work-Order` lines turns the managed check red, and because CI reads the stored event payload, fixing the body does not re-green it until the next push.
- Maturity: delegation implemented, unproven in production; skills two real, one adapter, three ghosts in the docs (issues #273, #274 open).

## 4. Cross-cutting findings

### 4.1 Overlap and too many names for one thing

- **Fact.** Three commands were folded or removed in four days (`focus`, `next`, `accept-candidate`); each left a tombstone guard. The list is now 22, down from 26 at the command audit.
- **Fact.** Remaining overlap: `preflight` versus `check --checkpoint start`; `doctor` re-running `validate`; `adopt` being `init` plus a report; `scaffold-domain` being a prerequisite of `create-artifact`.
- **Fact.** An artifact is named with `--artifact`, `--id`, `--work-order`, `--set ID=`, `--map OLD=NEW` or `--release-record` depending on the command. The repository root is a positional `target` in 18 commands, absent in 3, `--repository` in one, `--checkout-root` in another, `--root` for the scripts.

### 4.2 Hidden prerequisites

- The external evaluator venv and the `-I` flag.
- A clean tree, a tracked packet, an implemented work order, and a later commit for each record.
- The two-run handoff fixed point; the re-bind after each base merge; a refreshed local `main` for `--from-git main`.
- Line endings: evidence JSON is pinned to LF by the managed `.gitattributes`, a Markdown packet is not.
- A single `Harness-Work-Order` line in the PR body, read from the stored event.

### 4.3 Terminology and discoverability

- **Fact.** No glossary. "Restitution", "projection", "handoff" and the abbreviations VREC/RLS are used in the README and the managed instructions before any definition. The developer note counts "467 diagnostic codes across 36 prefixes"; there is no code index, and only seven `WEX` codes are tabulated anywhere. `MG`, `RID`, `EPS`, `PRE` codes are readable only in source.
- **Fact.** The route a human is pointed down is 11 documents (about 2,200 lines) before the 7 managed policies (another 1,000 lines plus 500 of JSON). There is no getting-started page; the one end-to-end walkthrough sits at step five of the suggested path.
- **Fact.** About a quarter of `docs/notes/` (2,300 lines) is dated approval and review material listed as live operator routes; nine notes are not indexed at all.
- **Fact.** The good news: the command reference matches the CLI exactly (a test enforces it), the target-expertise score on notes is a real aid, and `check`'s output is self-explaining to a first-time reader.

### 4.4 Temporary and special-case paths still in the product

**Fact.** Twenty-three retained compatibility paths were counted: schema-1 lock digests, legacy-newline hash matching, a one-release packet-header compatibility (`W-ECP-002`), two reserved-forever codes (`PV001`/`PV002`), legacy architecture and ADR exemptions in the validator, a legacy release-evidence module, retained `.gitattributes` rules waiting on a follow-up work order, and the 0.6.0 verifier branch in CI. **Inference.** Most protect only this repository's own history; a fresh adopter carries all of them for nothing.

### 4.5 Reliability

- **Fact.** Determinism is strong where it matters: digests reproduce across runs and platforms, records are immutable, the mutation guard blocks a candidate copy of the tool from writing state.
- **Fact.** The Windows suite has one standing error treated as the baseline; five subcommands are never exercised through the CLI entry point by any test; one CI reconcile digest is documented as run-dependent.
- **Fact.** Failures are refusals, never partial writes. Diagnosis is uneven: `WEX301` covers four unrelated causes.
- **Unconfirmed.** A Linux temp-directory teardown flake was filed as issue #269; its frequency could not be measured here.

## 5. Scores

| Dimension | Score | Evidence |
| --- | --- | --- |
| Complexity (0 simple, 10 extreme) | 8 | 22 commands with 4 sub-roles; 18 steps and about 15 commits per change; 36 code prefixes; 21 artifact-id prefixes; 23 compatibility paths; three environments to reason about (root evaluator, candidate, CI verifier). |
| Behaviour clarity (0 unpredictable, 10 clear) | 6 | The result block and plan-then-apply are exemplary; refusals name their rule. Against that: hidden two-run fixed point, rebind-after-merge, CRLF refusal, doubled code prefixes, one code for four causes. |
| Ease of use (0 hard, 10 effortless) | 3 | External venv plus `-I` before anything works; about 11 pushes per change; option names vary per command; a release needs 12 commands across three tools and two manual tag steps that were missed twice. |
| Effectiveness (0 to 10) | 7 | It does what it claims: scope enforced on every PR, decisions attributed, records immutable, releases reproducible byte for byte. Weakened by the warning flood and by delegation being unproven in production. |
| Reliability (0 fragile, 10 solid) | 6 | 922 tests, deterministic digests, refusal over partial write. Minus: one standing Windows error, five commands untested at the CLI, a run-dependent CI digest, one timeout reported as a refusal, one filed flake. |
| Discoverability (0 hidden, 10 self-explanatory) | 3 | No glossary, no code index, no getting-started page; about 2,200 lines before the policies; README describes skills that do not ship; a quarter of the notes are dated packets listed as live. |
| Overall functional maturity (0 to 10) | 5 | Core lifecycle and release evidence are complete and stable; authoring helpers and delegation are complete but unproven or dormant; documentation and CLI consistency lag the code by several releases. |

## 6. Summary and judgment

### The situation in plain words

The harness works. On this repository it has run every change for weeks, and it catches real things: a diff outside the declared scope, a record bound to a commit that no longer exists, a body missing the work-order line. The core loop for an agent (run `check`, do what it says) is genuinely good. But the product around that core has grown by accretion. There are too many commands with too many option spellings, a long tail of compatibility code that serves only this repository's past, and a documentation set where history, plans and live instructions sit side by side without labels. The result is a system that is trustworthy once you know it and hard to approach until you do.

### Strongest parts

1. The `check` result block: one shape for every operation, self-explaining, with the next command spelled out.
2. Commit-bound records and Git-derived change sets: evidence you cannot fake by typing.
3. Plan-then-apply `transition` with atomic multi-artifact transactions.
4. The managed-file lock and `doctor`: a flat, honest health check.
5. Byte-reproducible release builds verified from an independent released evaluator.
6. The delegation class: three decisions delegated with one table, no new commands.

### Main problems

1. Ceremony per change: about 15 commits and 11 pushes for a small fix, most of them governance-only.
2. Hidden prerequisites that produce confusing refusals: external venv, two-run digest, rebind after merge, CRLF on Windows, stored PR body.
3. CLI inconsistency: target addressing, artifact naming, `--json` coverage, exit codes, checkpoint sets.
4. Documentation debt: no glossary or code index, stale skill descriptions, dated packets indexed as live, about 2,200 lines before the policies.
5. Signal loss: 485 warnings and 700 findings that nobody acts on.
6. Dead weight: `renumber-artifacts`, legacy release evidence, schema-1 lock support, the 0.6.0 CI branch, `rehearse-recovery`.

### Simplify, combine, clarify, remove

| Action | Item | Why |
| --- | --- | --- |
| Combine | `preflight` into `check` | Already composed by the start checkpoint and the projection; last duplicate name. |
| Combine | `scaffold-domain` into `create-artifact --domain`; `adopt` into `init --report` | Each is the other plus one step. |
| Simplify | One spelling for the repository (`target`) and one for the artifact (`--artifact`); `--json` everywhere; one exit-code rule | Removes most of the per-command relearning. |
| Simplify | Let `check --checkpoint handoff` rebind the packet and reach its fixed point in one run | Removes two hidden steps and one commit per change. |
| Clarify | Glossary, diagnostic-code index, a 60-line getting-started page; banner or archive for dated notes; fix the README skill list | Discoverability is the lowest score and the cheapest to raise. |
| Clarify | Demote the style warnings (`W-AUT-*`) out of the default `validate` count | Restores the error/warning count as a signal. |
| Remove | Schema-1 lock support, legacy release evidence, the 0.6.0 verifier branch, retained `.gitattributes` rules, reserved `PV` codes | Only this repository's history needs them; fresh adopters pay for them. |
| Freeze or remove | `renumber-artifacts`, `rehearse-recovery` | Never used operationally; large surface to keep tested. |

### Final judgment

**Inference.** The complexity is justified at the core and not at the edges. The lifecycle engine, the commit-bound evidence and the reproducible release path deliver something most teams cannot get any other way: a repository whose own history proves who decided what, over which exact bytes. That is worth an evaluator venv and a fixed result format. It is not worth 22 commands with six ways to name a file, a 2,200-line reading list, or 15 commits per fix. Roughly a third of the current surface carries cost without delivering value to anyone but this repository's past. Trim that third and fix the ceremony, and the remaining complexity is proportionate to what the tool gives back.

## 7. Recommendations, by user impact

| Order | Issue | Priority | Recommendation |
| --- | --- | --- | --- |
| 1 | #280 | P1 | Cut the per-change ceremony: self-binding single-run handoff; fewer governance commits; no push to re-read a fixed PR body. Target: half the commits per change. |
| 2 | #281 | P1 | Write the three missing pages: getting started (venv, `-I`, first `check`), a glossary, a diagnostic-code index generated from source. Fix the README's skill list. |
| 3 | #282 | P1 | Normalise the CLI in one release: naming, `--json`, exit codes, the doubled prefix, one cause per code for `WEX301`. |
| 4 | #283 | P2 | Quiet the validator: style advisories off by default, so 0/0 means clean. |
| 5 | #284 | P1, decision | Release 0.12.0 and adopt it, then turn on branch protection so the delegation class does the work it was built for. |
| 6 | #285 | P2, decision | Retire the compatibility tail in one governed sweep, with a stated floor. |
| 7 | #286 | P2 | Label or archive the dated notes; index the nine orphans or delete them. |

Tracking: #287.

## 8. Implementation plan

Two facts drive the ordering. Anything merged before the 0.12.0 release ships in it, and this repository only feels a product change after that release is adopted as root (#284). And the ceremony itself (one work order per pull request, packet re-bind after every base merge) means more than two pull requests in flight on overlapping modules is self-defeating.

```text
WAVE 0  independent, parallel, no prerequisite
  #281a  README skill list fix, getting-started, glossary        (docs only)
  #286   archive/label dated notes, index orphans                (docs only)
  #283   W-AUT-* advisories out of default count                 (template validator only)
  #285a  CI 0.6.0 accept-candidate branch; legacy_release_evidence;
         schema-1 lock support  <- needs the floor decision (#285) first

WAVE 1  product changes, must be in 0.12.0 to matter; sequential on cli.py
  #282   CLI normalisation
  #280b  self-binding single-run handoff (same modules as #282: do it on top)
  #280c  managed lane reads the PR body live (template engineering-harness.yml)
  #281b  generated diagnostic-code index (after #282's WEX301 split)

WAVE 2  #284: release 0.12.0 -> adopt as root -> branch-protection decision
         -> hosted delegation demonstration

WAVE 3  only after adoption
  #285b  retained .gitattributes rules (root evaluator must advance first)
  #280c  takes effect on this repository (the managed lane is the root copy)
  #285c  delete the three tombstone guards, one release later (0.13.0)
```

Parallel sets: #281a, #286 and #283 touch disjoint files; #285a runs beside Wave 1 (installer/integrity modules versus cli/workflow modules). Not parallel: #282 and #280b both rewrite `cli.py` and `workflow_compliance.py`.

Hard prerequisites:

| Item | Waits on | Reason |
| --- | --- | --- |
| #285 (all of it) | owner floor decision | it removes readable history |
| #285b `.gitattributes` rules | #284 adoption | the root validator copy still carries the rule |
| #285c tombstones | one release after 0.12.0 | the removal window the specifications state |
| #280c effect here | #284 adoption | the managed workflow is hash-locked at the 0.11.0 bytes |
| #281b code index | #282 | otherwise it indexes codes about to be split or renamed |
| branch protection | #284 release and adoption | the required check must be the one the class reads |
| hosted delegation demonstration | branch protection | that is what turns refusal into prevention |

Two things the plan reveals. First, preparing and verifying a VREC in one commit (#280a) needs no product change: `capture-verification` writes the record and `transition --apply` works on the untracked file, and neither contains its own commit hash; that is a process fix for the getting-started page. Second, do not hold the release for the docs: notes are repository documents, not packaged; what must be in 0.12.0 is Wave 1.

Suggested sequence: (1) decide the compatibility floor (#285) and branch protection (#284); (2) start Wave 0 in parallel and #285a in its own lane; (3) Wave 1 as two stacked work orders, #282 then #280b/c; (4) #281b once #282 merges; (5) release 0.12.0, adopt, branch protection, hosted demonstration; (6) Wave 3 as one cleanup work order after adoption, tombstones with 0.13.0.

Critical path: floor decision, #282, #280b/c, release, adopt, branch protection.
