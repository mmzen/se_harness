"""Operation views retain original constraints; they cannot widen acceptance."""
import copy
import json
import unittest
from pathlib import Path
from native_schema import operation_view

ROOT=Path(__file__).resolve().parents[2]


class SchemaViews(unittest.TestCase):
    def test_read_views_preserve_allof_and_unevaluated_property_boundary(self):
        raw=(ROOT/'server/contracts/read-v1.json').read_bytes();source=json.loads(raw)
        for index,branch in enumerate(source['$defs']['Request']['oneOf']):
            operation=branch['allOf'][1]['properties']['operation']['const']
            result=operation_view(raw,'read-v1',operation);view=result['schema']
            self.assertEqual(result['source_pointer'],'/$defs/Request/oneOf/'+str(index))
            self.assertEqual(view['allOf'],branch['allOf'])
            self.assertIs(view['unevaluatedProperties'],False)
            self.assertEqual(view['$defs']['RequestFields'],source['$defs']['RequestFields'])
            self.assertEqual(view['$defs']['Budget'],source['$defs']['Budget'])
            for name,definition in view['$defs'].items():self.assertEqual(definition,source['$defs'][name])
        with self.assertRaises(ValueError):operation_view(raw,'read-v1','create-artifact')

    def test_remote_branches_and_reference_closure_are_unchanged(self):
        raw=(ROOT/'server/contracts/remote-v1.json').read_bytes();source=json.loads(raw)
        for index,branch in enumerate(source['$defs']['Command']['oneOf']):
            operation=branch['properties']['operation']['const']
            selected=operation_view(raw,'remote-v1',operation)
            view=selected['schema']
            self.assertEqual(selected['source_pointer'],'/$defs/Command/oneOf/'+str(index))
            for key,value in branch.items():self.assertEqual(view[key],value)
            for key,value in view.get('$defs',{}).items():self.assertEqual(value,source['$defs'][key])
            self.assertFalse(view['additionalProperties'])
        with self.assertRaises(ValueError):operation_view(raw,'remote-v1','invented')
        broken=copy.deepcopy(source)
        broken['$defs']['Command']['oneOf'][0]['properties']['extra']={'$ref':'https://example.invalid/schema'}
        with self.assertRaisesRegex(ValueError,'reference'):
            operation_view(json.dumps(broken).encode(),'remote-v1',source['$defs']['Command']['oneOf'][0]['properties']['operation']['const'])

    def test_lifecycle_shared_constraints_and_only_selected_action_preserved(self):
        raw=(ROOT/'server/contracts/lifecycle-v2.json').read_bytes();source=json.loads(raw)
        for branch in source['properties']['action']['oneOf']:
            operation=branch['properties']['kind']['const']
            view=operation_view(raw,'lifecycle-v2',operation)['schema']
            restored=copy.deepcopy(view)
            restored['properties']['action']['oneOf']=source['properties']['action']['oneOf']
            self.assertEqual(restored,source)
            self.assertEqual(view['properties']['action']['oneOf'],[branch])
            self.assertEqual(view['required'],source['required'])
            self.assertFalse(view['additionalProperties'])
        with self.assertRaises(ValueError):operation_view(raw,'unknown','check')


if __name__=='__main__':unittest.main()
