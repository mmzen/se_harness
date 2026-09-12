"""Run the real handler, replacing only its final evaluator command for C03."""
import importlib.util
from pathlib import Path
import sys

script, mode, folder = sys.argv[1:4]
spec = importlib.util.spec_from_file_location("fault_injected_tool_handler", script)
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)
original = handler.Deadline.run


def inject(self, argv, cwd, environment):
    if "check" in argv:
        fault = [argv[0], "-I", "-B", str(Path(__file__).with_name("fault_worker.py")), mode, folder]
        try:
            return original(self, fault, cwd, environment)
        finally:
            if self.records:
                self.records[-1]["fault_replaced_argv"] = argv
    return original(self, argv, cwd, environment)


handler.Deadline.run = inject
sys.argv = [script, *sys.argv[4:]]
raise SystemExit(handler.main())
