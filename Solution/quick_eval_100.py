#!/usr/bin/env python3
import json
import subprocess

# Quick evaluation on first 100 cases
with open('../public_cases.json', 'r') as f:
    cases = json.load(f)

print("🚀 QUICK EVALUATION - 100 CASES 🚀")

errors = []
total_error = 0

for i, case in enumerate(cases[:100]):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled'] 
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    result = subprocess.run(['../run.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    predicted = float(result.stdout.strip())
    
    error = abs(predicted - expected)
    errors.append(error)
    total_error += error

mae = total_error / 100

print(f"MAE on 100 cases: ${mae:.2f}")

if mae < 50:
    print("✅ SIGNIFICANT IMPROVEMENT - Running full evaluation!")
elif mae < 100:
    print("⚠️ MODERATE IMPROVEMENT - May be worth full evaluation")
else:
    print("❌ STILL POOR - Need more work before full evaluation")

accuracy_25 = sum(1 for e in errors if e < 25) / 100
print(f"Accuracy (<$25): {accuracy_25*100:.1f}%")

if mae < 25:
    print("🎉 TARGET ACHIEVED ON 100 CASES!")
elif mae < 30:
    print("🔥 VERY CLOSE TO TARGET!")

# Show a few examples
print(f"\nSample results:")
for i in [0, 25, 50, 75]:
    case = cases[i]
    result = subprocess.run(['../run.sh', str(case['input']['trip_duration_days']), 
                           str(case['input']['miles_traveled']), 
                           str(case['input']['total_receipts_amount'])], 
                          capture_output=True, text=True)
    predicted = float(result.stdout.strip())
    error = abs(predicted - case['expected_output'])
    print(f"  Case {i}: Expected ${case['expected_output']:.2f}, Got ${predicted:.2f}, Error ${error:.2f}")