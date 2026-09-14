# Design simplicity in governed projects

The candidate authoring policy now contains the shared design principle and review
questions. Authors and reviewers apply it against their project's agreed needs and
constraints. Significant complexity needs a reason; a trivial change needs no extra
comparison document. The policy is human judgement within existing decisions.

## Where it is read

The installed `ENGINEERING_HARNESS.md` routes authoring, design and review to
`docs/engineering/ARTIFACT_AUTHORING.md`. AGENTS and CLAUDE already load that router.
Start and review preflight include the policy in their reading manifests. Artifact
creation prints the existing type checklist. Templates and common plugin skills point
to the same policy; the evidence skill retains the existing review's material findings.

## Adoption

These are candidate source changes under WO-KIS-008. They reach governed projects
through a normal product release and explicit repository upgrade. SE Harness's own
repository adopts the same released policy through that process. This change leaves
its installed 0.17.0 governance intact.

The candidate installer preserves editable guidance by default. During an authorized
upgrade, explicitly select `docs/engineering/ARTIFACT_AUTHORING.md` with `--replace-file`
to take the supplied revision, or reconcile the shared rule with local edits first.
Select each desired revised artifact template in the same way. Preview the normal
upgrade before applying it. The locked router follows the selected release normally.
Consult that release's help for the exact command and the project's upgrade scope.

Update the plugin through its ordinary route to receive the common skill links.
A plugin update alone does not change the project's installed policy. No separate
KISS receipt, CI job or automatic quality score is needed for adoption or review.
