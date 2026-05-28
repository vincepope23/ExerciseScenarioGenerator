#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment '.venv' does not exist." >&2
    exit 1
else
    echo "Virtual environment '.venv' found."
fi

# Check if the virtual environment is active
if [ -z "$VIRTUAL_ENV" ] || [ "$VIRTUAL_ENV" != "$(pwd)/.venv" ]; then
    echo "Error: Virtual environment '.venv' is not active." >&2
    exit 1
else
    echo "Virtual environment '.venv' is active."
fi

# Check if ipykernel 'krise' exists in .venv, if not install it
if ! .venv/bin/jupyter kernelspec list | grep -q "krise "; then
    echo "Installing ipykernel 'krise' in .venv..."
    if ! .venv/bin/python -m ipykernel install --user --name=krise --display-name="krise"; then
        echo "Error: Failed to install ipykernel 'krise'." >&2
        exit 1
    else
        echo "ipykernel 'krise' installed successfully in .venv."
    fi
else
    echo "ipykernel 'krise' already exists in .venv."
fi

# Start Jupyter Notebook
 .venv/bin/jupyter notebook