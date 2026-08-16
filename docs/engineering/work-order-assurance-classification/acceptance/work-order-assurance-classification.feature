Feature: Explicit work-order commit-bound assurance applicability
  Commit-bound verification obligations are declared by accountable owners and
  projected by read-only tooling without changing existing lifecycle authority.

  Scenario: Assurance-bearing work is classified before execution
    Given a work order is ready for accountable approval
    When its owner records commit-bound verification as required with a rationale and deciding role
    Then formal validation accepts the supported assurance table
    And start preflight displays the explicit decision

  Scenario: Governance transport does not create recursive verification
    Given a work order solely records or transports an already authorized governance decision
    When its owner classifies commit-bound verification as not required
    Then the completed work order remains implemented
    And inspection does not infer a verification-record obligation

  Scenario: Implemented assurance-bearing work needs follow-up
    Given an implemented work order explicitly requires commit-bound verification
    And no ready, verified, or released verification record directly covers it
    When the repository is inspected
    Then the work order appears in assurance pending
    And the suggested preparation action is non-automatic

  Scenario: Active direct coverage clears pending preparation
    Given one ready verification record directly covers several implemented required work orders
    When the repository is inspected
    Then none of those work orders appears in assurance pending
    And the verification record appears once for accountable assurance review

  Scenario: Completed legacy work remains compatible
    Given a completed legacy work order has no assurance table
    Then formal validation does not invent a requirement or exemption
    But renewed start or review preflight requires an explicit accountable decision

  Scenario: Superseded coverage cannot satisfy pending assurance
    Given an implemented required work order is covered only by a superseded verification record
    When the repository is inspected
    Then the work order remains in assurance pending
    And no lifecycle transition or verification record is created automatically
