#!/bin/bash
# top-level wrapper to hybrid model
DIR="$(dirname "$0")/Solution/Hybrid_Model"
python3 "$DIR/hybrid_run.py" "$@" 