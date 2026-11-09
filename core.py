"""Typed numerical claims, not natural-language fact checking."""
import hashlib
import json
import math

def finite(value):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
        raise ValueError('finite numeric value required')
    return value

def quantity(metric,op):
    if metric['kind']=='ratio':
        numerator=finite(metric['numerator']); denominator=finite(metric['denominator'])
        if denominator<=0 or numerator<0 or numerator>denominator:
            raise ValueError('invalid ratio population')
        if op=='fraction': return numerator/denominator,'fraction'
        if op=='percent': return 100*numerator/denominator,'percent'
        if op=='count': return numerator,metric['count_unit']
    if metric['kind']=='scalar' and op=='scalar':
        return finite(metric['value']),metric['unit']
    raise ValueError('operation incompatible with metric kind')

def audit(claim,artifact,artifact_bytes):
    try:
        if claim['artifact_sha256']!=hashlib.sha256(artifact_bytes).hexdigest():
            return False,'artifact_digest_mismatch'
        if artifact!=json.loads(artifact_bytes):
            return False,'artifact_content_mismatch'
        metric=artifact['metrics'][claim['metric']]
        if claim['population']!=metric['population']:
            return False,'population_mismatch'
        if metric['kind']=='ratio' and claim.get('denominator')!=metric['denominator']:
            return False,'denominator_mismatch'
        op=claim['operation']
        if op in ('difference_points','relative_change'):
            base=artifact['metrics'][claim['baseline_metric']]
            if base['population']!=metric['population'] or base['kind']!=metric['kind']:
                return False,'incomparable_baseline'
            current,_=quantity(metric,'fraction'); previous,_=quantity(base,'fraction')
            if claim.get('baseline_denominator')!=base['denominator']:
                return False,'baseline_denominator_mismatch'
            if op=='difference_points': expected,unit=100*(current-previous),'percentage_points'
            else:
                if previous==0: return False,'zero_baseline'
                expected,unit=100*(current-previous)/previous,'percent_change'
        else: expected,unit=quantity(metric,op)
        if claim['unit']!=unit: return False,'unit_mismatch'
        digits=claim['digits']
        if isinstance(digits,bool) or not isinstance(digits,int) or not 0<=digits<=6:
            raise ValueError('digits outside declared contract')
        value=finite(claim['value'])
        # digits defines an absolute numerical rounding tolerance. It does not
        # constrain the number of decimal places in the claim's rendered text.
        tolerance=0.5*10**(-digits)+1e-12
        return (True,'supported') if abs(value-expected)<=tolerance else (False,'value_mismatch')
    except (KeyError,TypeError,ValueError,OverflowError):
        return False,'malformed_or_missing_evidence'

def number_presence(claim,artifact):
    values=[]
    for metric in artifact['metrics'].values():
        for op in ('scalar','fraction','percent','count'):
            try: values.append(quantity(metric,op)[0])
            except ValueError: pass
    try: return any(abs(finite(claim['value'])-v)<=0.51 for v in values)
    except (KeyError,ValueError): return False
