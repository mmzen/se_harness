"""One process launcher for the package (SPEC-ECP-023 ECP-PRM-001 to ECP-PRM-003).

Every subprocess the package or the repository tools start goes through `run`,
and every Git command through `run_git`. Both close standard input, capture both
streams as bytes, bound the run by a timeout and the captured output by a byte
cap, and turn a start failure or a timeout into the caller's own exception
class, passed as `error=`, so each caller keeps the refusal type its contract
names. Return codes are the caller's to read: a non-zero exit is not an error
here, because several callers read exit 1 as an answer.
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

#: The default bound on one launch; a caller may raise it, never remove it.
DEFAULT_TIMEOUT_SECONDS = 60
#: The default cap on each captured stream.
DEFAULT_OUTPUT_CAP_BYTES = 8 * 1024 * 1024

ErrorFactory = Callable[[str], BaseException]


class ProcessError(RuntimeError):
    """The launcher's own refusal when a caller names no error class."""


def run(
    argv: Sequence[str],
    *,
    cwd: Path | str | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    stdin: bytes | None = None,
    output_cap: int = DEFAULT_OUTPUT_CAP_BYTES,
    error: ErrorFactory = ProcessError,
    capture: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    """Run `argv` bounded by `timeout` and `output_cap`, standard input closed unless `stdin` is given.

    A start failure (`OSError`) or any `SubprocessError`, the timeout included,
    raises `error(message)` with the command named; an over-cap stream does the
    same. With `capture=False` both streams are inherited, for the one engine
    launch a user watches, and no cap applies. The completed process is
    returned whatever its exit status.
    """

    command = [str(item) for item in argv]
    name = command[0] if command else "<empty command>"
    try:
        completed = subprocess.run(  # noqa: S603 - fixed argument vector, shell=False
            command,
            cwd=None if cwd is None else str(cwd),
            env=None if env is None else dict(env),
            input=stdin,
            stdin=subprocess.DEVNULL if stdin is None else None,
            capture_output=capture,
            check=False,
            shell=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise error(f"{name} did not finish within {timeout} seconds") from exc
    except (OSError, subprocess.SubprocessError) as exc:
        raise error(f"{name} could not run: {exc}") from exc
    if capture and (len(completed.stdout) > output_cap or len(completed.stderr) > output_cap):
        raise error(f"{name} output exceeds {output_cap} bytes")
    return completed


def run_git(
    root: Path | str,
    *arguments: str,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    stdin: bytes | None = None,
    output_cap: int = DEFAULT_OUTPUT_CAP_BYTES,
    env: Mapping[str, str] | None = None,
    error: ErrorFactory = ProcessError,
) -> subprocess.CompletedProcess[bytes]:
    """Run `git -C root *arguments` through `run`; a missing `git` executable is the caller's error too."""

    executable = shutil.which("git")
    if executable is None:
        raise error("git executable is unavailable: none on PATH")
    return run(
        [executable, "-C", str(root), *arguments],
        timeout=timeout, stdin=stdin, output_cap=output_cap, env=env, error=error,
    )


def text(data: bytes | str | None) -> str:
    """Decode a captured stream as UTF-8, replacing what is not, so no launch depends on the locale."""

    if data is None:
        return ""
    if isinstance(data, str):
        return data
    return data.decode("utf-8", "replace")


def first_line(data: bytes) -> str:
    """The first non-empty line of a captured stream, decoded, or an empty string."""

    for line in text(data).splitlines():
        if line.strip():
            return line.strip()
    return ""
