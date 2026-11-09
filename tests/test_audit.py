import copy
import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from core import audit,quantity
from generate import generate
from support import verify_manifest

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.a,self.c=generate();self.raw=(ROOT/'data/experiment.json').read_bytes()
    def test_authored_contracts(self):
        for c in self.c:
            with self.subTest(case=c['id']):self.assertEqual(c['expected'],audit(c['claim'],self.a,self.raw)[0])
    def test_digest_binds_actual_bytes(self):
        self.assertFalse(audit(self.c[0]['claim'],self.a,self.raw+b' ')[0])
    def test_unbound_dictionary_cannot_replace_evidence(self):
        altered=copy.deepcopy(self.a);altered['metrics']['test_completion']['numerator']=99
        c=copy.deepcopy(self.c[0]['claim']);c['value']=99
        self.assertFalse(audit(c,altered,self.raw)[0])
    def test_nonfinite_claims_rejected(self):
        for v in [float('nan'),float('inf'),True,'52']:
            c=copy.deepcopy(self.c[0]['claim']);c['value']=v;self.assertFalse(audit(c,self.a,self.raw)[0])
    def test_empty_denominator_rejected(self):
        with self.assertRaises(ValueError):quantity({'kind':'ratio','numerator':0,'denominator':0},'percent')
    def test_percent_and_points_are_distinct(self):
        c=copy.deepcopy(self.c[4]['claim']);c['unit']='percent';self.assertFalse(audit(c,self.a,self.raw)[0])
    def test_rounding_bound(self):
        c=copy.deepcopy(self.c[0]['claim']);c['digits']=1;c['value']=52.049;self.assertTrue(audit(c,self.a,self.raw)[0]);c['value']=52.051;self.assertFalse(audit(c,self.a,self.raw)[0])
    def test_unknown_operation_refused(self):
        c=copy.deepcopy(self.c[0]['claim']);c['operation']='eval';self.assertFalse(audit(c,self.a,self.raw)[0])
    def test_committed_manifest(self):verify_manifest()
