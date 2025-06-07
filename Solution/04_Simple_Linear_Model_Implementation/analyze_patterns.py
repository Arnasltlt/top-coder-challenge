#!/usr/bin/env python3

import json

def analyze_data(filename):
    """Analyze patterns in the data"""
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Look at specific patterns
    single_day_trips = []
    multi_day_trips = []
    
    for case in data:
        input_data = case['input']
        days = input_data['trip_duration_days']
        miles = input_data['miles_traveled']
        receipts = input_data['total_receipts_amount']
        output = case['expected_output']
        
        if days == 1:
            single_day_trips.append((days, miles, receipts, output))
        else:
            multi_day_trips.append((days, miles, receipts, output))
    
    print(f"Single day trips: {len(single_day_trips)}")
    print(f"Multi day trips: {len(multi_day_trips)}")
    
    # Analyze single day trips to estimate per-mile rate
    print("\nAnalyzing single-day trips:")
    for i in range(min(20, len(single_day_trips))):
        days, miles, receipts, output = single_day_trips[i]
        per_mile_estimate = (output - receipts) / miles if miles > 0 else 0
        print(f"Days={days}, Miles={miles}, Receipts=${receipts:.2f}, Output=${output:.2f}, $/mile≈{per_mile_estimate:.2f}")
    
    # Look for patterns in per-day rates
    print("\nAnalyzing multi-day trips:")
    for i in range(min(20, len(multi_day_trips))):
        days, miles, receipts, output = multi_day_trips[i]
        per_day_estimate = (output - receipts - miles*0.5) / days if days > 0 else 0
        print(f"Days={days}, Miles={miles}, Receipts=${receipts:.2f}, Output=${output:.2f}, $/day≈{per_day_estimate:.2f}")
    
    # Try to find consistent patterns
    print("\nLooking for consistent rates...")
    
    # Check if there's a base rate per day
    base_rates = []
    for case in data:
        input_data = case['input']
        days = input_data['trip_duration_days']
        miles = input_data['miles_traveled']
        receipts = input_data['total_receipts_amount']
        output = case['expected_output']
        
        # Assume $0.50 per mile (common government rate)
        estimated_base = (output - miles*0.50 - receipts) / days
        base_rates.append(estimated_base)
    
    # Calculate average base rate
    avg_base_rate = sum(base_rates) / len(base_rates)
    print(f"Average base rate per day (assuming $0.50/mile): ${avg_base_rate:.2f}")
    
    # Test this hypothesis
    print(f"\nTesting hypothesis: reimbursement = {avg_base_rate:.2f} * days + 0.50 * miles + 1.0 * receipts")
    
    total_error = 0
    for i, case in enumerate(data[:10]):
        input_data = case['input']
        days = input_data['trip_duration_days']
        miles = input_data['miles_traveled']
        receipts = input_data['total_receipts_amount']
        actual = case['expected_output']
        
        predicted = avg_base_rate * days + 0.50 * miles + 1.0 * receipts
        error = abs(predicted - actual)
        total_error += error
        
        print(f"Case {i+1}: Predicted=${predicted:.2f}, Actual=${actual:.2f}, Error=${error:.2f}")
    
    avg_error = total_error / 10
    print(f"Average error on first 10 cases: ${avg_error:.2f}")

if __name__ == "__main__":
    analyze_data('../../public_cases.json')