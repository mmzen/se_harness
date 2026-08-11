Feature: Rationalized and enforceable repository instructions
  The harness exposes one managed route, preserves repository-owner guidance,
  and validates implementation readiness without inferring authority.

  Scenario: An agent follows the canonical managed route
    Given a repository with the standard harness installed
    When an engineering agent reads the managed block in AGENTS.md
    Then the only next harness document is ENGINEERING_HARNESS.md
    And that router directly identifies repository context, formal authority, and each policy module

  Scenario: Claude receives the same instructions
    Given a repository with owner content in CLAUDE.md
    When the harness is adopted
    Then the owner content remains unchanged outside managed markers
    And the managed adapter imports AGENTS.md without duplicating policy

  Scenario: Existing owner instructions survive an upgrade
    Given AGENTS.md contains valid owner content around an unchanged managed fragment
    When a safe harness upgrade is applied
    Then only the managed fragment may change
    And the owner content remains byte-for-byte equivalent

  Scenario: Ambiguous instruction ownership fails closed
    Given an instruction file contains duplicate or malformed managed markers
    When adoption or upgrade is planned
    Then the plan reports a conflict
    And no repository file is written

  Scenario: A managed engineering index becomes an owner seed safely
    Given the old engineering README exactly matches its managed lock entry
    When the ownership-mode migration is applied
    Then the new repository index seed is installed
    And its lock mode records owner-controlled presence
    And a second application is a no-op

  Scenario: A customized engineering index is not silently reclassified
    Given the old engineering README differs from its managed lock entry
    When the ownership-mode migration is planned
    Then its content is preserved
    And the plan requires manual reconciliation
    And its lock mode is not silently changed

  Scenario: Preflight returns a complete implementation reading manifest
    Given the installed harness is intact
    And repository context is complete
    And the formal graph is valid
    And one selected work order is approved with a complete governing chain
    When preflight runs for that work order
    Then it succeeds without writing a file
    And it lists the router, applicable policy, context, work order, and complete linked chain in deterministic order

  Scenario: Review preflight accepts honestly completed work
    Given the selected work order is implemented with a complete active governing chain
    When preflight runs in review phase
    Then it assesses the pull-request candidate without relabeling the work order as approved

  Scenario Outline: Preflight rejects an implementation blocker
    Given <condition>
    When preflight runs for the selected work order
    Then it fails with a stable diagnostic
    And it grants no authority

    Examples:
      | condition |
      | a managed fragment has drifted |
      | a required context field is unresolved |
      | the artifact graph is invalid |
      | the selected ID is not a work order |
      | the selected work order is not approved |
      | the governing chain is incomplete |

  Scenario: Required pull-request CI is independent from candidate scripts
    Given a pull request declares exactly one approved work-order ID
    And the candidate weakens its checked-in validator
    When the required harness job uses its exact external distribution pin
    Then the independent check still detects the violation
    And the candidate cannot pass by modifying only repository-controlled checker code

  Scenario: Unreleased checker behavior is not called independent
    Given the harness repository adds new preflight behavior
    When its required CI runs before that behavior is released
    Then the last released harness enforces the prior independent baseline
    And candidate tests verify the new behavior
    And the evidence requires a separate governed pin update after publication

  Scenario: CI never infers a work order
    Given a pull request has no unique valid structured work-order declaration
    When the required harness job starts
    Then it fails before implementation readiness is claimed
    And it does not infer an ID from the branch name, commit message, or changed files

  Scenario: Successful checks remain evidence rather than authority
    Given doctor, preflight, validation, and dashboard generation succeed
    When the results are reported
    Then no artifact status changes
    And no commit, verification, release, tag, publication, or deployment is performed
