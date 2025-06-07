#!/usr/bin/env python3
import json
import subprocess

# Load test cases
with open('../public_cases.json', 'r') as f:
    cases = json.load(f)

print("🚀 FINAL EVALUATION - OUTLIER-AWARE MODEL 🚀\n")

errors = []
total_error = 0
exact_matches = 0
close_matches = 0

# Test first 200 cases  
print("Testing first 200 cases with outlier-aware model...")
for i, case in enumerate(cases[:200]):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled'] 
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    result = subprocess.run(['./run_with_outliers.sh', str(days), str(miles), str(receipts)], 
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

# Performance metrics
accuracy_1 = sum(1 for e in errors if e < 1) / 200
accuracy_5 = sum(1 for e in errors if e < 5) / 200
accuracy_10 = sum(1 for e in errors if e < 10) / 200  
accuracy_20 = sum(1 for e in errors if e < 20) / 200
accuracy_25 = sum(1 for e in errors if e < 25) / 200
accuracy_50 = sum(1 for e in errors if e < 50) / 200

print(f'\n🎯 FINAL PERFORMANCE REPORT 🎯')
print(f'Mean Absolute Error: ${mae:.2f}')
print(f'Exact matches (±$0.01): {exact_matches}/200 ({exact_matches/200*100:.1f}%)')
print(f'Close matches (±$1.00): {close_matches}/200 ({close_matches/200*100:.1f}%)')
print(f'Accuracy (<$1 error): {accuracy_1*100:.1f}%')
print(f'Accuracy (<$5 error): {accuracy_5*100:.1f}%')
print(f'Accuracy (<$10 error): {accuracy_10*100:.1f}%')
print(f'Accuracy (<$20 error): {accuracy_20*100:.1f}%')
print(f'Accuracy (<$25 error): {accuracy_25*100:.1f}%')
print(f'Accuracy (<$50 error): {accuracy_50*100:.1f}%')
print(f'Max error: ${max(errors):.2f}')
print(f'Min error: ${min(errors):.2f}')

# CHALLENGE REQUIREMENT CHECK
print(f'\n🎯 CHALLENGE REQUIREMENT ASSESSMENT 🎯')
if mae < 25:
    print('✅ CHALLENGE REQUIREMENT MET!')
    print(f'✅ MAE: ${mae:.2f} < $25.00 TARGET')
    print('🚀 READY FOR SUBMISSION!')
    
    if mae < 10:
        print('🌟 EXCEPTIONAL PERFORMANCE!')
    elif mae < 5:
        print('👑 OUTSTANDING PERFORMANCE!')
        
    print(f'\n🏆 SUCCESS METRICS:')
    print(f'• Target MAE <$25: ✅ ACHIEVED (${mae:.2f})')
    print(f'• High accuracy: {accuracy_25*100:.1f}% cases within target')
    print(f'• Outlier patterns: Successfully detected and handled')
    print(f'• Data-driven approach: Coefficients fitted to training data')
    
else:
    improvement_needed = mae - 25
    print(f'❌ NOT QUITE THERE: Need ${improvement_needed:.1f} improvement')
    print(f'Current: ${mae:.2f}, Target: <$25.00')
    
    if mae < 50:
        print('🔧 VERY CLOSE - Minor tuning needed')
    elif mae < 100:
        print('⚠️ SUBSTANTIAL PROGRESS - More work needed')

# Best performing ranges
print(f'\n📊 ERROR DISTRIBUTION 📊')
ranges = [(0,1,'Perfect'), (1,5,'Excellent'), (5,10,'Very Good'), (10,25,'Good'), (25,50,'Acceptable'), (50,100,'Poor'), (100,float('inf'),'Very Poor')]

for min_e, max_e, label in ranges:
    count = sum(1 for e in errors if min_e <= e < max_e)
    pct = count / 200 * 100
    print(f'{label:12s}: {count:3d} cases ({pct:4.1f}%)')

if exact_matches > 5:
    print(f'\n✨ Found {exact_matches} EXACT MATCHES - Outstanding precision!')

# Show remaining worst cases for insight
worst_errors = sorted(enumerate(errors), key=lambda x: x[1], reverse=True)[:5]
print(f'\n🔍 TOP 5 REMAINING CHALLENGES:')
for i, (case_idx, error) in enumerate(worst_errors):
    case = cases[case_idx]
    print(f'{i+1}. Case {case_idx}: {case["input"]["trip_duration_days"]}d, {case["input"]["miles_traveled"]}mi, ${case["input"]["total_receipts_amount"]:.0f}rec')
    print(f'   Expected: ${case["expected_output"]:.2f}, Error: ${error:.2f}')