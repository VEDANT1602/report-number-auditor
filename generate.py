"""Authored numerical claims with declared correct outcomes."""
import copy
import hashlib
from support import ROOT,dump

def generate():
    artifact={'experiment':'fictional-duration-trial','metrics':{
        'test_completion':{'kind':'ratio','numerator':52,'denominator':100,'population':'test-orders','count_unit':'orders'},
        'baseline_completion':{'kind':'ratio','numerator':40,'denominator':100,'population':'test-orders','count_unit':'orders'},
        'train_completion':{'kind':'ratio','numerator':90,'denominator':100,'population':'train-orders','count_unit':'orders'},
        'latency':{'kind':'scalar','value':12.345,'unit':'milliseconds','population':'test-requests'},
        'zero':{'kind':'ratio','numerator':0,'denominator':100,'population':'test-orders','count_unit':'orders'}}}
    dump(ROOT/'data/experiment.json',artifact)
    digest=hashlib.sha256((ROOT/'data/experiment.json').read_bytes()).hexdigest()
    base={'metric':'test_completion','operation':'percent','value':52,'unit':'percent','population':'test-orders',
          'denominator':100,'digits':1,'artifact_sha256':digest}
    cases=[]
    def add(cid,changes=None,valid=True):
        c=copy.deepcopy(base);c.update(changes or {});cases.append({'id':cid,'claim':c,'expected':valid})
    add('valid-percent');add('valid-fraction',{'operation':'fraction','value':0.52,'unit':'fraction','digits':2})
    add('valid-count',{'operation':'count','value':52,'unit':'orders','digits':0})
    add('valid-scalar',{'metric':'latency','operation':'scalar','value':12.35,'unit':'milliseconds','population':'test-requests','digits':2})
    add('valid-points',{'operation':'difference_points','baseline_metric':'baseline_completion','baseline_denominator':100,'value':12,'unit':'percentage_points'})
    add('valid-relative',{'operation':'relative_change','baseline_metric':'baseline_completion','baseline_denominator':100,'value':30,'unit':'percent_change'})
    add('valid-rounding',{'metric':'latency','operation':'scalar','value':12.3,'unit':'milliseconds','population':'test-requests','digits':1})
    add('stale-bytes',{'artifact_sha256':'0'*64},False)
    add('wrong-population',{'population':'all-orders'},False)
    add('wrong-denominator',{'denominator':120},False)
    add('train-swap',{'metric':'train_completion','value':90},False)
    add('wrong-unit',{'unit':'fraction'},False)
    add('unsupported-rescale',{'value':5200},False)
    add('percent-as-points',{'operation':'difference_points','baseline_metric':'baseline_completion','baseline_denominator':100,'value':30,'unit':'percent_change'},False)
    add('wrong-baseline-population',{'operation':'difference_points','baseline_metric':'train_completion','baseline_denominator':100,'value':-38,'unit':'percentage_points'},False)
    add('wrong-baseline-count',{'operation':'relative_change','baseline_metric':'baseline_completion','baseline_denominator':1000,'value':30,'unit':'percent_change'},False)
    add('zero-relative-base',{'operation':'relative_change','baseline_metric':'zero','baseline_denominator':100,'value':52,'unit':'percent_change'},False)
    add('unknown-metric',{'metric':'missing'},False)
    add('too-many-digits',{'digits':9},False)
    add('numerical-near-miss',{'value':52.11},False)
    dump(ROOT/'data/claims.json',cases)
    return artifact,cases
