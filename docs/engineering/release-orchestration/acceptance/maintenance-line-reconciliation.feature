Feature: Reconcile the SE Harness repository maintenance line
  The repository release workflow establishes a canonical release/MAJOR.MINOR
  line without adding branching behavior to portable SE Harness.

  Scenario: Create the first maintenance branch for a release line
    Given released version 0.5.0 resolves candidate C from trusted main
    And refs/heads/release/0.5 does not exist
    When the exact GitHub Release has been materialized
    Then refs/heads/release/0.5 is created at C
    And the workflow reports the maintenance line as created

  Scenario: Replay an exact existing line
    Given released version 0.5.0 resolves candidate C
    And refs/heads/release/0.5 already points to C
    When maintenance-line reconciliation runs again
    Then no branch update or delete request is made
    And the workflow reports the maintenance line as existing

  Scenario: Preserve an advanced maintenance line
    Given released version 0.5.1 resolves candidate P
    And refs/heads/release/0.5 points to a descendant of P
    When maintenance-line reconciliation runs
    Then the existing branch remains unchanged
    And the workflow reports the maintenance line as existing

  Scenario: Refuse a conflicting maintenance line
    Given released version 0.5.0 resolves candidate C
    And refs/heads/release/0.5 does not contain C
    When maintenance-line reconciliation runs
    Then the workflow fails visibly
    And no branch mutation is requested

  Scenario: Recover from a concurrent compatible creator
    Given refs/heads/release/0.5 is absent at lookup
    And another actor creates it at C before this workflow creates it
    When the create request reports a reference conflict
    Then the workflow refetches the branch
    And accepts it only after proving that it contains C

  Scenario: Keep the feature repository specific
    Given a consumer installs or upgrades SE Harness
    When its package, managed templates, and workflow are inspected
    Then no automatic maintenance-line behavior is present
    And harnessctl exposes no maintenance-branch command or option
