from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from static_profile_inventory import snapshot


class StaticMetadataTests(unittest.TestCase):
    def test_named_metadata_only_never_reads_contents_or_session_records(self):
        with tempfile.TemporaryDirectory(prefix='codex-static-metadata-') as folder:
            root = Path(folder)
            (root / 'auth.json').write_bytes(b'synthetic credential fixture; must never be read')
            (root / 'session.sqlite').write_bytes(b'unrelated mutable session')
            manifest = root / 'plugins/cache/test/plugin/1/.codex-plugin/plugin.json'
            manifest.parent.mkdir(parents=True)
            manifest.write_bytes(b'{}')
            with patch.object(Path, 'read_bytes', side_effect=AssertionError('contents read')), patch.object(Path, 'read_text', side_effect=AssertionError('contents read')):
                observed = snapshot(root)
            self.assertTrue(observed['files']['auth.json']['exists'])
            self.assertEqual(observed['files']['plugins/cache/test/plugin/1/.codex-plugin/plugin.json']['bytes'], 2)
            self.assertNotIn('session.sqlite', observed['files'])
            self.assertEqual(observed['files']['config.toml'], {'exists': False})


if __name__ == '__main__':
    unittest.main()
