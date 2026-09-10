"""Explicit fixture asset copy/text replacement; invoked actions are recorded."""
import argparse, json, shutil
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
ap.add_argument('--copy-assets',type=Path);ap.add_argument('--path');ap.add_argument('--text-file',type=Path)
ap.add_argument('--old');ap.add_argument('--new');ns=ap.parse_args()
if ns.copy_assets:
    shutil.copytree(ns.copy_assets,ns.repo,dirs_exist_ok=True)
else:
    p=(ns.repo/ns.path).resolve()
    if not p.is_relative_to(ns.repo.resolve()):raise ValueError('fixture target outside root')
    p.parent.mkdir(parents=True,exist_ok=True)
    if ns.text_file:p.write_bytes(ns.text_file.read_bytes())
    else:
        text=p.read_text(encoding='utf8')
        if ns.old not in text:raise ValueError('exact old bytes absent')
        p.write_text(text.replace(ns.old,ns.new),encoding='utf8')
print(json.dumps({'fixture_edit':True,'target':str(ns.repo),'path':ns.path}))
