"""One TOML front-matter parser for the package (SPEC-ECP-023 ECP-PRM-004, ECP-PRM-005).

A formal artifact opens with a line that is exactly `+++`, carries TOML until the
next such line, and continues with its Markdown body. This module is the only
place that finds those two delimiters: it tolerates a UTF-8 BOM, reads CR, CRLF
and LF line endings alike, anchors both delimiters at the start of a line, and
hands back the metadata and the body. Callers that write artifacts back keep the
document's newline convention and BOM through `split_document`.
"""

from __future__ import annotations

import re

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DELIMITER = "+++"


class FrontMatterError(ValueError):
    """The document has no well-formed front matter."""


@dataclass(frozen=True)
class Document:
    """A split artifact: the front-matter lines, the body, and how to write it back unchanged."""

    front_lines: tuple[str, ...]
    body: str
    newline: str
    opening: str

    @property
    def toml_text(self) -> str:
        return "\n".join(self.front_lines)


def _decode(data: bytes | str) -> str:
    if isinstance(data, str):
        return data[1:] if data.startswith("﻿") else data
    return data.decode("utf-8-sig")


def front_matter_lines(text_or_bytes: bytes | str) -> tuple[list[str], bool] | None:
    """The lines between the two delimiters and whether the closing one was found.

    Returns `None` when the document does not open with the delimiter. Line
    endings are normalized, so a CRLF or CR document reads as its LF form.
    """

    text = _decode(text_or_bytes)
    lines = text.splitlines()
    if not lines or lines[0].rstrip() != DELIMITER:
        return None
    for index in range(1, len(lines)):
        if lines[index].rstrip() == DELIMITER:
            return lines[1:index], True
    return lines[1:], False


def parse_text(toml_lines: list[str] | tuple[str, ...]) -> dict[str, Any]:
    """The TOML table of the front-matter lines; a non-table or invalid TOML is a `FrontMatterError`."""

    try:
        value = tomllib.loads("\n".join(toml_lines))
    except tomllib.TOMLDecodeError as exc:
        raise FrontMatterError(f"front matter is not valid TOML: {exc}") from exc
    if not isinstance(value, dict):
        raise FrontMatterError("front matter is not a TOML table")
    return value


def parse(data: bytes | str) -> dict[str, Any]:
    """The metadata of a document, or a `FrontMatterError` naming what is missing."""

    found = front_matter_lines(data)
    if found is None:
        raise FrontMatterError("document has no TOML front matter")
    lines, terminated = found
    if not terminated:
        raise FrontMatterError("front matter is unterminated")
    return parse_text(lines)


def read(path: Path) -> dict[str, Any]:
    """The metadata of the artifact at `path`; reading, decoding and shape failures are `FrontMatterError`."""

    try:
        data = path.read_bytes()
    except OSError as exc:
        raise FrontMatterError(f"cannot read {path.name}: {exc}") from exc
    try:
        return parse(data)
    except UnicodeError as exc:
        raise FrontMatterError(f"{path.name} is not valid UTF-8: {exc}") from exc


def read_or_none(path: Path) -> dict[str, Any] | None:
    """The metadata of the artifact at `path`, or `None` on any failure, for callers that only look."""

    try:
        return read(path)
    except FrontMatterError:
        return None


def partition(text: str) -> tuple[str, str] | None:
    """(front matter text, body) of an already decoded and newline-normalized document, or `None`."""

    found = front_matter_lines(text)
    if found is None:
        return None
    lines, terminated = found
    if not terminated:
        return None
    body = "\n".join(text.replace("\r\n", "\n").replace("\r", "\n").split("\n")[len(lines) + 2 :])
    return "\n".join(lines), body


def split_document(data: bytes, *, error: type[Exception] = FrontMatterError) -> Document:
    """Split an artifact for rewriting: front lines, body with its endings, the newline and the opening line.

    The body keeps its original line endings so an edit of the front matter
    writes every other byte back unchanged; `opening` carries the BOM when the
    document had one.
    """

    try:
        text = data.decode("utf-8-sig")
    except UnicodeError as exc:
        raise error(f"formal artifact is not valid UTF-8: {exc}") from exc
    lines = text.splitlines(keepends=True)
    clean = [line.rstrip("\r\n") for line in lines]
    if not clean or clean[0].rstrip() != DELIMITER:
        raise error("formal artifact has no TOML front matter")
    closing = next((index for index in range(1, len(clean)) if clean[index].rstrip() == DELIMITER), None)
    if closing is None:
        raise error("formal artifact has no closing front-matter delimiter")
    opening_ending = lines[0][len(clean[0]) :]
    newline = opening_ending or ("\r\n" if "\r\n" in text else "\n")
    body = "".join(lines[closing + 1 :])
    bom = "﻿" if data.startswith(b"\xef\xbb\xbf") else ""
    return Document(tuple(clean[1:closing]), body, newline, bom + DELIMITER + newline)


_FENCE = re.compile(r"```.*?```", re.S)


def body_sections(body: str) -> dict[str, str]:
    """Second-level headings to their text, fenced code removed (ECP-ENG-008: the one body parser)."""

    sections: dict[str, str] = {}
    current = ""
    for line in _FENCE.sub(" ", body.replace("\r\n", "\n")).split("\n"):
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, "")
        elif current:
            sections[current] += line + "\n"
    return sections
