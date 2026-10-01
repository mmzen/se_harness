"""Check REL-SEH-032 candidate inputs and the separately observed public delivery."""
from copy import deepcopy
import json
import posixpath
from pathlib import Path
import re
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[3]
# Candidate identities come from approved REL-SEH-032, not candidate output.
PLUGIN = "0.2.3"
CANDIDATE_EVALUATOR = "0.20.1"
# Published identities retain REQ-PLG-039 / SPEC-PLG-023 and their actual receipt.
EVALUATOR = "0.19.0"
WHEEL_SHA = "43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8"
RELEASE = "docs/engineering/release-0-19-0/releases/RLS-SEH-028.md"
OBSERVATION = "docs/engineering/plugin-integration/evidence/WO-PLG-028/publication.json"


def selected_inputs():
    return {
        "manifests": [json.loads((ROOT / path).read_text(encoding="utf-8")) for path in (
            "plugins/verity-plane/codex/.codex-plugin/plugin.json",
            "plugins/verity-plane/claude-code/.claude-plugin/plugin.json")],
        "release": tomllib.loads((ROOT / RELEASE).read_text(encoding="utf-8").split("+++")[1]),
        "observation": json.loads((ROOT / OBSERVATION).read_text(encoding="utf-8")),
        "root": (ROOT / "README.md").read_text(encoding="utf-8"),
        "marketplace": (ROOT / "release/plugin-marketplace/README.md").read_text(encoding="utf-8"),
    }


def identity_findings(inputs):
    findings = []
    if any(m.get("version") != PLUGIN for m in inputs["manifests"]):
        findings.append("candidate manifest version")
    release = inputs["release"]
    if (release.get("id"), release.get("status"), release.get("version")) != (
            "RLS-SEH-028", "released", EVALUATOR):
        findings.append("released evaluator selection")
    distribution = release.get("distribution", {})
    if (distribution.get("wheel"), distribution.get("wheel_sha256")) != (
            f"se_harness-{EVALUATOR}-py3-none-any.whl", WHEEL_SHA):
        findings.append("released wheel identity")
    guide = " ".join(inputs["marketplace"].split())
    if (f"Plugin **{PLUGIN}**" not in guide or f"**SE Harness {CANDIDATE_EVALUATOR}**" not in guide):
        findings.append("assembled guide selection")
    root = " ".join(inputs["root"].split())
    observed = re.search(
        r"Observed public delivery \(\d{4}-\d{2}-\d{2}\): Plugin \*\*([^*]+)\*\* "
        r"bundles released \*\*SE Harness ([^*]+)\*\*", root)
    identity = inputs["observation"]["identity"]
    if not observed or observed.groups() != (identity["plugin_version"], identity["evaluator"]["version"]):
        findings.append("public claim lacks matching observation")
    if inputs["observation"].get("tree_matches_accepted_distribution") is not True:
        findings.append("public tree lacks accepted-package comparison")
    if "pending publication" in root:
        findings.append("stale publication status")
    return findings


def link_findings(files, sources):
    """Resolve Markdown links in the specified source or composed file space."""
    findings = []
    for source in sources:
        content = files[source].decode("utf-8")
        for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", content):
            if re.match(r"(?:https?://|mailto:)", target):
                continue
            path, _, anchor = target.partition("#")
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), path)) if path else source
            if resolved not in files:
                findings.append(f"{source}: missing file {target}")
            elif anchor:
                headings = re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", files[resolved].decode("utf-8"))
                anchors = {re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-") for title in headings}
                if anchor not in anchors:
                    findings.append(f"{source}: missing heading {target}")
    return findings


class RefreshGuidanceTests(unittest.TestCase):
    def test_selected_candidate_and_public_claims_have_independent_inputs(self):
        self.assertEqual([], identity_findings(selected_inputs()))

    def test_wrong_manifest_or_wheel_is_rejected(self):
        original = selected_inputs()
        for field in ("manifest", "wheel"):
            data = deepcopy(original)
            if field == "manifest":
                for manifest in data["manifests"]:
                    manifest["version"] = "0.2.0"
            else:
                data["release"]["distribution"]["wheel_sha256"] = "0" * 64
            with self.subTest(field=field):
                self.assertTrue(identity_findings(data))

    def test_mutually_stale_documents_do_not_establish_identity(self):
        data = selected_inputs()
        for name in ("root", "marketplace"):
            data[name] = data[name].replace(PLUGIN, "0.1.0").replace(CANDIDATE_EVALUATOR, "0.18.0").replace("0.2.1", "0.1.0").replace(EVALUATOR, "0.18.0")
        self.assertIn("assembled guide selection", identity_findings(data))

    def test_premature_public_claim_is_rejected(self):
        data = selected_inputs()
        # A contradictory retained observation must defeat a current claim.
        data["observation"]["identity"]["plugin_version"] = "0.1.0"
        data["observation"]["identity"]["evaluator"]["version"] = "0.18.0"
        self.assertIn("public claim lacks matching observation", identity_findings(data))

    def test_public_claim_requires_accepted_package_comparison(self):
        data = selected_inputs()
        data["observation"]["tree_matches_accepted_distribution"] = False
        self.assertIn("public tree lacks accepted-package comparison", identity_findings(data))

    def test_published_guide_rejects_pending_publication_status(self):
        data = selected_inputs()
        data["root"] += "\nThis package is pending publication.\n"
        self.assertIn("stale publication status", identity_findings(data))

    def test_source_links_resolve_in_source_context(self):
        sources = ["README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md"]
        files = {name: (ROOT / name).read_bytes() for name in sources}
        for source in sources:
            for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", files[source].decode()):
                if re.match(r"(?:https?://|mailto:|#)", target):
                    continue
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), target.split("#")[0]))
                if (ROOT / resolved).is_file():
                    files[resolved] = (ROOT / resolved).read_bytes()
        self.assertEqual([], link_findings(files, sources))

    def test_package_links_resolve_after_composition(self):
        plan = json.loads((ROOT / "release/plugin-assembly.json").read_bytes())
        files = {name: (ROOT / "release/plugin-marketplace" / name).read_bytes()
                 for name in ("README.md", "submissions/README.md", "submissions/reviewer-test-cases.md")}
        files["submissions/verity-plane-logo.png"] = (ROOT / "docs/images/verity-plane-logo.png").read_bytes()
        for host, mapping in plan["hosts"].items():
            for target, source in {**plan["shared"], **mapping}.items():
                files[f"packages/{host}/verity-plane/{target}"] = (ROOT / source).read_bytes()
        sources = ["README.md", "submissions/README.md", "submissions/reviewer-test-cases.md",
                   "packages/codex/verity-plane/README.md", "packages/claude/verity-plane/README.md"]
        self.assertEqual([], link_findings(files, sources))
        files["README.md"] += b"\n[Setup](packages/codex/verity-plane/skills/setup/SKILL.md#missing-heading)\n"
        self.assertTrue(any("missing heading" in finding for finding in link_findings(files, sources)))


if __name__ == "__main__":
    unittest.main()
