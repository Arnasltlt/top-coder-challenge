#!/usr/bin/env python3
"""
Pattern Mining - Looking for exact patterns and "bugs" mentioned in interviews
Focus on rounding behaviors, magic numbers, and exact case matching like Team 11
"""

import json
import numpy as np
from collections import defaultdict

def load_cases():
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    return data

def analyze_rounding_patterns(data):
    """Look for the 'rounding bug' Lisa mentioned"""
    print("=== ROUNDING PATTERN ANALYSIS ===")
    
    # Group by receipt cent values
    cent_patterns = defaultdict(list)
    
    for i, case in enumerate(data):
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        # Get cents value of receipts
        receipt_cents = int(round(receipts * 100)) % 100
        cent_patterns[receipt_cents].append({
            'case_id': i,
            'receipts': receipts,
            'expected': expected,
            'days': case['input']['trip_duration_days'],
            'miles': case['input']['miles_traveled']
        })
    
    # Analyze patterns for specific cent values Lisa mentioned
    special_cents = [49, 99, 0, 25, 50, 75]
    
    for cents in special_cents:
        if cents in cent_patterns and len(cent_patterns[cents]) >= 3:
            cases = cent_patterns[cents]
            avg_reimbursement = np.mean([c['expected'] for c in cases])
            print(f"Receipts ending in .{cents:02d}: {len(cases)} cases, avg ${avg_reimbursement:.2f}")
            
            # Look for bonuses compared to nearby cent values
            nearby_cents = [(cents-1)%100, (cents+1)%100]
            for nearby in nearby_cents:
                if nearby in cent_patterns and len(cent_patterns[nearby]) >= 2:
                    nearby_avg = np.mean([c['expected'] for c in cent_patterns[nearby]])
                    bonus = avg_reimbursement - nearby_avg
                    if abs(bonus) > 10:  # Significant difference
                        print(f"  Potential bonus vs .{nearby:02d}: ${bonus:+.2f}")
    
    print()

def analyze_magic_numbers(data):
    """Look for Marcus's 'magic number' theory"""
    print("=== MAGIC NUMBER ANALYSIS ===")
    
    # Group by exact receipt amounts
    receipt_groups = defaultdict(list)
    
    for i, case in enumerate(data):
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        # Round to nearest dollar for grouping
        receipt_rounded = round(receipts)
        receipt_groups[receipt_rounded].append({
            'case_id': i,
            'receipts': receipts,
            'expected': expected,
            'days': case['input']['trip_duration_days'],
            'miles': case['input']['miles_traveled']
        })
    
    # Find receipt amounts that appear multiple times
    frequent_amounts = {amt: cases for amt, cases in receipt_groups.items() if len(cases) >= 3}
    
    print(f"Found {len(frequent_amounts)} receipt amounts with 3+ occurrences")
    
    # Look for unusually consistent reimbursements
    for amount, cases in frequent_amounts.items():
        reimbursements = [c['expected'] for c in cases]
        std_dev = np.std(reimbursements)
        mean_reimb = np.mean(reimbursements)
        
        if std_dev < 50:  # Very consistent
            print(f"${amount} receipts: {len(cases)} cases, ${mean_reimb:.2f} ± ${std_dev:.2f} (very consistent)")
    
    print()

def analyze_exact_patterns(data):
    """Look for exact input combinations that repeat"""
    print("=== EXACT PATTERN ANALYSIS ===")
    
    # Group by exact input combinations
    input_patterns = defaultdict(list)
    
    for i, case in enumerate(data):
        inp = case['input']
        key = (inp['trip_duration_days'], inp['miles_traveled'], inp['total_receipts_amount'])
        input_patterns[key].append({
            'case_id': i,
            'expected': case['expected_output']
        })
    
    # Find exact duplicates
    duplicates = {key: cases for key, cases in input_patterns.items() if len(cases) > 1}
    
    print(f"Found {len(duplicates)} exact input combinations with multiple occurrences:")
    
    for (days, miles, receipts), cases in duplicates.items():
        expected_values = [c['expected'] for c in cases]
        if len(set(expected_values)) == 1:
            print(f"  ({days}d, {miles}mi, ${receipts}) → ${expected_values[0]:.2f} ({len(cases)} identical)")
        else:
            print(f"  ({days}d, {miles}mi, ${receipts}) → varying: {expected_values} (INCONSISTENT!)")
    
    print()

def analyze_simple_formulas(data):
    """Look for cases that might follow simple formulas"""
    print("=== SIMPLE FORMULA ANALYSIS ===")
    
    # Test various simple formulas mentioned in interviews
    formulas = {
        'per_diem_100': lambda d, m, r: d * 100,
        'mileage_58cent': lambda d, m, r: m * 0.58,
        'receipts_80pct': lambda d, m, r: r * 0.8,
        'combined_basic': lambda d, m, r: d * 100 + m * 0.58 + r * 0.8,
        'combined_lisa': lambda d, m, r: d * 120 + m * 0.45 + r * 0.7,
    }
    
    for formula_name, formula_func in formulas.items():
        errors = []
        exact_matches = 0
        close_matches = 0
        
        for case in data:
            inp = case['input']
            expected = case['expected_output']
            predicted = formula_func(inp['trip_duration_days'], inp['miles_traveled'], inp['total_receipts_amount'])
            
            error = abs(expected - predicted)
            errors.append(error)
            
            if error <= 0.01:
                exact_matches += 1
            elif error <= 1.0:
                close_matches += 1
        
        avg_error = np.mean(errors)
        print(f"{formula_name}: {exact_matches} exact, {close_matches} close, ${avg_error:.2f} avg error")
    
    print()

def find_best_linear_model(data):
    """Find the best overall linear model"""
    print("=== BEST LINEAR MODEL SEARCH ===")
    
    X = []
    y = []
    
    for case in data:
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        
        # Try various feature combinations
        features = [
            days,
            miles,
            receipts,
            days * days,  # Quadratic terms
            miles * miles,
            receipts * receipts,
            days * miles,  # Interaction terms
            days * receipts,
            miles * receipts,
            np.sqrt(miles),  # Non-linear transforms
            np.log(max(receipts, 0.01)),
        ]
        
        X.append(features)
        y.append(case['expected_output'])
    
    X = np.array(X)
    y = np.array(y)
    
    # Fit comprehensive linear model
    from sklearn.linear_model import LinearRegression
    reg = LinearRegression()
    reg.fit(X, y)
    
    r_squared = reg.score(X, y)
    print(f"Comprehensive linear model R² = {r_squared:.4f}")
    
    # Count exact and close matches
    predictions = reg.predict(X)
    exact_matches = sum(1 for i in range(len(y)) if abs(y[i] - predictions[i]) <= 0.01)
    close_matches = sum(1 for i in range(len(y)) if abs(y[i] - predictions[i]) <= 1.0)
    
    print(f"Exact matches: {exact_matches}/1000 ({exact_matches/10:.1f}%)")
    print(f"Close matches: {close_matches}/1000 ({close_matches/10:.1f}%)")
    
    avg_error = np.mean([abs(y[i] - predictions[i]) for i in range(len(y))])
    print(f"Average error: ${avg_error:.2f}")
    
    # Save the best model
    model_data = {
        'coefficients': reg.coef_.tolist(),
        'intercept': float(reg.intercept_),
        'r_squared': float(r_squared),
        'exact_matches': int(exact_matches),
        'close_matches': int(close_matches),
        'avg_error': float(avg_error),
        'feature_names': ['days', 'miles', 'receipts', 'days²', 'miles²', 'receipts²', 
                         'days×miles', 'days×receipts', 'miles×receipts', '√miles', 'log(receipts)']
    }
    
    with open('best_linear_model.json', 'w') as f:
        json.dump(model_data, f, indent=2)
    
    print("Best linear model saved to best_linear_model.json")

def main():
    print("Advanced Pattern Mining - Looking for Hidden Rules")
    print("=" * 60)
    
    data = load_cases()
    print(f"Analyzing {len(data)} cases\n")
    
    # Run all analyses
    analyze_rounding_patterns(data)
    analyze_magic_numbers(data)
    analyze_exact_patterns(data)
    analyze_simple_formulas(data)
    find_best_linear_model(data)

if __name__ == "__main__":
    main()