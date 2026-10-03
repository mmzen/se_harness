# Plugin 0.2.5 qualification progress

Evaluator 0.22.0 is published. Plugin qualification remains incomplete.
WO-RLS-035 stays `in_progress`; VREC-PLG-032 has not been prepared or verified.
The marketplace and latest/last markers have not been changed by this work.

## Published evaluator

- [GitHub release](https://github.com/mmzen/se_harness/releases/tag/v0.22.0)
- [PyPI 0.22.0](https://pypi.org/project/se-harness/0.22.0/)
- [Publisher](https://github.com/mmzen/se_harness/actions/runs/37096141972)
- [Demo site](https://www.verityplane.ai/)

The publisher's third observation passed all five public-install checks. GitHub,
PyPI and Pages report exact identities. Independent GitHub and PyPI-index wheel
downloads both match `44543f242ed19bb30cfd65da415372a87508a6e439204d7f3e37f9f45aefe4e4`. The first two observation attempts failed
while PyPI had not exposed the version in its index; those failures are preserved.
No privileged publication step was repeated.

Candidate: `abbec12ac5524c8adfb28693f846dd59de88f759`.
Governance snapshot: `01ec43c86c9d30949295c07ac91c742be91e713a`.
The approved wheel, sdist, release tag and released record were not rebuilt or replaced.

## Observed checks

| Check | Result |
| --- | --- |
| Both exact released-input packages and independent content check | Passed |
| Windows focused suite with selected 0.21.0 checker | 62 tests; 2 skipped |
| Linux focused suite with selected 0.21.0 checker | 62 tests; 1 skipped |
| Portable adapter walkthrough | 41 steps passed on each platform |
| Codex CLI startup, activation, manual/automatic compaction and resume | Passed with full entry |
| Codex CLI session isolation and selection boundaries | Passed |
| Claude authenticated native checks | Pending: expired OAuth |
| Codex Windows desktop | Pending: no exact-package desktop trace |
| Native new/resumed work and delivery handoff | Pending: not yet executed for these inputs |
| Human verification / public marketplace / public fresh and update tests | Pending |

The unit suite skips are retained in raw outputs. Portable checks exercise real
installed wheels but simulated host events; they do not establish native support.
Codex CLI codex-cli 0.159.2 delivered the complete expected entry and preserved
the fixture checkout. The disposable profile's prior plugin was restored.
Native tests used existing test authentication; no credentials were retained.

## Limits and failures

Claude's existing bound is 10,000 UTF-16 units for the full delivered context,
including paths. The long workspace test needed 10,052 and was correctly refused.
The identical packages passed from a shorter temporary directory. This result
does not establish support for the failed long-path configuration. No policy was
truncated, bound increased or package changed.

The first Linux test environment lacked the installed evaluator needed by its
isolated payload-hash subprocess. Preparing an isolated selected 0.21.0 environment
resolved that test prerequisite. Source and assertions were unchanged.

Claude's status command reported logged in, but its live request failed:
`Failed to authenticate: OAuth session expired and could not be refreshed`.
The human replied: **“Not now—keep those checks pending.”** Claude and desktop
remain unverified. This is not a waiver or risk acceptance.

## Retained evidence and continuation

[qualification.json](qualification.json) contains the result matrix, identities,
native claims, raw-file hashes and remaining actions. [raw.zip](raw.zip) retains
actual commands, failures, successful reruns and native traces.
[public-evaluator.json](public-evaluator.json) retains the successful publication
and independent public-install observations. [delivery-plan.json](delivery-plan.json)
is the next version of WO-RLS-034's approved five-surface plan; the earlier plan
is preserved unchanged with SHA-256 `a0fd4004b92e2018f0f096c337f9193d559b0ee4208b9e77d870641f8571d30c`. Public marketplace revision
and documentation closeout remain unset because their work is not complete.

The observed marketplace parent is `7e366438165a40a14783bac650a2887e7ec8bc75`; read it again before publication.
Continue exact-package native qualification when the human can refresh Claude
authentication and assist with the desktop check. Complete the repeated-work and
delivery-handoff criteria. Then finish the work-order checks, prepare VREC-PLG-032,
publish the review and request the reserved human verification decision.
Existing release execution authority remains recorded; no new publication grant
is requested. WO-RLS-036 follows with public-route checks and latest/last promotion.
