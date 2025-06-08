#!/bin/bash

# Final Model runner – isolated integration sandbox
DAYS=$1
MILES=$2
RECEIPTS=$3

python3 "$(dirname "$0")/vintage_final.py" "$DAYS" "$MILES" "$RECEIPTS"