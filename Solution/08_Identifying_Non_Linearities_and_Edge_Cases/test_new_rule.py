#!/usr/bin/env python3

import json
import subprocess

def run_model(script_path, trip_duration_days, miles_traveled, total_receipts_amount):
    """Run a model script and return the predicted reimbursement."""
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

def test_new_rule():
    """Test the new universal long trip penalty rule."""
    
    # Load worst cases
    with open("worst_cases_analysis.json", "r") as f:
        worst_cases = json.load(f)
    
    original_script = "../07_Receipt_Processing_Logic/run.sh"
    new_script = "./run_test_v2.sh"
    
    print("TESTING NEW UNIVERSAL LONG TRIP PENALTY RULE")
    print("="*70)
    print("Comparing original vs new rule on top 10 worst cases:")
    print()
    
    improvements = 0
    total_cases = 10
    
    for i, case in enumerate(worst_cases[:total_cases]):
        inp = case["input"]
        expected = case["expected"]
        
        # Run both models
        original_pred = run_model(original_script, inp["trip_duration_days"], inp["miles_traveled"], inp["total_receipts_amount"])
        new_pred = run_model(new_script, inp["trip_duration_days"], inp["miles_traveled"], inp["total_receipts_amount"])
        
        original_error = abs(original_pred - expected)
        new_error = abs(new_pred - expected)
        
        improvement = original_error - new_error
        
        print(f"Case #{i+1} ({inp['trip_duration_days']} days, {inp['miles_traveled']} miles, ${inp['total_receipts_amount']})")
        print(f"  Expected:     ${expected:.2f}")
        print(f"  Original:     ${original_pred:.2f} (error: ${original_error:.2f})")
        print(f"  New Rule:     ${new_pred:.2f} (error: ${new_error:.2f})")
        print(f"  Improvement:  ${improvement:.2f} {'✓' if improvement > 0 else '✗'}")
        print()
        
        if improvement > 0:
            improvements += 1
    
    print(f"SUMMARY: {improvements}/{total_cases} cases improved")
    print(f"Success rate: {improvements/total_cases*100:.1f}%")
    
    return improvements > total_cases / 2  # Return True if more than half improved

if __name__ == "__main__":
    success = test_new_rule()
    if success:
        print("\n✓ NEW RULE SHOWS PROMISE - Testing on full dataset...")
    else:
        print("\n✗ NEW RULE NOT EFFECTIVE - Need different approach")