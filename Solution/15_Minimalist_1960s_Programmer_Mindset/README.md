# Strategy 15: Minimalist 1960s Programmer Mindset

**ENGINEERING COMPLEXITY: LOW (Highly Speculative)**

## Core Hypothesis

Forget everything we know about modern programming. What if we think like a 1960s COBOL programmer with **3 months** to implement a reimbursement system on an IBM System/360? What would be the **simplest possible implementation** that could produce these results?

## The Revolutionary Mindset Shift

Instead of complex algorithms, think:
- **Tables and lookup logic** (punched card friendly)
- **Simple arithmetic** (addition, multiplication only)
- **Discrete categories** (no continuous functions)
- **Hardcoded special cases** (easier than general algorithms)
- **Sequential processing** (batch-oriented logic)

## Strategy Details

### Phase 1: 1960s Implementation Constraints
What would limit a 1960s programmer?

```cobol
WORKING-STORAGE SECTION.
01 REIMBURSEMENT-TABLES.
   05 PER-DIEM-TABLE.
      10 DAILY-RATE-1-DAY    PIC 9(3)V99 VALUE 85.00.
      10 DAILY-RATE-2-DAY    PIC 9(3)V99 VALUE 75.00.
      10 DAILY-RATE-3-PLUS   PIC 9(3)V99 VALUE 65.00.
   
   05 MILEAGE-TABLE.
      10 FIRST-500-MILES     PIC 9V999 VALUE 0.580.
      10 NEXT-500-MILES      PIC 9V999 VALUE 0.450.
      10 OVER-1000-MILES     PIC 9V999 VALUE 0.350.
   
   05 MEAL-ALLOWANCE-TABLE.
      10 LOW-MEAL-RATE       PIC 9(3)V99 VALUE 25.00.
      10 STANDARD-MEAL-RATE  PIC 9(3)V99 VALUE 45.00.
      10 HIGH-MEAL-RATE      PIC 9(3)V99 VALUE 65.00.
```

### Phase 2: Ultra-Simple Decision Tree
```python
def minimalist_1960s_logic(days, miles, receipts):
    # Step 1: Per-diem calculation (simplest possible)
    if days == 1:
        per_diem = 85
    elif days == 2:
        per_diem = 75 * 2
    else:
        per_diem = 65 * days
    
    # Step 2: Mileage calculation (three-tier table)
    if miles <= 500:
        mileage = miles * 0.58
    elif miles <= 1000:
        mileage = 500 * 0.58 + (miles - 500) * 0.45
    else:
        mileage = 500 * 0.58 + 500 * 0.45 + (miles - 1000) * 0.35
    
    # Step 3: Receipt handling (simple categories)
    daily_receipts = receipts / days
    if daily_receipts < 30:
        receipt_allowance = receipts * 0.5  # "Inadequate documentation"
    elif daily_receipts < 80:
        receipt_allowance = receipts * 0.85  # "Standard reimbursement"
    else:
        receipt_allowance = receipts * 0.65  # "Excessive spending penalty"
    
    # Step 4: Simple addition (no complex interactions)
    total = per_diem + mileage + receipt_allowance
    
    # Step 5: Hardcoded special cases (easier than algorithms)
    if days > 10:
        total = total * 0.9  # "Extended trip reduction"
    
    if miles > 2000:
        total = total + 100  # "Long distance bonus"
    
    return total
```

### Phase 3: Punched Card Logic
Think like processing batches of punched cards:

```python
def punched_card_processing(days, miles, receipts):
    # Card Column 1-2: Days (limited to 99)
    # Card Column 3-7: Miles (limited to 99999) 
    # Card Column 8-13: Receipts (dollars.cents)
    
    # Process in order cards would be sorted
    
    # Step 1: Validate card (reject invalid punches)
    if days > 30 or miles > 5000 or receipts > 9999:
        return 0  # "Invalid card - reject"
    
    # Step 2: Lookup table processing
    base_amount = lookup_base_amount(days)
    mile_amount = lookup_mile_amount(miles)
    meal_amount = lookup_meal_amount(receipts, days)
    
    # Step 3: Simple accumulation
    total = base_amount + mile_amount + meal_amount
    
    # Step 4: Apply standard adjustments
    if total > 2000:
        total = 2000  # "Maximum reimbursement limit"
    
    return total

def lookup_base_amount(days):
    # Hardcoded table (faster than calculation in 1960s)
    base_table = {
        1: 120, 2: 180, 3: 240, 4: 300, 5: 350,
        6: 400, 7: 440, 8: 480, 9: 520, 10: 560
    }
    if days <= 10:
        return base_table.get(days, 0)
    else:
        return 560 + (days - 10) * 35  # Linear extension
```

### Phase 4: "Good Enough" Engineering
1960s motto: "Make it work, don't make it perfect"

```python
def good_enough_solution(days, miles, receipts):
    # The simplest thing that could possibly work
    
    # Rule 1: Everyone gets a base amount
    base = 100
    
    # Rule 2: Add per day
    base += days * 50
    
    # Rule 3: Add per 100 miles  
    base += (miles // 100) * 25
    
    # Rule 4: Add fraction of receipts
    base += receipts * 0.4
    
    # Rule 5: A few hardcoded adjustments
    if days == 1 and miles > 500:
        base += 50  # "Day trip long distance bonus"
    
    if days > 7:
        base -= 30  # "Extended trip penalty"
    
    if receipts > 1000:
        base += 75  # "High receipt bonus"
    
    return base
```

## Why This Might Actually Work

### 1960s Programming Reality
1. **Limited Time**: 3-month deadline to implement entire system
2. **Limited Memory**: Every calculation had to be simple
3. **Limited Tools**: No debugging, no unit tests, no version control
4. **Business Pressure**: "Just make it work for the common cases"

### Occam's Razor Applied
- The simplest explanation is often correct
- 60-year-old system probably wasn't that sophisticated
- Complex edge cases might just be hardcoded special rules

## Implementation Strategy

### Step 1: Extreme Simplification
```python
def ultra_minimal_model(days, miles, receipts):
    # The absolute simplest model that could work
    return 80 + days * 45 + miles * 0.35 + receipts * 0.55
```

### Step 2: Add Minimal Complexity
```python
def slightly_less_minimal(days, miles, receipts):
    base = ultra_minimal_model(days, miles, receipts)
    
    # Add just the most obvious adjustments
    if days == 1:
        base += 20  # Day trip bonus
    
    if miles > 1000:
        base -= 50  # Long trip penalty
    
    return base
```

### Step 3: Test Iteratively
Add ONE simple rule at a time until performance stops improving.

## Files to Create

- `ultra_simple.py` - Absolute minimal implementation
- `cobol_style.py` - COBOL-like table lookup logic
- `punched_card.py` - Simulate punched card batch processing
- `good_enough.py` - "Just make it work" philosophy

## Success Criteria

The beauty of this approach: **If it works, it's probably right**
- Simple model performs surprisingly well
- Matches the "engineering pragmatism" of 1960s business software
- Explains complex behavior through simple rules

## Breakthrough Potential

This could be the ultimate breakthrough: discovering that decades of accumulated complexity comes from a fundamentally simple system with just a few hardcoded special cases.