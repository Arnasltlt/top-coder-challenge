# Challenge 4: Simple Linear Model Implementation

**Goal:** Create a first-pass model using simple linear regression to establish a quantitative baseline.

**Tasks:**
1.  Based on the insights from the data exploration, propose a simple linear model. The default assumption is `reimbursement = (A * days) + (B * miles) + (C * receipts)`.
2.  Using the `public_cases.json` data, determine the best-fit coefficients (A, B, C). You can use a statistical tool, a simple script to iterate and minimize error, or even manual estimation.
3.  Update the `run.sh` script to implement this linear calculation.
4.  Run `./eval.sh` to measure the performance of this model.

**Expected Outcome:** A `run.sh` script that implements a basic linear model and a new set of evaluation scores. This will serve as a much stronger baseline and reveal how much of the system's logic is non-linear. 