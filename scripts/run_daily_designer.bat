@echo off
setlocal

set PYTHON=C:\Users\itssh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe
set SCRIPT=C:\Users\itssh\SystemBuildPlanner_Executions\scripts\daily_system_designer.py
set LOG=C:\Users\itssh\SystemBuildPlanner_Executions\scripts\daily_run.log

echo [%date% %time%] Starting daily system designer >> %LOG%
"%PYTHON%" "%SCRIPT%" >> %LOG% 2>&1
echo [%date% %time%] Finished with exit code %errorlevel% >> %LOG%

endlocal
