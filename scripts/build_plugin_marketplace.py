#!/usr/bin/env python3
"""Compose or check a marketplace around the existing exact-source native packages."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from repository_tools import plugin_distribution as pkg

CATALOGS = {"codex": ".agents/plugins/marketplace.json", "claude": ".claude-plugin/marketplace.json"}
ASSETS = {path: "release/plugin-marketplace/" + path for path in (
    *CATALOGS.values(), "README.md", "submissions/README.md", "submissions/reviewer-test-cases.md")}
ASSETS.update({"LICENSE": "LICENSE", "submissions/verity-plane-logo.png": "docs/images/verity-plane-logo.png"})
IDENTITY = "PACKAGE-IDENTITY.json"
SKILLS = ("setup", "change", "evidence", "harness-orient", "harness-operator-brief")


def prepare_assets(repository, assembly):
    """Read fixed assets from the native assembly's commit before writing output."""
    assets = {target: pkg._blob(repository, assembly.source["revision"], source)[0]
              for target, source in ASSETS.items()}
    versions = set()
    for host, path in CATALOGS.items():
        catalog = pkg._json(assets[path])
        entries = catalog.get("plugins")
        if catalog.get("name") != "se-harness" or not isinstance(entries, list) or len(entries) != 1:
            raise pkg.AssemblyError(f"invalid single-plugin marketplace: {path}")
        entry = entries[0]
        expected = f"./packages/{host}/{assembly.name}"
        source = {"source": "local", "path": expected} if host == "codex" else expected
        if not isinstance(entry, dict) or entry.get("name") != assembly.name or entry.get("source") != source:
            raise pkg.AssemblyError(f"catalog must select complete package {expected}: {path}")
        required = {pkg.HOSTS[host], "LICENSE", "scripts/setup.py", *(f"skills/{skill}/SKILL.md" for skill in SKILLS)}
        missing = required - assembly.files[host].keys()
        if missing or any(not assembly.files[host][name][0].strip() for name in required):
            raise pkg.AssemblyError(f"incomplete {host} plugin: {sorted(missing)}")
        version = pkg._json(assembly.files[host][pkg.HOSTS[host]][0]).get("version")
        if not isinstance(version, str) or not version:
            raise pkg.AssemblyError(f"missing {host} plugin version")
        versions.add(version)
    if len(versions) != 1:
        raise pkg.AssemblyError("native plugin versions disagree")
    return assets, versions.pop()


def identity(assembly, assets, version, native):
    hashes = {path: pkg.digest(raw) for path, raw in assets.items()}
    for host, files in assembly.files.items():
        prefix = f"packages/{host}/{assembly.name}/"
        hashes.update({prefix + path: pkg.digest(raw) for path, (raw, _mode, _origin) in files.items()})
        hashes[prefix + pkg.INVENTORY] = pkg.digest(pkg.json_bytes(assembly.inventory(host)))
    hashes.update({"packages/" + path: value for path, value in native["archives"].items()})
    return pkg.json_bytes({"name": assembly.name, "plugin_version": version, "marketplace": "se-harness",
                           "source": assembly.source, "evaluator": assembly.evaluator,
                           "files": dict(sorted(hashes.items())),
                           "claim": "Checked distribution contents; no owner or provider publication decision."})


def check_wrapper(output, expected):
    """Native acceptance owns packages/; check the remaining fixed files here."""
    directories = {"packages"} | {str(parent).replace(os.sep, "/") for name in expected
                                    for parent in Path(name).parents if str(parent) != "."}
    actual = set()
    for directory, dirs, names in os.walk(output, followlinks=False):
        for name in dirs + names:
            path = Path(directory) / name
            pkg._safe_directory(path)
            relative = path.relative_to(output).as_posix()
            if path.is_dir():
                if relative not in directories:
                    raise pkg.AssemblyError(f"unexpected marketplace directory: {relative}")
            elif path.is_file():
                if path.stat().st_nlink != 1:
                    raise pkg.AssemblyError(f"hard-linked marketplace file: {relative}")
                actual.add(relative)
            else:
                raise pkg.AssemblyError(f"non-regular marketplace path: {relative}")
        if Path(directory) == output and "packages" in dirs:
            dirs.remove("packages")
    if actual != expected.keys():
        raise pkg.AssemblyError(f"missing or unexpected marketplace files: {sorted(actual ^ expected.keys())}")
    for name, raw in expected.items():
        path = output / name
        if path.stat().st_size != len(raw) or path.read_bytes() != raw:
            raise pkg.AssemblyError(f"marketplace differs from committed inputs: {name}")


def compose(repository, assembly, output, *, check=False):
    repository = repository.resolve(strict=True)
    output = output.absolute()
    pkg._safe_directory(output)
    output = output.resolve()
    if output == repository or output.is_relative_to(repository) or repository.is_relative_to(output):
        raise pkg.AssemblyError("choose a marketplace output outside the source repository")
    assets, version = prepare_assets(repository, assembly)
    if check:
        native = pkg.accept(assembly, output / "packages")
    else:
        if output.exists():
            raise pkg.AssemblyError("marketplace output already exists; inspect it or use a fresh directory")
        output.mkdir(parents=True)
        native = pkg.build(assembly, output / "packages")
        for path, raw in assets.items():
            pkg._write(output / path, raw)
        pkg._write(output / IDENTITY, identity(assembly, assets, version, native))
    expected = {**assets, IDENTITY: identity(assembly, assets, version, native)}
    check_wrapper(output, expected)
    return {"accepted": True, "source": assembly.source, "evaluator": assembly.evaluator,
            "plugin_version": version, "identity_sha256": pkg.digest(expected[IDENTITY]),
            "archives": native["archives"], "claim": "Contents only; native host testing and publication remain separate."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "check"))
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--revision", required=True)
    parser.add_argument("--plan", default="release/plugin-assembly.json")
    parser.add_argument("--release-revision", required=True)
    parser.add_argument("--release-record", required=True)
    parser.add_argument("--expected-wheel-sha256", required=True)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--evaluator-python", required=True, type=Path)
    parser.add_argument("--output-directory", required=True, type=Path)
    args = parser.parse_args()
    try:
        assembly = pkg.prepare(args.repository, args.revision, args.plan, args.release_revision,
                               args.release_record, args.expected_wheel_sha256, args.wheel, args.evaluator_python)
        result = compose(args.repository, assembly, args.output_directory, check=args.action == "check")
    except (pkg.AssemblyError, OSError, ValueError, KeyError, zipfile.BadZipFile, subprocess.SubprocessError) as exc:
        print(json.dumps({"accepted": False, "error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
