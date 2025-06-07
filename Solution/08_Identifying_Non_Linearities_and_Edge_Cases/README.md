# Challenge 8: Identifying Non-Linearities and Edge Cases

**Goal:** Find and replicate the quirks, bugs, and special conditions of the legacy system.

**Tasks:**
1.  Analyze the public cases where your current model has the largest errors (the residuals).
2.  Look for patterns in these high-error cases. Are they associated with specific input values?
    *   `trip_duration_days` = 1, 7, or 14?
    *   `miles_traveled` = 0?
    *   `total_receipts_amount` being very high or very low?
3.  Formulate hypotheses for the rules governing these edge cases. This is where you are most likely to find the system's "bugs" or strange historical logic.
4.  Implement these rules as conditional logic (e.g., `if/else` statements) in your `run.sh` script.
5.  Iteratively test and refine this logic until the errors in these specific cases are minimized.

**Expected Outcome:** A `run.sh` script with conditional branches that handles the special cases, leading to a significant improvement in "Exact matches." 