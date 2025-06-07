#!/usr/bin/env python3
"""
OPERATION: FINAL CLOSURE - Target Identification
Find the top 25 highest-error cases for surgical analysis
"""

import json
import subprocess
import sys

def load_public_cases():
    """Load the public test cases"""
    try:
        with open('public_cases.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        with open('../public_cases.json', 'r') as f:
            return json.load(f)

def get_model_prediction(days, miles, receipts):
    """Get prediction from current run.sh model"""
    try:
        result = subprocess.run(
            ['./run.sh', str(days), str(miles), str(receipts)],
            capture_output=True, text=True, check=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error running model for {days}, {miles}, {receipts}: {e}")
        return None

def analyze_outliers():
    """Find and analyze the worst-performing cases"""
    
    print("🎯 OPERATION: FINAL CLOSURE - TARGET IDENTIFICATION")
    print("=" * 60)
    
    cases = load_public_cases()
    
    print(f"📊 Analyzing {len(cases)} cases for outliers...")
    
    errors = []
    
    for i, case in enumerate(cases):
        if i % 100 == 0:
            print(f"   Processing case {i}...")
            
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        predicted = get_model_prediction(days, miles, receipts)
        
        if predicted is not None:
            error = abs(predicted - expected)
            errors.append({
                'case_index': i,
                'days': days,
                'miles': miles, 
                'receipts': receipts,
                'expected': expected,
                'predicted': predicted,
                'error': error,
                'signed_error': expected - predicted,
                'daily_receipts': receipts / max(days, 1),
                'daily_miles': miles / max(days, 1),
                'receipts_per_mile': receipts / max(miles, 1) if miles > 0 else 0
            })
    
    # Sort by error (worst first)
    errors.sort(key=lambda x: x['error'], reverse=True)
    
    print(f"\n🔍 TOP 25 OUTLIER CASES (SNIPER TARGETS):")
    print("=" * 80)
    
    outliers = errors[:25]
    
    for i, case in enumerate(outliers):
        print(f"TARGET {i+1:2d}: Case {case['case_index']:3d}")
        print(f"   Input: {case['days']}d, {case['miles']:4.0f}mi, ${case['receipts']:7.2f}")
        print(f"   Expected: ${case['expected']:8.2f} | Predicted: ${case['predicted']:8.2f} | Error: ${case['error']:7.2f}")
        print(f"   Daily: ${case['daily_receipts']:6.2f}/day, {case['daily_miles']:5.1f}mi/day")
        if case['miles'] > 0:
            print(f"   Ratio: ${case['receipts_per_mile']:.2f}/mile")
        print()
    
    print(f"\n📊 OUTLIER STATISTICS:")
    print(f"   Average error in top 25: ${sum(case['error'] for case in outliers) / len(outliers):.2f}")
    print(f"   Total error from top 25: ${sum(case['error'] for case in outliers):.2f}")
    print(f"   % of total error from top 25: {(sum(case['error'] for case in outliers) / sum(case['error'] for case in errors)) * 100:.1f}%")
    
    return outliers

def analyze_outlier_patterns(outliers):
    """Look for patterns in the outlier cases"""
    
    print(f"\n🔍 PATTERN ANALYSIS:")
    print("=" * 40)
    
    # Days analysis
    days_values = [case['days'] for case in outliers]
    unique_days = set(days_values)
    print(f"Days distribution: {sorted(unique_days)}")
    for day in sorted(unique_days):
        count = days_values.count(day)
        print(f"   {day} days: {count} cases ({count/len(outliers)*100:.1f}%)")
    
    # Miles analysis
    print(f"\nMiles analysis:")
    zero_miles = sum(1 for case in outliers if case['miles'] == 0)
    high_miles = sum(1 for case in outliers if case['miles'] > 1000)
    print(f"   Zero miles: {zero_miles} cases")
    print(f"   High miles (>1000): {high_miles} cases")
    
    # Receipt analysis
    print(f"\nReceipt analysis:")
    high_receipts = sum(1 for case in outliers if case['receipts'] > 2000)
    very_high_receipts = sum(1 for case in outliers if case['receipts'] > 3000)
    print(f"   High receipts (>$2000): {high_receipts} cases")
    print(f"   Very high receipts (>$3000): {very_high_receipts} cases")
    
    # Daily spending analysis
    print(f"\nDaily spending analysis:")
    daily_receipts = [case['daily_receipts'] for case in outliers]
    avg_daily = sum(daily_receipts) / len(daily_receipts)
    high_daily = sum(1 for dr in daily_receipts if dr > 300)
    print(f"   Average daily spending: ${avg_daily:.2f}")
    print(f"   High daily spending (>$300): {high_daily} cases")
    
    # Look for specific patterns
    print(f"\n🎯 SPECIFIC PATTERN CHECKS:")
    
    # Check for hard caps
    predictions = [case['predicted'] for case in outliers]
    max_prediction = max(predictions)
    print(f"   Max prediction in outliers: ${max_prediction:.2f}")
    
    # Check for over-predictions vs under-predictions
    over_predictions = sum(1 for case in outliers if case['signed_error'] < 0)
    under_predictions = sum(1 for case in outliers if case['signed_error'] > 0)
    print(f"   Over-predictions: {over_predictions} cases")
    print(f"   Under-predictions: {under_predictions} cases")
    
    # Look for extreme ratios
    print(f"\n🔍 EXTREME RATIO ANALYSIS:")
    for i, case in enumerate(outliers[:10]):
        receipt_to_expected = case['receipts'] / case['expected'] if case['expected'] > 0 else 0
        predicted_to_expected = case['predicted'] / case['expected'] if case['expected'] > 0 else 0
        print(f"   Target {i+1}: Receipts/Expected = {receipt_to_expected:.2f}, Predicted/Expected = {predicted_to_expected:.2f}")

if __name__ == "__main__":
    outliers = analyze_outliers()
    analyze_outlier_patterns(outliers)