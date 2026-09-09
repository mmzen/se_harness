"""Bounded metadata-only comparison inputs; never read credential contents."""
from pathlib import Path


def snapshot(root):
    root = Path(root).resolve()
    paths = {root / name for name in ('config.toml', 'auth.json', 'credentials.json', 'plugins.json')}
    plugins = root / 'plugins'
    if plugins.exists():
        paths.update(plugins.glob('cache/*/*/*/.codex-plugin/plugin.json'))
        paths.update(plugins.glob('marketplaces/*/.plugin/marketplace.json'))
        paths.update(plugins / name for name in ('installed_plugins.json', 'config.json', 'marketplaces.json'))
    files = {}
    for path in sorted(paths):
        if path.is_file():
            stat = path.stat()
            files[path.relative_to(root).as_posix()] = {'exists': True, 'bytes': stat.st_size, 'mtime_ns': stat.st_mtime_ns}
        else:
            files[path.relative_to(root).as_posix()] = {'exists': False}
    return {'root': str(root), 'files': files,
            'scope': 'Named config/auth inputs and installed plugin manifest metadata only. No file contents, credential hashes, session databases, or complete OS audit.'}
