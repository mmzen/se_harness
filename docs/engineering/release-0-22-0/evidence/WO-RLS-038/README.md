# Claude post-release observations for plugin 0.2.5

The tests below passed on 2026-10-03 after authentication was restored.
This supplements the original release evidence. Human mmzen selected
`record-tested-subset` in DEC-RLS-007/008 and approved WO-RLS-038 and VER-RLS-002
with required commit-bound verification. The implementation and evidence are
prepared for that separate human verification; this report supplies no verdict.

## Exact inputs

- Host: Claude Code 2.1.273 on Windows; native model: claude-sonnet-5.
- Plugin: 0.2.5; evaluator: 0.22.0.
- Plugin source: `abbec12ac5524c8adfb28693f846dd59de88f759`.
- Public marketplace: `7d30907f15bd7e06fb632e1ebf4e88e01b68726c`.
- Wheel SHA-256: `44543f242ed19bb30cfd65da415372a87508a6e439204d7f3e37f9f45aefe4e4`.
- Both public routes and the native test package contain the same 29 files.

## Observed coverage

| Check | Result |
| --- | --- |
| Startup above the future checkout | Bootstrap delivered. |
| Clone and exact activation | Complete selected entry delivered; no repository entry copy. |
| Resume from parent directory | Correct session, checkout, release and entry digest restored. |
| Manual compaction | Native manual boundary and complete SessionStart:compact entry observed. |
| Automatic compaction | Native auto boundary and complete SessionStart:compact entry observed. |
| Resume after automatic compaction | Same selection restored. |
| Two sessions and two releases | Interleaved sessions retained independent 0.22.0 and 0.20.0 selections. |
| Switch and clear | Only the selected session changed. |
| Unavailable checkout and recovery | Explicit delivery gap, then exact restored entry. |
| Public fresh installation | Plugin 0.2.5 installed; all 29 files match. |
| Public update | Preserved public 0.2.4 installation updated to 0.2.5; all 29 files match. |
| Fixture preservation | Repository files remained unchanged by instruction delivery. |

Native runs loaded the exact package through `--plugin-dir` in the authenticated
test profile. Public install/update ran separately in disposable profiles. File
identity connects those observations; this is not a claim that every installed
profile was exercised in an authenticated workflow. The synthetic compaction
workload used a 100,000-token automatic-compaction window and tools disabled.

## Follow-up to existing records

| Existing records | Recorded follow-up | Remaining coverage |
| --- | --- | --- |
| RISK-RLS-004 / DEC-RLS-005 | DEC-RLS-007 records mmzen's decision to retain the exact tested native subset. | Full Claude work-order walkthrough, long-path scenario and Codex desktop. |
| RISK-RLS-005 / DEC-RLS-006 | DEC-RLS-008 records mmzen's decision to retain the exact public fresh/update results. | Codex desktop and any broader native/workflow claim. |

The accepted risks are not closed. The original decisions, release records,
verification records and failure evidence remain unchanged. The earlier expired
OAuth observation remains historical failure evidence; current authentication
worked for these runs. There is no guarantee that it will remain valid later.
RISK-RLS-006 and earlier plugin 0.2.4 deviations are unaffected.

## Evidence and next work

[observations.json](observations.json) contains identities, results, original-record
hashes and the complete archive index. [observations-raw.zip](observations-raw.zip)
retains the original traces, command receipts and transient test drivers without
rewriting them. Earlier driver authorization labels are historical labels; this
rerun and retention follow the later human requests recorded in the index.

mmzen owns the remaining cases. Revisit them before the next plugin release or
a broader support claim. The [verification review](verification-review.md)
maps the retained checks to VER-RLS-002. Current guidance links this supplement;
human verification of its exact candidate remains a separate decision. This
evidence does not alter the release's delivery plan or prior human acceptance.
