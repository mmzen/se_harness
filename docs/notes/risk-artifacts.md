# Risk artifacts

<!-- Target expertise: 3/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Summary: a risk artifact (`RISK-`) records one threat to governed work as a
formal artifact: one cause, one effect, the stage it threatens, and a size on
a five-by-five scale. Recording it raises it. A raised risk stops nothing by
itself; the decision (`DEC-`) that names it holds the threatened artifacts
still until an owner answers, and the answer is copied onto the risk. This
note describes the model that `SPEC-RSK-010` fixes and that `WO-RSK-010`
implemented.

## When a threat becomes an artifact

A threat noticed during work used to land in a pull-request comment or in a
reviewer's memory, and the stage moved on. A risk artifact gives it a place
that is not lost, a size that makes a small threat and a large one read
differently, and a record of who answered it and on what grounds. There is no
threshold: every recorded threat is raised, and no configuration key decides
which ones count.

## The measurement

A risk carries `likelihood` and `impact`, each an integer from 1 to 5, and
`score`, their product, from 1 to 25. The validator refuses a value outside
the range and a score that is not the product (`E-RSK-002`). It also carries
one `cause` and one `effect`, each one sentence, a `stage` (definition,
architecture, implementation, verification, release or operation), a
`category` (safety, security, compliance, process, schedule or quality) and
the actor that raised it (`E-RSK-001` when one is missing). A risk holds no
question, no options and no decider: those live on the decision.

## Recording a threat

```text
harnessctl raise-risk . --domain <slug> --title TEXT --stage STAGE --category CATEGORY
    --cause TEXT --effect TEXT --likelihood N --impact N --threatens ID [--threatens ID ...]
    --raised-by ACTOR [--with-decision] [--id RISK-...] [--dry-run] [--json]
```

`raise-risk` computes the score, writes the file in `raised` and records the
raise as a lifecycle event, in one act. A measurement outside the range or an
identifier already declared anywhere is refused before anything is written,
exit 2. Anyone may raise a risk: a reviewer, an implementer, or an agent
mid-execution; the raise carries no decision right and grants none. The
`--domain` value is the domain slug (`harness-distribution`) or the identifier
token of exactly one domain (`DST`).

With `--with-decision` the command also writes the decision beside the risk:
an open question with the options `accept`, `avoid` and `mitigate`, naming the
risk and the threatened artifacts in `concerns` and exactly the threatened
artifacts in `blocks`.

## How a raised risk stops work

The risk itself blocks nothing and no gate reads risks. The stop is the
decision family's: while the paired decision is `open`, every transition of
the artifacts it blocks fails the `QGP-*-DECISION` predicate of its gate, and
the refusal names the decision, its three options and the deciding role. A
raised risk must be named in `concerns` by exactly one open or deferred
decision (`E-RSK-003`), and that decision's `blocks` must equal the risk's
`threatens` (`E-RSK-004`). A deferral with a scope lets the admitted
transition pass and leaves the risk `raised`.

## Answering

```text
harnessctl decide . --artifact DEC-... --option accept --revisit TEXT --decision ROLE --reason TEXT --apply
harnessctl decide . --artifact DEC-... --option avoid [--avoided-by ADR-...|DEC-...] --decision ROLE --reason TEXT --apply
harnessctl decide . --artifact DEC-... --option mitigate --mitigated-by WO-... --decision ROLE --reason TEXT --apply
```

Disposing the decision moves the risk in the same act, under the same lock:
`accept` to `accepted`, `avoid` to `avoided`, `mitigate` to `mitigating`, and
a withdrawal to `withdrawn`. The risk's `[disposition]` table repeats the
option, its label, the role, the time and the verbatim reason; a hand-written
one is `E-RSK-005`. Accepting is time-bounded and copies the `--revisit`
trigger onto the risk; when a released version matches that trigger and no
pending decision concerns the risk again, the validator warns (`W-RSK-001`).
Mitigating records `mitigated_by`, the work orders that reduce the threat.
Avoiding records `avoided_by`, one ADR or decision; it defaults to the
disposing decision. A bare `transition` never raises or answers a risk; it
may withdraw one, with a reason.

| State | Meaning |
| --- | --- |
| `identified` | Written by hand from the template and not yet raised. |
| `raised` | Recorded; a pending decision blocks the threatened artifacts. |
| `accepted` | The owner lives with the threat until the revisit trigger. |
| `avoided` | A design change removed the threat. |
| `mitigating` | Work orders reduce the threat; closure waits for verified coverage. |
| `mitigated` | Closed under verified coverage with a residual (`WO-RSK-011`). |
| `withdrawn` | Raised in error; retained. |

## Reading the threats to an artifact

```text
harnessctl risks . --artifact ID [--json]
```

Lists every risk whose `threatens` reaches the artifact or, for a work order,
its governing chain, with the score, the state and the pending decision. It
writes nothing.

## Recording a threat mid-execution

The scope check admits an added risk file of the work order's own domain,
`docs/engineering/<domain>/risks/RISK-<DOMAIN>-NNN.md`, to an in-progress work
order's change set without a declared path. Only an added file is admitted: a
modified or deleted risk file, a risk of another domain, and every other file
still need a declared path. Added-ness is read from Git, so without a checkout
the path must be declared. The decision that `--with-decision` writes is not
covered by this admission; a work order whose scope excludes its own domain
directory declares `docs/engineering/<domain>/decisions/`, or raises without
the flag and pairs the risk with a decision already in scope.

## What is not here yet

Closure under verified coverage (`mitigating -> mitigated` under
`DR-RISK-CLOSE`, `E-RSK-006`, `E-RSK-007`), the derived `[[risks]]` register
on a release record (`E-RSK-008`) and the Explorer's in-flight rows are
`WO-RSK-011`, stacked on this work.
