"""Check package identities and current claims against independent public receipts."""
from copy import deepcopy
import hashlib
import json
import posixpath
from pathlib import Path
import re
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[3]
# REL-SEH-036 selects these package identities; development source may advance.
# Expected identities are explicit inputs, never derived from tested manifests.
PACKAGE_PLUGIN = "0.2.7"
PACKAGE_EVALUATOR = "0.23.0"
PUBLIC_PLUGIN = "0.2.7"
# Published identities come from RLS-SEH-034 and independent public readback.
EVALUATOR = "0.23.0"
WHEEL_SHA = "ffa486d386383992349e75e2890b36ded105c797acaa483783d1380cfd520d5c"
RELEASE = "docs/engineering/release-0-23-0/releases/RLS-SEH-034.md"
OBSERVATION = "docs/engineering/release-0-23-0/evidence/WO-RLS-047/marketplace-public-ref.json"
QUALIFIED = "docs/engineering/release-0-23-0/evidence/WO-RLS-046/marketplace-review-commit-48e851bb.json"


def selected_inputs():
    return {
        "manifests": [json.loads((ROOT / path).read_text(encoding="utf-8")) for path in (
            "plugins/verity-plane/codex/.codex-plugin/plugin.json",
            "plugins/verity-plane/claude-code/.claude-plugin/plugin.json")],
        "release": tomllib.loads((ROOT / RELEASE).read_text(encoding="utf-8").split("+++")[1]),
        "observation": json.loads((ROOT / OBSERVATION).read_text(encoding="utf-8")),
        "qualified_bytes": (ROOT / QUALIFIED).read_bytes(),
        "root": (ROOT / "README.md").read_text(encoding="utf-8"),
        "marketplace": (ROOT / "release/plugin-marketplace/README.md").read_text(encoding="utf-8"),
    }


def identity_findings(inputs):
    findings = []
    if any(m.get("version") != PACKAGE_PLUGIN for m in inputs["manifests"]):
        findings.append("package manifest version")
    release = inputs["release"]
    if (release.get("id"), release.get("status"), release.get("version")) != (
            "RLS-SEH-034", "released", EVALUATOR):
        findings.append("released evaluator selection")
    distribution = release.get("distribution", {})
    if (distribution.get("wheel"), distribution.get("wheel_sha256")) != (
            f"se_harness-{EVALUATOR}-py3-none-any.whl", WHEEL_SHA):
        findings.append("released wheel identity")
    guide = " ".join(inputs["marketplace"].split())
    if (f"Plugin **{PACKAGE_PLUGIN}**" not in guide or f"**SE Harness {PACKAGE_EVALUATOR}**" not in guide):
        findings.append("assembled guide selection")
    root = " ".join(inputs["root"].split())
    observed = re.search(
        r"Observed public delivery \(\d{4}-\d{2}-\d{2}\): Plugin \*\*([^*]+)\*\* "
        r"bundles released \*\*SE Harness ([^*]+)\*\*", root)
    observation = inputs["observation"]
    identity = observation["assembly"]["content"]
    if not observed or observed.groups() != (identity["plugin_version"], identity["evaluator"]["version"]):
        findings.append("public claim lacks matching observation")
    publisher = observation["publisher"]
    readback = observation["readback"]
    public_refs = dict(line.split()[::-1] for line in readback["stdout"].splitlines())
    # The verified release receipt binds the separate marketplace proof by bytes.
    index = observation["qualification"]["retained_evidence_index"]["content"]
    binding = next((entry for entry in index["files"] if entry["path"] == QUALIFIED), {})
    qualified = json.loads(inputs["qualified_bytes"])
    if not (
        observation["status"] == "pass"
        and observation["release_record"] == "RLS-SEH-034"
        and readback["exit_code"] == 0
        and publisher["state"] == "exact"
        and publisher["applied"] is True
        and binding.get("sha256") == hashlib.sha256(inputs["qualified_bytes"]).hexdigest()
        and public_refs.get("refs/heads/plugin-marketplace") == publisher["commit"] == qualified["marketplace_commit"]
        and publisher["tree"] == qualified["marketplace_tree"]
        and publisher["identity_sha256"] == observation["assembly"]["sha256"] == qualified["package_identity_sha256"]
        and qualified["all_git_blob_bytes_match"] is True
        and (identity["plugin_version"], identity["evaluator"]["version"], identity["evaluator"]["archive_sha256"])
            == (PUBLIC_PLUGIN, EVALUATOR, WHEEL_SHA)
    ):
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
                target_content = files[resolved].decode("utf-8")
                headings = re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", target_content)
                anchors = {re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-") for title in headings}
                anchors.update(re.findall(r'<a id="([^"]+)"></a>', target_content))
                if anchor not in anchors:
                    findings.append(f"{source}: missing heading {target}")
    return findings


class RefreshGuidanceTests(unittest.TestCase):
    def test_package_and_public_claims_have_independent_inputs(self):
        self.assertEqual([], identity_findings(selected_inputs()))

    def test_each_host_must_match_the_selected_package(self):
        for index in range(2):
            for version in ("0.2.6", "0.2.8"):
                data = selected_inputs()
                data["manifests"][index]["version"] = version
                with self.subTest(host=index, version=version):
                    self.assertIn("package manifest version", identity_findings(data))

    def test_wrong_package_or_public_claim_is_rejected(self):
        data = selected_inputs()
        data["marketplace"] = data["marketplace"].replace(PACKAGE_PLUGIN, "0.2.6")
        self.assertIn("assembled guide selection", identity_findings(data))
        data = selected_inputs()
        data["root"] = data["root"].replace(PUBLIC_PLUGIN, "0.2.8")
        self.assertIn("public claim lacks matching observation", identity_findings(data))

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
            data[name] = data[name].replace(PUBLIC_PLUGIN, "0.1.0").replace(PACKAGE_PLUGIN, "0.1.0").replace(EVALUATOR, "0.18.0").replace(PACKAGE_EVALUATOR, "0.18.0")
        self.assertIn("assembled guide selection", identity_findings(data))

    def test_premature_public_claim_is_rejected(self):
        data = selected_inputs()
        # A contradictory retained observation must defeat a current claim.
        data["observation"]["assembly"]["content"]["plugin_version"] = "0.1.0"
        data["observation"]["assembly"]["content"]["evaluator"]["version"] = "0.18.0"
        self.assertIn("public claim lacks matching observation", identity_findings(data))

    def test_public_claim_requires_accepted_package_comparison(self):
        for field in ("state", "tree", "identity_sha256", "commit"):
            data = selected_inputs()
            data["observation"]["publisher"][field] = "unconfirmed"
            with self.subTest(field=field):
                self.assertIn("public tree lacks accepted-package comparison", identity_findings(data))
        for defect in ("missing proof binding", "changed proof bytes"):
            data = selected_inputs()
            if defect == "missing proof binding":
                index = data["observation"]["qualification"]["retained_evidence_index"]["content"]
                index["files"] = [entry for entry in index["files"] if entry["path"] != QUALIFIED]
            else:
                data["qualified_bytes"] += b"\n"
            with self.subTest(defect=defect):
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

    def test_packaged_skill_routes_resolve_for_both_hosts(self):
        plan = json.loads((ROOT / "release/plugin-assembly.json").read_bytes())
        for host, mapping in plan["hosts"].items():
            files = {target: (ROOT / source).read_bytes() for target, source
                     in {**plan["shared"], **mapping}.items()}
            pages = [name for name in files if name.startswith("skills/") and name.endswith(".md")]
            with self.subTest(host=host):
                self.assertEqual([], link_findings(files, pages))
                # Missing deep references must fail even when the entry file
                # and the package README still exist.
                for name in ("skills/setup/references/checkout.md",
                             "skills/change/references/hosted-drafts.md",
                             "skills/evidence/references/hosted-evidence.md"):
                    broken = {key: value for key, value in files.items() if key != name}
                    findings = link_findings(broken, [p for p in pages if p != name])
                    self.assertTrue(any("missing file" in finding for finding in findings), (host, name))


if __name__ == "__main__":
    unittest.main()
