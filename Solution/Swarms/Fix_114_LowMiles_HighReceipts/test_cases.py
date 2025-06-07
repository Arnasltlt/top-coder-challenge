#!/usr/bin/env python3
import subprocess
import sys

# Test cases with known over-prediction issues
cases = [
    {'id': 114, 'days': 7, 'miles': 237.33, 'receipts': 1262.27, 'expected': 1452.17},
    {'id': 243, 'days': 5, 'miles': 728, 'receipts': 423.16, 'expected': 947.72}
]

for case in cases:
    # Test vintage_arithmetic model
    result = subprocess.run(['python3', 'vintage_arithmetic.py', str(case['days']), str(case['miles']), str(case['receipts'])], 
                          capture_output=True, text=True)
    prediction = float(result.stdout.strip())
    error = prediction - case['expected']
    daily_receipts = case['receipts'] / case['days']
    
    print(f'Case #{case["id"]}:')
    print(f'  Input: {case["days"]} days, {case["miles"]} miles, ${case["receipts"]} receipts')
    print(f'  Daily receipts: ${daily_receipts:.2f}')
    print(f'  Expected: ${case["expected"]}')
    print(f'  Predicted: ${prediction:.2f}')
    print(f'  Error: ${error:.2f} ({error/case["expected"]*100:.1f}%)')
    print(f'  Meets new penalty criteria (miles<300 & daily_receipts>120): {case["miles"] < 300 and daily_receipts > 120}')
    print()