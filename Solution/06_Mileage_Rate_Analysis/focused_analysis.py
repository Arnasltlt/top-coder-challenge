#!/usr/bin/env python3
import json
from collections import defaultdict

def focused_analysis():
    # Read the JSON file
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    # Look for cases with minimal receipts to understand base structure
    print("=== CASES WITH MINIMAL RECEIPTS (< $2) ===")
    
    minimal_receipts = []
    for case in data:
        if case['input']['total_receipts_amount'] < 2.0:
            minimal_receipts.append(case)
    
    minimal_receipts.sort(key=lambda x: (x['input']['trip_duration_days'], x['input']['miles_traveled']))
    
    print(f"Found {len(minimal_receipts)} cases with receipts < $2")
    print("Days | Miles | Receipts | Output | Non-Receipt Component")
    print("-" * 55)
    
    for case in minimal_receipts:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        non_receipt = output - receipts
        
        print(f"{days:4d} | {miles:5.0f} | ${receipts:7.2f} | ${output:7.2f} | ${non_receipt:7.2f}")
    
    # Let's look at patterns by analyzing the relationship between days and non-receipt component
    print(f"\n=== ANALYZING BASE RATES BY TRIP DURATION ===")
    
    by_days = defaultdict(list)
    for case in minimal_receipts:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        non_receipt = output - receipts
        
        by_days[days].append({
            'miles': miles,
            'receipts': receipts,
            'output': output,
            'non_receipt': non_receipt
        })
    
    for days in sorted(by_days.keys()):
        cases = by_days[days]
        print(f"\n{days}-day trips:")
        print("Miles | Receipts | Output | Non-Receipt | Est. Per-Mile")
        print("-" * 55)
        
        for case in cases:
            per_mile = case['non_receipt'] / case['miles'] if case['miles'] > 0 else 0
            print(f"{case['miles']:5.0f} | ${case['receipts']:7.2f} | ${case['output']:7.2f} | "
                  f"${case['non_receipt']:7.2f} | ${per_mile:.4f}")
    
    # Let's try to infer the structure: base daily allowance + mileage
    print(f"\n=== INFERRING STRUCTURE: BASE DAILY + MILEAGE ===")
    
    # Use 1-day trips to find base daily allowance
    one_day_cases = by_days.get(1, [])
    if one_day_cases:
        print("Assuming structure: Daily_Base + (Miles * Rate)")
        
        # Try different base daily allowances
        for base_daily in [50, 55, 60, 65, 70, 75, 80]:
            print(f"\nTesting base daily allowance: ${base_daily}")
            rates = []
            
            for case in one_day_cases:
                mileage_component = case['non_receipt'] - base_daily
                if case['miles'] > 0:
                    rate = mileage_component / case['miles']
                    rates.append(rate)
                    print(f"  {case['miles']:3.0f} miles: ${mileage_component:6.2f} / {case['miles']:3.0f} = ${rate:.4f} per mile")
            
            if rates:
                avg_rate = sum(rates) / len(rates)
                print(f"  Average rate: ${avg_rate:.4f} per mile")
    
    # Look at patterns in multi-day trips
    print(f"\n=== TESTING MULTI-DAY PATTERNS ===")
    
    # Test if multi-day follows: (Days * Base) + (Miles * Rate)
    for days in sorted(by_days.keys()):
        if days == 1:
            continue
            
        cases = by_days[days]
        print(f"\n{days}-day trips:")
        
        # Test with different base daily rates
        for base_daily in [55, 60, 65, 70]:
            print(f"  Testing base daily: ${base_daily}")
            rates = []
            
            for case in cases[:3]:  # Just first 3 cases
                estimated_daily_component = days * base_daily
                mileage_component = case['non_receipt'] - estimated_daily_component
                if case['miles'] > 0:
                    rate = mileage_component / case['miles']
                    rates.append(rate)
                    print(f"    {case['miles']:3.0f} miles: (${case['non_receipt']:.2f} - ${estimated_daily_component}) / {case['miles']:3.0f} = ${rate:.4f}")
            
            if rates:
                avg_rate = sum(rates) / len(rates)
                print(f"    Average rate: ${avg_rate:.4f}")

if __name__ == "__main__":
    focused_analysis()