+++
id = "VER-ECP-025"
type = "verification"
title = "Verify wave 2: one primitive per family and the wired contract tables"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-ECP-034"]
+++

# Verification Contract: Verify wave 2: one primitive per family and the wired contract tables

## Independence

Expected values come from `REQ-ECP-034` and the rules of `SPEC-ECP-023`;
the copy counts and the seven duplicate blocks are those the assessment of
2026-09-07 recorded, and the before-and-after readings are compared with
them. Every digest expectation is read from `main`, a committed record or
an existing test pin, never from the changed code.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-034` launcher | test: `_process.run_git` with `git` absent from `PATH`, with a timeout of zero, with output over the cap; grep of `subprocess.run` in the package and tools | one launcher; each caller's exception type raised with the command named; no direct launch outside `_process.py` (`ECP-PRM-001` to `-003`) |
| `REQ-ECP-034` front matter | test: an artifact with a BOM, with CRLF, with a lone CR, with an unanchored `+++` in the body; grep of `"+++"` | one parser; every fixture parses as on LF; no split outside `front_matter.py` (`ECP-PRM-004`, `-005`) |
| `REQ-ECP-034` integrity | test: `canonical_json_bytes` and `pretty_json_bytes` on the package's and the tools' fixtures with both `ensure_ascii` values; `atomic_write_bytes` interrupted after staging; grep of `hashlib.sha256`, `sort_keys=True`, `object_pairs_hook`, `os.replace`, `"\r\n"` | one home; bytes equal the pre-change bytes for every caller; the target is untouched after an interrupted write; the greps name `integrity.py` and its re-export only (`ECP-PRM-006` to `-010`) |
| `REQ-ECP-034` closed sets and grammars | test: the checkpoint and definition-type sets imported from `workflow_contract.py`; a pre-release wheel through both `qualify` roles; the environment builder's output | one definition each; both roles agree on every fixture wheel; `PYTHONPATH` absent and user site disabled in every launch (`ECP-PRM-011` to `-015`) |
| `REQ-ECP-034` codes | test: every constant of `codes.py` appears in the committed diagnostic-code page; grep of `WEX`, `MG0`, `RID0`, `CC0`, `CP0`, `RR0` literals in the package | no literal outside `codes.py`; `CodedError` exposes `code` and `message`; the regenerated page equals the committed one (`ECP-PRM-016` to `-018`) |
| `REQ-ECP-034` declarative sections | test: each section removed or malformed in a throwaway copy; `gate_source`, `mutation_guard`, `workflow_result` and the aggregator read from the loaded contract | each loader refuses with one code; the Python copies are gone; behaviour on the unchanged contracts equals `main`'s (`ECP-PRM-019` to `-023`) |
| `REQ-ECP-034` digests | the release-qualification, hash-bound, installer and evidence suites; a replay of the bound recipe of `RLS-SEH-025`; `CONTRACT_SHA256` | every recorded digest equals `main`'s; the replay reproduces `a969d6ab…` (`ECP-PRM-024`, `-025`) |
| `SPEC-ECP-023` records | inspection | every amendment record `ECP-PRM-026` requires is present, dated and names the specification |
| `REQ-ECP-034` duplication and regression | `pylint --enable=duplicate-code` in a scratch environment, before and after; the full suite; `validate`; `doctor`; the hosted lanes | none of the seven blocks; suite at its baseline; graph 0 errors; every lane green (`ECP-PRM-027`, `-028`) |

## Acceptance scenarios

- Run the duplication scan on `main` and on each group's candidate; record
  both readings in the group's evidence.
- Replay the bound recipe of `RLS-SEH-025` on the group B candidate and
  compare the wheel and sdist digests with the record.
- Damage each declarative section in a throwaway copy and observe the
  refusal code at the process boundary.

## Evidence retention

One evidence packet per work order under
`docs/engineering/execution-control-plane/evidence/`, holding the scan
readings, the digest comparisons, the suite reading, `validate` and `doctor`
readings and the hosted lane ids.

## Pass criteria

Every row of the matrix passes for every group; the pull requests' lanes are
green through completion and the record heads; no managed path moves.

## Residual uncertainty

The duplication scan runs in a scratch environment on this workstation and
in the Linux lane only if the executor adds it to a job; the suite and the
digest pins are the record. The engine's copies remain by design until wave
3 (#378).
