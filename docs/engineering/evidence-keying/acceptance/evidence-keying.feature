Feature: Portable work-order evidence keying
  Retained evidence is attributed consistently without requiring historical path rewrites.

  Scenario: Preserve flat filename attribution
    Given a safe retained path "docs/engineering/example/evidence/WO-ABC-001-check.md"
    When every evidence-attribution surface assesses the path
    Then every surface associates it with "WO-ABC-001"

  Scenario: Recognize a directory named for the work order
    Given a safe retained path "docs/engineering/example/evidence/WO-ABC-001/check.md"
    When every evidence-attribution surface assesses the path
    Then every surface associates it with "WO-ABC-001"
    And aggregate verification capture does not reject that work order as uncovered

  Scenario: Recognize a nested descendant component
    Given a safe retained path "docs/engineering/example/evidence/archive/WO-ABC-001/check.md"
    When every evidence-attribution surface assesses the path
    Then every surface associates it with "WO-ABC-001"

  Scenario: Ignore a misleading ancestor before evidence
    Given a safe retained path "docs/engineering/WO-ABC-001/evidence/check.md"
    When every evidence-attribution surface assesses the path
    Then no surface associates it with "WO-ABC-001"

  Scenario Outline: Reject inexact component matches
    Given a safe retained path "<path>"
    When every evidence-attribution surface assesses the path
    Then no surface associates it with "WO-ABC-001"

    Examples:
      | path |
      | docs/engineering/example/evidence/X-WO-ABC-001/check.md |
      | docs/engineering/example/evidence/wo-abc-001/check.md |
      | docs/engineering/example/evidence/WO-ABC-0010/check.md |
      | docs/engineering/example/evidence/WO-ABC-001_check.md |

  Scenario: Deduplicate repeated exact keys
    Given a safe retained path "docs/engineering/example/evidence/WO-ABC-001/WO-ABC-001-check.md"
    When every evidence-attribution surface assesses the path
    Then every surface reports exactly one association with "WO-ABC-001"

  Scenario: Associate every distinct explicit key
    Given a safe retained path "docs/engineering/example/evidence/WO-ABC-001/WO-XYZ-002-check.md"
    When every evidence-attribution surface assesses the path
    Then every surface reports the ordered keys "WO-ABC-001, WO-XYZ-002"

  Scenario: Accept a mixed-layout aggregate candidate
    Given one selected work order has flat keyed evidence
    And another selected work order has directory-keyed evidence
    And all existing artifact, path, Git, and lifecycle checks pass
    When aggregate verification is captured and the resulting record is validated
    Then one ready record contains both exact evidence paths
    And formal validation reports no uncovered work order
    And no partial or authority-bearing side effect occurs

  Scenario: Preserve unsafe-path rejection
    Given an unsafe evidence path contains an exact work-order-looking component
    When capture or validation assesses the path
    Then the existing path-safety diagnostic remains blocking
    And the key match does not qualify the evidence

  Scenario: Clear only the false missing-evidence finding
    Given an implemented work order has safe directory-keyed evidence
    When inspection and Harness Explorer assess the repository
    Then "W-HEX-001" is absent for that work order
    And its exact path appears as retained readiness evidence
    And no verification or release authority is inferred
