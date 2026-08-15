Feature: Protected self-hosting upgrade, governor reconciliation, and replayable candidate acceptance
  The implementation repository preserves its repository-specific control plane
  while released verifier behavior qualifies candidate source and packages
  without granting the candidate authority over itself.

  Scenario: Standard upgrade preserves valid self-hosting controls
    Given the exact implementation repository is configured for self-hosting
    And both protected controls match their root lock
    When normal repository upgrade is planned and applied
    Then both controls are reported as protected and remain byte-identical
    And eligible ordinary managed files may still update transactionally

  Scenario: Protected drift blocks every upgrade write
    Given one protected control differs from its root lock
    When normal repository upgrade is applied
    Then the control mismatch is reported as blocking
    And no managed file or lock entry changes

  Scenario: Consumer workflow continues to upgrade normally
    Given an ordinary consumer workflow matches its prior managed lock
    And the newly installed harness contains a changed standard workflow template
    When consumer upgrade is applied
    Then the consumer workflow updates to the rendered template
    And a consumer customization still fails closed without partial writes

  Scenario: Reconciliation safely migrates repository configuration
    Given the current released governor is isolated outside the checkout
    And an approved work order selects an immutable published target release
    And the target adds a release-managed TOML property with a safe default
    And the current accepted file contains repository-owned policy values
    When governor reconciliation is planned and applied
    Then the new property and schema version are applied deterministically
    And every repository policy and identity value is preserved
    And target release code is not imported or executed

  Scenario: Reconciliation stops for an authority-bearing decision
    Given the target schema or workflow introduces a permission, trigger, environment, secret, or policy value without a safe default
    When governor reconciliation is planned without an explicit governed value
    Then the plan reports that a decision is required
    And the governor descriptor, controls, and lock remain byte-identical

  Scenario: Reconciliation selects only the self-hosting workflow
    Given the published target contains consumer and self-hosting workflow material
    When governor reconciliation targets the implementation repository
    Then the self-hosting workflow variant is selected
    And generic YAML merge and consumer workflow substitution are prohibited
    And unrecognized local workflow differences block apply

  Scenario: Explicit reconciliation is a recoverable bounded transaction
    Given the target descriptor, migrated TOML, self-hosting workflow, and lock all pass validation
    When governor reconciliation is applied
    Then only the declared governor descriptor, two protected controls, bounded transaction metadata, and lock may change
    And an interruption leaves a recoverable complete prior or complete target state
    And the command grants no approval, verification, release, publication, or promotion authority by itself

  Scenario: Candidate package is assessed by a released contract
    Given a released governor owns a pinned functional acceptance contract
    And an exact candidate wheel is installed outside the checkout
    When the contract exercises the candidate through its installed entry point
    Then every required black-box scenario runs with candidate-package identity
    And candidate-owned tests are not the sole acceptance oracle

  Scenario: Functional evidence is replayable
    Given governor, contract, candidate commit, wheel digest, Python identity, and scenario inputs are pinned
    When acceptance is executed twice in fresh equivalent environments
    Then the canonical evidence manifests are byte-equivalent
    And timing, temporary paths, and secrets are absent from canonical evidence

  Scenario: Candidate evidence cannot authorize itself
    Given candidate source and candidate package checks pass
    When their results are retained
    Then they are labelled candidate evidence
    And only accountable humans may verify, release, publish, or approve governor promotion

  Scenario: New verifier authority activates after publication
    Given candidate release A implements a new acceptance runner
    When A has not yet been immutably published and separately promoted
    Then A's runner remains candidate evidence for A
    And only a later governed cycle may use the published runner as released-governor assessment
