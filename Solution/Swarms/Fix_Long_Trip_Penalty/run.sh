#!/bin/bash

# Team 13: Precision Artifact Analysis - Fix Long Trip Penalty
# Simulate 1960s mainframe arithmetic limitations (IBM System/360 style)

DAYS=$1
MILES=$2
RECEIPTS=$3

# Call our vintage arithmetic simulator (local version with long trip fix)
python3 "$(dirname "$0")/vintage_arithmetic.py" "$DAYS" "$MILES" "$RECEIPTS"