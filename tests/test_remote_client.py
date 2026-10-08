"""The remote transport preserves explicit requests and uncertain outcomes."""
import http.server
import base64
import copy
import hashlib
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from se_harness.remote import RemoteError, TransportUncertain, endpoint_url, send, strict_json, save_export


class RemoteClientTests(unittest.TestCase):
    def export_value(self, files=None):
        def encoded(raw):
            return {'content_base64': base64.b64encode(raw).decode(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        def digest(scheme, value):
            raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
            return hashlib.sha256(scheme.encode() + b'\n' + raw).hexdigest()
        snapshot = {'schema': 'se-harness-test-snapshot/v2', 'test_copy': True,
                    'files': {p: encoded(b) for p, b in (files or {'docs/test.md': b'Exact\r\nbytes\n'}).items()},
                    'git_bundle': encoded(b'bundle fixture bytes')}
        snapshot['snapshot_id'] = 'sha256:' + digest(snapshot['schema'], snapshot)
        manifest = {'provenance': {'snapshot_id': snapshot['snapshot_id']}}
        scheme = 'se-harness-artifact-baseline/v1'
        return {'schema': 'se-harness-lifecycle-export/v2', 'test_copy': True, 'snapshot': snapshot,
                'baseline': {'schema': scheme, 'manifest': manifest, 'baseline_id': scheme + ':sha256:' + digest(scheme, manifest)}}

    def test_export_preserves_bytes_and_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'new-export'
            result = save_export(self.export_value(), target)
            self.assertTrue(result['test_copy'])
            self.assertEqual('not yet performed', result['independent_replay'])
            self.assertEqual(b'Exact\r\nbytes\n', (target / 'files/docs/test.md').read_bytes())
            self.assertFalse((target / '.incomplete').exists())
            with self.assertRaisesRegex(RemoteError, 'EXPORT_EXISTS'):
                save_export(self.export_value(), target)

    def test_export_refuses_unsafe_ambiguous_and_corrupt_data_before_writing(self):
        for path in ('../escape', '/absolute', 'C:/escape', '.GIT/config', 'CON', 'docs/trailing.', 'docs/line\nbreak'):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as folder:
                target = Path(folder) / 'refused'
                with self.assertRaises(RemoteError):
                    save_export(self.export_value({path: b'bad'}), target)
                self.assertFalse(target.exists())
        value = self.export_value()
        value['snapshot']['files']['docs/test.md']['content_base64'] = base64.b64encode(b'corrupt').decode()
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'refused'
            with self.assertRaises(RemoteError):
                save_export(value, target)
            self.assertFalse(target.exists())
        for files in ({'a': b'1', 'A': b'2'}, {'a': b'1', 'a/b': b'2'}):
            with tempfile.TemporaryDirectory() as folder, self.assertRaises(RemoteError):
                save_export(self.export_value(files), Path(folder) / 'refused')

    def test_interrupted_export_keeps_an_incomplete_marker(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'partial'
            with mock.patch('pathlib.Path.write_bytes', side_effect=OSError('simulated write interruption')):
                with self.assertRaises(OSError):
                    save_export(self.export_value(), target)
            self.assertTrue((target / '.incomplete').is_file())

    def test_private_endpoint_and_no_embedded_credentials(self):
        self.assertEqual(endpoint_url("http://127.0.0.1:8080/"), "http://127.0.0.1:8080")
        for endpoint in ("https://example.com", "http://127.0.0.1@evil.test", "http://u:p@localhost", "file:///tmp/x", "http://localhost/?token=x"):
            with self.subTest(endpoint=endpoint), self.assertRaises(RemoteError):
                endpoint_url(endpoint)

    def test_ambiguous_requests_refuse_before_transport(self):
        for raw in ('{"version":1,"version":2}', '{"version":1.0}', '{"version":NaN}'):
            with self.subTest(raw=raw), self.assertRaises(RemoteError):
                strict_json(raw)

    def test_transport_preserves_receipt_and_never_retries(self):
        requests = []
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                requests.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
                body = b'{"outcome":"accepted","receipt_id":"fixed"}'
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            def do_GET(self):
                self.send_response(302)
                self.send_header("Location", "http://example.invalid/never-send-credentials")
                self.end_headers()
            def log_message(self, *args):
                pass
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            endpoint = "http://127.0.0.1:" + str(server.server_port)
            request = {"operation_key": "same-key", "expected_project_version": 4}
            status, result = send(endpoint, "synthetic-test-token", "POST", "/command", request)
            self.assertEqual((status, result["receipt_id"]), (200, "fixed"))
            self.assertEqual(requests, [request])
            with self.assertRaises(TransportUncertain) as caught:
                send(endpoint, "synthetic-test-token", "GET", "/redirect")
            self.assertNotIn("synthetic-test-token", str(caught.exception))
            self.assertEqual(len(requests), 1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


class AuthoringTests(unittest.TestCase):
    def setUp(self):
        from se_harness.cli import build_parser
        self.parser = build_parser()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.evaluator = {'version': '0.22.1', 'archive_sha256': 'a'*64, 'payload_sha256': 'b'*64}
        self.evaluator_file = self.root / 'evaluator.json'
        self.evaluator_file.write_text(json.dumps(self.evaluator))
        self.project = '12345678-1234-4234-8234-123456789abc'
        self.context = 'abcdef12-1234-4234-8234-123456789abc'
        self.baseline = 'se-harness-artifact-baseline/v1:sha256:' + 'd'*64
        self.revision = 'sha256:' + 'e'*64

    def args(self, op, *extra):
        return self.parser.parse_args(['remote', op, '--endpoint', 'http://127.0.0.1:1',
            '--token-env', 'HAG_TEST_TOKEN', '--project', self.project, *map(str, extra)])

    def test_typed_inputs_match_independent_wire_contracts(self):
        from se_harness.remote_authoring import typed_request
        source = {'schema': 'se-harness-source-manifest/v1', 'source': {'repository':'fixture', 'object_format':'sha1','commit':'f'*40},
                  'artifacts': [{'artifact_id':'INT-TST-001','path':'docs/intent.md','blob_oid':'a'*40,'raw_sha256':'b'*64,'bytes':16}]}
        manifest_file = self.root / 'manifest.json'
        manifest_file.write_text(json.dumps(source))
        document = self.root / 'document.md'
        raw = 'exact\r\nUTF-8 café\n'.encode()
        document.write_bytes(raw)
        common = ['--typed','--evaluator-file', self.evaluator_file, '--operation-key','chosen-key','--expected-project-version','4']
        cases = [
            ('import', ['--source-manifest', manifest_file], {'source_manifest':source}),
            ('draft-open', ['--baseline', self.baseline, '--work-order','WO-TST-001'], {'base_baseline_id':self.baseline,'work_order_id':'WO-TST-001'}),
            ('create-artifact', ['--context',self.context,'--context-version','2','--domain','example','--artifact-type','intent','--artifact','INT-TST-001'],
             {'context_id':self.context,'expected_context_version':2,'domain':'example','artifact_type':'intent','artifact_id':'INT-TST-001'}),
            ('revise-artifact',['--context',self.context,'--context-version','2','--artifact','INT-TST-001','--expected-revision',self.revision,'--document-file',document],
             {'context_id':self.context,'expected_context_version':2,'artifact_id':'INT-TST-001','expected_revision_id':self.revision,'document_base64':base64.b64encode(raw).decode()}),
        ]
        for op, extra, expected in cases:
            with self.subTest(op=op):
                self.assertEqual({'schema':'se-harness-remote-command/v1','operation':op,'project_id':self.project,
                    'operation_key':'chosen-key','expected_project_version':4,'expected_evaluator':self.evaluator, **expected}, typed_request(self.args(op,*common,*extra)))
        read = typed_request(self.args('read','--typed','--baseline',self.baseline,'--artifact','INT-TST-001','--expected-revision',self.revision))
        self.assertEqual({'schema':'se-harness-graph-read/v1','operation':'revision','project_id':self.project,
            'view':{'kind':'baseline','baseline_id':self.baseline},'artifact_id':'INT-TST-001','revision_id':self.revision,
            'budget':{'rows':1,'bytes':2097152,'depth':0}},read)

    def test_invalid_inputs_never_send(self):
        from se_harness.remote import run
        import contextlib, io
        document = self.root / 'document.md'
        document.write_bytes(b'x'*1048577)
        cases = [self.args('read','--typed','--request',document), self.args('read','--artifact','INT-TST-001'),
                 self.args('status','--compact'), self.args('status','--typed'),
                 self.args('revise-artifact','--typed','--document-file',document),
                 self.args('read','--typed','--baseline',self.baseline,'--context-version','1','--artifact','INT-TST-001','--expected-revision',self.revision)]
        for args in cases:
            with self.subTest(args=args), mock.patch.dict('os.environ',{'HAG_TEST_TOKEN':'synthetic-secret'}), mock.patch('se_harness.remote.send') as transport, contextlib.redirect_stderr(io.StringIO()) as output:
                self.assertEqual(2,run(args))
                transport.assert_not_called()
                self.assertEqual('not_sent',json.loads(output.getvalue())['outcome'])

    def test_capture_preserves_wire_bytes_document_and_omissions(self):
        from se_harness.remote_authoring import Capture
        raw = b'Exact\r\ndocument\n'
        value = {'outcome':'accepted','evaluator_output':{'incomplete':['large finding'*3000]},
                 'data':{'envelope':{'document_sha256':hashlib.sha256(raw).hexdigest()},'document_base64':base64.b64encode(raw).decode()}}
        capture = Capture(self.root/'new','synthetic-secret')
        capture.request('POST','/command',{'operation_key':'fixed'})
        wire = json.dumps(value,indent=3).encode()+b'\n'
        capture.response(200,wire)
        view = capture.compact(value)
        capture.finish(0,'accepted')
        self.assertEqual(wire,(capture.path/'1-response.json').read_bytes())
        self.assertEqual(raw,Path(view['documents'][0]['path']).read_bytes())
        self.assertEqual(raw.decode(),view['documents'][0]['text'])
        self.assertFalse(view['findings_complete'])
        self.assertTrue(any(x.get('required_reading') for x in view['omitted']))
        self.assertNotIn('document_base64', view['result']['data'])
        with self.assertRaises(RemoteError):
            Capture(capture.path,'synthetic-secret')

    def test_wire_version_bounds_and_work_order_type_refuse_before_sending(self):
        from se_harness.remote import run
        import contextlib, io
        for version, work_order in [('9223372036854775808','WO-TST-001'),('1','INT-TST-001')]:
            args=self.args('draft-open','--typed','--evaluator-file',self.evaluator_file,
                '--operation-key','chosen','--expected-project-version',version,
                '--baseline',self.baseline,'--work-order',work_order)
            with mock.patch.dict('os.environ',{'HAG_TEST_TOKEN':'synthetic-secret'}),mock.patch('se_harness.remote.send') as transport,contextlib.redirect_stderr(io.StringIO()) as output:
                self.assertEqual(2,run(args))
                self.assertEqual('not_sent',json.loads(output.getvalue())['outcome'])
                transport.assert_not_called()

    def test_unicode_result_survives_a_legacy_windows_console(self):
        from se_harness.remote import run
        import contextlib, io
        value={'message':'“Résumé” — 你好'}
        buffer=io.BytesIO();console=io.TextIOWrapper(buffer,encoding='cp1252')
        with mock.patch.dict('os.environ',{'HAG_TEST_TOKEN':'synthetic-secret'}),mock.patch('se_harness.remote.send',return_value=(200,value)),contextlib.redirect_stdout(console):
            self.assertEqual(0,run(self.args('status')))
        console.flush()
        self.assertEqual(value,json.loads(buffer.getvalue()))
        console.detach()

    def test_post_send_capture_failure_is_unknown_not_not_sent(self):
        from se_harness.remote import run
        import contextlib, io
        request = self.root/'request.json'
        request.write_text(json.dumps({'operation':'create-artifact','operation_key':'original','project_id':self.project}))
        def accepted(*args, **kwargs):
            kwargs['capture'].response(200,b'{"outcome":"accepted"}')
            return 200, {'outcome':'accepted'}
        with mock.patch.dict('os.environ',{'HAG_TEST_TOKEN':'synthetic-secret'}), mock.patch('se_harness.remote.installed_client',return_value={'version':'test'}), mock.patch('se_harness.remote.send',side_effect=accepted) as transport, mock.patch('se_harness.remote_authoring.Capture.finish',side_effect=OSError('disk full')), contextlib.redirect_stderr(io.StringIO()) as output:
            code=run(self.args('create-artifact','--request',request,'--client-wheel','fixture','--compact','--record-directory',self.root/'new'))
        result=json.loads(output.getvalue())
        self.assertEqual(2,code)
        self.assertEqual('unknown',result['outcome'])
        self.assertEqual('original',result['operation_key'])
        self.assertTrue(result['capture_incomplete'])
        self.assertEqual(1,transport.call_count)
        self.assertEqual(b'{"outcome":"accepted"}',(self.root/'new/1-response.json').read_bytes())

    def test_linked_oversized_and_secret_documents_are_refused(self):
        from se_harness.remote_authoring import file_bytes, Capture
        p=self.root/'large';p.write_bytes(b'x'*1025)
        with self.assertRaises(ValueError):file_bytes(p,1024)
        capture=Capture(self.root/'capture','synthetic-secret')
        with self.assertRaisesRegex(RemoteError,'credential'):
            capture.write('secret',b'contains synthetic-secret')
        self.assertFalse((capture.path/'secret').exists())
        link=self.root/'link'
        try:link.symlink_to(p)
        except OSError:self.skipTest('host cannot create symlinks')
        with self.assertRaises(ValueError):file_bytes(link,2048)

    def test_create_returns_exact_document_with_one_read_and_raw_replay_unchanged(self):
        from se_harness.remote import run
        import contextlib, io
        owner=self;requests=[];raw=b'+++\r\nid = "INT-TST-001"\r\n+++\r\n'
        view={'kind':'context','context_id':self.context,'context_version':1}
        accepted={'outcome':'accepted','receipt_id':'original-receipt','project_id':self.project,'view':view,
                  'affected_artifacts':[{'artifact_id':'INT-TST-001','revision_id':self.revision}],
                  'evaluator_output':{'incomplete':['Complete the definition.']}}
        document={'complete':True,'continuation':None,'project_id':self.project,'view':view,
                  'data':{'revision_id':self.revision,'envelope':{'artifact_id':'INT-TST-001','document_sha256':hashlib.sha256(raw).hexdigest()},
                          'document_base64':base64.b64encode(raw).decode()}}
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                requests.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                value=document if self.path.endswith('/reads/revision') else accepted
                body=(json.dumps(value,indent=3)+'\n').encode()
                self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
            def log_message(self,*args):pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            args=self.args('create-artifact','--typed','--evaluator-file',self.evaluator_file,'--client-wheel','fixture',
                '--operation-key','chosen','--expected-project-version','2','--context',self.context,'--context-version','0',
                '--domain','example','--artifact-type','intent','--artifact','INT-TST-001','--include-document','--compact','--record-directory',self.root/'new')
            args.endpoint='http://127.0.0.1:'+str(server.server_port)
            with mock.patch.dict('os.environ',{'HAG_TEST_TOKEN':'synthetic-secret'}),mock.patch('se_harness.remote.installed_client',return_value={'version':'test','wheel_sha256':'a'*64}),contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(0,run(args))
            result=json.loads(out.getvalue());self.assertEqual(2,len(requests))
            self.assertEqual('revision',requests[1]['operation'])
            self.assertEqual(self.revision,requests[1]['revision_id'])
            self.assertEqual(raw,Path(result['document_read']['documents'][0]['path']).read_bytes())
            self.assertEqual(raw.decode(),result['document_read']['documents'][0]['text'])
            self.assertEqual(accepted,result['result'])
            record=json.loads((self.root/'new/capture.json').read_text())
            self.assertTrue(all(x['body_complete'] for x in record['exchanges']))
            original=json.loads((self.root/'new/1-request.json').read_bytes())
            request=self.root/'raw.json';request.write_text(json.dumps(original))
            args=self.args('create-artifact','--request',request,'--client-wheel','fixture')
            args.endpoint='http://127.0.0.1:'+str(server.server_port)
            with mock.patch.dict('os.environ',{'HAG_TEST_TOKEN':'synthetic-secret'}),mock.patch('se_harness.remote.installed_client',return_value=original['client']),contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(0,run(args))
            self.assertEqual(accepted,json.loads(out.getvalue()))
            self.assertEqual(requests[0],requests[2])
        finally:
            server.shutdown();server.server_close();thread.join()


if __name__ == "__main__":
    unittest.main()
