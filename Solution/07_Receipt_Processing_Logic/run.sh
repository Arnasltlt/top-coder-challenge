#!/bin/bash

# Test Version 2: Fix 1-day trip penalties and add short trip receipt caps
# Based on new analysis showing 1-day trips being under-estimated

trip_duration_days=$1
miles_traveled=$2
total_receipts_amount=$3

# Improved base calculation based on analysis
# Per diem: approximately $110 per day with some variation 
# Mileage: approximately $0.45 per mile with tiered rates
base_per_diem=$(echo "scale=2; $trip_duration_days * 110" | bc)

# Tiered mileage calculation
if (( $(echo "$miles_traveled <= 100" | bc -l) )); then
    # Standard rate for first 100 miles
    base_mileage=$(echo "scale=2; $miles_traveled * 0.58" | bc)
else
    # Reduced rate for miles over 100
    first_100=$(echo "scale=2; 100 * 0.58" | bc)
    excess_miles=$(echo "scale=2; $miles_traveled - 100" | bc)
    excess_mileage=$(echo "scale=2; $excess_miles * 0.42" | bc)
    base_mileage=$(echo "scale=2; $first_100 + $excess_mileage" | bc)
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

# NEW RULE 8: Short trip extreme spending cap
# Short trips (1-5 days) with very high daily spending (>$300/day) get severe caps
if (( $(echo "$trip_duration_days <= 5" | bc -l) )) && (( $(echo "$daily_spending > 300" | bc -l) )); then
    # Cap receipts at $200/day for short trips with extreme spending
    max_receipts=$(echo "scale=2; $trip_duration_days * 200" | bc)
    if (( $(echo "$total_receipts_amount > $max_receipts" | bc -l) )); then
        excess=$(echo "scale=2; $total_receipts_amount - $max_receipts" | bc)
        receipt_contribution=$(echo "scale=2; $max_receipts + $excess * 0.1" | bc)
    fi
fi

# Calculate final reimbursement
final_reimbursement=$(echo "scale=2; $base_total + $receipt_contribution" | bc)

# NEW RULE 7: Universal Long Trip Penalty (adjusted)
# Trips 11+ days get progressively larger penalties (not 10+ as before)
if (( $(echo "$trip_duration_days >= 11" | bc -l) )); then
    if (( $(echo "$trip_duration_days >= 14" | bc -l) )); then
        # 14+ days: 35% penalty (reduced from 40%)
        final_reimbursement=$(echo "scale=2; $final_reimbursement * 0.65" | bc)
    elif (( $(echo "$trip_duration_days >= 12" | bc -l) )); then
        # 12-13 days: 25% penalty (reduced from 30%)
        final_reimbursement=$(echo "scale=2; $final_reimbursement * 0.75" | bc)
    else
        # 11 days: 15% penalty (reduced from 20%)
        final_reimbursement=$(echo "scale=2; $final_reimbursement * 0.85" | bc)
    fi
fi

# EDGE CASE RULE 1: Long trip penalty (modified to be more specific)
# Trips 12+ days with high daily spending (>$150/day) get an additional penalty
if (( $(echo "$trip_duration_days >= 12" | bc -l) )) && (( $(echo "$daily_spending > 150" | bc -l) )); then
    # Apply additional 15% penalty (reduced from 25%)
    final_reimbursement=$(echo "scale=2; $final_reimbursement * 0.85" | bc)
fi

# EDGE CASE RULE 3: Medium trip with very high spending penalty
# Trips 8-10 days with very high daily spending (>$170/day) get a penalty
if (( $(echo "$trip_duration_days >= 8 && $trip_duration_days <= 10" | bc -l) )) && (( $(echo "$daily_spending > 170" | bc -l) )); then
    # Apply 25% penalty (reduced from 30%)
    final_reimbursement=$(echo "scale=2; $final_reimbursement * 0.75" | bc)
fi

# EDGE CASE RULE 4: "Sweet Spot Combo" from interviews
# 5 days + 180+ miles/day + under $100/day = guaranteed bonus (hypothesis line 87-88)
miles_per_day=$(echo "scale=2; $miles_traveled / $trip_duration_days" | bc)
if (( $(echo "$trip_duration_days == 5" | bc -l) )) && (( $(echo "$miles_per_day >= 180" | bc -l) )) && (( $(echo "$daily_spending < 100" | bc -l) )); then
    # Apply 15% bonus for the sweet spot combo
    final_reimbursement=$(echo "scale=2; $final_reimbursement * 1.15" | bc)
fi

# EDGE CASE RULE 5: Short trip high mileage bonus (efficiency recognition)
# 2-3 day trips with very high daily mileage (>400 miles/day) seem to get bonuses
if (( $(echo "$trip_duration_days <= 3" | bc -l) )) && (( $(echo "$miles_per_day > 400" | bc -l) )); then
    # Apply efficiency bonus for high daily mileage on short trips
    final_reimbursement=$(echo "scale=2; $final_reimbursement * 1.5" | bc)
fi

# EDGE CASE RULE 6: Impossible travel scenarios get manual caps (REVISED)
# Only truly impossible scenarios: >1200 miles/day gets capped
if (( $(echo "$miles_per_day > 1200" | bc -l) )); then
    # Apply severe cap for physically impossible travel
    final_reimbursement=$(echo "scale=2; $final_reimbursement * 0.25" | bc)
fi

echo $final_reimbursement