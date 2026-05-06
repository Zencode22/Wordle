@echo off
title Wordle with Dynamic Letter Bag
echo Installing dependencies...
python -m pip install -r requirements.txt --quiet
echo.
echo Starting Wordle Game...
echo.
python wordle/main.py
pause