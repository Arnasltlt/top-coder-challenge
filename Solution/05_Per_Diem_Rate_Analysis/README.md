# Challenge 5: Per Diem Rate Analysis

**Goal:** Isolate and model the reimbursement logic related to the trip duration.

**Tasks:**
1.  Focus on the `trip_duration_days` input. Using the hypotheses from Challenge 3 and the data from `public_cases.json`, investigate the existence of a "per diem" (daily) allowance.
2.  Test different models for the per diem rate:
    *   Is it a single flat rate for all days?
    *   Does the rate change after a certain number of days (e.g., a higher rate for the first week)?
    *   Are the first or last days treated differently, as suggested in the interviews?
3.  Modify the logic in `run.sh` to incorporate the most accurate per diem model you can find. You may need to subtract the effects of your baseline mileage and receipt model to isolate the per diem impact.
4.  Evaluate the change in performance.

**Expected Outcome:** An updated `run.sh` with a more sophisticated handling of trip duration and improved accuracy on the public test cases. 