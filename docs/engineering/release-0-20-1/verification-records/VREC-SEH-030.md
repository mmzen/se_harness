+++
id = "VREC-SEH-030"
type = "verification_record"
title = "Verification candidate for WO-RLS-027"
status = "verified"
owners = ["Codex"]
created = "2026-09-30"
updated = "2026-09-30"
commit = "b9af631b850c495eace9807361ed3ec3e36a10b2"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-30T20:36:35Z"
prepared_by = "Codex"
artifact_snapshot_sha256 = "f4a69744fd86f049f64bf7ff52dd75daac6b5194e2e5f6de0b5fa37e34532fad"
evidence_paths = ["docs/engineering/release-0-20-1/evidence/WO-RLS-027/WO-RLS-027-handoff.md", "docs/engineering/release-0-20-1/evidence/WO-RLS-027/WO-RLS-027-pre-action.md", "docs/engineering/release-0-20-1/evidence/WO-RLS-027/assessment.md", "docs/engineering/release-0-20-1/evidence/WO-RLS-027/handoff.json", "docs/engineering/release-0-20-1/evidence/WO-RLS-027/hosted-ci.json", "docs/engineering/release-0-20-1/evidence/WO-RLS-027/plan.json", "docs/engineering/release-0-20-1/evidence/WO-RLS-027/review.md", "docs/engineering/release-0-20-1/evidence/WO-RLS-027/tests.json"]
evaluator_evidence_path = "docs/engineering/release-0-20-1/evidence/VREC-SEH-030-evaluator.json"
evaluator_evidence_sha256 = "e47384120e30c37f16266e887354cc5e0f5cb956e4d93c53fc7a5bd43ffec9c2"

verified_at = "2026-09-30T20:43:10Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-RLS-027"]
conforms_to = ["VER-RLS-027"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-30T20:43:10Z"
decided_by = "assurance-owner"
reason = "Human mmzen: I verify VREC-SEH-030 as assurance owner. Decision covers exact candidate b9af631b850c495eace9807361ed3ec3e36a10b2 and unchanged retained evidence reviewed at commit 7b68abb8bcf86515bc98b6d189681d3f5bf22038. VREC SHA256 d2f9eefbaeb1f1b0fd40f15664a5505a2243afd003db2438de8e536b9efe786d; evaluator evidence SHA256 e47384120e30c37f16266e887354cc5e0f5cb956e4d93c53fc7a5bd43ffec9c2; final observations SHA256 806463b7983be392ff531c7c97944d4e5a1fb7650d3994a59f1dad6b100fa69f. Codex applies the human decision using the selected 0.19.0 assurance-owner encoding. This decision does not authorize merge, release, publication or adoption."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-RLS-027` to candidate commit `b9af631b850c495eace9807361ed3ec3e36a10b2`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Candidate test run

Commit: `b9af631b850c495eace9807361ed3ec3e36a10b2`. Exit status: 0.

Command arguments: `["C:/Users/mathi/AppData/Local/Python/pythoncore-3.14-64/python.exe", "-X", "utf8", "-c", "import hashlib,json,pathlib,subprocess,sys\nreport=pathlib.Path(sys.argv[1]);expected=sys.argv[2];candidate=sys.argv[3]\nraw=report.read_bytes();assert hashlib.sha256(raw).hexdigest()==expected\nd=json.loads(raw);assert d['candidate']==candidate\nactual=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert actual==candidate\nassert not subprocess.check_output(['git','status','--porcelain'])\nassert d['ci']['headRefOid']==candidate\nassert all(x['status']=='COMPLETED' and x['conclusion'] in ('SUCCESS','SKIPPED') for x in d['ci']['statusCheckRollup'])\np=d['pinned_replay'];assert p['candidate']['commit']==candidate and p['state']=='exact'\nassert len(p['builds'])==2 and p['builds'][0]['wheel_sha256']==p['builds'][1]['wheel_sha256'] and p['builds'][0]['sdist_sha256']==p['builds'][1]['sdist_sha256']\nfor name in ('windows','linux'):\n v=d[name];assert v['passed'] and v['candidate_commit']==candidate\n assert len(v['checks'])==16 and all(x['exit_code']==0 for x in v['checks'])\n q=json.loads(next(x['stdout'] for x in v['checks'] if x['label']=='independent-released020-qualification'))\n assert q['passed'] and q['independence']=='released-verifier'\nassert d['sdist_parity']['equal'] and d['sdist_parity']['candidate_commit']==candidate\nr=subprocess.run([sys.executable,'scripts/run_tests.py','--workers','4','--scale','full'],capture_output=True,text=True,encoding='utf-8',errors='replace')\nlog=pathlib.Path(sys.argv[4]);log.write_text(r.stdout+r.stderr,encoding='utf-8')\nprint((r.stdout+r.stderr)[-2500:]);assert r.returncode==0\nprint('Final candidate observations: docs/engineering/release-0-20-1/evidence/WO-RLS-027/final-candidate-observations.json')\nprint('Observed evidence SHA256: '+expected)\nprint('This post-candidate evidence is retained with the generated record, not represented as committed candidate content.')\nprint(json.dumps({'candidate':candidate,'pr':508,'ci_checks':'all applicable passed','manual_replay_run':d['manual_replay_run']['url'],'wheel_sha256':p['manifest']['wheel_sha256'],'sdist_sha256':p['manifest']['sdist_sha256'],'installed_sdist_checks':'16 operations on each platform, including public 0.20.0 independent qualification','source_test_exit':r.returncode,'source_log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}))\n", "C:\\Users\\mathi\\Documents\\Codex\\2026-09-20\\verity-plane-plugin-verity-plane-se\\work\\maintenance-0-20-1\\docs\\engineering\\release-0-20-1\\evidence\\WO-RLS-027\\final-candidate-observations.json", "806463b7983be392ff531c7c97944d4e5a1fb7650d3994a59f1dad6b100fa69f", "b9af631b850c495eace9807361ed3ec3e36a10b2", "C:\\Users\\mathi\\Documents\\Codex\\2026-09-20\\verity-plane-plugin-verity-plane-se\\work\\compatibility-0201-evidence\\final-capture-source.log"]`.

```text
WEX_SCALE artifacts=100 validation=0.116285s focus=0.263088s plan=0.227957s
WEX_SCALE artifacts=500 validation=0.529719s focus=0.687532s plan=0.983902s
WEX_SCALE artifacts=1000 validation=1.035393s focus=1.198834s plan=1.957347s
Evaluator Python: C:\Users\mathi\AppData\Local\Temp\simple-plugin-nc3ug6wu\private\verity-plane\evaluator\Scripts\python.exe
Evaluator Python: C:\Users\mathi\AppData\Local\Temp\simple-plugin-nc3ug6wu\private\verity-plane\evaluator\Scripts\python.exe
docs/notes/diagnostic-codes.md matches the source
0.20.1
----------------------------------------------------------------------
Ran 1167 tests in 226.896s (178 classes, 4 workers)

OK (skipped=17)
--workers must be at least 1

Final candidate observations: docs/engineering/release-0-20-1/evidence/WO-RLS-027/final-candidate-observations.json
Observed evidence SHA256: 806463b7983be392ff531c7c97944d4e5a1fb7650d3994a59f1dad6b100fa69f
This post-candidate evidence is retained with the generated record, not represented as committed candidate content.
{"candidate": "b9af631b850c495eace9807361ed3ec3e36a10b2", "pr": 508, "ci_checks": "all applicable passed", "manual_replay_run": "https://github.com/mmzen/se_harness/actions/runs/36772527503", "wheel_sha256": "300923b4ea800487a7b96822768ff5fbd5c428305ac670948aef404282349764", "sdist_sha256": "a4c38a50e3614cfe8b478f7903af3b829e9d605b864d0ba3caca3816f4f2464a", "installed_sdist_checks": "16 operations on each platform, including public 0.20.0 independent qualification", "source_test_exit": 0, "source_log_sha256": "69deb6888f711b377d31c78803f2577cf677212868ff250aa32b137616fb0fcc"}
warning: unable to access 'C:\Users\mathi/.config/git/ignore': Permission denied
warning: unable to access 'C:\Users\mathi/.config/git/ignore': Permission denied

```
