#!/bin/bash

# ULTRA-REFINED Model v5 - Non-monotonic relationships
# Based on critical pattern discovery
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Calculate activity metrics
DAILY_MILES=$(echo "scale=4; $MILES / $DAYS" | bc)
DAILY_SPENDING=$(echo "scale=4; $RECEIPTS / $DAYS" | bc)

# Base calculation by duration
if [ "$DAYS" -eq 1 ]; then
    # 1-day trips: Complex non-monotonic logic
    
    if (( $(echo "$MILES > 1000" | bc -l) )); then
        # Very high mileage: non-monotonic receipt relationship
        if (( $(echo "$RECEIPTS < 500" | bc -l) )); then
            # Very high miles + very low receipts: ~$550-570 range
            BASE=$(echo "scale=4; 100 + 0.45 * $MILES + 0.80 * $RECEIPTS" | bc)
            
        elif (( $(echo "$RECEIPTS >= 500 && $RECEIPTS < 2000" | bc -l) )); then
            # Very high miles + medium receipts: PENALTY zone (~$450)
            BASE=$(echo "scale=4; 150 + 0.25 * $MILES + 0.05 * $RECEIPTS" | bc)
            
        else
            # Very high miles + very high receipts: excellent (~$1400+)
            BASE=$(echo "scale=4; 300 + 1.05 * $MILES + 0.40 * $RECEIPTS" | bc)
            if (( $(echo "$BASE > 1475" | bc -l) )); then
                BASE="1475"
            fi
        fi
        
    elif (( $(echo "$MILES > 700" | bc -l) )); then
        # High mileage (700-1000): smoother relationship
        if (( $(echo "$RECEIPTS < 500" | bc -l) )); then
            # High miles + low receipts: decent
            BASE=$(echo "scale=4; 100 + 0.60 * $MILES + 0.70 * $RECEIPTS" | bc)
        else
            # High miles + higher receipts: good to excellent
            BASE=$(echo "scale=4; 200 + 0.90 * $MILES + 0.45 * $RECEIPTS" | bc)
            if (( $(echo "$BASE > 1475" | bc -l) )); then
                BASE="1475"
            fi
        fi
        
    elif (( $(echo "$MILES > 300" | bc -l) )); then
        # Medium mileage: receipt-focused  
        if (( $(echo "$RECEIPTS > 2000" | bc -l) )); then
            # Medium miles + very high receipts: capped but good
            BASE=$(echo "scale=4; 200 + 1.50 * $MILES + 0.35 * $RECEIPTS" | bc)
            if (( $(echo "$BASE > 1250" | bc -l) )); then
                BASE="1250"
            fi
        else
            # Medium miles + medium receipts: balanced
            BASE=$(echo "scale=4; 80 + 1.20 * $MILES + 0.60 * $RECEIPTS" | bc)
        fi
        
    else
        # Low mileage: receipt-dependent
        if (( $(echo "$RECEIPTS > 2000" | bc -l) )); then
            # Low miles + very high receipts: moderate (suspicious pattern)
            BASE=$(echo "scale=4; 300 + 2.00 * $MILES + 0.30 * $RECEIPTS" | bc)
        else
            # Low miles + low/medium receipts: basic calculation
            BASE=$(echo "scale=4; 80 + 1.50 * $MILES + 0.80 * $RECEIPTS" | bc)
        fi
    fi
    
elif [ "$DAYS" -eq 2 ]; then
    # 2-day trips: simpler logic
    BASE=$(echo "scale=4; 150 + 0.60 * $MILES + 0.40 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -eq 3 ]; then
    # 3-day trips
    BASE=$(echo "scale=4; 200 + 0.50 * $MILES + 0.35 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -ge 4 ] && [ "$DAYS" -le 6 ]; then
    # 4-6 day trips
    BASE=$(echo "scale=4; $DAYS * 110 + 0.45 * $MILES + 0.30 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -ge 7 ] && [ "$DAYS" -le 10 ]; then
    # 7-10 day trips: reduce coefficients slightly from v4
    BASE=$(echo "scale=4; $DAYS * 135 + 0.40 * $MILES + 0.25 * $RECEIPTS" | bc)
    
else
    # 11+ day trips
    FIRST_10=$(echo "scale=4; 10 * 135 + 0.40 * $MILES + 0.25 * $RECEIPTS" | bc)
    EXTRA_DAYS=$(echo "$DAYS - 10" | bc)
    EXTRA_AMOUNT=$(echo "scale=4; $EXTRA_DAYS * 75" | bc)
    BASE=$(echo "scale=4; $FIRST_10 + $EXTRA_AMOUNT" | bc)
fi

# Minimal global adjustments
if (( $(echo "$BASE < 80" | bc -l) )); then
    BASE="80"
fi

# Final output with 2 decimal places
printf "%.2f\n" $BASE