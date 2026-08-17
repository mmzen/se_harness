Feature: Install and upgrade simple consumer GitHub CI
  A consumer repository uses one dedicated managed workflow and one exact
  released SE Harness evaluator without adopting the implementation
  repository's self-hosting topology.

  Scenario: Add SE Harness beside existing workflows
    Given a repository with application build and deployment workflows
    When the user adopts the standard harness
    Then one dedicated engineering-harness workflow is installed
    And every unrelated workflow remains unchanged
    And GitHub can discover all workflows independently
    But required-check enforcement remains repository-owner configuration

  Scenario: Add SE Harness when no CI exists
    Given a repository without a GitHub workflow directory
    When the user adopts the standard harness
    Then the workflow directory and dedicated workflow are created safely
    And no separate CI installation command is required

  Scenario: Evaluate a consumer with one released runtime
    Given the dedicated workflow declares one exact released SE Harness version
    When GitHub runs consumer validation
    Then one isolated environment outside the checkout is used
    And package-owned logic selects work and performs every harness assessment
    And checkout scripts are not executed as the evaluator
    And application tests remain repository-owned checks

  Scenario: Upgrade consumer CI normally
    Given an unmodified older managed consumer workflow
    And the operator has installed a newer released SE Harness package
    When the user reviews and applies the standard repository upgrade
    Then the managed workflow selects the same newer evaluator version
    And configuration and lock evidence are updated atomically
    And a repeated upgrade is unchanged
    And reconcile-governor is not involved

  Scenario: Preserve a customized workflow
    Given the dedicated managed workflow no longer matches retained integrity evidence
    When the user applies the standard upgrade
    Then the complete transaction is blocked
    And the customized workflow and all other repository files remain unchanged

  Scenario: Preserve implementation-repository self-hosting
    Given the exact SE Harness implementation repository
    When ordinary standard upgrade is planned
    Then the protected self-hosting configuration and workflow remain protected
    And the independent released-governor and candidate roles are not replaced by consumer CI
