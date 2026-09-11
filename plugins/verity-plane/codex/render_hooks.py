"""Generate native inline commands; the source text is never executed as a file."""
import argparse
import json
from pathlib import Path


def definitions(root):
    source = (root / "native-guard.txt").read_text(encoding="utf8")
    return {"hooks": {event: [{**({"matcher": "startup|resume|clear|compact"} if event == "SessionStart" else {}),
                               "hooks": [{"type": "command", "command": source.replace("__EVENT__", event),
                                          "timeout": 30, "async": False}]}]
                      for event in ("SessionStart", "PreToolUse")}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    target = root / "hooks/hooks.json"
    raw = json.dumps(definitions(root), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if target.read_text(encoding="utf8") != raw:
            raise SystemExit("hooks differ from their native inline source")
    else:
        target.parent.mkdir(exist_ok=True)
        target.write_text(raw, encoding="utf8", newline="\n")
