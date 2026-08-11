Feature: Verification-record supersession
  Stale ready verification attempts must remain auditable without remaining active or release-eligible.

  Scenario: A ready record is superseded by verified superset coverage
    Given a ready verification record covering one work order
    And a distinct verified verification record covering that work order and additional work
    When an accountable owner records the supersession metadata and relation
    Then the artifact graph validates
    And the old record remains bound to its original candidate
    And the dashboard shows the old-to-new lineage

  Scenario: Creating a newer verified record does not grant authority
    Given a ready verification record whose work is covered by a newer verified record
    When no accountable supersession decision is recorded
    Then the ready record remains unchanged
    And the dashboard reports a derived stale-ready warning
    And automation does not select or apply a successor

  Scenario: An ineligible successor is rejected
    Given a superseded verification record
    When its superseded_by target is missing, ready, superseded, incorrectly typed, or itself
    Then validation fails with the affected record IDs

  Scenario: Successor coverage cannot shrink
    Given a source verification record covering two work orders
    When its proposed successor omits either work order
    Then validation rejects the supersession

  Scenario: Supersession cycles are rejected
    Given verification records connected by superseded_by relations
    When the relations form a directed cycle
    Then validation fails deterministically

  Scenario: Active release references block supersession
    Given a ready or released release record includes a ready verification record
    When that verification record is changed to superseded
    Then validation rejects the transition
    And no successor is silently substituted into the release record

  Scenario: Superseded records cannot prepare a release
    Given a valid superseded verification record
    When release preparation selects that record
    Then preparation fails without creating output

  Scenario: Existing verification records remain compatible
    Given a repository with valid ready, verified, and released verification records and no supersession metadata
    When the upgraded validator and dashboard run
    Then the existing graph remains valid
    And installation ownership and customization behavior are unchanged
