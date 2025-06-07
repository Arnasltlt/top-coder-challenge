# Test Results Analysis - First 10 Cases

## Current Model Performance

**Model Used**: Linear regression with coefficients:
- Days: 50.050486
- Miles: 0.446
- Receipts: 0.382861
- Intercept: 266.707681

**Formula**: `Reimbursement = 50.050486 × days + 0.446 × miles + 0.382861 × receipts + 266.707681`

## Test Results Summary

| Case | Days | Miles | Receipts | Expected | Actual | Error | Abs Error |
|------|------|-------|----------|----------|--------|--------|-----------|
| 1    | 3    | 93    | 1.42     | 364.51   | 458.88 | +94.37 | 94.37     |
| 2    | 1    | 55    | 3.6      | 126.06   | 342.67 | +216.61| 216.61    |
| 3    | 1    | 47    | 17.97    | 128.91   | 344.60 | +215.69| 215.69    |
| 4    | 2    | 13    | 4.67     | 203.52   | 374.39 | +170.87| 170.87    |
| 5    | 3    | 88    | 5.78     | 380.37   | 458.32 | +77.95 | 77.95     |
| 6    | 1    | 76    | 13.74    | 158.35   | 355.91 | +197.56| 197.56    |
| 7    | 3    | 41    | 4.52     | 320.12   | 436.88 | +116.76| 116.76    |
| 8    | 1    | 140   | 22.71    | 199.68   | 387.89 | +188.21| 188.21    |
| 9    | 3    | 121   | 21.17    | 464.07   | 478.93 | +14.86 | 14.86     |
| 10   | 3    | 117   | 21.99    | 359.10   | 477.46 | +118.36| 118.36    |

**Mean Absolute Error: 141.12**

## Error Pattern Analysis

### Critical Issues Identified:

1. **Short Trip Over-Prediction**: All 1-day trips show massive over-prediction (200+ error)
   - Case 2, 3, 6, 8 are all 1-day trips with huge errors
   - The intercept (266.71) is too high for short trips

2. **Low Mileage Issues**: Trips with < 100 miles tend to have higher errors
   - Cases 2, 3, 4, 7 all have low mileage and high errors

3. **Systematic Over-Prediction**: All cases show positive errors (over-prediction)
   - Suggests the model baseline is too high

### Best Performing Case:
- **Case 9**: 3 days, 121 miles, 21.17 receipts - Only 14.86 error
- This suggests the model works better for longer trips with moderate mileage

### Recommendations for Model Improvement:

1. **Reduce Intercept**: The base amount (266.71) is clearly too high
2. **Add Trip Length Penalty**: Short trips (1-2 days) need different treatment
3. **Non-Linear Mileage**: Consider tiered mileage rates
4. **Receipt Processing**: The linear treatment of receipts may be too simplistic

### Next Steps:
1. Analyze more test cases to confirm patterns
2. Implement non-linear adjustments for short trips
3. Consider separate models for different trip duration ranges
4. Add edge case handling for extreme values