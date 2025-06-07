#!/bin/bash

# ULTRA-REDESIGNED Reimbursement System
# Based on activity-reasonableness patterns and caps
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

DAYS=$1
MILES=$2  
RECEIPTS=$3

# Calculate activity metrics
DAILY_MILES=$(echo "scale=4; $MILES / $DAYS" | bc)
DAILY_SPENDING=$(echo "scale=4; $RECEIPTS / $DAYS" | bc)

# REASONABLENESS CHECK - Detect suspicious patterns
ACTIVITY_RATIO=0
if (( $(echo "$MILES > 0" | bc -l) )); then
    ACTIVITY_RATIO=$(echo "scale=4; $RECEIPTS / $MILES" | bc)
fi

# Base calculation by duration with different formulas
if [ "$DAYS" -eq 1 ]; then
    # 1-day trips: Cap around $1450, favor activity over receipts
    BASE=$(echo "scale=4; 80 + 0.95 * $MILES + 0.60 * $RECEIPTS" | bc)
    
    # Apply 1-day cap (observed max ~$1450)
    if (( $(echo "$BASE > 1450" | bc -l) )); then
        BASE="1450"
    fi
    
elif [ "$DAYS" -eq 2 ]; then
    # 2-day trips: Higher base, good mileage/receipt balance
    BASE=$(echo "scale=4; 160 + 0.75 * $MILES + 0.55 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -eq 3 ]; then
    # 3-day trips: Balanced approach
    BASE=$(echo "scale=4; 200 + 0.65 * $MILES + 0.50 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -ge 4 ] && [ "$DAYS" -le 6 ]; then
    # 4-6 day trips: Per diem focus
    BASE=$(echo "scale=4; $DAYS * 150 + 0.55 * $MILES + 0.45 * $RECEIPTS" | bc)
    
elif [ "$DAYS" -ge 7 ] && [ "$DAYS" -le 10 ]; then
    # 7-10 day trips: Higher per diem but diminishing returns
    BASE=$(echo "scale=4; $DAYS * 140 + 0.50 * $MILES + 0.40 * $RECEIPTS" | bc)
    
else
    # 11+ day trips: Strong diminishing returns
    FIRST_10=$(echo "scale=4; 10 * 140 + 0.50 * $MILES + 0.40 * $RECEIPTS" | bc)
    EXTRA_DAYS=$(echo "$DAYS - 10" | bc)
    EXTRA_AMOUNT=$(echo "scale=4; $EXTRA_DAYS * 80" | bc)
    BASE=$(echo "scale=4; $FIRST_10 + $EXTRA_AMOUNT" | bc)
fi

# REASONABLENESS PENALTIES

# High receipts with very low activity (major red flag)
if (( $(echo "$DAILY_MILES < 20" | bc -l) )) && (( $(echo "$DAILY_SPENDING > 400" | bc -l) )); then
    # SEVERE penalty for suspicious activity
    PENALTY=$(echo "scale=4; $BASE * 0.75" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
    
elif (( $(echo "$ACTIVITY_RATIO > 8" | bc -l) )) && (( $(echo "$MILES < 300" | bc -l) )); then
    # High receipt-to-mile ratio penalty
    PENALTY=$(echo "scale=4; $BASE * 0.40" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
fi

# MILEAGE CAPS - Very high mileage has diminishing returns
if (( $(echo "$MILES > 1000" | bc -l) )); then
    EXCESS_MILES=$(echo "scale=4; $MILES - 1000" | bc)
    PENALTY=$(echo "scale=4; $EXCESS_MILES * 0.30" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
fi

# RECEIPT CAPS - Very high daily spending diminishing returns  
if (( $(echo "$DAILY_SPENDING > 300" | bc -l) )); then
    EXCESS_DAILY=$(echo "scale=4; $DAILY_SPENDING - 300" | bc)
    TOTAL_EXCESS=$(echo "scale=4; $EXCESS_DAILY * $DAYS" | bc)
    PENALTY=$(echo "scale=4; $TOTAL_EXCESS * 0.60" | bc)
    BASE=$(echo "scale=4; $BASE - $PENALTY" | bc)
fi

# ACTIVITY BONUSES for reasonable patterns
if (( $(echo "$DAILY_MILES >= 100 && $DAILY_MILES <= 300" | bc -l) )) && (( $(echo "$DAILY_SPENDING >= 50 && $DAILY_SPENDING <= 200" | bc -l) )); then
    # Reasonable activity pattern bonus
    BONUS=$(echo "scale=4; $BASE * 0.05" | bc)
    BASE=$(echo "scale=4; $BASE + $BONUS" | bc)
fi

# Ensure minimum reimbursement (avoid negative values)
if (( $(echo "$BASE < 50" | bc -l) )); then
    BASE="50"
fi

# Final output with 2 decimal places
printf "%.2f\n" $BASE