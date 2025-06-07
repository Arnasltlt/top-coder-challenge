#!/usr/bin/env python3

import json
import subprocess

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

def analyze_case(case_num, input_data, expected, actual):
    """Analyze a single test case in detail"""
    days = input_data['trip_duration_days']
    miles = input_data['miles_traveled']
    receipts = input_data['total_receipts_amount']
    
    # Calculate what our model does step by step
    base_per_diem = days * 100
    base_mileage = miles * 0.50
    base_total = base_per_diem + base_mileage
    
    daily_spending = receipts / days
    
    # Determine receipt processing logic
    if daily_spending < 20:
        receipt_contribution = receipts * 0.5
        logic = "Very low spending (50% of receipts)"
    elif daily_spending < 50:
        receipt_contribution = receipts * 0.7
        logic = "Low spending (70% of receipts)"
    elif daily_spending < 120:
        receipt_contribution = receipts
        logic = "Medium spending (100% of receipts)"
    else:
        capped_amount = days * 120
        if receipts > capped_amount:
            excess = receipts - capped_amount
            receipt_contribution = capped_amount + excess * 0.3
            logic = f"High spending (cap at ${capped_amount}, excess at 30%)"
        else:
            receipt_contribution = receipts
            logic = "High spending range but under cap (100% of receipts)"
    
    calculated_total = base_total + receipt_contribution
    error = actual - expected
    error_pct = (error / expected) * 100 if expected != 0 else 0
    
    print(f"\nCase {case_num}:")
    print(f"  Input: {days} days, {miles} miles, ${receipts:.2f} receipts")
    print(f"  Daily spending: ${daily_spending:.2f}")
    print(f"  Base calculation: ${base_per_diem} (per diem) + ${base_mileage} (mileage) = ${base_total}")
    print(f"  Receipt logic: {logic}")
    print(f"  Receipt contribution: ${receipt_contribution:.2f}")
    print(f"  Our calculation: ${calculated_total:.2f}")
    print(f"  Actual output: ${actual:.2f}")
    print(f"  Expected: ${expected:.2f}")
    print(f"  Error: ${error:.2f} ({error_pct:.1f}%)")

def main():
    # Load test cases
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    print("Detailed Analysis of First 10 Cases:")
    print("=" * 80)
    
    for i, case in enumerate(test_cases[:10]):
        input_data = case['input']
        expected = case['expected_output']
        
        # Run the model
        actual = run_model(
            input_data['trip_duration_days'],
            input_data['miles_traveled'],
            input_data['total_receipts_amount']
        )
        
        if actual is not None:
            analyze_case(i+1, input_data, expected, actual)

if __name__ == "__main__":
    main()