Feature: Trace approved engineering work to exact commits

  Scenario: Capture a clean candidate verification
    Given an approved work order and verification contract
    And a clean candidate commit with retained evidence
    When verification provenance is captured
    Then a ready verification record names the full candidate commit
    And no Git state or approval is changed

  Scenario: Prepare a consistent release
    Given a verification record for a candidate commit
    When a release record is prepared
    Then the ready release record names the same commit
    And traces to its release contract, verification record, and work order

  Scenario: Reject inconsistent provenance
    Given a release record whose commit differs from its verification record
    When the graph is validated
    Then commit inconsistency is a blocking diagnostic

