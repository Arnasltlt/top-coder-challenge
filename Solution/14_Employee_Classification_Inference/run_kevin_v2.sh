#!/bin/bash

# Kevin-Inspired Multi-Path Reimbursement System v2
# Based on actual data analysis, not Kevin's theories

read -r trip_duration_days
read -r miles_traveled  
read -r total_receipts_amount

# Ensure we have valid numbers
if [ -z "$trip_duration_days" ] || [ -z "$miles_traveled" ] || [ -z "$total_receipts_amount" ]; then
    echo "0.00"
    exit 0
fi

# Calculate key metrics
efficiency=$(echo "$miles_traveled $trip_duration_days" | awk '{printf "%.2f", $1 / $2}')
spending_per_day=$(echo "$total_receipts_amount $trip_duration_days" | awk '{printf "%.2f", $1 / $2}')

# Classify trip based on actual patterns found
classify_trip() {
    local days=$1
    local miles=$2
    local receipts=$3
    local eff=$4
    local spend_per_day=$5
    
    # Check for vacation penalty pattern (8+ days, high spending)
    vacation_check=$(echo "$days $spend_per_day" | awk '{print ($1 >= 8 && $2 > 120)}')
    if [ "$vacation_check" = "1" ]; then
        echo "vacation_penalty"
        return
    fi
    
    # Check for efficiency sweet spot (180-220 mi/day)
    sweet_spot_check=$(echo "$eff" | awk '{print ($1 >= 180 && $1 <= 220)}')
    if [ "$sweet_spot_check" = "1" ]; then
        echo "efficiency_sweet_spot"
        return
    fi
    
    # Check for quick high mileage (≤3 days, >200 mi/day)
    quick_high_check=$(echo "$days $eff" | awk '{print ($1 <= 3 && $2 > 200)}')
    if [ "$quick_high_check" = "1" ]; then
        echo "quick_high_mileage"
        return
    fi
    
    # Check for long low mileage (≥7 days, <100 mi/day)
    long_low_check=$(echo "$days $eff" | awk '{print ($1 >= 7 && $2 < 100)}')
    if [ "$long_low_check" = "1" ]; then
        echo "long_low_mileage"
        return
    fi
    
    # Everything else is medium balanced
    echo "medium_balanced"
}

# Calculate reimbursement based on trip category
calculate_reimbursement() {
    local category=$1
    local days=$2
    local miles=$3
    local receipts=$4
    local eff=$5
    local spend_per_day=$6
    
    # Interaction terms that matter
    days_x_efficiency=$(echo "$days $eff" | awk '{printf "%.2f", $1 * $2}')
    spending_x_miles=$(echo "$spend_per_day $miles" | awk '{printf "%.2f", $1 * $2}')
    days_x_spending=$(echo "$days $spend_per_day" | awk '{printf "%.2f", $1 * $2}')
    
    case "$category" in
        "quick_high_mileage")
            # Coefficients: days=103.43, miles=0.2069, receipts=0.2248, intercept=-73.09
            result=$(echo "$days $miles $receipts $eff $spend_per_day $days_x_efficiency $spending_x_miles $days_x_spending" | \
                awk '{printf "%.2f", 103.43*$1 + 0.2069*$2 + 0.2248*$3 + 0*$4 + 0*$5 + 0*$6 + 0*$7 + 0*$8 - 73.09}')
            ;;
        "long_low_mileage")
            # Coefficients: days=40.36, miles=0.0871, receipts=0.5151, intercept=112.68
            result=$(echo "$days $miles $receipts $eff $spend_per_day $days_x_efficiency $spending_x_miles $days_x_spending" | \
                awk '{printf "%.2f", 40.36*$1 + 0.0871*$2 + 0.5151*$3 + 0*$4 + 0*$5 + 0*$6 + 0*$7 + 0*$8 + 112.68}')
            ;;
        "medium_balanced")
            # Coefficients: days=58.22, miles=0.3293, receipts=0.2556, intercept=139.73
            result=$(echo "$days $miles $receipts $eff $spend_per_day $days_x_efficiency $spending_x_miles $days_x_spending" | \
                awk '{printf "%.2f", 58.22*$1 + 0.3293*$2 + 0.2556*$3 + 0*$4 + 0*$5 + 0*$6 + 0*$7 + 0*$8 + 139.73}')
            ;;
        "efficiency_sweet_spot")
            # Coefficients: days=304.22, miles=-0.2340, receipts=0.3632, intercept=-902.63
            result=$(echo "$days $miles $receipts $eff $spend_per_day $days_x_efficiency $spending_x_miles $days_x_spending" | \
                awk '{printf "%.2f", 304.22*$1 + (-0.2340)*$2 + 0.3632*$3 + 0*$4 + 0*$5 + 0*$6 + 0*$7 + 0*$8 + (-902.63)}')
            ;;
        "vacation_penalty")
            # Coefficients: days=120.50, miles=0.0530, receipts=-0.1284, intercept=203.29
            result=$(echo "$days $miles $receipts $eff $spend_per_day $days_x_efficiency $spending_x_miles $days_x_spending" | \
                awk '{printf "%.2f", 120.50*$1 + 0.0530*$2 + (-0.1284)*$3 + 0*$4 + 0*$5 + 0*$6 + 0*$7 + 0*$8 + 203.29}')
            ;;
        *)
            # Fallback to medium balanced
            result=$(echo "$days $miles $receipts $eff $spend_per_day $days_x_efficiency $spending_x_miles $days_x_spending" | \
                awk '{printf "%.2f", 58.22*$1 + 0.3293*$2 + 0.2556*$3 + 139.73}')
            ;;
    esac
    
    echo $result
}

# Main execution
category=$(classify_trip $trip_duration_days $miles_traveled $total_receipts_amount $efficiency $spending_per_day)
reimbursement=$(calculate_reimbursement $category $trip_duration_days $miles_traveled $total_receipts_amount $efficiency $spending_per_day)

echo $reimbursement