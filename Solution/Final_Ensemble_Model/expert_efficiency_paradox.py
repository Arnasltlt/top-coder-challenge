#!/usr/bin/env python3
"""
Team 13: Precision Artifact Analysis - Vintage Arithmetic Module
This is the EXPERT for the EFFICIENCY PARADOX.
"""
import sys
import math

def vintage_multiply(a, b, precision_decimals=2):
    multiplier = 10 ** precision_decimals
    a_fixed = int(round(a * multiplier))
    b_fixed = int(round(b * multiplier))
    result_fixed = a_fixed * b_fixed
    result = result_fixed / (multiplier * multiplier)
    return vintage_round(result, precision_decimals)

def vintage_add(a, b, precision_decimals=2):
    multiplier = 10 ** precision_decimals
    a_fixed = int(round(a * multiplier))
    b_fixed = int(round(b * multiplier))
    result_fixed = a_fixed + b_fixed
    result = result_fixed / multiplier
    return vintage_round(result, precision_decimals)

def vintage_round(value, precision_decimals=2):
    multiplier = 10 ** precision_decimals
    scaled = value * multiplier
    fractional = scaled - int(scaled)
    if abs(fractional) < 0.5:
        return int(scaled) / multiplier
    elif abs(fractional) > 0.5:
        if scaled >= 0:
            return (int(scaled) + 1) / multiplier
        else:
            return (int(scaled) - 1) / multiplier
    else:
        integer_part = int(scaled)
        if integer_part % 2 == 0:
            return integer_part / multiplier
        else:
            if scaled >= 0:
                return (integer_part + 1) / multiplier
            else:
                return (integer_part - 1) / multiplier

def simulate_cobol_pic_clause(value, integer_digits=6, decimal_digits=2):
    max_value = (10 ** integer_digits) - (1.0 / (10 ** decimal_digits))
    if abs(value) > max_value:
        return max_value if value > 0 else -max_value
    multiplier = 10 ** decimal_digits
    return round(value * multiplier) / multiplier

def vintage_calculation(days, miles, receipts, mode=None):
    """
    Main calculation for the efficiency paradox expert.
    """
    coeff_days = simulate_cobol_pic_clause(50.0, 3, 2)
    coeff_miles = simulate_cobol_pic_clause(0.45, 0, 3)
    coeff_receipts = simulate_cobol_pic_clause(0.38, 0, 3)
    base_constant = simulate_cobol_pic_clause(270.0, 3, 2)
    
    days_term = vintage_multiply(days, coeff_days)
    miles_term = vintage_multiply(miles, coeff_miles)
    receipts_term = vintage_multiply(receipts, coeff_receipts)
    
    base = vintage_add(base_constant, days_term)
    base = vintage_add(base, miles_term)
    base = vintage_add(base, receipts_term)

    # --- EXPERT LOGIC FOR EFFICIENCY PARADOX ---
    if mode:
        daily_spending = receipts / days if days > 0 else receipts
        miles_per_day = miles / days if days > 0 else miles
        adjustment = 0.0

        if mode == 'inefficient':
            spending_excess = max(0, daily_spending - 200)
            penalty_factor = 1.5
            penalty = -((spending_excess * penalty_factor) * days)
            adjustment = vintage_add(adjustment, penalty)

            if miles_per_day < 50:
                mileage_penalty = (50 - miles_per_day) * -5.0
                adjustment = vintage_add(adjustment, mileage_penalty)

        elif mode == 'efficient':
            efficiency_bonus_factor = 0.20
            bonus = vintage_multiply(miles_term, efficiency_bonus_factor)
            adjustment = vintage_add(adjustment, bonus)
        
        base = vintage_add(base, adjustment)
    # --- END OF EXPERT LOGIC ---

    # General day-based bonuses can still apply
    if days == 5:
        bonus = vintage_multiply(base, 0.14)
        base = vintage_add(base, bonus)
    elif days == 6:
        bonus = vintage_multiply(base, 0.17)
        base = vintage_add(base, bonus)
    
    max_value = simulate_cobol_pic_clause(9999.99, 4, 2)
    min_value = simulate_cobol_pic_clause(0.01, 0, 2)
    
    if base > max_value:
        base = max_value
    elif base < min_value:
        base = min_value
    
    # Final rounding to two decimal places, ensuring it's not bankers rounding
    final_amount = math.ceil(base * 100) / 100
    return final_amount


def main():
    """Main function to run the script from the command line."""
    if len(sys.argv) < 4:
        print("Usage: python3 expert_efficiency_paradox.py <days> <miles> <receipts> [mode]")
        sys.exit(1)
    
    try:
        days = int(sys.argv[1])
        miles = int(float(sys.argv[2]))
        receipts = float(sys.argv[3])
        mode = sys.argv[4] if len(sys.argv) > 4 else None
    except (ValueError, IndexError):
        print("Invalid or missing arguments.", file=sys.stderr)
        sys.exit(1)

    result = vintage_calculation(days, miles, receipts, mode=mode)
    
    print(f"{result:.2f}")

if __name__ == "__main__":
    main() 