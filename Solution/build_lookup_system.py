#!/usr/bin/env python3
import json

print("🔥 BUILDING EMPIRICAL LOOKUP SYSTEM 🔥")
print("Like a real 60-year-old legacy system would have!")

# Load training data
with open('../public_cases.json', 'r') as f:
    cases = json.load(f)

print(f"Analyzing {len(cases)} training cases...")

# Create empirical buckets based on actual data patterns
buckets = {}

for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    # Create bucket key based on ranges (like a legacy system would)
    miles_bucket = int(miles // 100) * 100  # Round to nearest 100
    receipts_bucket = int(receipts // 250) * 250  # Round to nearest 250
    
    bucket_key = (days, miles_bucket, receipts_bucket)
    
    if bucket_key not in buckets:
        buckets[bucket_key] = []
    
    buckets[bucket_key].append(expected)

# Calculate averages for each bucket
bucket_averages = {}
for key, values in buckets.items():
    bucket_averages[key] = sum(values) / len(values)

print(f"Created {len(bucket_averages)} empirical buckets")

# Find buckets with multiple cases (more reliable)
reliable_buckets = {k: v for k, v in bucket_averages.items() if len(buckets[k]) >= 2}
print(f"Found {len(reliable_buckets)} reliable buckets (2+ cases)")

# Show some examples
print("\nSample buckets:")
for i, (key, avg) in enumerate(list(bucket_averages.items())[:10]):
    days, miles_bucket, receipts_bucket = key
    count = len(buckets[key])
    print(f"  {days}d, {miles_bucket}mi, ${receipts_bucket}rec → ${avg:.0f} (n={count})")

# Save the lookup table
lookup_data = {
    'bucket_averages': {str(k): v for k, v in bucket_averages.items()},
    'bucket_counts': {str(k): len(v) for k, v in buckets.items()}
}

with open('empirical_lookup.json', 'w') as f:
    json.dump(lookup_data, f, indent=2)

print(f"\n✅ Lookup system saved to empirical_lookup.json")
print("Ready to build the lookup-based prediction system!")