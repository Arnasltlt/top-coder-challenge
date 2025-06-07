#!/usr/bin/env python3

import json

def analyze_edge_case_triggers():
    """Analyze which edge cases are being triggered in worst performers."""
    
    with open("worst_cases_analysis.json", "r") as f:
        worst_cases = json.load(f)
    
    print("DETAILED ANALYSIS OF EDGE CASE TRIGGERS")
    print("="*60)
    
    for i, case in enumerate(worst_cases[:10]):  # Top 10
        inp = case["input"]
        days = inp["trip_duration_days"]
        miles = inp["miles_traveled"]
        receipts = inp["total_receipts_amount"]
        
        daily_spending = receipts / days
        miles_per_day = miles / days
        
        print(f"\nCase #{i+1} (ID: {case['case_id']})")
        print(f"  Input: {days} days, {miles} miles, ${receipts}")
        print(f"  Expected: ${case['expected']:.2f}, Predicted: ${case['predicted']:.2f}")
        print(f"  Daily spending: ${daily_spending:.2f}/day, Miles/day: {miles_per_day:.1f}")
        
        # Check which edge cases would trigger
        triggered_rules = []
        
        # EDGE CASE RULE 1: Long trip penalty
        if days >= 12 and daily_spending > 150:
            triggered_rules.append("RULE 1: Long trip + high spending (50% penalty)")
        
        # EDGE CASE RULE 2: Long trip with medium spending penalty  
        if days >= 12 and daily_spending >= 100 and daily_spending <= 150:
            triggered_rules.append("RULE 2: Long trip + medium-high spending (25% penalty)")
        
        # EDGE CASE RULE 3: Medium trip with very high spending penalty
        if days >= 8 and days <= 11 and daily_spending > 170:
            triggered_rules.append("RULE 3: Medium trip + very high spending (30% penalty)")
        
        # EDGE CASE RULE 4: "Sweet Spot Combo"
        if days == 5 and miles_per_day >= 180 and daily_spending < 100:
            triggered_rules.append("RULE 4: Sweet spot combo (15% bonus)")
        
        # EDGE CASE RULE 5: Short trip high mileage bonus
        if days <= 3 and miles_per_day > 400:
            triggered_rules.append("RULE 5: Short trip + high mileage (50% bonus)")
        
        # EDGE CASE RULE 6: Impossible travel scenarios
        if (days == 1 and miles > 800) or miles_per_day > 1000:
            triggered_rules.append("RULE 6: Impossible travel (75% penalty)")
        
        if triggered_rules:
            print("  TRIGGERED RULES:")
            for rule in triggered_rules:
                print(f"    - {rule}")
        else:
            print("  NO EDGE CASE RULES TRIGGERED")
            
        # Check receipt processing logic
        if daily_spending < 20:
            receipt_pct = "50%"
        elif daily_spending < 50:
            receipt_pct = "70%" 
        elif daily_spending < 120:
            receipt_pct = "100%"
        else:
            receipt_pct = "100% + 30% of excess over $120/day cap"
        
        print(f"  Receipt processing: {receipt_pct} (daily spending: ${daily_spending:.2f})")

if __name__ == "__main__":
    analyze_edge_case_triggers()