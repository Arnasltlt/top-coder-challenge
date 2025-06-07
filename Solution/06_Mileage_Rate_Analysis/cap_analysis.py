#!/usr/bin/env python3
import json
from collections import defaultdict

def cap_analysis():
    # Read the JSON file
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("=== ANALYZING FOR MILEAGE CAPS OR TIERS ===")
    
    # Sort all cases by miles traveled to look for patterns
    all_cases = []
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        # Calculate effective mileage component (assuming 65 base daily rate)
        base_daily = 65
        estimated_daily_component = days * base_daily
        mileage_component = output - receipts - estimated_daily_component
        effective_per_mile = mileage_component / miles if miles > 0 else 0
        
        all_cases.append({
            'days': days,
            'miles': miles,
            'receipts': receipts,
            'output': output,
            'mileage_component': mileage_component,
            'effective_per_mile': effective_per_mile
        })
    
    # Sort by miles
    all_cases.sort(key=lambda x: x['miles'])
    
    print("Analyzing effective per-mile rates across different mileage ranges:")
    print("(Assuming base daily rate of $65)")
    print()
    
    # Group by mile ranges
    ranges = [
        (0, 50),
        (51, 100),
        (101, 200),
        (201, 300),
        (301, 400),
        (401, 500),
        (501, 600),
        (601, 700),
        (701, 800),
        (801, 900),
        (901, 1000)
    ]
    
    for min_miles, max_miles in ranges:
        range_cases = [case for case in all_cases 
                      if min_miles <= case['miles'] <= max_miles]
        
        if range_cases:
            rates = [case['effective_per_mile'] for case in range_cases]
            avg_rate = sum(rates) / len(rates)
            min_rate = min(rates)
            max_rate = max(rates)
            
            print(f"Miles {min_miles:3d}-{max_miles:3d}: {len(range_cases):3d} cases, "
                  f"avg rate: ${avg_rate:6.3f}, range: ${min_rate:6.3f} to ${max_rate:6.3f}")
    
    # Look for specific patterns - maybe there's a cap at certain mile amounts
    print(f"\n=== DETAILED ANALYSIS OF HIGH MILEAGE CASES ===")
    
    high_mileage = [case for case in all_cases if case['miles'] > 400]
    high_mileage.sort(key=lambda x: x['miles'])
    
    print("Miles | Days | Receipts | Output | Mileage Component | Per-Mile Rate")
    print("-" * 75)
    
    for case in high_mileage[:25]:  # First 25 high mileage cases
        print(f"{case['miles']:5.0f} | {case['days']:4d} | ${case['receipts']:7.2f} | "
              f"${case['output']:7.2f} | ${case['mileage_component']:8.2f} | ${case['effective_per_mile']:8.4f}")
    
    # Test if there's a maximum mileage reimbursement
    print(f"\n=== TESTING FOR MILEAGE CAPS ===")
    
    # Test different cap amounts
    for cap_amount in [200, 250, 300, 350, 400, 450, 500]:
        print(f"\nTesting mileage cap at ${cap_amount}:")
        
        errors = []
        base_daily = 65
        per_mile_rate = 0.67  # Approximate from earlier analysis
        
        for case in all_cases[:100]:  # Test on first 100 cases
            days = case['days']
            miles = case['miles']
            receipts = case['receipts']
            actual_output = case['output']
            
            # Calculate with cap
            mileage_reimbursement = min(miles * per_mile_rate, cap_amount)
            predicted_output = (days * base_daily) + mileage_reimbursement + receipts
            
            error = abs(predicted_output - actual_output)
            errors.append(error)
        
        avg_error = sum(errors) / len(errors)
        print(f"  Average error with ${cap_amount} cap: ${avg_error:.2f}")
    
    # Test tiered rates
    print(f"\n=== TESTING TIERED RATES ===")
    
    # Test: First X miles at rate1, remaining at rate2
    for first_mile_limit in [200, 300, 400, 500]:
        for rate1_cents in [70, 80, 90]:
            for rate2_cents in [20, 30, 40, 50]:
                rate1 = rate1_cents / 100.0
                rate2 = rate2_cents / 100.0
                
                errors = []
                base_daily = 65
                
                for case in all_cases[:50]:  # Test on subset
                    days = case['days']
                    miles = case['miles']
                    receipts = case['receipts']
                    actual_output = case['output']
                    
                    # Calculate tiered mileage
                    if miles <= first_mile_limit:
                        mileage_reimbursement = miles * rate1
                    else:
                        mileage_reimbursement = (first_mile_limit * rate1) + ((miles - first_mile_limit) * rate2)
                    
                    predicted_output = (days * base_daily) + mileage_reimbursement + receipts
                    error = abs(predicted_output - actual_output)
                    errors.append(error)
                
                avg_error = sum(errors) / len(errors)
                
                if avg_error < 20:  # Only show promising results
                    print(f"  First {first_mile_limit} miles @ ${rate1:.2f}, rest @ ${rate2:.2f}: avg error ${avg_error:.2f}")

if __name__ == "__main__":
    cap_analysis()