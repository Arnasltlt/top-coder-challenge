#!/usr/bin/env python3
import json
import subprocess
import sys
import os

# Load test cases from parent directory
with open('../public_cases.json', 'r') as f:
    cases = json.load(f)

errors = []
total_error = 0
exact_matches = 0
close_matches = 0

print("Testing current model performance...")

# Test first 200 cases for faster analysis
for i, case in enumerate(cases[:200]):
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
    
    if error <= 0.01:
        exact_matches += 1
    elif error <= 1.0:
        close_matches += 1
    
    if i % 50 == 0:
        print(f"Processed {i+1} cases...")

mae = total_error / len(cases[:200])
print(f'\n=== PERFORMANCE REPORT - First 200 cases ===')
print(f'Mean Absolute Error: ${mae:.2f}')
print(f'Exact matches: {exact_matches}/200 ({exact_matches/200*100:.1f}%)')
print(f'Close matches: {close_matches}/200 ({close_matches/200*100:.1f}%)')
print(f'Accuracy (<$20 error): {sum(1 for e in errors if e < 20)}/200 ({sum(1 for e in errors if e < 20)/200*100:.1f}%)')
print(f'Max error: ${max(errors):.2f}')

# Find worst 10 cases
worst_cases = []
for i, case in enumerate(cases[:200]):
    if errors[i] > 500:  # Very high errors
        worst_cases.append((i, case, errors[i]))

worst_cases.sort(key=lambda x: x[2], reverse=True)
print(f'\n=== WORST 10 CASES ===')
for i, (case_idx, case, error) in enumerate(worst_cases[:10]):
    print(f"{i+1}. Case {case_idx}: {case['input']['trip_duration_days']} days, {case['input']['miles_traveled']} miles, ${case['input']['total_receipts_amount']:.2f} receipts")
    print(f"   Expected: ${case['expected_output']:.2f}, Error: ${error:.2f}")