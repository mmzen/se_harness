+++
id = "ADR-RLO-005"
type = "adr"
title = "Rehearse in a parallel lane behind a checked equivalence seam"
status = "approved"
owners = ["release-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-RLO-005"]
+++

# ADR: Rehearse in a parallel lane behind a checked equivalence seam

## Status

Accepted.

## Context

`RC-060-11` records that real hosted platform details were tested too late. The credential-free mechanics of the release orchestrator are split so that each half runs on exactly one platform: `resolve` proves evaluator identity through the POSIX `bin` layout on `ubuntu-latest`, and `qualify` exports, builds, normalizes, and verifies through `cygpath` and a re-pointed `TEMP`/`TMP` pair on `windows-2022`. Incidents `I-15` and `I-16` are what that costs — Windows publication could not open export paths, and seven Windows tests failed on two spellings of the same temporary path — and both were discovered during a live release.

The literal completion criterion for the remediation asks for rehearsals that use "the same shells, virtual environments, paths, build commands, tests, bundle checks, and cleanup behavior used by publication." The word *same* is the whole decision. Sameness can be structural, by making both paths execute one implementation, or checked, by keeping two paths and failing closed when they diverge.

The release orchestrator's real behavior is only provable during an actual release. A defect introduced into it would surface on the next production release — which is the release that a consumer repository is currently blocked waiting for.

## Decision drivers

- Exercise both platforms before release approval, which is the point of the remediation.
- Do not put the live release path at risk while building a control whose purpose is to protect it.
- Make divergence between rehearsal and publication a red check rather than a silent false signal.
- Keep candidate code credential-free, preserving the property `INT-RLO-001` already requires.
- Keep the rehearsal reproducible locally so a hosted failure can be diagnosed without a hosted run.
- Preserve the single `release_record` input, the `RLO-001` through `RLO-003` guarantees, and the portable boundary from `ADR-RLO-002`.

## Considered options

1. Keep platform coverage as it is and rely on the release itself, which is the status quo `RC-060-11` condemns.
2. Refactor the orchestrator's credential-free mechanics into one shared program that both publication and the rehearsal invoke, making sameness structural.
3. Add a parallel credential-free rehearsal lane on both platforms and enforce sameness with a fail-closed divergence check against a data-only declaration.
4. Extend the existing candidate-evidence integration lane to cover publication mechanics, reusing its two-platform matrix.
5. Add a dry-run input to the orchestrator that short-circuits before every credentialed step.

## Decision

Choose option 3. Add a repository-owned rehearsal program under `.github/scripts/`, a two-platform rehearsal workflow holding `contents: read` only, a data-only mechanic declaration, and a divergence checker that fails closed on an uncovered or stale mechanic. Leave `.github/workflows/publish-pypi.yml` byte-unchanged.

The accountable repository owner made this choice on 2026-08-24, selecting `Parallel lane + drift check` over the presented `Refactor to one shared script` option after both were framed with their trade-offs, and selecting `Fourth release-orchestration packet` as the governance home.

Option 2 is the stronger answer to the literal criterion and is not rejected on merit; it is deferred because it modifies the untested-until-release path. Option 4 is rejected because the integration-package lane is governed by `REQ-IPK-003`, which forbids its artifacts from touching release authority, and because that lane deliberately builds a non-promotable payload through its own implementation rather than the release build path. Option 5 is rejected because a dry-run input adds an operator-selectable mode to the credentialed orchestrator, enlarging exactly the surface this work is trying not to disturb.

## Consequences

- Positive: every credential-free mechanic is exercised on both platforms before release approval, which is what `RC-060-11` asks for.
- Positive: the release transaction carries no new risk, because it is not modified.
- Positive: the lane cannot publish anything, since it holds no credential and no write permission.
- Positive: a credential-free step added to the orchestrator without rehearsal coverage turns a required check red instead of reaching a release unexercised.
- Positive: the rehearsal runs locally, so a platform defect is reproducible without a hosted release.
- Negative: equivalence is checked rather than structural. Step digests bring argument-level and within-step ordering differences inside the checker's model, but sequence-and-environment equivalence between the two lanes stays outside it: the orchestrator can move a step between jobs, or change what an earlier step leaves behind, and every comparison still passes. `ARCH-RLO-005` records this as the accepted weakness.
- Negative: the credential-free mechanics now have two implementations of their orchestration glue, which is duplication that must be maintained in step. The divergence check is the mitigation, not a cure.
- Negative: the rehearsal builds twice and runs the unit suite on both platforms, so candidate integration gets slower.
- Operational: `pages_build` is credential-free by permission but uses actions that mutate external Pages state, so it is classified as excluded and reported as such rather than rehearsed. `observe` holds no credential of its own and is nonetheless excluded, because it depends on `github_release`; five of the orchestrator's seven jobs are excluded and two are rehearsed.
- Security: no credential, environment, token, or write permission is added anywhere.
- Migration: no consumer, package, template, lock, or upgrade behavior changes.

## Revisiting condition

Reconsider option 2 when the orchestrator's credential-free surface next changes materially, when a divergence escapes the checker's model, or when a release incident is traced to a difference in the sequence or the surrounding environment of a mechanic the two lanes both declare. At that point structural sameness becomes cheaper than maintaining the seam, and the refactor can be governed as its own work with its own release-risk decision.

## Validation

Test platform layout resolution on both platforms, alias canonicalization, temporary-path identity assertion, candidate export, deterministic build agreement and its failure, cross-set manifest and bundle verification and its failure, link-safe teardown and its refusal to escape the root, job classification including the unclassifiable case, both divergence directions, the data-only declaration property, and the byte-unchanged orchestrator. No production tag, release, package, index object, deployment, environment approval, or lifecycle transition may be created as implementation evidence.

## Approval

Accepted by the accountable repository owner on 2026-08-24 through the statement `OK go for #111` and the explicit selection of `Parallel lane + drift check`.

## Amendments during implementation

Stated for owner acceptance or rejection. The decision, the rejected options, and the deferral of option 2 are unchanged.

Two consequences and the revisiting condition were restated because implementation measured what the seam actually catches. The accepted negative said argument-level and ordering differences lie outside the checker's model; per-step script digests put both inside it, so leaving the sentence would have recorded a risk the owner did not in fact take on. The genuinely unmodelled case is narrower and had to be named honestly: the checker's unit is a step's script, not the pipeline that reaches it, so a step moved between jobs or a change in what an earlier step leaves behind passes. The revisiting condition now points at that case instead of the closed one, and the operational note now records `observe` as the second exclusion class — excluded transitively rather than by an attribute of its own — because that classification was found only by running the checker against the real orchestrator.
