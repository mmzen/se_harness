# Evidence skill implementation

The shared `evidence` skill prepares observed evidence through the existing
released evaluator. It distinguishes evidence writing from read-only checks,
keeps failures visible, inspects uncertain effects before retrying, and leaves
assurance, release and external delivery decisions with their owners.

## Delivered files

- `plugins/verity-plane/common/skills/evidence/SKILL.md` selects the existing
  procedure and requires current verified context before governed writes.
- `references/records.md` describes handoff, evidence, VREC and RLS preparation,
  including generated output and separate candidate/governance commits.
- `references/external-actions.md` matches the exact action, candidate, evidence
  and destination, and requires demonstrated independent enforcement before
  agent merge or publication. Read-only inspection keeps its existing permissions.

The skill reuses the sibling change skill's authority applicability reference.
It introduces no evaluator command, approval store, host hook or release build.

## Acceptance evidence

| Evidence | Purpose |
| --- | --- |
| `governance/start/` | Actual released 0.17.0 delegated start and live exact-HEAD gate. |
| [Instruction review](instruction-review.md) | Two narrow corrections, original limitations and reviewer scope. |
| [Independent Windows observations](acceptance/independent-windows/REPORT.md) | EVD01â€“10, 82 exact traces, passing retained-hash audit and zero duplicate approval prompts. Real released 0.16.0 preparation calls; intercepted external effects. |
| `checks/initial/` | Initial skill/distribution, released integrity/graph, review-preflight and scope observations; actual candidate doctor differences. |
| [Check qualification](checks/qualification.json) | Passing 1,134-test source CI (four skipped), exact job/log, and expected candidate/released skew. |
| `tests/plugin_integration/evidence-skill/portable/` | Fixed-observation Linux replay infrastructure; separate from an agent's instruction choices. |

The original capture expectation omitted generated dashboard files. That failure
is retained, alongside a fresh corrected capture with its full write footprint
declared before dispatch. A separate invalid fixture enum was corrected after
the released evaluator refused it. Neither original failure was removed.

Recovery observations cover a lost acknowledgement after successful capture,
unavailable inspection, and an explicitly injected partial record without its
sidecar. They demonstrate no further writes under uncertainty; they do not
simulate an in-flight evaluator crash. The external positive is one simulated
effect under a separately calibrated fixture control, with no production action.

[Linux replay](acceptance/linux-replay-attempt2/REPORT.md) passed 82 fixed
command calls using released 0.16.0 on Ubuntu 24.04 / Python 3.12.3. Native
candidate, evidence and governance identities were established before their
operations. Seventeen empty negative command spans remain replay evidence,
not additional model-refusal observations. Original attempts and test-runner
changes remain recorded alongside the corrected results.

The [replay-tool review](replay-review.md) identified missing per-call records
on timeout or launch failure. Its narrow correction has separate focused probes;
the prior acceptance runs retain their actual original runner identities.

## Scope of the claims

The acceptance work uses disposable repositories and intercepted external
tools. It does not qualify native host activation, production merge/publication
enforcement, or live skill migration. Fixture owner decisions are synthetic
inputs; they grant no authority over this repository or any real destination.
Record preparation is distinct from human assurance. The live delegated
completion and ready-record receipts are retained separately under `governance/`.
