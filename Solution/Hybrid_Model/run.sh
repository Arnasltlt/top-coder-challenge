#!/bin/bash
# Hybrid model runner: baseline + residual lookup
SCRIPT_DIR="$(dirname "$0")"
python3 "$SCRIPT_DIR/hybrid_run.py" "$@" 