from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = REPOSITORY_ROOT / ".github" / "scripts" / "publish_dashboard.py"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "publish-dashboard-pages.yml"

SPEC = importlib.util.spec_from_file_location("dashboard_publication", HELPER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("dashboard publication helper is unavailable")
PUBLICATION = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PUBLICATION
SPEC.loader.exec_module(PUBLICATION)


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class GitReleaseFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        self.root.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Harness Test")
        self.git("config", "user.email", "harness-test@example.invalid")
        self.write("README.md", "candidate\n")
        self.commit("candidate")
        self.candidate = self.git("rev-parse", "HEAD")
        self.git("tag", "-a", "v1.2.3", "-m", "release 1.2.3")
        self.record_path = "docs/engineering/release/releases/RLS-TST-001.md"
        self.write(self.record_path, self.release_record("RLS-TST-001"))
        self.commit("integrate released record")
        self.governance = self.git("rev-parse", "HEAD")
        self.write("later.txt", "unrelated later work\n")
        self.commit("later work")
        self.head = self.git("rev-parse", "HEAD")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return completed.stdout.strip()

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, message: str) -> None:
        self.git("add", ".")
        self.git("commit", "-m", message)

    def release_record(self, record_id: str, candidate: str | None = None) -> str:
        return f'''+++
id = "{record_id}"
type = "release_record"
title = "Release candidate 1.2.3"
status = "released"
owners = ["release-owner"]
created = "2026-08-16"
updated = "2026-08-16"
version = "1.2.3"
commit = "{candidate or self.candidate}"
git_object_format = "sha1"
released_at = "2026-08-16T12:00:00Z"
authorized_by = "release-owner"
tag = "v1.2.3"

[relations]
satisfies = ["REL-TST-001"]
includes_verification = ["VREC-TST-001"]
releases_work = ["WO-TST-001"]
+++

# Released test record
'''

    def resolve(self, **overrides: str | None):
        arguments = {
            "repository": self.root,
            "tag": "v1.2.3",
            "release_record": "RLS-TST-001",
            "default_ref": "refs/heads/main",
        }
        arguments.update(overrides)
        return PUBLICATION.resolve_release(**arguments)

    def test_resolver_selects_integration_commit_not_tag_or_later_head(self) -> None:
        result = self.resolve()
        self.assertEqual(self.candidate, result.candidate_commit)
        self.assertEqual(self.governance, result.governance_commit)
        self.assertEqual(self.head, result.default_head)
        self.assertNotEqual(result.candidate_commit, result.governance_commit)
        self.assertNotEqual(result.default_head, result.governance_commit)

    def test_exact_manual_replay_is_accepted_and_later_commit_is_rejected(self) -> None:
        self.assertEqual(self.governance, self.resolve(governance_commit=self.governance).governance_commit)
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "not the release integration commit"):
            self.resolve(governance_commit=self.head)
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "full sha1"):
            self.resolve(governance_commit=self.governance[:12])

    def test_tag_candidate_mismatch_fails_closed(self) -> None:
        self.git("tag", "-f", "v1.2.3", self.head)
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "tag target differs"):
            self.resolve()

    def test_duplicate_released_records_for_one_tag_fail_closed(self) -> None:
        self.write(
            "docs/engineering/other/releases/RLS-TST-002.md",
            self.release_record("RLS-TST-002"),
        )
        self.commit("duplicate release binding")
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "found 2"):
            PUBLICATION.resolve_release(
                self.root,
                "v1.2.3",
                default_ref="refs/heads/main",
            )

    def test_later_record_relocation_does_not_change_the_integration_commit(self) -> None:
        relocated = "docs/engineering/releases/RLS-TST-001.md"
        (self.root / relocated).parent.mkdir(parents=True, exist_ok=True)
        self.git("mv", self.record_path, relocated)
        self.commit("relocate historical release record")
        result = self.resolve()
        self.assertEqual(self.governance, result.governance_commit)
        self.assertEqual(self.record_path, result.release_record_path)

    def test_malformed_inputs_and_non_main_ref_are_rejected(self) -> None:
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "vMAJOR.MINOR.PATCH"):
            PUBLICATION.resolve_release(self.root, "latest", default_ref="refs/heads/main")
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "main integration branch"):
            PUBLICATION.resolve_release(self.root, "v1.2.3", default_ref="HEAD")


class GovernorDescriptorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / ".self-hosting").mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_descriptor(self, url: str) -> None:
        (self.root / ".self-hosting" / "governor.toml").write_text(
            f'''schema = 1
version = "0.3.0"
tag = "v0.3.0"
wheel = "se_harness-0.3.0-py3-none-any.whl"
url = "{url}"
sha256 = "{'a' * 64}"
selected_release_record = "RLS-SEH-005"
selected_candidate_commit = "{'b' * 40}"
''',
            encoding="utf-8",
        )

    def test_exact_github_release_governor_is_accepted(self) -> None:
        self.write_descriptor(
            "https://github.com/mmzen/se_harness/releases/download/"
            "v0.3.0/se_harness-0.3.0-py3-none-any.whl"
        )
        descriptor = PUBLICATION.read_governor(self.root)
        self.assertEqual("0.3.0", descriptor.version)
        self.assertEqual("a" * 64, descriptor.sha256)

    def test_other_host_or_query_is_rejected(self) -> None:
        self.write_descriptor(
            "https://example.invalid/mmzen/se_harness/releases/download/"
            "v0.3.0/se_harness-0.3.0-py3-none-any.whl"
        )
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "accepted GitHub release boundary"):
            PUBLICATION.read_governor(self.root)
        self.write_descriptor(
            "https://github.com/mmzen/se_harness/releases/download/"
            "v0.3.0/se_harness-0.3.0-py3-none-any.whl?replacement=1"
        )
        with self.assertRaises(PUBLICATION.PublicationError):
            PUBLICATION.read_governor(self.root)


class PayloadPackagingTests(unittest.TestCase):
    def write_bundle(
        self,
        *,
        revision: str | None = None,
        extra_resources: list[tuple[str, str, str, bytes]] | None = None,
    ) -> None:
        for directory in (self.source / "data", self.source / "content"):
            if directory.exists():
                shutil.rmtree(directory)
        observed_revision = revision or self.governance
        resources: list[tuple[str, str, str, bytes]] = []
        for role, schema, prefix, value in (
            (
                "summary",
                "harness-dashboard-summary-v2",
                "data/summary",
                {
                    "schema": "harness-dashboard-summary-v2",
                    "repository": {"name": "governance", "revision": observed_revision, "git_object_format": "sha1", "valid": True},
                },
            ),
            (
                "topology",
                "harness-dashboard-topology-v2",
                "data/topology",
                {"schema": "harness-dashboard-topology-v2", "repository_revision": observed_revision, "artifacts": [], "relations": []},
            ),
            (
                "readiness",
                "harness-dashboard-readiness-v2",
                "data/readiness",
                {"schema": "harness-dashboard-readiness-v2", "repository_revision": observed_revision, "readiness": [], "revision_provenance": []},
            ),
        ):
            resources.append((role, schema, prefix, PUBLICATION._json_bytes(value)))
        resources.extend(extra_resources or [])
        descriptors: list[dict] = []
        entrypoints: dict[str, dict] = {}
        for role, schema, prefix, content in resources:
            digest = sha256(content)
            suffix = "txt" if schema == "utf8-markdown-v1" else "json"
            path = f"{prefix}/{digest}.{suffix}"
            descriptor = {"role": role, "schema": schema, "path": path, "bytes": len(content), "sha256": digest}
            descriptors.append(descriptor)
            if role in {"summary", "topology", "readiness"}:
                entrypoints[role] = dict(descriptor)
            target = self.source.joinpath(*path.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        manifest = {
            "schema": "harness-dashboard-bundle-v2",
            "repository": {"name": "governance", "revision": observed_revision, "git_object_format": "sha1", "valid": True},
            "entrypoints": entrypoints,
            "resources": sorted(descriptors, key=lambda item: item["path"]),
        }
        self.manifest_bytes = PUBLICATION._json_bytes(manifest)
        (self.source / "dashboard-manifest.json").write_bytes(self.manifest_bytes)
        bootstrap = {
            "schema": "harness-dashboard-bootstrap-v2",
            "bundle_schema": "harness-dashboard-bundle-v2",
            "repository_revision": observed_revision,
            "manifest": {"path": "dashboard-manifest.json", "bytes": len(self.manifest_bytes), "sha256": sha256(self.manifest_bytes)},
        }
        bootstrap_json = json.dumps(bootstrap, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.dashboard_bytes = (
            '<html><body><div class="workspace">Explorer</div>'
            f'<script id="harness-dashboard-bootstrap" type="application/json">{bootstrap_json}</script>'
            "</body></html>\n"
        ).encode("utf-8")
        (self.source / "index.html").write_bytes(self.dashboard_bytes)
        (self.source / "generation-summary.json").write_bytes(
            PUBLICATION._json_bytes(
                {
                    "schema": "harness-dashboard-generation-v2",
                    "bundle_schema": "harness-dashboard-bundle-v2",
                    "outcome": "generated-valid",
                    "repository_revision": observed_revision,
                    "validator_error_count": 0,
                    "manifest_sha256": sha256(self.manifest_bytes),
                    "dashboard_sha256": sha256(self.dashboard_bytes),
                    "resource_count": len(descriptors),
                }
            )
        )

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self.root / "generated"
        self.source.mkdir()
        self.candidate = "a" * 40
        self.governance = "b" * 40
        self.provenance = PUBLICATION.ReleaseProvenance(
            repository="mmzen/se_harness",
            tag="v1.2.3",
            version="1.2.3",
            release_record="RLS-TST-001",
            release_record_path="docs/engineering/releases/RLS-TST-001.md",
            candidate_commit=self.candidate,
            git_object_format="sha1",
            governance_commit=self.governance,
            default_head="c" * 40,
        )
        self.provenance_path = self.root / "provenance.json"
        self.provenance_path.write_text(json.dumps(asdict(self.provenance)), encoding="utf-8")
        self.write_bundle()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_packaging_adds_constant_notice_and_exact_manifest(self) -> None:
        destination = self.root / "site"
        manifest = PUBLICATION.package_dashboard(self.source, destination, self.provenance_path)
        self.assertTrue(PUBLICATION.PUBLISHED_FIXED_FILES <= {path.name for path in destination.iterdir()})
        published = (destination / "index.html").read_bytes()
        self.assertIn(b"SE Harness development demonstration", published)
        self.assertIn(b"derived, read-only view", published)
        self.assertIn(b"Included artifact bodies and retained evidence are public", published)
        self.assertEqual(sha256(self.manifest_bytes), manifest["bundle_manifest_sha256"])
        self.assertEqual(sha256(published), manifest["published_dashboard_sha256"])
        self.assertEqual(3, len(manifest["resource_files"]))
        summary = json.loads((destination / "generation-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(sha256(published), summary["dashboard_sha256"])
        self.assertTrue(summary["publication"]["derived_non_authoritative"])

    def test_packaging_is_repeatable_for_identical_source_and_provenance(self) -> None:
        first = self.root / "first"
        second = self.root / "second"
        PUBLICATION.package_dashboard(self.source, first, self.provenance_path)
        PUBLICATION.package_dashboard(self.source, second, self.provenance_path)
        for name in PUBLICATION.PUBLISHED_FIXED_FILES:
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())

    def test_manifest_declared_raw_evidence_is_hash_verified_and_published(self) -> None:
        raw = b"# Retained evidence\n\nExact content.\n"
        digest = sha256(raw)
        raw_path = f"content/{digest}.txt"
        self.write_bundle(extra_resources=[("evidence", "utf8-markdown-v1", "content", raw)])

        destination = self.root / "content-site"
        manifest = PUBLICATION.package_dashboard(self.source, destination, self.provenance_path)
        self.assertEqual(raw, (destination / raw_path).read_bytes())
        self.assertIn(raw_path, manifest["resource_files"])

        (self.source / raw_path).write_bytes(b"tampered\n")
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "differs from its descriptor"):
            PUBLICATION.package_dashboard(self.source, self.root / "tampered", self.provenance_path)

    def test_unexpected_file_and_revision_mismatch_fail_closed(self) -> None:
        (self.source / "secret.txt").write_text("not public", encoding="utf-8")
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "differs from its manifest"):
            PUBLICATION.package_dashboard(self.source, self.root / "unexpected", self.provenance_path)
        (self.source / "secret.txt").unlink()
        self.write_bundle(revision="d" * 40)
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "selected governance snapshot"):
            PUBLICATION.package_dashboard(self.source, self.root / "mismatch", self.provenance_path)

    def test_github_release_metadata_must_be_final_and_exact(self) -> None:
        metadata = self.root / "release.json"
        metadata.write_text(
            json.dumps({"tagName": "v1.2.3", "isDraft": False, "isPrerelease": False}),
            encoding="utf-8",
        )
        PUBLICATION.verify_github_release(metadata, "v1.2.3")
        metadata.write_text(
            json.dumps({"tagName": "v1.2.3", "isDraft": True, "isPrerelease": False}),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "must not be a draft"):
            PUBLICATION.verify_github_release(metadata, "v1.2.3")


class PagesWorkflowPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    def test_workflow_has_only_main_controlled_replay_trigger(self) -> None:
        self.assertNotIn("  release:\n", self.workflow)
        self.assertIn("  workflow_dispatch:\n", self.workflow)
        self.assertNotIn("  push:\n", self.workflow)
        self.assertNotIn("  pull_request:\n", self.workflow)
        for name in ("release_record", "governance_commit"):
            self.assertIn(f"      {name}:\n", self.workflow)
        self.assertNotIn("      release_tag:\n", self.workflow)
        self.assertIn("github.repository == 'mmzen/se_harness'", self.workflow)
        self.assertIn("github.ref == 'refs/heads/main'", self.workflow)

    def test_actions_are_immutable_reviewed_pins(self) -> None:
        pins = {
            "actions/checkout": ("3d3c42e5aac5ba805825da76410c181273ba90b1", "v7.0.1"),
            "actions/setup-python": ("5fda3b95a4ea91299a34e894583c3862153e4b97", "v7.0.0"),
            "actions/configure-pages": ("45bfe0192ca1faeb007ade9deae92b16b8254a0d", "v6.0.0"),
            "actions/upload-pages-artifact": ("fc324d3547104276b827a68afc52ff2a11cc49c9", "v5.0.0"),
            "actions/deploy-pages": ("cd2ce8fcbc39b97be8ca5fce6e763baed58fa128", "v5.0.0"),
        }
        for action, (commit, release) in pins.items():
            self.assertIn(f"uses: {action}@{commit} # {release}", self.workflow)
        self.assertNotRegex(self.workflow, r"uses: actions/[a-z-]+@v[0-9]")

    def test_permissions_environment_and_concurrency_are_bounded(self) -> None:
        self.assertNotIn("contents: write", self.workflow)
        self.assertEqual(1, self.workflow.count("pages: write"))
        self.assertEqual(1, self.workflow.count("id-token: write"))
        self.assertIn("  group: se-harness-pages-demonstration\n", self.workflow)
        self.assertIn("  cancel-in-progress: false\n", self.workflow)
        self.assertIn("      name: github-pages\n", self.workflow)
        self.assertIn("url: ${{ steps.deployment.outputs.page_url }}", self.workflow)
        self.assertIn("persist-credentials: false", self.workflow)
        self.assertIn("fetch-depth: 0", self.workflow)

    def test_workflow_preserves_governor_generator_and_payload_boundaries(self) -> None:
        self.assertIn("governor-env/bin/harnessctl\" validate", self.workflow)
        self.assertIn("governance/scripts/generate_harness_dashboard.py", self.workflow)
        self.assertIn("publish_dashboard.py package", self.workflow)
        self.assertIn("--destination \"$RUNNER_TEMP/pages-site\"", self.workflow)
        self.assertNotIn("git push", self.workflow)
        self.assertFalse(
            (REPOSITORY_ROOT / "templates" / "repository" / "standard" / ".github" / "workflows" / "publish-dashboard-pages.yml").exists()
        )


if __name__ == "__main__":
    unittest.main()
