#!/usr/bin/env python3
"""
Per Diem Rate Analysis Script

Analyzes public test cases to identify per diem patterns by:
1. Testing different mileage rates to isolate per diem component
2. Grouping by trip duration to find patterns
3. Looking for bonuses on specific durations (especially 5-day trips)
4. Analyzing first/last day variations
"""

import json
import statistics
from collections import defaultdict
from typing import List, Dict, Any, Tuple


def load_test_cases(file_path: str) -> List[Dict[str, Any]]:
    """Load test cases from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def analyze_mileage_rates_with_base(test_cases: List[Dict[str, Any]], mileage_rates: List[float], base_amounts: List[float]) -> Dict[Tuple[float, float], Dict[str, Any]]:
    """Test different mileage rates and base amounts to see which gives cleanest per diem isolation."""
    results = {}
    
    for rate in mileage_rates:
        for base in base_amounts:
            per_diem_by_duration = defaultdict(list)
            
            for case in test_cases:
                trip_days = case['input']['trip_duration_days']
                miles = case['input']['miles_traveled']
                receipts = case['input']['total_receipts_amount']
                expected = case['expected_output']
                
                # Calculate potential per diem component
                mileage_component = miles * rate
                per_diem_component = expected - mileage_component - receipts - base
                per_diem_per_day = per_diem_component / trip_days if trip_days > 0 else 0
                
                per_diem_by_duration[trip_days].append({
                    'per_diem_component': per_diem_component,
                    'per_diem_per_day': per_diem_per_day,
                    'case': case
                })
            
            # Calculate statistics for each duration
            duration_stats = {}
            for duration, per_diems in per_diem_by_duration.items():
                per_day_rates = [pd['per_diem_per_day'] for pd in per_diems]
                duration_stats[duration] = {
                    'count': len(per_day_rates),
                    'mean_per_day': statistics.mean(per_day_rates),
                    'median_per_day': statistics.median(per_day_rates),
                    'std_dev': statistics.stdev(per_day_rates) if len(per_day_rates) > 1 else 0,
                    'min_per_day': min(per_day_rates),
                    'max_per_day': max(per_day_rates),
                    'cases': per_diems
                }
            
            # Calculate overall consistency metric (lower std dev across durations is better)
            all_per_day_rates = []
            for stats in duration_stats.values():
                all_per_day_rates.extend([case['per_diem_per_day'] for case in stats['cases']])
            
            overall_std = statistics.stdev(all_per_day_rates) if len(all_per_day_rates) > 1 else float('inf')
            
            results[(rate, base)] = {
                'duration_stats': duration_stats,
                'overall_std_dev': overall_std,
                'overall_mean': statistics.mean(all_per_day_rates)
            }
    
    return results


def analyze_five_day_bonus(test_cases: List[Dict[str, Any]], best_mileage_rate: float, best_base: float) -> Dict[str, Any]:
    """Specifically analyze 5-day trips to look for bonus patterns."""
    five_day_cases = []
    other_cases = []
    
    for case in test_cases:
        trip_days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        mileage_component = miles * best_mileage_rate
        per_diem_component = expected - mileage_component - receipts - best_base
        per_diem_per_day = per_diem_component / trip_days if trip_days > 0 else 0
        
        case_data = {
            'case': case,
            'per_diem_component': per_diem_component,
            'per_diem_per_day': per_diem_per_day
        }
        
        if trip_days == 5:
            five_day_cases.append(case_data)
        else:
            other_cases.append(case_data)
    
    # Calculate averages
    five_day_avg = statistics.mean([c['per_diem_per_day'] for c in five_day_cases]) if five_day_cases else 0
    other_avg = statistics.mean([c['per_diem_per_day'] for c in other_cases]) if other_cases else 0
    
    return {
        'five_day_count': len(five_day_cases),
        'five_day_avg_per_day': five_day_avg,
        'other_avg_per_day': other_avg,
        'potential_bonus': five_day_avg - other_avg if five_day_cases and other_cases else 0,
        'five_day_cases': five_day_cases[:5]  # Show first 5 examples
    }


def test_flat_rate_models(test_cases: List[Dict[str, Any]], mileage_rate: float, base_amount: float) -> Dict[str, Any]:
    """Test various flat rate per diem models."""
    flat_rates = [50, 75, 100, 120, 125, 130, 150]
    results = {}
    
    for flat_rate in flat_rates:
        errors = []
        
        for case in test_cases:
            trip_days = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            expected = case['expected_output']
            
            predicted = (flat_rate * trip_days) + (miles * mileage_rate) + receipts + base_amount
            error = abs(predicted - expected)
            errors.append(error)
        
        results[flat_rate] = {
            'mean_error': statistics.mean(errors),
            'median_error': statistics.median(errors),
            'max_error': max(errors),
            'std_error': statistics.stdev(errors) if len(errors) > 1 else 0
        }
    
    return results


def analyze_first_last_day_patterns(test_cases: List[Dict[str, Any]], mileage_rate: float, base_amount: float) -> Dict[str, Any]:
    """Analyze if there are different rates for first/last days vs middle days."""
    # Group by duration to look for patterns
    by_duration = defaultdict(list)
    
    for case in test_cases:
        trip_days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        mileage_component = miles * mileage_rate
        per_diem_component = expected - mileage_component - receipts - base_amount
        
        by_duration[trip_days].append({
            'per_diem_component': per_diem_component,
            'case': case
        })
    
    # Test different first/last day models
    models = [
        {'first_last': 75, 'middle': 125},  # Reduced first/last
        {'first_last': 100, 'middle': 125}, # Standard first/last
        {'first_last': 62.5, 'middle': 125}, # Half rate first/last
    ]
    
    model_results = {}
    
    for i, model in enumerate(models):
        total_error = 0
        case_count = 0
        
        for case in test_cases:
            trip_days = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            expected = case['expected_output']
            
            # Calculate per diem based on model
            if trip_days == 1:
                per_diem = model['first_last']  # Only first/last day rate
            else:
                per_diem = (2 * model['first_last']) + ((trip_days - 2) * model['middle'])
            
            predicted = per_diem + (miles * mileage_rate) + receipts + base_amount
            error = abs(predicted - expected)
            total_error += error
            case_count += 1
        
        model_results[f"Model_{i+1}"] = {
            'description': f"First/Last: ${model['first_last']}, Middle: ${model['middle']}",
            'mean_error': total_error / case_count if case_count > 0 else float('inf')
        }
    
    return model_results


def reverse_engineer_model(test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Try to reverse engineer the actual model by exploring different coefficient combinations."""
    
    # Test a wide range of coefficients based on the provided linear model in run.sh
    # Current model: 50.050486 * days + 0.445645 * miles + 0.382861 * receipts + 266.707681
    
    coefficient_tests = [
        # Test around the current model
        (50.0, 0.45, 0.38, 267),
        (50.05, 0.446, 0.383, 266.7),
        (50.050486, 0.445645, 0.382861, 266.707681),  # Exact current model
        
        # Test simpler models
        (100, 0.5, 1.0, 0),    # Simple: $100/day + $0.50/mile + full receipts
        (125, 0.575, 1.0, 0),  # Government rates: $125/day + $0.575/mile + full receipts
        (75, 0.5, 1.0, 50),    # With base amount
        (100, 0.4, 1.0, 50),   # Lower mileage rate
        
        # Test per diem variations with first/last day differences
        (62.5, 0.5, 1.0, 125), # Assuming 62.5 for first/last, 125 for middle days as base
    ]
    
    best_error = float('inf')
    best_model = None
    results = []
    
    for days_coeff, miles_coeff, receipts_coeff, intercept in coefficient_tests:
        total_error = 0
        max_error = 0
        errors = []
        
        for case in test_cases:
            trip_days = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            expected = case['expected_output']
            
            predicted = (days_coeff * trip_days) + (miles_coeff * miles) + (receipts_coeff * receipts) + intercept
            error = abs(predicted - expected)
            
            total_error += error
            max_error = max(max_error, error)
            errors.append(error)
        
        mean_error = total_error / len(test_cases)
        
        model_result = {
            'coefficients': (days_coeff, miles_coeff, receipts_coeff, intercept),
            'mean_error': mean_error,
            'max_error': max_error,
            'std_error': statistics.stdev(errors) if len(errors) > 1 else 0
        }
        
        results.append(model_result)
        
        if mean_error < best_error:
            best_error = mean_error
            best_model = model_result
    
    return {
        'best_model': best_model,
        'all_results': sorted(results, key=lambda x: x['mean_error'])
    }


def main():
    """Main analysis function."""
    print("=== Per Diem Rate Analysis ===\n")
    
    # Load test cases
    file_path = "/Users/seima/8090/top-coder-challenge/public_cases.json"
    test_cases = load_test_cases(file_path)
    print(f"Loaded {len(test_cases)} test cases\n")
    
    # First, let's reverse engineer the actual model
    print("0. Reverse engineering the actual model:")
    model_analysis = reverse_engineer_model(test_cases)
    
    print("Top 5 models by accuracy:")
    for i, result in enumerate(model_analysis['all_results'][:5]):
        days_c, miles_c, receipts_c, intercept = result['coefficients']
        print(f"  {i+1}. ${days_c:.3f} * days + ${miles_c:.3f} * miles + {receipts_c:.3f} * receipts + ${intercept:.2f}")
        print(f"     Mean error: ${result['mean_error']:.2f}, Max error: ${result['max_error']:.2f}")
    
    best_model = model_analysis['best_model']
    print(f"\nBest model: ${best_model['coefficients'][0]:.6f} * days + ${best_model['coefficients'][1]:.6f} * miles + {best_model['coefficients'][2]:.6f} * receipts + ${best_model['coefficients'][3]:.6f}")
    print(f"Mean error: ${best_model['mean_error']:.2f}\n")
    
    # Test different mileage rates and base amounts
    print("1. Testing different mileage rates and base amounts to isolate per diem component:")
    mileage_rates = [0.40, 0.45, 0.50, 0.575, 0.65]
    base_amounts = [0, 50, 100, 150, 200, 250]
    mileage_results = analyze_mileage_rates_with_base(test_cases, mileage_rates, base_amounts)
    
    best_combo = min(mileage_results.keys(), key=lambda combo: mileage_results[combo]['overall_std_dev'])
    best_rate, best_base = best_combo
    
    print("Top 5 combinations (lowest std dev):")
    sorted_combos = sorted(mileage_results.items(), key=lambda x: x[1]['overall_std_dev'])[:5]
    for i, ((rate, base), result) in enumerate(sorted_combos):
        print(f"  {i+1}. Rate ${rate:.3f}, Base ${base:.0f}: std dev {result['overall_std_dev']:.2f}, mean per day ${result['overall_mean']:.2f}")
    
    print(f"\nBest combination: ${best_rate:.3f}/mile + ${best_base:.0f} base\n")
    
    # Analyze per duration with best combination
    print("2. Per diem analysis by trip duration (using best combination):")
    best_result = mileage_results[best_combo]
    
    for duration in sorted(best_result['duration_stats'].keys()):
        stats = best_result['duration_stats'][duration]
        print(f"  {duration} day trips ({stats['count']} cases):")
        print(f"    Mean per day: ${stats['mean_per_day']:.2f}")
        print(f"    Median per day: ${stats['median_per_day']:.2f}")
        print(f"    Std dev: {stats['std_dev']:.2f}")
        print(f"    Range: ${stats['min_per_day']:.2f} - ${stats['max_per_day']:.2f}")
        print()
    
    # Test flat rate models
    print("3. Testing flat rate per diem models:")
    flat_rate_results = test_flat_rate_models(test_cases, best_rate, best_base)
    
    best_flat_rate = min(flat_rate_results.keys(), key=lambda r: flat_rate_results[r]['mean_error'])
    
    for rate in sorted(flat_rate_results.keys()):
        result = flat_rate_results[rate]
        print(f"  ${rate}/day: Mean error ${result['mean_error']:.2f}, Max error ${result['max_error']:.2f}")
    
    print(f"\nBest flat rate: ${best_flat_rate}/day (lowest mean error)\n")
    
    # Analyze 5-day bonus
    print("4. Five-day trip bonus analysis:")
    five_day_analysis = analyze_five_day_bonus(test_cases, best_rate, best_base)
    print(f"  5-day trips: {five_day_analysis['five_day_count']} cases")
    print(f"  5-day avg per day: ${five_day_analysis['five_day_avg_per_day']:.2f}")
    print(f"  Other trips avg per day: ${five_day_analysis['other_avg_per_day']:.2f}")
    print(f"  Potential bonus: ${five_day_analysis['potential_bonus']:.2f}/day")
    print()
    
    # Analyze first/last day patterns
    print("5. First/Last day variation analysis:")
    first_last_results = analyze_first_last_day_patterns(test_cases, best_rate, best_base)
    
    for model, result in first_last_results.items():
        print(f"  {result['description']}: Mean error ${result['mean_error']:.2f}")
    
    print()
    
    # Summary and recommendations
    print("=== SUMMARY AND RECOMMENDATIONS ===")
    print(f"Best mileage rate: ${best_rate:.3f} per mile")
    print(f"Best base amount: ${best_base:.0f}")
    print(f"Best flat per diem rate: ${best_flat_rate} per day")
    
    flat_error = flat_rate_results[best_flat_rate]['mean_error']
    best_first_last = min(first_last_results.items(), key=lambda x: x[1]['mean_error'])
    
    print(f"Flat rate model error: ${flat_error:.2f}")
    print(f"Best first/last model: {best_first_last[1]['description']}")
    print(f"First/last model error: ${best_first_last[1]['mean_error']:.2f}")
    
    if five_day_analysis['potential_bonus'] > 10:
        print(f"Significant 5-day bonus detected: ${five_day_analysis['potential_bonus']:.2f}/day")
    else:
        print("No significant 5-day bonus detected")
    
    print(f"\nRecommended model: {best_first_last[1]['description']} + ${best_rate:.3f}/mile + ${best_base:.0f} base + receipts")
    
    # Interpret the actual linear model in per diem terms
    print("\n=== INTERPRETATION OF ACTUAL MODEL ===")
    actual_model = model_analysis['best_model']['coefficients']
    days_coeff, miles_coeff, receipts_coeff, intercept = actual_model
    
    print(f"Actual model: {days_coeff:.6f} * days + {miles_coeff:.6f} * miles + {receipts_coeff:.6f} * receipts + {intercept:.6f}")
    print(f"This can be interpreted as:")
    print(f"  - Base reimbursement: ${intercept:.2f}")
    print(f"  - Per day rate: ${days_coeff:.2f}")
    print(f"  - Mileage rate: ${miles_coeff:.3f} per mile")
    print(f"  - Receipt reimbursement: {receipts_coeff:.1%} of receipts")
    print(f"  - Mean error: ${model_analysis['best_model']['mean_error']:.2f}")
    
    print(f"\nThis is NOT a traditional per diem system, but rather a linear combination model.")
    print(f"The '{days_coeff:.2f} per day' is not a per diem allowance, but part of a linear formula.")
    print(f"The large base amount (${intercept:.2f}) suggests fixed processing/administrative costs.")
    print(f"The partial receipt reimbursement ({receipts_coeff:.1%}) suggests a receipt review/audit factor.")


if __name__ == "__main__":
    main()