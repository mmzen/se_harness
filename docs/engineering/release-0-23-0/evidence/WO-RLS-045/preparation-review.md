# Review: prepare evaluator 0.23.0 and plugin 0.2.7

## Useful result

Make the merged hosted client and plugin guidance available through a normal
release, with a reproducible private sandbox built from the same tagged source.
Git remains authoritative. No public service or container registry is proposed.

## Proposed work

| Work | Result | Verification |
| --- | --- | --- |
| [WO-RLS-045](../../work-orders/WO-RLS-045.md) | Set release versions, correct sandbox build identities, update current guidance, qualify and prepare the release inputs. | [VER-RLS-039](../../verification/VER-RLS-039.md) |
| [WO-RLS-046](../../work-orders/WO-RLS-046.md) | Qualify both exact plugin packages and the hosted combination; prepare marketplace staging. | [VER-RLS-040](../../verification/VER-RLS-040.md) and existing VER-IAR-021 |
| [WO-RLS-047](../../work-orders/WO-RLS-047.md) | After complete-release authorization, execute delivery and confirm all public surfaces. | [VER-RLS-041](../../verification/VER-RLS-041.md) |

[REL-SEH-036](../../release/REL-SEH-036.md) defines membership, versions, recovery
and the existing one-approval delivery route. All seven new records remain draft.
The proposed required assurance classification has not been recorded as a human
decision. The two raised HAG risks gain only links to the preparation work; their
state, ownership, action and history remain unchanged.

## Concrete changes

- Core evaluator/client: 0.22.2 development source becomes proposed 0.23.0.
- Both plugin manifests retain the proposed unused 0.2.7 release identity.
- The sandbox build helper stops hard-coding client 0.22.2. It checks the actual
  wheel against source/replay and consumes the exact staged plugin pair. Its
  existing development route remains available, with mismatch tests.
- The shared hosted setup guide accepts the exact qualified released client in
  a separate environment; selection and authority checks remain unchanged.
- Current docs distinguish the plugin's bundled 0.23.0 from the hosted service's
  pinned 0.22.1 evaluator. Stale pending-qualification text is corrected.
- The existing combination manifest records the built service image and private
  deployment conditions as a companion to the evaluator release bundle.

No service runtime, database/schema/protocol, dependency lock, publisher,
workflow or provider-setting change is planned. No new release framework or
duplicate product definitions are needed. The three work orders separate
candidate inputs, native package evidence and observations that can only happen
after publication; the last one is not a prerequisite of its own publication.

## Evidence required

Use the merged main base `4fb5dbc29ffd7a2ccdc9a081c9c9b9f82b99d999` and released
governor 0.22.1. Retain Windows/Linux checks, exact pinned two-build replay,
installed packages, applicable native delivery and hosted scenarios, independent
content/replay assessments, staging identities and read-only provider readiness.
An aggregate VREC must cover the final candidate and complete release membership.
Earlier verified candidates and evidence remain unchanged.

The advisory census found one untraced prior release merge, PR #536. It is not
an evaluator blocker and needs no invented exemption. Its inspected packaging
delta from the previous tag is the verified three-file WO-RLS-044 documentation
correction; this release's current wording is within WO-RLS-045.

## Limits and dependencies

- Codex Windows desktop must be assessed separately. The prior accepted omission
  applied to 0.22.1 only; this proposal does not carry it forward.
- Native authentication must be live when qualification runs. No new auth session
  or provider test was performed during this draft preparation.
- Authentication/DB ACL implementation, graph authority cutover and broad
  performance improvements remain deferred. RISK-HAG-001/002 remain raised.
- No test, build, staging, release-record preparation or publication is claimed
  by these drafts. Preparation checks assess the proposed artifacts and scope.

## Preparation checks

Released validation assessed 2,003 artifacts with zero errors, 63 existing
warnings and zero advisories. Planned scope checks cover the supplied 42, 5
and 22 paths for WO-RLS-045, WO-RLS-046 and WO-RLS-047 respectively, with no
uncovered or invalid paths. These checks do not prove complete implementation
impact coverage.

The approval checks pass graph, integrity, decision and lifecycle-edge checks.
Each still fails `QGS-ASSURANCE`: the human must confirm the proposed required
commit-bound verification before its classification can be recorded. This is
the pending approval below. All seven records remain draft.

The [check summary](preparation-checks.json) binds the reviewed formal files by
SHA-256. The [retained command archive](preparation-checks.zip) contains actual
commands, results and earlier preparation failures, plus the unchanged base
versions of the two raised risk records.

## Approval requested

Approve REL-SEH-036, WO-RLS-045/046/047 and VER-RLS-039/040/041, with required
commit-bound verification. Include ordinary review pushes and draft PRs from
`codex/release-0-23-0` to `mmzen/se_harness:main`, later verification-decision
updates, read-only CI rehearsals and review staging at
`codex/plugin-0-2-7-staging`.

This authorizes bounded preparation and qualification. Human verification,
preparation-PR merge and the later exact complete-release approval remain
separate. That final approval will cover evaluator, GitHub/PyPI, marketplace,
documentation, Pages, maintenance line and latest/last together. Repository
adoption and actual host-plugin updates remain outside this package.
