# Challenge 6: Mileage Rate Analysis

**Goal:** Determine the reimbursement rules for miles traveled.

**Tasks:**
1.  Focus on the `miles_traveled` input. Analyze its relationship with the reimbursement amount, controlling for the per diem and receipt logic developed so far.
2.  Determine the mileage reimbursement model:
    *   Is there a constant rate (e.g., $0.50 per mile)?
    *   Are there tiers? For example, is there a different rate for the first 100 miles versus subsequent miles?
    *   Does the mileage rate depend on the trip duration?
    *   Is there a maximum cap on mileage reimbursement?
3.  Update `run.sh` to implement the discovered mileage calculation rules.
4.  Run `./eval.sh` and assess the improvement in the model's accuracy.

**Expected Outcome:** A more accurate `run.sh` script that correctly models the contribution of miles traveled to the final reimbursement amount. 