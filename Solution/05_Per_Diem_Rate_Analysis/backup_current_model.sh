#!/bin/bash

# Current implementation backup - this is the more accurate model
trip_duration_days=$1
miles_traveled=$2
total_receipts_amount=$3

# Improved base calculation based on analysis
# Per diem: approximately $110 per day with some variation 
# Mileage: approximately $0.45 per mile with tiered rates
base_per_diem=$(echo "scale=2; $trip_duration_days * 110" | bc)

# Tiered mileage calculation based on analysis findings
# Analysis showed first 400 miles at ~$0.80/mile, then ~$0.40/mile for excess
if (( $(echo "$miles_traveled <= 400" | bc -l) )); then
    # First 400 miles at higher rate
    base_mileage=$(echo "scale=2; $miles_traveled * 0.80" | bc)
else
    # First 400 miles at 0.80, remaining at 0.40
    first_400=$(echo "scale=2; 400 * 0.80" | bc)
    excess_miles=$(echo "scale=2; $miles_traveled - 400" | bc)
    excess_mileage=$(echo "scale=2; $excess_miles * 0.40" | bc)
    base_mileage=$(echo "scale=2; $first_400 + $excess_mileage" | bc)
fi

base_total=$(echo "scale=2; $base_per_diem + $base_mileage" | bc)

# Receipt processing with diminishing returns
# Based on interview analysis: medium spending ($50-120/day) gets good treatment
# Low spending gets penalized, high spending has caps

# Calculate daily spending rate
daily_spending=$(echo "scale=2; $total_receipts_amount / $trip_duration_days" | bc)

# Receipt processing logic based on daily spending patterns
if (( $(echo "$daily_spending < 20" | bc -l) )); then
    # Very low spending: penalized (get only 50% of receipts)
    receipt_contribution=$(echo "scale=2; $total_receipts_amount * 0.5" | bc)
elif (( $(echo "$daily_spending < 50" | bc -l) )); then
    # Low spending: reduced benefit (get 70% of receipts)
    receipt_contribution=$(echo "scale=2; $total_receipts_amount * 0.7" | bc)
elif (( $(echo "$daily_spending < 120" | bc -l) )); then
    # Medium spending: full benefit (get 100% of receipts)
    receipt_contribution=$total_receipts_amount
else
    # High spending: capped with diminishing returns
    # First $120 per day gets full value, excess gets 30%
    capped_amount=$(echo "scale=2; $trip_duration_days * 120" | bc)
    if (( $(echo "$total_receipts_amount > $capped_amount" | bc -l) )); then
        excess=$(echo "scale=2; $total_receipts_amount - $capped_amount" | bc)
        receipt_contribution=$(echo "scale=2; $capped_amount + $excess * 0.3" | bc)
    else
        receipt_contribution=$total_receipts_amount
    fi
fi

# Calculate final reimbursement
final_reimbursement=$(echo "scale=2; $base_total + $receipt_contribution" | bc)

echo $final_reimbursement