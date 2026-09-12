"""Regress false-positive acceptance using retained native captures, without a host."""
import copy
import json
from pathlib import Path
import unittest

import assess_capture as a

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-006/acceptance-04'


class CaptureAssessmentTests(unittest.TestCase):
    def case(self, name):
        folder = EVIDENCE / name
        return folder, json.loads((folder / 'commands.json').read_text(encoding='utf8')), json.loads((folder / 'observations.json').read_text(encoding='utf8'))

    def test_retained_checked_and_refused_write_correlate(self):
        folder, rows, original = self.case('C03')
        self.assertEqual(a.assess(folder, rows=rows, original=original)['conclusion'], 'pass')
        # A successful result cannot substitute for independently observed bytes.
        rows[0]['target_after'] = copy.deepcopy(rows[0]['target_before'])
        self.assertEqual(a.assess(folder, rows=rows, original=original)['conclusion'], 'fail')

    def test_debug_source_strings_do_not_prove_hook_receipt(self):
        folder, rows, original = self.case('C05')
        rows[1]['stdout'] = json.dumps({'type':'assistant','message':{'content':[{'type':'text','text':'UNREADY permissionDecision deny'}]}})
        rows[1]['stderr'] = 'source command includes UNREADY permissionDecision deny'
        self.assertEqual(a.assess(folder, rows=rows, original=original)['conclusion'], 'fail')

    def test_different_requested_target_cannot_substitute(self):
        folder, rows, original = self.case('C03')
        rows[1]['argv'][rows[1]['argv'].index('-p')+1] = rows[1]['argv'][rows[1]['argv'].index('-p')+1].replace('outside-scope.txt', 'another-target.txt')
        self.assertEqual(a.assess(folder, rows=rows, original=original)['conclusion'], 'fail')

    def test_active_child_invalidates_timely_denial(self):
        folder, rows, original = self.case('C09')
        self.assertEqual(a.assess(folder, rows=rows, original=original)['conclusion'], 'pass')
        original['observed']['faults'][2]['children_alive']['child'] = True
        self.assertEqual(a.assess(folder, rows=rows, original=original)['conclusion'], 'fail')

    def test_static_rejection_needs_actual_loaded_hook(self):
        folder, rows, original = self.case('C12')
        self.assertEqual(a.assess(folder, rows=rows, original=original)['conclusion'], 'pass')
        rows[1]['timeline'] = []
        self.assertEqual(a.assess(folder, rows=rows, original=original)['conclusion'], 'unavailable')

    def test_missing_refusal_retains_failed_enforcement(self):
        for name in ('C10', 'C11'):
            folder, rows, original = self.case(name)
            assessment = a.assess(folder, rows=rows, original=original)
            self.assertEqual(assessment['conclusion'], 'fail')
            self.assertFalse(assessment['qualification'])
            self.assertTrue(all(x['expected_target_effect'] for x in assessment['observations']))


if __name__ == '__main__':
    unittest.main()
