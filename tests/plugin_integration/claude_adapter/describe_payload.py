"""Read-only inventory of the exact disposable content proposed for Claude."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import support as s


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox', type=Path, required=True)
    args=parser.parse_args()
    space=args.sandbox.resolve()
    data=json.loads((space/'run.json').read_text())
    repo=Path(data['repo'])
    plugin=Path(data['plugin'])
    files=[]
    for origin,folder in [('released-evaluator initialized synthetic repository',repo),('accepted package shared skills',plugin/'skills')]:
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                raw=path.read_bytes()
                files.append({'origin':origin,'path':str(path),'bytes':len(raw),'sha256':s.sha(path)})
    ancestors=[str(p/'CLAUDE.md') for p in repo.parents if (p/'CLAUDE.md').exists()]
    value={'destination':'Claude Code 2.1.266 official Anthropic service, api.anthropic.com/v1/messages',
        'scope':'WO-PLG-006 C01-C12 synthetic disposable adapter tests only',
        'representative_inspected_sandbox':str(space),'package_source_revision':data['revision'],
        'content_sent_by_hook':['Exact released 0.16.0 AGENTS.md managed gate','Exact released 0.16.0 ENGINEERING_HARNESS.md router','Runtime refusal/coverage diagnostics containing disposable paths and fixed version/hash values'],
        'other_model_context':['Released fixture CLAUDE.md and installed managed instructions','Packaged shared skill metadata and selected skill content','Explicit synthetic test prompts and Read results for the two fixture target files','Local fixture paths, host/OS/environment metadata normally supplied by Claude Code'],
        'target_contents':{p.name:p.read_text(encoding='utf8') for p in repo.glob('*.txt')},
        'ancestor_CLAUDE_files':ancestors,'fixture_has_git_repository':(repo/'.git').exists(),
        'source_exclusions':['No product implementation checkout mounted as the host working directory','No real work-order transition or product source edit','No observer read/copy of credential contents; existing isolated profile is used through normal Claude CLI authentication','No normal-profile plugin installation or host upgrade'],
        'actual_inspection':files,
        'proposed_shell_command':"$env:GIT_CONFIG_COUNT='1'; $env:GIT_CONFIG_KEY_0='safe.directory'; $env:GIT_CONFIG_VALUE_0='C:/Users/mathi/Documents/Codex/2026-09-04/hel/work/se-harness-plugin-claude-adapter'; & 'C:/Users/mathi/AppData/Local/Python/pythoncore-3.14-64/python.exe' -I -B -S tests/plugin_integration/claude_adapter/run_acceptance.py --sandbox '../plugin-probe-sandboxes/claude-adapter-20260911-04' --evidence 'docs/engineering/plugin-integration/evidence/WO-PLG-006/acceptance-04' --cases C01,C02,C03,C04,C05,C06,C07,C08,C09,C10,C11,C12",
        'approval_boundary':'No API-backed retry is made by this inventory. Network execution awaits the specifically requested user authorization.'}
    print(json.dumps(value,indent=2))


if __name__=='__main__':
    main()
