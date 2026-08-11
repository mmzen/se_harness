Feature: Qualify and release multiple governed work items as one version

  Scenario: Capture a final aggregate candidate
    Given multiple active release-bearing work orders with declared verification contracts
    And retained evidence for each work order at one clean final candidate commit
    When aggregate verification is captured with explicit repeated options
    Then one ready verification record lists the complete work, contract, and evidence sets
    And the record names the clean final candidate commit
    And no Git state or approval is changed

  Scenario: Prepare an aggregate release
    Given aggregate verification records that cover the selected work at one candidate commit
    And an active release contract that gates every selected work order
    When an aggregate release is prepared
    Then one ready release record lists the exact verified work set
    And it names the same candidate commit and object format

  Scenario: Reject incomplete aggregate scope
    Given selected work, verification, evidence, and release gates that do not describe the same scope
    When verification capture, release preparation, or graph validation runs
    Then a blocking diagnostic identifies the inconsistent IDs
    And no partial record is created

  Scenario: Preserve a single-work-order workflow
    Given one active work order, one verification contract, and one evidence path
    When the existing command shape is invoked once for each option
    Then the ready verification and release records remain valid aggregates of cardinality one

  Scenario: Keep governance outside the release payload
    Given publication and approval work orders created after the candidate
    When release lineage is inspected
    Then those governance records remain auditable on the governing branch
    But they are not automatically listed as released work or included in the candidate wheel
