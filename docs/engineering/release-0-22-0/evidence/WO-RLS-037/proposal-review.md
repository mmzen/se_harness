# Review: one-paragraph README correction

**Requested approval:** WO-RLS-037 and VER-RLS-001, with required verification
tied to the corrected commit and delivery through existing PR #530.

CI found one failing test among 1,259 tests (2 skips): the README is 676 words,
above its accepted 650-word limit. [Original failure](ci-failure.json).

**Proposed fix:** Remove only the second duplicate paragraph under
`Fewer repository files`. The complete warning stays beside the installation
instructions. No commands, versions, links, unique claims or test limits change.
The proposed README has **648 words**.

```diff
--- a/README.md
+++ b/README.md
@@ -61,8 +61,6 @@
 
 Instructions and templates live in the evaluator wheel; initialization writes
 configuration and lock files. Activation restores the checkout after compaction.
-Claude Code installation/update and native session tests, and Codex Windows desktop tests, were not run for this release and remain unverified under DEC-RLS-005/006. Both distributed packages were byte-checked.
-
 See [migration](docs/notes/harness-installation-and-upgrades.md#minimal-installation-0210).
 The published package retains its pre-publication README.
 
```

[Proposal checks](proposal-checks.json) retain the original/proposed hashes and
word counts. These are pre-approval inspections, not implementation evidence.
The repository README is still unchanged from the verified candidate.

All 14 existing public-onboarding tests pass when reading the proposed temporary
README. [Probe result](proposal-test.json). This checks the proposal before
approval; the corrected committed candidate still requires its own verification.

The existing public-onboarding and documentation suites will check the corrected
commit. Full candidate-source CI must pass before merge. A new ready VREC will be
pushed for the human verification decision; no old record will be rebound.

Why approval is needed: WO-RLS-036 is already implemented. The selected released
verification procedure says a completed work order does not become executable
again when verification finds a defect. This small new work order covers that
correction and its evidence without rewriting the approved history.

VREC-PLG-033 records the human's decision for its original candidate. It does not
waive this CI failure. Claude and Codex Windows desktop remain untested, and
merge/latest/last closeout remain outstanding.
