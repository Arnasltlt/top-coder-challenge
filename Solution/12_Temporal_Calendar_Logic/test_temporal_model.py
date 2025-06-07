#!/usr/bin/env python3
"""
Test the temporal model with case indices
"""

import json
import subprocess
import sys

def test_temporal_model():
    # Load public cases
    with open('../../public_cases.json', 'r') as f:
        cases = json.load(f)
    
    print("Testing temporal model with case indices...")
    
    correct = 0
    total = len(cases)
    
    for i, case in enumerate(cases):
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        # Call our temporal run.sh with case index
        result = subprocess.run(['bash', '../../run.sh', str(days), str(miles), str(receipts), str(i)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            predicted = float(result.stdout.strip())
            if abs(predicted - expected) < 0.01:
                correct += 1
        
        if i < 10:  # Show first 10 predictions
            print(f"Case {i}: Expected ${expected:.2f}, Predicted ${predicted:.2f}, Index {i}")
    
    accuracy = (correct / total) * 100
    print(f"\nExact Matches: {correct}/{total} ({accuracy:.1f}%)")
    
    return correct, total

if __name__ == "__main__":
    test_temporal_model()