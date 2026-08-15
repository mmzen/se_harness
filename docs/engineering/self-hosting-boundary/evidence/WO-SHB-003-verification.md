# Verification evidence for WO-SHB-003

Date: 2026-08-15

## Accountable assurance decision

The accountable repository owner explicitly instructed `ok i validate the verification record` after reviewing `VREC-SHB-001`, then reported `merged` after the exact candidate and unchanged ready record entered `main` through pull request 40 with the required hosted checks green. The implementation agent had withheld the transition until those objective prerequisites were satisfied. These human instructions authorize this separate `ready -> verified` decision; automation only records and checks it.

## Reviewed lineage and retained evidence

- Candidate commit: `94ef1ac10420d79c61aa43c916d2a1bae15d650a`.
- Candidate tree: `0eecad9dcee61929076559ae961bd4b0842fd59b`.
- Ready-record governance commit: `a3f708f658326e60aa4592fc09336a9f84b90b54`.
- Ready-record and merged tree: `4eec400dbdc7060307ff58587e4d53c9f0707397`.
- Pull-request merge commit: `a89f67f`.
- Covered work order: `WO-SHB-002`.
- Verification contract: `VER-SHB-002`.
- Captured artifact snapshot SHA-256: `d74924829798300bddaa635ef52e769535ddbc882f3d05913749bbc42f0fe026`.
- Ready VREC SHA-256 before transition: `6b1e3624fe4b90cc4dc536ab83ebfd7d5c25005be4a64370c1a54ecfa71acc4e`.
- Retained `WO-SHB-002` evidence SHA-256: `8c984bf83b85827b2f378b5d3df57f609d27c88ecb256346fc709d69ce097885`.
- Exact candidate wheel SHA-256: `94f1c0a96769312691453ab8b1b1b71bde35955f0ff71f5029b1712fde43b197`.
- Repeated canonical acceptance-manifest SHA-256: `af126d5c62596aa931a740f615294adc92fce418c43b42fc95d9f440e55ef62a`.

The candidate, ready-record, and merge commits exist. Ancestry and captured-field preservation are rechecked below before the transition is retained.

## Pull-request and hosted-CI state

Pull request 40 merged the exact ready-record head. Its first pull-request selection attempt exposed CRLF line endings in the PR body's standalone `Harness-Work-Order` declaration. The candidate source and VREC were not changed. The PR body alone was normalized to LF and the PR was closed/reopened to request a fresh evaluation. Run `31877197027` then passed `Released governor`, `Candidate source`, and `Candidate package`; the candidate-package plane included the exact-governor-to-candidate upgrade acceptance outside the checkout. GitHub's final PR check report listed all six reported job instances as passing.

The metadata interoperability defect is retained as an observation, not silently attributed to the payload. General CRLF normalization in the selector is a separate potential work item and is not implemented by this governance transition.

## Local commands and results

| Check | Result |
| --- | --- |
| `python -B scripts/validate_engineering_artifacts.py --root .` | PASS: 296 artifacts, 0 errors, 38 classified historical warnings |
| candidate-source `python -B -m se_harness doctor .` | PASS: required, distribution, managed, and self-hosting integrity checks passed; 9 existing canonical-location advisories remained nonblocking |
| candidate-source start preflight for `WO-SHB-003` | PASS in both `approved` and `in_progress`; complete governing manifest inspected |
| installed released-governor 0.2.1 start preflight | Expected cross-version refusal: one `I001` reports the post-0.2.1 Explorer asset differs from that release's packaged distribution; no write occurred and this result was not treated as candidate-semantic assessment |
| `python -B -m unittest tests.test_self_hosting_boundary -v` | PASS: 24 tests |
| `python -B -m unittest discover -s tests -p "test_*.py"` | PASS: 160 tests, 3 conditional skips |
| deterministic Explorer generation to two explicit external outputs | PASS twice: 296 artifacts, 1060 relations, 0 errors, 46 derived warnings, identical snapshot `5d0376f198a226c19dfb270cc539110263080d1e58c8d5ee1fab888fc7110558` |
| candidate, ready-record, and merge ancestry | PASS |
| ready/verified VREC hashes, captured-field preservation, and bounded VREC diff | PASS |
| candidate-source review preflight, CLI help, `git diff --check`, and final three-path scope | PASS |

The released governor remains the independent authority for stable facts that its published contract understands. It cannot parse or bless work-order semantics and managed distribution content introduced after release 0.2.1. Candidate-source checks therefore supply explicitly labelled candidate evidence, while pull request 40's released-governor, candidate-source, and candidate-package planes keep those roles separate.

## Transition integrity

The verified VREC SHA-256 is `33a18ae8f39ff22b849d20cbe2466b0da9f31f5ff9c4d4f5cd1fbd2c4266bdb2`. The VREC diff changes only:

- front-matter status from `ready` to `verified`;
- the heading from candidate to verified record;
- pending-review wording to the owner's dated decision, merged PR, and this governance work order;
- the preservation statement; and
- the final bootstrap paragraph from gates remaining required to those gates having been satisfied.

The following captured values remain textually unchanged: candidate `94ef1ac10420d79c61aa43c916d2a1bae15d650a`, `sha1` object format, clean worktree state, timestamp `2026-08-15T09:23:57Z`, artifact snapshot, evidence path, `WO-SHB-002` relation, and `VER-SHB-002` relation. No release relation, new payload, version, tag, or governor selection was introduced.

## Authority boundary and residual risks

This decision verifies only `VREC-SHB-001`. It does not independently verify this governance work order, release or publish the payload, reconcile or promote a governor, change a protected control, merge this pull request, create or move a tag, deploy, force push, or rewrite history.

GitHub Actions reported nonblocking Node.js 20 deprecation annotations for action versions forced to Node.js 24. The CRLF-sensitive work-order selector remains a known metadata risk until separately corrected. Neither condition changes the reviewed candidate identity or this bounded assurance decision.

The final governance diff is limited to `VREC-SHB-001`, `WO-SHB-003`, and this evidence file. The formal warnings are pre-existing legacy architecture and canonical-location compatibility findings; Explorer warnings are derived observations and do not grant or remove authority. Three complete-suite tests remain conditionally skipped on this Windows host.
