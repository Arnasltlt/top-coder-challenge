#!/bin/bash

# ULTRA-BREAKTHROUGH Model v4
# Bracket-based logic with activity thresholds
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Calculate activity metrics
DAILY_MILES=$(echo "scale=4; $MILES / $DAYS" | bc)
DAILY_SPENDING=$(echo "scale=4; $RECEIPTS / $DAYS" | bc)

# Base calculation by duration with bracket logic
if [ "$DAYS" -eq 1 ]; then
    # 1-day trips: Complex bracket logic based on data patterns
    
    if (( $(echo "$MILES > 800" | bc -l) )) && (( $(echo "$RECEIPTS > 2000" | bc -l) )); then
        # High activity + very high receipts: ~$1400-1475 range
        BASE=$(echo "scale=4; 400 + 1.10 * $MILES + 0.45 * $RECEIPTS" | bc)
        if (( $(echo "$BASE > 1475" | bc -l) )); then
            BASE="1475"
        fi
        
    elif (( $(echo "$MILES > 1000" | bc -l) )) && (( $(echo "$RECEIPTS > 1500 && $RECEIPTS < 2000" | bc -l) )); then
        # SUSPICIOUS: Very high mileage + medium-high receipts = penalty
        BASE=$(echo "scale=4; 200 + 0.30 * $MILES + 0.10 * $RECEIPTS" | bc)
        
    elif (( $(echo "$MILES > 600" | bc -l) )); then
        # High mileage with various receipt levels
        if (( $(echo "$RECEIPTS < 500" | bc -l) )); then
            # High mileage, low receipts: moderate reimbursement
            BASE=$(echo "scale=4; 100 + 0.80 * $MILES + 0.60 * $RECEIPTS" | bc)
        else
            # High mileage, decent receipts: good reimbursement
            BASE=$(echo "scale=4; 200 + 1.00 * $MILES + 0.50 * $RECEIPTS" | bc)
            if (( $(echo "$BASE > 1475" | bc -l) )); then
                BASE="1475"
            fi
        fi
        
    else
        # Lower mileage cases: simpler calculation
        BASE=$(echo "scale=4; 80 + 1.20 * $MILES + 0.80 * $RECEIPTS" | bc)
    fi
    
elif [ "$DAYS" -eq 2 ]; then
    # 2-day trips
    BASE=$(echo "scale=4; 150 + 0.70 * $MILES + 0.45 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -eq 3 ]; then
    # 3-day trips
    BASE=$(echo "scale=4; 200 + 0.60 * $MILES + 0.40 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -ge 4 ] && [ "$DAYS" -le 6 ]; then
    # 4-6 day trips
    BASE=$(echo "scale=4; $DAYS * 120 + 0.50 * $MILES + 0.35 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -ge 7 ] && [ "$DAYS" -le 10 ]; then
    # 7-10 day trips: Based on good performance in v3
    BASE=$(echo "scale=4; $DAYS * 140 + 0.45 * $MILES + 0.30 * $RECEIPTS" | bc)
    
else
    # 11+ day trips
    FIRST_10=$(echo "scale=4; 10 * 140 + 0.45 * $MILES + 0.30 * $RECEIPTS" | bc)
    EXTRA_DAYS=$(echo "$DAYS - 10" | bc)
    EXTRA_AMOUNT=$(echo "scale=4; $EXTRA_DAYS * 80" | bc)
    BASE=$(echo "scale=4; $FIRST_10 + $EXTRA_AMOUNT" | bc)
fi

# Global adjustments (lighter than before)

# Very high receipt cap
if (( $(echo "$RECEIPTS > 2500" | bc -l) )); then
    EXCESS=$(echo "scale=4; $RECEIPTS - 2500" | bc)
    PENALTY=$(echo "scale=4; $EXCESS * 0.20" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
fi

# Ensure minimum
if (( $(echo "$BASE < 80" | bc -l) )); then
    BASE="80"
fi

# Final output with 2 decimal places
printf "%.2f\n" $BASE