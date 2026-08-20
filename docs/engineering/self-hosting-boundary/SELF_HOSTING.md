# Standard Repository Lifecycle

This guide supersedes the former specialized self-hosting operating model. The filename is retained so historical formal artifacts and links remain readable; it does not identify an active installation profile.

## Current boundary

The `se_harness` implementation checkout is a standard governed repository:

- `.engineering-harness.toml` selects the exact released evaluator version and ordinary repository policy.
- `.github/workflows/engineering-harness.yml` is the standard managed released-evaluator workflow.
- `.engineering-harness.lock` protects the standard managed installation.
- `.github/workflows/candidate-evidence.yml` is repository-owned CI for candidate source and package evidence.
- Candidate execution never changes formal lifecycle state or root managed controls.

There is no active governor descriptor, protected implementation-repository class, packaged migration data, role-specific reusable workflow, or `reconcile-governor` command.

## Evidence planes

| Plane | Identity | Permitted target | Meaning |
| --- | --- | --- | --- |
| Released evaluator | exact released version installed outside the checkout | the standard root repository | independent root-governance evidence |
| Candidate source | exact checkout commit | source tests and declared derived output | implementation evidence |
| Candidate package | exact wheel built from the commit and installed externally | disposable standard repositories | packaged-behavior evidence |

The planes are distinct observations. None approves a work order, transitions a VREC or RLS, commits, merges, tags, publishes, or deploys.

## Ordinary development

An approved implementation work order uses standard start and review preflight. The released evaluator runs root doctor, graph validation, and Explorer generation. Repository-owned candidate CI runs the complete source suite and an isolated wheel lane. Runtime identity checks reject checkout fallback, editable or user-site substitution, ambiguous entry points, and candidate claims to released-evaluator identity.

## Future evaluator upgrades

After version N+1 is immutably published:

1. approve a bounded repository-upgrade work order;
2. install exact N+1 outside the checkout;
3. attest its package, module, template, and entry-point origins;
4. run ordinary `harnessctl upgrade` without `--apply`;
5. review every managed change and repository customization;
6. separately authorize and run the standard transactional apply;
7. rerun doctor, validation, preflight, source tests, package evidence, and hosted CI;
8. retain commit-bound evidence when configured provenance requires it.

An unpublished candidate, local wheel, editable install, successful test run, or mutable reference cannot substitute for publication. Historical SHB artifacts and evidence retain the facts of the retired model and do not grant current authority.
