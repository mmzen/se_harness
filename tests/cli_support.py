"""One entry to the `harnessctl` command line for tests (SPEC-TST-002 TST-HYG-004).

Every in-process command-line call in the suite goes through `invoke`, so a
refusal by the argument parser is observed as its exit code rather than as a
`SystemExit` escaping the test.
"""

from __future__ import annotations

import contextlib
import io

from se_harness.cli import main


def exit_code(raised: SystemExit) -> int:
    """The process exit code a `SystemExit` carries, as the interpreter would report it."""
    if raised.code is None:
        return 0
    if isinstance(raised.code, int):
        return raised.code
    return 1


def invoke(*arguments: str) -> tuple[int, str, str]:
    """Run `harnessctl` in this process and return its exit code, stdout and stderr."""
    output, error = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
        try:
            code = main(list(arguments))
        except SystemExit as raised:
            code = exit_code(raised)
    return code, output.getvalue(), error.getvalue()
