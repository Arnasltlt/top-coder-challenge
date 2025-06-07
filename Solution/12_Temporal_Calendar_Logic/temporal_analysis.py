#!/usr/bin/env python3
"""
Temporal/Calendar Logic Analysis for ACME Reimbursement System
Strategy 12: Find hidden temporal patterns in the legacy 1960s system
"""

import json
import sys
from datetime import datetime, timedelta
import statistics
import math

def load_public_cases():
    """Load public cases and assign proxy dates"""
    with open('../../public_cases.json', 'r') as f:
        cases = json.load(f)
    
    # Assign proxy dates assuming chronological order
    # Start from a fictional 1960s date - fiscal year starting April 1, 1960
    base_date = datetime(1960, 4, 1)
    
    for i, case in enumerate(cases):
        # Spread cases across ~3 years, roughly 1 case per day
        case['proxy_date'] = base_date + timedelta(days=i)
        case['index'] = i
        case['fiscal_quarter'] = get_fiscal_quarter(case['proxy_date'])
        case['day_of_week'] = case['proxy_date'].weekday()  # 0=Monday, 6=Sunday
        case['month'] = case['proxy_date'].month
    
    return cases

def get_fiscal_quarter(date):
    """Get fiscal quarter (1960s style: April-March fiscal year)"""
    if date.month >= 4:
        fiscal_month = date.month - 3
    else:
        fiscal_month = date.month + 9
    
    return (fiscal_month - 1) // 3 + 1

def run_current_model(case):
    """Run the current best model to get predictions and errors"""
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled'] 
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    # Simplified version of current model logic
    if days == 1:
        base_days = 874
    elif days == 2:
        base_days = 1046
    elif days == 3:
        base_days = 1011
    elif days == 4:
        base_days = 1218
    elif days == 5:
        base_days = 1273
    elif days == 6:
        base_days = 1366
    elif days == 7:
        base_days = 1521
    elif days == 8:
        base_days = 1443
    elif days == 9:
        base_days = 1439
    elif days == 10:
        base_days = 1496
    else:
        base_days = 1496 + (days - 10) * 50
    
    receipts_deviation = receipts - 1211.06
    receipts_adjustment = receipts_deviation * 0.35
    
    miles_deviation = miles - 597.41
    miles_adjustment = miles_deviation * 0.25
    
    base = base_days + receipts_adjustment + miles_adjustment
    
    # Apply penalty logic (simplified)
    daily_miles = miles / days
    daily_spending = receipts / days
    
    penalty_factor = 1.0
    
    if daily_miles < 25 and daily_spending > 500:
        penalty_factor = 0.25
    elif days == 1 and miles > 1000 and receipts > 1500:
        penalty_factor = 0.37
    elif daily_miles < 40 and daily_spending > 400:
        penalty_factor = 0.40
    elif daily_miles < 60 and daily_spending > 300:
        penalty_factor = 0.50
    elif daily_miles < 80 and daily_spending > 250:
        penalty_factor = 0.65
    elif daily_miles < 100 and daily_spending > 200:
        penalty_factor = 0.75
    elif daily_miles < 50 and days >= 3:
        penalty_factor = 0.80
    elif daily_spending > 400:
        penalty_factor = 0.85
    
    if penalty_factor < 1.0:
        base *= penalty_factor
    
    # High performer bonuses
    if days >= 7 and miles > 900 and 100 <= daily_miles <= 200:
        base *= 1.35
    elif days >= 8 and miles > 1000 and daily_spending < 200:
        base *= 1.40
    
    # Apply bounds
    if base < 100:
        base = 100
    elif base > 3000:
        base = 3000
    
    predicted = round(base, 2)
    error = abs(predicted - expected)
    
    return predicted, error

def analyze_temporal_patterns(cases):
    """Analyze temporal patterns in the error data"""
    print("🕰️  TEMPORAL ANALYSIS - Strategy 12")
    print("=" * 50)
    
    # Calculate predictions and errors for all cases
    for case in cases:
        predicted, error = run_current_model(case)
        case['predicted'] = predicted
        case['error'] = error
    
    print(f"📊 Analyzed {len(cases)} cases")
    print(f"📅 Date range: {cases[0]['proxy_date'].strftime('%Y-%m-%d')} to {cases[-1]['proxy_date'].strftime('%Y-%m-%d')}")
    
    # Fiscal Quarter Analysis
    print("\n🏢 FISCAL QUARTER ANALYSIS")
    print("-" * 30)
    quarterly_errors = {}
    quarterly_cases = {}
    
    for case in cases:
        q = case['fiscal_quarter']
        if q not in quarterly_errors:
            quarterly_errors[q] = []
            quarterly_cases[q] = []
        quarterly_errors[q].append(case['error'])
        quarterly_cases[q].append(case)
    
    temporal_adjustments = {}
    
    for q in sorted(quarterly_errors.keys()):
        mean_error = statistics.mean(quarterly_errors[q])
        median_error = statistics.median(quarterly_errors[q])
        print(f"Q{q}: Mean Error = ${mean_error:.2f}, Median = ${median_error:.2f}, Cases = {len(quarterly_errors[q])}")
        
        # Calculate adjustment factor based on error patterns
        # If this quarter has consistently higher errors, we need a correction
        overall_mean_error = statistics.mean([e for errors in quarterly_errors.values() for e in errors])
        if mean_error > overall_mean_error * 1.1:
            temporal_adjustments[f'fiscal_q{q}'] = 0.95  # Reduce predictions
        elif mean_error < overall_mean_error * 0.9:
            temporal_adjustments[f'fiscal_q{q}'] = 1.05  # Increase predictions
    
    # Day of Week Analysis
    print("\n📅 DAY OF WEEK ANALYSIS")
    print("-" * 30)
    dow_errors = {}
    dow_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for case in cases:
        dow = case['day_of_week']
        if dow not in dow_errors:
            dow_errors[dow] = []
        dow_errors[dow].append(case['error'])
    
    for dow in sorted(dow_errors.keys()):
        mean_error = statistics.mean(dow_errors[dow])
        print(f"{dow_names[dow]}: Mean Error = ${mean_error:.2f}, Cases = {len(dow_errors[dow])}")
        
        # Weekend processing different?
        if dow >= 5:  # Saturday/Sunday
            overall_weekday_errors = [e for d, errors in dow_errors.items() for e in errors if d < 5]
            weekend_mean = statistics.mean(dow_errors[dow])
            weekday_mean = statistics.mean(overall_weekday_errors) if overall_weekday_errors else weekend_mean
            
            if abs(weekend_mean - weekday_mean) > 20:  # Significant difference
                adjustment = weekday_mean / weekend_mean if weekend_mean > 0 else 1.0
                temporal_adjustments[f'weekend_{dow_names[dow].lower()}'] = adjustment
    
    # Monthly Pattern Analysis (End of month batch processing)
    print("\n📆 MONTHLY PATTERN ANALYSIS")
    print("-" * 30)
    
    # Group by position within month (simulate batch processing)
    month_position_errors = {}
    for case in cases:
        day_of_month = case['proxy_date'].day
        if day_of_month <= 5:
            pos = 'early'
        elif day_of_month <= 15:
            pos = 'mid'
        elif day_of_month <= 25:
            pos = 'late'
        else:
            pos = 'end'
        
        if pos not in month_position_errors:
            month_position_errors[pos] = []
        month_position_errors[pos].append(case['error'])
    
    for pos in ['early', 'mid', 'late', 'end']:
        if pos in month_position_errors:
            mean_error = statistics.mean(month_position_errors[pos])
            print(f"{pos.title()} month: Mean Error = ${mean_error:.2f}, Cases = {len(month_position_errors[pos])}")
    
    # Cyclic Pattern Detection
    print("\n🔄 CYCLIC PATTERN DETECTION")
    print("-" * 30)
    
    # Test various cycle lengths
    for cycle_length in [7, 14, 30, 52, 90]:
        cycle_errors = {}
        for case in cases:
            cycle_pos = case['index'] % cycle_length
            if cycle_pos not in cycle_errors:
                cycle_errors[cycle_pos] = []
            cycle_errors[cycle_pos].append(case['error'])
        
        # Calculate variance across cycle positions
        cycle_means = [statistics.mean(errors) for errors in cycle_errors.values()]
        if len(cycle_means) > 1:
            cycle_variance = statistics.variance(cycle_means)
            print(f"Cycle {cycle_length}: Variance in errors = {cycle_variance:.2f}")
            
            # If high variance, there might be a pattern
            if cycle_variance > 100:  # Threshold for "interesting" pattern
                print(f"  ⚠️  Potential {cycle_length}-day cycle detected!")
                for pos in sorted(cycle_errors.keys())[:min(5, cycle_length)]:
                    mean_err = statistics.mean(cycle_errors[pos])
                    print(f"    Position {pos}: Mean Error = ${mean_err:.2f}")
    
    return temporal_adjustments

def generate_temporal_run_script(adjustments):
    """Generate a new run.sh with temporal adjustments"""
    
    script_content = '''#!/bin/bash

# TEMPORAL/CALENDAR LOGIC MODEL - Strategy 12
# Based on 1960s batch processing and fiscal calendar patterns
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Calculate case index for temporal logic (simulated)
# In real system, this would be based on actual processing date
CASE_INDEX=${4:-0}  # Optional 4th parameter for testing

# Base reimbursement by days (from training data)
if [ "$DAYS" -eq 1 ]; then
    BASE_DAYS=874    
elif [ "$DAYS" -eq 2 ]; then
    BASE_DAYS=1046   
elif [ "$DAYS" -eq 3 ]; then
    BASE_DAYS=1011   
elif [ "$DAYS" -eq 4 ]; then
    BASE_DAYS=1218   
elif [ "$DAYS" -eq 5 ]; then
    BASE_DAYS=1273   
elif [ "$DAYS" -eq 6 ]; then
    BASE_DAYS=1366   
elif [ "$DAYS" -eq 7 ]; then
    BASE_DAYS=1521   
elif [ "$DAYS" -eq 8 ]; then
    BASE_DAYS=1443   
elif [ "$DAYS" -eq 9 ]; then
    BASE_DAYS=1439   
elif [ "$DAYS" -eq 10 ]; then
    BASE_DAYS=1496   
else
    BASE_DAYS=$(echo "scale=2; 1496 + ($DAYS - 10) * 50" | bc)
fi

# Standard adjustments
RECEIPTS_DEVIATION=$(echo "scale=4; $RECEIPTS - 1211.06" | bc)
RECEIPTS_ADJUSTMENT=$(echo "scale=4; $RECEIPTS_DEVIATION * 0.35" | bc)

MILES_DEVIATION=$(echo "scale=4; $MILES - 597.41" | bc)
MILES_ADJUSTMENT=$(echo "scale=4; $MILES_DEVIATION * 0.25" | bc)

BASE=$(echo "scale=4; $BASE_DAYS + $RECEIPTS_ADJUSTMENT + $MILES_ADJUSTMENT" | bc)

# TEMPORAL ADJUSTMENTS - The 1960s Calendar Logic
TEMPORAL_FACTOR="1.0"

# Fiscal Quarter Logic (April-March fiscal year)
FISCAL_QUARTER=$(echo "scale=0; (($CASE_INDEX / 250) % 4) + 1" | bc)

'''
    
    # Add fiscal quarter adjustments
    for key, factor in adjustments.items():
        if 'fiscal_q' in key:
            quarter = key.replace('fiscal_q', '')
            script_content += f'''if [ "$FISCAL_QUARTER" -eq {quarter} ]; then
    TEMPORAL_FACTOR=$(echo "scale=4; $TEMPORAL_FACTOR * {factor}" | bc)
fi

'''
    
    script_content += '''
# Month-end batch processing logic (1960s style)
MONTH_POSITION=$(echo "scale=0; ($CASE_INDEX % 30)" | bc)
if [ "$MONTH_POSITION" -lt 5 ]; then
    # Early month - new budget, slightly generous
    TEMPORAL_FACTOR=$(echo "scale=4; $TEMPORAL_FACTOR * 1.02" | bc)
elif [ "$MONTH_POSITION" -gt 25 ]; then
    # End of month - budget constraints
    TEMPORAL_FACTOR=$(echo "scale=4; $TEMPORAL_FACTOR * 0.98" | bc)
fi

# Day of week processing (weekend batch runs)
DAY_OF_WEEK=$(echo "scale=0; ($CASE_INDEX % 7)" | bc)
if [ "$DAY_OF_WEEK" -gt 4 ]; then
    # Weekend processing - different approval levels
    TEMPORAL_FACTOR=$(echo "scale=4; $TEMPORAL_FACTOR * 0.97" | bc)
fi

# Apply temporal adjustments
if (( $(echo "$TEMPORAL_FACTOR != 1.0" | bc -l) )); then
    BASE=$(echo "scale=4; $BASE * $TEMPORAL_FACTOR" | bc)
fi

# Continue with original penalty logic...
PENALTY_FACTOR="1.0"
DAILY_MILES=$(echo "scale=4; $MILES / $DAYS" | bc)
DAILY_SPENDING=$(echo "scale=4; $RECEIPTS / $DAYS" | bc)

# GRADUATED PENALTY SYSTEM (same as before)
if (( $(echo "$DAILY_MILES < 25" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 500" | bc -l) )); then
    PENALTY_FACTOR="0.25"
elif [ "$DAYS" -eq 1 ] && (( $(echo "$MILES > 1000" | bc -l) )) && (( $(echo "$RECEIPTS > 1500" | bc -l) )); then
    PENALTY_FACTOR="0.37"
elif (( $(echo "$DAILY_MILES < 40" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 400" | bc -l) )); then
    PENALTY_FACTOR="0.40"
elif (( $(echo "$DAILY_MILES < 60" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 300" | bc -l) )); then
    PENALTY_FACTOR="0.50"
elif (( $(echo "$DAILY_MILES < 80" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 250" | bc -l) )); then
    PENALTY_FACTOR="0.65"
elif (( $(echo "$DAILY_MILES < 100" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 200" | bc -l) )); then
    PENALTY_FACTOR="0.75"
elif (( $(echo "$DAILY_MILES < 50" | bc -l) )) && (( $(echo "$DAYS >= 3" | bc -l) )); then
    PENALTY_FACTOR="0.80"
elif (( $(echo "$DAILY_SPENDING > 400" | bc -l) )); then
    PENALTY_FACTOR="0.85"
fi

if (( $(echo "$PENALTY_FACTOR < 1.0" | bc -l) )); then
    BASE=$(echo "scale=4; $BASE * $PENALTY_FACTOR" | bc)
fi

# HIGH PERFORMER BONUSES
if (( $(echo "$DAYS >= 7" | bc -l) )) && (( $(echo "$MILES > 900" | bc -l) )) && (( $(echo "$DAILY_MILES >= 100 && $DAILY_MILES <= 200" | bc -l) )); then
    BASE=$(echo "scale=4; $BASE * 1.35" | bc)
elif (( $(echo "$DAYS >= 8" | bc -l) )) && (( $(echo "$MILES > 1000" | bc -l) )) && (( $(echo "$DAILY_SPENDING < 200" | bc -l) )); then
    BASE=$(echo "scale=4; $BASE * 1.40" | bc)
fi

# Apply bounds
if (( $(echo "$BASE < 100" | bc -l) )); then
    BASE="100"
elif (( $(echo "$BASE > 3000" | bc -l) )); then
    BASE="3000"
fi

printf "%.2f\\n" $BASE
'''
    
    return script_content

def main():
    print("Loading and analyzing temporal patterns...")
    cases = load_public_cases()
    adjustments = analyze_temporal_patterns(cases)
    
    print("\n🎯 TEMPORAL ADJUSTMENTS DISCOVERED:")
    print("-" * 40)
    for key, factor in adjustments.items():
        print(f"  {key}: {factor:.3f}")
    
    # Generate new run script
    script_content = generate_temporal_run_script(adjustments)
    
    with open('../../run.sh', 'w') as f:
        f.write(script_content)
    
    print(f"\n✅ Generated new temporal run.sh with {len(adjustments)} adjustments")
    print("💡 The script now includes 1960s fiscal calendar and batch processing logic!")

if __name__ == "__main__":
    main()