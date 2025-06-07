#!/bin/bash

# ULTRA-TUNED Reimbursement System v3
# Refined reasonableness checks and activity patterns
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Calculate activity metrics
DAILY_MILES=$(echo "scale=4; $MILES / $DAYS" | bc)
DAILY_SPENDING=$(echo "scale=4; $RECEIPTS / $DAYS" | bc)

# Base calculation by duration 
if [ "$DAYS" -eq 1 ]; then
    # 1-day trips: High activity can earn high reimbursement
    BASE=$(echo "scale=4; 100 + 1.20 * $MILES + 0.45 * $RECEIPTS" | bc)
    
    # 1-day caps based on activity level
    if (( $(echo "$MILES > 800" | bc -l) )); then
        # High activity 1-day trips can go up to ~$1450
        if (( $(echo "$BASE > 1450" | bc -l) )); then
            BASE="1450"
        fi
    else
        # Lower activity 1-day trips have lower caps
        if (( $(echo "$BASE > 800" | bc -l) )); then
            BASE="800"
        fi
    fi
    
elif [ "$DAYS" -eq 2 ]; then
    # 2-day trips
    BASE=$(echo "scale=4; 180 + 0.85 * $MILES + 0.50 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -eq 3 ]; then
    # 3-day trips  
    BASE=$(echo "scale=4; 250 + 0.70 * $MILES + 0.45 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -ge 4 ] && [ "$DAYS" -le 6 ]; then
    # 4-6 day trips
    BASE=$(echo "scale=4; $DAYS * 160 + 0.60 * $MILES + 0.40 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -ge 7 ] && [ "$DAYS" -le 10 ]; then
    # 7-10 day trips: Good performance here
    BASE=$(echo "scale=4; $DAYS * 150 + 0.55 * $MILES + 0.35 * $RECEIPTS" | bc)
    
else
    # 11+ day trips
    FIRST_10=$(echo "scale=4; 10 * 150 + 0.55 * $MILES + 0.35 * $RECEIPTS" | bc)
    EXTRA_DAYS=$(echo "$DAYS - 10" | bc)
    EXTRA_AMOUNT=$(echo "scale=4; $EXTRA_DAYS * 90" | bc)
    BASE=$(echo "scale=4; $FIRST_10 + $EXTRA_AMOUNT" | bc)
fi

# REFINED REASONABLENESS CHECKS (much less harsh)

# Only penalize EXTREME mismatches (very low miles + very high receipts)
if (( $(echo "$MILES < 100" | bc -l) )) && (( $(echo "$RECEIPTS > 2000" | bc -l) )); then
    # This is suspicious - apply moderate penalty
    PENALTY=$(echo "scale=4; $BASE * 0.30" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
    
elif (( $(echo "$DAILY_MILES < 10" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 500" | bc -l) )); then
    # Very extreme mismatch
    PENALTY=$(echo "scale=4; $BASE * 0.50" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
fi

# High mileage diminishing returns (less harsh)
if (( $(echo "$MILES > 1200" | bc -l) )); then
    EXCESS_MILES=$(echo "scale=4; $MILES - 1200" | bc)
    PENALTY=$(echo "scale=4; $EXCESS_MILES * 0.20" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
fi

# Very high receipt spending caps (less harsh)
if (( $(echo "$DAILY_SPENDING > 400" | bc -l) )); then
    EXCESS_DAILY=$(echo "scale=4; $DAILY_SPENDING - 400" | bc)
    TOTAL_EXCESS=$(echo "scale=4; $EXCESS_DAILY * $DAYS" | bc)
    PENALTY=$(echo "scale=4; $TOTAL_EXCESS * 0.30" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
fi

# Activity bonuses for good patterns
if (( $(echo "$DAILY_MILES >= 80 && $DAILY_MILES <= 250" | bc -l) )) && (( $(echo "$DAILY_SPENDING >= 50 && $DAILY_SPENDING <= 300" | bc -l) )); then
    BONUS=$(echo "scale=4; $BASE * 0.03" | bc)
    BASE=$(echo "scale=4; $BASE + $BONUS" | bc)
fi

# Ensure reasonable minimum
if (( $(echo "$BASE < 80" | bc -l) )); then
    BASE="80"
fi

# Final output with 2 decimal places
printf "%.2f\n" $BASE