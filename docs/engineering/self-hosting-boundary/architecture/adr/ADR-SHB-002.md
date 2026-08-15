+++
id = "ADR-SHB-002"
type = "adr"
title = "Protect and reconcile self-hosting controls and externalize candidate acceptance"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner", "security-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
decides = ["ARCH-SHB-002"]
+++

# ADR: Protect and reconcile self-hosting controls and externalize candidate acceptance

## Status

Approved with the Phase 1 governance packet on 2026-08-15. The owner separately authorized implementation on the same date.

## Context

`doctor` correctly treats `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml` as repository-specific self-hosting controls, while normal upgrade does not. Because both current files match their root lock but differ from the consumer template, `harnessctl upgrade .` currently proposes replacing both. The replacement would erase the self-hosting role and three-plane workflow. Protection alone would then make intentional schema, workflow, and published-governor changes depend on undocumented manual edits. Candidate source and package tests also remain candidate-controlled evidence; a future governor needs independently published, replayable black-box acceptance.

## Decision drivers

- Preserve the exact two-file self-hosting exception without creating a product profile.
- Keep ordinary consumer upgrade automatic, safe, and transactional.
- Fail closed on ambiguous identity or protected-control drift.
- Preserve governed repository policy while allowing deterministic configuration-schema evolution.
- Avoid generic YAML merge and consumer/self-hosting workflow substitution.
- Make release-managed workflow mechanics reproducible while keeping authority-bearing repository choices explicit.
- Provide a supported, auditable way to adopt an exact published governor and reconcile the complete control set.
- Ensure the current released governor interprets target migration data without executing target code.
- Prevent a candidate from owning the sole acceptance oracle used to qualify itself.
- Support gradual evolution when an old governor cannot understand new semantics.

## Considered options

1. **Continue treating both controls as standard managed files.** Simple and already implemented, but normal upgrade destroys the self-hosting boundary precisely when integrity says the current repository state is valid.
2. **Convert both controls to repository-owned seeds.** Prevents overwrite, but removes managed-integrity checks and makes missing or modified trust controls look like ordinary owner customization.
3. **Protect lock-matching controls during normal upgrade; add current-governor-driven, field-aware reconciliation of immutable published target data; publish a governor-owned black-box acceptance runner.** Keeps consumer behavior intact, preserves repository policy and integrity, makes self-hosting changes deliberate, and separates candidate evidence from future independent assessment.
4. **Create a second public self-hosting installation profile.** Could render a distinct workflow automatically, but exports an implementation-repository concern into the consumer product and increases upgrade/profile complexity.
5. **Use candidate tests only and rely on human review of test changes.** Useful but insufficient as the sole package acceptance oracle because candidate code and tests change together.
6. **Protect both files and reconcile them manually or through a generic three-way text/YAML merge.** Avoids a new protocol, but cannot reliably distinguish schema mechanics from repository policy, cannot safely merge GitHub Actions sequences and authority settings, and leaves recovery and lock alignment error-prone.

## Decision

Choose option 3.

Normal upgrade recognizes the exact implementation repository through one shared fail-closed policy. It preserves the two lock-matching controls and reports their consumer-template divergence explicitly. Missing, ambiguous, or modified controls block all writes.

A separate `reconcile-governor` plan/apply operation runs from the currently selected checksum-verified governor and targets one exact immutable published release. It treats the target release's migration manifest, configuration schema, and workflow material as data and never imports target code. TOML migration is field-aware: release-managed fields may change deterministically, repository identity and policy survive, safe defaults may be added, and authority-bearing choices require explicit governed values. Workflow mechanics use the target self-hosting variant and are replaced rather than generically merged; repository variation survives only through documented inputs or extension points. The governor descriptor, configuration, workflow, and lock update through one recoverable transaction after all invariants pass.

The operation implements an already authorized mechanical transition; it does not itself approve work, verify the candidate, publish the target, or remove the separate accountable decision to promote that published target. If the current governor cannot interpret the target data-only migration protocol, a compatible bridge release is required.

Package acceptance is driven by a black-box contract shipped by the released governor or another immutable verifier artifact selected by it. Candidate source and package continue to run extensive checks, but their outputs remain candidate evidence. A new runner becomes independent only after publication and separate governor promotion, so activation follows a two-release-compatible sequence.

## Consequences

- Normal `harnessctl upgrade . --apply` can no longer replace the self-hosting workflow or remove its role declaration.
- The upgrade plan gains an explicit protected disposition and shared self-hosting classification.
- Intentional governor, workflow, schema, or repository-policy changes require a bounded reconciliation step and human-reviewed work order.
- The protected files remain managed integrity controls rather than owner seeds.
- Target releases must publish versioned data-only migration and role-specific workflow material compatible with the current governor.
- Repository policy needs explicit schema ownership; workflow customization needs documented inputs, extension points, or a separate workflow.
- Unsafe schema jumps, policy ambiguity, unrecognized workflow deltas, and authority changes without an explicit decision fail closed.
- Reconciliation becomes a multi-file recoverable transaction rather than a lock-only acknowledgement.
- A released governor carries more durable acceptance responsibility and evidence schema.
- CI and packaging gain replayable black-box scenarios and canonical evidence manifests.
- Release A implements the mechanism but cannot claim retroactive independent governance; a separate promotion is required before future candidates rely on it as governor authority.
- Implementation is more involved than a two-line installer exception, but the resulting authority and migration model is testable and auditable.

## Validation

Execute `VER-SHB-002`. In particular, prove consumer upgrade compatibility, self-hosting protected preservation, immutable target resolution, current-governor execution, target-code non-execution, field-owned TOML migration, safe-default and decision-required behavior, role-correct workflow replacement, fail-closed ambiguity, transaction recovery, source/package/governor origin isolation, verifier ownership, canonical replay, authority-denial scenarios, and staged post-publication activation.
