Feature: Governed PyPI Trusted Publishing
  An accountable release owner can promote exact verified GitHub release assets
  without rebuilding them or storing a PyPI credential.

  Scenario: Exact final release is eligible for approved publication
    Given a final GitHub release tag and independently retained wheel and sdist hashes
    And the downloaded checksum manifest contains exactly those files and hashes
    And the protected pypi environment approves the deployment
    When the pinned Trusted Publishing action runs
    Then only the existing wheel and source distribution are submitted to PyPI
    And metadata verification and attestations remain enabled

  Scenario: Artifact identity mismatch stops publication
    Given a selected release asset differs from an independently retained hash
    When publication preflight runs
    Then the workflow fails before the publisher step
    And it does not rebuild or replace the asset

  Scenario: Publication capability does not grant authority
    Given the workflow and pypi environment are configured
    But no separate release-owner publication authorization names the tag and hashes
    Then no workflow dispatch is authorized

  Scenario: Existing PyPI filename is not ignored
    Given PyPI already contains a distribution filename for the selected version
    When the publisher reports the duplicate
    Then the workflow fails visibly
    And correction requires a new verified version
