# WO-KIS-006 implementation evidence

Source candidate: `b0405a575e9cd5e7bef12625ec4342c763ed51a5`. Governing evaluator: isolated released 0.17.0.
WO-KIS-006 is implemented through delegated completion. All 18 hosted checks passed; exact URLs are in ci-implementation.json. Owner verification remains pending.

K31 is implemented: new source/release-record runs keep a small summary beside a full CI log. The summary records the command, candidate, actual checker version/origin, outcome, output tail, download command and expiry estimate. CI uploads the artifact even after a test failure. Ordinary result uploads state 14-day retention. Publication bundle evidence keeps its existing durable location.

The full Windows source suite ran **1,096 tests, 16 skipped**, in 131.905s, with four workers and full scale. The exact command is in local-source-summary.json. This is one observation, not a speed comparison. Graph, distribution validation (14 records), CLI help and isolated released review/scope checks passed.

The focused acceptance tests produce a million-byte log and a summary below 6 KB, preserve a nonzero exit code and useful failure detail, and report missing/expired/unreachable raw artifacts as unavailable even when an earlier test passed. A small real Git fixture proves the inventory measures committed bytes, ignores dirty changes, preserves files, and follows VREC references into an RLS.

The real hosted source artifact was downloaded successfully. ci-source-summary.json is the unmodified captured summary; raw-artifact.json records the actual artifact ID, URL and expiry observation. The hosted run tests the PR merge commit shown in that summary; its code was compared with the source candidate. The local run tests the branch candidate shown above. Neither is relabelled as the other.

Raw logs stay outside Git. The retained summary does not promise permanent availability. Use its download command and `python scripts/record_evidence.py check-raw <summary.json>`; missing raw evidence is unavailable, never an inferred pass.

[Archive assessment](archive-assessment.md) measures **232.83 MiB** of historical evidence, 92.9% of a 250.72 MiB committed checkout. The three largest bundles hold 134.67 MiB. The inventory reports bundle sizes and direct VREC/RLS references, including RLS links through VRECs. Indirect sidecars still need review before an archive move. The proposed destination reuses GitHub archive release assets, with original paths, source commit, digests and a tested reader plan. No historical bundle was removed or moved; current readers retain their paths and bound bytes. Existing clones and Git history are not made smaller by this change.

Initial validation caught an exact command-spelling assertion and a missing CI handoff packet. Both were corrected. The first workflow edit also needed a YAML block around the job-summary echo. All final workflow YAML parses. The initial full test failure remains in local raw results; it is not presented as a passing run.

This adds two small repository tools and replaces ad hoc evidence copying with a documented summary/log workflow. It adds no storage service, lock, signature or size gate. Test selection, permissions and publication authority remain as before. Root adoption and owner verification are separate decisions.
