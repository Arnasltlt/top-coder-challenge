#!/usr/bin/env python3
"""
Employee Classification Inference - Reimbursement Rules Analysis

This script analyzes the discovered clusters to derive specific reimbursement 
rules for each employee class.
"""

import json
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

def load_cluster_data():
    """Load the cluster analysis results."""
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        public_cases = json.load(f)
    
    with open('cluster_analysis.json', 'r') as f:
        cluster_analysis = json.load(f)
    
    with open('clustering_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    return public_cases, cluster_analysis, model_data

def analyze_cluster_rules(public_cases, cluster_analysis):
    """Analyze reimbursement rules for each cluster."""
    
    # Assign cluster labels to cases
    with open('clustering_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    kmeans = model_data['kmeans']
    scaler = model_data['scaler']
    
    # Recreate features for all cases
    features = []
    for case in public_cases:
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']
        
        daily_spending = receipts / max(days, 1)
        daily_miles = miles / max(days, 1)
        daily_reimbursement = expected / max(days, 1)
        reimbursement_ratio = expected / max(receipts, 0.01)
        miles_per_dollar_receipts = miles / max(receipts, 0.01)
        
        feature_vector = [
            days, miles, receipts, daily_spending, daily_miles,
            daily_reimbursement, reimbursement_ratio, miles_per_dollar_receipts, expected
        ]
        features.append(feature_vector)
    
    features = np.array(features)
    features_scaled = scaler.transform(features)
    cluster_labels = kmeans.predict(features_scaled)
    
    # Analyze each cluster's reimbursement patterns
    cluster_rules = {}
    
    for cluster_id in range(model_data['n_clusters']):
        cluster_cases = []
        for i, label in enumerate(cluster_labels):
            if label == cluster_id:
                inp = public_cases[i]['input']
                cluster_cases.append({
                    'days': inp['trip_duration_days'],
                    'miles': inp['miles_traveled'],
                    'receipts': inp['total_receipts_amount'],
                    'expected': public_cases[i]['expected_output']
                })
        
        if not cluster_cases:
            continue
        
        print(f"\n=== CLUSTER {cluster_id} RULE ANALYSIS ({len(cluster_cases)} cases) ===")
        
        # Prepare data for regression analysis
        X = []
        y = []
        
        for case in cluster_cases:
            X.append([case['days'], case['miles'], case['receipts']])
            y.append(case['expected'])
        
        X = np.array(X)
        y = np.array(y)
        
        # Fit linear regression
        reg = LinearRegression()
        reg.fit(X, y)
        
        days_coef = reg.coef_[0]
        miles_coef = reg.coef_[1]
        receipts_coef = reg.coef_[2]
        intercept = reg.intercept_
        
        print(f"Linear regression coefficients:")
        print(f"  Days: ${days_coef:.2f}")
        print(f"  Miles: ${miles_coef:.4f}")
        print(f"  Receipts: {receipts_coef:.4f}")
        print(f"  Intercept: ${intercept:.2f}")
        print(f"  R² score: {reg.score(X, y):.3f}")
        
        # Analyze per-unit rates
        total_days = sum(case['days'] for case in cluster_cases)
        total_miles = sum(case['miles'] for case in cluster_cases)
        total_receipts = sum(case['receipts'] for case in cluster_cases)
        total_expected = sum(case['expected'] for case in cluster_cases)
        
        avg_per_day = total_expected / total_days if total_days > 0 else 0
        avg_per_mile = total_expected / total_miles if total_miles > 0 else 0
        avg_receipt_multiplier = total_expected / total_receipts if total_receipts > 0 else 0
        
        print(f"Average rates:")
        print(f"  Per day: ${avg_per_day:.2f}")
        print(f"  Per mile: ${avg_per_mile:.4f}")
        print(f"  Receipt multiplier: {avg_receipt_multiplier:.4f}")
        
        # Analyze mileage tiers
        miles_list = [case['miles'] for case in cluster_cases]
        expected_list = [case['expected'] for case in cluster_cases]
        
        # Sort by miles to analyze tier patterns
        sorted_data = sorted(zip(miles_list, expected_list))
        
        # Analyze low, medium, high mileage patterns
        n = len(sorted_data)
        low_third = sorted_data[:n//3]
        mid_third = sorted_data[n//3:2*n//3]
        high_third = sorted_data[2*n//3:]
        
        if low_third:
            low_miles_avg = np.mean([x[0] for x in low_third])
            low_expected_avg = np.mean([x[1] for x in low_third])
            low_rate = low_expected_avg / low_miles_avg if low_miles_avg > 0 else 0
            print(f"  Low mileage (avg {low_miles_avg:.0f} miles): ${low_rate:.4f}/mile")
        
        if mid_third:
            mid_miles_avg = np.mean([x[0] for x in mid_third])
            mid_expected_avg = np.mean([x[1] for x in mid_third])
            mid_rate = mid_expected_avg / mid_miles_avg if mid_miles_avg > 0 else 0
            print(f"  Mid mileage (avg {mid_miles_avg:.0f} miles): ${mid_rate:.4f}/mile")
        
        if high_third:
            high_miles_avg = np.mean([x[0] for x in high_third])
            high_expected_avg = np.mean([x[1] for x in high_third])
            high_rate = high_expected_avg / high_miles_avg if high_miles_avg > 0 else 0
            print(f"  High mileage (avg {high_miles_avg:.0f} miles): ${high_rate:.4f}/mile")
        
        # Store rules for this cluster
        cluster_rules[cluster_id] = {
            'linear_coeffs': {
                'days': float(days_coef),
                'miles': float(miles_coef),
                'receipts': float(receipts_coef),
                'intercept': float(intercept)
            },
            'avg_rates': {
                'per_day': float(avg_per_day),
                'per_mile': float(avg_per_mile),
                'receipt_multiplier': float(avg_receipt_multiplier)
            },
            'r_squared': float(reg.score(X, y)),
            'count': len(cluster_cases)
        }
    
    return cluster_rules

def derive_classification_rules(cluster_analysis, cluster_rules):
    """Derive rules for classifying new cases into clusters."""
    
    print(f"\n=== CLASSIFICATION RULES ===")
    
    # Based on the cluster analysis, derive classification thresholds
    cluster_0 = cluster_analysis['clusters']['0']  # Longer trips (avg 7.8 days)
    cluster_1 = cluster_analysis['clusters']['1']  # Short trips (avg 1.5 days)
    
    # The main distinguishing factor is trip duration
    day_threshold = (cluster_0['avg_days'] + cluster_1['avg_days']) / 2
    
    print(f"Primary classification rule: Trip duration")
    print(f"  Short trips (≤ {day_threshold:.1f} days) → Cluster 1 (High daily rates)")
    print(f"  Long trips (> {day_threshold:.1f} days) → Cluster 0 (Lower daily rates)")
    
    # Secondary factors
    daily_spending_threshold = (cluster_0['avg_daily_spending'] + cluster_1['avg_daily_spending']) / 2
    daily_miles_threshold = (cluster_0['avg_daily_miles'] + cluster_1['avg_daily_miles']) / 2
    
    print(f"Secondary factors:")
    print(f"  Daily spending threshold: ${daily_spending_threshold:.0f}")
    print(f"  Daily miles threshold: {daily_miles_threshold:.0f}")
    
    classification_rules = {
        'day_threshold': day_threshold,
        'daily_spending_threshold': daily_spending_threshold,
        'daily_miles_threshold': daily_miles_threshold
    }
    
    return classification_rules

def save_reimbursement_model(cluster_rules, classification_rules):
    """Save the complete reimbursement model."""
    
    model = {
        'classification_rules': classification_rules,
        'cluster_rules': cluster_rules,
        'model_type': 'employee_classification_inference'
    }
    
    with open('reimbursement_model.json', 'w') as f:
        json.dump(model, f, indent=2)
    
    print(f"\nReimbursement model saved to reimbursement_model.json")

def main():
    print("Employee Classification Inference - Reimbursement Rules Analysis")
    print("=" * 70)
    
    # Load data
    public_cases, cluster_analysis, model_data = load_cluster_data()
    
    # Analyze cluster-specific rules
    cluster_rules = analyze_cluster_rules(public_cases, cluster_analysis)
    
    # Derive classification rules
    classification_rules = derive_classification_rules(cluster_analysis, cluster_rules)
    
    # Save the complete model
    save_reimbursement_model(cluster_rules, classification_rules)

if __name__ == "__main__":
    main()