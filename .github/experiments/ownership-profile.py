"""Disposable profiler wrapper; runs one unchanged source acceptance method."""
import cProfile
import ctypes
import datetime
import importlib.util
import json
import os
import pathlib
import pstats
import sys
import threading
import time
import unittest

source, output = map(pathlib.Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(source))
os.environ['SE_HARNESS_OWNERSHIP_PACKAGE'] = '0'
os.environ['SE_HARNESS_OWNERSHIP_EVIDENCE'] = str(output / 'cases')
path = source / 'tests/test_skill_ownership.py'
spec = importlib.util.spec_from_file_location('ownership_acceptance', path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
name = 'test_own10_killed_process_recovers_each_durable_boundary'
case = module.SkillOwnershipAcceptanceTests(name)
suite = unittest.TestSuite([case])
class MemoryStatus(ctypes.Structure):
    _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [(name, ctypes.c_ulonglong) for name in
        ('total_physical', 'available_physical', 'commit_limit', 'available_commit', 'total_virtual', 'available_virtual', 'extended')]
memory_samples = []
done = threading.Event()
def sample_memory():
    while not done.is_set():
        status = MemoryStatus()
        status.length = ctypes.sizeof(status)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            memory_samples.append({'available_physical': status.available_physical, 'load_percent': status.load,
                                   'commit_limit': status.commit_limit, 'available_commit': status.available_commit})
        done.wait(1)
sampler = threading.Thread(target=sample_memory, daemon=True)
sampler.start()
utc = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
facts = dict(pid=os.getpid(), thread_id=threading.get_native_id(), start_utc=utc(),
             python=sys.executable, source=str(source), temp=os.environ['TEMP'],
             candidate=os.environ['RAMDISK_TESTED_COMMIT'], method=name)
started, cpu = time.perf_counter(), time.process_time()
profile = cProfile.Profile()
profile.enable()
try:
    result = unittest.TextTestRunner(verbosity=2).run(suite)
finally:
    profile.disable()
    facts.update(end_utc=utc(), elapsed_seconds=time.perf_counter()-started,
                 parent_cpu_seconds=time.process_time()-cpu)
    profile.dump_stats(str(output / 'parent.pstats'))
    done.set()
    sampler.join()
facts.update(passed=result.wasSuccessful(), tests=result.testsRun,
             failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
             killed_workers=sum(e.get('operation') == 'killed-independent-process' for e in case.events))
facts['memory_samples'] = len(memory_samples)
facts['minimum_available_physical_bytes'] = min((m['available_physical'] for m in memory_samples), default=None)
facts['maximum_memory_load_percent'] = max((m['load_percent'] for m in memory_samples), default=None)
(output / 'window.json').write_text(json.dumps(facts), encoding='utf-8')
print('TRACE_WINDOW ' + json.dumps(facts), flush=True)
stats = pstats.Stats(profile)
rows = []
for (filename, line, function), (primitive, calls, own, cumulative, callers) in stats.stats.items():
    rows.append(dict(file=filename, line=line, function=function, calls=calls,
                     own_seconds=own, cumulative_seconds=cumulative))
for kind, field in [('SELF', 'own_seconds'), ('CUMULATIVE', 'cumulative_seconds')]:
    print('PYTHON_PROFILE_' + kind + ' ' + json.dumps(sorted(rows, key=lambda r:r[field], reverse=True)[:35]))
sys.exit(0 if result.wasSuccessful() and result.testsRun == 1 and not result.skipped else 1)
