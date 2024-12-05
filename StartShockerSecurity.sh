#!/bin/bash

# Change to the specified directory
cd /home/jmund/ShockerSecurity || { echo "Directory not found!"; exit 1; }

# Activate the virtual environment
source venv/bin/activate || { echo "Virtual environment not found!"; exit 1; }

# Run the Python file
python backend/flaskApp.py || { echo "Python script failed!"; exit 1; }

# Deactivate the virtual environment (optional)
deactivate