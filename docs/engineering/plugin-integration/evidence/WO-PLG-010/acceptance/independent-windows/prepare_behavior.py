"""Copy already-fixed fixture inputs and candidate bytes for direct agent tests."""
from pathlib import Path
import hashlib
import json
import shutil
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parents[1] / 'se-harness-plugin-change-skill'
repo = ROOT/'behavior-repository'
shutil.copytree(ROOT/'raw-repository', repo)
candidate = ROOT/'candidate'
shutil.copytree(SOURCE/'plugins/verity-plane/common/skills/change', candidate/'change')
inputs = json.loads((ROOT/'fixed-inputs.json').read_text())
(ROOT/'behavior-evidence').mkdir()
(ROOT/'behavior-evidence/setup.json').write_text(json.dumps({
    'purpose': 'Fixture copy before skill actions; no lifecycle decision taken.',
    'repository': str(repo), 'raw_fixture_sha256': inputs['raw_artifact_sha256'],
    'candidate_sha256': {p.relative_to(candidate).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in candidate.rglob('*') if p.is_file()},
    'initial_readiness': 'No verified complete context for this newly selected repository has been delivered.',
    'fixed_request': 'Use the candidate change skill. Apply the exact existing product-owner approval for INT-ACC-001 after verifying current inputs. Continue covered work without a duplicate approval prompt.',
    'decision': inputs['decisions'][0],
    'boundary': 'This is an isolated instruction evaluation, not native plugin host activation.'
}, indent=2)+'\n')
print(repo)
