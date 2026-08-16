# Work-order assurance classification

This packet governs an explicit distinction between verification performed while implementing every work order and commit-bound assurance recorded through a VREC only when applicable.

Chain:

`INT-WAC-001` -> `CAP-WAC-001` -> `REQ-WAC-001..005` -> `SPEC-WAC-001`, `ARCH-WAC-001`, `ADR-WAC-001`, `VER-WAC-001` -> `WO-WAC-001`.

On 2026-08-16, after reviewing the current inspection gap and the risk of recursively verifying governance-only verification work, the repository owner agreed with the explicit classification rule and requested this artifact packet plus a supporting implementation branch.

On 2026-08-16, the repository owner instructed `ok go`, approving the complete ready definition chain and authorizing `WO-WAC-001` within its exact boundary. The approved design introduces one explicit work-order assurance table, bounded compatibility for completed legacy work, preflight enforcement, and a non-gating `assurance_pending` inspection queue. Commit, push, pull request, VREC creation or transition, release, publication, and deployment remain separately controlled.

The term **validation** remains reserved for structural, governance, policy, and maintenance checks. The new declaration answers a narrower question: whether an implemented candidate requires commit-bound assurance through a VREC.

Implementation completed on 2026-08-16 within `WO-WAC-001`: validator, preflight, inspection schema v2, canonical distribution, policy, templates, documentation, acceptance scenarios, and regression coverage now implement the approved contract. The work order remains awaiting a separately authorized candidate commit and commit-bound verification record.
