#!/usr/bin/env python3
import subprocess

# Test the critical pattern cases I identified
test_cases = [
    # Format: (days, miles, receipts, expected, description)
    (1, 1082, 1809, 446.94, "CRITICAL: High miles + med-high receipts = penalty"),
    (1, 989, 2196.84, 1439.17, "High miles + very high receipts = good"),
    (1, 822, 2170.53, 1374.91, "High miles + very high receipts = good"),
    (1, 815, 98, 539.36, "High miles + low receipts = moderate"),
    (1, 893, 20, 570.71, "High miles + very low receipts = moderate"),
    (1, 420, 2273.60, 1220.35, "Moderate miles + very high receipts = good"),
    (1, 123, 2076.65, 1171.68, "Low miles + very high receipts = decent"),
    (7, 1010, 1514, 2064, "Good long trip pattern"),
]

print("=== TESTING BRACKET-BASED MODEL V4 ===\n")

total_error = 0
critical_case_error = 0

for i, (days, miles, receipts, expected, description) in enumerate(test_cases):
    result = subprocess.run(['./run_v4.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    predicted = float(result.stdout.strip())
    error = abs(predicted - expected)
    total_error += error
    
    if i == 0:  # Critical case
        critical_case_error = error
    
    print(f"Case {i+1}: {days}d, {miles}mi, ${receipts:.0f}rec")
    print(f"  {description}")
    print(f"  Expected: ${expected:.2f}, Predicted: ${predicted:.2f}, Error: ${error:.2f}")
    
    # Check if this is much better
    if error < 25:
        print(f"  🎉 EXCELLENT (error < $25)")
    elif error < 50:
        print(f"  ✅ GOOD (error < $50)")
    elif error < 100:
        print(f"  ⚠️  OK (error < $100)")
    else:
        print(f"  ❌ BAD (error > $100)")
    print()

mae = total_error / len(test_cases)
print(f"CRITICAL TEST MAE: ${mae:.2f}")
print(f"CRITICAL CASE ERROR: ${critical_case_error:.2f}")
print(f"TARGET: <$25")

if mae < 25:
    print("🎉 BREAKTHROUGH! READY FOR FULL TEST!")
elif mae < 50:
    print("🔧 MAJOR IMPROVEMENT - GETTING CLOSE")
elif mae < 100:
    print("⚠️ SOME PROGRESS")
else:
    print("💀 STILL BROKEN")