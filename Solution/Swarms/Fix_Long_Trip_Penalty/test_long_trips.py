#!/usr/bin/env python3
"""
Test script to identify problematic long trip cases (12+ days)
"""
import json
import subprocess
import sys

def test_case(days, miles, receipts):
    """Test a single case using our run.sh script"""
    try:
        result = subprocess.run(['./run.sh', str(days), str(miles), str(receipts)], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            return float(result.stdout.strip())
        else:
            print(f"Error running case: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    # Load test cases
    with open('public_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    print("LONG TRIP ANALYSIS (12+ days)")
    print("="*60)
    
    long_trip_cases = []
    for i, case in enumerate(test_cases):
        inp = case['input']
        days = inp['trip_duration_days']
        
        if days >= 12:
            miles = inp['miles_traveled']
            receipts = inp['total_receipts_amount']
            expected = case['expected_output']
            
            predicted = test_case(days, miles, receipts)
            if predicted is not None:
                error = abs(predicted - expected)
                error_pct = (error / expected) * 100 if expected > 0 else 0
                
                long_trip_cases.append({
                    'case_id': i,
                    'days': days,
                    'miles': miles,
                    'receipts': receipts,
                    'expected': expected,
                    'predicted': predicted,
                    'error': error,
                    'error_pct': error_pct
                })
    
    # Sort by error (worst first)
    long_trip_cases.sort(key=lambda x: x['error'], reverse=True)
    
    print(f"Found {len(long_trip_cases)} cases with 12+ days")
    print(f"Top 10 worst performing long trip cases:")
    print()
    
    total_error = 0
    for i, case in enumerate(long_trip_cases[:10]):
        print(f"Case {case['case_id']:3d}: {case['days']:2.0f} days, {case['miles']:4.0f} miles, ${case['receipts']:5.0f} receipts")
        print(f"    Expected: ${case['expected']:7.2f}, Predicted: ${case['predicted']:7.2f}, Error: ${case['error']:6.2f} ({case['error_pct']:5.1f}%)")
        total_error += case['error']
        print()
    
    if long_trip_cases:
        avg_error = sum(case['error'] for case in long_trip_cases) / len(long_trip_cases)
        print(f"Average error for all {len(long_trip_cases)} long trip cases: ${avg_error:.2f}")
        
        # Show distribution by days
        by_days = {}
        for case in long_trip_cases:
            days = int(case['days'])
            if days not in by_days:
                by_days[days] = []
            by_days[days].append(case['error'])
        
        print("\nError by trip length:")
        for days in sorted(by_days.keys()):
            errors = by_days[days]
            avg_err = sum(errors) / len(errors)
            print(f"  {days:2d} days: {len(errors):2d} cases, avg error ${avg_err:6.2f}")

if __name__ == '__main__':
    main()