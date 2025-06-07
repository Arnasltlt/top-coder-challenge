# Strategy 14: Employee Classification Inference

**ENGINEERING COMPLEXITY: MEDIUM**

## Core Hypothesis

What if the seemingly random variations in reimbursement amounts actually represent **different employee classifications** with different reimbursement policies? The 1960s context suggests rigid hierarchical structures and role-based policies.

## The Business Logic Insight

In the 1960s, companies had very stratified employee classifications:
- **Executives**: Unlimited or high-limit reimbursements
- **Senior Sales**: Standard business travel allowances  
- **Junior Sales**: Restricted budgets, closer oversight
- **Technical Staff**: Different rates for different types of travel
- **Regional Managers**: Territory-specific allowances

## Strategy Details

### Phase 1: Reverse-Engineer Employee Types
Use unsupervised clustering to identify distinct employee classifications:

```python
def infer_employee_types():
    # Create feature vectors for each case
    features = []
    for case in public_cases:
        features.append([
            case.days,
            case.miles, 
            case.receipts,
            case.receipts / case.days,     # Daily spending
            case.miles / case.days,        # Daily mileage  
            case.expected / case.days,     # Daily reimbursement
            case.expected / case.receipts  # Reimbursement ratio
        ])
    
    # Use K-means clustering to find employee types
    from sklearn.cluster import KMeans
    
    # Test different numbers of employee types (3-8 seems reasonable)
    for n_types in range(3, 9):
        kmeans = KMeans(n_clusters=n_types)
        employee_types = kmeans.fit_predict(features)
        
        # Analyze each cluster for distinct reimbursement patterns
        analyze_employee_clusters(employee_types, public_cases)
```

### Phase 2: 1960s Employee Hierarchy Simulation
Model realistic 1960s corporate hierarchies:

```python
def classify_by_1960s_hierarchy(days, miles, receipts):
    daily_spending = receipts / days
    daily_miles = miles / days
    
    # Executive Class: High-spend, low mileage (flying first class)
    if daily_spending > 200 and daily_miles < 100:
        return "EXECUTIVE"
    
    # Senior Sales: High mileage, moderate spending (traveling salesmen)
    elif daily_miles > 300 and daily_spending > 80:
        return "SENIOR_SALES"
    
    # Junior Sales: Moderate everything (constrained budgets)
    elif daily_miles < 300 and daily_spending < 120:
        return "JUNIOR_SALES"
    
    # Technical Staff: Low mileage, low spending (local calls)
    elif daily_miles < 150 and daily_spending < 80:
        return "TECHNICAL"
    
    # Regional Managers: Balanced spending and travel
    else:
        return "REGIONAL_MGR"

def get_employee_multipliers(employee_type):
    multipliers = {
        "EXECUTIVE": {
            "base_rate": 150,     # High per-diem
            "mile_rate": 0.12,    # Low mileage (flying)
            "receipt_rate": 0.85, # High receipt reimbursement
            "bonus": 50           # Executive bonus
        },
        "SENIOR_SALES": {
            "base_rate": 120,
            "mile_rate": 0.58,    # Standard IRS rate
            "receipt_rate": 0.70,
            "bonus": 0
        },
        "JUNIOR_SALES": {
            "base_rate": 90,      # Lower per-diem
            "mile_rate": 0.45,    # Reduced mileage rate
            "receipt_rate": 0.60, # Lower reimbursement
            "bonus": 0
        },
        "TECHNICAL": {
            "base_rate": 80,
            "mile_rate": 0.40,
            "receipt_rate": 0.75, # Good meal reimbursement
            "bonus": 0
        },
        "REGIONAL_MGR": {
            "base_rate": 130,
            "mile_rate": 0.52,
            "receipt_rate": 0.72,
            "bonus": 25
        }
    }
    return multipliers.get(employee_type, multipliers["JUNIOR_SALES"])
```

### Phase 3: Territory/Department Logic
Model geographical or departmental variations:

```python
def infer_territory_from_patterns(case_index, miles, days):
    # Use case index as proxy for different territories/departments
    territory = case_index % 5  # Assume 5 territories
    
    territory_adjustments = {
        0: 1.05,  # West Coast (higher costs)
        1: 0.95,  # Midwest (lower costs) 
        2: 1.10,  # Northeast (highest costs)
        3: 0.90,  # South (lowest costs)
        4: 1.00   # Central (baseline)
    }
    
    return territory_adjustments[territory]
```

## Why This Could Be The Breakthrough

### Historical Business Context
1. **Rigid Hierarchies**: 1960s companies had very structured employee levels
2. **Role-Based Policies**: Different reimbursement rules for different roles
3. **Geographic Variations**: Territory-based cost-of-living adjustments
4. **Department Budgets**: Engineering vs Sales vs Executive travel budgets

### Observable Evidence
- High variation in reimbursement rates for similar trip profiles
- Some cases show "premium" reimbursement rates
- Others show "constrained" reimbursement patterns

## Advanced Classification Strategies

### Strategy A: Spending Behavior Analysis
```python
def analyze_spending_behaviors():
    behaviors = {
        'frugal': [],      # Low receipts relative to days/miles
        'standard': [],    # Normal spending patterns
        'premium': [],     # High spending, likely executives
        'constrained': []  # Artificially low spending (budget limits)
    }
    
    for case in public_cases:
        spending_ratio = case.receipts / (case.days * case.miles + 1)
        reimbursement_ratio = case.expected / case.receipts
        
        if spending_ratio < 0.1 and reimbursement_ratio > 1.2:
            behaviors['frugal'].append(case)
        elif spending_ratio > 0.5 and reimbursement_ratio > 1.0:
            behaviors['premium'].append(case)
        elif reimbursement_ratio < 0.8:
            behaviors['constrained'].append(case)
        else:
            behaviors['standard'].append(case)
    
    return behaviors
```

### Strategy B: Expense Pattern Recognition
```python
def detect_expense_patterns():
    patterns = {
        'round_numbers': [],      # Receipts end in .00 (per-diem limits)
        'detailed_receipts': [],  # Precise amounts (actual receipts)
        'policy_limits': [],      # Receipts hit exact policy maximums
        'reimbursement_caps': []  # Expected amounts hit caps
    }
    
    for case in public_cases:
        receipt_cents = int(case.receipts * 100) % 100
        expected_cents = int(case.expected * 100) % 100
        
        # Round number receipts suggest per-diem policies
        if receipt_cents == 0:
            patterns['round_numbers'].append(case)
        
        # Receipts ending in common policy amounts
        if case.receipts % 25 == 0 or case.receipts % 50 == 0:
            patterns['policy_limits'].append(case)
    
    return patterns
```

## Implementation Files

- `employee_clustering.py` - Unsupervised classification of employee types
- `hierarchy_simulation.py` - Model 1960s corporate hierarchies
- `territory_analysis.py` - Geographic/departmental variations
- `spending_behavior.py` - Analyze spending pattern classifications

## Success Indicators

1. **Distinct Clusters**: Clear separation of cases into logical employee types
2. **Pattern Consistency**: Each cluster shows consistent reimbursement behavior
3. **Business Logic Match**: Classifications align with 1960s corporate structures
4. **Improved Accuracy**: Type-specific models outperform general model

## Breakthrough Scenarios

- **Scenario A**: Cases clearly separate into 4-6 employee types with distinct policies
- **Scenario B**: Geographic/territorial patterns explain regional variation
- **Scenario C**: Combination of employee type + territory explains most variation