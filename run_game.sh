#!/bin/bash
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt --quiet
echo ""
echo "Starting Wordle Game..."
echo ""
python3 wordle/main.py