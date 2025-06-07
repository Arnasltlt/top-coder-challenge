#!/bin/bash

# ULTRA-SIMPLE ROBUST Model
# Focus on broad patterns rather than edge cases
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Calculate key metrics
DAILY_SPENDING=$(echo "scale=4; $RECEIPTS / $DAYS" | bc)
TOTAL_ACTIVITY=$(echo "scale=4; $MILES + ($RECEIPTS * 0.5)" | bc)

# Simple duration-based calculation with activity scaling
if [ "$DAYS" -eq 1 ]; then
    # 1-day: Simple caps based on total activity
    if (( $(echo "$TOTAL_ACTIVITY > 2000" | bc -l) )); then
        BASE="1400"  # High activity cap
    elif (( $(echo "$TOTAL_ACTIVITY > 1000" | bc -l) )); then
        BASE=$(echo "scale=4; 400 + 0.60 * $TOTAL_ACTIVITY" | bc)
    else
        BASE=$(echo "scale=4; 80 + 1.20 * $TOTAL_ACTIVITY" | bc)
    fi
    
elif [ "$DAYS" -eq 2 ]; then
    # 2-day trips
    BASE=$(echo "scale=4; 200 + 0.50 * $MILES + 0.40 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -eq 3 ]; then
    # 3-day trips  
    BASE=$(echo "scale=4; 280 + 0.45 * $MILES + 0.35 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -ge 4 ] && [ "$DAYS" -le 6 ]; then
    # 4-6 day trips: Check for suspicious low activity
    if (( $(echo "$MILES < 200" | bc -l) )) && (( $(echo "$RECEIPTS > 2000" | bc -l) )); then
        # Very suspicious pattern (Case 151 type) - severely limit
        BASE=$(echo "scale=4; 100 + 0.80 * $MILES + 0.08 * $RECEIPTS" | bc)
    else
        # Normal calculation
        BASE=$(echo "scale=4; $DAYS * 90 + 0.40 * $MILES + 0.30 * $RECEIPTS" | bc)
    fi
    
elif [ "$DAYS" -ge 7 ] && [ "$DAYS" -le 10 ]; then
    # 7-10 day trips: Moderate per diem
    BASE=$(echo "scale=4; $DAYS * 85 + 0.35 * $MILES + 0.25 * $RECEIPTS" | bc)
    
else
    # 11+ day trips: Conservative approach
    BASE=$(echo "scale=4; 850 + ($DAYS - 10) * 60 + 0.30 * $MILES + 0.20 * $RECEIPTS" | bc)
fi

# Global reasonableness checks
if (( $(echo "$DAILY_SPENDING > 500" | bc -l) )); then
    # Very high daily spending - apply cap
    EXCESS=$(echo "scale=4; ($DAILY_SPENDING - 500) * $DAYS" | bc)
    PENALTY=$(echo "scale=4; $EXCESS * 0.40" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
fi

# Ensure reasonable bounds
if (( $(echo "$BASE < 80" | bc -l) )); then
    BASE="80"
elif (( $(echo "$BASE > 2500" | bc -l) )); then
    BASE="2500"
fi

# Final output with 2 decimal places
printf "%.2f\n" $BASE