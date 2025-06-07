#!/bin/bash

# EMPIRICAL LOOKUP SYSTEM - Like a real 60-year-old legacy system!
# Uses actual data patterns instead of mathematical formulas
# Usage: ./run_lookup.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Create bucket keys (same logic as training)
MILES_BUCKET=$(echo "($MILES / 100) * 100" | bc)
RECEIPTS_BUCKET=$(echo "($RECEIPTS / 250) * 250" | bc)

# Python helper to do the lookup
python3 -c "
import json
import sys

days = int(sys.argv[1])
miles_bucket = int(sys.argv[2])
receipts_bucket = int(sys.argv[3])
miles = int(sys.argv[4])
receipts = float(sys.argv[5])

# Load lookup table
with open('empirical_lookup.json', 'r') as f:
    data = json.load(f)

bucket_averages = {eval(k): v for k, v in data['bucket_averages'].items()}
bucket_counts = {eval(k): v for k, v in data['bucket_counts'].items()}

# Try exact bucket match first
exact_key = (days, miles_bucket, receipts_bucket)
if exact_key in bucket_averages:
    result = bucket_averages[exact_key]
    print(f'{result:.2f}')
    exit()

# Find similar buckets (same days, close miles/receipts)
similar_buckets = []
for key, avg in bucket_averages.items():
    key_days, key_miles, key_receipts = key
    if key_days == days:
        # Calculate similarity based on miles and receipts proximity
        miles_diff = abs(key_miles - miles_bucket)
        receipts_diff = abs(key_receipts - receipts_bucket)
        
        # Weight by bucket reliability (number of cases)
        weight = bucket_counts[key]
        
        if miles_diff <= 300 and receipts_diff <= 500:  # Reasonable proximity
            similarity = 1 / (1 + miles_diff/100 + receipts_diff/250) * weight
            similar_buckets.append((similarity, avg, key))

if similar_buckets:
    # Weighted average of similar buckets
    similar_buckets.sort(reverse=True)  # Best matches first
    
    total_weight = sum(sim for sim, _, _ in similar_buckets[:5])  # Top 5 matches
    weighted_sum = sum(sim * avg for sim, avg, _ in similar_buckets[:5])
    
    result = weighted_sum / total_weight if total_weight > 0 else 0
    print(f'{result:.2f}')
    exit()

# Fallback: Look for any buckets with same days
day_buckets = [(avg, key) for key, avg in bucket_averages.items() if key[0] == days]
if day_buckets:
    # Simple average of all same-day buckets
    avg_reimbursement = sum(avg for avg, _ in day_buckets) / len(day_buckets)
    print(f'{avg_reimbursement:.2f}')
    exit()

# Last resort: Very simple calculation
base = days * 100 + miles * 0.5 + receipts * 0.3
print(f'{base:.2f}')

" $DAYS $MILES_BUCKET $RECEIPTS_BUCKET $MILES $RECEIPTS