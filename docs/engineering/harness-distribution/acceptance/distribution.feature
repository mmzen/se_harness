Feature: Reuse the standard software engineering harness

  Scenario: Initialize a new repository
    Given an empty target directory
    When the user initializes the harness
    Then the complete standard file set is installed
    And the artifact graph validates
    And the dashboard can be generated

  Scenario: Adopt an existing repository safely
    Given an existing repository with agent and ignore files
    When the user adopts the harness
    Then existing content is preserved
    And bounded harness instructions are integrated
    And the adoption report does not infer approved intent

  Scenario: Preserve a customized managed file
    Given a harness installation whose managed workflow was customized
    When an upgrade is applied
    Then the customized workflow remains unchanged
    And manual reconciliation is reported

