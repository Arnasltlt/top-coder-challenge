#!/usr/bin/env python3

import json
import math

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
    
    return X, y

def matrix_multiply(A, B):
    """Simple matrix multiplication"""
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            sum_val = 0
            for k in range(len(B)):
                sum_val += A[i][k] * B[k][j]
            row.append(sum_val)
        result.append(row)
    return result

def matrix_transpose(matrix):
    """Transpose a matrix"""
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def matrix_inverse_3x3(matrix):
    """Calculate inverse of 3x3 matrix"""
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    
    det = a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)
    
    if abs(det) < 1e-10:
        raise ValueError("Matrix is singular")
    
    inv = [
        [(e*i - f*h)/det, (c*h - b*i)/det, (b*f - c*e)/det],
        [(f*g - d*i)/det, (a*i - c*g)/det, (c*d - a*f)/det],
        [(d*h - e*g)/det, (b*g - a*h)/det, (a*e - b*d)/det]
    ]
    
    return inv

def solve_normal_equations(X, y):
    """Solve normal equations to find coefficients"""
    # Add intercept column (column of 1s)
    X_with_intercept = []
    for row in X:
        X_with_intercept.append(row + [1.0])
    
    # X^T
    Xt = matrix_transpose(X_with_intercept)
    
    # X^T * X
    XtX = matrix_multiply(Xt, X_with_intercept)
    
    # X^T * y
    Xty = []
    for i in range(len(Xt)):
        sum_val = 0
        for j in range(len(y)):
            sum_val += Xt[i][j] * y[j]
        Xty.append([sum_val])
    
    # (X^T * X)^-1
    XtX_inv = matrix_inverse_3x3(XtX[:3])  # Take first 3x3 for the main coefficients
    
    # Actually, let's use a simpler approach with least squares
    # We'll solve the system using Gaussian elimination
    
    # Build augmented matrix for system XtX * beta = Xty
    n = len(XtX)
    augmented = []
    for i in range(n):
        row = XtX[i] + [Xty[i][0]]
        augmented.append(row)
    
    # Gaussian elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                max_row = k
        
        # Swap rows
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            if augmented[i][i] != 0:
                factor = augmented[k][i] / augmented[i][i]
                for j in range(i, n+1):
                    augmented[k][j] -= factor * augmented[i][j]
    
    # Back substitution
    solution = [0] * n
    for i in range(n-1, -1, -1):
        solution[i] = augmented[i][n]
        for j in range(i+1, n):
            solution[i] -= augmented[i][j] * solution[j]
        if augmented[i][i] != 0:
            solution[i] /= augmented[i][i]
    
    return solution

def simple_least_squares(X, y):
    """Simple least squares using direct calculation"""
    n = len(X)
    
    # Calculate means
    mean_days = sum(row[0] for row in X) / n
    mean_miles = sum(row[1] for row in X) / n
    mean_receipts = sum(row[2] for row in X) / n
    mean_y = sum(y) / n
    
    # Try simple approach: minimize sum of squared errors
    # We'll use grid search to find approximate values first
    best_error = float('inf')
    best_coeffs = None
    
    # Rough grid search
    for A in range(0, 200, 5):
        for B in range(0, 5, 1):
            for C in range(0, 20, 1):
                error = 0
                for i in range(n):
                    days, miles, receipts = X[i]
                    predicted = A * days + B * miles + C * receipts
                    error += (predicted - y[i]) ** 2
                
                if error < best_error:
                    best_error = error
                    best_coeffs = (A, B, C)
    
    # Fine-tune around best values
    A_base, B_base, C_base = best_coeffs
    best_error = float('inf')
    
    for A in [A_base + i * 0.1 for i in range(-10, 11)]:
        for B in [B_base + i * 0.1 for i in range(-10, 11)]:
            for C in [C_base + i * 0.1 for i in range(-10, 11)]:
                error = 0
                for i in range(n):
                    days, miles, receipts = X[i]
                    predicted = A * days + B * miles + C * receipts
                    error += (predicted - y[i]) ** 2
                
                if error < best_error:
                    best_error = error
                    best_coeffs = (A, B, C)
    
    return best_coeffs

def main():
    # Load the public cases data
    X, y = load_data('../../public_cases.json')
    
    print(f"Loaded {len(X)} test cases")
    
    # Find best coefficients using simple approach
    A, B, C = simple_least_squares(X, y)
    
    print(f"\nLinear Model Coefficients:")
    print(f"A (days coefficient): {A:.6f}")
    print(f"B (miles coefficient): {B:.6f}")
    print(f"C (receipts coefficient): {C:.6f}")
    
    # Calculate performance metrics
    total_error = 0
    total_abs_error = 0
    
    for i in range(len(X)):
        days, miles, receipts = X[i]
        predicted = A * days + B * miles + C * receipts
        actual = y[i]
        error = predicted - actual
        total_error += error ** 2
        total_abs_error += abs(error)
    
    mse = total_error / len(X)
    rmse = math.sqrt(mse)
    mae = total_abs_error / len(X)
    
    print(f"\nModel Performance:")
    print(f"Mean Squared Error: {mse:.6f}")
    print(f"Root Mean Squared Error: {rmse:.6f}")
    print(f"Mean Absolute Error: {mae:.6f}")
    
    # Show some example predictions vs actual
    print(f"\nSample Predictions vs Actual:")
    for i in range(min(10, len(X))):
        days, miles, receipts = X[i]
        actual = y[i]
        predicted = A * days + B * miles + C * receipts
        print(f"Case {i+1}: Days={days}, Miles={miles}, Receipts=${receipts:.2f} -> Predicted: ${predicted:.2f}, Actual: ${actual:.2f}, Error: ${abs(predicted-actual):.2f}")
    
    # Write coefficients to a file for the run.sh script
    with open('coefficients.txt', 'w') as f:
        f.write(f"{A:.6f}\n")
        f.write(f"{B:.6f}\n")
        f.write(f"{C:.6f}\n")
    
    print(f"\nCoefficients saved to coefficients.txt")

if __name__ == "__main__":
    main()