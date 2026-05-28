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

# Install/Update dependencies from pyproject.toml
if [ -f "pyproject.toml" ]; then
    echo "Installing/Updating dependencies from pyproject.toml..."
    pip install -e .
else
    echo "Warning: pyproject.toml not found. Skipping dependency installation." >&2
fi

echo "Virtual environment '.venv' is activated."