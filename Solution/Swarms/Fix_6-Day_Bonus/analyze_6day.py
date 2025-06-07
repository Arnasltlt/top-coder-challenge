#!/usr/bin/env python3
import json
import subprocess

with open('public_cases.json', 'r') as f:
    cases = json.load(f)

six_day_cases = []
for i, case in enumerate(cases):
    if case['input']['trip_duration_days'] == 6:
        six_day_cases.append((i, case))

print(f'Found {len(six_day_cases)} 6-day cases')

total_error = 0
under_predictions = 0
over_predictions = 0

for case_idx, case in six_day_cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    result = subprocess.run(['python3', 'vintage_arithmetic.py', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    actual = float(result.stdout.strip())
    error = abs(actual - expected)
    total_error += error
    
    if actual < expected:
        under_predictions += 1
    else:
        over_predictions += 1
    
    if len(six_day_cases) <= 20 or error > 100:  # Show all if few cases, or large errors
        print(f'Case {case_idx+1}: {days}d, {miles}mi, ${receipts} -> Expected: ${expected:.2f}, Got: ${actual:.2f}, Error: ${error:.2f}')

if six_day_cases:
    avg_error = total_error / len(six_day_cases)
    print(f'\nSummary for {len(six_day_cases)} 6-day cases:')
    print(f'Average error: ${avg_error:.2f}')
    print(f'Under-predictions: {under_predictions}')
    print(f'Over-predictions: {over_predictions}')