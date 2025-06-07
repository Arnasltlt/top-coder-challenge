#!/bin/bash

# FINAL: Best Linear Model Implementation
# Must be rock-solid reliable for evaluation

read -r days
read -r miles  
read -r receipts

# Basic validation and ensure we have numbers
days=$(echo "$days" | awk '{print $1 + 0}')
miles=$(echo "$miles" | awk '{print $1 + 0}')  
receipts=$(echo "$receipts" | awk '{print $1 + 0}')

# Ensure receipts is positive for log calculation
if [ "$(echo "$receipts" | awk '{print ($1 <= 0)}')" = "1" ]; then
    receipts="0.01"
fi

# All-in-one calculation using awk for maximum reliability
awk -v d="$days" -v m="$miles" -v r="$receipts" '
BEGIN {
    # Calculate all features
    days_sq = d * d
    miles_sq = m * m
    receipts_sq = r * r
    days_x_miles = d * m
    days_x_receipts = d * r
    miles_x_receipts = m * r
    sqrt_miles = sqrt(m)
    log_receipts = log(r)
    
    # Apply the comprehensive model
    result = 101.43812092241279 * d + \
             0.9159822252696035 * m + \
             1.7412290638839176 * r + \
             (-2.91522454129986) * days_sq + \
             (-0.0001461776136881632) * miles_sq + \
             (-0.0004023037445342217) * receipts_sq + \
             0.007604553460334047 * days_x_miles + \
             (-0.011331502380787627) * days_x_receipts + \
             (-0.0001482594897139667) * miles_x_receipts + \
             (-8.147963153598235) * sqrt_miles + \
             (-148.82333158224108) * log_receipts + \
             422.2031061975697
             
    printf "%.2f\n", result
}'