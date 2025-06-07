#!/bin/bash

# DATA-DRIVEN MODEL WITH OUTLIER PATTERN DETECTION
# Implements suspicious activity penalties and high performer bonuses
# Based on training data analysis showing two types of outliers
# Usage: ./run_with_outliers.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Calculate efficiency metrics
DAILY_MILES=$(echo "scale=4; $MILES / $DAYS" | bc)
DAILY_SPENDING=$(echo "scale=4; $RECEIPTS / $DAYS" | bc)

# Base reimbursement by days (from actual training data averages)
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
elif [ "$DAYS" -ge 11 ] && [ "$DAYS" -le 15 ]; then
    BASE_DAYS=$(echo "scale=2; 1496 + ($DAYS - 10) * 50" | bc)
else
    BASE_DAYS=$(echo "scale=2; 1496 + 5 * 50 + ($DAYS - 15) * 20" | bc)
fi

# Standard adjustments (receipts strongest predictor)
RECEIPTS_DEVIATION=$(echo "scale=4; $RECEIPTS - 1211.06" | bc)
RECEIPTS_ADJUSTMENT=$(echo "scale=4; $RECEIPTS_DEVIATION * 0.35" | bc)

MILES_DEVIATION=$(echo "scale=4; $MILES - 597.41" | bc)
MILES_ADJUSTMENT=$(echo "scale=4; $MILES_DEVIATION * 0.25" | bc)

# Calculate base prediction
BASE=$(echo "scale=4; $BASE_DAYS + $RECEIPTS_ADJUSTMENT + $MILES_ADJUSTMENT" | bc)

# OUTLIER PATTERN DETECTION

# SUSPICIOUS ACTIVITY PENALTY (based on training data outliers)
SUSPICIOUS=0

# Pattern 1: Very low daily miles with high receipts (like 4d, 69mi, $2321)
if (( $(echo "$DAILY_MILES < 30" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 400" | bc -l) )); then
    SUSPICIOUS=1
    PENALTY_FACTOR="0.22"  # Ratio observed: 322/1474 ≈ 0.22
    
# Pattern 2: Unrealistic single-day activity (like 1d, 1082mi, $1809)  
elif [ "$DAYS" -eq 1 ] && (( $(echo "$MILES > 1000" | bc -l) )) && (( $(echo "$RECEIPTS > 1500" | bc -l) )); then
    SUSPICIOUS=1
    PENALTY_FACTOR="0.37"  # Ratio observed: 446/1204 ≈ 0.37
    
# Pattern 3: Medium trips with very low efficiency + high receipts
elif (( $(echo "$DAYS >= 5 && $DAYS <= 8" | bc -l) )) && (( $(echo "$DAILY_MILES < 120" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 300" | bc -l) )); then
    SUSPICIOUS=1
    PENALTY_FACTOR="0.45"  # Average ratio for this pattern
fi

if [ "$SUSPICIOUS" -eq 1 ]; then
    BASE=$(echo "scale=4; $BASE * $PENALTY_FACTOR" | bc)
fi

# HIGH PERFORMER BONUS (based on training data outliers with ratios 1.3-1.5)
HIGH_PERFORMER=0

# Pattern: High mileage + reasonable efficiency + longer trips
if (( $(echo "$DAYS >= 7" | bc -l) )) && (( $(echo "$MILES > 900" | bc -l) )) && (( $(echo "$DAILY_MILES >= 100 && $DAILY_MILES <= 200" | bc -l) )); then
    HIGH_PERFORMER=1
    BONUS_FACTOR="1.35"  # Average bonus ratio observed
    
elif (( $(echo "$DAYS >= 8" | bc -l) )) && (( $(echo "$MILES > 1000" | bc -l) )) && (( $(echo "$DAILY_SPENDING < 200" | bc -l) )); then
    HIGH_PERFORMER=1
    BONUS_FACTOR="1.40"  # Higher bonus for very efficient long trips
fi

if [ "$HIGH_PERFORMER" -eq 1 ]; then
    BASE=$(echo "scale=4; $BASE * $BONUS_FACTOR" | bc)
fi

# Apply reasonable bounds
if (( $(echo "$BASE < 100" | bc -l) )); then
    BASE="100"
elif (( $(echo "$BASE > 3000" | bc -l) )); then
    BASE="3000"
fi

# Final output with 2 decimal places
printf "%.2f\n" $BASE