Feature: Install and understand SE Harness from its released package
  A repository owner can discover, install, and operate the released harness
  without cloning candidate source or confusing package and repository state.

  Scenario: Install the released package in a Windows virtual environment
    Given Python 3.11 or later and a new local virtual environment
    When the user installs se-harness from PyPI
    Then the README explains how to activate the environment
    And harnessctl is discoverable in the environment Scripts directory
    And the user can invoke the same CLI through the environment interpreter

  Scenario: Start with either a new or existing repository
    Given the released harness CLI is available
    When the user reads the quick start
    Then init is identified for an absent or empty repository
    And adopt is identified for an existing repository
    And doctor and dashboard are the first observation commands
    And installation is not described as product or release authority

  Scenario: Upgrade the package without mutating a repository
    Given an existing harness-enabled repository
    When the user upgrades the se-harness Python package
    Then the CLI and canonical distribution available to the environment change
    But the target repository remains unchanged
    And a separate upgrade plan and explicit apply are required

  Scenario: Expose public metadata in the next release
    Given the root README and license exist
    When static project metadata is inspected
    Then the README is selected as the Markdown long description
    And canonical project, repository, issue, and release URLs are present
    And the existing Python requirement, empty runtime dependencies, and harnessctl entry point remain unchanged
    But no existing PyPI release is claimed to have changed

  Scenario: Keep version and baseline statements truthful
    Given package metadata declares one current version
    When public documentation is validated
    Then the exact installation example names the same version
    And conceptual CI text refers to the configured released baseline
    And the workflow remains the observation of the current exact pin
    And README changes do not advance that pin

  Scenario: Understand the value without operating the control plane manually
    Given a repository owner delegates a representative engineering change to a coding agent
    When the user reads the practical README example
    Then the agent prepares and executes only an approved governed scope
    And the user retains work approval, assurance, and release decisions
    And the resulting graph connects purpose, evidence, and the exact candidate revision
    And Harness Explorer exposes traceability, readiness, and anomalies
    And the explanation remains useful when Mermaid is displayed as source
