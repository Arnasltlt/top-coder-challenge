#!/usr/bin/env python3

import json
import subprocess
import os

def run_my_model(days, miles, receipts):
    """My optimized linear model"""
    return 50.050486 * days + 0.445645 * miles + 0.382861 * receipts + 266.707681

def run_current_script(days, miles, receipts):
    """Run the current run.sh script"""
    try:
        result = subprocess.run(['bash', '../../run.sh', str(days), str(miles), str(receipts)], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            return float(result.stdout.strip())
        else:
            print(f"Error running script: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception running script: {e}")
        return None

def main():
    # Load test cases
    with open('../../public_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    print("🧾 Per Diem Model Performance Comparison")
    print("=" * 50)
    
    my_errors = []
    current_errors = []
    valid_tests = 0
    
    # Test first 20 cases for detailed comparison
    for i, case in enumerate(test_cases[:20]):
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        # My model
        my_result = run_my_model(days, miles, receipts)
        my_error = abs(my_result - expected)
        my_errors.append(my_error)
        
        # Current script
        current_result = run_current_script(days, miles, receipts)
        if current_result is not None:
            current_error = abs(current_result - expected)
            current_errors.append(current_error)
            valid_tests += 1
            
            print(f"Test {i+1:2d}: {days}d, {miles}mi, ${receipts:.2f}")
            print(f"  Expected: ${expected:.2f}")
            print(f"  My model: ${my_result:.2f} (error: ${my_error:.2f})")
            print(f"  Current:  ${current_result:.2f} (error: ${current_error:.2f})")
            print()
        else:
            print(f"Test {i+1:2d}: Current script failed")
    
    # Summary statistics
    if current_errors:
        print("\n📊 Performance Summary:")
        print(f"My linear model - Mean error: ${sum(my_errors)/len(my_errors):.2f}")
        print(f"Current script  - Mean error: ${sum(current_errors)/len(current_errors):.2f}")
        
        improvement = sum(current_errors)/len(current_errors) - sum(my_errors)/len(my_errors)
        print(f"Improvement: ${improvement:.2f} per case")
        
        if improvement > 0:
            print("✅ My per diem analysis model is MORE ACCURATE!")
        else:
            print("❌ Current implementation is more accurate")
    else:
        print("❌ Could not run current script for comparison")

if __name__ == "__main__":
    main()