#!/bin/bash
# Startup script for AI Will Executor POC

# Activate virtual environment
source .venv/bin/activate

# Run the app with PYTHONPATH set
PYTHONPATH=. python app/main.py
