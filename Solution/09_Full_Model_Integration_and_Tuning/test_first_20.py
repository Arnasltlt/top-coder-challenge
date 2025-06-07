#!/usr/bin/env python3

import json
import subprocess
import sys
import os

def test_model_on_first_20():
    """Test the current run.sh model against the first 20 test cases."""
    
    # Read the public cases
    public_cases_path = "/Users/seima/8090/top-coder-challenge/public_cases.json"
    run_script_path = "/Users/seima/8090/top-coder-challenge/run.sh"
    
    try:
        with open(public_cases_path, 'r') as f:
            cases = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {public_cases_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return
    
    # Take first 20 cases
    first_20_cases = cases[:20]
    
    results = []
    errors = []
    
    print("Testing first 20 cases...")
    print("="*80)
    
    for i, case in enumerate(first_20_cases):
        input_data = case["input"]
        expected = case["expected_output"]
        
        days = input_data["trip_duration_days"]
        miles = input_data["miles_traveled"] 
        receipts = input_data["total_receipts_amount"]
        
        try:
            # Run the model
            result = subprocess.run(
                [run_script_path, str(days), str(miles), str(receipts)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                error_msg = f"Case {i+1}: Script failed with return code {result.returncode}"
                if result.stderr:
                    error_msg += f". Error: {result.stderr.strip()}"
                errors.append(error_msg)
                continue
                
            try:
                predicted = float(result.stdout.strip())
            except ValueError:
                errors.append(f"Case {i+1}: Invalid output '{result.stdout.strip()}'")
                continue
                
            absolute_error = abs(predicted - expected)
            results.append({
                'case': i + 1,
                'days': days,
                'miles': miles,
                'receipts': receipts,
                'expected': expected,
                'predicted': predicted,
                'error': absolute_error
            })
            
        except subprocess.TimeoutExpired:
            errors.append(f"Case {i+1}: Script timed out")
        except Exception as e:
            errors.append(f"Case {i+1}: Unexpected error: {str(e)}")
    
    # Print any errors
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  {error}")
        print()
    
    if not results:
        print("No valid results to analyze!")
        return
        
    # Calculate statistics
    total_error = sum(r['error'] for r in results)
    mean_absolute_error = total_error / len(results)
    
    # Sort by error (worst first)
    results_by_error = sorted(results, key=lambda x: x['error'], reverse=True)
    
    print(f"RESULTS SUMMARY:")
    print(f"  Cases tested: {len(results)}")
    print(f"  Mean Absolute Error: ${mean_absolute_error:.2f}")
    print(f"  Previous MAE: $92.32")
    print(f"  Improvement: ${92.32 - mean_absolute_error:.2f}")
    print()
    
    print("TOP 5 WORST PERFORMING CASES:")
    print("-" * 80)
    for i, r in enumerate(results_by_error[:5]):
        print(f"{i+1}. Case {r['case']}: {r['days']} days, {r['miles']} miles, ${r['receipts']:.2f} receipts")
        print(f"   Expected: ${r['expected']:.2f}, Predicted: ${r['predicted']:.2f}, Error: ${r['error']:.2f}")
        print()
    
    print("ALL CASES DETAILED:")
    print("-" * 80)
    print("Case | Days | Miles | Receipts | Expected | Predicted | Error")
    print("-" * 80)
    for r in results:
        print(f"{r['case']:4d} | {r['days']:4d} | {r['miles']:5.0f} | {r['receipts']:8.2f} | {r['expected']:8.2f} | {r['predicted']:9.2f} | {r['error']:5.2f}")

if __name__ == "__main__":
    test_model_on_first_20()