# Independent WO012 helper archive review

Passed bounded retention review at `6db8bd61d91a0785d79a7bb1db3b70f815f58d39`.

The oracle was frozen from Git `5aba54143d43d1b64be4b6cb2529c30570cabc26` before candidate ZIP inspection. Its SHA-256 is `ec08a100e7e352dc468f8aadf003601b0b71765ed8c0b5793da7e6827256a9fd`; the original inventory remains `332a379e7fc242ab869998495de624135718115743ebffe145d9b3cb42800119`.

All 415 ZIP payloads, totaling 4,785,760 bytes, equal their original Git blobs byte for byte. Entry names, uniqueness, file types, sizes, CRCs, and hashes pass independent reconciliation. The original REPORT.md, audit.json, inventory.json, and source-path-map.json are unchanged. All 415 former loose payloads are absent. Candidate raw.zip is 1,196,071 bytes, SHA-256 `77989599bf2db7c68636cf614e285a9794c191cee0a64c92576b4882a9314311`.

The actual committed checker passed the exact disposable package; rejected a one-byte raw payload mutation after outer archive/index metadata was updated; and rejected coordinated payload, original-inventory, and index alteration. Both refusals returned 1. Restored checks returned 0, and independent six-file snapshots prove the fixture restored and source package unchanged. Checker SHA-256: `f931406a355890a91d4f18c5c41b705fec0b1165524e4f7a335c588236e82c22`.

Native Linux Python 3.12.3 called the actual committed build_integration_package.py `extract_safe_archive` against the exact Git archive. It successfully extracted 9,816 members (8,127 regular files and 1,689 directories), under the unchanged 10,000-member limit. The 138,752,000-byte archive has SHA-256 `0b2577a1a27fcefb0858c1e0d212aa3badc1ad449129c28b54dc251bc017c178`. The actual guard source SHA-256 is `2f8228f5a1b054def1787922d24f98efe21a4a9158c6d1cf3fe5767f5147bf89`. All six extracted helper package files match the Windows-reviewed and committed bytes.

The complete committed diff against parent `731014d8fa58ba193f6eaf05af3408ed5c41e43f` is retained and stays within WO012 product, tests, evidence, and work-order paths. The narrow repack diff `5aba5414..290f4425` removes exactly 415 raw copies and adds two archive files; its other changes are the retention checker and WO012 evidence/retention records. Product skill and CI bytes are unchanged since the original 5aba commit. The repack is an ancestor of the tested merge candidate.

Original review setup failures remain visible: an initial working-tree scope read omitted Windows longpaths and showed projected deletions plus inherited governance; the first committed review formed a double slash in one Git blob path; the second used the whole WO012 parent for a narrow removal expectation. Each was corrected without source changes. Original raw records and executed source snapshots are retained alongside the corrected committed result. These are review setup defects, not candidate failures.

This review covers byte preservation, scoped checker tamper behavior, and native archive/extraction only. It does not rerun native helpers, model reasoning, full source tests, a full integration build, or CI, and makes no lifecycle or assurance decision.

The four-file bundle contains this report, audit.json, inventory.json, and raw.zip of exact flat raw records/scripts/original helper bytes. inventory.json binds every member. The whole-repository tar stream, extracted repository, and disposable fixture remain outside this bundle; the tar is reproducible from the immutable Git commit and exact recorded archive argv. No source files or Git state were changed by this review.
