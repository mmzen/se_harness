"""Actual importer variants in disposable source copies; no accepted import writes."""
import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

from qualify_boundaries import Boundaries
from hosted_artifact_graph.canonical import canonical_json
from hosted_artifact_graph.protocol import Refusal, EVALUATOR
from hosted_artifact_graph.service import Service


class Imports(Boundaries):
    def check_import(self, name, service, manifest, allowed):
        request = {'schema': 'se-harness-remote-command/v1', 'project_id': self.project,
                   'operation': 'import', 'operation_key': str(uuid.uuid4()),
                   'expected_project_version': self.snapshot()['version'],
                   'expected_evaluator': EVALUATOR, 'client': self.config['client'],
                   'source_manifest': manifest}
        before = self.snapshot()
        try:
            result = service.command(self.principal('operator'), request)
        except Refusal as exc:
            result = exc.result()
        after = self.snapshot()
        self.record(name, {'request': request, 'result': result, 'before': before, 'after': after})
        if result.get('error', {}).get('code') not in {'HAG_REMOTE_' + c for c in allowed}:
            self.failures.append(name)
        if name == 'duplicate-document-id' and 'REQ-RLO-019' not in result.get('error', {}).get('message', ''):
            self.failures.append(name + ': missing duplicate identity')
        assert before == after, name

    def imports(self):
        self.failures = []
        manifest = copy.deepcopy(self.service.evaluator.manifest)
        duplicate = copy.deepcopy(manifest)
        duplicate['artifacts'][1]['artifact_id'] = duplicate['artifacts'][0]['artifact_id']
        self.check_import('duplicate-manifest-id', self.service, duplicate, {'INVALID_IMPORT'})
        explorer = {'schema': 'explorer-export', 'nodes': [], 'edges': []}
        self.check_import('unsupported-explorer-export', self.service, explorer, {'INVALID_IMPORT'})
        changed = copy.deepcopy(manifest)
        changed['artifacts'][0]['raw_sha256'] = 'ab' * 32
        self.check_import('same-provenance-changed-declared-bytes', self.service, changed, {'SOURCE_MISMATCH'})

        chosen = next(x for x in manifest['artifacts'] if x['artifact_id'] == 'REQ-IAR-030')
        raw = (self.service.evaluator.source / chosen['path']).read_bytes()
        variants = {
            'duplicate-document-id': raw.replace(b'id = "REQ-IAR-030"', b'id = "REQ-RLO-019"', 1),
            'unresolved-document-target': raw.replace(b'"CAP-IAR-002"', b'"CAP-IAR-999"'),
        }
        for name, proposed in variants.items():
            assert proposed != raw
            with tempfile.TemporaryDirectory(prefix='hag-import-variant-') as directory:
                base = Path(directory)
                source = base / 'source'
                shutil.copytree(self.service.evaluator.source, source)
                (source / chosen['path']).write_bytes(proposed)
                env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
                env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
                def git(*args):
                    return subprocess.check_output(['git', '-c', 'core.hooksPath=/dev/null', '-c',
                        'core.autocrlf=false', '-c', 'user.name=Sandbox fixture', '-c',
                        'user.email=sandbox@example.invalid', *args], cwd=source, env=env, stderr=subprocess.PIPE).decode().strip()
                git('init', '--quiet', '--template=')
                git('add', '--all')
                git('commit', '--quiet', '--no-gpg-sign', '-m', 'Synthetic import refusal fixture: ' + name)
                commit = git('rev-parse', 'HEAD')
                variant = copy.deepcopy(manifest)
                variant['source']['commit'] = commit
                support = copy.deepcopy(self.service.evaluator.support)
                support['source'] = variant['source']
                entry = next(x for x in variant['artifacts'] if x['path'] == chosen['path'])
                entry.update(bytes=len(proposed), raw_sha256=hashlib.sha256(proposed).hexdigest(),
                             blob_oid=git('rev-parse', 'HEAD:' + chosen['path']))
                item = next(x for x in support['files'] if x['path'] == chosen['path'])
                item.update(bytes=len(proposed), sha256=hashlib.sha256(proposed).hexdigest())
                # Declared unique IDs cannot conceal a duplicate in canonical content.
                config = copy.deepcopy(self.config)
                config.update(source_directory=str(source), source_manifest=str(base/'manifest.json'),
                              source_inventory=str(base/'inventory.json'))
                (base/'manifest.json').write_bytes(canonical_json(variant))
                (base/'inventory.json').write_bytes(canonical_json(support))
                config['components']['deployment_sha256'] = hashlib.sha256(canonical_json({
                    'configuration': {k:v for k,v in config.items() if k != 'components'},
                    'compose_sha256': hashlib.sha256(Path('/opt/compose.yaml').read_bytes()).hexdigest()
                })).hexdigest()
                other = Service(config, self.credentials)
                try:
                    self.check_import(name, other, variant, {'INVALID_IMPORT'})
                finally:
                    other.store.driver.close()
                self.record(name + '-fixture', {'derived_from': manifest['source'], 'synthetic_commit': commit,
                    'changed_path': chosen['path'], 'changed_document_utf8': proposed.decode(),
                    'changed_git_blob_oid': entry['blob_oid'], 'no_original_input_changed': True})
        assert not self.failures, self.failures


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path('/run/config/config.json'))
    parser.add_argument('--credentials', type=Path, default=Path('/run/secrets/sandbox_credentials'))
    parser.add_argument('--endpoint', default='http://service:8080')
    parser.add_argument('--walkthrough', type=Path, required=True)
    parser.add_argument('--continuation', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); args.only = 'imports'
    suite = Imports(args)
    try:
        suite.run()
    finally:
        suite.service.store.driver.close()
