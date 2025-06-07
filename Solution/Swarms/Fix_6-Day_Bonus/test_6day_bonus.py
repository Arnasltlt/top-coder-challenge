#!/usr/bin/env python3
import json
import subprocess
import tempfile
import os

# Test different bonus values for 6-day trips
bonus_values = [0.10, 0.12, 0.14, 0.15, 0.16, 0.17, 0.18, 0.20]

with open('public_cases.json', 'r') as f:
    cases = json.load(f)

six_day_cases = []
for i, case in enumerate(cases):
    if case['input']['trip_duration_days'] == 6:
        six_day_cases.append((i, case))

print(f'Testing {len(six_day_cases)} 6-day cases with different bonus values...')

best_bonus = 0.17
best_error = float('inf')

for bonus in bonus_values:
    # Create modified vintage_arithmetic.py
    with open('vintage_arithmetic.py', 'r') as f:
        content = f.read()
    
    # Replace the 6-day bonus line
    modified_content = content.replace(
        'bonus = vintage_multiply(base, 0.17)  # 17% bonus for 6-day trips',
        f'bonus = vintage_multiply(base, {bonus:.2f})  # {bonus*100:.0f}% bonus for 6-day trips'
    )
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(modified_content)
        temp_filename = temp_file.name
    
    try:
        total_error = 0
        for case_idx, case in six_day_cases:
            days = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            expected = case['expected_output']
            
            result = subprocess.run(['python3', temp_filename, str(days), str(miles), str(receipts)], 
                                  capture_output=True, text=True)
            actual = float(result.stdout.strip())
            error = abs(actual - expected)
            total_error += error
        
        avg_error = total_error / len(six_day_cases)
        print(f'Bonus {bonus*100:2.0f}%: Average error ${avg_error:.2f}')
        
        if avg_error < best_error:
            best_error = avg_error
            best_bonus = bonus
            
    finally:
        os.unlink(temp_filename)

print(f'\nBest bonus: {best_bonus*100:.0f}% with average error ${best_error:.2f}')