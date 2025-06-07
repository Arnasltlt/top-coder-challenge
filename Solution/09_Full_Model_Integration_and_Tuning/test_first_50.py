#!/usr/bin/env python3
"""
Test the current run.sh model against the first 50 test cases from public_cases.json
Calculate MAE, percentage of cases with errors under $20, and identify worst 5 cases.
Analyze performance by trip duration.
"""

import json
import subprocess
import statistics
from typing import List, Dict, Tuple
import os

def load_test_cases(n_cases: int = 50) -> List[Dict]:
    """Load the first n test cases from public_cases.json"""
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        all_cases = json.load(f)
    return all_cases[:n_cases]

def run_model(days: int, miles: float, receipts: float) -> float:
    """Run the current model and return the prediction"""
    result = subprocess.run([
        '/bin/bash', '/Users/seima/8090/top-coder-challenge/run.sh',
        str(days), str(miles), str(receipts)
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Model execution failed: {result.stderr}")
    
    return float(result.stdout.strip())

def calculate_metrics(predictions: List[float], actual: List[float]) -> Dict:
    """Calculate various performance metrics"""
    errors = [abs(pred - act) for pred, act in zip(predictions, actual)]
    
    mae = statistics.mean(errors)
    under_20_count = sum(1 for error in errors if error < 20)
    under_20_percentage = (under_20_count / len(errors)) * 100
    
    # Find worst 5 cases
    error_indices = [(i, error) for i, error in enumerate(errors)]
    error_indices.sort(key=lambda x: x[1], reverse=True)
    worst_5_indices = [idx for idx, _ in error_indices[:5]]
    
    return {
        'mae': mae,
        'under_20_count': under_20_count,
        'under_20_percentage': under_20_percentage,
        'worst_5_indices': worst_5_indices,
        'all_errors': errors
    }

def analyze_by_duration(test_cases: List[Dict], predictions: List[float], errors: List[float]) -> Dict:
    """Analyze performance by trip duration"""
    duration_analysis = {}
    
    for i, (case, pred, error) in enumerate(zip(test_cases, predictions, errors)):
        duration = case['input']['trip_duration_days']
        
        if duration not in duration_analysis:
            duration_analysis[duration] = {
                'cases': [],
                'predictions': [],
                'actual': [],
                'errors': []
            }
        
        duration_analysis[duration]['cases'].append(i)
        duration_analysis[duration]['predictions'].append(pred)
        duration_analysis[duration]['actual'].append(case['expected_output'])
        duration_analysis[duration]['errors'].append(error)
    
    # Calculate metrics for each duration
    duration_metrics = {}
    for duration, data in duration_analysis.items():
        duration_metrics[duration] = {
            'count': len(data['cases']),
            'mae': statistics.mean(data['errors']),
            'under_20_count': sum(1 for e in data['errors'] if e < 20),
            'under_20_percentage': (sum(1 for e in data['errors'] if e < 20) / len(data['errors'])) * 100,
            'avg_prediction': statistics.mean(data['predictions']),
            'avg_actual': statistics.mean(data['actual'])
        }
    
    return duration_metrics

def main():
    print("Loading first 50 test cases...")
    test_cases = load_test_cases(50)
    
    print("Running model predictions...")
    predictions = []
    actual_values = []
    
    for i, case in enumerate(test_cases):
        input_data = case['input']
        days = input_data['trip_duration_days']
        miles = input_data['miles_traveled']
        receipts = input_data['total_receipts_amount']
        expected = case['expected_output']
        
        try:
            prediction = run_model(days, miles, receipts)
            predictions.append(prediction)
            actual_values.append(expected)
            print(f"Case {i+1:2d}: Days={days}, Miles={miles:6.1f}, Receipts=${receipts:6.2f} | "
                  f"Predicted=${prediction:7.2f}, Actual=${expected:7.2f}, Error=${abs(prediction-expected):6.2f}")
        except Exception as e:
            print(f"Error running case {i+1}: {e}")
            return
    
    print("\n" + "="*80)
    print("PERFORMANCE ANALYSIS")
    print("="*80)
    
    # Calculate overall metrics
    metrics = calculate_metrics(predictions, actual_values)
    
    print(f"\nOVERALL METRICS:")
    print(f"Mean Absolute Error (MAE): ${metrics['mae']:.2f}")
    print(f"Cases with error < $20: {metrics['under_20_count']}/50 ({metrics['under_20_percentage']:.1f}%)")
    
    # Show worst 5 cases
    print(f"\nWORST 5 CASES:")
    print(f"{'Case':>4} {'Days':>4} {'Miles':>6} {'Receipts':>8} {'Predicted':>9} {'Actual':>9} {'Error':>8}")
    print("-" * 60)
    
    for idx in metrics['worst_5_indices']:
        case = test_cases[idx]
        input_data = case['input']
        days = input_data['trip_duration_days']
        miles = input_data['miles_traveled']
        receipts = input_data['total_receipts_amount']
        pred = predictions[idx]
        actual = actual_values[idx]
        error = abs(pred - actual)
        
        print(f"{idx+1:4d} {days:4d} {miles:6.1f} ${receipts:7.2f} ${pred:8.2f} ${actual:8.2f} ${error:7.2f}")
    
    # Analyze by trip duration
    print(f"\nPERFORMANCE BY TRIP DURATION:")
    duration_metrics = analyze_by_duration(test_cases, predictions, metrics['all_errors'])
    
    print(f"{'Duration':>8} {'Count':>5} {'MAE':>8} {'<$20':>4} {'<$20%':>6} {'Avg Pred':>9} {'Avg Actual':>10}")
    print("-" * 70)
    
    for duration in sorted(duration_metrics.keys()):
        data = duration_metrics[duration]
        print(f"{duration:8d} {data['count']:5d} ${data['mae']:7.2f} "
              f"{data['under_20_count']:4d} {data['under_20_percentage']:5.1f}% "
              f"${data['avg_prediction']:8.2f} ${data['avg_actual']:9.2f}")
    
    # Model readiness assessment
    print(f"\n" + "="*80)
    print("MODEL READINESS ASSESSMENT")
    print("="*80)
    
    mae_threshold = 60
    accuracy_threshold = 60
    
    mae_ready = metrics['mae'] < mae_threshold
    accuracy_ready = metrics['under_20_percentage'] > accuracy_threshold
    
    print(f"MAE Criterion: ${metrics['mae']:.2f} < ${mae_threshold} = {'✓ PASS' if mae_ready else '✗ FAIL'}")
    print(f"Accuracy Criterion: {metrics['under_20_percentage']:.1f}% > {accuracy_threshold}% = {'✓ PASS' if accuracy_ready else '✗ FAIL'}")
    
    if mae_ready and accuracy_ready:
        print(f"\n🎉 MODEL IS READY FOR FULL EVALUATION!")
    else:
        print(f"\n⚠️  MODEL NEEDS FURTHER IMPROVEMENT")
        
        # Identify main issues
        print(f"\nMAIN REMAINING ISSUES:")
        
        # Analyze patterns in errors
        high_error_cases = [i for i, error in enumerate(metrics['all_errors']) if error >= 50]
        if high_error_cases:
            print(f"• {len(high_error_cases)} cases with errors ≥ $50")
            
            # Group high error cases by duration
            duration_high_errors = {}
            for idx in high_error_cases:
                duration = test_cases[idx]['input']['trip_duration_days']
                if duration not in duration_high_errors:
                    duration_high_errors[duration] = 0
                duration_high_errors[duration] += 1
            
            for duration, count in sorted(duration_high_errors.items()):
                print(f"  - {count} cases with {duration}-day trips")
        
        # Check for systematic bias by duration
        print(f"\nSYSTEMATIC BIAS BY DURATION:")
        for duration in sorted(duration_metrics.keys()):
            data = duration_metrics[duration]
            bias = data['avg_prediction'] - data['avg_actual']
            bias_type = "over-predicting" if bias > 0 else "under-predicting"
            if abs(bias) > 20:
                print(f"  - {duration}-day trips: {bias_type} by ${abs(bias):.2f} on average")

if __name__ == "__main__":
    main()