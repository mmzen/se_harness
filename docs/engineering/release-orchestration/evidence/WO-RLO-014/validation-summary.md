# Draft package validation

Selected released evaluator: 0.21.0, invoked with its absolute private Python
path and `-I -m se_harness` from outside the checkout. Base: merged main commit
`745884fd6c6b7dd0c7185b7427efcf9bd33c7e0d`.

- Formal validation: **0 errors**, 58 repository warnings.
- None of the warnings names an artifact in this new package.
- All three checkpoint-free checks completed with instruction discovery available.
- The work orders and governing definitions remain drafts. No approval, start,
  implementation, verification acceptance or external publication has occurred.

| Work order | Current state | Passing checks | Remaining approval input |
| --- | --- | --- | --- |
| WO-RLO-014 | draft | Graph, integrity and decision checks pass | QGS-ASSURANCE: human confirmation of required commit-bound verification |
| WO-RLO-015 | draft | Graph, integrity and decision checks pass | QGS-ASSURANCE: human confirmation of required commit-bound verification |
| WO-RLO-016 | draft | Graph, integrity and decision checks pass | QGS-ASSURANCE: human confirmation of required commit-bound verification |

The evaluator's current corrective step is to supply the assurance classification
for each work order (`QGS-ASSURANCE`). The proposal is **required** verification
bound to the exact commit. The authoring procedure requires human confirmation;
no invented decision-maker is placed in a draft assurance table. After confirmation,
record the actual human, preview the selected approvals, and apply only the exact
reviewed transitions that pass. The governing definitions need their own selected
approval transitions in that transaction.

Commands used:

```text
harnessctl validate REPO --json
harnessctl check REPO --artifact WO-ID --json
harnessctl check REPO --artifact WO-ID --checkpoint transition --target approved --json
```

Here `REPO` is the selected absolute checkout; `WO-ID` is each of WO-RLO-014,
WO-RLO-015 and WO-RLO-016. These checks are read-only.

[Raw evaluator results](draft-evaluator-results.zip) retain all seven JSON outputs.
[Reviewed artifact digests](reviewed-artifacts.json) identify the exact draft bytes.
Implementation tests have not been run because no implementation has started.
