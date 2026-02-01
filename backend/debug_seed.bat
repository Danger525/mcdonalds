
@echo off
echo Starting Seed...
"c:\Users\subha\OneDrive\Desktop\menu\venv\Scripts\python.exe" seed.py > seed_debug.log 2>&1
echo Seed Finished with ErrorLevel %ERRORLEVEL%
type seed_debug.log
