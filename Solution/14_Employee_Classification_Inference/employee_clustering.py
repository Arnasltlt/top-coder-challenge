#!/usr/bin/env python3
"""
Employee Classification Inference - Clustering Analysis

This script implements unsupervised clustering to identify hidden employee 
classifications in the reimbursement data.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import pandas as pd

def load_public_cases():
    """Load and parse the public cases data."""
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    cases = []
    for i, case in enumerate(data):
        inp = case['input']
        cases.append({
            'case_id': i,
            'days': inp['trip_duration_days'],
            'miles': inp['miles_traveled'],
            'receipts': inp['total_receipts_amount'],
            'expected': case['expected_output']
        })
    
    return cases

def create_feature_vectors(cases):
    """Create feature vectors for clustering analysis."""
    features = []
    
    for case in cases:
        days = case['days']
        miles = case['miles']
        receipts = case['receipts']
        expected = case['expected']
        
        # Avoid division by zero
        daily_spending = receipts / max(days, 1)
        daily_miles = miles / max(days, 1)
        daily_reimbursement = expected / max(days, 1)
        reimbursement_ratio = expected / max(receipts, 0.01)
        miles_per_dollar_receipts = miles / max(receipts, 0.01)
        
        feature_vector = [
            days,
            miles,
            receipts,
            daily_spending,
            daily_miles,
            daily_reimbursement,
            reimbursement_ratio,
            miles_per_dollar_receipts,
            expected
        ]
        
        features.append(feature_vector)
    
    return np.array(features)

def find_optimal_clusters(features, max_clusters=10):
    """Find the optimal number of clusters using elbow method and silhouette score."""
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    inertias = []
    silhouette_scores = []
    k_range = range(2, max_clusters + 1)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(features_scaled)
        
        inertias.append(kmeans.inertia_)
        sil_score = silhouette_score(features_scaled, cluster_labels)
        silhouette_scores.append(sil_score)
        
        print(f"k={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={sil_score:.3f}")
    
    # Find best k based on silhouette score
    best_k = k_range[np.argmax(silhouette_scores)]
    print(f"\nOptimal number of clusters: {best_k} (Silhouette: {max(silhouette_scores):.3f})")
    
    return best_k, scaler

def perform_clustering(cases, features, n_clusters, scaler):
    """Perform K-means clustering with the specified number of clusters."""
    features_scaled = scaler.transform(features)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(features_scaled)
    
    # Add cluster labels to cases
    for i, case in enumerate(cases):
        case['cluster'] = cluster_labels[i]
    
    return cases, kmeans

def analyze_clusters(cases, n_clusters):
    """Analyze the characteristics of each cluster."""
    print(f"\n=== CLUSTER ANALYSIS ({n_clusters} clusters) ===")
    
    for cluster_id in range(n_clusters):
        cluster_cases = [case for case in cases if case['cluster'] == cluster_id]
        
        if not cluster_cases:
            continue
        
        print(f"\n--- CLUSTER {cluster_id} ({len(cluster_cases)} cases) ---")
        
        # Calculate statistics
        days_list = [c['days'] for c in cluster_cases]
        miles_list = [c['miles'] for c in cluster_cases]
        receipts_list = [c['receipts'] for c in cluster_cases]
        expected_list = [c['expected'] for c in cluster_cases]
        
        daily_spending = [c['receipts']/max(c['days'],1) for c in cluster_cases]
        daily_miles = [c['miles']/max(c['days'],1) for c in cluster_cases]
        daily_reimbursement = [c['expected']/max(c['days'],1) for c in cluster_cases]
        reimbursement_ratio = [c['expected']/max(c['receipts'],0.01) for c in cluster_cases]
        
        print(f"Days: {np.mean(days_list):.1f} ± {np.std(days_list):.1f} (range: {min(days_list)}-{max(days_list)})")
        print(f"Miles: {np.mean(miles_list):.1f} ± {np.std(miles_list):.1f} (range: {min(miles_list)}-{max(miles_list)})")
        print(f"Receipts: ${np.mean(receipts_list):.2f} ± ${np.std(receipts_list):.2f}")
        print(f"Expected: ${np.mean(expected_list):.2f} ± ${np.std(expected_list):.2f}")
        print(f"Daily spending: ${np.mean(daily_spending):.2f} ± ${np.std(daily_spending):.2f}")
        print(f"Daily miles: {np.mean(daily_miles):.1f} ± {np.std(daily_miles):.1f}")
        print(f"Daily reimbursement: ${np.mean(daily_reimbursement):.2f} ± ${np.std(daily_reimbursement):.2f}")
        print(f"Reimbursement ratio: {np.mean(reimbursement_ratio):.2f} ± {np.std(reimbursement_ratio):.2f}")
        
        # Characterize the cluster
        avg_daily_spending = np.mean(daily_spending)
        avg_daily_miles = np.mean(daily_miles)
        avg_reimbursement_ratio = np.mean(reimbursement_ratio)
        
        # Business logic classification
        if avg_daily_spending > 200 and avg_daily_miles < 100:
            cluster_type = "EXECUTIVE (High spend, low miles)"
        elif avg_daily_miles > 300 and avg_daily_spending > 80:
            cluster_type = "SENIOR_SALES (High miles, moderate spend)"
        elif avg_daily_miles < 300 and avg_daily_spending < 120:
            cluster_type = "JUNIOR_SALES (Moderate miles and spend)"
        elif avg_daily_miles < 150 and avg_daily_spending < 80:
            cluster_type = "TECHNICAL (Low miles, low spend)"
        else:
            cluster_type = "REGIONAL_MGR (Balanced)"
        
        print(f"Inferred type: {cluster_type}")

def save_cluster_analysis(cases, n_clusters):
    """Save detailed cluster analysis to file."""
    with open('cluster_analysis.json', 'w') as f:
        analysis = {
            'n_clusters': n_clusters,
            'clusters': {}
        }
        
        for cluster_id in range(n_clusters):
            cluster_cases = [case for case in cases if case['cluster'] == cluster_id]
            
            if cluster_cases:
                days_list = [c['days'] for c in cluster_cases]
                miles_list = [c['miles'] for c in cluster_cases]
                receipts_list = [c['receipts'] for c in cluster_cases]
                expected_list = [c['expected'] for c in cluster_cases]
                
                daily_spending = [c['receipts']/max(c['days'],1) for c in cluster_cases]
                daily_miles = [c['miles']/max(c['days'],1) for c in cluster_cases]
                daily_reimbursement = [c['expected']/max(c['days'],1) for c in cluster_cases]
                reimbursement_ratio = [c['expected']/max(c['receipts'],0.01) for c in cluster_cases]
                
                analysis['clusters'][str(cluster_id)] = {
                    'count': len(cluster_cases),
                    'avg_days': float(np.mean(days_list)),
                    'avg_miles': float(np.mean(miles_list)),
                    'avg_receipts': float(np.mean(receipts_list)),
                    'avg_expected': float(np.mean(expected_list)),
                    'avg_daily_spending': float(np.mean(daily_spending)),
                    'avg_daily_miles': float(np.mean(daily_miles)),
                    'avg_daily_reimbursement': float(np.mean(daily_reimbursement)),
                    'avg_reimbursement_ratio': float(np.mean(reimbursement_ratio)),
                    'case_ids': [c['case_id'] for c in cluster_cases[:10]]  # First 10 cases
                }
        
        json.dump(analysis, f, indent=2)
        print(f"\nCluster analysis saved to cluster_analysis.json")

def main():
    print("Employee Classification Inference - Clustering Analysis")
    print("=" * 60)
    
    # Load data
    cases = load_public_cases()
    print(f"Loaded {len(cases)} public cases")
    
    # Create feature vectors
    features = create_feature_vectors(cases)
    print(f"Created feature vectors with {features.shape[1]} features")
    
    # Find optimal number of clusters
    optimal_k, scaler = find_optimal_clusters(features)
    
    # Perform clustering with optimal k
    cases_with_clusters, kmeans = perform_clustering(cases, features, optimal_k, scaler)
    
    # Analyze clusters
    analyze_clusters(cases_with_clusters, optimal_k)
    
    # Save analysis
    save_cluster_analysis(cases_with_clusters, optimal_k)
    
    # Save the trained model components
    import pickle
    with open('clustering_model.pkl', 'wb') as f:
        pickle.dump({
            'kmeans': kmeans,
            'scaler': scaler,
            'n_clusters': optimal_k
        }, f)
    
    print(f"\nClustering model saved to clustering_model.pkl")

if __name__ == "__main__":
    main()