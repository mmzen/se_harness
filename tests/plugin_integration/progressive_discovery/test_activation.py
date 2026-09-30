"""Selection boundary tests; native delivery is assessed separately."""
import json
import os
from pathlib import Path
from unittest.mock import patch

import unittest
from tests.plugin_integration.progressive_discovery import test_delivery as fixtures
delivery = fixtures.delivery
import activate
import harness_runtime as runtime


class SessionActivationTests(unittest.TestCase):
    setUp = fixtures.InstructionDeliveryTests.setUp
    fixture = fixtures.InstructionDeliveryTests.fixture
    event = fixtures.InstructionDeliveryTests.event
    context = fixtures.InstructionDeliveryTests.context

    def test_clone_after_startup_activation_and_parent_compaction(self):
        event = {**self.event(), 'cwd':str(self.base)}
        self.assertIn('# Select the working repository', self.context(event))
        before = {p.name:p.read_bytes() for p in self.repo.iterdir()}
        immediate = activate.activate('codex','fixture-session',self.data,self.repo)
        self.assertIn('A complete root.', immediate)
        for source in ('compact','resume'):
            restored = self.context({**event,'source':source})
            self.assertIn(str(self.repo), restored)
            self.assertIn('A complete root.', restored)
        self.assertEqual(before, {p.name:p.read_bytes() for p in self.repo.iterdir()})

    def test_parallel_sessions_switch_clear_and_plugin_data_survive(self):
        other = self.fixture('other','0.20.0','Other release.\n')
        activate.activate('codex','one',self.data,self.repo)
        activate.activate('codex','two',self.data,other)
        for session, text in [('one','A complete root.'),('two','Other release.')]:
            self.assertIn(text,self.context({**self.event('compact',self.base),'session_id':session}))
        activate.activate('codex','one',self.data,other)
        activate.activate('codex','one',self.data,None)
        self.assertIn('# Select the working repository',self.context({**self.event(repo=self.base),'session_id':'one'}))
        self.assertIn('Other release.',self.context({**self.event('compact',self.base),'session_id':'two'}))
        self.assertIn('# Select the working repository',self.context({**self.event(repo=self.base),'session_id':'new'}))

    def test_failed_activation_and_atomic_replace_keep_old_selection(self):
        activate.activate('codex','fixture-session',self.data,self.repo)
        record = runtime.session_file('codex','fixture-session',self.data)
        before = record.read_bytes()
        bad = self.fixture('bad','0.20.0','Wrong.\n')
        (bad/'ENGINEERING_HARNESS.md').write_text('tampered')
        with self.assertRaises(runtime.DeliveryError):
            activate.activate('codex','fixture-session',self.data,bad)
        self.assertEqual(before,record.read_bytes())
        other = self.fixture('other','0.20.0','Other.\n')
        with patch.object(runtime.os,'replace',side_effect=OSError('interrupted')):
            with self.assertRaises(OSError):activate.activate('codex','fixture-session',self.data,other)
        self.assertEqual(before,record.read_bytes())
        self.assertIn('A complete root.',self.context(self.event('compact',self.base)))

    def test_invalid_or_missing_saved_checkout_never_falls_back_to_cwd(self):
        activate.activate('codex','fixture-session',self.data,self.repo)
        record = runtime.session_file('codex','fixture-session',self.data)
        raw = record.read_bytes()
        record.write_text('{')
        self.assertIn('delivery is unavailable',self.context())
        record.write_bytes(raw)
        self.repo.rename(self.base/'gone')
        other = self.fixture('fallback','0.20.0','Must not borrow.\n')
        refused = self.context(self.event('compact',other))
        self.assertIn('delivery is unavailable',refused)
        self.assertNotIn('Must not borrow.',refused)

    def test_missing_identity_and_concurrent_switch_refuse(self):
        event=self.event(); event.pop('session_id')
        self.assertIn('host-supplied session_id',self.context(event))
        record=runtime.session_file('codex','fixture-session',self.data)
        with runtime.exclusive(record.with_suffix('.lock')):
            self.assertIn('being changed',self.context())
        with patch.object(delivery,'repository_context',side_effect=lambda *args: (runtime.atomic_json(record,{'changed':True}) or 'Mixed')):
            self.assertIn('changed during delivery',self.context())

    def test_private_data_cannot_live_in_repository(self):
        with self.assertRaisesRegex(runtime.DeliveryError,'outside the repository'):
            activate.activate('codex','fixture-session',self.repo/'private',self.repo)
        self.assertFalse((self.repo/'private').exists())
