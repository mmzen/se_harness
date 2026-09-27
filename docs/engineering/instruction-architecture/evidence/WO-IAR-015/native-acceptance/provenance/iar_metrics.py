from pathlib import Path
import re,json,hashlib

R=Path(__file__).resolve().parent/'se_harness'
T=R/'templates/repository/standard'
H='docs/engineering/harness/'
O=R/'docs/engineering/instruction-architecture/acceptance/progressive-discovery'
source=R/'docs/engineering/instruction-architecture/proposals/progressive-discovery/instruction-review-source.md'
def slug(s):return re.sub(r'[^\w\- ]','',s.lower()).replace(' ','-')
def select(ref,selected):
    file,sep,anchor=ref.partition('#')
    path=T/(file+'.tpl' if file=='ENGINEERING_HARNESS.md' else file)
    lines=path.read_text(encoding='utf-8').splitlines()
    if not sep: start,end=0,len(lines)
    else:
        found=[(n,len(m[1]),m[2]) for n,line in enumerate(lines) if (m:=re.match(r'^(#{1,6}) (.+)$',line))]
        start,level,_=next(x for x in found if slug(x[2])==anchor)
        end=next((n for n,l,_ in found if n>start and l<=level),len(lines))
    selected.setdefault(file,set()).update(range(start,end))
    return lines
baseline=['ENGINEERING_HARNESS.md',H+'COMMUNICATION.md']
cases={
 'New requirement draft':['DEFINE_CHANGE.md','DRAFT_DEFINITIONS.md#draft-any-missing-definitions','DRAFT_DEFINITIONS.md#type-checklists','ARTIFACTS.md#artifact-types','ARTIFACTS.md#artifact-locations','DEFINITION_LINKS.md','../ARTIFACT_AUTHORING.md#design-simplicity','../ARTIFACT_AUTHORING.md#requirement'],
 'Resumed implementation':['CONTINUE.md','EXECUTE_WORK.md#establish-the-execution-context','EXECUTE_WORK.md#implement-the-approved-scope','AUTHORITY.md#authority-from-work-approval','../ARTIFACT_AUTHORING.md#review-of-implemented-changes','RESULTS.md#report-a-lifecycle-result'],
 'Verification decision':['CONTINUE.md','VERIFY_OUTCOME.md#obtain-the-humans-verification-decision','VERIFY_OUTCOME.md#record-the-verification-decision','AUTHORITY.md#decision-rights','AUTHORITY.md#delegation-and-separation','RESULTS.md#report-a-lifecycle-result'],
 'PR preparation':['CONTINUE.md','DELIVER_RESULT.md#select-the-delivery-action','DELIVER_RESULT.md#prepare-the-delivery-package','PULL_REQUEST.md','AUTHORITY.md#decision-rights','DELIVER_RESULT.md#confirm-authority-for-the-external-action','RESULTS.md#report-a-lifecycle-result'],
 'Blocker recovery':['CONTINUE.md','RESULTS.md','AUTHORITY.md#decision-rights'],
 'Evaluator setup':['SETUP.md','RESULTS.md#report-a-lifecycle-result']
}
rows=[]
for name,refs in cases.items():
    selected={};readings=list(baseline)
    for ref in refs:
        # Normalize paths such as harness/../ARTIFACT_AUTHORING.md without
        # losing file identity when the same reference is selected twice.
        part,sep,anchor=ref.partition('#')
        file=(T/H/part).resolve().relative_to(T.resolve()).as_posix()
        readings.append(file+(sep+anchor if sep else ''))
        if sep and (T/file).read_text(encoding='utf-8').find('## Before this action')>=0:
            readings += [file+'#read-this-when',file+'#before-this-action']
    texts={}
    for ref in readings:
        file=ref.partition('#')[0];texts[file]=select(ref,selected)
    words=sum(len('\n'.join(texts[file][n] for n in sorted(indices)).split()) for file,indices in selected.items())
    assert words<len(source.read_text(encoding='utf-8').split())
    rows.append({'case':name,'unique_instruction_words':words,'references':list(dict.fromkeys(readings)),
                 'formal_artifact_reading':'Separate, variable input: selected records and governing artifacts returned by the evaluator; exact evidence/candidate records when the action requires them. No formal-artifact word count is assumed.'})
report={'method':'Whitespace word counts over the union of selected line ranges, once per file. Root and the entire Communication policy are included in every fresh context. Selected actions include their entry conditions and conditional prerequisites for the named scenario. Whole-file reads are conservative where listed. No tokenizer or token-saving guarantee is used.',
        'source_words':len(source.read_text(encoding='utf-8').split()),'root_words':len((T/'ENGINEERING_HARNESS.md.tpl').read_text(encoding='utf-8').split()),'cases':rows,
        'qualification':'Reading walks over candidate content, not native-host traces or a completed migration. File integrity and automatic injection are separate work-order checks.'}
(O/'reading-cost.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
md='# Candidate instruction reading cost\n\n'+report['method']+'\n\n'
md+=f"Reviewed source: **{report['source_words']:,} words**. Injected root: **{report['root_words']:,} words**. The root is within the advisory 1,000–1,300-word target.\n\n"
md+='| Scenario | Unique instruction words |\n| --- | ---: |\n'
for row in rows:md+=f"| {row['case']} | {row['unique_instruction_words']:,} |\n"
md+='\nFormal artifacts and retained evidence are separate, variable inputs. Each scenario still requires the exact selected records. These counts do not replace their reading or claim measured model-token use.\n\n'+report['qualification']+'\n\nExact file/heading selections are retained in `reading-cost.json`.\n'
(O/'reading-cost.md').write_text(md,encoding='utf-8')
print(json.dumps({row['case']:row['unique_instruction_words'] for row in rows}))
