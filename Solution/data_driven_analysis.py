#!/usr/bin/env python3
import json

# Load all test cases
with open('../public_cases.json', 'r') as f:
    cases = json.load(f)

print("=== ULTRA DATA-DRIVEN REVERSE ENGINEERING ===\n")

# Group by similar patterns to find coefficients
duration_groups = {}
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    if days not in duration_groups:
        duration_groups[days] = []
    
    duration_groups[days].append({
        'miles': miles,
        'receipts': receipts,
        'expected': expected
    })

# Focus on 1-day trips to understand the pattern
print("=== 1-DAY TRIP ANALYSIS ===")
one_day = duration_groups[1]

# Sort by expected value to see patterns
one_day_sorted = sorted(one_day, key=lambda x: x['expected'])

print(f"Total 1-day cases: {len(one_day_sorted)}")
print("\nLow reimbursement cases:")
for case in one_day_sorted[:10]:
    print(f"  {case['miles']:4.0f}mi, ${case['receipts']:4.0f}rec → ${case['expected']:6.2f}")

print("\nHigh reimbursement cases:")
for case in one_day_sorted[-10:]:
    print(f"  {case['miles']:4.0f}mi, ${case['receipts']:4.0f}rec → ${case['expected']:6.2f}")

print("\n=== LOOKING FOR COMPONENT PATTERNS ===")

# Try to find if there are obvious breakpoints
print("\nCases where high receipts don't translate to high reimbursement:")
suspicious = [c for c in one_day if c['receipts'] > 1500 and c['expected'] < 800]
for case in suspicious:
    ratio = case['expected'] / case['receipts']
    print(f"  {case['miles']:4.0f}mi, ${case['receipts']:4.0f}rec → ${case['expected']:6.2f} (ratio: {ratio:.3f})")

print("\nCases where high mileage + high receipts = good reimbursement:")
good_cases = [c for c in one_day if c['receipts'] > 1500 and c['expected'] > 1200]
for case in good_cases:
    ratio = case['expected'] / case['receipts']
    mile_ratio = case['expected'] / case['miles']
    print(f"  {case['miles']:4.0f}mi, ${case['receipts']:4.0f}rec → ${case['expected']:6.2f} (rec_ratio: {ratio:.3f}, mile_ratio: {mile_ratio:.3f})")

# Try to find linear relationships in subsets
print("\n=== LOOKING FOR LINEAR RELATIONSHIPS ===")

# Cases with similar mileage ranges
moderate_mile_cases = [c for c in one_day if 800 <= c['miles'] <= 1000]
print(f"\nModerate mileage cases (800-1000 miles): {len(moderate_mile_cases)}")
for case in moderate_mile_cases:
    print(f"  {case['miles']:4.0f}mi, ${case['receipts']:4.0f}rec → ${case['expected']:6.2f}")

# Try to fit simple patterns
print("\n=== SIMPLE RATIO ANALYSIS ===")
print("Expected / Miles ratios:")
for case in one_day_sorted[-5:]:
    mile_ratio = case['expected'] / case['miles'] if case['miles'] > 0 else 0
    rec_ratio = case['expected'] / case['receipts'] if case['receipts'] > 0 else 0
    print(f"  {case['miles']:4.0f}mi, ${case['receipts']:4.0f}rec → ${case['expected']:6.2f} | Mile: {mile_ratio:.3f}, Rec: {rec_ratio:.3f}")