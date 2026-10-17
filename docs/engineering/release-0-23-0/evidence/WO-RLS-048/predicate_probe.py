import ast,json
from pathlib import Path
from types import SimpleNamespace
p=Path(__file__).resolve().parents[5]/"server/hosted_artifact_graph/service.py"
t=ast.parse(p.read_bytes())
m=next(n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=="compatibility")
e=next(n.args[0] for n in ast.walk(m) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="expect" and any(isinstance(x,ast.Constant) and x.value=="0.22.2" for x in ast.walk(n)))
r={}
for v in ("0.22.2","0.23.0","9.9.9"):
 c={"version":v,"wheel_sha256":"1"*64}
 r[v]=eval(compile(ast.Expression(e),str(p),"eval"),{},{"value":{"client":c},"self":SimpleNamespace(config={"client":c})})
print(json.dumps(r))
