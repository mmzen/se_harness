# WO-DOC-017: README restoration

The owner approved the exact presented README package with "i approive" on
2026-09-20. Released 0.18.0 recorded VER-DST-030 and WO-DOC-017 approval, then
started the work under the existing execution grant. README.md now matches
the reviewed SHA-256 6566a636021d3aaa29345094ad19362289cd26efe01b3684a26da57e7c2d2c9d.

## Change and review

Restored the previously reviewed CLI setup section, including Windows/Linux
environment creation, init/doctor examples, adoption and safe upgrade guidance.
Preserved plugin onboarding and the two navigation links on origin/main at
2b87e04490b933a71a9986c0235ea8b201b3bffc. No tests or product code changed in this order.
The result has 604 words, 110 lines and six level-two headings, within the
approved presentation budget. Existing requirements and tests were reused.
Historical approval/evidence files were left unchanged.

The exact patch, restored text and local render were reviewed. There were no
material remaining findings in this documentation change. Reusing the earlier
text was the smallest correction; no new installation route or dependency was
introduced. The locally checked render had no broken images/links or desktop
and mobile horizontal overflow. It is not a hosted GitHub render or publication.

## Actual checks

| Check | Result |
| --- | --- |
| Applied onboarding + progressive documentation | 32 passed |
| Windows Python 3.14.6 full source suite | 1081 run; no failures; 15 skipped |
| Ubuntu/WSL Python 3.12.3 full source suite | 1081 run; no failures; 2 skipped |
| Released 0.18.0 doctor, graph, review and Git-derived documentation scope | Passed |
| Distribution provenance, CLI help and whitespace | Passed |
| README init/doctor syntax | Candidate and released parsers passed |
| Earlier proposal tests | 32 passed against redirected README input; kept separately from applied checks |

Both full suites ran the normal scale. The existing hosted Python 3.11/full-scale
CI route was not run. No network package install or new plugin qualification is
claimed. The prior 12 onboarding failures retained under WO-KIS-010/014 are now
absent in these combined-source runs; old failures and records remain intact.

## Inputs and boundaries

Tests ran on HEAD c90a3dbf7d56c2554aeca0f9fa87010f24960062 plus the three working files
listed and hashed in logs/doc017-windows-suite.json and
logs/doc017-linux-input.json. The Linux run reconstructed the same HEAD and
working bytes in a native temporary checkout, with the verified source origin.
Source files stayed fixed during the runs. Later evidence and completion
metadata do not change README or executable/test bytes; compare them explicitly
before preparing commit-bound verification. This summary is not a VREC decision.

This work's Git base is c90a3dbf7d56c2554aeca0f9fa87010f24960062; it owns only the README
repair and its approved records. It does not relabel or hide the earlier
WO-KIS-014 implementation, whose original base and scope checks remain retained.
Completion/handoff results, when obtained, are retained under logs/. Record
states and the future VREC govern the current lifecycle; this check summary
does not claim independent assurance, merge or publication.

The exact reviewed diff is retained in README.patch.zip (entry README.patch).
Its intentional blank context lines triggered the staged whitespace check as
plain text. The ZIP preserves those bytes; product Markdown was unaffected.
The original result and resolution are in logs/patch-retention-whitespace.json.
