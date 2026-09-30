+++
id = "VREC-IAR-017"
type = "verification_record"
title = "Verification candidate for WO-IAR-027"
status = "ready"
owners = ["Codex preparation agent under mmzen approval"]
created = "2026-09-30"
updated = "2026-09-30"
commit = "1b54fb4854e20b3e9e4072f2b95bd60c4376fbfd"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-30T07:19:21Z"
prepared_by = "Codex preparation agent under mmzen approval"
artifact_snapshot_sha256 = "40ee8405074d9009d8e49fe083b514b2c6f6fbe5fdd40ddefcea1b1d0c5bc118"
evidence_paths = ["docs/engineering/instruction-architecture/evidence/WO-IAR-027/WO-IAR-027-handoff.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-027/checks.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-027/handoff.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-027/preservation.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-027/review-preflight.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-027/review.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-027/wording-review.json"]
evaluator_evidence_path = "docs/engineering/instruction-architecture/evidence/VREC-IAR-017-evaluator.json"
evaluator_evidence_sha256 = "5f2209f1d8d60901e7f8cf46ea5b62f7bb9705e4603c72f15489f9be90af2384"

[relations]
verifies_work_order = ["WO-IAR-027"]
conforms_to = ["VER-IAR-019"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-IAR-027` to candidate commit `1b54fb4854e20b3e9e4072f2b95bd60c4376fbfd`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Candidate test run

Commit: `1b54fb4854e20b3e9e4072f2b95bd60c4376fbfd`. Exit status: 0.

Command arguments: `["C:/Users/mathi/AppData/Local/Python/pythoncore-3.14-64/python.exe", "-X", "utf8", "-c", "\"\"\"Transient exact-candidate check for the approved glossary correction.\"\"\"\nimport hashlib,json,re,subprocess,sys,os\nfrom pathlib import Path\nrepo=Path.cwd().resolve()\nreview_path=Path(sys.argv[1])\nreview=json.loads(review_path.read_text(encoding='utf-8'))\nraw=(repo/'GLOSSARY.md').read_bytes();normalized=raw.replace(b'\\r\\n',b'\\n')\nassert hashlib.sha256(normalized).hexdigest()==review['proposed_lf_sha256']\ntext=normalized.decode('utf-8')\nfor change in review['changes']: assert change['after'] in text,change['section']\nlinks=[]\nfor target in re.findall(r'\\]\\(([^)]+)\\)',text):\n    path,_,anchor=target.partition('#');p=repo/path\n    assert p.is_file(),target\n    headings=[]\n    for heading in re.findall(r'^#+\\s+(.+)$',p.read_text(encoding='utf-8'),re.M):\n        headings.append(re.sub(r'[^\\w\\- ]','',heading.lower()).replace(' ','-'))\n    assert not anchor or anchor in headings,target\n    links.append(target)\nprint(json.dumps({'check':'reviewed glossary text and links','passed':True,'sha256_lf':hashlib.sha256(normalized).hexdigest(),'replacements':len(review['changes']),'links':links}),flush=True)\nargs=[sys.executable,'-X','utf8','-m','unittest','tests.test_glossary','tests.test_workflow_documentation_contract']\nprint(json.dumps({'argv':args,'cwd':str(repo)}),flush=True)\nr=subprocess.run(args,cwd=repo,timeout=300)\nprint(json.dumps({'exit_code':r.returncode}),flush=True)\nraise SystemExit(r.returncode)\n", "docs/engineering/instruction-architecture/evidence/WO-IAR-027/wording-review.json"]`.

```text
{"check": "reviewed glossary text and links", "passed": true, "sha256_lf": "4eb639dffb6308db4633c9f5046194041d27aca7e9ada7d49f4bd340c9c6f410", "replacements": 12, "links": ["docs/notes/getting-started.md", "docs/engineering/harness/VERIFY_OUTCOME.md#record-the-verification-decision", "docs/engineering/harness/RELEASE.md#obtain-the-release-decision-when-required", "docs/engineering/harness/AUTHORITY.md#decision-rights", "docs/engineering/harness/UPGRADE.md#upgrade-the-installed-harness", "docs/engineering/harness/CONTINUE.md#continue-selected-work", "docs/engineering/harness/RESULTS.md#report-a-lifecycle-result", "docs/engineering/harness/RESULTS.md#report-a-lifecycle-result", "docs/engineering/harness/PULL_REQUEST.md#check-a-governed-pull-request", "docs/engineering/harness/AUTHORITY.md#authority-from-work-approval", "docs/engineering/harness/RESULTS.md#report-a-lifecycle-result", "docs/engineering/harness/AUTHORITY.md#decision-rights", "docs/engineering/harness/RESULTS.md#gates", "docs/engineering/harness/EXCEPTIONS.md#availability"]}
{"argv": ["C:\\Users\\mathi\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe", "-X", "utf8", "-m", "unittest", "tests.test_glossary", "tests.test_workflow_documentation_contract"], "cwd": "C:\\Users\\mathi\\AppData\\Local\\Temp\\se-harness-candidate-wyn8df6y\\checkout"}
{"exit_code": 0}
.................
----------------------------------------------------------------------
Ran 17 tests in 4.513s

OK

```
