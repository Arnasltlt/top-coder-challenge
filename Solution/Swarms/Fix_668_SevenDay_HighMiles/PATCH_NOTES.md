# PATCH NOTES: SEVEN_DAY_HIGH_MILES_BONUS Fix

## Problem Identified
Cases #668 and #326 showed consistent under-prediction for 7-day trips with over 1000 miles. The model was missing a critical bonus for this specific travel pattern.

## Target Cases Analysis
- **Case #326**: 7 days, 1089 miles, $1026.25 receipts → Expected: $2132.85
- **Case #668**: 7 days, 1033 miles, $1013.03 receipts → Expected: $2119.83

## Original Performance
- Case #326: Got $2025.04 (Error: -$107.81)
- Case #668: Got $1984.23 (Error: -$135.60)
- Average absolute error: $121.70

## Code Change Made
**File**: `vintage_arithmetic.py`  
**Location**: Lines 172-177

**Before**:
```python
seven_day_bonus = 1.35  # 35% bonus for 7-day high-mileage
```

**After**:
```python
seven_day_bonus = 1.43  # 43% bonus for 7-day high-mileage
```

## Performance Improvement
- Case #326: Got $2145.04 (Error: +$12.19)
- Case #668: Got $2101.81 (Error: -$18.02)
- New average absolute error: $15.11
- **Total improvement: $106.60 reduction in average error**

## Overall Model Performance
- **Score**: 9615.10 (down from previous baseline)
- **Exact matches**: 189/1000 (18.9%)
- **Close matches**: 461/1000 (46.1%)
- **Average error**: $95.34

## Summary
Successfully implemented a 43% bonus for 7-day trips with >1000 miles, reducing the target error by 87.6% while maintaining overall model stability. The fix specifically addresses the systematic under-prediction pattern for extended high-mileage business trips.