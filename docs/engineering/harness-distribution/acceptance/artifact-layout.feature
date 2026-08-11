Feature: Organize and author governed artifacts consistently

  Scenario: Scaffold a canonical engineering domain
    Given a repository with the standard harness installed
    When a coding agent scaffolds the domain "simulation"
    Then the canonical domain organization is planned safely
    And an absent repository-owned domain index is seeded
    And no product artifact or approval is invented

  Scenario: Create an incomplete draft artifact
    Given the canonical domain "simulation"
    When a coding agent creates requirement "REQ-MOK-012"
    Then the artifact is created under "simulation/requirements"
    And it uses the canonical requirement template
    And its lifecycle status is "draft"
    And accountable fields still require completion and validation

  Scenario: Reject an unsafe or conflicting authoring request
    Given an untrusted domain, identifier, parent chain, or destination
    When a coding agent plans a scaffold or artifact creation
    Then traversal and containment are checked before writing
    And existing repository content is not overwritten
    And a rejected operation leaves no partial files

  Scenario: Co-locate single-domain provenance
    Given all selected work orders belong unambiguously to "simulation"
    When verification or release provenance is prepared without an explicit output
    Then the record defaults to the matching domain record directory
    And its relations and authority remain metadata-driven

  Scenario: Preserve a repository-wide aggregate record
    Given selected work spans "simulation" and "billing"
    When verification or release provenance is prepared without an explicit output
    Then the record defaults to the repository-wide aggregate directory
    And no common domain is guessed

  Scenario: Diagnose a valid legacy flat layout
    Given a valid requirement directly below the "simulation" domain
    When artifact validation and doctor diagnostics run
    Then the requirement remains in the authoritative graph
    And validation remains successful
    And a nonblocking advisory reports its canonical destination

  Scenario: Preserve repository-owned artifacts during upgrade
    Given a harness installation with flat and canonical owner artifacts
    When the harness is upgraded
    Then owner artifact bytes and paths remain unchanged
    And existing domain indexes remain unchanged

  Scenario: Keep metadata and relations authoritative
    Given an artifact is stored in a canonical directory
    But its metadata or required relations are invalid
    When the graph is validated
    Then the artifact remains invalid
    And its path does not supply approval or repair the graph
