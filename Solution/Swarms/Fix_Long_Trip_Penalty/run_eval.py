#!/usr/bin/env python3
"""
Run evaluation script from Team 13 directory
"""
import subprocess
import os
import sys

# Change to the parent directory where eval.sh is located
original_dir = os.getcwd()
eval_dir = "/Users/seima/8090/top-coder-challenge"

try:
    os.chdir(eval_dir)
    result = subprocess.run(["./eval.sh"], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)
    
    sys.exit(result.returncode)
    
finally:
    os.chdir(original_dir)