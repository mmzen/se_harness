"""Measure the actual configured read transaction timeout without graph writes.

The stress statement targets the database/driver mechanism directly. It is not
an admitted public Cypher form and does not claim HTTP timeout classification.
"""
import json
import time
from hosted_artifact_graph.protocol import Refusal
from pathlib import Path
from hosted_artifact_graph.service import Service

service = Service(json.loads(Path('/run/config/config.json').read_text()),
                  json.loads(Path('/run/secrets/sandbox_credentials').read_text()))
query = ('UNWIND range(1,1000) AS a UNWIND range(1,1000) AS b '
         'UNWIND range(1,1000) AS c RETURN sum(a+b+c) AS total')
start = time.monotonic()
try:
    try:
        with service.store.transaction(timeout=5) as tx:
            tx.run(query).consume()
    except Exception as exc:
        result = {'type':type(exc).__name__, 'code':getattr(exc,'code',None), 'message':str(exc), 'status':getattr(exc,'status',None)}
    else:
        result = {'unexpected_completion': True}
finally:
    service.store.driver.close()
seconds = time.monotonic() - start
print(json.dumps({'query':query,'requested_transaction_timeout_seconds':5,'seconds':seconds,'result':result,
                  'claim':'Database/driver time limit only; no public grammar or HTTP error-code proof.'}))
assert 4 <= seconds < 12
assert result.get('code') == 'HAG_REMOTE_RESOURCE_LIMIT' and result.get('status') == 429
