#!/usr/bin/env python3
import json

print("🎯 DATA-DRIVEN COEFFICIENT FITTING 🎯")
print("Using LINEAR REGRESSION on training data (like we should have from the start!)")

# Load training data
with open('../public_cases.json', 'r') as f:
    cases = json.load(f)

print(f"Analyzing {len(cases)} training cases for optimal coefficients...")

# Prepare data for linear regression
X = []  # Features: [days, miles, receipts]
y = []  # Target: reimbursement amounts

for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    X.append([1, days, miles, receipts])  # Include intercept term
    y.append(expected)

print(f"Prepared {len(X)} data points for regression")

# Manual least squares implementation (since we don't have numpy)
# Using normal equations: β = (X'X)^(-1)X'y

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def matrix_inverse_2x2(A):
    # For 2x2 matrix [[a,b],[c,d]], inverse is (1/det) * [[d,-b],[-c,a]]
    a, b = A[0][0], A[0][1]
    c, d = A[1][0], A[1][1]
    det = a*d - b*c
    if abs(det) < 1e-10:
        return None
    return [[d/det, -b/det], [-c/det, a/det]]

# Simple approach: analyze correlations and patterns
print("\n📊 CORRELATION ANALYSIS:")

# Calculate means
n = len(cases)
mean_days = sum(case['input']['trip_duration_days'] for case in cases) / n
mean_miles = sum(case['input']['miles_traveled'] for case in cases) / n  
mean_receipts = sum(case['input']['total_receipts_amount'] for case in cases) / n
mean_reimbursement = sum(case['expected_output'] for case in cases) / n

print(f"Mean days: {mean_days:.2f}")
print(f"Mean miles: {mean_miles:.2f}")
print(f"Mean receipts: ${mean_receipts:.2f}")
print(f"Mean reimbursement: ${mean_reimbursement:.2f}")

# Calculate simple correlations
def correlation(x_vals, y_vals):
    n = len(x_vals)
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n
    
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
    den_x = sum((x - mean_x)**2 for x in x_vals)**0.5
    den_y = sum((y - mean_y)**2 for y in y_vals)**0.5
    
    if den_x == 0 or den_y == 0:
        return 0
    return num / (den_x * den_y)

days_vals = [case['input']['trip_duration_days'] for case in cases]
miles_vals = [case['input']['miles_traveled'] for case in cases]
receipts_vals = [case['input']['total_receipts_amount'] for case in cases]
reimbursement_vals = [case['expected_output'] for case in cases]

corr_days = correlation(days_vals, reimbursement_vals)
corr_miles = correlation(miles_vals, reimbursement_vals)
corr_receipts = correlation(receipts_vals, reimbursement_vals)

print(f"Days correlation: {corr_days:.3f}")
print(f"Miles correlation: {corr_miles:.3f}")
print(f"Receipts correlation: {corr_receipts:.3f}")

# Simple coefficient estimation using ratios
print(f"\n🔢 ESTIMATED COEFFICIENTS:")

# Days coefficient: reimbursement per day
days_coeff = mean_reimbursement / mean_days
print(f"Days coefficient (naive): ${days_coeff:.2f}/day")

# Miles coefficient: reimbursement per mile
miles_coeff = corr_miles * (sum((r - mean_reimbursement)**2 for r in reimbursement_vals)**0.5 / 
                            sum((m - mean_miles)**2 for m in miles_vals)**0.5) / n
print(f"Miles coefficient (correlation-based): ${miles_coeff:.3f}/mile")

# Receipts coefficient
receipts_coeff = corr_receipts * (sum((r - mean_reimbursement)**2 for r in reimbursement_vals)**0.5 / 
                                  sum((r - mean_receipts)**2 for r in receipts_vals)**0.5) / n
print(f"Receipts coefficient (correlation-based): ${receipts_coeff:.3f}/dollar")

# 5-day trip analysis
print(f"\n🎯 5-DAY TRIP ANALYSIS:")
by_days = {}
for case in cases:
    days = case['input']['trip_duration_days']
    if days not in by_days:
        by_days[days] = []
    by_days[days].append(case['expected_output'])

for days in sorted(by_days.keys())[:10]:
    avg_reimbursement = sum(by_days[days]) / len(by_days[days])
    print(f"{days}-day trips: ${avg_reimbursement:.2f} average ({len(by_days[days])} cases)")

if 5 in by_days:
    five_day_avg = sum(by_days[5]) / len(by_days[5])
    overall_avg = mean_reimbursement
    five_day_bonus = five_day_avg - overall_avg
    print(f"5-day bonus: ${five_day_bonus:.2f}")

print(f"\n✅ Analysis complete! Use these insights to build data-driven model.")