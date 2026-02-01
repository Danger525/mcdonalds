
@echo off
echo Starting Flask Run...
set FLASK_APP=run.py
set FLASK_DEBUG=1
"c:\Users\subha\OneDrive\Desktop\menu\venv\Scripts\python.exe" -m flask run --host=0.0.0.0 --port=5000 > run_debug.log 2>&1
echo Run Finished with ErrorLevel %ERRORLEVEL%
type run_debug.log
