#!/usr/bin/env python3
import json
import subprocess

# Load test cases
with open('../public_cases.json', 'r') as f:
    cases = json.load(f)

print("=== FULL EVALUATION - V6 FINAL MODEL ===\n")

errors = []
total_error = 0
exact_matches = 0
close_matches = 0

# Test first 200 cases
print("Testing first 200 cases...")
for i, case in enumerate(cases[:200]):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled'] 
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    result = subprocess.run(['./run_v6_final.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    predicted = float(result.stdout.strip())
    
    error = abs(predicted - expected)
    errors.append(error)
    total_error += error
    
    if error <= 0.01:
        exact_matches += 1
    elif error <= 1.0:
        close_matches += 1
    
    if i % 50 == 49:
        print(f"  Processed {i+1} cases...")

mae = total_error / len(cases[:200])
accuracy_20 = sum(1 for e in errors if e < 20) / 200
accuracy_50 = sum(1 for e in errors if e < 50) / 200

print(f'\n=== FINAL PERFORMANCE REPORT ===')
print(f'Mean Absolute Error: ${mae:.2f}')
print(f'Exact matches: {exact_matches}/200 ({exact_matches/200*100:.1f}%)')
print(f'Close matches: {close_matches}/200 ({close_matches/200*100:.1f}%)')
print(f'Accuracy (<$20 error): {accuracy_20*100:.1f}%')
print(f'Accuracy (<$50 error): {accuracy_50*100:.1f}%')
print(f'Max error: ${max(errors):.2f}')
print(f'Min error: ${min(errors):.2f}')

print(f'\n=== READINESS ASSESSMENT ===')
if mae < 25:
    print('🚀 TARGET ACHIEVED! READY FOR SUBMISSION!')
elif mae < 50:
    print(f'🔧 CLOSE! Need ${mae-25:.1f} improvement to reach target')
elif mae < 100:
    print(f'⚠️ PROGRESS MADE. Need ${mae-25:.1f} improvement')  
else:
    print(f'❌ MORE WORK NEEDED. Need ${mae-25:.1f} improvement')

# Find remaining worst cases for potential quick fixes
print(f'\n=== TOP 5 WORST CASES (for potential quick fixes) ===')
worst_indices = sorted(range(len(errors)), key=lambda i: errors[i], reverse=True)[:5]
for i, idx in enumerate(worst_indices):
    case = cases[idx]
    print(f"{i+1}. Case {idx}: {case['input']['trip_duration_days']}d, {case['input']['miles_traveled']}mi, ${case['input']['total_receipts_amount']:.0f}rec")
    print(f"   Expected: ${case['expected_output']:.2f}, Error: ${errors[idx]:.2f}")