import sys
import subprocess
import os

def get_script_path(script_name):
    """Gets the absolute path to a script in the same directory."""
    return os.path.join(os.path.dirname(__file__), script_name)

def main():
    if len(sys.argv) != 4:
        # This should not be reached if called from run.sh
        print("Usage: python ensemble_router.py <days> <miles> <receipts>", file=sys.stderr)
        sys.exit(1)

    try:
        days = int(sys.argv[1])
        miles = int(float(sys.argv[2]))
        receipts = float(sys.argv[3])
    except ValueError:
        print("Invalid input types.", file=sys.stderr)
        sys.exit(1)

    # Basic feature engineering
    # Avoid division by zero for trips with 0 days, though unlikely.
    daily_spending = receipts / days if days > 0 else receipts
    miles_per_day = miles / days if days > 0 else miles

    # Routing Logic
    chosen_expert = None
    expert_args = [] # To allow for future expert-specific flags

    # These thresholds are initial estimates based on the error analysis.
    # They are the primary knobs we will tune.
    INEFFICIENCY_SPENDING_THRESHOLD = 220 # High daily spend
    INEFFICIENCY_MILES_THRESHOLD = 75    # Low miles per day
    EFFICIENCY_SPENDING_THRESHOLD = 100   # Low daily spend
    EFFICIENCY_MILES_THRESHOLD = 400     # High miles per day

    if days > 7:
        chosen_expert = get_script_path("expert_long_trip.py")
    elif days == 1 and miles > 600:
        # Isolate the high-miles, 1-day anomaly specifically
        chosen_expert = get_script_path("expert_one_day_anomaly.py")
    elif daily_spending > INEFFICIENCY_SPENDING_THRESHOLD and miles_per_day < INEFFICIENCY_MILES_THRESHOLD:
        chosen_expert = get_script_path("expert_efficiency_paradox.py")
        expert_args.append("inefficient")
    elif daily_spending < EFFICIENCY_SPENDING_THRESHOLD and miles_per_day > EFFICIENCY_MILES_THRESHOLD:
        chosen_expert = get_script_path("expert_efficiency_paradox.py")
        expert_args.append("efficient")
    else:
        chosen_expert = get_script_path("expert_default.py")

    # Execute the chosen expert
    command = ["python", chosen_expert] + sys.argv[1:] + expert_args
    
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        # Pass through any errors from the expert
        print(f"Expert {chosen_expert} failed:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    
    # Print the expert's output to stdout
    print(result.stdout.strip())

if __name__ == "__main__":
    main()
