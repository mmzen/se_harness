Feature: Reuse the standard software engineering harness

  Scenario: Initialize a new repository
    Given an empty target directory
    When the user initializes the harness
    Then the complete standard file set is installed
    And the artifact graph validates
    And the dashboard can be generated

  Scenario: Adopt an existing repository safely
    Given an existing repository with agent, Claude, context, and ignore files
    When the user adopts the harness
    Then existing content is preserved
    And bounded harness instructions are integrated
    And Claude imports the shared AGENTS contract
    And the repository context remains repository-owned
    And the adoption report does not infer approved intent

  Scenario: Initialize shared agent instructions
    Given an empty target directory
    When the user initializes the harness
    Then AGENTS contains the bounded shared contract
    And CLAUDE imports AGENTS without duplicating the contract

  Scenario: Preserve repository-owned context
    Given a harness installation with curated repository context
    When an upgrade is applied
    Then the curated context remains unchanged
    And an intentionally removed accounted seed is not regenerated

  Scenario: Preserve a customized managed file
    Given a harness installation whose managed workflow was customized
    When an upgrade is applied
    Then the customized workflow remains unchanged
    And manual reconciliation is reported

  Scenario: Retire the repository-context scaffold without touching owner content
    Given a fresh installation and an installation whose retired context path holds owner-authored bytes
    When an upgrade is applied to each
    Then the fresh installation has no file at the retired path
    And the owner-authored bytes at the retired path are unchanged
    And neither regenerated lock has an entry or tombstone for the retired path
    And start preflight is ready with no retired context diagnostic and no repository command payload
