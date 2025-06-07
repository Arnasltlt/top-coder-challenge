#!/usr/bin/env python3

import json
import subprocess
import os
import sys
from typing import List, Dict, Tuple

def load_test_cases(filename: str, limit: int = 20) -> List[Dict]:
    """Load and return the first N test cases from the JSON file."""
    with open(filename, 'r') as f:
        cases = json.load(f)
    return cases[:limit]

def run_model(days: int, miles: int, receipts: float) -> float:
    """Run the model script and return the predicted output."""
    try:
        # Run the shell script with the given parameters
        result = subprocess.run(
            ['bash', '/Users/seima/8090/top-coder-challenge/run.sh', str(days), str(miles), str(receipts)],
            capture_output=True,
            text=True,
            check=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error running model: {e}")
        return 0.0

def calculate_metrics(test_cases: List[Dict]) -> Tuple[float, List[Tuple[int, float, float, float, float]]]:
    """
    Calculate mean absolute error and identify worst performing cases.
    Returns (mae, worst_cases) where worst_cases is a list of tuples:
    (case_index, predicted, expected, absolute_error, error_percentage)
    """
    errors = []
    results = []
    
    print("Testing model against first 20 test cases...")
    print("=" * 80)
    print(f"{'Case':<4} {'Days':<4} {'Miles':<6} {'Receipts':<8} {'Expected':<10} {'Predicted':<10} {'Error':<8} {'Error %':<8}")
    print("=" * 80)
    
    for i, case in enumerate(test_cases):
        input_data = case['input']
        expected = case['expected_output']
        
        # Run the model
        predicted = run_model(
            input_data['trip_duration_days'],
            input_data['miles_traveled'],
            input_data['total_receipts_amount']
        )
        
        # Calculate errors
        absolute_error = abs(predicted - expected)
        error_percentage = (absolute_error / expected) * 100 if expected != 0 else 0
        
        errors.append(absolute_error)
        results.append((i + 1, predicted, expected, absolute_error, error_percentage))
        
        print(f"{i+1:<4} {input_data['trip_duration_days']:<4} {input_data['miles_traveled']:<6} "
              f"{input_data['total_receipts_amount']:<8.2f} {expected:<10.2f} {predicted:<10.2f} "
              f"{absolute_error:<8.2f} {error_percentage:<8.2f}%")
    
    # Calculate mean absolute error
    mae = sum(errors) / len(errors)
    
    # Sort by error percentage to find worst cases
    worst_cases = sorted(results, key=lambda x: x[4], reverse=True)[:5]
    
    return mae, worst_cases

def main():
    # Load test cases
    test_cases = load_test_cases('/Users/seima/8090/top-coder-challenge/public_cases.json', 20)
    
    # Calculate metrics
    mae, worst_cases = calculate_metrics(test_cases)
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Average Error Percentage: {sum(case[4] for case in worst_cases[:len(test_cases)]) / len(test_cases):.2f}%")
    
    print("\nTop 5 Worst Performing Cases:")
    print("-" * 80)
    print(f"{'Case':<4} {'Predicted':<10} {'Expected':<10} {'Abs Error':<10} {'Error %':<10}")
    print("-" * 80)
    
    for case_num, predicted, expected, abs_error, error_pct in worst_cases:
        print(f"{case_num:<4} {predicted:<10.2f} {expected:<10.2f} {abs_error:<10.2f} {error_pct:<10.2f}%")
    
    print("\nDetailed Analysis of Worst Cases:")
    print("-" * 80)
    
    for case_num, predicted, expected, abs_error, error_pct in worst_cases:
        case_data = test_cases[case_num - 1]['input']
        print(f"\nCase {case_num}:")
        print(f"  Input: {case_data['trip_duration_days']} days, {case_data['miles_traveled']} miles, ${case_data['total_receipts_amount']:.2f} receipts")
        print(f"  Expected: ${expected:.2f}")
        print(f"  Predicted: ${predicted:.2f}")
        print(f"  Error: ${abs_error:.2f} ({error_pct:.2f}%)")
        
        # Analysis of why this case might be failing
        daily_miles = case_data['miles_traveled'] / case_data['trip_duration_days']
        daily_spending = case_data['total_receipts_amount'] / case_data['trip_duration_days']
        
        print(f"  Daily miles: {daily_miles:.1f}")
        print(f"  Daily spending: ${daily_spending:.2f}")
        
        if predicted > expected:
            print(f"  Issue: Over-predicting by ${abs_error:.2f}")
        else:
            print(f"  Issue: Under-predicting by ${abs_error:.2f}")

if __name__ == "__main__":
    main()