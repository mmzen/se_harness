"""Reapply public-capture sanitization; never opens a host profile or raw log."""
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('probe', Path(__file__).with_name('probe.py'))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

root = probe.ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-004'
changed = []
inspected = 0
for path in sorted(root.rglob('*')):
    relative = path.relative_to(root)
    if not path.is_file() or 'governance' in relative.parts or path.name == 'redaction-audit.json':
        continue
    if path.suffix not in {'.txt', '.json', '.jsonl'}:
        continue
    text = path.read_text(encoding='utf-8-sig')
    public = probe.sanitize_text(text)
    if path.suffix == '.json':
        json.loads(public)
    elif path.suffix == '.jsonl':
        for line in public.splitlines():
            json.loads(line)
    inspected += 1
    if public != text:
        probe.publish_text(path, public)
        changed.append(str(relative).replace('\\', '/'))

probe.publish_json(root / 'redaction-audit.json', {
    'policy': 'sanitized-public-v1', 'files_inspected': inspected,
    'files_changed': changed, 'host_profiles_opened': False,
    'private_raw_captures_opened': False, 'governance_directory_excluded': True,
    'sanitizer_source_sha256': probe.digest(Path(__file__).with_name('probe.py')),
    'note': 'Public captures are sanitized observations, not byte-for-byte raw logs. Local raw debug logs remain outside the checkout.'})
print(json.dumps({'files_inspected': inspected, 'files_changed': len(changed)}))
