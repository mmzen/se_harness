# WO-VSP-001 Implementation Verification Evidence

Date: 2026-08-11

Platform: Windows, PowerShell, repository virtual environment

Scope: implementation and non-committing verification authorized by the repository owner with `go implementation`

## Outcome

The bounded implementation satisfies `REQ-VSP-001` through `REQ-VSP-007`. It adds an explicit, typed, human-authorized `ready -> superseded` verification-record lifecycle; prevents unsafe release use; exposes lineage and stale-ready anomalies in the dashboard and Explorer; preserves existing repository behavior; and distributes the same semantics through the standard template and wheel.

No concrete verification record was changed. In particular, `VREC-AGR-001` remains `ready`. No commit, push, pull request, tag, release, publication, or deployment was performed under `WO-VSP-001`.

## Requirement evidence

| Requirement | Implementation | Verification result |
|---|---|---|
| `REQ-VSP-001` | `superseded` VREC status with structured `superseded_at`, `supersession_authorized_by`, and `superseded_by` metadata | valid lifecycle and field-presence tests pass |
| `REQ-VSP-002` | typed, single-successor relation to a distinct `verified` or `released` VREC | wrong type, duplicate successor, and ineligible target tests pass |
| `REQ-VSP-003` | successor work-order superset rule and iterative cycle detection | lost-coverage and cycle tests pass |
| `REQ-VSP-004` | explicit authorizer and timestamp; no automatic lifecycle mutation | structured-field tests and non-mutating stale-ready analysis pass |
| `REQ-VSP-005` | superseded records excluded from release preparation and active release back-references rejected | provenance CLI and active-release validation tests pass |
| `REQ-VSP-006` | old-to-new lineage, inverse `supersedes`, lifecycle class, Explorer details, and derived `W-REV-004` | dashboard JSON, finding, and rendered-label tests pass |
| `REQ-VSP-007` | source/canonical parity, managed-lock refresh, full regression suite, wheel inspection, and fresh installation | all applicable checks pass; two Windows symlink cases skip as documented below |

## Automated verification

Artifact graph:

```powershell
.\.venv\Scripts\python.exe scripts\validate_engineering_artifacts.py --root . --artifact-root docs\engineering
.\.venv\Scripts\python.exe -m se_harness validate .
```

Both commands passed with 102 artifacts, 0 errors, and 0 warnings.

Complete test suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Result: 51 tests passed; 2 tests were skipped because the Windows account lacks symlink-creation privilege. The supersession cases cover valid lineage, structured field rules, ineligible and wrong-type targets, duplicate successors, lost coverage, cycles, active release references, stale-ready findings, Explorer projection, and release-preparation rejection.

Focused provenance suite:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_revision_provenance -v
```

Result: 26 tests passed; 1 symlink test skipped for the same Windows privilege limitation.

CLI and installed-source health:

```powershell
.\.venv\Scripts\python.exe -m se_harness --help
.\.venv\Scripts\python.exe -m se_harness doctor .
.\.venv\Scripts\python.exe -m se_harness dashboard .
```

The CLI help exposed the standard command set. Doctor passed every required, seed, managed, and cross-agent check. After the artifact lifecycle updates, dashboard generation passed with 102 artifacts, 327 relations, 0 blocking errors, and 7 derived warnings; snapshot `92e5de5fe0c327e7a0b9dca3868c24fa51b0d1dc5e455066cafe2ab10273b7e2`.

The seven dashboard warnings consist of six pre-existing `W-REV-001` findings for verified governance work orders without VRECs and the intended `W-REV-004` stale-ready observation. `W-REV-004` identifies `VREC-AGR-001` and possible successor `VREC-PMI-001`, while explicitly requiring a human decision and making no mutation.

Repository hygiene:

```powershell
git diff --check
```

Result: no whitespace errors. Git emitted only the repository's normal LF-to-CRLF checkout notices.

## Distribution and compatibility

The managed lock was refreshed through the supported command:

```powershell
.\.venv\Scripts\python.exe -m se_harness upgrade . --apply
```

The upgrade updated managed content and deliberately preserved the repository-specific `ENGINEERING_HARNESS.md` and `docs/engineering/README.md` customizations for manual review. A subsequent doctor run passed all managed hashes. The full test suite also passed init, adopt, upgrade, customized-file preservation, validation, dashboard, and distribution-metadata regressions.

Source and canonical installed-template SHA-256 hashes match exactly:

| Pair | SHA-256 |
|---|---|
| validator | `192f0b25c1ea186cb94308062405de8339dca638e6de70e6a6ed1ce64dcae1be` |
| dashboard generator | `3b95681e60e79a7acf7036743cfb19ea65846fdc4d4b74be26b9a643b2773183` |
| Explorer HTML | `b7dde5bcdb4a569d90f1f4a6f2bb294234a2ab92b30e90c203a41608b9de12b6` |
| workflow | `99c7014335bbc0d851436ecacdc047d3d837a7c0256cb226c6d262220827ca23` |
| traceability | `e1c45ceda0c3b1db33f3bf0865b62c2f150c8c8907a8f125b3d2f7173426fe1f` |
| VREC template | `a7d49894f9bbc103adb49b30022b23ae99fb286bb5a376d38b7db0c718cfedf` |

Wheel verification:

- File: `C:\Users\mathi\Documents\Codex\2026-08-10\st\vsp-wheel-verification-20260811\se_harness-0.2.0-py3-none-any.whl`
- SHA-256: `3d977448c6ffe3c9503af09e0f51ade3defd39e2e9cd13b30701ef9ba9de87f9`
- Contents: 41 archive entries
- Byte comparison: packaged provenance module, validator, dashboard generator, Explorer template, workflow, traceability, and VREC template all match their repository canonical files.

The wheel was installed into a fresh virtual environment at `C:\Users\mathi\Documents\Codex\2026-08-10\st\vsp-fresh-install-20260811`. Version `0.2.0` initialized a fresh 30-file standard harness; doctor passed. Against a copy of the current engineering graph, the installed validator passed with 102 artifacts, 0 errors, and 0 warnings, and the installed dashboard produced 102 artifacts, 327 relations, and the expected 7 derived warnings including `W-REV-004`.

## Manual and architectural observations

- The generated Explorer was reviewed at its default desktop viewport (1280 x 720) and a narrow viewport (390 x 844). Both layouts remained readable, with no page-level horizontal overflow and no browser console errors or warnings; the narrow question tabs retain their deliberate local horizontal scroller.
- Selecting `VREC-AGR-001` displayed its `active candidate` lifecycle class and the complete supersession detail fields. The inconsistency view rendered `W-REV-004` as a visible derived warning and named `VREC-PMI-001` only as a possible successor requiring human review.
- No concrete repository VREC is currently `superseded`, so historical-record styling was exercised by the rendered fixture assertion rather than by mutating the real graph.
- The validator remains the normative owner of supersession rules.
- Release preparation only reads validated eligibility and rejects `superseded` records.
- Dashboard findings remain derived and non-authoritative.
- Explorer styling separates historical `superseded`, active candidate, and assured records; the detail panel shows successor, inverse predecessor, timestamp, and authorizer.
- Declared graph edges read from the older record to its newer successor.
- No runtime dependency, database, network service, installation profile, or new artifact type was introduced.

## Deviations and residual risks

- Two symlink security tests could not execute because this Windows account lacks the required privilege; the production path-safety code and non-symlink tests remain covered.
- The available virtual environment uses Python 3.14.6; Python 3.11 is declared by package metadata and the implementation introduces no post-3.11 syntax, but this workstation has no 3.11 runtime for a separate execution pass.
- Current-state validation cannot reconstruct unretained prior VREC bytes. Review of the governance diff remains necessary to prove that a real transition changed only permitted lifecycle metadata and narrative while preserving captured provenance.
- Work-set overlap cannot establish accountable intent. `W-REV-004` therefore lists possible successors but never chooses or applies one.
- The current repository still contains the intended anomaly: `VREC-AGR-001` is `ready` while `VREC-PMI-001` covers its work. Resolving it is explicitly outside this implementation authorization.
- Commit-bound independent verification and any transition of `VER-VSP-001` require later governance steps after an implementation commit exists.
