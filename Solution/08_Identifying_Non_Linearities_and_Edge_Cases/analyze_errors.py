#!/usr/bin/env python3
"""
Script to identify the top 20 worst-performing cases with the current best model.
This will help us identify patterns in the remaining errors for edge case analysis.
"""

import json
import subprocess
import sys
from typing import List, Tuple, Dict

def load_test_cases(json_file: str) -> List[Dict]:
    """Load test cases from JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)

def run_model(run_script: str, days: int, miles: int, receipts: float) -> float:
    """Run the current model and return the predicted reimbursement."""
    try:
        result = subprocess.run(
            ['bash', run_script, str(days), str(miles), str(receipts)],
            capture_output=True,
            text=True,
            check=True
        )
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Error running model for case {days}, {miles}, {receipts}: {e}")
        return 0.0

def analyze_worst_cases(test_cases: List[Dict], run_script: str, top_n: int = 20) -> List[Tuple[Dict, float, float]]:
    """Analyze test cases and return the worst performing ones."""
    errors = []
    
    for i, case in enumerate(test_cases):
        inputs = case['input']
        expected = case['expected_output']
        
        days = inputs['trip_duration_days']
        miles = inputs['miles_traveled'] 
        receipts = inputs['total_receipts_amount']
        
        predicted = run_model(run_script, days, miles, receipts)
        absolute_error = abs(predicted - expected)
        
        errors.append((case, predicted, absolute_error))
        
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1} cases...")
    
    # Sort by absolute error (worst first)
    errors.sort(key=lambda x: x[2], reverse=True)
    
    return errors[:top_n]

def print_analysis(worst_cases: List[Tuple[Dict, float, float]]):
    """Print detailed analysis of the worst cases."""
    print(f"\n=== TOP {len(worst_cases)} WORST-PERFORMING CASES ===\n")
    
    for i, (case, predicted, error) in enumerate(worst_cases, 1):
        inputs = case['input']
        expected = case['expected_output']
        
        print(f"Case #{i} - Error: ${error:.2f}")
        print(f"  Days: {inputs['trip_duration_days']}")
        print(f"  Miles: {inputs['miles_traveled']}")
        print(f"  Receipts: ${inputs['total_receipts_amount']:.2f}")
        print(f"  Expected: ${expected:.2f}")
        print(f"  Predicted: ${predicted:.2f}")
        print(f"  Daily Spending: ${inputs['total_receipts_amount'] / inputs['trip_duration_days']:.2f}")
        print()
    
    # Analyze patterns
    print("=== PATTERN ANALYSIS ===")
    
    # Duration analysis
    durations = [case[0]['input']['trip_duration_days'] for case in worst_cases]
    long_trips = sum(1 for d in durations if d > 10)
    print(f"Long trips (>10 days): {long_trips}/{len(worst_cases)} ({100*long_trips/len(worst_cases):.1f}%)")
    
    # Mileage analysis
    mileages = [case[0]['input']['miles_traveled'] for case in worst_cases]
    high_mileage = sum(1 for m in mileages if m > 500)
    print(f"High mileage (>500 miles): {high_mileage}/{len(worst_cases)} ({100*high_mileage/len(worst_cases):.1f}%)")
    
    # Receipt analysis
    receipts = [case[0]['input']['total_receipts_amount'] for case in worst_cases]
    high_receipts = sum(1 for r in receipts if r > 1000)
    print(f"High receipts (>$1000): {high_receipts}/{len(worst_cases)} ({100*high_receipts/len(worst_cases):.1f}%)")
    
    # Daily spending analysis
    daily_spending = [case[0]['input']['total_receipts_amount'] / case[0]['input']['trip_duration_days'] for case in worst_cases]
    very_high_spending = sum(1 for d in daily_spending if d > 150)
    print(f"Very high daily spending (>$150/day): {very_high_spending}/{len(worst_cases)} ({100*very_high_spending/len(worst_cases):.1f}%)")
    
    print(f"\nAvg duration: {sum(durations)/len(durations):.1f} days")
    print(f"Avg mileage: {sum(mileages)/len(mileages):.1f} miles") 
    print(f"Avg receipts: ${sum(receipts)/len(receipts):.2f}")
    print(f"Avg daily spending: ${sum(daily_spending)/len(daily_spending):.2f}")

def main():
    # Use the current best model from Receipt Processing Logic
    run_script = "/Users/seima/8090/top-coder-challenge/Solution/07_Receipt_Processing_Logic/run.sh"
    test_cases_file = "/Users/seima/8090/top-coder-challenge/Solution/07_Receipt_Processing_Logic/public_cases.json"
    
    print("Loading test cases...")
    test_cases = load_test_cases(test_cases_file)
    print(f"Loaded {len(test_cases)} test cases")
    
    print("Analyzing worst-performing cases...")
    worst_cases = analyze_worst_cases(test_cases, run_script)
    
    print_analysis(worst_cases)

if __name__ == "__main__":
    main()