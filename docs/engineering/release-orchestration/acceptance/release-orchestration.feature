Feature: Deterministic released-record publication
  A release owner can complete the SE Harness last mile from one released RLS
  without re-entering governed identities or weakening publication boundaries.

  Scenario: One released record drives a complete release
    Given a released RLS is integrated into main with exact distribution provenance
    When the release owner dispatches the workflow with that RLS identifier
    Then the version, tag, commits, verification records, filenames, and hashes are derived
    And exact GitHub, PyPI, Pages, and public-install outcomes are reported separately

  Scenario: A ready or branch-only release record is refused
    Given the selected RLS is not released in trusted main history
    When orchestration resolves the request
    Then it fails before candidate execution or external mutation

  Scenario: Candidate bytes must reproduce the release record
    Given the selected RLS carries a complete distribution block
    When the exact candidate is built twice at its recorded epoch
    Then both wheels and normalized sdists are byte-identical
    And their hashes equal the release record

  Scenario: Candidate code cannot enter a credential boundary
    Given the workflow contains qualification and publication jobs
    When permissions and executed content are inspected
    Then candidate code runs only in jobs without write, OIDC, or Pages permissions

  Scenario: Exact GitHub state is replayable
    Given the tag and final GitHub Release already match the released RLS exactly
    When orchestration is replayed
    Then the GitHub stage is observed as complete without replacing any state

  Scenario: Mismatched immutable state stops
    Given an existing tag or final release asset differs from the released RLS
    When orchestration reconciles GitHub state
    Then it fails without moving the tag, replacing assets, or deleting the release

  Scenario: Exact PyPI state is not uploaded twice
    Given both expected PyPI files already exist with exact hashes
    When orchestration reaches PyPI reconciliation
    Then it reports the stage complete without invoking the publisher
    And publisher-side duplicate suppression remains disabled

  Scenario: Partial PyPI state requires accountable disposition
    Given only one expected distribution exists on PyPI
    When orchestration reaches PyPI reconciliation
    Then it stops and records partial immutable state

  Scenario: Pages deploys from main governance context
    Given the GitHub Release is complete and the released RLS governance commit is known
    When the orchestrator generates the demonstration
    Then the main-authorized Pages job deploys that immutable governance snapshot
    And a tag-ref release event cannot independently deploy it

  Scenario: Pages failure does not falsify package success
    Given GitHub and PyPI publication succeeded but Pages deployment failed
    When the result is reported
    Then package stages remain complete and Pages remains failed
    And a bounded Pages-only replay is available for the same identities
