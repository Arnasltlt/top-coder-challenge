#!/usr/bin/env python3
import subprocess

# Test the worst cases from our analysis
test_cases = [
    # Format: (days, miles, receipts, expected)
    (1, 989, 2196.84, 1439.17),    # High 1-day case
    (1, 822, 2170.53, 1374.91),    # High 1-day case  
    (4, 69, 2321.49, 322.00),      # Low activity high receipts
    (1, 123, 2076.65, 1171.68),    # Low miles high receipts
    (3, 1317.07, 476.87, 787.42),  # Very high mileage
    (1, 1082, 1809, 447),          # High miles high receipts low result
    (9, 1182, 1342, 2164),         # Good long trip
    (7, 1010, 1514, 2064),         # Good long trip
]

print("=== TESTING NEW MODEL V3 ===\n")

total_error = 0
for i, (days, miles, receipts, expected) in enumerate(test_cases):
    result = subprocess.run(['./run_v3.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    predicted = float(result.stdout.strip())
    error = abs(predicted - expected)
    total_error += error
    
    print(f"Case {i+1}: {days}d, {miles}mi, ${receipts:.0f}rec")
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
print(f"QUICK TEST MAE: ${mae:.2f}")
print(f"TARGET: <$25")

if mae < 25:
    print("🎉 READY FOR FULL TEST!")
elif mae < 50:
    print("🔧 GETTING CLOSER - NEEDS TUNING")
else:
    print("💀 STILL NEEDS WORK")