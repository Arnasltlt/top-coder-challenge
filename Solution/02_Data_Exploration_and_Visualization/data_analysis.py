#!/usr/bin/env python3

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_data():
    """Load and parse the public_cases.json file"""
    data_path = Path("../../public_cases.json")
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Extract input features and reimbursement amounts
    records = []
    for case in data:
        record = {
            'trip_duration_days': case['input']['trip_duration_days'],
            'miles_traveled': case['input']['miles_traveled'],
            'total_receipts_amount': case['input']['total_receipts_amount'],
            'reimbursement_amount': case['expected_output']
        }
        records.append(record)
    
    return pd.DataFrame(records)

def calculate_summary_stats(df):
    """Calculate and display summary statistics"""
    print("=== SUMMARY STATISTICS ===\n")
    
    variables = ['trip_duration_days', 'miles_traveled', 'total_receipts_amount', 'reimbursement_amount']
    
    for var in variables:
        print(f"{var.upper().replace('_', ' ')}:")
        print(f"  Mean:   {df[var].mean():.2f}")
        print(f"  Median: {df[var].median():.2f}")
        print(f"  Min:    {df[var].min():.2f}")
        print(f"  Max:    {df[var].max():.2f}")
        print(f"  Std:    {df[var].std():.2f}")
        print()

def create_histograms(df):
    """Generate histograms for each variable"""
    variables = ['trip_duration_days', 'miles_traveled', 'total_receipts_amount', 'reimbursement_amount']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Distribution of Variables', fontsize=16)
    
    for i, var in enumerate(variables):
        row, col = i // 2, i % 2
        axes[row, col].hist(df[var], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[row, col].set_title(f'{var.replace("_", " ").title()}')
        axes[row, col].set_xlabel(var.replace('_', ' ').title())
        axes[row, col].set_ylabel('Frequency')
        axes[row, col].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('variable_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Histograms saved as 'variable_distributions.png'")

def create_scatter_plots(df):
    """Generate scatter plots showing relationships with reimbursement amount"""
    input_vars = ['trip_duration_days', 'miles_traveled', 'total_receipts_amount']
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Relationship Between Inputs and Reimbursement Amount', fontsize=16)
    
    for i, var in enumerate(input_vars):
        axes[i].scatter(df[var], df['reimbursement_amount'], alpha=0.6, color='coral')
        axes[i].set_xlabel(var.replace('_', ' ').title())
        axes[i].set_ylabel('Reimbursement Amount')
        axes[i].set_title(f'Reimbursement vs {var.replace("_", " ").title()}')
        axes[i].grid(True, alpha=0.3)
        
        # Add correlation coefficient
        corr = df[var].corr(df['reimbursement_amount'])
        axes[i].text(0.05, 0.95, f'Correlation: {corr:.3f}', 
                    transform=axes[i].transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('input_vs_reimbursement_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Scatter plots saved as 'input_vs_reimbursement_scatter.png'")

def analyze_patterns(df):
    """Analyze and report key findings"""
    print("\n=== DATA ANALYSIS FINDINGS ===\n")
    
    print(f"Dataset contains {len(df)} travel reimbursement cases\n")
    
    # Correlation analysis
    input_vars = ['trip_duration_days', 'miles_traveled', 'total_receipts_amount']
    print("CORRELATION WITH REIMBURSEMENT AMOUNT:")
    for var in input_vars:
        corr = df[var].corr(df['reimbursement_amount'])
        print(f"  {var.replace('_', ' ').title()}: {corr:.3f}")
    
    print("\nKEY PATTERNS OBSERVED:")
    
    # Trip duration patterns
    trip_corr = df['trip_duration_days'].corr(df['reimbursement_amount'])
    print(f"• Trip duration shows {'strong' if abs(trip_corr) > 0.7 else 'moderate' if abs(trip_corr) > 0.4 else 'weak'} correlation ({trip_corr:.3f}) with reimbursement")
    
    # Miles patterns
    miles_corr = df['miles_traveled'].corr(df['reimbursement_amount'])
    print(f"• Miles traveled shows {'strong' if abs(miles_corr) > 0.7 else 'moderate' if abs(miles_corr) > 0.4 else 'weak'} correlation ({miles_corr:.3f}) with reimbursement")
    
    # Receipts patterns
    receipts_corr = df['total_receipts_amount'].corr(df['reimbursement_amount'])
    print(f"• Receipt amounts show {'strong' if abs(receipts_corr) > 0.7 else 'moderate' if abs(receipts_corr) > 0.4 else 'weak'} correlation ({receipts_corr:.3f}) with reimbursement")
    
    # Range analysis
    print(f"\nRANGE ANALYSIS:")
    print(f"• Trip durations range from {df['trip_duration_days'].min()} to {df['trip_duration_days'].max()} days")
    print(f"• Miles traveled range from {df['miles_traveled'].min()} to {df['miles_traveled'].max()} miles")
    print(f"• Receipt amounts range from ${df['total_receipts_amount'].min():.2f} to ${df['total_receipts_amount'].max():.2f}")
    print(f"• Reimbursements range from ${df['reimbursement_amount'].min():.2f} to ${df['reimbursement_amount'].max():.2f}")

def main():
    # Load data
    df = load_data()
    print(f"Loaded {len(df)} records from public_cases.json\n")
    
    # Calculate summary statistics
    calculate_summary_stats(df)
    
    # Create visualizations
    create_histograms(df)
    create_scatter_plots(df)
    
    # Analyze patterns
    analyze_patterns(df)

if __name__ == "__main__":
    main()