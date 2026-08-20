+++
id = "ARCH-DST-013"
type = "architecture"
title = "Apply capacity headroom within the existing progressive bundle"
status = "approved"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
addresses = ["REQ-DST-062", "REQ-DST-063", "REQ-DST-064"]
conforms_to = ["SPEC-DST-020"]

[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The proposal changes one repository acceptance target inside the content-addressed progressive bundle already selected by ARCH-DST-010 and ADR-DST-010. It preserves schemas, partitioning, data ownership, trust boundaries, dependency direction, public commands, persistence, deployment, publication, failure strategy, and every hard content budget; it also preserves the already selected released-evaluator/candidate separation. No controlled architectural trigger or material structural alternative is introduced."
assessed_by = "technical-owner"
+++

# Architecture: Apply capacity headroom within the existing progressive bundle

## Context and scope

The bundle-v2 architecture intentionally keeps topology as one compact deferred resource and makes larger consumer size observational. Ordinary governed history has now outgrown the original SE Harness repository acceptance target by 1,401 bytes. This architecture applies numerical headroom without reopening the selected partition, trust, browser, or publication architecture.

## Components and responsibilities

- The candidate standard-template generator owns the future 2 MiB target.
- Existing deterministic topology projection and serialization own actual bytes.
- Candidate-source and package tests own exact constant and behavior qualification.
- GitHub pull-request execution supplies integration-history observation.
- Existing product definitions own aligned capacity wording.
- The external public 0.5.0 evaluator owns root preflight, validation, doctor, and managed integrity.
- Accountable humans own approval, assurance, merge, release, and root-upgrade decisions.

## Dependency direction

`existing validated projection -> unchanged topology serializer -> candidate target observation -> local/hosted acceptance evidence`

Separately:

`public 0.5.0 evaluator -> unchanged managed root -> governance assessment`

Candidate template bytes never flow into the evaluator process or active managed root.

## Data and control flow

1. Capture baseline graph and topology bytes on merged main.
2. Approve the exact 2 MiB target and candidate/root boundary.
3. Run public-0.5.0 start preflight and read the complete manifest.
4. Change the candidate template, aligned definitions, and focused tests only.
5. Generate twice and compare deterministic resources.
6. Qualify current branch, hosted pull-request merge ref, and disposable installed candidate package.
7. Retain evidence and stop before separately controlled commit-bound assurance and release actions.

## Trust boundaries

- Repository artifacts, Git histories, workflows, generated resources, and candidate packages remain untrusted inputs.
- Public 0.5.0 is trusted only as the external released evaluator; it does not supply candidate implementation.
- Size is an operational observation, not product authority or a graph-validity judgment.
- Human owners retain every lifecycle and external-action decision.

## Required patterns

- One exact named target shared by candidate generator and tests.
- Complete topology with unchanged manifest integrity.
- Integration-history evidence in addition to branch evidence.
- Candidate/evaluator origin separation.
- Explicit preservation of every other budget and boundary.

## Prohibited patterns

- Candidate source used as governor.
- Direct active-root managed generator or lock edits.
- Data omission, truncation, compression-only accounting, or history rewriting to pass.
- Schema, sharding, browser, publisher, version, release, or deployment changes.
- Automatic approval, verification, merge, or release based on byte count.

## Quality attributes

- **Capacity:** fourfold target and more than 1.5 MiB initial headroom.
- **Determinism:** same accepted bytes and history yield identical output.
- **Integrity:** every resource remains manifest-size and SHA-256 bound.
- **Compatibility:** bundle-v2 consumers and historical output remain valid.
- **Independence:** candidate product and released evaluator stay separate.
- **Auditability:** actual/target bytes and each execution topology are retained.

## Conformance checks

Apply `VER-DST-020`, including exact constant assertions, current and boundary fixtures, repeat generation, branch/merge history observations, managed-root doctor, candidate-source/package origin checks, full supported-runtime suites, formal validation, and changed-surface review.

## Related ADRs

No new ADR is required. `ADR-DST-010` already selects the one-resource compact deferred topology and explicitly defers sharding. This amendment accepts additional numerical headroom inside that selected design and introduces no new significant decision. The `no_significant_decision` assessment requires accountable technical-owner approval with the packet.
