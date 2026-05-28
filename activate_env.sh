#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d ".venv" ]; then
    echo "No .venv found. Creating virtual environment '.venv'..."
    python3 -m venv .venv
else
    echo "Virtual environment '.venv' exists already."
fi

# Activate the virtual environment (Linux)
if ! source .venv/bin/activate; then
    echo "Error: Failed to activate virtual environment '.venv'" >&2
    exit 1
fi

# Install/Update dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing/Updating dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Skipping dependency installation." >&2
fi

echo "Virtual environment '.venv' is activated."