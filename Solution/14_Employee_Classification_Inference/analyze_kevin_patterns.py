#!/usr/bin/env python3
"""
Advanced Pattern Analysis - Based on Kevin's Insights
Implementing the multi-path system Kevin described
"""

import json
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def load_and_analyze():
    """Load public cases and analyze using Kevin's framework"""
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    cases = []
    for i, case in enumerate(data):
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']
        
        # Kevin's key metrics
        efficiency = miles / max(days, 1)  # Miles per day
        spending_per_day = receipts / max(days, 1)
        
        cases.append({
            'case_id': i,
            'days': days,
            'miles': miles,
            'receipts': receipts,
            'expected': expected,
            'efficiency': efficiency,
            'spending_per_day': spending_per_day,
            'total_spending': receipts
        })
    
    return cases

def classify_trips_kevin_style(cases):
    """Classify trips into Kevin's 6 categories"""
    
    categories = {
        'quick_high_mileage': [],    # Short trips, high efficiency
        'long_low_mileage': [],      # Long trips, low efficiency  
        'medium_balanced': [],       # Medium trips, balanced
        'efficiency_sweet_spot': [], # Kevin's 180-220 miles/day sweet spot
        'vacation_penalty': [],      # 8+ days with high spending
        'sweet_spot_combo': []       # 5-day, 180+ miles/day, <$100/day
    }
    
    for case in cases:
        days = case['days']
        efficiency = case['efficiency']
        spending_per_day = case['spending_per_day']
        
        # Kevin's "sweet spot combo": 5-day trips with 180+ miles/day and <$100/day
        if (days == 5 and efficiency >= 180 and spending_per_day < 100):
            categories['sweet_spot_combo'].append(case)
        # Kevin's "vacation penalty": 8+ day trips with high spending
        elif (days >= 8 and spending_per_day > 120):
            categories['vacation_penalty'].append(case)
        # Efficiency sweet spot: 180-220 miles per day
        elif (180 <= efficiency <= 220):
            categories['efficiency_sweet_spot'].append(case)
        # Quick high mileage: ≤3 days, high efficiency
        elif (days <= 3 and efficiency > 200):
            categories['quick_high_mileage'].append(case)
        # Long low mileage: ≥7 days, low efficiency  
        elif (days >= 7 and efficiency < 100):
            categories['long_low_mileage'].append(case)
        # Everything else is medium balanced
        else:
            categories['medium_balanced'].append(case)
    
    return categories

def analyze_category_patterns(categories):
    """Analyze reimbursement patterns for each category"""
    
    print("=== KEVIN'S TRIP CATEGORY ANALYSIS ===\n")
    
    category_models = {}
    
    for cat_name, cat_cases in categories.items():
        if len(cat_cases) < 5:  # Need minimum cases for analysis
            continue
            
        print(f"--- {cat_name.upper()} ({len(cat_cases)} cases) ---")
        
        # Basic statistics
        days_list = [c['days'] for c in cat_cases]
        efficiency_list = [c['efficiency'] for c in cat_cases]
        spending_list = [c['spending_per_day'] for c in cat_cases]
        expected_list = [c['expected'] for c in cat_cases]
        
        print(f"Days: {np.mean(days_list):.1f} ± {np.std(days_list):.1f}")
        print(f"Efficiency (mi/day): {np.mean(efficiency_list):.1f} ± {np.std(efficiency_list):.1f}")
        print(f"Spending/day: ${np.mean(spending_list):.2f} ± ${np.std(spending_list):.2f}")
        print(f"Avg reimbursement: ${np.mean(expected_list):.2f} ± ${np.std(expected_list):.2f}")
        
        # Fit regression model
        X = []
        y = []
        for case in cat_cases:
            # Include interaction terms Kevin mentioned
            features = [
                case['days'],
                case['miles'], 
                case['receipts'],
                case['efficiency'],
                case['spending_per_day'],
                case['days'] * case['efficiency'],  # Trip length × efficiency
                case['spending_per_day'] * case['miles'],  # Spending × mileage
                case['days'] * case['spending_per_day'],   # Length × daily spending
            ]
            X.append(features)
            y.append(case['expected'])
        
        X = np.array(X)
        y = np.array(y)
        
        if len(X) > 3:  # Need minimum for regression
            reg = LinearRegression()
            reg.fit(X, y)
            r_squared = reg.score(X, y)
            
            print(f"R² score: {r_squared:.3f}")
            print(f"Coefficients: days={reg.coef_[0]:.2f}, miles={reg.coef_[1]:.4f}, receipts={reg.coef_[2]:.4f}")
            print(f"Intercept: ${reg.intercept_:.2f}")
            
            category_models[cat_name] = {
                'model': reg,
                'r_squared': r_squared,
                'feature_names': ['days', 'miles', 'receipts', 'efficiency', 'spending_per_day', 
                                'days_x_efficiency', 'spending_x_miles', 'days_x_spending']
            }
        
        print()
    
    return category_models

def analyze_bonuses_and_penalties(cases):
    """Analyze specific bonuses and penalties Kevin identified"""
    
    print("=== BONUS/PENALTY ANALYSIS ===\n")
    
    # 5-day bonus analysis
    five_day_cases = [c for c in cases if c['days'] == 5]
    other_cases = [c for c in cases if c['days'] in [4, 6]]  # Compare to nearby lengths
    
    if five_day_cases and other_cases:
        five_day_avg = np.mean([c['expected'] for c in five_day_cases])
        other_avg = np.mean([c['expected'] for c in other_cases])
        print(f"5-day trips: ${five_day_avg:.2f} avg reimbursement ({len(five_day_cases)} cases)")
        print(f"4&6-day trips: ${other_avg:.2f} avg reimbursement ({len(other_cases)} cases)")
        print(f"5-day bonus: ${five_day_avg - other_avg:.2f} ({((five_day_avg/other_avg-1)*100):+.1f}%)\n")
    
    # Efficiency bonus analysis
    high_eff_cases = [c for c in cases if 180 <= c['efficiency'] <= 220]
    low_eff_cases = [c for c in cases if c['efficiency'] < 100]
    
    if high_eff_cases and low_eff_cases:
        high_eff_avg = np.mean([c['expected'] for c in high_eff_cases])
        low_eff_avg = np.mean([c['expected'] for c in low_eff_cases])
        print(f"High efficiency (180-220): ${high_eff_avg:.2f} ({len(high_eff_cases)} cases)")
        print(f"Low efficiency (<100): ${low_eff_avg:.2f} ({len(low_eff_cases)} cases)")
        print(f"Efficiency bonus: ${high_eff_avg - low_eff_avg:.2f}\n")
    
    # Receipt threshold analysis
    low_receipt_cases = [c for c in cases if c['spending_per_day'] < 50]
    high_receipt_cases = [c for c in cases if c['spending_per_day'] > 150]
    medium_receipt_cases = [c for c in cases if 80 <= c['spending_per_day'] <= 120]
    
    if all([low_receipt_cases, high_receipt_cases, medium_receipt_cases]):
        low_avg = np.mean([c['expected'] for c in low_receipt_cases])
        high_avg = np.mean([c['expected'] for c in high_receipt_cases]) 
        medium_avg = np.mean([c['expected'] for c in medium_receipt_cases])
        
        print(f"Low spending (<$50/day): ${low_avg:.2f} ({len(low_receipt_cases)} cases)")
        print(f"Medium spending ($80-120/day): ${medium_avg:.2f} ({len(medium_receipt_cases)} cases)")
        print(f"High spending (>$150/day): ${high_avg:.2f} ({len(high_receipt_cases)} cases)")

def save_kevin_model(category_models, cases):
    """Save the Kevin-inspired model"""
    
    model_data = {
        'model_type': 'kevin_multi_path',
        'categories': {}
    }
    
    for cat_name, cat_data in category_models.items():
        model_data['categories'][cat_name] = {
            'coefficients': cat_data['model'].coef_.tolist(),
            'intercept': float(cat_data['model'].intercept_),
            'r_squared': float(cat_data['r_squared']),
            'feature_names': cat_data['feature_names']
        }
    
    with open('kevin_model.json', 'w') as f:
        json.dump(model_data, f, indent=2)
    
    print(f"Kevin-inspired model saved to kevin_model.json")

def main():
    print("Advanced Pattern Analysis - Kevin's Multi-Path System")
    print("=" * 60)
    
    # Load and analyze data
    cases = load_and_analyze()
    print(f"Loaded {len(cases)} cases")
    
    # Classify trips using Kevin's framework
    categories = classify_trips_kevin_style(cases)
    
    # Analyze each category
    category_models = analyze_category_patterns(categories)
    
    # Analyze bonuses and penalties
    analyze_bonuses_and_penalties(cases)
    
    # Save the model
    save_kevin_model(category_models, cases)

if __name__ == "__main__":
    main()