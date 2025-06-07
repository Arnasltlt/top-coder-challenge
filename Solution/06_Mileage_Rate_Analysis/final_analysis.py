#!/usr/bin/env python3
import json
import statistics

def final_analysis():
    # Read the JSON file
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("=== FINAL MILEAGE RATE ANALYSIS REPORT ===")
    print()
    
    # Extract representative examples for different mileage ranges
    print("=== REPRESENTATIVE INPUT/OUTPUT EXAMPLES ===")
    
    # Group by mileage ranges and select clean examples (low receipts to isolate mileage effect)
    examples = []
    
    # Look for cases with low receipts to isolate base structure
    low_receipt_cases = [case for case in data if case['input']['total_receipts_amount'] < 50.0]
    low_receipt_cases.sort(key=lambda x: x['input']['miles_traveled'])
    
    print("Selected examples with low receipts (< $50) to isolate mileage component:")
    print("Days | Miles | Receipts | Output | Pure Base+Mileage")
    print("-" * 65)
    
    selected_examples = []
    mile_ranges = [(0, 50), (51, 100), (101, 200), (201, 400), (401, 600), (601, 800), (801, 1000)]
    
    for min_miles, max_miles in mile_ranges:
        range_cases = [case for case in low_receipt_cases 
                      if min_miles <= case['input']['miles_traveled'] <= max_miles]
        
        if range_cases:
            # Take first case from this range
            case = range_cases[0]
            days = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            output = case['expected_output']
            base_plus_mileage = output - receipts
            
            selected_examples.append((days, miles, receipts, output, base_plus_mileage))
            print(f"{days:4d} | {miles:5.0f} | ${receipts:7.2f} | ${output:7.2f} | ${base_plus_mileage:7.2f}")
    
    # Calculate implied rates using the current linear model assumptions
    print(f"\n=== ANALYSIS OF MILEAGE COMPONENT ===")
    print("Current linear model suggests: reimbursement = 50.05*days + 0.446*miles + 0.383*receipts + 266.71")
    print()
    
    # Test this model on our clean examples
    days_coeff = 50.050486
    miles_coeff = 0.445645
    receipts_coeff = 0.382861
    intercept = 266.707681
    
    print("Testing linear model on clean examples:")
    print("Days | Miles | Receipts | Actual | Predicted | Error | Implied Rate/Mile")
    print("-" * 80)
    
    for days, miles, receipts, actual, base_plus_mileage in selected_examples:
        predicted = days_coeff * days + miles_coeff * miles + receipts_coeff * receipts + intercept
        error = predicted - actual
        
        # Calculate what the effective per-mile rate would be if we subtract a reasonable daily base
        # Let's assume a daily base of $60 and see what mileage rate that implies
        assumed_daily_base = 60
        mileage_component = base_plus_mileage - (days * assumed_daily_base)
        implied_rate = mileage_component / miles if miles > 0 else 0
        
        print(f"{days:4d} | {miles:5.0f} | ${receipts:7.2f} | ${actual:7.2f} | ${predicted:8.2f} | "
              f"${error:6.2f} | ${implied_rate:8.4f}")
    
    # Look for patterns in different scenarios
    print(f"\n=== MILEAGE RATE PATTERNS BY SCENARIO ===")
    
    # Analyze 1-day trips with minimal receipts (easiest to isolate mileage)
    one_day_minimal = [case for case in data 
                      if case['input']['trip_duration_days'] == 1 
                      and case['input']['total_receipts_amount'] < 20.0]
    
    if one_day_minimal:
        print("1-day trips with minimal receipts:")
        print("Miles | Receipts | Output | Mileage Component* | Implied Rate/Mile")
        print("*Assuming $70 base daily allowance")
        print("-" * 70)
        
        one_day_minimal.sort(key=lambda x: x['input']['miles_traveled'])
        
        for case in one_day_minimal[:10]:
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            output = case['expected_output']
            
            # Assume $70 daily base for 1-day trips
            mileage_component = output - receipts - 70
            rate = mileage_component / miles if miles > 0 else 0
            
            print(f"{miles:5.0f} | ${receipts:7.2f} | ${output:7.2f} | ${mileage_component:8.2f} | ${rate:8.4f}")
    
    # Look at high mileage cases for caps
    print(f"\n=== HIGH MILEAGE ANALYSIS (>600 miles) ===")
    
    high_mileage = [case for case in data if case['input']['miles_traveled'] > 600]
    high_mileage.sort(key=lambda x: x['input']['miles_traveled'])
    
    print("Miles | Days | Receipts | Output | Effective Rate/Mile**")
    print("**Using linear model rate as baseline")
    print("-" * 60)
    
    for case in high_mileage[:10]:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        # Calculate what rate would be needed to match actual output
        # Using the linear model's other components
        base_component = days_coeff * days + receipts_coeff * receipts + intercept
        mileage_component = output - base_component
        effective_rate = mileage_component / miles if miles > 0 else 0
        
        print(f"{miles:5.0f} | {days:4d} | ${receipts:7.2f} | ${output:7.2f} | ${effective_rate:8.4f}")
    
    print(f"\n=== RECOMMENDATIONS FOR MILEAGE CALCULATION ===")
    
    # Calculate average rates for different ranges
    low_mile_rates = []
    high_mile_rates = []
    
    for case in data:
        if case['input']['total_receipts_amount'] < 50:  # Low receipt cases
            days = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            output = case['expected_output']
            
            # Use linear model for other components
            other_component = days_coeff * days + receipts_coeff * receipts + intercept
            mileage_component = output - other_component
            rate = mileage_component / miles if miles > 0 else 0
            
            if miles <= 200:
                low_mile_rates.append(rate)
            elif miles > 500:
                high_mile_rates.append(rate)
    
    if low_mile_rates and high_mile_rates:
        avg_low = sum(low_mile_rates) / len(low_mile_rates)
        avg_high = sum(high_mile_rates) / len(high_mile_rates)
        
        print(f"1. Average effective rate for low mileage (≤200 miles): ${avg_low:.4f} per mile")
        print(f"2. Average effective rate for high mileage (>500 miles): ${avg_high:.4f} per mile")
        print(f"3. Current linear model uses: ${miles_coeff:.4f} per mile")
        
        if abs(avg_low - avg_high) > 0.1:
            print(f"4. SIGNIFICANT DIFFERENCE detected - suggests tiered or capped structure")
        else:
            print(f"4. Rates are similar - linear model may be reasonable approximation")
    
    print(f"\n5. Based on analysis, recommended approach:")
    print(f"   - Use ${miles_coeff:.3f} per mile as baseline rate")
    print(f"   - Consider implementing caps or tiers if accuracy requirements are high")
    print(f"   - Current linear model has average error of ~$175, may be acceptable")

if __name__ == "__main__":
    final_analysis()