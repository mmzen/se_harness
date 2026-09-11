"""Synthetic preservation and refusal cases; no production fixture is modified."""

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("stack_integration_check", Path(__file__).with_name("check.py"))
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
DOMAIN = check.DOMAIN
WO = DOMAIN + "work-orders/WO-PLG-010.md"
VREC = DOMAIN + "verification-records/VREC-PLG-007.md"
SIDECAR = DOMAIN + "evidence/VREC-PLG-007-evaluator.json"


class IntegrationCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="plg018-check-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME="Synthetic fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Synthetic fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
        self.git("init", "-q", "--object-format=sha1")
        self.write("policy.txt", b"Unchanged baseline\n")
        self.write("integration/existing.txt", b"An integration-only baseline file\n")
        self.base = self.commit()
        self.write("evidence/fact.txt", b"Observed fixture result\n")
        self.bound = self.commit()
        self.import_scope = ["payload/", "evidence/", WO, VREC, SIDECAR]
        self.write("payload/skill.md", b"Frozen implementation\n")
        self.write(SIDECAR, b'{"evaluator":"fixture"}\n')
        self.write(WO, ("+++\nid = \"WO-PLG-010\"\ntype = \"work_order\"\nstatus = \"implemented\"\n"
                        "[execution_scope]\npaths = " + json.dumps(self.import_scope) + "\n+++\n").encode())
        self.write_record()
        self.source = self.commit()
        self.plan_file = self.root / "approved-plan.json"
        self.plan = self.make_plan()
        self.approved = self.save_plan(self.plan)

    def git(self, *args, input=None):
        result = subprocess.run(["git", "-c", f"safe.directory={self.repo.as_posix()}",
                                 "-c", "core.autocrlf=false", "-c", "core.longpaths=true",
                                 "-c", "core.hooksPath=" + str(self.root / "no-hooks"),
                                 "-C", str(self.repo), *args], input=input, env=self.env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
        return result.stdout.decode("utf-8").strip()

    def write(self, name, data):
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def commit(self):
        self.git("add", "--all")
        self.git("commit", "-q", "-m", "Synthetic fixture")
        return self.git("rev-parse", "HEAD")

    def write_record(self):
        self.write(VREC, ("+++\nid = \"VREC-PLG-007\"\ntype = \"verification_record\"\n"
                          "status = \"verified\"\ncommit = " + json.dumps(self.bound) + "\n"
                          "git_object_format = \"sha1\"\nworktree_state = \"clean\"\n"
                          "evidence_paths = [\"evidence/fact.txt\"]\n"
                          "evaluator_evidence_path = " + json.dumps(SIDECAR) + "\n"
                          "evaluator_evidence_sha256 = " + json.dumps(check.digest((self.repo / SIDECAR).read_bytes()))
                          + "\n[relations]\nverifies_work_order = [\"WO-PLG-010\"]\n+++\n").encode())

    def make_plan(self):
        reader = check.Git(self.repo)
        baseline, source = reader.tree(self.base), reader.tree(self.source)
        changes = [{"path": name, "change": "A" if name not in baseline else "M",
                    "base": None if name not in baseline else dict(zip(("mode", "blob"), baseline[name])),
                    "expected": dict(zip(("mode", "blob"), source[name])),
                    "source_work_orders": ["WO-PLG-010"]}
                   for name in sorted(source)
                   if baseline.get(name) != source[name] and check.covered(name, self.import_scope)]
        expected = baseline.copy()
        expected.update({c["path"]: source[c["path"]] for c in changes})
        return {"schema": "plugin-stack-integration-plan-v1", "base_main": self.base,
                "source_heads": {"fixture": self.source},
                "assembly": {"left": self.source, "right": self.source, "conflicts": False,
                             "expected_tree": check.tree_oid(expected)},
                "source_import_scope": self.import_scope, "integration_only_scope": ["integration/"],
                "source_changed_paths": len(changes), "source_change_counts": dict(check.Counter(c["change"] for c in changes)),
                "source_archive_entries": check.archive_entries(expected), "archive_entry_limit": 10000,
                "changes": changes, "verified_records_and_preserved_history": [
                    {"id": "VREC-PLG-007", "status": "verified", "candidate": self.bound,
                     "verifies_work_order": ["WO-PLG-010"], "selected_evidence_files": 1,
                     "record_blob": source[VREC][1], "record_sha256": check.digest((self.repo / VREC).read_bytes()),
                     "evaluator_sha256": check.digest((self.repo / SIDECAR).read_bytes())}]}

    def save_plan(self, plan):
        self.plan_file.write_text(json.dumps(plan, sort_keys=True), encoding="utf-8")
        return check.digest(self.plan_file.read_bytes())

    def verify(self, candidate=None, approved=None):
        return check.verify(self.repo, candidate or self.source, self.plan_file, approved or self.approved)

    def refused(self, pattern, candidate=None, approved=None):
        with self.assertRaisesRegex(check.Refusal, pattern):
            self.verify(candidate, approved)

    def snapshot(self):
        # Include worktree, refs, objects, index and logs, but not filesystem atime.
        return {p.relative_to(self.repo).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.repo.rglob("*") if p.is_file()}

    def test_preserved_candidate_and_reads_do_not_mutate(self):
        before = self.snapshot()
        result = self.verify()
        self.assertTrue(result["passed"])
        self.assertEqual(result["imported_paths"], 5)
        self.assertEqual(result["preserved_records"][0]["selected_evidence_files"], 1)
        self.assertEqual(before, self.snapshot())

    def test_integration_only_additions_and_modifications(self):
        self.write("integration/existing.txt", b"New integration observation\n")
        self.write("integration/new/report.json", b"{}\n")
        candidate = self.commit()
        self.assertTrue(self.verify(candidate)["passed"])

    def test_expected_preview_tree_does_not_need_to_exist(self):
        self.write("payload/skill.md", b"A different frozen source\n")
        self.write("integration/existing.txt", b"New integration content\n")
        self.source = self.commit()
        plan = self.make_plan()
        self.approved = self.save_plan(plan)
        with self.assertRaises(check.Refusal):
            check.Git(self.repo).kind(plan["assembly"]["expected_tree"], "tree")
        self.assertTrue(self.verify()["passed"])

    def test_incorrect_expected_tree_digest_is_rejected(self):
        invalid = copy.deepcopy(self.plan)
        invalid["assembly"]["expected_tree"] = "0" * 40
        self.approved = self.save_plan(invalid)
        self.refused("Pinned assembly differs")

    def test_tree_hash_matches_git_directory_order(self):
        for name in ("a/item", "a.txt", "a-else", "évidence/file", "a0"):
            self.write("integration/" + name, name.encode())
        candidate = self.commit()
        reader = check.Git(self.repo)
        self.assertEqual(check.tree_oid(reader.tree(candidate)), self.git("rev-parse", candidate + "^{tree}"))

    def test_changed_import_payload_is_rejected(self):
        self.write("payload/skill.md", b"Unauthorized behavior\n")
        self.refused("Candidate differs", self.commit())

    def test_changed_import_mode_is_rejected(self):
        self.git("update-index", "--chmod=+x", "payload/skill.md")
        self.git("commit", "-q", "-m", "Executable mode tamper")
        self.refused("Candidate differs", self.git("rev-parse", "HEAD"))

    def test_changed_record_is_rejected(self):
        self.write(VREC, (self.repo / VREC).read_bytes().replace(b'"verified"', b'"ready"'))
        self.refused("Candidate differs", self.commit())

    def test_unlisted_path_inside_import_prefix_is_rejected(self):
        self.write("payload/new.md", b"Not a planned import\n")
        self.refused("Candidate differs", self.commit())

    def test_baseline_change_and_deletion_are_rejected(self):
        for operation in ("modify", "delete"):
            with self.subTest(operation=operation):
                self.git("reset", "--hard", self.source)
                if operation == "modify":
                    self.write("policy.txt", b"Unapproved policy\n")
                else:
                    (self.repo / "policy.txt").unlink()
                self.refused("Candidate differs", self.commit())

    def test_same_tree_with_missing_source_ancestry_is_rejected(self):
        tree = self.git("rev-parse", self.source + "^{tree}")
        candidate = self.git("commit-tree", tree, "-p", self.base, input=b"Squashed fixture\n")
        self.refused("Missing required ancestry", candidate)

    def test_altered_plan_and_coordinated_payload_tampering_are_rejected(self):
        original = self.approved
        altered = copy.deepcopy(self.plan)
        altered["archive_entry_limit"] = 9999
        self.save_plan(altered)
        self.refused("independently approved digest")
        self.write("payload/skill.md", b"Coordinated unapproved change\n")
        self.source = self.commit()
        self.plan = self.make_plan()
        self.save_plan(self.plan)
        self.refused("independently approved digest", approved=original)

    def test_record_evidence_must_exist_at_bound_commit(self):
        self.bound = self.base  # New source record names a commit before evidence existed.
        self.write_record()
        self.source = self.commit()
        self.approved = self.save_plan(self.make_plan())
        self.refused("Selected evidence absent from bound candidate")

    def test_later_pinned_evidence_refresh_does_not_rewrite_history(self):
        self.write("evidence/fact.txt", b"Later explanatory receipt\n")
        self.source = self.commit()
        self.approved = self.save_plan(self.make_plan())
        record = self.verify()["preserved_records"][0]
        self.assertEqual(record["current_evidence_entries_differ_from_bound_commit"], 1)

    def test_missing_historical_blob_is_rejected(self):
        # A later imported version keeps the current tree readable while the
        # original selected evidence object is deliberately absent.
        blob = check.Git(self.repo).tree(self.bound)["evidence/fact.txt"][1]
        self.write("evidence/fact.txt", b"Current receipt\n")
        self.source = self.commit()
        self.approved = self.save_plan(self.make_plan())
        loose_object = self.repo / ".git/objects" / blob[:2] / blob[2:]
        loose_object.chmod(stat.S_IREAD | stat.S_IWRITE)  # Git objects are read-only on Windows.
        loose_object.unlink()
        self.refused("Missing evidence or imported blob")

    def test_archive_count_includes_directories(self):
        small_limit = copy.deepcopy(self.plan)
        small_limit["archive_entry_limit"] = small_limit["source_archive_entries"]
        self.approved = self.save_plan(small_limit)
        self.write("integration/one/two/new.txt", b"An added leaf and directories\n")
        self.refused("Archive entry limit exceeded", self.commit())

    def test_in_repository_plan_must_match_committed_plan(self):
        self.plan_file = self.repo / "integration/plan.json"
        self.save_plan(self.plan)
        candidate = self.commit()
        self.assertTrue(self.verify(candidate)["passed"])
        altered = copy.deepcopy(self.plan)
        altered["archive_entry_limit"] = 9999
        (self.repo / "integration/plan.json").write_text(json.dumps(altered), encoding="utf-8")
        candidate = self.commit()
        self.save_plan(self.plan)  # Restored external input cannot hide the committed tamper.
        self.refused("Candidate plan differs", candidate)

    def test_missing_and_malformed_inputs_fail_closed(self):
        for candidate in ("HEAD", "--help", "f" * 40):
            with self.subTest(candidate=candidate):
                self.refused("immutable|Git read failed", candidate)
        for key, value in (("changes", []), ("archive_entry_limit", 10001),
                           ("source_changed_paths", True), ("source_heads", {})):
            with self.subTest(key=key):
                invalid = copy.deepcopy(self.plan)
                invalid[key] = value
                approved = self.save_plan(invalid)
                self.refused("Missing|Invalid|Incorrect", approved=approved)
        invalid = copy.deepcopy(self.plan)
        invalid["changes"][0]["path"] = "../escape"
        approved = self.save_plan(invalid)
        self.refused("Unsafe repository path", approved=approved)

    def test_approved_but_inconsistent_plan_is_rejected(self):
        for field in ("base", "expected"):
            with self.subTest(field=field):
                invalid = copy.deepcopy(self.plan)
                invalid["changes"][0][field] = {"mode": "100644", "blob": "1" * 40}
                approved = self.save_plan(invalid)
                self.refused("Incorrect baseline|absent from pinned sources", approved=approved)

    def test_duplicate_json_key_is_rejected(self):
        raw = self.plan_file.read_bytes().rstrip()
        raw = raw[:-1] + b',"archive_entry_limit":10000}'
        self.plan_file.write_bytes(raw)
        self.refused("Duplicate JSON key", approved=check.digest(raw))

    def test_repository_environment_and_replacement_refs_cannot_fake_ancestry(self):
        tree = self.git("rev-parse", self.source + "^{tree}")
        candidate = self.git("commit-tree", tree, "-p", self.base, input=b"Unrelated source history\n")
        self.git("replace", candidate, self.source)
        before = self.snapshot()
        with patch.dict(os.environ, {"GIT_DIR": str(self.root / "missing"), "GIT_WORK_TREE": str(self.root),
                                     "GIT_INDEX_FILE": str(self.root / "other-index")}):
            self.refused("Missing required ancestry", candidate)
            self.assertTrue(self.verify()["passed"])
        self.assertEqual(before, self.snapshot())

    def test_cli_returns_machine_readable_failure_without_mutation(self):
        before = self.snapshot()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = check.main(["--repository", str(self.repo), "--candidate", self.source,
                                 "--plan", str(self.plan_file), "--approved-plan-sha256", "0" * 64])
        self.assertEqual(status, 1)
        self.assertFalse(json.loads(output.getvalue())["passed"])
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main(verbosity=2)
