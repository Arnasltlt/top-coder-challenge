#!/bin/bash

# DATA-DRIVEN REIMBURSEMENT SYSTEM
# Based on actual correlation analysis of training data
# Receipts = strongest predictor (0.704), followed by days (0.514), then miles (0.432)
# Usage: ./run_data_driven.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Base reimbursement by days (from actual training data averages)
if [ "$DAYS" -eq 1 ]; then
    BASE_DAYS=874    # Actual average: $873.55
elif [ "$DAYS" -eq 2 ]; then
    BASE_DAYS=1046   # Actual average: $1046.24
elif [ "$DAYS" -eq 3 ]; then
    BASE_DAYS=1011   # Actual average: $1010.56
elif [ "$DAYS" -eq 4 ]; then
    BASE_DAYS=1218   # Actual average: $1217.96
elif [ "$DAYS" -eq 5 ]; then
    BASE_DAYS=1273   # Actual average: $1272.59
elif [ "$DAYS" -eq 6 ]; then
    BASE_DAYS=1366   # Actual average: $1366.48
elif [ "$DAYS" -eq 7 ]; then
    BASE_DAYS=1521   # Actual average: $1521.48
elif [ "$DAYS" -eq 8 ]; then
    BASE_DAYS=1443   # Actual average: $1442.64
elif [ "$DAYS" -eq 9 ]; then
    BASE_DAYS=1439   # Actual average: $1438.67
elif [ "$DAYS" -eq 10 ]; then
    BASE_DAYS=1496   # Actual average: $1496.15
elif [ "$DAYS" -ge 11 ] && [ "$DAYS" -le 15 ]; then
    # Extrapolate for longer trips (diminishing returns pattern)
    BASE_DAYS=$(echo "scale=2; 1496 + ($DAYS - 10) * 50" | bc)
else
    # Very long trips: conservative approach
    BASE_DAYS=$(echo "scale=2; 1496 + 5 * 50 + ($DAYS - 15) * 20" | bc)
fi

# Receipts adjustment (strongest correlation 0.704)
# Use training data: mean receipts $1211.06, mean reimbursement $1349.11
RECEIPTS_DEVIATION=$(echo "scale=4; $RECEIPTS - 1211.06" | bc)
RECEIPTS_ADJUSTMENT=$(echo "scale=4; $RECEIPTS_DEVIATION * 0.35" | bc)

# Miles adjustment (moderate correlation 0.432)  
# Use training data: mean miles 597.41
MILES_DEVIATION=$(echo "scale=4; $MILES - 597.41" | bc)
MILES_ADJUSTMENT=$(echo "scale=4; $MILES_DEVIATION * 0.25" | bc)

# Combine all components
BASE=$(echo "scale=4; $BASE_DAYS + $RECEIPTS_ADJUSTMENT + $MILES_ADJUSTMENT" | bc)

# Apply reasonable bounds based on training data
if (( $(echo "$BASE < 100" | bc -l) )); then
    BASE="100"
elif (( $(echo "$BASE > 3000" | bc -l) )); then
    BASE="3000"
fi

# Final output with 2 decimal places
printf "%.2f\n" $BASE