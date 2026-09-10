"""One explicit fixture edit selected by the agent; no action routing."""
from pathlib import Path
import sys
repo=Path(sys.argv[1])
message=sys.argv[2]
(repo/'src/feature.py').write_text('def message():\n    return '+repr(message)+'\n',encoding='utf8')
