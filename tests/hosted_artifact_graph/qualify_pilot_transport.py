"""Drop one real committed HTTP reply, then reconcile through the installed client."""
import argparse
import copy
import json
import socket
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from qualify_pilot import Pilot


def run(args):
    pilot = Pilot(args)
    state = json.loads(args.state.read_text())
    pilot.version, pilot.context = state['project_version'], state['context']
    request = pilot.action({'kind':'raise-risk','domain':'lifecycle-pilot','id':'RISK-P3-040',
        'title':'Lost reply rehearsal','description':'The transport drops an acknowledged test write.',
        'action':'Retrieve the original operation receipt.','owner':'test-owner','raised_by':'test-executor',
        'threatens':['WO-P3-001']})
    preview = pilot.cli('preview-lost-reply','rehearse',request)
    request.update(mode='apply',preview_digest=preview['preview_digest'])
    endpoint = args.endpoint
    received = []
    class DropReply(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def do_POST(self):
            body = self.rfile.read(int(self.headers['Content-Length']))
            upstream = urllib.request.Request(endpoint+self.path, body, method='POST',
                headers={'Authorization':self.headers['Authorization'],'Content-Type':'application/json'})
            with urllib.request.urlopen(upstream, timeout=180) as response:
                received.append({'status':response.status,'result':json.load(response)})
            self.close_connection = True
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
    proxy = ThreadingHTTPServer(('127.0.0.1',0),DropReply)
    thread=threading.Thread(target=proxy.serve_forever,daemon=True); thread.start()
    try:
        args.endpoint='http://127.0.0.1:'+str(proxy.server_port)
        unknown=pilot.cli('lost-reply','rehearse',request,expected=2)
    finally:
        args.endpoint=endpoint; proxy.shutdown();proxy.server_close();thread.join()
    pilot.save('server-committed.json',received)
    assert unknown['outcome']=='unknown' and len(received)==1 and received[0]['status']==200
    receipt=pilot.cli('receipt','operation',extra=('--key',request['operation_key']))
    assert receipt==received[0]['result']
    repeated=pilot.cli('identical-retry','rehearse',request)
    assert repeated==receipt
    status=pilot.cli('unchanged-after-retry','status')
    assert status['project_version']==pilot.version+1
    pilot.version=status['project_version'];pilot.context=receipt['view']
    exported=pilot.export('after-lost-reply',receipt['baseline_id'])
    pilot.save('transport.json',{'state':'unknown_reply_recovered','events':pilot.events,
        'request':request,'result':receipt,'context':pilot.context,'project_version':pilot.version,
        'export':str(exported),'source':pilot.source['source']})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('client-python','client-wheel','configuration','credentials','source-manifest','repository','output','state'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--endpoint',required=True)
    run(parser.parse_args())
