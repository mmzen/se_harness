# WO-PLG-018 integration evidence

**Implementation in progress; full hosted acceptance remains pending.**

The operator-approved [amended plan](plan-main.json) pins main
`fc1f087371b100d5fda7a1f254ee00ebde8cbadf` and five source heads. Its SHA-256 is
`eb0fa0a8e8e5e77428f45fdcde3c99f2080c318bdcb75a6425216081002feefb`.
The exact #446 and #444 commits were merged with their ancestry intact.

## Preservation and failure checks

All 3,177 imports match the planned modes and blobs. All five source heads and
four previous VREC candidates remain ancestors. A separate inspection read all
446 selected evidence files at their bound commits. Original WOs stay implemented;
VREC007/009/010 stay verified and VREC008 stays ready.

The checker and its 22 synthetic tests passed on Windows/Python 3.14 and
Linux/Python 3.12. Tests reject changed payloads, modes, records, scope, ancestry,
evidence and plan digests; they exercise replacement refs and read-only behavior.
The actual checker passed on both platforms against a reachable-history-only
copy of assembly `90f6cb082e7eb5171f772b5e761a7010b4623e42`. That copy lacks the
preview tree object. Expected tree hashes are derived from the approved inputs.
The committed checker also passed at `001f60fc294844c2bef9ad959992b89b141a54c6`.

The tests ran before their unchanged files were committed at `001f60fc`; their
logs correctly retain the preceding HEAD. Source SHA-256 values are:

| File | SHA-256 |
| --- | --- |
| check.py | `7165a36582780d8bc276537bb803547a414ab3cd512730982eac04110c0ab11a` |
| test_check.py | `abada3b5f5398276301633d3c2316096e5e38b9ad56996e352493c08cfd08148` |

## Hosted and governing checks

Hosted acceptance is pending. At `001f60fc`, source and package checks passed, but managed validate failed because the required handoff packet was missing (QGP-G4I-EVIDENCE). Its log is retained; other unfinished or unavailable results are not passes.

Released 0.17.0 integrity, graph, review and Git-derived scope checks passed.
Source CLI help and distribution validation passed (14 distribution-bearing
records). Candidate-source doctor returns failure for the documented 0.18
source-template versus managed 0.17 mismatch. AGENTS.md assigns the governing
verdict to the external released evaluator; no managed file was overwritten.

## Preserved history and limits

VREC007 has one already-recorded post-candidate handoff refresh. VREC008 has
two later explanatory/receipt changes. Their original bytes remain readable at
their bound commits; the imported current bytes remain exactly pinned. VREC009
and VREC010 selected evidence matches their candidates. No record is rebound.

Development observations include the corrected Windows read-only-object test
fixture and three local clone transport ownership failures. A reachable-only
Git bundle provided the clean-copy test without changing global Git trust.
These observations are retained alongside the successful runs.

The implementation tree at `001f60fc` has 9,971 entries before this evidence.
The actual completed candidate and final governance tree must both remain within
10,000. Existing host-qualification limits remain; this work adds no live-host
qualification, assurance, release, supersession or external merge authority.

## Read or repeat the checks

[raw-index.json](raw-index.json) identifies every member of [raw.zip](raw.zip)
by size and SHA-256. The archive preserves commands, results and CI observations;
it contains no complete repository export. Run `python -B
tests/plugin_integration/stack-integration/test_check.py` for the synthetic cases.
Run `check.py --help` for the four explicit verification inputs. Supply the
approved plan digest from the approval record, never a newly calculated approval.
