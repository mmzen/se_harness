+++
id = "ARCH-IAR-001"
type = "architecture"
title = "Layered instruction and enforcement architecture"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-09-08"

[relations]
addresses = ["REQ-IAR-001", "REQ-IAR-002", "REQ-IAR-003", "REQ-IAR-004", "REQ-IAR-006", "REQ-IAR-007", "REQ-IAR-008", "REQ-IAR-009"]
conforms_to = ["SPEC-IAR-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "cross-cutting-policy", "material-alternatives"]
rationale = "ADR-IAR-001 chose a thin AGENTS.md fragment, one fully managed router and focused policy modules over seven rejected alternatives. It fixed the instruction system boundary and where authority is defined for every actor reading the repository."
assessed_by = "technical-owner"
+++

# Architecture: Layered instruction and enforcement architecture

## Components

- **Tool adapters**: managed fragments in `AGENTS.md` and `CLAUDE.md` expose one common route while leaving repository-owner content intact.
- **Managed router**: `ENGINEERING_HARNESS.md` states the non-waivable boundary and selects focused policy by engineering stage.
- **Owner information**: the owner-controlled region of `AGENTS.md` and the engineering README hold repository facts and domain navigation without granting authority. The harness neither scaffolds nor tracks that region.
- **Formal memory**: typed artifacts and relations hold product intent, requirements, work authorization, verification contracts, and release constraints.
- **Local enforcement**: `harnessctl preflight` composes integrity, graph, status, and chain checks into a read-only readiness report.
- **Remote enforcement**: an independently pinned harness distribution executes the required CI check; repository-host protection makes the result a merge condition.
- **Bootstrap verification**: the harness repository separates last-release independent baseline checks from candidate tests, then advances the external pin through later governance.
- **Safe distribution**: the installer, schema-2 lock, canonical templates, and explicit mode migration preserve managed and owner boundaries.

## Control flow

```text
tool adapter -> AGENTS managed gate -> managed router
                                      |       |
                                      |       +-> stage policy modules
                                      +----------> preflight(WO)
                                                    |
                         +--------------------------+----------------------+
                         |             |              |                   |
                      integrity     policy        artifact graph      WO chain
                         +-------------+--------------+-------------------+
                                                       |
                                              readiness evidence
                                                       |
                                      accountable human decisions remain separate
```

## Trust boundaries

- Target paths, existing file content, lock data, artifact metadata, pull-request text, and work-order IDs are untrusted input.
- Owner content is preserved but is not allowed to mutate or surround managed markers ambiguously.
- Candidate-controlled validators and workflows are product code under test, not independent proof of their own correctness.
- The exact external harness pin, required-check setting, CODEOWNERS review, and branch protection form one governance boundary; weakening any member is an accountable host change.
- Preflight output is evidence. Artifact approval and lifecycle transitions remain human decisions.

## Constraints

- Preserve Python 3.11+ and standard-library runtime behavior for installed checks.
- Preserve the single standard install; do not add minimal, offline, tool-specific, or enforcement profiles.
- Do not use symlinks for instruction routing because adoption must remain portable across Windows and archive distributions.
- Keep text and JSON output deterministic and avoid timestamps or checkout-specific absolute paths unless explicitly reported as observations.
- Reuse the formal parser and integrity comparison rather than implementing divergent validation rules.
- Apply root self-hosting changes through the same installer and lock behavior delivered to target repositories.

## Residual limitations

No structural mechanism can prove a person read the returned manifest, correctly interpret owner prose, or determine that an arbitrary diff semantically fits the declared work order. Offline installation cannot set or continuously audit remote branch protection. An unreleased checker cannot independently verify its own new behavior. These limitations must be visible in preflight, CI evidence, and installation guidance and mitigated by accountable review rather than hidden by an automation claim.

## Amendment record

**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-IAR-001`).** Eight of the
nine requirements of the legacy relation become `addresses`; `conforms_to`
names `SPEC-IAR-001`, the active specification that specifies them.
`REQ-IAR-005` is left out of `addresses`: it is `superseded`, and an active
architecture may not address an inactive requirement. `SPEC-IAR-001` still
specifies it, so the historical edge remains readable in the graph. The
assessment reads the rationale and seven rejected alternatives of
`ADR-IAR-001`, the one active ADR that decides this architecture. Title,
status, statement and ADR relations are unchanged.
