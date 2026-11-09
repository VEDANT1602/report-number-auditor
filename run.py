import argparse
from pathlib import Path
from generate import generate
from core import audit,number_presence
from support import ROOT,dump,manifest

def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    artifact,cases=generate();raw=(ROOT/'data/experiment.json').read_bytes();rows=[]
    for case in cases:
        decision,reason=audit(case['claim'],artifact,raw)
        baseline=number_presence(case['claim'],artifact)
        rows.append({'id':case['id'],'expected':case['expected'],'typed_accept':decision,'reason':reason,'number_presence_accept':baseline})
    metrics={'cases':len(rows),'valid_claims':sum(r['expected'] for r in rows),
             'typed_correct':sum(r['typed_accept']==r['expected'] for r in rows),
             'baseline_correct':sum(r['number_presence_accept']==r['expected'] for r in rows),
             'typed_false_accepts':sum(r['typed_accept'] and not r['expected'] for r in rows),
             'baseline_false_accepts':sum(r['number_presence_accept'] and not r['expected'] for r in rows),
             'scope':'Authored structured-claim contracts, not natural-language factuality.'}
    dump(output/'decisions.json',rows);dump(output/'metrics.json',metrics)
    report=f"# Numerical evidence experiment\n\nThe typed auditor meets {metrics['typed_correct']}/{metrics['cases']} authored contracts, compared with {metrics['baseline_correct']}/{metrics['cases']} for numerical-presence checking. There are {metrics['valid_claims']} valid claims and {metrics['cases']-metrics['valid_claims']} invalid claims. False accepts are {metrics['typed_false_accepts']} versus {metrics['baseline_false_accepts']}.\n\nThis experiment deliberately targets known report failure boundaries. Number-presence is a weak ablation, not a mature fact-checking product. Both methods receive the same artifact and authored claims.\n\nMy approach binds the bytes, metric, population, denominator, operation, units and rounding tolerance before accepting a number. The useful result is an inspectable rejection reason. The next step is independently annotated real report sidecars; no LLM prose or automatic publishing was evaluated.\n"
    (output/'report.md').write_bytes(report.encode());manifest(output);return metrics

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='results');args=p.parse_args();print(run(ROOT/args.output))
