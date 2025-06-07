#!/bin/bash

# Team 11: Brute Force Memorization Strategy
# Use k-Nearest Neighbors to find closest memorized cases

DAYS=$1
MILES=$2
RECEIPTS=$3

# Call our Python KNN memorizer
python3 knn_memorizer.py "$DAYS" "$MILES" "$RECEIPTS"