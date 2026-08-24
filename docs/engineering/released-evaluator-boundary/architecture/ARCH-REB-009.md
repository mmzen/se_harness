+++
id = "ARCH-REB-009"
type = "architecture"
title = "Typed release qualification boundary"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-REB-020", "REQ-REB-021", "REQ-REB-022"]
conforms_to = ["SPEC-REB-010"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The change introduces a public command protocol, fixes dependency direction between workflows and evaluators, and makes independence claims depend on enforced trust boundaries across every release lane. A free-form role flag, workflow-only wrappers, and separate commands are material alternatives with different long-term compatibility costs."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:15:39Z"
decided_by = "technical-owner"
+++

# Architecture: Typed release qualification boundary

## Context and scope

Today, release workflows reach directly for `doctor`, `validate`, repository scripts, package entry points, and interpreter paths. Those pieces can be correct individually while the combination is wrong. The caller effectively decides whether an evaluator is a root governor, predecessor, candidate self-checker, released verifier, or public install. That dependency direction caused the evaluator/target confusion recorded in issue #109.

This architecture puts one typed qualification boundary between workflow orchestration and low-level validators. Workflows select a named operation. The operation owns evaluator identity, target binding, isolation, required checks, result semantics, and no-change proof.

## Components and responsibilities

### CLI qualification router

Owns the `harnessctl qualify` namespace and five subcommand parsers. It rejects cross-role argument combinations before dispatch and contains no validation policy of its own.

### Runtime and target identity guard

Extends the released runtime-identity and evaluator-identity mechanisms. It establishes the running distribution, interpreter isolation, entry point, payload/archive digest, checkout separation, target kind, lock/release binding, and immutable target identities before role handlers execute.

### Released-root handler

Reads the target lock, binds it to the current installed evaluator, then runs the installed doctor and complete validator without importing target package code.

### Predecessor-view coordinator

Calls the shared production predecessor-view service, binds the view manifest to the source/release inputs, verifies the external predecessor environment, and invokes only the approved version-specific predecessor adapter. Successor code coordinates the subprocess but never enters the predecessor interpreter.

### Complete-candidate handler

Binds candidate source/package identity to an exact commit and runs full candidate-controlled validation. It always labels the result non-independent.

### Candidate-package verifier

Reuses the hardened candidate-acceptance implementation behind a role-specific handler. The released verifier inspects the untrusted wheel as data, installs it into a disposable environment, and delegates candidate execution to that environment.

The first deployment has one explicit bootstrap boundary. Exact public 0.6.0 cannot execute a command introduced after its release, so the candidate workflow invokes that immutable verifier's existing `accept-candidate` contract after independently binding its archive, payload, entry point, and isolation. Its output remains legacy-schema evidence and is not passed through the canonical result builder. This path accepts no selectable implementation and expires as soon as a released verifier contains the typed handler.

### Public-install handler

Binds an already downloaded exact wheel, immutable released record/manifest, installed payload, runtime entry point, and public smoke checks. It performs no acquisition or publication.

### Canonical result builder

Builds and serializes `se-harness-release-qualification-v1` from trusted identity observations and fixed check results. It owns atomic exclusive output and removes workstation-specific or secret material.

### Workflow conformance checks

Statically and behaviorally verify that each repository-owned release lane invokes the correct subcommand from the correct environment with the required provenance inputs. They reject raw validator substitution even if workflow step prose remains unchanged.

## Dependency direction

```text
repository-owned workflow
        |
        v
harnessctl qualify <fixed-operation>
        |
        +--> identity/target guard
        +--> one role handler
        |       +--> installed low-level validator/doctor
        |       +--> external predecessor subprocess
        |       +--> disposable candidate environment
        |       `--> shared predecessor-view service
        `--> canonical result builder
```

Workflows depend on typed operations, never on validator/script paths for release-qualification claims. Role handlers may reuse low-level validators through internal APIs or installed resources. Low-level validators do not depend on workflow definitions or the qualification router.

The exact-public-0.6.0 bootstrap lane is a bounded deployment predecessor, not a second architecture path: it preserves the already released verifier-owned acceptance boundary without pretending that immutable bytes contain the new namespace. Static conformance binds the sole allowed version, digests, entry point, legacy schema, and removal trigger.

The predecessor-view service is the sole production view constructor. The qualification layer calls it; it does not duplicate view policy. Lifecycle semantics remain owned by workflow contract v3 and are consumed rather than redefined.

## Data and control flow

1. A workflow supplies the named operation and only its permitted inputs.
2. The router parses the closed schema and dispatches to one handler.
3. The identity guard derives expected evaluator/target facts from locks, release records, manifests, and the running environment.
4. The handler stops on identity mismatch; it does not fall back.
5. The handler executes fixed checks in its declared isolation boundary.
6. The result builder combines independently observed provenance and ordered outcomes.
7. The CLI renders or atomically retains the result and returns a matching exit status.

For an external predecessor, the successor process constructs and hashes the view, then starts the exact predecessor interpreter with a minimal environment. The predecessor sees only the read-only view and its own installed entry points. For a candidate wheel, the verifier inspects archive bytes and creates a disposable candidate environment; candidate code never loads into the verifier process.

## Trust boundaries

- Repository content, Git metadata, candidate wheels, public wheels, locks, manifests, release records, view manifests, subprocess output, and all path inputs are untrusted.
- A candidate source/package process is not independent, even if its bytes equal a later release.
- A released verifier is independent of candidate code only while its interpreter and import path remain outside the candidate checkout/environment.
- A predecessor result is independent only while exact external identity and no-import isolation hold.
- A public-install result observes published bytes but does not inherit release decision authority.
- The root lock, not a workflow comment, determines which evaluator may claim `released-root` ownership.
- Canonical results are evidence objects, not capability tokens or lifecycle decisions.

## Required patterns

- One closed parser and one handler per qualification operation.
- Runtime identity before substantive target validation.
- Expected identities derived from governed inputs; caller path inputs locate runtimes but do not define what counts as correct.
- Argument-vector subprocess execution with isolated Python and minimal environment.
- Exclusive, atomic evidence output outside the target.
- Shared canonical result builder and stable check identifiers.
- Static workflow command checks plus adversarial executable behavior tests.
- Exact candidate/source/package/public/predecessor provenance and no-change proofs.

## Prohibited patterns

- A general `--role`, `--validator`, `--script`, or arbitrary command option.
- Inferring evaluator role only from an executable filename or working directory.
- Importing candidate/successor code into a released verifier or predecessor process.
- Copying the predecessor-view omission policy into the qualification layer.
- Allowing candidate output to set the independent verifier's overall result without independent corroboration.
- Using raw `doctor`, `validate`, or validator scripts as claimed release qualification in migrated workflows.
- Editing root managed files as part of this implementation.
- Retrying a role failure with a less strict role or a compatibility bypass.
- Relabeling the exact-public-0.6.0 bootstrap result as canonical qualification evidence, allowing another version or digest into that lane, or retaining the lane after a typed released verifier is available.

## Quality attributes

- **Safety:** invalid evaluator/target combinations fail before their results can be misclassified.
- **Auditability:** every retained result identifies role, evaluator, target, checks, and independence.
- **Determinism:** immutable inputs produce stable decision-bearing output.
- **Portability:** the same operations and trust checks work on Windows and POSIX runners without shell-specific path tricks.
- **Maintainability:** workflows name business intent while handlers own reusable technical detail.
- **Compatibility:** pre-command predecessors remain reachable only through a bounded version adapter; existing diagnostic commands remain available.

## Conformance checks

- Parser tests enumerate accepted and rejected options for all five subcommands.
- An independent matrix mutates runtime, lock, commit, wheel, view, payload, entry point, checkout/import path, and result output.
- Candidate validator/source mutation cannot change the released verifier's independently collected identity or decision.
- Workflow tests parse all relevant workflow command blocks and exercise representative environments.
- Source, template, wheel, and sdist CLI/help/resource parity is checked.
- Tests prove root managed files, governed history, refs, credentials, and external state remain unchanged.

## Related ADRs

`ADR-REB-009` selects the single `qualify` namespace with five typed subcommands and a shared result protocol over documentation-only guidance, a free-form role flag, five unrelated top-level commands, or workflow-only wrappers.
