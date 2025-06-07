#!/usr/bin/env python3
import json

def percentile(data, pct):
    return sorted(data)[int(len(data) * pct / 100)]

# Load test cases
with open('../public_cases.json', 'r') as f:
    cases = json.load(f)

print("=== ULTRA-ANALYSIS OF REAL SYSTEM PATTERNS ===\n")

# Analyze by trip duration
duration_analysis = {}
for case in cases[:500]:  # Analyze more cases
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    if days not in duration_analysis:
        duration_analysis[days] = []
    
    duration_analysis[days].append({
        'miles': miles,
        'receipts': receipts,
        'expected': expected,
        'per_mile': expected / miles if miles > 0 else 0,
        'per_receipt': expected / receipts if receipts > 0 else 0
    })

# Print patterns for each duration
for days in sorted(duration_analysis.keys())[:10]:  # Focus on common durations
    data = duration_analysis[days]
    print(f"=== {days}-DAY TRIPS ({len(data)} cases) ===")
    
    expected_vals = [d['expected'] for d in data]
    miles_vals = [d['miles'] for d in data]
    receipt_vals = [d['receipts'] for d in data]
    
    print(f"Expected range: ${min(expected_vals):.2f} - ${max(expected_vals):.2f}")
    print(f"Miles range: {min(miles_vals):.0f} - {max(miles_vals):.0f}")
    print(f"Receipts range: ${min(receipt_vals):.2f} - ${max(receipt_vals):.2f}")
    
    # Look for patterns in high cases
    high_reimbursement = [d for d in data if d['expected'] > percentile(expected_vals, 90)]
    if high_reimbursement:
        print(f"High reimbursement cases (top 10%):")
        for hr in high_reimbursement[:3]:
            print(f"  {hr['miles']:.0f}mi, ${hr['receipts']:.0f}rec → ${hr['expected']:.0f}")
    
    # Look for patterns in receipt heavy cases  
    high_receipt = [d for d in data if d['receipts'] > percentile(receipt_vals, 90)]
    if high_receipt:
        print(f"High receipt cases (top 10%):")
        for hr in high_receipt[:3]:
            print(f"  {hr['miles']:.0f}mi, ${hr['receipts']:.0f}rec → ${hr['expected']:.0f}")
    
    print()

print("\n=== EXTREME CASE ANALYSIS ===")

# Find cases with very high receipts to understand caps
high_receipt_cases = [(c['input'], c['expected_output']) for c in cases 
                     if c['input']['total_receipts_amount'] > 2000]

print(f"Cases with receipts >$2000 ({len(high_receipt_cases)} cases):")
for inp, exp in high_receipt_cases[:10]:
    print(f"  {inp['trip_duration_days']}d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.0f}rec → ${exp:.0f}")

# Find cases with very high mileage
high_mileage_cases = [(c['input'], c['expected_output']) for c in cases 
                     if c['input']['miles_traveled'] > 1000]

print(f"\nCases with mileage >1000 ({len(high_mileage_cases)} cases):")
for inp, exp in high_mileage_cases[:10]:
    print(f"  {inp['trip_duration_days']}d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.0f}rec → ${exp:.0f}")

# Look for very low expected values (might reveal caps)
low_expected = [(c['input'], c['expected_output']) for c in cases 
               if c['expected_output'] < 500 and c['input']['total_receipts_amount'] > 1000]

print(f"\nLow reimbursement despite high receipts ({len(low_expected)} cases):")
for inp, exp in low_expected[:10]:
    print(f"  {inp['trip_duration_days']}d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.0f}rec → ${exp:.0f}")