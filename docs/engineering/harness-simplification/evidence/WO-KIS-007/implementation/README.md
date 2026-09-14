# WO-KIS-007 implementation evidence

Source candidate: `9f734ab129d2328c89baddb549c4c40d60b8bec3`. Governing evaluator: isolated released 0.17.0.
WO-KIS-007 is implemented through delegated completion. Hosted checks passed or were intentionally skipped; exact results and URLs are in ci-implementation.json. Owner verification remains pending.

| Check | Implemented result | Evidence |
| --- | --- | --- |
| K32 | Deleted internal function/module inventories, exact source-spelling checks and object-identity assertions. Public CLI entry points and the real package/build-tools import boundary remain tested. | refactor-example.md runs three existing behavior tests unchanged after a private-helper rename; full source results cover retained public failures. |
| K33 | Replaced three autocrlf clone settings and aggressive Git GC with one real checkout for the running OS. Small LF/CRLF examples and the distinct Git attributes override case remain. | Hosted Linux full suite and hosted Windows checkout subset passed. No integrity test invokes aggressive GC. |
| K34 | Retained real linked Python environments, actual origin/path failures and one unavailable-path-resolution failure. Replaced eight fabricated identity rejection codes with one wrong-origin propagation case. | Hosted Windows subset passed (one POSIX-only case skipped); Linux full suite and existing cross-platform package installation checks passed. |

The original eight-capability runtime matrix was already removed by WO-KIS-003.
This work finishes the remaining test restrictions; it does not claim that earlier deletion again.

Tests shrink by **650 net lines** (709 removed, 59 added) and **33 test methods** relative to `c3d361353d0e5dea00078dd2413544395d593652`.
The module-seam inventory file is deleted. These are measurements of this patch,
not a claim of faster execution. The original review's 64-case runtime corpus is
not the before count for this work order.

| Run | Tests | Skipped | Seconds |
| --- | ---: | ---: | ---: |
| Local Windows / Python 3.14 / full scale | 1063 | 15 | 139.734 |
| Hosted Linux / Python 3.11 / full scale | 1063 | 2 | 32.317 |
| Hosted Windows / Python 3.11 / checkout and interpreter paths | 6 | 1 | 1.141 |

Exact commands, checker versions/origins and output tails are in the captured summaries.
The Windows subset's single skip is the declared POSIX virtualenv entry-point case;
the Windows checkout, junction, real environment and unavailable-path cases ran.
The hosted suites test PR merge commit `4769aae3f58028ff435037ff03e6c4333fd1fe88`; its implementation
paths were compared with the branch source above. They are distinct Git commits.
Both hosted logs were downloaded and their byte counts checked. raw-artifacts.json
records artifact IDs, URLs and observed expiry; raw logs remain outside Git.

The initial focused run passed 105 tests (2 skipped), workflow/suite hygiene passed
45 tests, and all workflow YAML parsed. All 14 distribution records, CLI help,
source/released graph and released review/scope checks passed. checks.json records
commands and outcomes. The small Windows step uses the existing upgrade job and
artifact; it adds no job or platform matrix. Publication rehearsals are skipped
because this patch changes no publication or build input.

Atomic-write failures, unsafe destinations, changed evidence, wrong checker
versions/origins and useful no-repeated-validation performance checks remain.
No product implementation, installed root policy, historical record or bound
archive is changed. Root adoption, release and owner verification remain separate.
