#!/usr/bin/env python3
import subprocess

# Test the worst over-prediction cases identified
worst_cases = [
    {'id': 115, 'days': 5, 'miles': 195.7, 'receipts': 1228.49, 'expected': 511.23},
    {'id': 244, 'days': 4, 'miles': 286.0, 'receipts': 1063.49, 'expected': 418.17},
    {'id': 434, 'days': 5, 'miles': 210.0, 'receipts': 710.49, 'expected': 483.34},
    {'id': 82, 'days': 6, 'miles': 204.0, 'receipts': 818.99, 'expected': 628.40},
    {'id': 83, 'days': 1, 'miles': 263.0, 'receipts': 396.49, 'expected': 198.42},
]

print("TESTING WORST OVER-PREDICTION CASES:")
print("=" * 80)

for case in worst_cases:
    # Test vintage_arithmetic model
    result = subprocess.run(['python3', 'vintage_arithmetic.py', str(case['days']), str(case['miles']), str(case['receipts'])], 
                          capture_output=True, text=True)
    prediction = float(result.stdout.strip())
    error = prediction - case['expected']
    daily_receipts = case['receipts'] / case['days']
    
    # Calculate what penalty would be applied
    meets_criteria = case['miles'] < 300 and daily_receipts > 120
    if meets_criteria:
        miles_factor = max(0.2, (300 - case['miles']) / 300)
        receipts_factor = min(1.5, daily_receipts / 120)
        penalty_factor = 0.15 + (miles_factor * receipts_factor * 0.25)
        penalty_factor = min(0.40, penalty_factor)
        penalty_multiplier = 1.0 - penalty_factor
    else:
        penalty_factor = 0
        penalty_multiplier = 1.0
    
    print(f'Case #{case["id"]:3d}: {case["days"]}d, {case["miles"]:6.1f}mi, ${case["receipts"]:7.2f} receipts')
    print(f'             Daily receipts: ${daily_receipts:.2f}')
    print(f'             Expected: ${case["expected"]:7.2f}, Predicted: ${prediction:7.2f}')
    print(f'             Error: ${error:+7.2f} ({error/case["expected"]*100:+5.1f}%)')
    print(f'             Meets penalty criteria: {meets_criteria}')
    if meets_criteria:
        print(f'             Penalty applied: {penalty_factor:.1%} (multiplier: {penalty_multiplier:.3f})')
    print()