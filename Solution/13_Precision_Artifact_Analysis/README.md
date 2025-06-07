# Strategy 13: Precision Artifact Analysis

**ENGINEERING COMPLEXITY: MEDIUM**

## Core Hypothesis

What if the key to cracking this system lies in the **exact precision, rounding, and computational artifacts** from 1960s computing systems? The penny-level precision in expected outputs suggests the original system had very specific rounding behaviors.

## The Technical Insight

1960s systems had severe computational limitations:
- **Fixed-point arithmetic**: No floating-point, everything was integers or fixed decimals
- **Punched card precision**: Limited to specific decimal places
- **Mainframe rounding**: IBM systems had specific rounding algorithms
- **Currency calculations**: Always rounded to nearest cent using specific methods

## Strategy Details

### Phase 1: Rounding Behavior Analysis
```python
def analyze_rounding_patterns():
    # Analyze the cent digits of all expected outputs
    cent_patterns = []
    for case in public_cases:
        cents = int((case.expected * 100) % 100)
        cent_patterns.append(cents)
    
    # Look for non-uniform distribution
    # Random rounding: roughly equal distribution 0-99
    # System rounding: specific patterns (e.g., bias toward 0, 25, 50, 75)
    return analyze_distribution(cent_patterns)
```

### Phase 2: Vintage Computing Simulation
Model how 1960s systems actually performed calculations:

```python
def vintage_calculation(days, miles, receipts):
    # Simulate 1960s fixed-point arithmetic
    
    # Convert to "millidollars" (1/1000 of dollar) for calculation
    # This was common in 1960s financial systems
    days_millis = days * 1000
    miles_millis = miles * 1000  
    receipts_millis = int(receipts * 1000)
    
    # Perform calculation in millidollar space
    # Use integer arithmetic to avoid floating point
    base_millis = calculate_in_millis(days_millis, miles_millis, receipts_millis)
    
    # Apply 1960s-style rounding
    return vintage_round_to_cents(base_millis)

def vintage_round_to_cents(millidollars):
    # IBM System/360 used "round half to even" (banker's rounding)
    cents = millidollars // 10  # Convert millidollars to cents
    remainder = millidollars % 10
    
    if remainder < 5:
        return cents / 100.0
    elif remainder > 5:
        return (cents + 1) / 100.0
    else:  # remainder == 5
        # Banker's rounding: round to nearest even
        if cents % 2 == 0:
            return cents / 100.0
        else:
            return (cents + 1) / 100.0
```

### Phase 3: Precision Artifact Detection
Look for telltale signs of specific computational systems:

```python
def detect_precision_artifacts():
    artifacts = {
        'banker_rounding': 0,      # Round half to even
        'truncation': 0,           # Always round down
        'round_up': 0,             # Always round up
        'round_nearest': 0,        # Standard round half up
        'quarter_bias': 0,         # Bias toward .00, .25, .50, .75
        'fixed_point_overflow': 0  # Evidence of fixed-point arithmetic limits
    }
    
    for case in public_cases:
        expected_cents = int(case.expected * 100) % 100
        
        # Check for banker's rounding pattern
        if expected_cents % 2 == 0 and has_half_cent_input(case):
            artifacts['banker_rounding'] += 1
        
        # Check for quarter bias (common in old accounting systems)
        if expected_cents in [0, 25, 50, 75]:
            artifacts['quarter_bias'] += 1
            
        # Check for fixed-point overflow patterns
        if case.expected == int(case.expected):  # Whole dollar amounts
            artifacts['fixed_point_overflow'] += 1
    
    return artifacts
```

## Why This Might Be The Key

### Historical Technical Evidence
1. **IBM System/360 Rounding**: Used banker's rounding (round half to even)
2. **Fixed-Point Arithmetic**: All calculations in integer millidollars or centidollars
3. **Punched Card Limitations**: Only specific decimal precision allowed
4. **COBOL Currency Handling**: Specific PIC clauses for currency formatting

### Observable Patterns
- Expected outputs have exact penny precision
- No evidence of floating-point rounding errors
- Potential bias in cent digit distribution

## Advanced Precision Strategies

### Strategy A: Reverse-Engineer the Calculation Order
```python
def test_calculation_orders():
    # In 1960s systems, order of operations mattered due to rounding
    orders = [
        lambda d, m, r: ((d * coeff_d) + (m * coeff_m)) + (r * coeff_r),
        lambda d, m, r: (d * coeff_d) + ((m * coeff_m) + (r * coeff_r)),
        lambda d, m, r: ((d * coeff_d) + (r * coeff_r)) + (m * coeff_m),
    ]
    
    for order_func in orders:
        test_accuracy(order_func)
```

### Strategy B: Mainframe Arithmetic Simulation
```python
def ibm_360_arithmetic(value1, value2, operation):
    # Simulate IBM System/360 fixed-point decimal arithmetic
    # Convert to packed decimal format
    packed1 = to_packed_decimal(value1)
    packed2 = to_packed_decimal(value2)
    
    if operation == 'multiply':
        result = packed_multiply(packed1, packed2)
    elif operation == 'add':
        result = packed_add(packed1, packed2)
    
    return from_packed_decimal(result)
```

### Strategy C: Detect Systematic Precision Errors
```python
def find_systematic_precision_errors():
    # Look for cases where our model is off by exactly predictable amounts
    errors = []
    for case in public_cases:
        predicted = current_model(case.days, case.miles, case.receipts)
        error = case.expected - predicted
        errors.append(error)
    
    # Look for patterns in the errors
    # E.g., all errors are multiples of 0.05 (nickel rounding)
    # Or errors follow specific rounding patterns
    return analyze_error_patterns(errors)
```

## Implementation Files

- `vintage_arithmetic.py` - Simulate 1960s fixed-point calculations
- `rounding_analysis.py` - Analyze rounding patterns in expected outputs
- `precision_test.py` - Test different precision/rounding models
- `ibm_360_simulator.py` - Simulate specific mainframe arithmetic

## Breakthrough Indicators

1. **Cent Distribution Bias**: Non-uniform distribution of cent digits
2. **Rounding Pattern Match**: Our precision model matches expected outputs exactly
3. **Systematic Error Reduction**: Precision fixes eliminate systematic bias
4. **Historical Validation**: Patterns match known 1960s computing behavior

## Risk Assessment

- **Medium Risk**: Requires deep understanding of vintage computing
- **High Reward**: Could eliminate systematic precision errors
- **Implementation Complexity**: Moderate - need to simulate old arithmetic systems