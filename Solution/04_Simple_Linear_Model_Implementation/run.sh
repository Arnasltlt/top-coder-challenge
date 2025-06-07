#!/bin/bash

# Black Box Challenge - Reimbursement Calculation Implementation
# This script calculates reimbursement amounts based on trip duration, miles traveled, and receipt amounts
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

# Input parameters validation
if [ $# -ne 3 ]; then
    echo "Error: Exactly 3 parameters required" >&2
    echo "Usage: $0 <trip_duration_days> <miles_traveled> <total_receipts_amount>" >&2
    exit 1
fi

# Extract input parameters
trip_duration_days=$1
miles_traveled=$2
total_receipts_amount=$3

# Reimbursement calculation coefficients (derived from linear regression analysis)
# These coefficients were determined through systematic analysis of the public test cases:
# - Days coefficient: 50.050486 (base daily rate component)
# - Miles coefficient: 0.445645 (per-mile reimbursement rate)  
# - Receipts coefficient: 0.382861 (percentage of receipts reimbursed)
# - Intercept: 266.707681 (fixed base amount)
#
# Linear formula: reimbursement = 50.050486 * days + 0.445645 * miles + 0.382861 * receipts + 266.707681

# Perform calculation using bc for precise floating point arithmetic
result=$(echo "scale=2; 50.050486 * $trip_duration_days + 0.445645 * $miles_traveled + 0.382861 * $total_receipts_amount + 266.707681" | bc)

# Output the calculated reimbursement amount (single number as required)
echo $result 