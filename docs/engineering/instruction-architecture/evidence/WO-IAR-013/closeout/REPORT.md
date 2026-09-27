# WO-IAR-013 completion review

Reviewed on 2026-09-27 against SPEC-IAR-014 and VER-IAR-014. This report
records implementation evidence. The released evaluator records completion;
the human makes the later verification decision.

## Delivered scope

The candidate contains the compact root and 25 supporting guides. The retained
source map assigns all 58 headings and 31 main steps. The steps have addressable
headings and the agreed Inputs, Output, Actions, Harness commands, Completion
and Later use fields. The content checks resolve local file and heading links,
preserve every source command operand and reject unresolved review markers.

The root retains the nine named invariants. AUTHORITY.md explains the two
profiles, human-reserved decisions and agent application of recorded decisions.
COMMUNICATION.md is the canonical communication guide. The six legacy guides
are compatibility pointers. EXCEPTIONS.md and AMEND_DEFINITIONS.md state the
unsupported capabilities without inventing commands or waiving gates.

The migration guide contains the separate repository owner-edit map. The
installed AGENTS.md, root instructions and lock still select 0.18.0. This work
does not perform adoption or rewrite accepted history.

## Evidence

- `../../../acceptance/progressive-discovery/source-map.json`: complete source
  heading and step allocation.
- The reading-cost JSON and Markdown beside that map: 21,888 source words,
  1,191 root words and 2,406–5,049 unique instruction words for six complete
  action walks. Formal artifacts are additional inputs; these are not token
  measurements. WO-IAR-015's retained recheck reproduced all counts.
- `../../WO-IAR-014/closeout-focused.*`: current focused run, 90 tests, one skip.
  This includes the source identity, headings, step fields, links, protected
  command operands, discovery and packaging checks.
- `../../WO-IAR-014/closeout/REPORT.md`: shared source identity, full Windows
  and Linux regressions, lifecycle comparison and review results.
- `../../WO-IAR-015/native-acceptance/README.md`: the actual native delivery
  observations and their limits, accepted separately through VREC-IAR-011.

The earlier LF/CRLF source-identity failure and correction remain in
`../ci-correction/`. The fixed assertion normalizes CRLF only. It still refuses
changed content, extra whitespace and bare carriage returns. The later Linux
run passes the assertion. No failed historical observation was relabelled.

## Review conclusion

The split meets the bounded content contract. One root, one set of detailed
guides and one discovery catalogue avoid per-host policy copies. The catalogue
serves exact evaluator-selected identifiers; it does not compute authority.
The added files and link checks serve the agreed discovery requirement.
No further product edit was identified in this completion review.

The old work-order body still contains its original draft-stage wording. Its
applied lifecycle events and evaluator result establish its current state;
this review does not rewrite those historical statements.
