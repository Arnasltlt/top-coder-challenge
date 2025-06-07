#!/bin/bash

# 1960s FINAL CHAMPION - v8 (OUR BEST SCORE)
# Team 15: Claude-M60 - ULTIMATE 1960s SIMPLICITY CHAMPION!

set -e

TRIP_DAYS=$1
MILES=$2
RECEIPTS=$3

# Optimized daily rates (granular but simple)
if [ "$TRIP_DAYS" -eq 1 ]; then
    DAYS_AMOUNT=$(echo "$TRIP_DAYS * 125" | bc)
elif [ "$TRIP_DAYS" -eq 2 ]; then
    DAYS_AMOUNT=$(echo "$TRIP_DAYS * 108" | bc)
elif [ "$TRIP_DAYS" -eq 3 ]; then
    DAYS_AMOUNT=$(echo "$TRIP_DAYS * 102" | bc)
else
    DAYS_AMOUNT=$(echo "$TRIP_DAYS * 98" | bc)
fi

MILES_AMOUNT=$(echo "$MILES * 0.56" | bc -l)

# Receipt handling with 1960s-style caps and tiers
DAILY_RECEIPT_AVG=$(echo "scale=2; $RECEIPTS / $TRIP_DAYS" | bc -l)

if [ "$(echo "$DAILY_RECEIPT_AVG > 200" | bc -l)" -eq 1 ]; then
    RECEIPTS_AMOUNT=$(echo "$RECEIPTS * 0.20" | bc -l)
elif [ "$(echo "$DAILY_RECEIPT_AVG > 150" | bc -l)" -eq 1 ]; then
    RECEIPTS_AMOUNT=$(echo "$RECEIPTS * 0.35" | bc -l)
elif [ "$(echo "$DAILY_RECEIPT_AVG < 30" | bc -l)" -eq 1 ]; then
    RECEIPTS_AMOUNT=$(echo "$RECEIPTS * 0.80" | bc -l)
else
    RECEIPTS_AMOUNT=$(echo "$RECEIPTS * 0.55" | bc -l)
fi

TOTAL=$(echo "$DAYS_AMOUNT + $MILES_AMOUNT + $RECEIPTS_AMOUNT" | bc -l)

printf "%.2f\n" "$TOTAL"