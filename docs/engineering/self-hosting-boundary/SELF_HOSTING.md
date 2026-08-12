# Self-Hosting Operations

This guide applies only while developing `se_harness`. It does not create a consumer installation profile and it grants no implementation, verification, release, publication, or governor-promotion authority.

## Runtime planes

| Plane | Identity source | Permitted target | Assurance meaning |
| --- | --- | --- | --- |
| Released governor | `.self-hosting/governor.toml` plus the hash-checked published wheel | A governor-created disposable repository and explicitly compatible read-only candidate data | Independent bootstrap evidence |
| Candidate source | The reviewed checkout at `GITHUB_SHA` | Candidate tests and declared ignored derived output | Source implementation evidence |
| Candidate package | A wheel built from an exported candidate commit and installed in a fresh environment | Fresh and upgrade acceptance repositories outside the checkout | Packaged behavior evidence |

`harnessctl identity` emits the role, Python executable and version, harness version, module, distribution and template origins, expected boundary, and the applicable candidate commit or governor digest. A mismatch fails the lane.

## CI composition

The repository-specific workflow runs `governor -> candidate-source -> candidate-package`. The governor is acquired by immutable release URL and SHA-256, imported with isolated Python outside the checkout, and doctored only against a repository it created. Candidate package construction uses a Git export and writes only below the runner temporary directory. Every lane proves that it did not modify the checkout.

The checkout is candidate source. All normal managed files retain candidate distribution parity. The self-hosting workflow and root `[self_hosting]` configuration are the only repository-specific control files that intentionally differ from the rendered standard template, and both remain protected by the root lock. The governor creates its own same-version managed target outside the checkout. These controls are not alternative product profiles.

## Initial migration

Before this boundary, pull request #28 installed 0.2.1 but could import candidate source from the checkout and ran 0.2.1 `doctor` against 0.2.2-managed files. The corrected workflow records the selected 0.2.1 governor explicitly, proves its installed origin, runs its same-version integrity check in a disposable target, and labels all candidate execution as evidence.

The initial migration is necessarily implemented by candidate source. It is not retroactive proof for candidate `9ba0cec3710167ad4568931747ed5f4e48a63532`. Closed PR #28 retains its failed `VREC-SEH-003` and `RLS-SEH-003` attempt as audit history; the clean recovery candidate excludes those files and must receive new aggregate record IDs.

## Promoting the next governor

After a candidate is immutably published, use a separate approved work order to:

1. name the previous and proposed governor, published release record, immutable URL, wheel name, and SHA-256;
2. acquire the published wheel independently and verify its digest before installation;
3. test its identity, fresh installation, transactional upgrade, customized-content failure, doctor, validation, and rollback path outside the checkout;
4. update `.self-hosting/governor.toml` and the repository-specific CI constants in one reviewable change;
5. retain the previous descriptor through Git history and capture a new commit-bound VREC if configured provenance requires it.

Publication does not update the governor automatically. Until the separate promotion change is accepted, the prior descriptor remains authoritative.
