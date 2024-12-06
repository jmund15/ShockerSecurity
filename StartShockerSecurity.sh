#!/bin/bash

# Change to the specified directory
cd /home/jmund/ShockerSecurity || { echo "Directory not found!"; exit 1; }

git config --global user.name "jmund15"
git config --global user.email "jmundy2001@gmail.com"

# Pull any changes
git pull || { echo "Couldn't pull repo changes!"; exit 1; }
echo ""

# Activate the virtual environment
source venv/bin/activate || { echo "Virtual environment not found!"; exit 1; }

# Run the Python file
python backend/flaskApp.py || { echo "StartShockerSecurity.sh bash script exited with code 1!"; }

echo ""
echo ""
echo "Commiting logs..."

# Commit logs
git add .
git commit -am "updated logs"
git push

# Deactivate the virtual environment (optional)
deactivate
