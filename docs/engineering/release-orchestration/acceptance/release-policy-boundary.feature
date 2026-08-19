Feature: Portable release governance remains independent from repository publication
  Repository owners can use SE Harness release governance without inheriting
  the se_harness project's Python packaging and publication policy.

  Scenario: A consumer receives format-neutral release preparation
    Given a repository installs or upgrades the standard SE Harness distribution
    When its agent inspects prepare-release, the managed validator, and the release template
    Then no wheel, sdist, SHA256SUMS, PyPI, Pages, or se_harness package rule is present
    And generic commit-bound release preparation remains available

  Scenario: Exact SE Harness distribution provenance is bound locally
    Given generic preparation created one ready RLS
    And repository build tooling created an exact bundle for the same version and candidate
    When the repository binder validates the inputs
    Then it atomically adds the complete repository distribution table
    And it changes no lifecycle, relation, version, commit, owner, or tag field

  Scenario: Invalid binding preserves the ready record
    Given a ready RLS and a malformed, partial, unsafe, or mismatched bundle
    When the repository binder is invoked
    Then it fails without changing any byte of the RLS

  Scenario: A repository extension is not core assurance
    Given an RLS carries repository-owned distribution metadata
    When portable graph validation evaluates the record
    Then it validates only the core RLS governance contract
    And repository CI separately evaluates the distribution contract

  Scenario: Publication retains one input and separated trust
    Given a released RLS in trusted main carries exact repository distribution provenance
    When the release owner dispatches publication with only the RLS identifier
    Then trusted repository tooling validates the distribution before candidate execution
    And credential-free qualification, immutable replay, GitHub, PyPI, Pages, and observations retain their existing boundaries

  Scenario: Missing repository provenance blocks only publication
    Given a historical or consumer RLS has no repository distribution table
    When portable validation evaluates it
    Then the RLS remains valid when its core governance is valid
    But the se_harness publication resolver refuses it before candidate execution or external mutation
