#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path

def load_public_cases():
    """Load the public test cases"""
    public_cases_path = Path("../../public_cases.json")
    with open(public_cases_path, 'r') as f:
        return json.load(f)

def run_current_model(trip_duration, miles_traveled, receipts_amount):
    """Run the current model and get prediction"""
    try:
        result = subprocess.run(
            ["../../run.sh", str(trip_duration), str(miles_traveled), str(receipts_amount)],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
        else:
            print(f"Error running model: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception running model: {e}")
        return None

def analyze_errors():
    """Analyze the cases with largest errors to find patterns"""
    
    # Load test cases
    public_cases = load_public_cases()
    
    # Calculate predictions and errors for all cases
    results = []
    for i, case in enumerate(public_cases):
        trip_duration = case['input']['trip_duration_days']
        miles_traveled = case['input']['miles_traveled']
        receipts_amount = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        predicted = run_current_model(trip_duration, miles_traveled, receipts_amount)
        
        if predicted is not None:
            error = abs(predicted - expected)
            results.append({
                'case_num': i + 1,
                'trip_duration_days': trip_duration,
                'miles_traveled': miles_traveled,
                'total_receipts_amount': receipts_amount,
                'expected': expected,
                'predicted': predicted,
                'error': error
            })
        
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1} cases...")
    
    print(f"\n=== ERROR ANALYSIS RESULTS ===")
    print(f"Total cases processed: {len(results)}")
    
    # Calculate basic statistics
    errors = [r['error'] for r in results]
    errors.sort()
    
    avg_error = sum(errors) / len(errors)
    median_error = errors[len(errors) // 2]
    max_error = max(errors)
    
    print(f"Average error: ${avg_error:.2f}")
    print(f"Median error: ${median_error:.2f}")
    print(f"Max error: ${max_error:.2f}")
    
    # Count high error cases
    high_error_100 = len([e for e in errors if e > 100])
    high_error_50 = len([e for e in errors if e > 50])
    high_error_10 = len([e for e in errors if e > 10])
    
    print(f"Cases with error > $100: {high_error_100}")
    print(f"Cases with error > $50: {high_error_50}")
    print(f"Cases with error > $10: {high_error_10}")
    
    # Sort by error and get top 20 highest error cases
    results.sort(key=lambda x: x['error'], reverse=True)
    top_errors = results[:20]
    
    print(f"\n=== TOP 20 HIGHEST ERROR CASES ===")
    for row in top_errors:
        print(f"Case {row['case_num']:3d}: {row['trip_duration_days']:2.0f} days, {row['miles_traveled']:6.1f} miles, ${row['total_receipts_amount']:6.2f} receipts")
        print(f"          Expected: ${row['expected']:7.2f}, Predicted: ${row['predicted']:7.2f}, Error: ${row['error']:6.2f}")
    
    # Analyze patterns in high-error cases (top 100)
    print(f"\n=== PATTERN ANALYSIS (Top 100 High-Error Cases) ===")
    high_error_cases = results[:100]
    
    # Check for specific edge cases
    print("\nEDGE CASE ANALYSIS:")
    
    # Trip duration = 1
    duration_1_cases = [c for c in high_error_cases if c['trip_duration_days'] == 1]
    total_duration_1 = len([c for c in results if c['trip_duration_days'] == 1])
    print(f"• Cases with trip_duration_days = 1: {len(duration_1_cases)} / {total_duration_1} total")
    
    # Miles = 0
    miles_0_cases = [c for c in high_error_cases if c['miles_traveled'] == 0]
    total_miles_0 = len([c for c in results if c['miles_traveled'] == 0])
    print(f"• Cases with miles_traveled = 0: {len(miles_0_cases)} / {total_miles_0} total")
    
    # Very high miles
    high_miles_cases = [c for c in high_error_cases if c['miles_traveled'] > 1000]
    total_high_miles = len([c for c in results if c['miles_traveled'] > 1000])
    print(f"• Cases with miles_traveled > 1000: {len(high_miles_cases)} / {total_high_miles} total")
    
    # Low receipts
    low_receipts_cases = [c for c in high_error_cases if c['total_receipts_amount'] < 10]
    total_low_receipts = len([c for c in results if c['total_receipts_amount'] < 10])
    print(f"• Cases with total_receipts_amount < $10: {len(low_receipts_cases)} / {total_low_receipts} total")
    
    # High receipts
    high_receipts_cases = [c for c in high_error_cases if c['total_receipts_amount'] > 500]
    total_high_receipts = len([c for c in results if c['total_receipts_amount'] > 500])
    print(f"• Cases with total_receipts_amount > $500: {len(high_receipts_cases)} / {total_high_receipts} total")
    
    # Look for specific patterns
    print(f"\n=== SPECIFIC PATTERN DETECTION ===")
    
    # Zero miles cases
    zero_miles = [c for c in high_error_cases if c['miles_traveled'] == 0]
    print(f"• Zero miles cases in top errors: {len(zero_miles)}")
    if zero_miles:
        avg_error_zero_miles = sum(c['error'] for c in zero_miles) / len(zero_miles)
        print(f"  Average error for zero miles: ${avg_error_zero_miles:.2f}")
        print(f"  Zero miles cases details:")
        for case in zero_miles[:5]:  # Show first 5
            print(f"    Case {case['case_num']}: {case['trip_duration_days']} days, ${case['total_receipts_amount']:.2f} receipts")
            print(f"      Expected: ${case['expected']:.2f}, Predicted: ${case['predicted']:.2f}, Error: ${case['error']:.2f}")
    
    # Very short trips
    very_short = [c for c in high_error_cases if c['trip_duration_days'] == 1]
    print(f"\n• 1-day trips in top errors: {len(very_short)}")
    if very_short:
        avg_error_short = sum(c['error'] for c in very_short) / len(very_short)
        print(f"  Average error for 1-day trips: ${avg_error_short:.2f}")
        print(f"  1-day trip cases details:")
        for case in very_short[:5]:  # Show first 5
            print(f"    Case {case['case_num']}: {case['miles_traveled']:.1f} miles, ${case['total_receipts_amount']:.2f} receipts")
            print(f"      Expected: ${case['expected']:.2f}, Predicted: ${case['predicted']:.2f}, Error: ${case['error']:.2f}")
    
    # Short trips with high miles
    short_high_miles = [c for c in high_error_cases if c['trip_duration_days'] <= 2 and c['miles_traveled'] > 200]
    print(f"\n• Short trips (≤2 days) with high miles (>200): {len(short_high_miles)}")
    if short_high_miles:
        for case in short_high_miles[:3]:
            print(f"    Case {case['case_num']}: {case['trip_duration_days']} days, {case['miles_traveled']:.1f} miles, ${case['total_receipts_amount']:.2f} receipts")
            print(f"      Expected: ${case['expected']:.2f}, Predicted: ${case['predicted']:.2f}, Error: ${case['error']:.2f}")
    
    return results

if __name__ == "__main__":
    analyze_errors()