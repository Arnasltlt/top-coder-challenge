#!/usr/bin/env python3

import json
import subprocess
import math

def run_model(trip_duration_days, miles_traveled, total_receipts_amount):
    """Run the bash script and return the result"""
    try:
        result = subprocess.run([
            '/Users/seima/8090/top-coder-challenge/run.sh',
            str(trip_duration_days),
            str(miles_traveled),
            str(total_receipts_amount)
        ], capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error running model: {e}")
        return None

def main():
    # Load test cases
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    # Test first 20 cases
    print("Testing First 20 Cases:")
    print("=" * 80)
    print(f"{'Case':<4} {'Days':<4} {'Miles':<6} {'Receipts':<10} {'Expected':<10} {'Actual':<10} {'Error':<10} {'Error%':<8}")
    print("=" * 80)
    
    total_error = 0
    total_abs_error = 0
    valid_cases = 0
    
    for i, case in enumerate(test_cases[:20]):
        input_data = case['input']
        expected = case['expected_output']
        
        # Run the model
        actual = run_model(
            input_data['trip_duration_days'],
            input_data['miles_traveled'],
            input_data['total_receipts_amount']
        )
        
        if actual is not None:
            error = actual - expected
            error_pct = (error / expected) * 100 if expected != 0 else 0
            
            print(f"{i+1:<4} {input_data['trip_duration_days']:<4} {input_data['miles_traveled']:<6} {input_data['total_receipts_amount']:<10.2f} {expected:<10.2f} {actual:<10.2f} {error:<10.2f} {error_pct:<8.1f}%")
            
            total_error += error
            total_abs_error += abs(error)
            valid_cases += 1
        else:
            print(f"{i+1:<4} ERROR running case")
    
    print("=" * 80)
    if valid_cases > 0:
        mean_error = total_error / valid_cases
        mean_abs_error = total_abs_error / valid_cases
        print(f"Summary Statistics:")
        print(f"Mean Error: {mean_error:.2f}")
        print(f"Mean Absolute Error: {mean_abs_error:.2f}")
        print(f"Valid Cases: {valid_cases}/20")

if __name__ == "__main__":
    main()