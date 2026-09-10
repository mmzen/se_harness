"""Fault injection for the controlled fixture read interface only."""
import json
print(json.dumps({'inspection':'unavailable','fault_injection':True,'message':'Controlled fixture file/state inspection unavailable. Operation effects cannot currently be determined.'}))
raise SystemExit(13)
