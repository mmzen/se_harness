# SE Harness — KISS codebase review

The next simplification should remove proof and paperwork from ordinary work. Keep a small core: one selected task, readable acceptance checks, the tested code reference, and your explicit decision.

Reviewed current main `93677e69dacb08367a7079e3372118c5064087c8` after PR #465. This report contains **38 simplification candidates and 7 protections to retain**. The earlier plugin locks and automatic hooks are already removed and are not counted again.

This is analysis, not an approved work order. No product code, managed files, tests or lifecycle records were changed.

## Start here

1. **Remove accidental blockers:** CRLF rejection, raw instruction-byte limits, strict evidence headers and the dashboard prerequisite.
2. **Make local work independent of GitHub availability:** retain owner authorization, move CI enforcement to integration, and scope evidence to the actual change.
3. **Shrink runtime identity checks:** keep the selected checker’s origin/version; stop hashing Python and the full installation for ordinary writes.
4. **Move release rehearsal to release-related changes:** stop retesting an old release and rebuilding twice on every ordinary PR. Make interrupted draft publication resumable.
5. **Delete the tests of removed machinery:** retain behavior and real failure tests, not exact internal call shapes or prose.

These are candidate work packages, not newly created formal work orders. No speedup or line-removal total is promised before implementing and measuring them.

## Concrete examples reproduced

| Input | Current result |
| --- | --- |
| PR work-order line with LF | Accepted |
| Same line with CRLF | Refused with W-ADS-001 |
| docs/notes/draft.md | Accepted as a changed path |
| docs/notes/[draft].md | Refused with WEX200 |
| Four-field evidence header | Accepted |
| Same header plus notes = "reviewed" | Refused with WEX-ECP-010 |
| Identical owner instructions | 5,957 LF bytes pass the size rule; 6,024 CRLF bytes fail |

The machine-readable companion contains the direct observations. These were small read-only probes, not a rerun of the full test suite.

## What the scores mean

**Complexity:** 1 = small/local; 3 = several moving parts; 5 = cross-cutting machinery. **Value:** 1 = little benefit for your one-user project now; 3 = useful but disproportionate; 5 = protects a concrete outcome. Both are judgments, not measurements. Score the current mechanism, not the importance of its stated goal.

**First** means the strongest simplification targets. **Later** means the tradeoff needs a focused product choice. **Keep** means retain the useful protection. A low value score does not prove a scenario impossible.

## What “hypothetical” means here

Some cases defend against local package tampering, obscure runtime layouts or inconsistent metadata. They are technically possible; I found no user-frequency data showing that they justify all this machinery for one development user. The recommendation is proportionality, not a claim that they can never happen.

Other cases are completely ordinary: Windows newlines, interrupted uploads and owner edits. In those cases the rigid response is the problem. The authoring word budgets are mostly **advisories**, and the Python-binary hash is mainly an **observation**; they are not all execution blockers.

The remaining “locks” mostly describe managed files and the selected evaluator. I found no remaining general plugin migration mutex or cryptographic signing system in the runtime/repository/publication Python searched. SHA-256 values show whether bytes match; they do not prove that a person approved an action. Atomic writes and ordinary rollback are listed separately as useful protections.

## Size and test inventory

| Area | Python files | Python lines |
| --- | --- | --- |
| Runtime package | 50 | 21,375 |
| Repository tools | 10 | 3,481 |
| CLI/build scripts | 9 | 1,752 |
| GitHub helper scripts | 4 | 2,841 |
| Tests and Python test support | 154 | 37,585 |

The nine tracked workflow files total 2,188 lines. Static parsing found 1,221 test-method definitions under tests; this is not a discovered/executed test count and does not count loop iterations. Fixture JSON/Markdown and vendored JavaScript are excluded from the Python line table. Line counts include comments and blank lines.

The current Git tree contains 10,093 files and 250.44 MiB of blob content. Engineering evidence accounts for 7,714 files and 232.53 MiB. These sizes exclude Git history and filesystem overhead. Historical evidence is a storage opportunity, not permission to delete records.

## Test clusters to inspect first

| Test module | Methods / lines | What to simplify |
| --- | --- | --- |
| test_hash_bound_integrity.py | 98 / 1,445 | Central checksum registry, attribute placement, checkout matrix and source-shape checks. |
| test_interpreter_safety.py | 64 / 1,158 | Linked interpreter restrictions, simulated capability combinations and AST inventories. |
| test_workflow_execution.py | 70 / 1,719 | Exact result wording and protocol details; retain real lifecycle outcomes and atomic failure tests. |
| test_workflow_compliance.py | 42 / 1,004 | Handoff header/freshness machinery; retain actual scope checks. |
| test_revision_provenance.py | 38 / 1,112 | Dashboard coupling and repeated candidate-record preparation; retain tested-code identity. |
| test_instruction_architecture.py | 31 / 1,135 | Byte limits and literal instruction/workflow text; retain correct routing and fragment preservation. |
| test_release_orchestration.py | 32 / 872 | Partial-draft refusal and extra-asset refusal; retain wrong-package and credential-boundary tests. |

These are module sizes, not proposed deletions. The modules contain useful tests too, and method counts do not include subcases.

## Detailed findings


## Everyday friction


### KISS-01 — Windows line endings reject a valid PR declaration

**First · Complexity 2/5 · Value 1/5 · Hard blocker**

**Example:** The same Harness-Work-Order line passes with LF and fails with CRLF.

**Current behavior:** The selector detects the carriage return and tells the author to rewrite the PR body. Directly reproduced.

**Assessment:** This is normal Windows text, not a different work order. The special rejection creates a problem the parser could avoid.

**Recommendation:** Normalize line endings before reading the declaration. Keep rejection of missing, conflicting or malformed IDs. One LF/CRLF equivalence test is enough.

Evidence: [se_harness/github_ci.py:49](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/github_ci.py#L49), [tests/test_instruction_architecture.py:680](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_instruction_architecture.py#L680).


### KISS-02 — A byte budget fails identical owner instructions

**First · Complexity 2/5 · Value 1/5 · Test blocker**

**Example:** The committed owner text is 5,957 bytes with LF and 6,024 with CRLF. The test demands less than 6,000.

**Current behavior:** The test counts raw UTF-8 bytes outside the managed markers. Directly reproduced from committed text; this also interrupted our previous local implementation run.

**Assessment:** Keeping instructions short is useful. Failing CI because of checkout newlines is not.

**Recommendation:** Make length a review hint, or count normalized words. Keep the test that owner edits leave the managed block intact.

Evidence: [tests/test_instruction_architecture.py:943](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_instruction_architecture.py#L943), [tests/test_instruction_architecture.py:933](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_instruction_architecture.py#L933).


### KISS-03 — Literal filenames are treated like unsafe patterns

**First · Complexity 3/5 · Value 2/5 · Hard blocker**

**Example:** docs/notes/[draft].md is rejected. A relative Windows path with backslashes is also rejected.

**Current behavior:** The change-set parser bans brackets and backslashes before checking scope. Directly reproduced; this is about declaring changed paths, not deleting files.

**Assessment:** A literal bracket is a valid filename. Input normalization and wildcard interpretation have been mixed together.

**Recommendation:** Accept literal paths from Git. Normalize native separators at the CLI boundary; keep traversal and outside-root rejection. Test real scope escapes, not every harmless spelling.

Evidence: [se_harness/workflow_change_set.py:42](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/workflow_change_set.py#L42), [tests/test_workflow_compliance.py:86](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_workflow_compliance.py#L86).


### KISS-04 — One PR can name only one work order

**Later · Complexity 2/5 · Value 3/5 · Hard blocker**

**Example:** A small change touches two independently approved work orders and names both in its PR body.

**Current behavior:** The selector requires exactly one standalone declaration. The regression test explicitly rejects two.

**Assessment:** Bounded scope is useful. A universal one-work-order PR rule is a process choice, not a safety property.

**Recommendation:** Keep one selected work order as the ordinary route. If multi-work-order delivery is needed, accept an explicit list and check its combined scope; do not add an elaborate aggregation protocol now.

Evidence: [se_harness/github_ci.py:49](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/github_ci.py#L49), [tests/test_instruction_architecture.py:694](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_instruction_architecture.py#L694).


### KISS-05 — Delegation must already exist on the base branch

**First · Complexity 4/5 · Value 2/5 · Delegated-route blocker**

**Example:** You approve a work order and ask the agent to execute it in the same branch.

**Current behavior:** The delegation code reads the work order from merge-base, not just the approved branch. Missing base approval denies the delegated route.

**Assessment:** Preventing an agent from inventing its own permission is sensible. Requiring a preliminary merge for this one-owner project adds a delivery round trip.

**Recommendation:** Use one explicitly owner-approved scope as the authorization record. Retain the owner decision, but stop making a separate base-branch merge the only way to express it.

Evidence: [se_harness/gate_source.py:154](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/gate_source.py#L154), [se_harness/gate_source.py:261](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/gate_source.py#L261).


### KISS-06 — Local progress depends on a live GitHub check

**First · Complexity 4/5 · Value 2/5 · Delegated-route blocker**

**Example:** The work and tests are ready, but GitHub is unavailable or the latest documentation commit is still queued.

**Current behavior:** Delegated start, completion and verification preparation query the exact HEAD check and require success. HTTP errors, missing checks and pending checks refuse the action.

**Assessment:** CI is valuable at integration. Making local bookkeeping depend on a fresh network response is fragile. The outage is real; an attacker changing approval is only one possible threat.

**Recommendation:** Keep the CI gate at merge/publication. Let an explicitly authorized local task progress using its retained test result; show CI status separately.

Evidence: [se_harness/gate_source.py:177](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/gate_source.py#L177), [se_harness/gate_source.py:217](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/gate_source.py#L217).


### KISS-07 — A handoff note needs an exact machine header

**First · Complexity 3/5 · Value 1/5 · Evidence-path blocker**

**Example:** Add notes = "reviewed" to an otherwise valid handoff header: it is rejected.

**Current behavior:** The header must start at byte zero, use exact LF fences, and contain exactly four keys. Directly reproduced for the extra key.

**Assessment:** The selected work order and evidence location matter. Exact presentation bytes and refusal of harmless extra metadata do not add comparable value.

**Recommendation:** Use a simple evidence reference in the work order. If metadata remains, parse required fields and tolerate additional descriptive fields.

Evidence: [se_harness/workflow_evidence_packet.py:25](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/workflow_evidence_packet.py#L25), [tests/test_workflow_compliance.py:437](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_workflow_compliance.py#L437).


### KISS-08 — Unrelated artifact edits invalidate handoff freshness

**First · Complexity 4/5 · Value 2/5 · Rebinding and refusal paths**

**Example:** Another task edits its requirement while you prepare a handoff for your own work.

**Current behavior:** The formal snapshot hashes every artifact passed from the full report. Handoff code then rebinds the header to the new snapshot and checks Git newline attributes.

**Assessment:** This assumes every artifact edit can change the meaning of your selected evidence. The code already knows the selected dependencies.

**Recommendation:** Bind evidence to the tested code and the governing inputs it actually uses. Remove global-snapshot freshness from ordinary handoff notes.

Evidence: [se_harness/workflow_change_set.py:218](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/workflow_change_set.py#L218), [se_harness/workflow_compliance.py:352](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/workflow_compliance.py#L352), [tests/test_workflow_compliance.py:562](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_workflow_compliance.py#L562).


### KISS-09 — Recording verification depends on building the dashboard

**First · Complexity 4/5 · Value 1/5 · Hard blocker**

**Example:** Tests pass, but dashboard generation fails or its manifest is missing.

**Current behavior:** capture-verification calls the dashboard generator to get a snapshot digest. Generation failure prevents the record. A regression test explicitly preserves this refusal.

**Assessment:** The UI is useful for viewing evidence. It should not be a prerequisite for recording that evidence.

**Recommendation:** Create the verification record from the selected structured data. Generate the dashboard separately, when requested.

Evidence: [se_harness/provenance.py:334](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/provenance.py#L334), [tests/test_revision_provenance.py:775](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_revision_provenance.py#L775).


### KISS-10 — An unrelated untracked file blocks evidence capture

**Later · Complexity 2/5 · Value 3/5 · Hard blocker**

**Example:** You have a scratch note in the repository while recording tests for a committed candidate.

**Current behavior:** The clean-worktree check includes every untracked file. Any output from git status refuses capture.

**Assessment:** Knowing which code was tested is essential. Requiring unrelated scratch files to disappear is a broader restriction.

**Recommendation:** Keep a clean committed candidate as the default. Allow evidence capture from that exact commit in a temporary worktree, or report unrelated files without treating them as part of the candidate.

Evidence: [se_harness/provenance.py:102](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/provenance.py#L102), [tests/test_revision_provenance.py:759](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_revision_provenance.py#L759).


### KISS-11 — Checks require the caller to understand internal procedure names

**First · Complexity 4/5 · Value 2/5 · Hard blocker**

**Example:** You ask for a pre-action check but omit --procedure, even though the tool has already selected a procedure.

**Current behavior:** The check code resolves the current workflow rule, then requires an explicit procedure for pre-action. Unsupported checkpoint/type combinations are separately refused.

**Assessment:** A safe next action is useful. Requiring users and agents to repeat a computed internal identifier creates avoidable wrong-command failures.

**Recommendation:** Expose one check for the selected artifact and return the next action. Keep specialized checkpoints as an internal implementation detail where possible.

Evidence: [se_harness/workflow_compliance.py:531](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/workflow_compliance.py#L531), [tests/test_workflow_compliance.py:155](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_workflow_compliance.py#L155).


### KISS-12 — Preflight collects errors from the whole repository

**First · Complexity 3/5 · Value 2/5 · Preflight blocker**

**Example:** An unrelated draft has a semantic error while you are working on a different approved task.

**Current behavior:** run_preflight adds every validation error to its diagnostics. In contrast, the selected workflow layer already distinguishes scoped, repository and unrelated findings.

**Assessment:** Unreadable structure and duplicate IDs can affect everyone. An unrelated semantic problem should not always stop the selected work.

**Recommendation:** Use the existing scoped diagnostic split in preflight too. Keep global blockers for genuinely ambiguous repository structure.

Evidence: [se_harness/preflight.py:539](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/preflight.py#L539), [se_harness/repository_graph.py:130](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/repository_graph.py#L130).


## Locks and identity


### KISS-13 — Every new checksum field needs central classification

**First · Complexity 4/5 · Value 1/5 · Integrity/test blocker**

**Example:** An evidence artifact gains a new field named novel_payload_sha256.

**Current behavior:** The checker scans tracked artifact metadata for *_sha256 fields and fails when a field belongs to neither a declared class nor an exemption. Tests even scan historical evidence trees.

**Assessment:** A checksum is useful when a specific consumer verifies it. A registry of every checksum name adds maintenance without proving the claim behind the bytes.

**Recommendation:** Let each format validate the checksums it actually consumes. Remove the global field-name census and its exemptions.

Evidence: [se_harness/hash_bound.py:431](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/hash_bound.py#L431), [tests/test_hash_bound_integrity.py:633](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_hash_bound_integrity.py#L633).


### KISS-14 — Correct Git attributes can still be in the wrong section

**First · Complexity 4/5 · Value 1/5 · Integrity blocker**

**Example:** A byte-preservation rule is present and works, but sits in the owner region instead of the template region.

**Current behavior:** The hash-bound check verifies both the effective Git attributes and the physical declaration region. It can reject a rule for placement.

**Assessment:** Preventing unwanted newline conversion is useful for exact binary evidence. The location of an otherwise effective rule adds another policy layer.

**Recommendation:** Check the bytes that matter, or the effective attribute once. Remove region ownership as a separate integrity condition.

Evidence: [se_harness/hash_bound.py:476](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/hash_bound.py#L476), [tests/test_hash_bound_integrity.py:879](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_hash_bound_integrity.py#L879).


### KISS-15 — A normal Python environment under a linked directory is refused

**First · Complexity 4/5 · Value 2/5 · Runtime blocker**

**Example:** Your tools directory is a Windows junction or a symbolic link to another disk.

**Current behavior:** Interpreter validation walks enclosing directories and rejects links, even when the executable resolves correctly outside the target repository.

**Assessment:** Links at deletion destinations are dangerous. Links in the location of a deliberately selected interpreter are a different, lower-value restriction.

**Recommendation:** Resolve the selected executable once and verify the actual import origin. Keep isolation from candidate code; permit ordinary linked tool directories.

Evidence: [se_harness/interpreter_safety.py:242](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/interpreter_safety.py#L242), [tests/test_interpreter_safety.py:887](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_interpreter_safety.py#L887).


### KISS-16 — The Python executable is hashed during runtime identity inspection

**First · Complexity 3/5 · Value 1/5 · Extra work and refusal paths**

**Example:** A command records the checksum of the Python binary in addition to the checker identity.

**Current behavior:** Interpreter evaluation reads and hashes the resolved executable. Runtime identity records that observation for every role that can be inspected successfully.

**Assessment:** This is an observation, not proof that the executable is trusted. No allowed Python-binary digest is compared here. It adds I/O and a readability/size failure path.

**Recommendation:** Remove the Python-binary digest from ordinary commands. Record the Python version for troubleshooting; identify the installed checker where its version matters.

Evidence: [se_harness/interpreter_safety.py:333](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/interpreter_safety.py#L333), [se_harness/runtime_identity.py:186](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/runtime_identity.py#L186).


### KISS-17 — An ignored PYTHONPATH still causes refusal

**First · Complexity 3/5 · Value 1/5 · Runtime blocker**

**Example:** Python is launched with -I, but the parent process has a nonempty PYTHONPATH variable.

**Current behavior:** Runtime identity checks whether the environment variable is present, independently of whether isolated Python uses it, and emits RID008.

**Assessment:** Checking effective imports protects against running the wrong code. Rejecting an ignored variable is weaker evidence of a problem.

**Recommendation:** Check the effective search path and imported module origin. Do not fail solely because an unused environment variable exists.

Evidence: [se_harness/runtime_identity.py:178](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/runtime_identity.py#L178), [se_harness/runtime_identity.py:219](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/runtime_identity.py#L219), [tests/test_mutation_guard.py:323](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_mutation_guard.py#L323).


### KISS-18 — A module command also requires the console launcher

**First · Complexity 3/5 · Value 1/5 · Mutation blocker**

**Example:** python -I -m se_harness works, but the harnessctl wrapper is absent.

**Current behavior:** The mutation guard supplies require_entry_point=True. Identity checking then refuses when it cannot find the console entry point.

**Assessment:** The current command is already running through the selected Python module. An unused alternate launcher should not decide whether it can work.

**Recommendation:** Validate the route actually invoked. Check the console script when using the console script, and the module when using the module.

Evidence: [se_harness/mutation_guard.py:106](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/mutation_guard.py#L106), [se_harness/mutation_guard.py:121](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/mutation_guard.py#L121), [se_harness/runtime_identity.py:279](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/runtime_identity.py#L279).


### KISS-19 — Ordinary writes recompute the complete installed payload identity

**First · Complexity 5/5 · Value 2/5 · Repeated I/O and mutation blocker**

**Example:** Creating an artifact needs to read and hash the checker package and its templates.

**Current behavior:** Mutation authority calls runtime identity, which calls installed_evaluator_identity and builds a manifest by walking and reading the installed payload.

**Assessment:** Detecting the wrong checker is useful. Reproving the full installed payload on every small write assumes unnoticed local package tampering is a routine event.

**Recommendation:** Keep exact package verification at installation, upgrade and release. For ordinary commands, check version and origin; reserve full integrity inspection for doctor or an explicit check.

Evidence: [se_harness/mutation_guard.py:192](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/mutation_guard.py#L192), [se_harness/runtime_identity.py:296](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/runtime_identity.py#L296), [se_harness/evaluator_identity.py:106](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/evaluator_identity.py#L106), [tests/test_mutation_guard.py:323](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_mutation_guard.py#L323).


### KISS-20 — A valid index install cannot prepare a release without an archive receipt

**First · Complexity 4/5 · Value 2/5 · Release-preparation blocker**

**Example:** The correct checker was installed from the package index, which did not retain a PEP 610 wheel-file digest.

**Current behavior:** Ordinary upgrades accept the missing archive digest, but prepare-release explicitly requires one in the lock. The missing receipt stops that operation.

**Assessment:** Release package identity matters. The installation route of the checker is not the same thing as the identity of the candidate being released.

**Recommendation:** Validate the exact release artifacts separately. Accept the already verified checker payload identity without forcing a reinstall just to obtain an installation receipt.

Evidence: [se_harness/provenance.py:518](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/provenance.py#L518), [se_harness/mutation_guard.py:186](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/mutation_guard.py#L186), [tests/test_mutation_guard.py:284](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_mutation_guard.py#L284).


### KISS-21 — Formatting alone can invalidate evaluator evidence

**First · Complexity 3/5 · Value 1/5 · Evidence blocker**

**Example:** Someone pretty-prints an evaluator-evidence JSON file without changing its values.

**Current behavior:** The parser checks canonical bytes, not just the parsed identity and values. The test explicitly feeds indented JSON and expects rejection.

**Assessment:** Exact file hashes make sense for a published download. For internal structured evidence, formatting can be normalized before comparison.

**Recommendation:** Parse and validate the required values, then canonicalize for hashing. Reject changed identity or duplicate keys; tolerate equivalent whitespace.

Evidence: [se_harness/evaluator_evidence.py:196](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/evaluator_evidence.py#L196), [tests/test_mutation_guard.py:347](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_mutation_guard.py#L347).


### KISS-22 — Guidance, templates and policy are all treated as locked installation bytes

**Later · Complexity 4/5 · Value 3/5 · Upgrade/integrity blocker**

**Example:** An owner improves a managed guide or changes a template locally, then wants an ordinary upgrade.

**Current behavior:** The root lock covers full managed files and fragments. The installer refuses the entire update when any planned item is customized or conflicts.

**Assessment:** Silently overwriting owner content would be wrong. Treating every guidance edit as installed-policy damage also makes early product iteration rigid.

**Recommendation:** Reduce the managed surface to what actually needs machine-enforced versioning. Keep owner settings editable and show explicit replace/keep decisions for customized files. Preserve fragment boundaries.

Evidence: [se_harness/installer.py:573](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/installer.py#L573), [AGENTS.md:27](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/AGENTS.md#L27).


## Release and CI


### KISS-23 — Combining verified work requires all records to name one exact commit

**Later · Complexity 4/5 · Value 3/5 · Release-preparation blocker**

**Example:** Two changes were verified on successive commits and both should ship together.

**Current behavior:** prepare-release rejects multiple candidate identities and requires exact agreement between verified and released work sets.

**Assessment:** The final package must be tested. Recreating all intermediate verification paperwork at the same commit adds administrative work beyond that need.

**Recommendation:** Verify the final release candidate once, with links to earlier evidence. Let prior work records remain historical inputs rather than forcing artificial commit equality between them.

Evidence: [se_harness/provenance.py:551](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/provenance.py#L551), [tests/test_revision_provenance.py:992](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_revision_provenance.py#L992).


### KISS-24 — A rebase can orphan a ready record even when the relevant code is unchanged

**Later · Complexity 3/5 · Value 3/5 · Handoff blocker**

**Example:** A branch is rebased and the old candidate commit is no longer an ancestor of HEAD.

**Current behavior:** Preflight requires a ready record to be verified, rejected or superseded before handoff. It uses commit ancestry rather than equivalence of the tested content.

**Assessment:** Changed code must not inherit an old test result. A commit-ID change can also be bookkeeping only.

**Recommendation:** Offer one explicit refresh of the candidate binding after confirming the relevant tree and governing inputs are unchanged. Keep rerun requirements when content differs.

Evidence: [se_harness/preflight.py:322](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/preflight.py#L322), [tests/test_revision_provenance.py:472](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_revision_provenance.py#L472).


### KISS-25 — Package acceptance snapshots the whole supplied checkout

**First · Complexity 4/5 · Value 2/5 · Acceptance blocker / extra I/O**

**Example:** A test of an installed wheel also reads a large unrelated repository tree to prove it stayed unchanged.

**Current behavior:** The snapshot routine hashes eligible files and refuses over 20,000 files or 250 MiB. The minimal checkout fix avoids the former CI failure, but this mechanism remains.

**Assessment:** Checking that a tool did not alter its target is useful. Repeatedly hashing unrelated history is an unnecessarily broad way to establish that.

**Recommendation:** Use a small disposable target and inspect the paths the operation may touch. Keep bounded inputs, but size them to the actual acceptance scenario.

Evidence: [se_harness/candidate_acceptance.py:222](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/candidate_acceptance.py#L222), [se_harness/candidate_acceptance.py:282](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/candidate_acceptance.py#L282), [.github/workflows/candidate-evidence.yml:159](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/workflows/candidate-evidence.yml#L159).


### KISS-26 — Every PR rehearses two deterministic builds of the candidate

**First · Complexity 4/5 · Value 2/5 · CI cost**

**Example:** A documentation-only PR triggers release recipe replay.

**Current behavior:** Publication Rehearsal runs on every PR and main push. Its candidate leg replays the recipe twice; it does not rerun the full candidate suite in that leg.

**Assessment:** Reproducible release builds have value. Running the same release proof for every ordinary edit has much lower value.

**Recommendation:** Run replay when build inputs or publication code change, and before an actual release. Keep normal PR tests separate.

Evidence: [.github/workflows/publication-rehearsal.yml:22](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/workflows/publication-rehearsal.yml#L22), [.github/workflows/release-qualification.yml:142](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/workflows/release-qualification.yml#L142).


### KISS-27 — Every PR can requalify a previously released candidate

**First · Complexity 5/5 · Value 2/5 · CI cost**

**Example:** A plugin documentation change triggers tests and rebuilds of an older release record selected from the base branch.

**Current behavior:** The second rehearsal leg selects the newest eligible release record. Release-record mode checks out its candidate, runs the full test suite, and replays the build.

**Assessment:** This catches publication regressions when publication code changes. It is mostly unrelated work on a routine product PR.

**Recommendation:** Run this leg on publication-path changes, scheduled compatibility checks if needed, or release preparation. Do not run it unconditionally for every PR.

Evidence: [.github/workflows/publication-rehearsal.yml:95](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/workflows/publication-rehearsal.yml#L95), [.github/workflows/release-qualification.yml:123](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/workflows/release-qualification.yml#L123).


### KISS-28 — An interrupted draft release cannot resume normally

**First · Complexity 4/5 · Value 1/5 · Publication blocker**

**Example:** A network error uploads only some of the expected files into a draft GitHub Release.

**Current behavior:** The classifier reports partial. The publisher accepts only absent or exact states, so rerunning stops instead of uploading the missing files.

**Assessment:** Partial network operations are real and should be easy to retry. A draft release is still reversible.

**Recommendation:** For an unpublished draft, verify existing expected files and upload only missing ones. Keep refusal on conflicting bytes and on attempted replacement of published packages.

Evidence: [.github/scripts/publish_release.py:431](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/scripts/publish_release.py#L431), [.github/workflows/publish-pypi.yml:256](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/workflows/publish-pypi.yml#L256), [tests/test_release_orchestration.py:711](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_release_orchestration.py#L711).


### KISS-29 — An extra GitHub Release attachment is treated as a package mismatch

**First · Complexity 2/5 · Value 1/5 · Publication blocker**

**Example:** The owner attaches a screenshot or a release note alongside the expected wheel, source archive and checksum file.

**Current behavior:** The classifier treats any asset name outside its expected set as mismatched, even when the required files are correct.

**Assessment:** The required package bytes matter. An unrelated attachment does not change those bytes.

**Recommendation:** Validate the required asset subset. Ignore unrelated attachments; still reject conflicting content under a required filename.

Evidence: [.github/scripts/publish_release.py:439](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/scripts/publish_release.py#L439), [tests/test_release_orchestration.py:681](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_release_orchestration.py#L681).


### KISS-30 — Release census turns commit trailers into release prerequisites

**Later · Complexity 4/5 · Value 2/5 · Census-route blocker**

**Example:** A legitimate merge lacks a work-order trailer and the release-unit contract uses the measured census route.

**Current behavior:** The derivation walks first-parent history and merged commits. Untraced commits need full-commit exemptions, and contract gates must equal the measured set.

**Assessment:** This is a real traceability check, not a universal requirement for every contract. For one owner it duplicates reviewing a release diff and listing the included work.

**Recommendation:** Generate the census as review assistance. Let the owner approve the final release scope without hand-maintaining exemptions for harmless integration commits.

Evidence: [se_harness/release_unit.py:117](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/release_unit.py#L117), [se_harness/release_unit.py:155](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/release_unit.py#L155), [tests/test_release_unit.py:213](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_release_unit.py#L213).


### KISS-31 — Historical evidence dominates the current checkout

**First · Complexity 3/5 · Value 2/5 · Storage / checkout cost**

**Example:** A fresh checkout contains about 232.5 MiB under engineering evidence directories.

**Current behavior:** Git tree inventory found 7,714 such files and 243,824,162 bytes: about 92.8% of all tracked blob bytes at this commit. That is current-tree data, not Git history size.

**Assessment:** Past results matter. Retaining full copied trees and repeated raw observations in the normal working tree makes every full checkout heavier.

**Recommendation:** For new runs, retain concise summaries and stable links to downloadable raw artifacts. Review existing large historical bundles for separate archival storage; do not silently delete or rewrite bound evidence.

Evidence: [.github/workflows/release-qualification.yml:70](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/workflows/release-qualification.yml#L70), [docs/engineering/plugin-integration/evidence/WO-PLG-021/implementation/README.md:1](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/docs/engineering/plugin-integration/evidence/WO-PLG-021/implementation/README.md#L1).


## Tests and paperwork


### KISS-32 — Tests enforce internal call shapes and variable names

**First · Complexity 4/5 · Value 1/5 · Refactor/test blocker**

**Example:** A refactor changes how a function obtains an environment root while preserving its behavior.

**Current behavior:** Static tests parse Python ASTs, compare inventories of selected function calls, inspect argument-name fragments, and forbid alternate derivations.

**Assessment:** Preventing duplicated policy can be useful. Exact source-shape tests also fail safe refactors and can pass behaviorally wrong code with the expected shape.

**Recommendation:** Replace these inventories with a few behavior tests at public boundaries. Keep an import-layer rule only where an actual packaging dependency requires it.

Evidence: [tests/test_interpreter_safety.py:1055](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_interpreter_safety.py#L1055), [tests/test_interpreter_safety.py:1077](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_interpreter_safety.py#L1077).


### KISS-33 — Checkout matrices and aggressive Git cleanup preserve the checksum design

**First · Complexity 4/5 · Value 2/5 · Test cost**

**Example:** A test creates one clone per core.autocrlf setting, compares paths and hashes, then runs aggressive Git garbage collection before deleting the clones.

**Current behavior:** FreshCheckoutMatrixTests constructs the matrix in setUpClass and explicitly runs git gc --aggressive --prune=now in tearDownClass.

**Assessment:** A Windows/Linux newline regression test is useful. Much of this matrix exists because the byte-class/attribute system is elaborate; aggressive GC in disposable fixtures is difficult to justify.

**Recommendation:** Remove the aggressive GC. After simplifying text hashing, retain a small LF/CRLF equivalence test and one real checkout test per supported OS.

Evidence: [tests/test_hash_bound_integrity.py:801](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_hash_bound_integrity.py#L801), [tests/test_hash_bound_integrity.py:815](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_hash_bound_integrity.py#L815).


### KISS-34 — The runtime test matrix models combinations rather than supported installations

**First · Complexity 4/5 · Value 2/5 · Test maintenance**

**Example:** Tests simulate combinations of missing pathlib support, missing stat support and observable reparse information.

**Current behavior:** One explicit matrix has eight capability combinations. The interpreter-safety test module contains 64 static test methods plus supporting corpus machinery.

**Assessment:** Some link handling fixes address real portability problems. The abstract route matrix should not become a promise to support every invented runtime shape.

**Recommendation:** Test the interpreters and OSes actually supported. Keep one unavailable-capability failure case and actual escape cases; retire matrices for removed restrictions.

Evidence: [tests/test_interpreter_safety.py:796](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_interpreter_safety.py#L796), [tests/test_interpreter_safety.py:1147](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_interpreter_safety.py#L1147).


### KISS-35 — A requirement must literally contain SHALL

**First · Complexity 2/5 · Value 1/5 · Validation blocker**

**Example:** A clear statement uses “must” instead of “SHALL”.

**Current behavior:** Validation adds an error if the statement lacks the exact uppercase word SHALL.

**Assessment:** A keyword does not establish whether a requirement is clear, testable or useful. This is a document convention enforced as product validity.

**Recommendation:** Move keyword style to optional authoring advice. Keep required intent and a concrete acceptance condition.

Evidence: [se_harness/engine/validation_evidence.py:358](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/engine/validation_evidence.py#L358), [tests/test_authoring_gate.py:1](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_authoring_gate.py#L1).


### KISS-36 — Writing advice is implemented as a detailed grammar engine

**Later · Complexity 4/5 · Value 2/5 · Advisory only**

**Example:** A draft exceeds 30 statement words, three code identifiers or a prescribed number of sentences.

**Current behavior:** The authoring module has separate budgets for requirements, intents, capabilities and specifications, plus paragraph, heading and vocabulary parsing.

**Assessment:** Most of these are draft-only advisories, not hard blockers. Their maintenance cost is real, but they should not be described as stopping execution.

**Recommendation:** Keep a short plain-language checklist and a few high-signal hints. Remove exact sentence/identifier budgets unless users find them useful.

Evidence: [se_harness/engine/validation_authoring.py:45](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/engine/validation_authoring.py#L45), [se_harness/engine/validation_authoring.py:193](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/engine/validation_authoring.py#L193).


### KISS-37 — Recording a risk demands a scoring and sentence format

**Later · Complexity 4/5 · Value 1/5 · Risk-feature blocker**

**Example:** A risk cause has two sentences, or its category is “budget” rather than a closed allowed value.

**Current behavior:** Risk creation requires fixed categories/stages, likelihood and impact from 1–5, computed score, and one-sentence cause/effect. Tests explicitly reject these ordinary descriptions.

**Assessment:** Risks can be real. For one owner, stopping their recording because of wording or a scoring scheme is counterproductive. This only affects users of the risk feature.

**Recommendation:** Allow a short risk description, owner and action first. Make scores and categories optional; create a separate blocking decision only when the owner needs one.

Evidence: [se_harness/risks.py:363](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/risks.py#L363), [se_harness/risks.py:86](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/risks.py#L86), [tests/test_risk_management.py:231](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_risk_management.py#L231).


### KISS-38 — Human-facing response text is part of a checksum protocol

**Later · Complexity 4/5 · Value 2/5 · Protocol/test rigidity**

**Example:** The tool changes a useful response sentence or adds a descriptive result field.

**Current behavior:** Results require exact field sets and one typed next step; a digest is computed over a canonical rendered block. Tests assert exact digest and rendering behavior.

**Assessment:** Stable machine fields and accurate outcomes are valuable. Binding human prose makes communication changes more expensive and creates another place for format disagreements.

**Recommendation:** Hash stable evidence data only where a consumer needs it. Keep machine status and command arguments structured, and let prose evolve without a new proof binding.

Evidence: [se_harness/workflow_result.py:39](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/workflow_result.py#L39), [se_harness/workflow_result.py:129](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/workflow_result.py#L129), [tests/test_workflow_execution.py:1034](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_workflow_execution.py#L1034).


## Keep these protections


### KISS-39 — Prevent writes and deletes outside the selected target

**Keep · Complexity 3/5 · Value 5/5 · Useful boundary**

**Example:** A destination escapes through .., a symbolic link, a junction or a Windows path alias.

**Current behavior:** Destination validation and migration checks prevent operations from landing in unrelated directories.

**Assessment:** This can destroy the owner’s real files, even with one user. It is not an imaginary multi-user threat.

**Recommendation:** Keep a shared, small path boundary check and one real test for each supported escape mechanism.

Evidence: [se_harness/installer.py:581](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/installer.py#L581), [se_harness/integrity.py:39](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/integrity.py#L39), [tests/test_skill_ownership.py:1](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_skill_ownership.py#L1).


### KISS-40 — Preserve owner content outside managed fragments

**Keep · Complexity 3/5 · Value 5/5 · Useful data protection**

**Example:** AGENTS.md contains your own commands around the harness block.

**Current behavior:** Fragment tracking lets the harness update its block without claiming the rest of the file.

**Assessment:** The plugin skills were disposable. Your repository instructions and other project files are not automatically disposable.

**Recommendation:** Keep fragment preservation and explicit conflict handling. Do not apply delete-and-replace to all repository files.

Evidence: [tests/test_instruction_architecture.py:933](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_instruction_architecture.py#L933), [se_harness/installer.py:573](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/installer.py#L573).


### KISS-41 — Write each file atomically and handle an ordinary failure

**Keep · Complexity 3/5 · Value 5/5 · Useful data protection**

**Example:** The process fails while saving a lock or updating related lifecycle records.

**Current behavior:** The code stages writes and can restore prior bytes after an ordinary failure. This is not the removed plugin mutex/journal system.

**Assessment:** Avoiding half-written files is useful. A few shared primitives and focused failure tests justify themselves.

**Recommendation:** Keep atomic replacement and a bounded rollback for actual multi-file edits. Do not add a distributed transaction or crash-state matrix.

Evidence: [se_harness/integrity.py:128](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/integrity.py#L128), [se_harness/workflow.py:654](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/workflow.py#L654), [se_harness/installer.py:691](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/installer.py#L691).


### KISS-42 — Detect wrong or corrupt published packages

**Keep · Complexity 3/5 · Value 5/5 · Useful publication boundary**

**Example:** A download is truncated, changed, or contains different bytes under the expected release filename.

**Current behavior:** Release checks compare the actual files with the approved package identities.

**Assessment:** Package mix-ups and incomplete downloads happen. A checksum at this boundary has a clear purpose.

**Recommendation:** Keep one checksum verification at download/publication and refuse conflicting published bytes. Simplify repeated internal receipts around it.

Evidence: [.github/scripts/publish_release.py:295](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/scripts/publish_release.py#L295), [tests/test_release_orchestration.py:681](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_release_orchestration.py#L681).


### KISS-43 — Keep publication credentials out of candidate test jobs

**Keep · Complexity 3/5 · Value 5/5 · Useful security boundary**

**Example:** Changed source or a workflow step runs code during PR testing.

**Current behavior:** Candidate qualification and privileged publication use separate jobs and permissions.

**Assessment:** One owner still uses third-party dependencies and a hosted runner. Credential separation limits real damage.

**Recommendation:** Keep this separation even if the surrounding release pipeline is shortened.

Evidence: [.github/workflows/publish-pypi.yml:195](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/.github/workflows/publish-pypi.yml#L195), [tests/test_release_orchestration.py:757](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_release_orchestration.py#L757).


### KISS-44 — Make the owner’s approval explicit

**Keep · Complexity 2/5 · Value 5/5 · Useful authority boundary**

**Example:** Tests pass, but the owner has not approved verification, merge or publication.

**Current behavior:** Lifecycle decisions record the artifact, outcome and accountable role. Passing tests do not automatically exercise another decision.

**Assessment:** The basic distinction protects the owner’s intent. It does not require repeating it through many files, hashes or separate delivery loops.

**Recommendation:** Keep one clear recorded decision per meaningful action. Simplify the surrounding paperwork and never invent approval.

Evidence: [docs/engineering/DECISION_RIGHTS.md:42](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/docs/engineering/DECISION_RIGHTS.md#L42), [tests/test_workflow_execution.py:144](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/tests/test_workflow_execution.py#L144).


### KISS-45 — Identify the checker and the candidate being tested

**Keep · Complexity 3/5 · Value 5/5 · Useful correctness boundary**

**Example:** A local checkout shadows the installed checker, or evidence refers to different code.

**Current behavior:** Origin/version checks distinguish candidate code from the selected installed evaluator; verification records name the tested commit.

**Assessment:** The repository has documented real release-governance incidents involving this boundary. Calling all identity checks hypothetical would be wrong.

**Recommendation:** Keep a simple origin/version check and exact candidate reference. Cut repeated whole-payload proof, rigid interpreter layout and receipt-only failures around that core.

Evidence: [se_harness/runtime_identity.py:257](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/se_harness/runtime_identity.py#L257), [docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md:11](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md#L11), [docs/rca/2026-08-23-0.6.0-release-recovery.md:15](https://github.com/mmzen/se_harness/blob/93677e69dacb08367a7079e3372118c5064087c8/docs/rca/2026-08-23-0.6.0-release-recovery.md#L15).


## Test cleanup rule

Delete a test when its only purpose is to preserve a behavior we deliberately remove. Keep a test when it verifies a useful outcome: the intended file is written, unrelated content survives, the reported result is true, wrong package bytes are rejected, or a real operation can be retried. Replace an abstract failure matrix with one representative test per distinct remaining behavior. A high test count alone is not evidence of waste.

## Coverage and limits

I inventoried all tracked runtime Python, repository tools, GitHub helpers, ordinary scripts, tests and workflows at the stated commit. I inspected the main refusal paths in identity, hashing, evidence, workflow, installation, release, risk authoring and the tests that preserve them. Dashboard generation was reviewed for its coupling to workflow, not as a full UI code review. General graph algorithms, browser rendering and every individual test were not exhaustively audited.

The report links to exact committed source lines. Test links show code inspected, not tests executed during this audit. Recommendations involving permission or lifecycle contracts need an explicit replacement contract if adopted. That requirement does not prevent this read-only analysis.

The repository records real 0.5.0 and 0.6.0 release-governance incidents. Those support retaining a clear boundary between the checker and the candidate, while also showing how the governance mechanism itself can become a source of failure. They do not establish the frequency of hypothetical tampering scenarios.

No current runtime benchmark, CI rerun, live installation, release, file deletion or implementation was performed. The prior plugin CI speedup is not a measurement of these new proposals.
