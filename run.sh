#!/bin/bash
# top-level wrapper to hybrid model (score ~7.9k)
DIR="$(dirname "$0")/Solution/Hybrid_Model"
python3 "$DIR/hybrid_run.py" "$@" 