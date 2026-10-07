# Hosted setup correction — proposal

Claude loaded the setup skill, then followed startup text that required checkout
activation. The test had selected only a hosted sandbox and explicitly prohibited
activation. The run was stopped. No completed activation result was observed.
The plugin-data directory was empty on readback.

**Proposal:** add the missing hosted route to startup text and clarify that setup
stops before local activation. Reuse the selected installed candidate client.
Keep the existing local checkout route, hooks and permission checks.

This changes two instruction files. It introduces no new selector, storage,
runtime behavior or lifecycle policy. The bootstrap asset is outside WO-HAG-009,
so WO-HAG-010 requests that additional scope with required commit-bound verification.
Both hosts still must pass VER-HAG-007. Existing decisions are preserved.

The exact diff below is proposed text only; neither product file is edited yet.

```diff
--- a/plugins/verity-plane/common/assets/bootstrap.md
+++ b/plugins/verity-plane/common/assets/bootstrap.md
@@ -1,4 +1,19 @@
 # Select the working repository
+
+First use the target already selected by the operator.
+
+## Explicit hosted sandbox
+
+If the operator selected a hosted sandbox, use the setup skill's "Hosted sandbox
+selection" procedure. Retain its endpoint, project and versioned context. Leave
+any existing checkout selection unchanged. This route does not activate or clear
+a checkout, install a repository harness, or switch real authority to the graph.
+After checking the hosted selection, follow harness-orient for reads or change
+for authorized sandbox work. Do not continue into checkout activation.
+
+## Local checkout
+
+Use this route for work in a cloned or existing repository.
 
 When asked to clone, clone to the intended destination, then activate that exact
 checkout. For existing work, reuse the known checkout path. Ask for a path only

--- a/plugins/verity-plane/common/skills/setup/SKILL.md
+++ b/plugins/verity-plane/common/skills/setup/SKILL.md
@@ -11,6 +11,9 @@
 does not pin that release. A development wheel is only for disposable testing.
 
 Use the target and action already requested; ask only for a missing choice.
+For an explicitly selected hosted sandbox, complete only "Hosted sandbox
+selection" and the applicable "Private lifecycle test copy" guidance below.
+Checkout activation and repository setup are separate routes.
 
 ## Hosted sandbox selection
 
@@ -20,8 +23,10 @@
 Never print the credential. The sandbox is not repository authority.
 
 Obtain the qualified combination report and exact candidate client wheel.
-Create a separate disposable Python environment outside the checkout. Verify the
-wheel's SHA-256 against that report, then install that file with `pip --no-deps`.
+If the selected candidate client is already installed in a separate disposable
+environment, verify its identity and reuse it. Otherwise create that environment
+outside the checkout. Verify the wheel's SHA-256 against the combination report,
+then install that file with `pip --no-deps`.
 The plugin's bundled released evaluator remains unchanged; do not replace it with
 the candidate client. Use the candidate environment's absolute Python as
 `CLIENT_PYTHON` in the remote commands below.
@@ -34,6 +39,7 @@
 all component identities with the selected combination. A mismatch stops the
 remote action. An unavailable service never selects local file writes as a fallback.
 Use harness-orient for reads or change for authorized sandbox draft preparation.
+Do not continue into "Activate the checkout" for this hosted selection.
 This route grants no approval, verification, release, adoption or deployment right.
 
 ## Activate the checkout
@@ -81,5 +87,5 @@
 client, a loopback endpoint, an explicit test project and a new disposable volume.
 Use the repository's `server/README.md` Phase 3 procedure. Its configuration must
 report `test_copy: true`; select `--test-copy` for each rehearsal or export.
-Keep the real checkout selected with its released evaluator. Remote setup does
+Leave any existing real checkout selection unchanged. Remote setup does
 not activate graph authority or install this candidate into the user's host.
```

## Review and qualification

Existing package tests compare the full source text with both generated archives.
Existing activation/delivery tests cover the local route. Fresh native tests must
show that the hosted task follows the selected project without activation and
still completes the required lifecycle, reads, recovery and exports.

The affected scenario will be rerun with final packaged guidance. Earlier Codex
observations remain evidence at their exact source; they do not prove a new
package automatically. No Claude pass or actual VREC is claimed.

See [WO-HAG-010](../../work-orders/WO-HAG-010.md),
[the stopped trial](../WO-HAG-009/sonnet03-stop.json), and its
[transcript inventory](../WO-HAG-009/sonnet03-stopped.json).

Preparation validation: 1987 artifacts, zero errors, 63 existing warnings.
All seven planned file destinations are covered; no invalid scope declaration.
These checks do not approve WO-HAG-010.
