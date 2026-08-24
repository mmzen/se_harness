# Hash-Bound Text Integrity

This domain governs one narrow question: when a committed text file's bytes are
bound by a recorded SHA-256, what preserves those exact bytes across every
supported checkout, and what fails closed when nothing does.

It exists because saying a file is canonical does not make its checked-out bytes
canonical. `RC-060-02` in
[`docs/rca/2026-08-23-0.6.0-release-recovery.md`](../../rca/2026-08-23-0.6.0-release-recovery.md)
recorded that root cause after Git rewrote evaluator-evidence LF bytes to CRLF
after their digest had been recorded. The correction made at the time
(`ADR-REB-003`, `REQ-REB-009`) was right but deliberately narrow: it declared one
path class. This domain generalizes the obligation and makes completeness
machine-checked.

| Artifact class | Directory |
|---|---|
| Intent | [`intent/`](intent/) |
| Capabilities | [`capabilities/`](capabilities/) |
| Requirements | [`requirements/`](requirements/) |
| Specifications | [`specifications/`](specifications/) |
| Architecture and ADRs | [`architecture/`](architecture/) |
| Verification contracts | [`verification/`](verification/) |
| Work orders | [`work-orders/`](work-orders/) |
| Retained evidence | [`evidence/`](evidence/) |
| Verification records | [`verification-records/`](verification-records/) |

## Scope boundary

In scope: files tracked in Git whose bytes a governed artifact field or an
authorization input binds by SHA-256.

Out of scope: uncommitted release-bundle text such as `SHA256SUMS` and the source
manifest named by `RLS-SEH-012`; generated content under `target/`; binary
archives; and the canonical digests of managed files, which are immune by
construction because `utf8-text-lf-v1` normalizes line endings before hashing.

Related domains: [`portable-managed-integrity/`](../portable-managed-integrity/)
owns the canonical digest for managed files and fragments;
[`released-evaluator-boundary/`](../released-evaluator-boundary/) owns the
narrow evaluator-evidence checkout policy this domain generalizes.
