#!/bin/bash

# SIMILARITY MATCHING APPROACH
# Find closest cases in training data and use their reimbursement amounts
# Like a 60-year-old system with lookup tables
# Usage: ./run_similarity_match.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Use Python for similarity calculation
python3 -c "
import json
import sys
import math

days = int(sys.argv[1])
miles = int(sys.argv[2])
receipts = float(sys.argv[3])

# Load training data
with open('../public_cases.json', 'r') as f:
    cases = json.load(f)

# Find most similar cases using weighted distance
best_matches = []

for case in cases:
    train_days = case['input']['trip_duration_days']
    train_miles = case['input']['miles_traveled']
    train_receipts = case['input']['total_receipts_amount']
    train_output = case['expected_output']
    
    # Calculate weighted similarity (days most important, then receipts, then miles)
    days_diff = abs(train_days - days)
    miles_diff = abs(train_miles - miles) / 100  # Scale down miles
    receipts_diff = abs(train_receipts - receipts) / 100  # Scale down receipts
    
    # Weighted distance (days weighted heavily)
    distance = days_diff * 3 + receipts_diff + miles_diff
    
    best_matches.append((distance, train_output, case))

# Sort by similarity and take top matches
best_matches.sort()

# Use top 5 most similar cases for prediction
top_matches = best_matches[:5]

if len(top_matches) > 0:
    # Weight by inverse distance
    total_weight = 0
    weighted_sum = 0
    
    for distance, output, case in top_matches:
        weight = 1 / (1 + distance)  # Inverse distance weighting
        weighted_sum += weight * output
        total_weight += weight
    
    if total_weight > 0:
        result = weighted_sum / total_weight
    else:
        result = top_matches[0][1]  # Fallback to closest match
    
    print(f'{result:.2f}')
else:
    # Fallback calculation
    print(f'{(days * 150 + miles * 0.5 + receipts * 0.3):.2f}')

" $DAYS $MILES $RECEIPTS