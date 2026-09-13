# Accepted proposal coverage

All 50 scenarios are accounted for: 43 changes and seven kept protections.
These are required outcomes, not implementation results.

| # | Scenario | Disposition | Requirement | Rules | Acceptance |
| --- | --- | --- | --- | --- | --- |
| 1 | Someone edited an old skill | Simplify/remove: Delete the old skill directory, including edits. | REQ-PLG-032 | PLG-KIS-002 | K01 |
| 2 | An old skill is missing or its lock entry is wrong | Simplify/remove: Missing old files are normal. Remove the known entries and continue. | REQ-PLG-032 | PLG-KIS-003 | K01 |
| 3 | Someone put extra notes inside an old harness skill | Simplify/remove: The named old skill directories are disposable. Preserve other skill directories. | REQ-PLG-032 | PLG-KIS-002, PLG-KIS-013 | K01 |
| 4 | Some other harness file changed before the switch | Simplify/remove: Read the existing lock. Do not make unrelated content a migration prerequisite. | REQ-PLG-032 | PLG-KIS-003 | K01 |
| 5 | The evaluator is a different build | Simplify/remove: Migration only changes skill files and their provider. It does not make a lifecycle decision. | REQ-PLG-032 | PLG-KIS-008, PLG-KIS-017 | K01 |
| 6 | The plugin has a different version or content hash | Simplify/remove: Supply the installed plugin directory. Check its manifest and required skill files. | REQ-PLG-032 | PLG-KIS-004, PLG-KIS-008 | K02 |
| 7 | A plugin helper changed in a later release | Simplify/remove: Allow plugin updates. Do not pin its content in the repository lock. | REQ-PLG-034 | PLG-KIS-009, PLG-KIS-012 | K06 |
| 8 | An unrelated plugin file changed or an extra file appeared | Simplify/remove: Migration checks only the replacement skill files. | REQ-PLG-032 | PLG-KIS-004, PLG-KIS-008 | K02 |
| 9 | A binding has an extra field or future metadata | Simplify/remove: Keep one small provider record and ordinary plugin metadata. | REQ-PLG-034 | PLG-KIS-009, PLG-KIS-012 | K06 |
| 10 | The provider record was edited | Simplify/remove: Remove the self-checksum. Keep provider=plugin. | REQ-PLG-034 | PLG-KIS-009 | K06 |
| 11 | The evaluator template changed after migration | Simplify/remove: Use the provider to exclude the old skills from installation. No frozen catalog hashes. | REQ-PLG-034 | PLG-KIS-010 | K06 |
| 12 | Files changed after a preview | Simplify/remove: Preview is optional. Apply reads current inputs. | REQ-PLG-032 | PLG-KIS-006 | K01 |
| 13 | Two processes switch ownership at once | Simplify/remove: Remove the migration mutex. Run this occasional switch once on a selected repository. | REQ-PLG-033 | PLG-KIS-008 | K12 |
| 14 | A file is replaced while it is being read | Simplify/remove: Use normal reads for the selected local plugin. Keep a short check against redirected deletion paths. | REQ-PLG-033 | PLG-KIS-005, PLG-KIS-008 | K03 |
| 15 | The process dies between individual writes | Simplify/remove: Delete old files, save the lock last, rerun to finish after an interruption. | REQ-PLG-033 | PLG-KIS-007 | K04 |
| 16 | Someone edits files after a crash | Simplify/remove: No recovery engine. Disposable files can be replaced on the next run. | REQ-PLG-033 | PLG-KIS-007, PLG-KIS-008 | K04 |
| 17 | Someone replaces a file with identical bytes after a crash | Simplify/remove: Delete this scenario and its special identity tracking. | REQ-PLG-033 | PLG-KIS-008 | K12 |
| 18 | Someone forges, truncates or rewrites the recovery journal | Simplify/remove: Remove the journal; its attack cases disappear with it. | REQ-PLG-033 | PLG-KIS-008 | K12 |
| 19 | A pending journal is left behind | Simplify/remove: No pending-recovery blocker. The migration command can simply be rerun. | REQ-PLG-033 | PLG-KIS-007, PLG-KIS-008 | K04 |
| 20 | Restoring repository skills encounters an existing local copy | Simplify/remove: Overwrite the disposable skill files from the current templates. | REQ-PLG-033 | PLG-KIS-011 | K05 |
| 21 | A hand-built internal installer Change object uses a path alias | Simplify/remove: Remove the special internal-caller threat model. The ordinary planner excludes plugin-owned skills. | REQ-PLG-034 | PLG-KIS-010 | K06 |
| 22 | Every intermediate test state must be retained | Simplify/remove: Keep normal test output and meaningful assertions. | REQ-PLG-037 | PLG-KIS-029, PLG-KIS-032 | K12 |
| 23 | The full fault matrix must run in several environments | Simplify/remove: Normal source suite plus one small installed-package run per OS, using the existing environments. | REQ-PLG-037 | PLG-KIS-028, PLG-KIS-029 | K12 |
| 24 | Migration acceptance needs its own source archive proof | Simplify/remove: The installed migration test imports the actual wheel. Remove the ownership-only source archive and inventory tests. | REQ-PLG-037 | PLG-KIS-029 | K12 |
| 25 | The slow migration needs permanent runner diagnostics | Simplify/remove: Remove the investigation-only step from normal CI after removing the costly migration design. | REQ-PLG-037 | PLG-KIS-029 | K12 |
| 26 | The selected plugin is wrong or incomplete | Keep: Check the Verity Plane manifest and six replacement files before deleting anything. | REQ-PLG-032 | PLG-KIS-004 | K02 |
| 27 | A deletion path points into another directory | Keep: Keep a short destination check. Do not scan or authenticate the entire filesystem. | REQ-PLG-033 | PLG-KIS-005 | K03 |
| 28 | The replacement plugin is inside the directory being deleted | Keep: Reject that location before deleting old files. | REQ-PLG-033 | PLG-KIS-005 | K03 |
| 29 | A write fails or the command is interrupted | Keep: Keep atomic lock replacement and two retry tests; remove the full crash-recovery system. | REQ-PLG-033 | PLG-KIS-007 | K04 |
| 30 | An ordinary upgrade recreates the old skills | Keep: Keep the provider marker and verify migration, doctor and upgrade together. | REQ-PLG-034 | PLG-KIS-010 | K06 |
| 31 | The repository is cloned onto a machine without the plugin | Keep: The lock contains only the portable provider choice. | REQ-PLG-034 | PLG-KIS-009, PLG-KIS-010 | K06 |
| 32 | A report is written over project or installation files | Keep: Keep the ordinary report destination checks; remove references to deleted recovery files. | REQ-PLG-033 | PLG-KIS-013 | K03 |
| 33 | A setup attempt left an incomplete private environment | Simplify/remove: Allow setup to rerun in its own environment. Reinstall the selected wheel and report the actual result. | REQ-PLG-035 | PLG-KIS-014 | K07 |
| 34 | The environment or observation file is in an unexpected layout | Simplify/remove: Use one documented private environment path. A routine setup needs no separate receipt file. | REQ-PLG-035 | PLG-KIS-014, PLG-KIS-016 | K07 |
| 35 | Installing the checker is treated as a release proof ceremony | Simplify/remove: Create/reuse the environment, install the intended checker, then run it once. Keep repository upgrade decisions in the harness. | REQ-PLG-035 | PLG-KIS-015, PLG-KIS-016, PLG-KIS-017 | K07 |
| 36 | A session starts or resumes | Simplify/remove: Read the repository instructions once. Run a fresh harness check when beginning governed work. | REQ-PLG-036 | PLG-KIS-018, PLG-KIS-019 | K08, K09 |
| 37 | Instructions exceed an invented delivery capacity | Simplify/remove: Point the agent to the instruction files and let it read them normally. | REQ-PLG-036 | PLG-KIS-018 | K09 |
| 38 | The agent was compacted or switched repositories | Simplify/remove: Reread the selected repository instructions and continue through the normal CLI. | REQ-PLG-036 | PLG-KIS-018 | K09 |
| 39 | Codex or Python receives a patch update | Simplify/remove: Check the features actually used. Do not make an observed test profile a runtime allowlist. | REQ-PLG-036 | PLG-KIS-021 | K08 |
| 40 | Claude or Python receives a patch update | Simplify/remove: Remove exact host/patch pins. Check that the selected interpreter and required hook interface work. | REQ-PLG-036 | PLG-KIS-021 | K08 |
| 41 | A newer repository uses a newer evaluator | Simplify/remove: Use the repository-selected checker instead of duplicating its identity in plugin source. | REQ-PLG-036 | PLG-KIS-017 | K08 |
| 42 | An optional diagnostic file cannot be written | Simplify/remove: Log the diagnostic error without changing the result of the user operation. | REQ-PLG-036 | PLG-KIS-022 | K09 |
| 43 | A read-only check might leave arbitrary child processes behind | Simplify/remove: Prefer an explicit CLI check. If automatic hooks stay, use one bounded subprocess invocation for this known checker. | REQ-PLG-036 | PLG-KIS-020, PLG-KIS-023 | K08 |
| 44 | Every supported edit must be interpreted and checked by a hook | Simplify/remove: Accepted recommendation: explicit checks; remove automatic blocking hooks. | REQ-PLG-036 | PLG-KIS-020 | K08 |
| 45 | The same hook response is validated again by each wrapper | Simplify/remove: Keep only the fields needed to route the result. Put shared parsing in one place. | REQ-PLG-036 | PLG-KIS-020, PLG-KIS-032 | K08 |
| 46 | Plugin assembly is used for local development | Simplify/remove: Give local development a copy-and-zip path. Keep release provenance work at publication time. | REQ-PLG-037 | PLG-KIS-024, PLG-KIS-025, PLG-KIS-027 | K10, K11 |
| 47 | An assembly output directory already exists | Simplify/remove: Allow rebuilding a directory owned by this build command, without touching other directories. | REQ-PLG-037 | PLG-KIS-026 | K10 |
| 48 | Plugin files must be proven identical through several layers | Simplify/remove: Validate packaging once. Migration no longer repeats package acceptance. | REQ-PLG-037 | PLG-KIS-025 | K10 |
| 49 | A qualification fixture becomes a permanent product restriction | Simplify/remove: Retain historical observations as history. Keep a small smoke test for the current plugin instead of making every probe permanent. | REQ-PLG-037 | PLG-KIS-030, PLG-KIS-031 | K12 |
| 50 | Changing the design requires amending many contracts | Simplify/remove: Replace current migration requirements with a short behavior contract. Do not alter past release/verification facts. | REQ-PLG-037 | PLG-KIS-001, PLG-KIS-031, PLG-KIS-032 | K12 |
