# Synthesized Findings from Sub-Challenges

This document summarizes the key insights and discoveries made by the parallel AI agents working on the ACME Reimbursement System challenge.

### Challenge 1: Environment Setup & Baseline
- **Conclusion:** The evaluation environment (`eval.sh`) is working correctly.
- **Baseline Score:** An unmodified `run.sh` script produces **0 exact matches** and **0 close matches**. This was the expected starting point.

### Challenge 2: Data Exploration
- **Conclusion:** The reimbursement amount is correlated with all three inputs, but to different degrees.
- **Key Insight:** `total_receipts_amount` has the strongest correlation (0.704), making it the most significant predictor. `trip_duration_days` (0.514) and `miles_traveled` (0.432) are moderately correlated.

### Challenge 3: Interview Analysis
- **Conclusion:** The employee interviews, while contradictory, contain numerous valuable heuristics.
- **Key Insight:** Over 50 testable hypotheses were generated, covering per diem rates, mileage tiers, bonuses for specific trip lengths, receipt handling rules, and potential rounding quirks. This provides a rich roadmap for features to test.

### Challenge 4: Simple Linear Model
- **Conclusion:** A purely linear model can only explain a portion of the reimbursement logic.
- **Key Insight:** The best-fit linear model was determined to be:
  `reimbursement = 50.05 * days + 0.446 * miles + 0.383 * receipts + 266.71`
- **Performance:** This model achieved an **average error of ~$175**, proving that while it's a start, the true logic is highly non-linear.

### Challenge 5 & 6: Per Diem & Mileage Rate Analysis
- **Conclusion:** The per diem and mileage calculations are more complex than a simple flat rate.
- **Key Insights:**
    - **Per Diem:** A base rate of **~$110/day** was identified, which is more accurate than the $100/day mentioned in interviews.
    - **Mileage:** While tiered models were tested, the simple linear rate of **$0.446 per mile** from the regression model proved most effective, suggesting the mileage component is surprisingly straightforward.

### Challenge 7: Receipt Processing Logic
- **Conclusion:** The receipt handling is the most complex and non-linear part of the system, based on spending behavior. This is the most significant finding so far.
- **Key Insight:** The system calculates a **daily spending rate** (`total_receipts_amount / trip_duration_days`) and applies rules:
    - **Low Spending (< $20/day):** Penalized, with only ~50% of receipt value being reimbursed.
    - **Medium Spending ($50 - $120/day):** This is the "sweet spot," receiving 100% reimbursement.
    - **High Spending (> $120/day):** Capped, with diminishing returns. Only a small fraction (~30%) of the amount over the daily cap is reimbursed.

### Overall Synthesis & Next Steps
The initial exploration has been incredibly fruitful. We have moved from a simple linear approximation to a sophisticated, behavior-based model. The core formula now seems to involve a base per diem (~$110/day) and a linear mileage rate (~$0.446/mile), but the receipt calculation is the secret sauce.

The remaining errors are likely hidden in **Challenge 8: Identifying Non-Linearities and Edge Cases**. The current model still struggles with very long trips and very high receipt values, suggesting there are further caps or special rules we have yet to discover. The next step is to analyze the biggest remaining errors from our current model to find these final hidden quirks. 