"""Transparent call recorder around the unchanged real export_tracked_tree."""
import argparse,gzip,hashlib,importlib.util,json,pathlib,subprocess,sys,time,traceback

ap=argparse.ArgumentParser();ap.add_argument('--source',type=pathlib.Path,required=True);ap.add_argument('--destination',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True)
a=ap.parse_args();out=a.output;out.mkdir(exist_ok=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def js(name,x):(out/name).write_bytes((json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
module_path=a.source/'repository_tools/upgrade_rehearsal.py'
(out/'worker-source.py').write_bytes(pathlib.Path(__file__).read_bytes());(out/'exporter-source.py').write_bytes(module_path.read_bytes())
spec=importlib.util.spec_from_file_location('actual_upgrade_rehearsal',module_path)
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
real_run=subprocess.run;records=[]
def traced_run(*args,**kwargs):
    name='call%02d'%(len(records)+1);records.append(name)
    record=dict(argv=[str(x) for x in args[0]],cwd=str(kwargs.get('cwd','')),timeout=kwargs.get('timeout'),
        text_mode=bool(kwargs.get('text')),observer='Passthrough to original subprocess.run; no command or returned output replacement')
    start=time.time();p=None
    try:
        p=real_run(*args,**kwargs);record['returncode']=p.returncode
        return p
    except BaseException as e:
        record['error']=dict(type=type(e).__name__,message=str(e))
        if isinstance(e,subprocess.TimeoutExpired):p=e
        raise
    finally:
        record['elapsed_seconds']=time.time()-start
        for stream in ['stdout','stderr']:
            value=getattr(p,stream,None) if p is not None else None
            if value is None:value=b''
            raw=value.encode('utf-8') if isinstance(value,str) else value
            compressed=len(raw)>1000000
            filename=name+'.'+stream+('.gz' if compressed else '')
            stored=gzip.compress(raw,mtime=0) if compressed else raw
            (out/filename).write_bytes(stored)
            record[stream]=dict(path=filename,encoding='gzip' if compressed else 'identity',bytes=len(raw),sha256=sha(raw),stored_sha256=sha(stored),
                representation='UTF-8 bytes of text returned by unchanged helper' if isinstance(value,str) else 'raw subprocess bytes')
        js(name+'.json',record)
subprocess.run=traced_run
result=dict(source=str(a.source),destination=str(a.destination),destination_characters=len(str(a.destination)),
    worker_sha256=sha(pathlib.Path(__file__).read_bytes()),exporter_sha256=sha(module_path.read_bytes()),passed=False)
try:
    module.export_tracked_tree(a.source,a.destination)
    result['passed']=True
except BaseException as e:result['error']=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc())
finally:
    subprocess.run=real_run;result['calls']=records;js('result.json',result)
    print(json.dumps(result,indent=2))
raise SystemExit(0 if result['passed'] else 1)
