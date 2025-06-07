#!/usr/bin/env python3

import json
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import sys

def load_data(filename):
    """Load the test cases from JSON file"""
    with open(filename, 'r') as f:
        data = json.load(f)
    
    X = []  # Features: [days, miles, receipts]
    y = []  # Target: expected_output
    
    for case in data:
        input_data = case['input']
        X.append([
            input_data['trip_duration_days'],
            input_data['miles_traveled'], 
            input_data['total_receipts_amount']
        ])
        y.append(case['expected_output'])
    
    return np.array(X), np.array(y)

def main():
    # Load the public cases data
    X, y = load_data('../../public_cases.json')
    
    print(f"Loaded {len(X)} test cases")
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Fit linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Get coefficients
    A, B, C = model.coef_
    intercept = model.intercept_
    
    print(f"\nLinear Model Coefficients:")
    print(f"A (days coefficient): {A:.6f}")
    print(f"B (miles coefficient): {B:.6f}")
    print(f"C (receipts coefficient): {C:.6f}")
    print(f"Intercept: {intercept:.6f}")
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate metrics
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, y_pred)
    
    print(f"\nModel Performance:")
    print(f"Mean Squared Error: {mse:.6f}")
    print(f"Root Mean Squared Error: {rmse:.6f}")
    print(f"Mean Absolute Error: {mae:.6f}")
    
    # Show some example predictions vs actual
    print(f"\nSample Predictions vs Actual:")
    for i in range(min(10, len(X))):
        days, miles, receipts = X[i]
        actual = y[i]
        predicted = y_pred[i]
        print(f"Case {i+1}: Days={days}, Miles={miles}, Receipts=${receipts:.2f} -> Predicted: ${predicted:.2f}, Actual: ${actual:.2f}, Error: ${abs(predicted-actual):.2f}")
    
    # Write coefficients to a file for the run.sh script
    with open('coefficients.txt', 'w') as f:
        f.write(f"{A:.6f}\n")
        f.write(f"{B:.6f}\n") 
        f.write(f"{C:.6f}\n")
        f.write(f"{intercept:.6f}\n")
    
    print(f"\nCoefficients saved to coefficients.txt")

if __name__ == "__main__":
    main()