from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import os
from pathlib import Path, PurePosixPath
import sys
import tarfile
import tempfile
from typing import Sequence


MAX_GZIP_EPOCH = (1 << 32) - 1


class NormalizationError(ValueError):
    """Raised when an sdist cannot be normalized safely."""


def parse_epoch(value: str) -> int:
    try:
        epoch = int(value, 10)
    except ValueError as error:
        raise argparse.ArgumentTypeError("epoch must be an integer") from error
    if not 0 <= epoch <= MAX_GZIP_EPOCH:
        raise argparse.ArgumentTypeError(
            f"epoch must be between 0 and {MAX_GZIP_EPOCH}"
        )
    return epoch


def canonical_member_name(member: tarfile.TarInfo) -> str:
    name = member.name
    if not name or "\x00" in name or "\\" in name:
        raise NormalizationError(f"unsafe archive member path: {name!r}")

    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts:
        raise NormalizationError(f"unsafe archive member path: {name!r}")
    if path.parts and len(path.parts[0]) == 2 and path.parts[0][1] == ":":
        raise NormalizationError(f"unsafe archive member path: {name!r}")

    canonical = path.as_posix()
    if canonical in {"", "."} or name.rstrip("/") != canonical:
        raise NormalizationError(f"non-canonical archive member path: {name!r}")
    return canonical


def validated_members(
    source: tarfile.TarFile,
) -> list[tuple[str, tarfile.TarInfo]]:
    members: list[tuple[str, tarfile.TarInfo]] = []
    names: set[str] = set()
    for member in source.getmembers():
        name = canonical_member_name(member)
        if name in names:
            raise NormalizationError(f"duplicate archive member path: {name}")
        if not (member.isfile() or member.isdir()):
            raise NormalizationError(
                f"unsupported archive member type for deterministic sdist: {name}"
            )
        names.add(name)
        members.append((name, member))
    if not members:
        raise NormalizationError("source distribution is empty")
    return sorted(members, key=lambda item: item[0])


def normalized_member(
    member: tarfile.TarInfo,
    *,
    name: str,
    epoch: int,
) -> tarfile.TarInfo:
    normalized = copy.copy(member)
    normalized.name = name
    normalized.mtime = epoch
    normalized.uid = 0
    normalized.gid = 0
    normalized.uname = ""
    normalized.gname = ""
    normalized.pax_headers = {}
    normalized.linkname = ""
    normalized.devmajor = 0
    normalized.devminor = 0
    return normalized


def normalize_sdist(source_path: Path, output_path: Path, *, epoch: int) -> str:
    source = source_path.resolve(strict=True)
    if source_path.is_symlink() or not source.is_file():
        raise NormalizationError("input must be an ordinary source-distribution file")

    output_parent = output_path.parent.resolve(strict=True)
    output = output_parent / output_path.name
    if output.exists() or output.is_symlink():
        raise NormalizationError(f"output already exists: {output}")
    if source == output:
        raise NormalizationError("input and output must be different paths")

    temporary: Path | None = None
    try:
        with tarfile.open(source, mode="r:gz") as source_archive:
            members = validated_members(source_archive)
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{output.name}.",
                suffix=".tmp",
                dir=output_parent,
            )
            temporary = Path(temporary_name)
            with os.fdopen(descriptor, "wb") as raw_output:
                with gzip.GzipFile(
                    filename="",
                    mode="wb",
                    compresslevel=9,
                    fileobj=raw_output,
                    mtime=epoch,
                ) as compressed_output:
                    with tarfile.open(
                        fileobj=compressed_output,
                        mode="w",
                        format=tarfile.PAX_FORMAT,
                    ) as output_archive:
                        for name, member in members:
                            payload = (
                                source_archive.extractfile(member)
                                if member.isfile()
                                else None
                            )
                            try:
                                output_archive.addfile(
                                    normalized_member(member, name=name, epoch=epoch),
                                    payload,
                                )
                            finally:
                                if payload is not None:
                                    payload.close()
                raw_output.flush()
                os.fsync(raw_output.fileno())

        try:
            os.link(temporary, output)
        except FileExistsError as error:
            raise NormalizationError(f"output already exists: {output}") from error
        return hashlib.sha256(output.read_bytes()).hexdigest()
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create a deterministic .tar.gz sdist by preserving member payloads and "
            "normalizing archive order, ownership, timestamps, and gzip metadata."
        )
    )
    parser.add_argument("input", type=Path, help="raw .tar.gz source distribution")
    parser.add_argument("output", type=Path, help="new normalized .tar.gz output")
    parser.add_argument(
        "--epoch",
        required=True,
        type=parse_epoch,
        help="explicit Unix timestamp used for every tar member and the gzip header",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        checksum = normalize_sdist(
            arguments.input,
            arguments.output,
            epoch=arguments.epoch,
        )
    except (NormalizationError, FileNotFoundError, tarfile.TarError, OSError) as error:
        print(f"normalize-sdist: {error}", file=sys.stderr)
        return 2
    print(f"normalized sdist: {arguments.output}")
    print(f"sha256: {checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
