# Risk artifacts

A risk is a note about something that could go wrong, with an owner and a next action.
Recording one does not stop work.

```sh
harnessctl raise-risk . --domain product --title "Setup on another machine" --description "Only the owner's machine has been tried." --action "Try setup on the next development machine." --owner engineering-owner
```

The command creates a raised `RISK-` artifact. Use `--dry-run` to preview it.
`--stage` and `--category` are optional text. `--threatens` optionally links an artifact.
If useful, add both `--likelihood` and `--impact` (integers 1–5); their product is the
stored score. No score or taxonomy is required.

Add `--with-decision --threatens WO-PRD-001` only when a blocking decision is wanted.
That creates a separate `DEC-` record with accept, avoid and mitigate options.
Answer it with `harnessctl decide` and the appropriate owner decision. Accept requires
a residual and revisit trigger; mitigation names its work order; avoidance names an ADR
or decision. The decision and risk disposition are written together with rollback on failure.

Existing cause/effect records, scores, paired decisions and dispositions remain readable
without rewriting history. `harnessctl risks . --artifact WO-PRD-001` lists linked risks.
A bare risk note can be withdrawn through its normal lifecycle transition.
