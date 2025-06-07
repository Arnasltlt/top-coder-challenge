#!/bin/bash

# GRADUATED PENALTY SYSTEM
# Broader detection with multiple penalty levels instead of binary
# Based on analysis showing 73% of cases need some form of adjustment
# Usage: ./run_graduated_penalties.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Calculate efficiency metrics
DAILY_MILES=$(echo "scale=4; $MILES / $DAYS" | bc)
DAILY_SPENDING=$(echo "scale=4; $RECEIPTS / $DAYS" | bc)

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

# GRADUATED PENALTY SYSTEM

PENALTY_FACTOR="1.0"

# EXTREME SUSPICIOUS ACTIVITY (Severe penalties)
if (( $(echo "$DAILY_MILES < 25" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 500" | bc -l) )); then
    PENALTY_FACTOR="0.25"  # Very harsh penalty
    
elif [ "$DAYS" -eq 1 ] && (( $(echo "$MILES > 1000" | bc -l) )) && (( $(echo "$RECEIPTS > 1500" | bc -l) )); then
    PENALTY_FACTOR="0.37"  # Unrealistic single day
    
# HIGH SUSPICIOUS ACTIVITY (Major penalties)
elif (( $(echo "$DAILY_MILES < 40" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 400" | bc -l) )); then
    PENALTY_FACTOR="0.40"  # Major penalty
    
elif (( $(echo "$DAILY_MILES < 60" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 300" | bc -l) )); then
    PENALTY_FACTOR="0.50"  # Significant penalty
    
# MODERATE SUSPICIOUS ACTIVITY (Moderate penalties)
elif (( $(echo "$DAILY_MILES < 80" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 250" | bc -l) )); then
    PENALTY_FACTOR="0.65"  # Moderate penalty
    
elif (( $(echo "$DAILY_MILES < 100" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 200" | bc -l) )); then
    PENALTY_FACTOR="0.75"  # Light penalty
    
# EFFICIENCY-BASED ADJUSTMENTS
elif (( $(echo "$DAILY_MILES < 50" | bc -l) )) && (( $(echo "$DAYS >= 3" | bc -l) )); then
    PENALTY_FACTOR="0.80"  # Low efficiency multi-day trips
    
elif (( $(echo "$DAILY_SPENDING > 400" | bc -l) )); then
    PENALTY_FACTOR="0.85"  # Very high spending regardless of miles
fi

# Apply penalty
if (( $(echo "$PENALTY_FACTOR < 1.0" | bc -l) )); then
    BASE=$(echo "scale=4; $BASE * $PENALTY_FACTOR" | bc)
fi

# HIGH PERFORMER BONUSES (keep existing logic)
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

printf "%.2f\n" $BASE