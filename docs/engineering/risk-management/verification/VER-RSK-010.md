+++
id = "VER-RSK-010"
type = "verification"
title = "Independent evidence for the risk artifact and its borrowed stop"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[relations]
verifies = ["REQ-RSK-010", "REQ-RSK-011", "REQ-RSK-012", "REQ-RSK-013", "REQ-RSK-014", "REQ-RSK-015", "REQ-RSK-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:49:30Z"
decided_by = "assurance-owner"
reason = "Approved by the accountable owner on 2026-09-07, by selecting the presented option in the ratified decision channel. The evidence contract covers all seven requirements with an independent reading."
+++

# Verification Contract: Independent evidence for the risk artifact and its borrowed stop

## Independence

Expected values come from `SPEC-RSK-010`'s rules and from `SPEC-DCM-001`'s
existing stop, never from candidate output. Two cases in particular are stated
against the contract and not against the code: the refusal text a threatened
artifact receives must name the decision, and the absence of a new predicate is
asserted against the two quality-gate contract copies, by comparing their
predicate identifier sets with the sets on `main`. Every score expectation is
computed by hand in the case, not read back from the artifact.

The governing reading is the exact released evaluator named in
`.engineering-harness.toml`, run with `-I` from a virtual environment outside the
checkout. An in-tree run is a control and never the record.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-RSK-010` | test | a risk fixture per boundary: likelihood 0, 1, 5, 6; impact 0, 1, 5, 6; score disagreeing by one | in-range fixtures draw no finding; every out-of-range or disagreeing fixture draws `E-RSK-002` naming the field |
| `REQ-RSK-010` | test | a fixture missing each of the eight required fields in turn | each draws `E-RSK-001` naming the missing field, and no other code |
| `REQ-RSK-010` | inspection | the `risk` row of the artifact catalog and the `risks/` entry of the layout registry | both name the type, prefix and directory of RSK-MGT-001 |
| `REQ-RSK-011` | test | `raise-risk` run twice in a fixture repository, once valid and once with likelihood 6 | the first writes one file in `raised` with the hand-computed score; the second writes nothing and exits 2 |
| `REQ-RSK-011` | analysis | a search for a configuration reader of any raise threshold across the package and both template trees | no reader exists, and the installed template still declares five keys |
| `REQ-RSK-012` | test | a raised risk with a paired open decision; the threatened work order asked to transition | the refusal names the decision identifier, its options and the deciding role, and does not name the risk |
| `REQ-RSK-012` | test | a raised risk with no decision, and one whose decision blocks a different set | `E-RSK-003` and `E-RSK-004`, each naming both sets or the corrective command |
| `REQ-RSK-012` | analysis | the predicate identifier sets of `se_harness/quality_gates_contract.json` and the template copy, against `main` | the sets are equal; no identifier is added or removed |
| `REQ-RSK-013` | test | `decide --apply` on the paired decision, once per option: accept, avoid, mitigate | the decision and the risk both move in one act; the risk's disposition repeats option, role, time and reason verbatim |
| `REQ-RSK-013` | test | a risk with a hand-written `[disposition]` and no lifecycle event | `E-RSK-005` |
| `REQ-RSK-013` | test | `decide --defer --scope … --revisit …` on the paired decision | the risk stays `raised`; the threatened artifacts stay blocked outside the scope |
| `REQ-RSK-014` | test | closure attempted with the mitigating work order at `implemented`, then at `verified` | the first is refused with the work order named and nothing written; the second writes `mitigated` |
| `REQ-RSK-014` | test | a stored `mitigated` risk whose coverage or residual is absent | `E-RSK-006` and `E-RSK-007` respectively |
| `REQ-RSK-014` | analysis | the decision-rights catalog before and after | exactly one row is added, `DR-RISK-CLOSE`, held by the assurance owner, and no disposal right for a risk exists |
| `REQ-RSK-015` | test | scope and handoff checkpoints on an in-progress work order whose change set adds one risk file its paths do not admit | both pass, and the admitted path is the risk file only |
| `REQ-RSK-015` | test | the same change set plus one unrelated file, and a change modifying an existing risk file | each fails, naming only the offending path |
| `REQ-RSK-016` | test | a release prepared over work with one accepted, one mitigating and one raised risk, and one unrelated risk | the register carries exactly the three reachable rows with score, status, revisit and residual |
| `REQ-RSK-016` | test | a prepared record with one row deleted and one added by hand | `E-RSK-008` in both directions |
| every requirement | test | each rule identifier from RSK-MGT-001 to RSK-MGT-035 cited by at least one case | the citation map is complete, and RSK-MGT-036 holds for each: the case fails on the code before its change |

## Acceptance scenarios

1. A threat recorded mid-execution. An in-progress work order's implementer runs
   `raise-risk --with-decision`; the scope checkpoint still passes; the work
   order's handoff is refused, naming the decision; the engineering owner disposes
   it with `accept` and a revisit trigger; the handoff then passes and the risk
   reads `accepted` with the owner's words.
2. A threat that is mitigated. The same risk disposed with `mitigate` names a new
   work order; closure is refused while that work order is `implemented`; after
   its record is `verified` and a residual is recorded, closure succeeds.
3. A threat carried into a release. A release record prepared over that work
   lists the accepted risk with its score and residual, and refuses when the row
   is removed by hand.
4. A threat withdrawn. A risk raised in error is withdrawn together with its
   decision; the threatened artifacts move; both files are retained.

Each scenario is run end to end from the released evaluator, and the refusal
text of every blocked step is retained verbatim.

## Property and invariant tests

- For every generated risk with likelihood and impact in range, the stored score
  equals the product, and no risk exists whose stored score is accepted while
  disagreeing.
- No risk state other than the six declared states is reachable by any command.
- For every risk in `raised`, exactly one decision in `open` or `deferred` names
  it in `concerns`.
- The derived release register is a function of the graph alone: preparing twice
  from the same commit produces identical bytes.

## Static and architecture checks

- No predicate identifier is added to either quality-gates contract copy
  (ARCH-RSK-010 conformance check 1).
- The risk schema declares no `question`, `options`, `recommendation` or decider
  field (conformance check 3).
- `se_harness/decisions.py` gains no import of the risk module; the dependency
  runs one way only.
- The installed configuration template still declares exactly five keys, and
  `tests/test_configuration_surface.py` passes unchanged.

## Security and privacy checks

- A risk whose `cause`, `effect`, `title` or `residual` contains Markdown,
  a shell fragment or a control character is rendered as text in the refusal, the
  Explorer and the release register.
- The raise carries no authority: a raise by an actor holding no decision right
  succeeds, and the same actor's attempt to dispose or close is refused with no
  change.
- A risk identifier crafted with path components is refused by `raise-risk`.

## Performance and resilience checks

- The graph read cost does not change materially: the artifact count of this
  repository plus the fixture risks is validated within the existing budget, and
  the reading is recorded on both platforms.
- `decide --apply` interrupted between the decision write and the risk write
  leaves neither file half-written; the act is applied under one lock and is
  re-runnable.

## Manual assessments

- The assurance owner reads the four acceptance scenarios' retained refusal text
  and confirms that a reader can tell, from the refusal alone, what is blocked,
  who answers and how.
- The technical owner confirms against `ARCH-RSK-010` that no prohibited pattern
  appears.

## Evidence retention

One evidence packet per work order under
`docs/engineering/risk-management/evidence/`, holding the rule-to-case citation
map, the verbatim refusal text of every blocked step, the predicate-set
comparison against `main`, the decision-rights diff, the derived register bytes,
and the governing readings with their commands, platforms and evaluator version.
Readings are labelled per platform; the hosted Linux lane is the record and the
local Windows run is a control.

## Residual uncertainty

The pairing rule between a risk and its decision is new and its ergonomics are
unproven; the evidence records how many raises trip `E-RSK-003` during the work
itself. Whether owners answer threats within the intent's seven-day measure
cannot be verified here and is observed in operation. No case here proves that
the absence of a raise threshold is the right policy; that is a judgement the
architecture records and a later amendment may revisit.
