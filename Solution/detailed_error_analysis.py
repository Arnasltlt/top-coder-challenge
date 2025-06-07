#!/usr/bin/env python3
"""
OPERATION: CASE-BY-CASE PRECISION DEBUGGING
Systematic analysis of every error to climb the leaderboard
"""

import json
import subprocess
import sys
from collections import defaultdict

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

def comprehensive_error_analysis():
    """Comprehensive analysis of ALL errors, not just top 25"""
    
    print("🔬 COMPREHENSIVE ERROR ANALYSIS - EVERY CASE")
    print("=" * 60)
    
    cases = load_public_cases()
    errors = []
    
    print(f"📊 Analyzing ALL {len(cases)} cases...")
    
    for i, case in enumerate(cases):
        if i % 50 == 0:
            print(f"   Processing case {i}...")
            
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        predicted = get_model_prediction(days, miles, receipts)
        
        if predicted is not None:
            error = abs(predicted - expected)
            if error > 0.01:  # Only non-exact matches
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
                    'error_percentage': (error / expected * 100) if expected > 0 else 0
                })
    
    # Sort by error (worst first)
    errors.sort(key=lambda x: x['error'], reverse=True)
    
    print(f"\n📊 ERROR SUMMARY:")
    print(f"   Total cases with errors: {len(errors)}")
    print(f"   Exact matches: {1000 - len(errors)}")
    print(f"   Average error: ${sum(e['error'] for e in errors) / len(errors):.2f}")
    
    return errors

def categorize_errors_by_characteristics(errors):
    """Categorize errors by various characteristics"""
    
    print(f"\n🔍 ERROR CATEGORIZATION:")
    print("=" * 40)
    
    categories = {
        'by_days': defaultdict(list),
        'by_miles_range': defaultdict(list),
        'by_receipts_range': defaultdict(list),
        'by_error_type': defaultdict(list),
        'by_daily_spending': defaultdict(list),
        'by_efficiency': defaultdict(list)
    }
    
    for error in errors:
        # By days
        categories['by_days'][error['days']].append(error)
        
        # By miles range
        if error['miles'] == 0:
            miles_cat = 'zero_miles'
        elif error['miles'] < 100:
            miles_cat = 'very_low_miles'
        elif error['miles'] < 300:
            miles_cat = 'low_miles'
        elif error['miles'] < 600:
            miles_cat = 'medium_miles'
        elif error['miles'] < 1000:
            miles_cat = 'high_miles'
        else:
            miles_cat = 'very_high_miles'
        categories['by_miles_range'][miles_cat].append(error)
        
        # By receipts range
        if error['receipts'] < 200:
            receipts_cat = 'low_receipts'
        elif error['receipts'] < 600:
            receipts_cat = 'medium_receipts'
        elif error['receipts'] < 1200:
            receipts_cat = 'high_receipts'
        else:
            receipts_cat = 'very_high_receipts'
        categories['by_receipts_range'][receipts_cat].append(error)
        
        # By error type
        if error['signed_error'] > 0:
            error_type = 'under_prediction'
        else:
            error_type = 'over_prediction'
        categories['by_error_type'][error_type].append(error)
        
        # By daily spending
        daily = error['daily_receipts']
        if daily < 50:
            daily_cat = 'low_daily_spending'
        elif daily < 150:
            daily_cat = 'medium_daily_spending'
        elif daily < 300:
            daily_cat = 'high_daily_spending'
        else:
            daily_cat = 'very_high_daily_spending'
        categories['by_daily_spending'][daily_cat].append(error)
        
        # By efficiency (receipts per mile)
        if error['miles'] > 0:
            efficiency = error['receipts'] / error['miles']
            if efficiency < 0.5:
                eff_cat = 'very_efficient'
            elif efficiency < 1.5:
                eff_cat = 'efficient'
            elif efficiency < 3.0:
                eff_cat = 'inefficient'
            else:
                eff_cat = 'very_inefficient'
            categories['by_efficiency'][eff_cat].append(error)
    
    # Report on each category
    for category_name, category_data in categories.items():
        print(f"\n{category_name.upper()}:")
        for sub_cat, cases in category_data.items():
            avg_error = sum(c['error'] for c in cases) / len(cases)
            print(f"   {sub_cat}: {len(cases)} cases, avg error ${avg_error:.2f}")
    
    return categories

def find_specific_patterns(errors):
    """Look for very specific patterns that might need targeted rules"""
    
    print(f"\n🎯 SPECIFIC PATTERN HUNTING:")
    print("=" * 40)
    
    patterns = []
    
    # Pattern 1: Exact day-mile-receipt combinations with consistent errors
    value_combinations = defaultdict(list)
    for error in errors:
        key = (error['days'], error['miles'], int(error['receipts']))
        value_combinations[key].append(error)
    
    # Find combinations that appear multiple times
    multi_occurrence = {k: v for k, v in value_combinations.items() if len(v) > 1}
    if multi_occurrence:
        print(f"\n🔍 REPEATED COMBINATIONS:")
        for combo, cases in multi_occurrence.items():
            avg_error = sum(c['error'] for c in cases) / len(cases)
            print(f"   {combo}: {len(cases)} cases, avg error ${avg_error:.2f}")
    
    # Pattern 2: Zero miles cases
    zero_miles = [e for e in errors if e['miles'] == 0]
    if zero_miles:
        print(f"\n🚗 ZERO MILES CASES: {len(zero_miles)}")
        for case in zero_miles[:5]:
            print(f"   Case {case['case_index']}: {case['days']}d, $0mi, ${case['receipts']:.2f} → ${case['expected']:.2f} vs ${case['predicted']:.2f}")
    
    # Pattern 3: Round number receipts (might indicate per-diem limits)
    round_receipts = [e for e in errors if e['receipts'] % 50 == 0 or e['receipts'] % 25 == 0]
    if round_receipts:
        print(f"\n💰 ROUND RECEIPT AMOUNTS: {len(round_receipts)}")
        round_errors = sum(e['error'] for e in round_receipts) / len(round_receipts)
        print(f"   Average error: ${round_errors:.2f}")
    
    # Pattern 4: Extremely high or low reimbursement ratios
    extreme_ratios = []
    for error in errors:
        ratio = error['predicted'] / error['expected'] if error['expected'] > 0 else 0
        if ratio > 2.0 or ratio < 0.5:
            extreme_ratios.append((error, ratio))
    
    if extreme_ratios:
        print(f"\n⚡ EXTREME PREDICTION RATIOS: {len(extreme_ratios)}")
        for case, ratio in extreme_ratios[:5]:
            print(f"   Case {case['case_index']}: ratio {ratio:.2f}, error ${case['error']:.2f}")
    
    # Pattern 5: Specific day ranges with consistent bias
    for day_count in range(1, 15):
        day_errors = [e for e in errors if e['days'] == day_count]
        if len(day_errors) >= 5:  # At least 5 cases
            avg_signed_error = sum(e['signed_error'] for e in day_errors) / len(day_errors)
            if abs(avg_signed_error) > 50:  # Systematic bias > $50
                bias_type = "under" if avg_signed_error > 0 else "over"
                print(f"\n📅 {day_count}-DAY TRIPS: {len(day_errors)} cases, systematic {bias_type}-prediction by ${abs(avg_signed_error):.2f}")
    
    return patterns

def top_50_detailed_analysis(errors):
    """Detailed analysis of top 50 worst cases"""
    
    print(f"\n🎯 TOP 50 WORST CASES - DETAILED ANALYSIS:")
    print("=" * 60)
    
    top_50 = errors[:50]
    
    for i, case in enumerate(top_50):
        print(f"\nRank {i+1:2d}: Case {case['case_index']:3d} - Error ${case['error']:6.2f}")
        print(f"   Input: {case['days']}d, {case['miles']:4.0f}mi, ${case['receipts']:7.2f}")
        print(f"   Expected: ${case['expected']:8.2f} | Predicted: ${case['predicted']:8.2f}")
        print(f"   Daily: ${case['daily_receipts']:6.2f}/day, {case['daily_miles']:5.1f}mi/day")
        print(f"   Error%: {case['error_percentage']:5.1f}%")
        
        # Identify potential rule candidates
        potential_rules = []
        
        if case['miles'] == 0:
            potential_rules.append("ZERO_MILES_RULE")
        if case['days'] >= 10:
            potential_rules.append("LONG_TRIP_RULE")
        if case['daily_receipts'] > 300:
            potential_rules.append("HIGH_DAILY_SPENDING_RULE")
        if case['receipts'] % 50 == 0:
            potential_rules.append("ROUND_RECEIPTS_RULE")
        if case['miles'] > 1500:
            potential_rules.append("ULTRA_HIGH_MILES_RULE")
        
        if potential_rules:
            print(f"   Candidates: {', '.join(potential_rules)}")

if __name__ == "__main__":
    print("🚀 STARTING COMPREHENSIVE ERROR ANALYSIS")
    
    errors = comprehensive_error_analysis()
    categories = categorize_errors_by_characteristics(errors)
    patterns = find_specific_patterns(errors)
    top_50_detailed_analysis(errors)
    
    print(f"\n✅ Analysis complete! Found {len(errors)} cases to debug.")
    print("💡 Ready to implement targeted fixes for each pattern.")