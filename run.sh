#!/bin/bash

# Team 13: Precision Artifact Analysis
# Simulate 1960s mainframe arithmetic limitations (IBM System/360 style)

DAYS=$1
MILES=$2
RECEIPTS=$3

# Call our vintage arithmetic simulator
python3 "$(dirname "$0")/Solution/13_Precision_Artifact_Analysis/vintage_arithmetic.py" "$DAYS" "$MILES" "$RECEIPTS"