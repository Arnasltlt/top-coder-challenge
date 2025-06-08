#!/usr/bin/env python3
"""Builds a simple residual look-up table (3D buckets) from the public_cases.json using the frozen baseline engine.
Outputs residual_table.json with the mean residual for each bucket.
Buckets:
   days_bucket: 1-14 (individual days), >=15 aggregated
   miles_bucket: 0-100,100-300,300-600,600-1000,>1000
   spend_bucket (daily receipts): <50,50-150,150-300,>300
"""
import json, math, subprocess, os, sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PUBLIC = os.path.join(ROOT, 'public_cases.json')
BASELINE = os.path.join(os.path.dirname(__file__), 'baseline_vintage_arithmetic.py')

if not os.path.exists(PUBLIC):
    print('public_cases.json not found'); sys.exit(1)

def days_bucket(d):
    return str(d) if d<=14 else '15+'

def miles_bucket(m):
    if m<100: return '0-100'
    if m<300: return '100-300'
    if m<600: return '300-600'
    if m<1000: return '600-1000'
    return '1000+'

def spend_bucket(daily):
    if daily<50: return '<50'
    if daily<150: return '50-150'
    if daily<300: return '150-300'
    return '300+'

def baseline_predict(days,miles,receipts):
    # Call baseline vintage script via subprocess to reuse same logic
    result = subprocess.check_output([
        'python3', BASELINE, str(days), str(miles), str(receipts)
    ], text=True)
    return float(result.strip())

table = defaultdict(list)
with open(PUBLIC) as f:
    cases = json.load(f)
for idx, case in enumerate(cases):
    inp = case['input']; expected = case['expected_output']
    days = inp['trip_duration_days']; miles = inp['miles_traveled']; receipts = inp['total_receipts_amount']
    pred = baseline_predict(days,miles,receipts)
    resid = expected - pred
    key = (days_bucket(days), miles_bucket(miles), spend_bucket(receipts/days))
    table[key].append(resid)

# compute mean residual per bucket
mean_table = {"|".join(k): sum(v)/len(v) for k,v in table.items() if v}
with open(os.path.join(os.path.dirname(__file__), 'residual_table.json'), 'w') as f:
    json.dump(mean_table, f, indent=2)
print('Residual table written with', len(mean_table), 'buckets') 