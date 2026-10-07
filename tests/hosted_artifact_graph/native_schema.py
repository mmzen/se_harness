"""Stage exact operation-specific schema views for native test input discovery.

No workflow order, requests, defaults, decisions or service actions are supplied.
The native agent chooses an operation; the original schemas remain available.
"""
import copy
import hashlib
import json


def operation_view(raw, family, operation):
    source = json.loads(raw)
    if family == 'remote-v1':
        branches = source['$defs']['Command']['oneOf']
        key = 'operation'
        pointer = '/$defs/Command/oneOf/'
    elif family == 'lifecycle-v2':
        branches = source['properties']['action']['oneOf']
        key = 'kind'
        pointer = '/properties/action/oneOf/'
    else:
        raise ValueError('Unsupported schema family')
    matches = [(i,b) for i,b in enumerate(branches) if b['properties'][key]['const']==operation]
    if len(matches)!=1:
        raise ValueError('Expected one exact operation')
    index, branch = matches[0]
    if family == 'remote-v1':
        view = copy.deepcopy(branch)
        definitions = {}
        def include(value):
            if isinstance(value,dict):
                if '$ref' in value:
                    ref=value['$ref']
                    if not ref.startswith('#/$defs/') or ref.count('/')!=2:
                        raise ValueError('Unsupported schema reference')
                    name=ref.split('/')[-1]
                    if name not in definitions:
                        definitions[name]=copy.deepcopy(source['$defs'][name])
                        include(definitions[name])
                for child in value.values():include(child)
            elif isinstance(value,list):
                for child in value:include(child)
        include(view)
        if definitions:view['$defs']=definitions
        view['$schema']=source['$schema']
    else:
        view=copy.deepcopy(source)
        view['properties']['action']['oneOf']=[copy.deepcopy(branch)]
    return {'source_sha256':hashlib.sha256(raw).hexdigest(),
            'source_pointer':pointer+str(index),'operation':operation,
            'scope':'Selected operation shape only; all shared constraints and referenced definitions retained. Original schema remains authoritative.',
            'schema':view}
