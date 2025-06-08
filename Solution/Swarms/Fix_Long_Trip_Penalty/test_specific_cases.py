#!/usr/bin/env python3
"""
Test specific problematic long trip cases to understand patterns
"""
import json
import subprocess

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
    # Load test cases to get exact case data
    with open('public_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    # Test specific problematic cases mentioned in eval output
    problem_cases = [
        (520, 14, 481, 939.99, 877.17),   # From eval output
        (294, 14, 124, 1065, 1761.68),   # From our long trip analysis  
        (277, 12, 104, 1300, 1779.92),   # From our long trip analysis
        (310, 14, 127, 988, 1688.90),    # From our long trip analysis
    ]
    
    print("SPECIFIC CASE ANALYSIS")
    print("="*60)
    
    for case_id, days, miles, receipts, expected in problem_cases:
        predicted = test_case(days, miles, receipts)
        if predicted is not None:
            error = abs(predicted - expected)
            
            # Calculate efficiency metrics
            miles_per_day = miles / days
            receipts_per_day = receipts / days
            
            print(f"Case {case_id:3d}: {days:2.0f} days, {miles:4.0f} miles, ${receipts:5.0f} receipts")
            print(f"    Expected: ${expected:7.2f}, Predicted: ${predicted:7.2f}, Error: ${error:6.2f}")
            print(f"    Efficiency: {miles_per_day:5.1f} miles/day, ${receipts_per_day:5.1f} receipts/day")
            
            # Determine which logic branch this case would trigger
            if miles_per_day >= 80 and receipts_per_day <= 100:
                print(f"    -> Triggers EFFICIENT bonus (+5%)")
            elif miles_per_day <= 30 or receipts_per_day <= 20:
                print(f"    -> Triggers INEFFICIENT penalty")
            else:
                print(f"    -> No long trip adjustment (moderate efficiency)")
            print()

if __name__ == '__main__':
    main()