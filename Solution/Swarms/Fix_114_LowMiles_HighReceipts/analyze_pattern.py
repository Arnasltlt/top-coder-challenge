#!/usr/bin/env python3
import json
import subprocess

with open('public_cases.json', 'r') as f:
    cases = json.load(f)

# Find cases with low miles (<300) and various receipt levels
low_miles_cases = []

for i, case in enumerate(cases):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled'] 
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    daily_receipts = receipts / days if days > 0 else 0
    
    # Check for low miles cases
    if miles < 300:
        # Test current model prediction
        result = subprocess.run(['python3', 'vintage_arithmetic.py', str(days), str(miles), str(receipts)], 
                              capture_output=True, text=True)
        try:
            prediction = float(result.stdout.strip())
            error = prediction - expected
            error_pct = (error / expected) * 100 if expected > 0 else 0
            
            low_miles_cases.append({
                'id': i + 1,
                'days': days,
                'miles': miles,
                'receipts': receipts,
                'daily_receipts': daily_receipts,
                'expected': expected,
                'predicted': prediction,
                'error': error,
                'error_pct': error_pct
            })
        except:
            continue

# Sort by error (worst first)
low_miles_cases.sort(key=lambda x: x['error'], reverse=True)

print("LOW MILES (<300) CASES - WORST OVER-PREDICTIONS:")
print("=" * 80)
for case in low_miles_cases[:10]:  # Top 10 worst
    print(f"Case #{case['id']:3d}: {case['days']}d, {case['miles']:6.1f}mi, ${case['receipts']:7.2f} receipts")
    print(f"             Daily receipts: ${case['daily_receipts']:6.2f}")
    print(f"             Expected: ${case['expected']:7.2f}, Predicted: ${case['predicted']:7.2f}")
    print(f"             Error: ${case['error']:+7.2f} ({case['error_pct']:+5.1f}%)")
    print()

print("\nLOW MILES (<300) CASES WITH HIGH DAILY RECEIPTS (>$120):")
print("=" * 80)
high_receipt_low_miles = [c for c in low_miles_cases if c['daily_receipts'] > 120 and c['error'] > 50]
high_receipt_low_miles.sort(key=lambda x: x['error'], reverse=True)

for case in high_receipt_low_miles[:15]:
    print(f"Case #{case['id']:3d}: {case['days']}d, {case['miles']:6.1f}mi, ${case['receipts']:7.2f} receipts")
    print(f"             Daily receipts: ${case['daily_receipts']:6.2f}")
    print(f"             Expected: ${case['expected']:7.2f}, Predicted: ${case['predicted']:7.2f}")
    print(f"             Error: ${case['error']:+7.2f} ({case['error_pct']:+5.1f}%)")
    print()