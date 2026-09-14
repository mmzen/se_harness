# Private-helper rename example

Run this one-off example from the candidate checkout. It copies one module to a temporary folder, renames private helpers, then runs three existing behavior tests unchanged. It changes no repository file and is not an additional permanent test gate.

```python
from pathlib import Path
REPO = Path.cwd()  # Run from the source checkout.
import importlib.util, sys, tempfile, unittest
sys.path.insert(0,str(REPO))
import tests.test_interpreter_safety as cases
source=(REPO/'se_harness/interpreter_safety.py').read_text(encoding='utf-8')
with tempfile.TemporaryDirectory() as directory:
    target=__import__('pathlib').Path(directory)/'renamed.py'
    assert '_lexical' in source
    target.write_text(source.replace('_lexical','_normalized_input'),encoding='utf-8')
    spec=importlib.util.spec_from_file_location('kiss_refactor_example',target)
    module=importlib.util.module_from_spec(spec); sys.modules[spec.name]=module; spec.loader.exec_module(module)
    cases.interpreter_safety=module
    suite=unittest.TestSuite(cases.InterpreterPathsTests(name) for name in (
        'test_linked_environment_retains_its_entry_point',
        'test_missing_directory_and_checkout_interpreters_fail',
        'test_unavailable_path_resolution_reports_one_clear_failure'))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
```

Observed result on Windows, Python 3.14:

```text
test_linked_environment_retains_its_entry_point (tests.test_interpreter_safety.InterpreterPathsTests.test_linked_environment_retains_its_entry_point) ... ok
test_missing_directory_and_checkout_interpreters_fail (tests.test_interpreter_safety.InterpreterPathsTests.test_missing_directory_and_checkout_interpreters_fail) ... ok
test_unavailable_path_resolution_reports_one_clear_failure (tests.test_interpreter_safety.InterpreterPathsTests.test_unavailable_path_resolution_reports_one_clear_failure) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.049s

OK
```
