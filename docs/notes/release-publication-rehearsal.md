# Rehearsing the credential-free publication path

<!-- Target expertise: 6/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is a repository-specific control for `mmzen/se_harness`. It is not installed into consumer repositories, `harnessctl` exposes no rehearsal command, and a rehearsal result grants no verification, release, publication, deployment, or evaluator-adoption authority.

`.github/workflows/publish-pypi.yml` performs the last mile of a release as one credentialed transaction. Most of its work needs no credential at all: resolving a plan, proving the released evaluator's identity, exporting the candidate, building it twice, normalizing sdists, assembling a bundle, and verifying that bundle. Only after all of that does a credential appear.

That credential-free work is split by platform. `resolve` runs only on `ubuntu-latest`, `qualify` only on `windows-2022`. So before this control existed, no run ever exercised the Linux half on Windows or the Windows half on Linux. `RC-060-11` in the `0.6.0` release recovery analysis records what that cost: incidents `I-15` and `I-16` were both platform details — Git Bash path conversion, and a Windows 8.3 short-name alias for the temporary directory — discovered *during* a live release.

The rehearsal closes that gap. It runs the whole credential-free set on **both** platforms, on ordinary candidate integration, with `contents: read` and nothing else.

## Two pieces, one seam

```text
.github/workflows/publish-pypi.yml          <- unchanged, byte for byte
        |
        | read as untrusted text
        v
check-divergence  --------------------------> fails closed on drift
        ^
        | compares against
        v
.github/scripts/publication_rehearsal_mechanics.json   <- data only, no logic
        ^
        | declares what is covered
        v
.github/scripts/rehearse_publication.py     <- runs the mechanics, both platforms
```

The owner chose deliberately to leave the orchestrator alone rather than refactor publication and the rehearsal into one shared program. `ADR-RLO-004` records the trade: refactoring is the stronger answer, but it changes a path whose real behavior is only provable during an actual release. Two programs can drift, so drift is made a red check instead of a silent one.

## Running it yourself

Both subcommands are plain Python with no dependency beyond the standard library.

```bash
# Does the orchestrator still match what the rehearsal covers?
python .github/scripts/rehearse_publication.py check-divergence --repository .

# Rehearse the current candidate. --root must be an empty or absent directory.
python .github/scripts/rehearse_publication.py rehearse --repository . --root ../rehearsal-root
```

Three things to know before the first local run.

**Start from a clean checkout.** One mechanic drives the released evaluator's predecessor-view qualification, and predecessor preparation refuses to run against a dirty worktree. The failure is real but it is about your checkout, not about publication — so the result reports the inherited checkout condition next to the outcomes. A fresh clone at the commit you want to rehearse removes it.

**Line endings matter here.** The candidate checkout is created with `git worktree add`, exactly as publication creates it, so it inherits `core.autocrlf`. On a Windows checkout with `core.autocrlf=true`, a few tests that assert on exact bytes fail for that reason alone; the same commit is green in a `core.autocrlf=false` clone. The result reports the inherited setting, so check a suspected regression against a clean worktree at the same commit before believing it.

**One mechanic is excluded in candidate mode, on purpose.** Publication resolves the evaluator from the schema-3 lock and then qualifies the candidate against the *release record's own* predecessor contract. Those name the same evaluator while a record is being prepared, and differ by one release afterwards: a released record names the evaluator that qualified it, while the lock names the evaluator that release advanced to. So on ordinary integration there is no record the mechanic can accept, and the result says so — reporting `excluded` with both measured identities — rather than reporting a failure of publication. A `release-record` rehearsal of a record under preparation exercises it for real, and there a mismatch is a defect in the record and fails. The repository owner ruled on 2026-08-24 that this is the right report, so treat a candidate that hides the mechanic or calls it `executed` as a defect rather than as a tidy-up; `SPEC-RLO-004` rule 37 governs.

A release owner can also rehearse a *prepared* record before approving it, which is the only mode that compares against an authorized release identity:

```bash
python .github/scripts/rehearse_publication.py rehearse --repository . --root ../rehearsal-root \
  --mode release-record --release-record RLS-SEH-007
```

The hosted lane is `.github/workflows/publication-rehearsal.yml`. It runs on pull requests and on pushes to `main`, and accepts an optional `release_record` on manual dispatch.

## How drift is detected

The divergence check works in layers, because each layer alone leaves a way for the orchestrator to move without anyone noticing.

| Layer | What it catches |
| --- | --- |
| Job classification | a credential-free job appears, or a job's permissions, environment, or secret use changes |
| Mechanic coverage | a mechanic is invoked but undeclared (`uncovered`), or declared but no longer invoked (`stale`) |
| Command keys | a new command appears inside a declared step |
| Step digests | a declared step's script changed at all — a new flag, a changed argument, a reordering |
| Action surface | a step uses an action that is undeclared, or not pinned to a full 40-character commit |

Classification is *fail-closed* in three ways worth spelling out. A job that declares no `permissions` block is excluded, not assumed harmless. A job that cannot be classified fails the check rather than defaulting either way. And exclusion is **transitive**: the orchestrator's `observe` job holds only `contents: read`, but it `needs: github_release`, so it runs after a credential has been used and is excluded too. Five of the orchestrator's seven jobs are excluded; `resolve` and `qualify` are rehearsed.

Every exclusion is reported with the attribute that caused it. A shrinking rehearsal surface has to be visible, or the check quietly protects less and less.

## Why the YAML reader is hand-written

The check parses workflow files with a bounded reader restricted to the Actions subset the two files actually use — it refuses a tab, a duplicate key, or a construct it does not model. That is not a preference for reinvention. `pyproject.toml` declares no dependencies, and a drift check that fails to import is a drift check that does not run.

The second opinion is still available. `--cross-check-yaml` parses the same text with PyYAML and fails if the two disagree about the job mapping, and fails outright if PyYAML is absent rather than falling back silently. The hosted lane installs PyYAML and passes the flag; a local run does not have to.

## What it does not prove

Step digests catch a change *inside* a step. They do not prove that the rehearsal drives its mechanics in the orchestrator's order, or that a mechanic sees the same surrounding state the orchestrator gives it. The checker's unit is one step's script, not the pipeline that reaches it — so a step moved between jobs passes every comparison. `ARCH-RLO-004` records this as the accepted weakness, and `ADR-RLO-004` records what would reopen the refactor decision.

A local run also proves one platform. The other platform's real behavior is first proven by the hosted lane, and hosted runner-image behavior cannot be proven locally at all — which is the same class of gap `RC-060-11` is about, now moved from release time to integration time rather than eliminated.

## Operational boundary

The rehearsal acquires no credential, requests no protected environment, and uses no repository token. It creates and moves no ref, tag, release, index object, deployment, or environment approval, and changes no artifact lifecycle state. It writes only under the rehearsal root you name, and tears that down by unlinking links rather than following them.

A green rehearsal is derived operational evidence. It is not verification, not approval, and no substitute for the qualification that runs inside an authorized release. The governing artifacts are `CAP-RLO-003`, `REQ-RLO-013`, `REQ-RLO-014`, `SPEC-RLO-004`, `ARCH-RLO-004`, `ADR-RLO-004`, and `VER-RLO-004`, under the existing `INT-RLO-001` intent. If this note and those artifacts disagree, the artifacts are authoritative and the disagreement should be reported.
