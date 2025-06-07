#!/usr/bin/env python3
import json
import sys
import math

def load_cases(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def euclidean_distance(input1, input2):
    # Normalize features to similar scales for better distance calculation
    # Days: 1-7 typical range
    # Miles: 0-1000+ typical range  
    # Receipts: 0-1000+ typical range
    
    # Scale factors to normalize features
    days_scale = 10.0  # Give days more weight
    miles_scale = 1.0
    receipts_scale = 1.0
    
    days_diff = (input1["trip_duration_days"] - input2["trip_duration_days"]) * days_scale
    miles_diff = (input1["miles_traveled"] - input2["miles_traveled"]) * miles_scale
    receipts_diff = (input1["total_receipts_amount"] - input2["total_receipts_amount"]) * receipts_scale
    
    return math.sqrt(days_diff**2 + miles_diff**2 + receipts_diff**2)

def find_nearest_neighbors(target_input, cases, k=5):
    distances = []
    
    for case in cases:
        dist = euclidean_distance(target_input, case["input"])
        distances.append((dist, case["expected_output"]))
    
    # Sort by distance and take k nearest
    distances.sort(key=lambda x: x[0])
    return distances[:k]

def predict_reimbursement(target_input, cases, k=5):
    neighbors = find_nearest_neighbors(target_input, cases, k)
    
    if not neighbors:
        return 0.0
    
    # Check for exact matches first
    if neighbors[0][0] == 0.0:
        return neighbors[0][1]
    
    # Weighted average based on inverse distance
    total_weight = 0.0
    weighted_sum = 0.0
    
    for distance, output in neighbors:
        # Use inverse distance weighting, with small epsilon to avoid division by zero
        weight = 1.0 / (distance + 0.001)
        weighted_sum += weight * output
        total_weight += weight
    
    return weighted_sum / total_weight if total_weight > 0 else neighbors[0][1]

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 knn_memorizer.py <days> <miles> <receipts>", file=sys.stderr)
        sys.exit(1)
    
    try:
        days = int(sys.argv[1])
        miles = int(sys.argv[2])
        receipts = float(sys.argv[3])
    except ValueError:
        print("Error: Invalid input format", file=sys.stderr)
        sys.exit(1)
    
    target_input = {
        "trip_duration_days": days,
        "miles_traveled": miles,
        "total_receipts_amount": receipts
    }
    
    # Load the memorized cases
    cases = load_cases("public_cases.json")
    
    # Predict using k-nearest neighbors
    result = predict_reimbursement(target_input, cases, k=7)
    
    # Format to 2 decimal places
    print(f"{result:.2f}")

if __name__ == "__main__":
    main()