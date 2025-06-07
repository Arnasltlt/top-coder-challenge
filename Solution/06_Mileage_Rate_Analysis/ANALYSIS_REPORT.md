# Mileage Rate Analysis Report

## Summary
Analysis of 1,000 test cases from public_cases.json to understand the relationship between miles_traveled and reimbursement amounts.

## Key Findings

### 1. Representative Input/Output Examples
Here are 15 representative examples showing the relationship between miles and reimbursement:

| Days | Miles | Receipts | Output | Miles-Only Component* |
|------|-------|----------|--------|-----------------------|
| 2    | 13    | $4.67    | $203.52| $198.85              |
| 1    | 55    | $3.60    | $126.06| $122.46              |
| 1    | 47    | $17.97   | $128.91| $110.94              |
| 3    | 93    | $1.42    | $364.51| $363.09              |
| 1    | 76    | $13.74   | $158.35| $144.61              |
| 3    | 117   | $21.99   | $359.10| $337.11              |
| 2    | 202   | $21.24   | $356.17| $334.93              |
| 1    | 141   | $10.15   | $195.14| $184.99              |
| 4    | 477   | $18.97   | $631.50| $612.53              |
| 5    | 733   | $41.18   | $771.83| $730.65              |
| 7    | 803   | $12.75   | $1146.78| $1134.03            |
| 1    | 893   | $19.76   | $570.71| $550.95              |
| 5    | 592   | $433.75  | $869.00| $435.25              |
| 3    | 606   | $1184.23 | $1364.54| $180.31             |
| 8    | 795   | $1645.99 | $644.69| $-1001.30           |

*Miles-Only Component = Output - Receipts (rough approximation)

### 2. Current Linear Model Performance
The existing linear model uses: `reimbursement = 50.05 * days + 0.446 * miles + 0.383 * receipts + 266.71`

**Performance Metrics:**
- Average error: $175.49
- Median error: $156.59
- Maximum error: $1,064.47

**Error by Mileage Range:**
| Range    | Cases | Avg Error | Median Error |
|----------|-------|-----------|--------------|
| 0-100    | 93    | $179.04   | $177.57      |
| 101-200  | 86    | $170.46   | $166.23      |
| 201-400  | 170   | $157.99   | $147.25      |
| 401-600  | 135   | $172.76   | $154.04      |
| 601-800  | 184   | $164.38   | $146.00      |
| 801-1000 | 167   | $176.66   | $159.42      |

### 3. Mileage Rate Structure Analysis

#### Evidence for Complexity Beyond Linear Model:
1. **Negative effective rates** for low mileage suggest the linear model's coefficients don't properly capture the base structure
2. **Different effective rates** between low and high mileage cases
3. **Large errors** on cases with high receipts suggest receipt processing affects mileage calculation

#### Observed Patterns:
- **Low mileage (≤200 miles)**: Average effective rate of -$2.45/mile (indicates base structure issues)
- **High mileage (>500 miles)**: Average effective rate of $0.43/mile
- **Linear model baseline**: $0.446/mile

### 4. Specific Mileage Component Insights

From 1-day trips with minimal receipts (isolates mileage effect):
| Miles | Output | Estimated Mileage Rate |
|-------|--------|-----------------------|
| 47    | $128.91| $0.87/mile            |
| 55    | $126.06| $0.95/mile            |
| 76    | $158.35| $0.98/mile            |
| 133   | $179.06| $0.76/mile            |
| 141   | $195.14| $0.82/mile            |
| 893   | $570.71| $0.54/mile            |

*Assuming $70 base daily allowance

### 5. Evidence for Caps or Tiers
High mileage cases show significantly lower effective rates:
- Cases with 600+ miles show rates between $0.15-$0.83/mile
- Some high-mileage cases even show negative effective rates
- This suggests either caps on mileage reimbursement or complex interaction with other factors

## Recommendations

### Primary Recommendation: Refined Linear Model
Continue using the linear model as the baseline with **$0.446 per mile** rate because:
1. It provides consistent performance across all mileage ranges
2. Average error (~$175) may be acceptable for business purposes
3. Implementation simplicity

### Secondary Recommendations for Accuracy Improvement:

1. **Investigate Receipt Processing Impact**: The large errors often correlate with high receipt amounts, suggesting the receipt coefficient (0.383) may not be constant

2. **Consider Tiered Structure**: If higher accuracy is needed:
   - First 400 miles: ~$0.80/mile
   - Miles above 400: ~$0.40/mile
   - This could reduce errors on high-mileage cases

3. **Validate Base Structure**: The significant negative effective rates for low mileage suggest the daily base ($50.05) and intercept ($266.71) may need adjustment

### Formula for Implementation:
```
reimbursement = 50.05 * trip_duration_days + 0.446 * miles_traveled + 0.383 * total_receipts_amount + 266.71
```

This provides the best balance of accuracy and simplicity based on the available data.