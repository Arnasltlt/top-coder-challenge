# Challenge 7: Receipt Processing Logic

**Goal:** Understand how the total amount from submitted receipts is handled in the calculation.

**Tasks:**
1.  Focus on the `total_receipts_amount` input.
2.  Analyze its impact on the final reimbursement, subtracting the effects of the per diem and mileage models you have already built.
3.  Investigate the following possibilities:
    *   Are receipts simply added to the total reimbursement?
    *   Is there a cap on the amount that can be claimed via receipts?
    *   Is the treatment of receipts dependent on other factors, like trip duration or miles traveled? (e.g., "receipts are only considered for trips longer than 3 days").
    *   Is only a certain percentage of the receipt amount reimbursed?
4.  Update the `run.sh` script with the logic for processing receipts.
5.  Evaluate the model's new performance.

**Expected Outcome:** An updated `run.sh` that correctly accounts for the role of submitted receipts in the reimbursement calculation. 