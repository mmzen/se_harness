"""Bounded metadata-only comparison inputs; never read credential contents."""
from pathlib import Path
import os
import stat


def snapshot(root):
    root = Path(root).resolve()
    paths = {root / name for name in ('config.toml', 'auth.json', 'credentials.json', 'plugins.json')}
    plugins = root / 'plugins'
    errors = []

    def directories(path):
        try:
            with os.scandir(path) as entries:
                found = []
                for number, entry in enumerate(entries):
                    if number >= 4096:
                        errors.append({'path': str(path), 'error': 'Bounded directory limit reached'})
                        break
                    try:
                        if stat.S_ISDIR(entry.stat(follow_symlinks=False).st_mode):
                            found.append(Path(entry.path))
                    except OSError as error:
                        errors.append({'path': entry.path, 'error': type(error).__name__})
                return found
        except FileNotFoundError:
            return []
        except OSError as error:
            errors.append({'path': str(path), 'error': type(error).__name__})
            return []

    for provider in directories(plugins / 'cache'):
        for plugin in directories(provider):
            for version in directories(plugin):
                paths.add(version / '.codex-plugin/plugin.json')
    for marketplace in directories(plugins / 'marketplaces'):
        paths.add(marketplace / '.plugin/marketplace.json')
    paths.update(plugins / name for name in ('installed_plugins.json', 'config.json', 'marketplaces.json'))
    files = {}
    for path in sorted(paths):
        key = path.relative_to(root).as_posix()
        try:
            metadata = path.stat()
            files[key] = {'exists': True, 'bytes': metadata.st_size, 'mtime_ns': metadata.st_mtime_ns}
        except FileNotFoundError:
            files[key] = {'exists': False, 'absence_confirmed': True}
        except OSError as error:
            files[key] = {'exists': None, 'error': type(error).__name__}
            errors.append({'path': str(path), 'error': type(error).__name__})
    return {'root': str(root), 'files': files,
            'errors': errors,
            'scope': 'Named config/auth inputs and installed plugin manifest metadata only. No file contents, credential hashes, session databases, or complete OS audit.'}
