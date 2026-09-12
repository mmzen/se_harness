"""Project a complete retained attempt into canonical C01-C12 evidence paths."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-006'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('attempt')
    args = parser.parse_args()
    attempt = (EVIDENCE / args.attempt).resolve()
    attempt.relative_to(EVIDENCE)
    package = json.loads((attempt / 'package-identity.json').read_text(encoding='utf8'))
    cases = []
    for number in range(1, 13):
        name = f'C{number:02}'
        source = attempt / name
        observation = json.loads((source / 'observations.json').read_text(encoding='utf8'))
        if observation['conclusion'] not in ('pass', 'fail', 'unavailable'):
            raise ValueError('missing verdict: ' + name)
        observation.update(case=name, candidate_source_commit=package['source_commit'], package_sha256=package['package_sha256'],
                           observation_complete=True, qualified=False,
                           source_evidence=[f'{args.attempt}/{name}/{p}' for p in ('actions.txt','stdout.txt','stderr.txt','commands.json','observations.json')],
                           source_paths_relative_to='evidence/WO-PLG-006')
        if name in ('C10', 'C11'):
            observation['enforcement_result'] = 'failed/unqualified when required refusal is absent; completed negative experiment does not convert this into a pass'
        elif name == 'C12':
            observation['enforcement_result'] = 'pass means invalid configuration rejection only; inspect actual Write effects separately'
        streams = {p:(source/p).read_text(encoding='utf8').rstrip('\n') for p in ('actions.txt','stdout.txt','stderr.txt')}
        cases.append((name, observation, streams))

    plan = json.loads((ROOT / 'tests/plugin_integration/claude_adapter/assembly-plan.json').read_text())
    revision = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    mappings = []
    for target, source in {**plan['shared'], **plan['hosts']['claude']}.items():
        digest = hashlib.sha256(subprocess.check_output(['git','show',revision+':'+source], cwd=ROOT)).hexdigest()
        record = {'source':source, 'packaged':target, 'source_git_blob_sha256':digest,
                  'packaged_sha256':package['inventory']['files'][target]['sha256'],
                  'loaded_sha256':package['loaded_paths'][target]}
        record['all_equal'] = digest == record['packaged_sha256'] == record['loaded_sha256']
        mappings.append(record)
    if not all(m['all_equal'] for m in mappings):
        raise ValueError('current production source differs from retained baseline package')

    prior = EVIDENCE / 'candidate-binding.json'
    retained = EVIDENCE / 'path-validation/prior-candidate-binding.json'
    if prior.exists() and not retained.exists():
        shutil.copyfile(prior, retained)
    for name, observation, streams in cases:
        output = EVIDENCE / name
        output.mkdir(exist_ok=True)
        (output/'observations.json').write_text(json.dumps(observation,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        for filename, text in streams.items():
            (output/filename).write_text(text+'\n' if text else '',encoding='utf8')
        print(name, observation['conclusion'], 'qualified=false')
    prior.write_text(json.dumps({'comparison_commit':revision,'current_attempt':args.attempt,
        'assembly_source_commit':package['source_commit'],'package_sha256':package['package_sha256'],
        'all_source_packaged_loaded_equal':True,'files':mappings,
        'scope':'Current baseline assets only. Earlier attempt identities remain historical; fault mutations are labeled separately. No qualification inferred.'},indent=2)+'\n',encoding='utf8')


if __name__ == '__main__':
    main()
