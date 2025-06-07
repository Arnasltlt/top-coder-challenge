#!/usr/bin/env python3
import json
import sys
from collections import defaultdict

def analyze_mileage_data():
    # Read the JSON file
    with open('/Users/seima/8090/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    print(f"Total test cases: {len(data)}")
    
    # Group by trip_duration_days to analyze mileage patterns
    by_duration = defaultdict(list)
    
    for case in data:
        duration = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        by_duration[duration].append({
            'miles': miles,
            'receipts': receipts,
            'output': output
        })
    
    print(f"\nBreakdown by trip duration:")
    for duration in sorted(by_duration.keys()):
        print(f"  {duration} days: {len(by_duration[duration])} cases")
    
    # Analyze 1-day trips first (should be easiest to isolate mileage component)
    print(f"\n=== ANALYZING 1-DAY TRIPS ===")
    one_day_trips = by_duration[1]
    
    # Sort by miles traveled
    one_day_trips.sort(key=lambda x: x['miles'])
    
    print(f"Total 1-day trips: {len(one_day_trips)}")
    print("\nSample of 1-day trips (sorted by miles):")
    print("Miles | Receipts | Output | Est. Per-Mile Rate")
    print("-" * 50)
    
    for i in range(0, min(50, len(one_day_trips)), 3):  # Every 3rd sample
        trip = one_day_trips[i]
        # Try to estimate per-mile rate (very rough approximation)
        estimated_rate = (trip['output'] - trip['receipts']) / trip['miles'] if trip['miles'] > 0 else 0
        print(f"{trip['miles']:4.0f} | ${trip['receipts']:7.2f} | ${trip['output']:7.2f} | ${estimated_rate:.3f}")
    
    # Look for patterns with minimal receipts
    print(f"\n=== 1-DAY TRIPS WITH LOW RECEIPTS (< $5) ===")
    low_receipt_trips = [t for t in one_day_trips if t['receipts'] < 5.0]
    low_receipt_trips.sort(key=lambda x: x['miles'])
    
    print("Miles | Receipts | Output | Mileage Component | Per-Mile Rate")
    print("-" * 65)
    
    for trip in low_receipt_trips[:20]:
        mileage_component = trip['output'] - trip['receipts']
        per_mile_rate = mileage_component / trip['miles'] if trip['miles'] > 0 else 0
        print(f"{trip['miles']:4.0f} | ${trip['receipts']:7.2f} | ${trip['output']:7.2f} | ${mileage_component:8.2f} | ${per_mile_rate:.4f}")
    
    # Check for tiered rates
    print(f"\n=== CHECKING FOR TIERED RATES (1-day trips, low receipts) ===")
    
    # Group by mile ranges
    ranges = [(0, 50), (51, 100), (101, 200), (201, 400), (401, 800), (801, 1000)]
    
    for min_miles, max_miles in ranges:
        range_trips = [t for t in low_receipt_trips 
                      if min_miles <= t['miles'] <= max_miles]
        
        if range_trips:
            rates = []
            for trip in range_trips:
                mileage_component = trip['output'] - trip['receipts']
                rate = mileage_component / trip['miles']
                rates.append(rate)
            
            avg_rate = sum(rates) / len(rates)
            min_rate = min(rates)
            max_rate = max(rates)
            
            print(f"Miles {min_miles:3d}-{max_miles:3d}: {len(range_trips):3d} trips, "
                  f"avg rate: ${avg_rate:.4f}, range: ${min_rate:.4f}-${max_rate:.4f}")
    
    # Look at some 2-day and 3-day trips for comparison
    print(f"\n=== COMPARING WITH MULTI-DAY TRIPS ===")
    
    for days in [2, 3]:
        trips = by_duration[days]
        low_receipt_trips = [t for t in trips if t['receipts'] < 10.0]
        low_receipt_trips.sort(key=lambda x: x['miles'])
        
        print(f"\n{days}-day trips with low receipts (< $10):")
        print("Miles | Receipts | Output | Estimated Mileage | Per-Mile")
        print("-" * 55)
        
        for trip in low_receipt_trips[:10]:
            # Rough estimate: assume some base amount per day
            estimated_daily_base = 50 * days  # This is a guess
            mileage_component = trip['output'] - trip['receipts'] - estimated_daily_base
            per_mile_rate = mileage_component / trip['miles'] if trip['miles'] > 0 else 0
            print(f"{trip['miles']:4.0f} | ${trip['receipts']:7.2f} | ${trip['output']:7.2f} | "
                  f"${mileage_component:8.2f} | ${per_mile_rate:.4f}")

if __name__ == "__main__":
    analyze_mileage_data()