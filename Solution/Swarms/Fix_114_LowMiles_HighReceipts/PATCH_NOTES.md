# PATCH NOTES: LOW_MILES_HIGH_RECEIPTS_PENALTY Fix

## Problem Analysis
The original model suffered from massive over-predictions for trips with low miles (<300) and high daily receipts (>$120). The worst cases included:
- Case #115: +714.17 error (148.1% over-prediction)
- Case #244: +584.66 error (139.8% over-prediction)
- Case #434: +560.36 error (115.9% over-prediction)
- Case #82: +510.03 error (81.2% over-prediction)
- Case #83: +390.60 error (196.9% over-prediction)

## Solution Implemented
Replaced the simple penalty logic in vintage_arithmetic.py with a progressive penalty system:

### Code Changes (Lines 164-179):
```python
# OLD CODE:
if miles < 250 and daily_receipts > 280:
    penalty_multiplier = 0.80  # 20% penalty (conservative)
    base = vintage_multiply(base, penalty_multiplier)

# NEW CODE:
if miles < 300 and daily_receipts > 120:
    # Calculate penalty based on how inefficient the trip is
    miles_factor = max(0.2, (300 - miles) / 300)  # More penalty for lower miles
    receipts_factor = min(1.5, daily_receipts / 120)  # More penalty for higher daily receipts
    
    # Base penalty starts at 15% and can go up to 40% for worst cases
    penalty_factor = 0.15 + (miles_factor * receipts_factor * 0.25)
    penalty_factor = min(0.40, penalty_factor)  # Cap at 40% penalty
    
    penalty_multiplier = 1.0 - penalty_factor
    base = vintage_multiply(base, penalty_multiplier)
```

## Performance Results

### Target Case Improvements:
- **Case #115**: Error reduced from +$714.17 to +$371.04 (**48% improvement**)
- **Case #244**: Error reduced from +$584.66 to +$364.04 (**38% improvement**)
- **Case #434**: Error reduced from +$560.36 to +$282.98 (**49% improvement**)
- **Case #82**: Error reduced from +$510.03 to +$236.81 (**54% improvement**)
- **Case #83**: Error reduced from +$390.60 to +$261.02 (**33% improvement**)

### Overall Impact:
- **Original Score**: 9569.10
- **Patched Score**: 10886.10
- **Score Change**: +1317.00 (13.8% worse overall)

## Analysis
The patch successfully addressed the specific LOW_MILES_HIGH_RECEIPTS pattern, reducing the worst over-predictions by 33-54%. However, the overall score degraded because the penalty affected more cases than expected. The progressive penalty system correctly identifies inefficient trips but may be overly aggressive for borderline cases.

## Recommendation
This patch successfully solves the target error pattern but requires further tuning to minimize impact on overall score. Consider:
1. Reducing penalty factors by 10-20%
2. Tightening criteria to only target the most extreme cases
3. Adding compensating bonuses for efficient trips

## Files Modified
- `vintage_arithmetic.py`: Lines 164-179 (penalty logic)
- Created: `run.sh`, `test_cases.py`, `test_worst_cases.py`, `analyze_pattern.py`