@echo off
:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Start the signal server in a new terminal window
start cmd /k "python p.py"

:: Start the interaction module in another new terminal window
start cmd /k "python m.py"
