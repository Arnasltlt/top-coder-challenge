#!/usr/bin/env python3

import json
import subprocess
import sys
import os

def run_model(trip_duration_days, miles_traveled, total_receipts_amount):
    """Run the current model and return the predicted reimbursement."""
    script_path = "../07_Receipt_Processing_Logic/run.sh"
    try:
        result = subprocess.run([
            "bash", script_path, 
            str(trip_duration_days), 
            str(miles_traveled), 
            str(total_receipts_amount)
        ], capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error running model: {e}")
        return 0

def analyze_worst_cases():
    """Analyze all cases and find the worst performing ones."""
    # Load test cases
    with open("../07_Receipt_Processing_Logic/public_cases.json", "r") as f:
        test_cases = json.load(f)
    
    errors = []
    
    print("Analyzing all test cases...")
    for i, case in enumerate(test_cases):
        input_data = case["input"]
        expected = case["expected_output"]
        
        predicted = run_model(
            input_data["trip_duration_days"],
            input_data["miles_traveled"], 
            input_data["total_receipts_amount"]
        )
        
        error = abs(predicted - expected)
        error_pct = (error / expected * 100) if expected > 0 else 0
        
        errors.append({
            "case_id": i,
            "input": input_data,
            "expected": expected,
            "predicted": predicted,
            "absolute_error": error,
            "error_percentage": error_pct
        })
        
        if i % 100 == 0:
            print(f"Processed {i+1} cases...")
    
    # Sort by absolute error (worst first)
    errors.sort(key=lambda x: x["absolute_error"], reverse=True)
    
    print(f"\nTop 20 worst cases by absolute error:")
    print("=" * 80)
    
    for i, error_case in enumerate(errors[:20]):
        inp = error_case["input"]
        print(f"\nCase #{i+1} (ID: {error_case['case_id']})")
        print(f"  Input: {inp['trip_duration_days']} days, {inp['miles_traveled']} miles, ${inp['total_receipts_amount']}")
        print(f"  Expected: ${error_case['expected']:.2f}")
        print(f"  Predicted: ${error_case['predicted']:.2f}")
        print(f"  Error: ${error_case['absolute_error']:.2f} ({error_case['error_percentage']:.1f}%)")
        
        # Calculate derived metrics for pattern analysis
        daily_spending = inp['total_receipts_amount'] / inp['trip_duration_days']
        miles_per_day = inp['miles_traveled'] / inp['trip_duration_days']
        print(f"  Daily spending: ${daily_spending:.2f}/day")
        print(f"  Miles per day: {miles_per_day:.1f} miles/day")
    
    # Save results for further analysis
    with open("worst_cases_analysis.json", "w") as f:
        json.dump(errors[:50], f, indent=2)
    
    print(f"\n\nSaved top 50 worst cases to worst_cases_analysis.json")
    
    # Quick pattern analysis
    print("\n" + "="*80)
    print("QUICK PATTERN ANALYSIS")
    print("="*80)
    
    worst_20 = errors[:20]
    
    # Duration patterns
    durations = [case["input"]["trip_duration_days"] for case in worst_20]
    print(f"Trip durations in worst 20: {sorted(durations)}")
    print(f"Average duration: {sum(durations)/len(durations):.1f} days")
    
    # Miles patterns
    miles = [case["input"]["miles_traveled"] for case in worst_20]
    print(f"Miles range in worst 20: {min(miles)} to {max(miles)}")
    print(f"Average miles: {sum(miles)/len(miles):.1f}")
    
    # Receipt patterns
    receipts = [case["input"]["total_receipts_amount"] for case in worst_20]
    print(f"Receipt amounts range: ${min(receipts):.2f} to ${max(receipts):.2f}")
    print(f"Average receipts: ${sum(receipts)/len(receipts):.2f}")
    
    # Daily spending patterns
    daily_spendings = [case["input"]["total_receipts_amount"] / case["input"]["trip_duration_days"] for case in worst_20]
    print(f"Daily spending range: ${min(daily_spendings):.2f} to ${max(daily_spendings):.2f} per day")
    print(f"Average daily spending: ${sum(daily_spendings)/len(daily_spendings):.2f} per day")

if __name__ == "__main__":
    analyze_worst_cases()