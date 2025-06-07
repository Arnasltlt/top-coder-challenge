#!/usr/bin/env python3

import json
import subprocess
import statistics
from collections import defaultdict

def test_first_30_cases():
    """Test the current run.sh model against the first 30 test cases from public_cases.json"""
    
    # Load the test cases
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    # Take only the first 30 cases
    first_30_cases = test_cases[:30]
    
    print("Testing current run.sh model against first 30 cases from public_cases.json")
    print("=" * 80)
    
    results = []
    errors_by_duration = defaultdict(list)
    
    for i, case in enumerate(first_30_cases, 1):
        input_data = case['input']
        expected = case['expected_output']
        
        days = input_data['trip_duration_days']
        miles = input_data['miles_traveled']  
        receipts = input_data['total_receipts_amount']
        
        # Run the model
        try:
            result = subprocess.run([
                '/Users/seima/8090/top-coder-challenge/run.sh',
                str(days), str(miles), str(receipts)
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print(f"Case {i}: ERROR - Script failed: {result.stderr}")
                continue
                
            predicted = float(result.stdout.strip())
            error = abs(predicted - expected)
            
            results.append({
                'case': i,
                'days': days,
                'miles': miles,
                'receipts': receipts,
                'expected': expected,
                'predicted': predicted,
                'error': error
            })
            
            errors_by_duration[days].append(error)
            
            print(f"Case {i:2d}: Days={days}, Miles={miles:3d}, Receipts=${receipts:6.2f} -> "
                  f"Expected=${expected:7.2f}, Predicted=${predicted:7.2f}, Error=${error:6.2f}")
                  
        except Exception as e:
            print(f"Case {i}: ERROR - {e}")
            continue
    
    if not results:
        print("No successful test cases!")
        return
    
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    # Calculate overall statistics
    all_errors = [r['error'] for r in results]
    mean_error = statistics.mean(all_errors)
    median_error = statistics.median(all_errors)
    max_error = max(all_errors)
    min_error = min(all_errors)
    
    print(f"Total test cases run: {len(results)}")
    print(f"Mean Absolute Error: ${mean_error:.2f}")
    print(f"Median Absolute Error: ${median_error:.2f}")
    print(f"Max Error: ${max_error:.2f}")
    print(f"Min Error: ${min_error:.2f}")
    
    # Calculate percentage of cases with errors under $20
    under_20_count = sum(1 for error in all_errors if error < 20)
    under_20_percent = (under_20_count / len(all_errors)) * 100
    print(f"Cases with error < $20: {under_20_count}/{len(results)} ({under_20_percent:.1f}%)")
    
    # Analyze errors by trip duration
    print("\n" + "=" * 80)
    print("ERRORS BY TRIP DURATION")
    print("=" * 80)
    
    duration_stats = []
    for duration in sorted(errors_by_duration.keys()):
        errors = errors_by_duration[duration]
        mean_err = statistics.mean(errors)
        count = len(errors)
        max_err = max(errors)
        duration_stats.append((duration, mean_err, count, max_err))
        
        print(f"{duration}-day trips: {count} cases, Mean Error=${mean_err:.2f}, Max Error=${max_err:.2f}")
    
    # Find which durations have highest errors
    duration_stats.sort(key=lambda x: x[1], reverse=True)
    print(f"\nTrip durations with HIGHEST mean errors:")
    for i, (duration, mean_err, count, max_err) in enumerate(duration_stats[:5]):
        print(f"{i+1}. {duration}-day trips: Mean Error=${mean_err:.2f} ({count} cases)")
    
    # Detailed breakdown of worst cases
    print("\n" + "=" * 80)
    print("WORST PERFORMING CASES (Top 10)")
    print("=" * 80)
    
    worst_cases = sorted(results, key=lambda x: x['error'], reverse=True)[:10]
    for i, case in enumerate(worst_cases, 1):
        print(f"{i:2d}. Case {case['case']:2d}: {case['days']}-day, {case['miles']} miles, "
              f"${case['receipts']:.2f} receipts -> Error=${case['error']:.2f}")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if mean_error > 50:
        print("❌ Mean error is quite high (>${:.2f}). Significant tuning needed.".format(mean_error))
    elif mean_error > 25:
        print("⚠️  Mean error is moderate (>${:.2f}). Some tuning recommended.".format(mean_error))
    else:
        print("✅ Mean error is reasonable (${:.2f}). Minor tuning may help.".format(mean_error))
    
    if under_20_percent < 60:
        print("❌ Only {:.1f}% of cases have errors under $20. Need significant improvement.".format(under_20_percent))
    elif under_20_percent < 80:
        print("⚠️  {:.1f}% of cases have errors under $20. Room for improvement.".format(under_20_percent))
    else:
        print("✅ {:.1f}% of cases have errors under $20. Good performance.".format(under_20_percent))
    
    print(f"\nFocus tuning efforts on: {duration_stats[0][0]}-day trips (highest mean error: ${duration_stats[0][1]:.2f})")

if __name__ == "__main__":
    test_first_30_cases()