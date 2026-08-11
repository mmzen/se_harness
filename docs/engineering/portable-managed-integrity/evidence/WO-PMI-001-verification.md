# Verification Evidence for WO-PMI-001

Date: 2026-08-11

## Scope and authority

The accountable repository owner accepted the portable managed-integrity packet and `WO-PMI-001` with the instruction `ok accepted`, then explicitly requested implementation with `go implementation`. This evidence records bounded implementation and verification only. No commit, push, pull request, verification transition, release record, tag, package publication, or deployment was authorized or performed.

## Implemented behavior

- Added one standard-library integrity component for strict lock parsing, schema validation, legacy digest reproduction, `utf8-text-lf-v1` canonicalization, SHA-256 generation, and typed comparisons.
- New init, adopt, and fully safe upgrade outcomes write deterministic schema-2 locks declaring `sha256` and `utf8-text-lf-v1`.
- LF, CRLF, CR, mixed line endings, managed files, and managed fragments use the same schema-2 canonical rule while final-newline presence and every non-terminator content distinction remain significant.
- Doctor now validates managed fragments and seed state, recognizes conservative schema-1 exact or desired-canonical matches, rejects stale schema-2 entries, and remains read-only.
- Upgrade treats canonical desired equality as unchanged, preserves actual or ambiguous customizations, reproduces historical schema-1 fragment CRLF semantics, and migrates safe evidence without rewriting newline-only differences.
- Strict lock validation rejects duplicate JSON keys, boolean or unknown schemas, unsupported algorithms or modes, invalid entry modes, invalid seed states, and malformed digests.
- The self-repository lock was regenerated through `harnessctl upgrade . --apply` as schema 2; all 28 tracked entries pass doctor, including the formerly stale validator entry.
- Root and canonical workflow documentation describe the portable integrity and legacy-migration contract; the wheel contains the shared component and updated standard template.

## Requirement evidence

| Requirement | Evidence | Result |
|---|---|---|
| REQ-PMI-001 | Independent LF/CRLF/CR vectors, final-newline and content-sensitivity tests, invalid UTF-8 rejection | PASS |
| REQ-PMI-002 | Schema-2 doctor on managed file and fragment after CRLF conversion, both in unit fixtures and a fresh wheel installation | PASS |
| REQ-PMI-003 | Full-file customization, managed-block mutation, owner text outside blocks, malformed markers, and preservation assertions | PASS |
| REQ-PMI-004 | Schema-1 exact, historical fragment, desired-canonical, ambiguous customized, missing-entry, and schema-2 migration cases | PASS |
| REQ-PMI-005 | Static call-site review and shared integration across lock loading, writer, installer, upgrade, and doctor | PASS |
| REQ-PMI-006 | Self-lock regeneration, source/canonical parity, final wheel inspection, fresh install, CRLF doctor, upgrade, and validation | PASS |
| REQ-PMI-007 | Complete installer and provenance regressions, path and symlink checks, unchanged CLI surface, no Git or authority actions | PASS |

## Commands and outcomes

### Artifact graph

```powershell
python scripts/validate_engineering_artifacts.py --root .
```

Result: PASS. 84 formal artifacts, 0 errors, 0 warnings.

### Automated test suite

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Result: PASS. 45 tests ran successfully; 2 of them were conditionally skipped because this Windows host lacks symbolic-link privilege. The 25 installer/doctor tests include canonical vectors, schema validation, migration, fragment, stale-lock, customization, path, install, adopt, upgrade, and distribution behavior.

### CLI and source-repository diagnostics

```powershell
python -m se_harness --help
python -m se_harness doctor .
```

Result: PASS. The existing command surface loaded, Python 3.14.6 satisfied the Python 3.11-or-later contract, and every one of the 28 self-lock entries passed under schema 2.

### Supported self-lock migration

```powershell
python -m se_harness upgrade .
python -m se_harness upgrade . --apply
```

The plan reported 28 unchanged tracked paths and two intentional repository-specific customizations, `ENGINEERING_HARNESS.md` and `docs/engineering/README.md`, that had no legacy lock entries. Applied upgrade preserved both files and returned the existing manual-review status, while safely writing a schema-2 lock for the 28 proven entries. Subsequent doctor passed. No hash was hand-entered.

### Source and canonical-template parity

Raw SHA-256 equality was confirmed for:

- `docs/engineering/WORKFLOW.md` and its canonical standard-template copy;
- the artifact validator and its canonical copy;
- the Harness Explorer template and its canonical copy.

Result: PASS.

### Final wheel

```powershell
python -m build . --wheel --no-isolation `
  --outdir C:\Users\mathi\Documents\Codex\2026-08-10\st\wheel-verification-pmi-final
```

Result: PASS. The wheel contains 41 entries, including `se_harness/integrity.py`, the integrated installer and CLI, and the updated canonical workflow.

Wheel: `C:\Users\mathi\Documents\Codex\2026-08-10\st\wheel-verification-pmi-final\se_harness-0.2.0-py3-none-any.whl`

SHA-256:

```text
dae75a4940e515e10fc6967bcebb8691e70b65b93fe1e2329df23490e2e9335f
```

### Fresh wheel installation and CRLF smoke

The final wheel was installed without dependencies into a fresh virtual environment. `harnessctl init` created the complete 30-file standard harness with schema 2 and `utf8-text-lf-v1`. `docs/engineering/WORKFLOW.md` and the managed block in `AGENTS.md` were converted from LF to CRLF.

Results after conversion:

- `harnessctl doctor`: PASS for every managed file and fragment.
- `harnessctl upgrade`: PASS, 30 files unchanged and no rewrite planned.
- `harnessctl validate`: PASS, 0 errors and 0 warnings in the empty initialized artifact graph.

### Diff hygiene

```powershell
git diff --check
```

Result: PASS. Git emitted only LF-to-CRLF checkout notices and no whitespace errors.

## Deviations and residual risks

- Direct Python 3.11 execution was not assessable because it is not installed on this host. Python 3.14.6 satisfies the declared version range, and the implementation uses Python 3.11-compatible standard-library syntax.
- Two symlink tests remain conditionally skipped due host privilege; no symlink handling was changed.
- Ambiguous schema-1 mismatches intentionally remain manual review because the original bytes cannot be reconstructed safely from a digest.
- The source repository intentionally leaves `ENGINEERING_HARNESS.md` and `docs/engineering/README.md` outside managed lock entries; upgrade continues to report and preserve them rather than asserting ownership.
- `VREC-AGR-001` remains `ready` and names the earlier aggregate candidate. After a separately authorized corrected candidate commit, a new aggregate verification record must cover both `WO-AGR-001` and `WO-PMI-001` with `VER-AGR-001` and `VER-PMI-001`; no existing commit binding may be rewritten or approved implicitly.

## Authority boundary

The implementation is locally verified evidence for `WO-PMI-001`. It does not verify a VREC, approve release scope, create a release, mutate Git history, publish the wheel, or authorize deployment.
