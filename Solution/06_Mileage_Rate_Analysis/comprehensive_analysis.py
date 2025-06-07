#!/usr/bin/env python3
import json
from collections import defaultdict
import statistics

def comprehensive_analysis():
    # Read the JSON file
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("=== COMPREHENSIVE MILEAGE RATE ANALYSIS ===")
    
    # Look for cases with low receipts across all trip durations
    low_receipt_cases = []
    for case in data:
        if case['input']['total_receipts_amount'] < 20.0:  # Increased threshold
            low_receipt_cases.append(case)
    
    print(f"Found {len(low_receipt_cases)} cases with receipts < $20")
    
    # Group by trip duration
    by_days = defaultdict(list)
    for case in low_receipt_cases:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        non_receipt = output - receipts
        
        by_days[days].append({
            'miles': miles,
            'receipts': receipts,
            'output': output,
            'non_receipt': non_receipt
        })
    
    # Print summary by days
    print(f"\nBreakdown by trip duration (low receipt cases):")
    for days in sorted(by_days.keys()):
        print(f"  {days} days: {len(by_days[days])} cases")
    
    # Test hypothesis: Output = (Days * Base_Daily) + (Miles * Rate) + Receipts
    print(f"\n=== TESTING HYPOTHESIS: Output = (Days * Base) + (Miles * Rate) + Receipts ===")
    
    # Try different base daily amounts
    best_fit = None
    best_error = float('inf')
    
    for base_daily in range(50, 81, 5):  # Test 50, 55, 60, 65, 70, 75, 80
        for mileage_rate_cents in range(50, 300, 10):  # Test 0.50 to 2.90 per mile
            mileage_rate = mileage_rate_cents / 100.0
            
            errors = []
            for case in low_receipt_cases[:50]:  # Test on first 50 cases
                days = case['input']['trip_duration_days']
                miles = case['input']['miles_traveled']
                receipts = case['input']['total_receipts_amount']
                actual_output = case['expected_output']
                
                predicted_output = (days * base_daily) + (miles * mileage_rate) + receipts
                error = abs(predicted_output - actual_output)
                errors.append(error)
            
            avg_error = sum(errors) / len(errors) if errors else float('inf')
            
            if avg_error < best_error:
                best_error = avg_error
                best_fit = (base_daily, mileage_rate)
    
    print(f"Best fit: Base daily = ${best_fit[0]}, Mileage rate = ${best_fit[1]:.2f}/mile")
    print(f"Average error: ${best_error:.2f}")
    
    # Test the best fit on more cases
    base_daily, mileage_rate = best_fit
    print(f"\n=== TESTING BEST FIT ON SAMPLE CASES ===")
    print(f"Formula: Output = (Days * ${base_daily}) + (Miles * ${mileage_rate:.2f}) + Receipts")
    print()
    print("Days | Miles | Receipts | Actual | Predicted | Error")
    print("-" * 65)
    
    test_cases = low_receipt_cases[:20]
    total_error = 0
    
    for case in test_cases:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        predicted = (days * base_daily) + (miles * mileage_rate) + receipts
        error = abs(predicted - actual)
        total_error += error
        
        print(f"{days:4d} | {miles:5.0f} | ${receipts:7.2f} | ${actual:7.2f} | ${predicted:8.2f} | ${error:6.2f}")
    
    avg_error = total_error / len(test_cases)
    print(f"\nAverage error on test cases: ${avg_error:.2f}")
    
    # Let's also test with some higher receipt cases to validate
    print(f"\n=== VALIDATION ON HIGHER RECEIPT CASES ===")
    high_receipt_cases = [case for case in data if case['input']['total_receipts_amount'] > 100.0][:10]
    
    print("Days | Miles | Receipts | Actual | Predicted | Error")
    print("-" * 65)
    
    validation_error = 0
    for case in high_receipt_cases:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        predicted = (days * base_daily) + (miles * mileage_rate) + receipts
        error = abs(predicted - actual)
        validation_error += error
        
        print(f"{days:4d} | {miles:5.0f} | ${receipts:7.2f} | ${actual:7.2f} | ${predicted:8.2f} | ${error:6.2f}")
    
    avg_validation_error = validation_error / len(high_receipt_cases)
    print(f"\nAverage error on validation cases: ${avg_validation_error:.2f}")
    
    # Check for any special handling of first miles or caps
    print(f"\n=== CHECKING FOR TIERED RATES OR CAPS ===")
    
    # Look at high mileage cases
    high_mileage_cases = [case for case in data if case['input']['miles_traveled'] > 500][:10]
    
    print("Testing on high mileage cases (>500 miles):")
    print("Days | Miles | Receipts | Actual | Predicted | Error | Per-Mile-Effective")
    print("-" * 85)
    
    for case in high_mileage_cases:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        predicted = (days * base_daily) + (miles * mileage_rate) + receipts
        error = abs(predicted - actual)
        
        # Calculate effective per-mile rate
        non_receipt_component = actual - receipts
        effective_daily_component = days * base_daily
        effective_mileage_component = non_receipt_component - effective_daily_component
        effective_per_mile = effective_mileage_component / miles if miles > 0 else 0
        
        print(f"{days:4d} | {miles:5.0f} | ${receipts:7.2f} | ${actual:7.2f} | ${predicted:8.2f} | ${error:6.2f} | ${effective_per_mile:8.4f}")

if __name__ == "__main__":
    comprehensive_analysis()