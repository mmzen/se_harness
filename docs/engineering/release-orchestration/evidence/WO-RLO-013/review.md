# Review of the release-record selector correction

Human mmzen approved WO-RLO-013 and VER-RLO-010 with required commit-bound
verification. Released 0.20.1 recorded the approvals and start. The two-file
implementation matches that scope.

The replay now scans the same canonical formal-record locations as the existing
publisher. It excludes non-files and file symlinks and keeps the exact-one-match
rule. Status, distribution, candidate, recipe and accepted-hash checks are unchanged.
The general distribution scanner is unchanged. No portable evaluator or plugin
file imports this correction. No new framework or workflow was introduced.

The added regression cases reproduced the duplicate-copy failure and evidence-only
false acceptance before the fix. After correction, all 28 release-build tests pass
on Linux. Windows passes with three platform skips, including symlink creation;
the new symlink boundary is exercised on Linux. The full Windows suite passes
1,215 tests with 21 skips. Distribution validation passes for 20 records.

The real RLS-SEH-030 selector returns only its formal releases/ record. Its
SHA-256 and the archived copy's SHA-256 both remain
29e700835b097dde4050bc648dcb9582db1712b265f088b09abdabaad9d89a34.
The original hosted failure remains retained. A corrected hosted rehearsal is
still required before work completion and verification preparation.

This is repository replay-tool work with separate assurance. REL-SEH-033's
thirteen wheel release members are unchanged. WO-RLS-031's desktop criterion
remains unverified. No final release verification, release decision, publication,
marketplace update, adoption or instruction deletion is implied.

The first combined PR check required a current handoff header (QGP-G4I-EVIDENCE).
The released evidence command wrote the required headers at the approved paths.
The original refusal and correction remain in the preparation receipts. Header
creation does not supply the pending hosted replay or a completion decision.
