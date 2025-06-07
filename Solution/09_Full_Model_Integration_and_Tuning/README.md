# Challenge 9: Full Model Integration and Tuning

**Goal:** Combine all discovered logic into a final, cohesive model and fine-tune it for maximum accuracy.

**Tasks:**
1.  Review the logic implemented in `run.sh` from all previous steps (per diem, mileage, receipts, edge cases).
2.  Ensure that the different pieces of logic interact correctly. For example, does a per diem rule affect the mileage cap?
3.  Fine-tune the parameters of your model (e.g., reimbursement rates, thresholds for conditional logic) to maximize the "Exact matches" score on the `public_cases.json` dataset.
4.  This is an iterative process of making small adjustments and re-running `./eval.sh` until the score is as high as possible.

**Expected Outcome:** A highly accurate `run.sh` script where all individual rules are integrated and tuned to work together, closely replicating the output of the legacy system for the public dataset. 