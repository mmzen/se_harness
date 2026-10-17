# WO-ECP-007 verification assessment

The selected result removes the viewer's repository-ID exception, detects its
return in executable wheel members, and explains and tests Git readiness after
minimal installation. The assessment covers REQ-ECP-012 and REQ-ECP-013 under
the activated SPEC-ECP-007 and VER-ECP-007 revisions.

## Evidence applicability

The final verification record binds one exact clean candidate and the evidence
listed in that record. Qualification ran against source commit
`49b4f3fb7715d42d8c096a3fdcc57ca4bc7d2e71` and wheel SHA-256
`57bfed79d107021fb0ea3136709cf71edf57ef0db497de87719cb78d92daaaf7`.
The [input comparison](input-equivalence.json) records unchanged package, build,
test and harness-selection inputs. Later work records the authorized statement
correction, lifecycle results and evidence. The old observations keep their
original source identity; they are not relabelled as newly executed tests.

The statement correction aligns the accepted requirement with the installation
choice already exercised by both platform demonstrations. The
[correction receipt](definition-revisions/2026-10-17/statement-correction.json)
retains the actual human decision and the preserved first revision. The
initial activation receipt and its seven original accepted versions are intact.

## Requirement and criterion results

| Selected criterion | Assessment | Evidence and reason |
| --- | --- | --- |
| REQ-ECP-012: two-file default and owner preservation | Passed | Installed-wheel demonstrations on [Windows](qualification-2026-10-17/installed-consumer-windows.json) and [Linux](qualification-2026-10-17/installed-consumer-linux.json) check exact initial file sets and unchanged owner bytes. |
| REQ-ECP-012: missing Git evidence attributes fail before evidence exists | Passed | Both platform reports record exit 1 and `hash-bound-attribute-effective`, while the artifact directory remains absent. |
| REQ-ECP-012: explicit Git integration or an equivalent owner rule permits doctor | Passed | Both modes commit their selected attributes and produce doctor exit 0 on each platform. |
| REQ-ECP-012: damaged attributes remain a named failure | Passed | Both modes append an overriding attribute rule and require exit 1 with the named attribute check. |
| REQ-ECP-013: ID-independent viewer selection | Passed | The actual wheel's component produces the expected four ID/status outcomes on [Windows](qualification-2026-10-17/packaged-viewer-windows.json) and [Linux](qualification-2026-10-17/packaged-viewer-linux.json). An unrelated verification record is not selected. The regression fails against the old viewer. |
| REQ-ECP-013: built wheel and generated executable UI exclude forbidden literals | Passed | The exact wheel passes the scanner on both platforms. Its viewer bytes equal the tested source. The raw scan commands and both wheel inventories are retained. |
| REQ-ECP-013: contaminated members fail with location; permitted references pass | Passed | Four independent contamination cases cover Python, JavaScript, HTML and JSON. Clean content, historical Markdown and METADATA references pass. These cases run in both affected-module suites. |
| VER-ECP-007: deterministic generation | Passed | Two generated outputs and the checked-in template have SHA-256 `694b643b80f3a72d760343f255eca6388a36682cbe8a44eda7f2e07240d16c92`; builder check passes. |
| VER-ECP-007: preserve historical bytes and existing product boundaries | Passed | The [preservation report](preservation.json) covers 12,475 prior evidence paths, unchanged retained design exports and seven byte-exact accepted definitions. The source suite retains retirement, lock-floor, archive and qualification checks. |
| VER-ECP-007: initialization and doctor within 60 seconds | Passed | Each measured command is below 1.3 seconds on Windows and 0.4 seconds on Linux. |
| Required repository checks | Passed | Full-scale Windows run: 1,349 tests, 24 skips; affected Linux modules: 120 tests, no skips. Distribution validation covers 24 records; CLI smoke and package checks pass. |
| REQ-ECP-014 and unrelated skill qualification | Outside selected scope | The approved revision explicitly preserves these obligations for other work. No new skill-qualification claim is made. |

## Review and limits

The [implementation review](README.md) records the resolved statement omission,
the minimal builder/checker changes and the test setup corrections. Original
failures and later successful runs remain in the
[transcript archive](qualification-2026-10-17/transcripts.zip), with
[commands](qualification-2026-10-17/commands.json) and a
[byte inventory](qualification-2026-10-17/transcript-index.json).

Windows' 24 full-suite skips are not passes. All selected cross-platform
acceptance scenarios were executed. Linux qualification uses Ubuntu 24.04 under
WSL2; no full Linux suite or native-agent/desktop qualification is claimed.
The static scanner covers the approved literal form `[A-Z]+-SEH-[0-9]+`; it is
not a general proof against every encoded special case. The behavior tests
cover the known viewer defect.

No unresolved finding remains in the selected acceptance criteria. Human
verification, merge, release and adoption are separate from this assessment.
