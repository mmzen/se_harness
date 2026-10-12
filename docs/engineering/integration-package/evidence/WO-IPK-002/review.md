# Proposed bounded CI capacity correction

Observed at C43: the exact Git source archive is 542,105,600 bytes (about 517 MiB).
The integration-package build rejects it because MAX_ARCHIVE_TOTAL is 512 MiB.
The retained historical evidence crossed the limit; source and installed-package
checks passed. Repeating CI cannot correct this failure.

Propose a fixed 1 GiB archive and expanded-total budget in the existing builder.
Keep the 128 MiB per-member limit, 20,000-entry limit, all unsafe-path/link/duplicate
checks, wheel budgets, exact-commit export and two independent builds unchanged.
Keep all historical evidence. Add no CLI override or automatic growth.

The exact proposed implementation is in proposed.diff: one constant plus the
matching expectation and above-limit fixture (nine 128 MiB declared members).
The focused suite already tests archive limit +1, expanded-limit rejection before
extraction, member size, traversal, links, duplicate names, empty archive and entry
boundaries. Verify the real committed archive and the actual CI build/verification
jobs after this change, then record commit-bound assurance.

Cost: worst-case archive/extraction disk budget doubles; this is a bounded capacity
choice, not a performance improvement. Exporting less content would change the
accepted exact-commit comparison and evidence-selection rules and requires a larger
design change. Deleting or moving historical evidence would alter review access and
bindings. Neither alternative is part of this correction.

WO-IPK-002 and VER-IPK-002 are formal drafts. No CI implementation file or accepted artifact
has changed. WO-HAG-009/011 exclude CI policy, so a new bounded work order and its
verification must be approved before applying it. The old WO-CIP-009/VER-CIP-005
512 MiB observations and accepted historical versions remain unchanged.

The proposed three-line diff passed 19 focused tests in a disposable prototype. Released validation found 1,993 artifacts, zero errors and 63 existing warnings. The planned-path assessment covers both implementation files and the proposed records/evidence. Approval must confirm required commit-bound verification and the named draft-PR publication grant; no approval is recorded yet.

`diff
--- a/.github/scripts/build_integration_package.py
+++ b/.github/scripts/build_integration_package.py
@@ -39,7 +39,7 @@
 MAX_PAYLOAD_FILE = 128 * 1024 * 1024
 MAX_MANIFEST = 1024 * 1024
 MAX_ARCHIVE_MEMBER = 128 * 1024 * 1024
-MAX_ARCHIVE_TOTAL = 512 * 1024 * 1024
+MAX_ARCHIVE_TOTAL = 1024 * 1024 * 1024
 # WO-CIP-009: allow repository growth; directories count and byte budgets stay fixed.
 MAX_ARCHIVE_MEMBERS = 20_000
 MAX_WHEEL_MEMBERS = 20_000
--- a/tests/test_integration_package.py
+++ b/tests/test_integration_package.py
@@ -277,7 +277,7 @@
 
     def test_archive_byte_budgets_remain_enforced_before_extraction(self) -> None:
         self.assertEqual(128 * 1024 * 1024, integration.MAX_ARCHIVE_MEMBER)
-        self.assertEqual(512 * 1024 * 1024, integration.MAX_ARCHIVE_TOTAL)
+        self.assertEqual(1024 * 1024 * 1024, integration.MAX_ARCHIVE_TOTAL)
         archive = self.root / "byte-budget.tar"
         self.write_tar(archive, [("pyproject.toml", b"abc"), ("se_harness/__init__.py", b"x")])
         with mock.patch.object(integration, "MAX_ARCHIVE_MEMBER", 2):
@@ -290,7 +290,7 @@
         self.assertFalse((self.root / "archive-budget").exists())
 
         # Test declared expanded sizes without allocating hundreds of MiB.
-        members = [tarfile.TarInfo(f"large-{index}") for index in range(5)]
+        members = [tarfile.TarInfo(f"large-{index}") for index in range(9)]
         for member in members:
             member.size = 128 * 1024 * 1024
         with mock.patch.object(integration.tarfile, "open") as open_archive:
`
