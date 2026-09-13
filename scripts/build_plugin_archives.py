#!/usr/bin/env python3
"""Build or independently recheck Codex/Claude archives from an exact Git plan."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from repository_tools.plugin_distribution import AssemblyError, accept, build, develop, prepare


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("develop", "build", "check"))
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--revision", help="full committed source ID (release build/check)")
    parser.add_argument("--plan", help="committed repository-relative assembly plan (release build/check)")
    parser.add_argument("--release-revision", help="trusted full commit containing the released record")
    parser.add_argument("--release-record", help="repository-relative released RLS record")
    parser.add_argument("--expected-wheel-sha256", help="independently obtained published archive SHA-256")
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--evaluator-python", type=Path, help="absolute external released-evaluator Python (release build/check)")
    parser.add_argument("--output-directory", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.action == "develop":
            result = develop(args.repository, args.wheel, args.output_directory)
        else:
            required = ('revision', 'plan', 'release_revision', 'release_record', 'expected_wheel_sha256', 'evaluator_python')
            missing = [name for name in required if getattr(args, name) is None]
            if missing:
                raise AssemblyError('release build/check requires ' + ', '.join('--' + name.replace('_', '-') for name in missing))
            assembly = prepare(args.repository, args.revision, args.plan, args.release_revision,
                               args.release_record, args.expected_wheel_sha256, args.wheel, args.evaluator_python)
            result = (build if args.action == "build" else accept)(assembly, args.output_directory.absolute())
    except (AssemblyError, OSError, ValueError, KeyError, zipfile.BadZipFile, subprocess.SubprocessError) as exc:
        print(json.dumps({"accepted": False, "error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
