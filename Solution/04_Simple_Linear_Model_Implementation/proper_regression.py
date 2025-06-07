#!/usr/bin/env python3

import json

def load_data(filename):
    """Load the test cases from JSON file"""
    with open(filename, 'r') as f:
        data = json.load(f)
    
    X = []  # Features: [days, miles, receipts, 1] (with intercept)
    y = []  # Target: expected_output
    
    for case in data:
        input_data = case['input']
        X.append([
            input_data['trip_duration_days'],
            input_data['miles_traveled'], 
            input_data['total_receipts_amount'],
            1.0  # intercept term
        ])
        y.append(case['expected_output'])
    
    return X, y

def matrix_transpose(matrix):
    """Transpose a matrix"""
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def matrix_multiply(A, B):
    """Matrix multiplication"""
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

def gauss_elimination(matrix):
    """Solve system using Gaussian elimination"""
    n = len(matrix)
    m = len(matrix[0])
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Make diagonal 1
        if matrix[i][i] != 0:
            pivot = matrix[i][i]
            for j in range(m):
                matrix[i][j] /= pivot
        
        # Eliminate column
        for k in range(n):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(m):
                    matrix[k][j] -= factor * matrix[i][j]
    
    # Extract solution
    solution = [matrix[i][m-1] for i in range(n)]
    return solution

def solve_linear_regression(X, y):
    """Solve linear regression using normal equations"""
    # X^T
    Xt = matrix_transpose(X)
    
    # X^T * X
    XtX = matrix_multiply(Xt, X)
    
    # X^T * y
    Xty = []
    for i in range(len(Xt)):
        sum_val = 0
        for j in range(len(y)):
            sum_val += Xt[i][j] * y[j]
        Xty.append(sum_val)
    
    # Create augmented matrix [XtX | Xty]
    augmented = []
    for i in range(len(XtX)):
        row = XtX[i] + [Xty[i]]
        augmented.append(row)
    
    # Solve using Gaussian elimination
    solution = gauss_elimination(augmented)
    
    return solution

def main():
    # Load the public cases data
    X, y = load_data('../../public_cases.json')
    
    print(f"Loaded {len(X)} test cases")
    
    # Solve linear regression
    coefficients = solve_linear_regression(X, y)
    
    A, B, C, intercept = coefficients
    
    print(f"\nLinear Model Coefficients:")
    print(f"A (days coefficient): {A:.6f}")
    print(f"B (miles coefficient): {B:.6f}")
    print(f"C (receipts coefficient): {C:.6f}")
    print(f"Intercept: {intercept:.6f}")
    
    # Calculate performance metrics
    total_error = 0
    total_abs_error = 0
    
    for i in range(len(X)):
        days, miles, receipts, _ = X[i]
        predicted = A * days + B * miles + C * receipts + intercept
        actual = y[i]
        error = predicted - actual
        total_error += error ** 2
        total_abs_error += abs(error)
    
    mse = total_error / len(X)
    rmse = (mse ** 0.5)
    mae = total_abs_error / len(X)
    
    print(f"\nModel Performance:")
    print(f"Mean Squared Error: {mse:.6f}")
    print(f"Root Mean Squared Error: {rmse:.6f}")
    print(f"Mean Absolute Error: {mae:.6f}")
    
    # Show some example predictions vs actual
    print(f"\nSample Predictions vs Actual:")
    for i in range(min(10, len(X))):
        days, miles, receipts, _ = X[i]
        actual = y[i]
        predicted = A * days + B * miles + C * receipts + intercept
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