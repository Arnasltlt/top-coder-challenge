#!/usr/bin/env python3
import json
import statistics

def test_current_model():
    # Read the JSON file
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("=== TESTING CURRENT LINEAR MODEL ===")
    print("Formula: reimbursement = 50.050486 * days + 0.445645 * miles + 0.382861 * receipts + 266.707681")
    print()
    
    # Current model coefficients
    days_coeff = 50.050486
    miles_coeff = 0.445645
    receipts_coeff = 0.382861
    intercept = 266.707681
    
    errors = []
    test_cases = []
    
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        # Calculate prediction using current model
        predicted = days_coeff * days + miles_coeff * miles + receipts_coeff * receipts + intercept
        error = abs(predicted - actual)
        errors.append(error)
        
        test_cases.append({
            'days': days,
            'miles': miles,
            'receipts': receipts,
            'actual': actual,
            'predicted': predicted,
            'error': error
        })
    
    avg_error = sum(errors) / len(errors)
    median_error = statistics.median(errors)
    max_error = max(errors)
    
    print(f"Total test cases: {len(data)}")
    print(f"Average error: ${avg_error:.2f}")
    print(f"Median error: ${median_error:.2f}")
    print(f"Maximum error: ${max_error:.2f}")
    
    # Show some examples
    print(f"\n=== SAMPLE PREDICTIONS ===")
    print("Days | Miles | Receipts | Actual | Predicted | Error")
    print("-" * 65)
    
    # Show first 20 cases
    for case in test_cases[:20]:
        print(f"{case['days']:4d} | {case['miles']:5.0f} | ${case['receipts']:7.2f} | "
              f"${case['actual']:7.2f} | ${case['predicted']:8.2f} | ${case['error']:6.2f}")
    
    # Analyze mileage component specifically
    print(f"\n=== MILEAGE RATE ANALYSIS ===")
    print(f"Current model uses ${miles_coeff:.6f} per mile")
    print()
    
    # Group cases by mile ranges to see if the rate varies
    mile_ranges = [
        (0, 100),
        (101, 200),
        (201, 400),
        (401, 600),
        (601, 800),
        (801, 1000)
    ]
    
    print("Analyzing model accuracy by mileage range:")
    print("Range     | Cases | Avg Error | Median Error | Max Error")
    print("-" * 60)
    
    for min_miles, max_miles in mile_ranges:
        range_cases = [case for case in test_cases 
                      if min_miles <= case['miles'] <= max_miles]
        
        if range_cases:
            range_errors = [case['error'] for case in range_cases]
            avg_err = sum(range_errors) / len(range_errors)
            med_err = statistics.median(range_errors)
            max_err = max(range_errors)
            
            print(f"{min_miles:3d}-{max_miles:3d}   | {len(range_cases):5d} | ${avg_err:8.2f} | "
                  f"${med_err:9.2f} | ${max_err:8.2f}")
    
    # Look at cases with largest errors to understand where model fails
    print(f"\n=== CASES WITH LARGEST ERRORS ===")
    test_cases.sort(key=lambda x: x['error'], reverse=True)
    
    print("Days | Miles | Receipts | Actual | Predicted | Error")
    print("-" * 65)
    
    for case in test_cases[:15]:  # Top 15 worst predictions
        print(f"{case['days']:4d} | {case['miles']:5.0f} | ${case['receipts']:7.2f} | "
              f"${case['actual']:7.2f} | ${case['predicted']:8.2f} | ${case['error']:6.2f}")
    
    # Look at cases with smallest errors
    print(f"\n=== CASES WITH SMALLEST ERRORS ===")
    test_cases.sort(key=lambda x: x['error'])
    
    print("Days | Miles | Receipts | Actual | Predicted | Error")
    print("-" * 65)
    
    for case in test_cases[:15]:  # Top 15 best predictions
        print(f"{case['days']:4d} | {case['miles']:5.0f} | ${case['receipts']:7.2f} | "
              f"${case['actual']:7.2f} | ${case['predicted']:8.2f} | ${case['error']:6.2f}")
    
    # Analyze if there are any patterns in the errors
    print(f"\n=== ERROR PATTERN ANALYSIS ===")
    
    # Check if errors correlate with specific input ranges
    high_mileage_errors = [case['error'] for case in test_cases if case['miles'] > 500]
    low_mileage_errors = [case['error'] for case in test_cases if case['miles'] <= 100]
    
    if high_mileage_errors and low_mileage_errors:
        print(f"High mileage (>500 miles) average error: ${sum(high_mileage_errors)/len(high_mileage_errors):.2f}")
        print(f"Low mileage (<=100 miles) average error: ${sum(low_mileage_errors)/len(low_mileage_errors):.2f}")
    
    long_trip_errors = [case['error'] for case in test_cases if case['days'] > 7]
    short_trip_errors = [case['error'] for case in test_cases if case['days'] <= 3]
    
    if long_trip_errors and short_trip_errors:
        print(f"Long trips (>7 days) average error: ${sum(long_trip_errors)/len(long_trip_errors):.2f}")
        print(f"Short trips (<=3 days) average error: ${sum(short_trip_errors)/len(short_trip_errors):.2f}")

if __name__ == "__main__":
    test_current_model()