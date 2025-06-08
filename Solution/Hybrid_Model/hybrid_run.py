#!/usr/bin/env python3
"""Hybrid runner: calls baseline engine and optionally applies residual correction from lookup table."""
import sys, os, json, subprocess

def load_table():
    table_path = os.path.join(os.path.dirname(__file__), 'residual_table.json')
    if not os.path.exists(table_path):
        return {}
    with open(table_path) as f:
        return json.load(f)

def bucketize(days, miles, receipts):
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
    return "|".join((days_bucket(days), miles_bucket(miles), spend_bucket(receipts/days)))

def baseline_predict(days,miles,receipts):
    baseline_script = os.path.join(os.path.dirname(__file__), 'baseline_vintage_arithmetic.py')
    out = subprocess.check_output(['python3', baseline_script, str(days), str(miles), str(receipts)], text=True)
    return float(out.strip())

def main():
    if len(sys.argv)!=4:
        print('Usage: hybrid_run.py <days> <miles> <receipts>'); sys.exit(1)
    days = int(float(sys.argv[1])); miles = float(sys.argv[2]); receipts = float(sys.argv[3])

    base = baseline_predict(days,miles,receipts)
    tbl = load_table()
    key = bucketize(days,miles,receipts)
    residual = tbl.get(key,0.0)

    # apply correction only if abs(residual)>50
    if abs(residual)>=50:
        corrected = base + residual
    else:
        corrected = base
    print(f"{corrected:.2f}")

if __name__=='__main__':
    main() 