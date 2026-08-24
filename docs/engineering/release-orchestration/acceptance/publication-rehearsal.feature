Feature: Rehearse the credential-free publication path on both runner platforms
  The repository exercises every credential-free publication mechanic on the
  Linux and the Windows runner type before release approval, without changing
  the release orchestrator and without acquiring any credential.

  Scenario: Windows exercises the mechanics publication performs only on Linux
    Given the release orchestrator proves evaluator identity only on ubuntu-latest
    When the rehearsal runs on the Windows runner type
    Then it resolves the Scripts virtual-environment layout
    And it proves evaluator identity after verifying the public wheel digest
    And it reports the evaluator mechanics as executed on Windows

  Scenario: Linux exercises the mechanics publication performs only on Windows
    Given the release orchestrator exports, builds, normalizes, and verifies only on windows-2022
    When the rehearsal runs on the Linux runner type
    Then it completes candidate export, build, sdist normalization, and bundle verification
    And it invokes no cygpath and no POSIX-only utility absent from a Windows runner
    And it reports those mechanics as executed on Linux

  Scenario: Temporary-path identity is asserted, not assumed
    Given a rehearsal root reached through an alias such as a Windows 8.3 short name
    When the rehearsal canonicalizes its root and sets the platform temporary variables
    Then a child process reports the same temporary root the rehearsal set
    And a mismatch fails as a temporary-path identity divergence

  Scenario: Determinism is proven between two independent builds
    Given the candidate is exported twice from the same commit
    When each tree is built with the pinned build tools and its sdist normalized
    Then the wheel and the normalized sdist of the two sets compare byte-identical
    And a difference fails reporting the first differing offset and both digests

  Scenario: Bundle verification cross-checks independent builds
    Given two independent distribution sets for the same candidate in candidate mode
    When the bundle manifest and plan are derived from the first set
    Then the second set is verified against that manifest
    And the result states that only release-record mode compares against an authorized release identity

  Scenario: Teardown does not escape the rehearsal root
    Given a derived tree containing a virtual environment with links
    And a link inside that tree pointing outside the rehearsal root
    When teardown runs
    Then every derived tree is removed by unlinking links rather than following them
    And no path outside the rehearsal root is deleted
    And the repository worktree is reported clean with no untracked residue

  Scenario: A release owner rehearses a prepared record before approving it
    Given a prepared release record committed to the repository
    When the release owner dispatches the rehearsal in release-record mode
    Then the plan is resolved through the orchestrator's own resolution command
    And the assembled bundle is verified against that record's bound distribution identity
    And no tag, release, index object, deployment, or lifecycle transition is created

  Scenario: Publication gaining an unrehearsed credential-free step fails closed
    Given a credential-free orchestrator job invokes a mechanic absent from the declaration
    When the divergence check runs
    Then it fails and names the mechanic, its orchestrator location, and the uncovered direction

  Scenario: A declaration entry publication no longer performs fails closed
    Given the declaration names a mechanic the orchestrator no longer invokes
    When the divergence check runs
    Then it fails and reports the declaration entry as stale

  Scenario: Credential-bearing jobs are excluded and reported
    Given a job declares a write permission, an id-token permission, an environment, a token, or an external-state-mutating action
    When the divergence check classifies orchestrator jobs
    Then that job's mechanics are excluded from the required rehearsal set
    And the exclusion is reported together with the attribute that caused it

  Scenario: Exclusion reaches a job that holds no credential of its own
    Given a job declares contents read only but needs a job that was excluded
    When the divergence check classifies orchestrator jobs
    Then that job is excluded as well
    And the reported attribute names the excluded dependency rather than a permission

  Scenario: A declared step that changes without changing a command fails closed
    Given a declared credential-free step gains an argument and still invokes only declared commands
    When the divergence check runs
    Then it fails because the step's normalized run digest no longer matches the declared digest
    And it names the job, the step, and both digests

  Scenario: An action surface is classified and pinned
    Given a rehearsed job uses an action that is undeclared or not pinned to a full commit
    When the divergence check runs
    Then it fails naming the job, the step, and the action
    And a credential-free job cannot gain a publication mechanic through a marketplace action unnoticed

  Scenario: A mechanic cannot claim a realization surface that does not exist
    Given a declared mechanic names a realization surface outside the declared vocabulary
    When the declaration is loaded
    Then it is refused before any comparison runs

  Scenario: A mechanic with no valid subject is excluded rather than failed
    Given the run resolved the governing evaluator from the schema-three lock
    And no committed released record binds that evaluator as its predecessor
    When the rehearsal reaches the predecessor-view qualification in candidate mode
    Then it reports the mechanic as excluded
    And the reason names the resolved evaluator identity and the record's own
    And release-record mode against a record under preparation still fails on a mismatch

  Scenario: Teardown's audit accepts the removal of the root itself
    Given teardown has removed every derived tree and then the rehearsal root
    When the post-audit re-examines every reported deletion
    Then the root's own entry is accepted although its parent lies outside the root
    And any other reported deletion outside the root is refused

  Scenario: An inherited checkout that converts line endings is reported
    Given the repository is checked out with line-ending conversion enabled
    When the candidate checkout is created the way publication creates it
    Then the result reports the inherited conversion setting
    And a byte-exact assertion failing for that reason is attributable to the checkout

  Scenario: An inherited dirty checkout is reported rather than misread
    Given the rehearsal runs locally in a worktree with uncommitted changes
    When a mechanic requires a clean worktree and therefore fails
    Then the result reports the inherited checkout condition and the uncommitted entry count
    And the failure is attributable to the checkout rather than to the publication path

  Scenario: The declaration cannot satisfy itself
    Given the declaration of covered mechanics
    When it is inspected
    Then it contains only data
    And a declaration containing executable logic fails the check

  Scenario: The release orchestrator is unchanged
    Given the rehearsal and its divergence check exist
    When the release orchestrator is compared with its merge-base content
    Then it is byte-identical
    And its single release_record input, permissions, and job structure are unchanged

  Scenario: The rehearsal holds no publication authority
    Given any rehearsal outcome, successful or failed
    When the lane permissions and external state are inspected
    Then the lane declares contents read only with no environment, secret, or token
    And no tag, branch, release, index upload, deployment, environment approval, or artifact lifecycle transition exists as a result

  Scenario: The rehearsal stays repository specific
    Given a consumer installs or upgrades SE Harness
    When its package, managed templates, and workflows are inspected
    Then no publication-rehearsal behavior is present
    And harnessctl exposes no rehearsal command or option
