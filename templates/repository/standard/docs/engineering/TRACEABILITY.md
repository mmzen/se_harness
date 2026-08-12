# Traceability

The normative chain is:

```text
Intent -> Capability -> Requirement <- specifies - Specification
                             ^                         ^
                             | addresses               | conforms_to
                         Architecture <----- decides - ADR
                             |
                         Work order(s) -> Verification
                             |
                  Verification record + commit
                             |
                    Release record + same commit
                             |
                     Operating contract
```

Only declared relations in formal TOML metadata establish authority. Source comments, filenames, commits, tickets, and conversational references may aid discovery but do not satisfy formal coverage.

`ARCH.addresses -> REQ` declares only architecturally significant requirement drivers. `ARCH.conforms_to -> SPEC` declares the detailed behavioral or interface contracts relevant to that architecture. Every addressed requirement must be reachable through a conforming specification's `SPEC.specifies -> REQ` relation, but a specification may also cover routine requirements that do not drive architecture. Explorer may show that transitive path as derived context; it never replaces the direct declared relations or creates authority.

Work-order definition and verification coverage remain independent: every implemented requirement needs selected specification and verification coverage. Architecture is applicable when an active architecture directly addresses an implemented requirement, and every selected architecture must share a conforming specification with the work order. Do not fabricate architecture coverage for routine requirements.

The old polymorphic `ARCH.constrains` relation is compatibility-only. Completed unambiguous historical forms may be classified with a migration advisory; mixed target types fail closed. Installation and upgrade never rewrite repository-owned formal artifacts.

Architecture decision applicability is declared on each architecture. `ADR.decides -> ARCH` establishes coverage for an `adr_required` architecture; the mere presence of an ADR elsewhere in the work order does not. A work order selects every applicable architecture and each required deciding ADR. An accepted `no_significant_decision` assessment permits omission of an ADR for that architecture. ADR cardinality follows coherent significant decisions and is independent of requirement, specification, work-order, or architecture counts.

`verification_record` binds one or more release-bearing work orders, their declared verification contracts, and retained evidence to one clean final candidate commit. `release_record` binds a release contract to the same commit and an exact released-work set equal to included verification coverage. Single-work-order records remain aggregates of cardinality one.

Governance-only work may authorize review, verification transition, release transition, tagging, or publication in later commits, but it is not automatically release payload. The dashboard's observed checkout revision is derived context, not release authority.

A governance-only work order records completed execution as `implemented`. It does not become `verified` merely because it authorizes the transition of a different VREC; doing so would create recursive governance work. When configured provenance is required, a work order may claim `verified` or `released` only when a verified or released VREC explicitly includes it. VREC and RLS records, rather than work-order status alone, are the authoritative commit and release bindings.

A stale `ready` verification record may be retained as `superseded` only through a separate accountable governance decision. Its `superseded_by` relation names one distinct verified or released VREC that covers every original work order. Supersession preserves the old candidate and evidence facts, is terminal, and never contributes verification or release readiness. Dashboard overlap findings are non-authoritative prompts, not lifecycle decisions.
